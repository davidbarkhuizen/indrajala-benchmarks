"""
Validate the archive (FORMAT.md): every record's files, every profile snapshot against its schema,
every golden file against its note, INDEX.md, and, given a base commit, that nothing merged changed.

    python tools/check_archive.py --indrajala-ml PATH [--base REF] [--reproduce]

PATH is a clone of indrajala-ml with its history: profile schemas are read from it at the commit
each profile was captured at, and --reproduce re-renders every run's reports with its checked-out
scripts/ab.py and compares them with the stored ones. Prints one line per problem and exits 1 if
there are any.
"""

import argparse
import gzip
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
TOP_LEVEL = {".git", ".github", ".gitignore", "README.md", "FORMAT.md", "INDEX.md", "LICENSE", "tools"}
RECORD_DIRS = ("machines", "golden", "runs")
FORMAT = 1
CAPTURED = re.compile(r"^\d{8}T\d{6}Z(-\d+)?-profile\.json$")
RUN_DIR = re.compile(r"^\d{4}-\d{2}-\d{2}-[A-Za-z0-9._-]+$")
GOLDEN = re.compile(r"^(\d{4}-\d{2}-\d{2})-([0-9a-f]{7})\.(json\.gz|md)$")
INDEX_LINE = re.compile(r"^- (\d{4}-\d{2}-\d{2}) · ([^ ]+) · (run|golden|profile) · \[([^\]]+)\]\(([^)]+)\) · (.+)$")
RUN_FIELDS = {
    "format",
    "kind",
    "host",
    "name",
    "archived_at",
    "reason",
    "replaces",
    "profile",
    "profile_source",
    "formats",
    "rendered_by",
    "files",
    "reports",
}
GOLDEN_FIELDS = {
    "format",
    "kind",
    "host",
    "date",
    "commit",
    "crate",
    "reason",
    "note",
    "previous",
    "added",
    "moved",
    "removed",
    "networks",
    "sha256",
    "profile",
    "replaces",
}
RAW_SUFFIXES = (".json", ".stdout", ".stderr")


class Checker:
    def __init__(self, indrajala_ml: Path) -> None:
        self.indrajala_ml = indrajala_ml
        self.problems: list[str] = []
        self.index_entries: dict[str, tuple[str, str, str]] = {}  # path -> (date, host, kind)
        self.schemas: dict[object, tuple[str, dict[str, Any]] | None] = {}  # by schema_version

    def problem(self, where: Path | str, text: str) -> None:
        path = where.relative_to(ROOT) if isinstance(where, Path) else where
        self.problems.append(f"{path}: {text}")

    def json(self, path: Path) -> Any:
        try:
            return json.loads(path.read_text())
        except (OSError, ValueError) as error:
            self.problem(path, f"not readable JSON ({error})")
            return None

    # ---- profiles

    def schema_for(self, version: object) -> tuple[str, dict[str, Any]] | None:
        """(commit, schema) of the newest machine profile schema in indrajala-ml's history whose
        schema_version is version: a profile migrated to a newer version keeps its capture time."""
        if version not in self.schemas:
            self.schemas[version] = None
            log = self.git("log", "--format=%H", "--", "*machine_profile.schema.json")
            for commit in log.splitlines():
                paths = [
                    p
                    for p in self.git("ls-tree", "-r", "--name-only", commit).splitlines()
                    if p.endswith("machine_profile.schema.json")
                ]
                if len(paths) != 1:
                    continue
                schema = json.loads(self.git("show", f"{commit}:{paths[0]}"))
                if schema.get("properties", {}).get("schema_version", {}).get("const") == version:
                    self.schemas[version] = (commit, schema)
                    break
        return self.schemas[version]

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(self.indrajala_ml), *args], capture_output=True, text=True, check=True
        ).stdout

    def check_profile(self, path: Path) -> None:
        if not CAPTURED.match(path.name):
            self.problem(path, "not named <YYYYMMDDTHHMMSSZ>[-N]-profile.json")
        profile = self.json(path)
        if not isinstance(profile, dict):
            return
        state = profile.get("state", {})
        if state.get("hostname") != path.parent.name:
            self.problem(path, f"state.hostname {state.get('hostname')!r} isn't its directory's")
        stamp = re.sub(r"[-:]", "", str(state.get("captured_at", "")))
        if not path.name.startswith(stamp):
            self.problem(path, f"name doesn't match state.captured_at {state.get('captured_at')!r}")
        self.index_entries[str(path.relative_to(ROOT))] = (
            str(state.get("captured_at"))[:10],
            path.parent.name,
            "profile",
        )
        found = self.schema_for(profile.get("schema_version"))
        if found is None:
            self.problem(
                path, f"no machine profile schema in indrajala-ml with schema_version {profile.get('schema_version')!r}"
            )
            return
        commit, schema = found
        import jsonschema

        try:
            jsonschema.validate(profile, schema, cls=jsonschema.Draft202012Validator)
        except jsonschema.ValidationError as error:
            self.problem(path, f"doesn't match the schema at {commit[:7]}: {error.message}")

    # ---- runs

    def check_run(self, run: Path) -> None:
        if not RUN_DIR.match(run.name):
            self.problem(run, "not named <YYYY-MM-DD>-<name>")
        record = self.json(run / "record.json")
        manifest = self.json(run / "manifest.json")
        if not isinstance(record, dict) or not isinstance(manifest, dict):
            return
        if set(record) != RUN_FIELDS:
            self.problem(run / "record.json", f"fields {sorted(set(record) ^ RUN_FIELDS)} missing or unknown")
            return
        if record["format"] != FORMAT or record["kind"] != "run":
            self.problem(run / "record.json", "not a format 1 run record")
        if record["host"] != run.parent.name or record["name"] != run.name:
            self.problem(run / "record.json", "host or name doesn't match its path")
        self.check_cited(run / "record.json", record, run.parent.name)
        if record["profile_source"] not in ("checked", "assigned"):
            self.problem(run / "record.json", f"profile_source {record['profile_source']!r}")
        if record["formats"].get("ab_manifest") != manifest.get("version"):
            self.problem(run / "record.json", "formats.ab_manifest isn't the manifest's version")
        stems = {p["stem"] for p in manifest.get("passes", [])} | {"smoke-old", "smoke-new"}
        allowed = {"manifest.json", "progress.jsonl"} | {stem + suffix for stem in stems for suffix in RAW_SUFFIXES}
        reports = {"brief.txt", "report.md"} | ({"pooled.md"} if _is_aa(manifest) else set())
        if sorted(reports) != record["reports"]:
            self.problem(run / "record.json", f"reports {record['reports']} should be {sorted(reports)}")
        if "manifest.json" not in record["files"] or not set(record["files"]) <= allowed:
            self.problem(
                run / "record.json", f"files outside what ab.py writes: {sorted(set(record['files']) - allowed)}"
            )
        on_disk = {p.name for p in run.iterdir()}
        expected = set(record["files"]) | reports | {"record.json"}
        if on_disk != expected:
            self.problem(run, f"files on disk differ from record.json: {sorted(on_disk ^ expected)}")
        if any(p.is_symlink() or p.is_dir() for p in run.iterdir()):
            self.problem(run, "holds a symlink or a directory")
        self.index_entries[str(run.relative_to(ROOT))] = (run.name[:10], run.parent.name, "run")

    def check_cited(self, where: Path, record: dict[str, Any], host: str) -> None:
        """The record's profile snapshot exists and is this host's; a replaced record exists."""
        profile = ROOT / str(record["profile"])
        if not (profile.parent.parent.name == "machines" and profile.parent.name == host and profile.is_file()):
            self.problem(where, f"profile {record['profile']!r} isn't a snapshot of host {host}")
        if record["replaces"] is not None and not (ROOT / str(record["replaces"])).exists():
            self.problem(where, f"replaces {record['replaces']!r}, which doesn't exist")

    def reproduce(self, run: Path) -> None:
        manifest = self.json(run / "manifest.json")
        if not isinstance(manifest, dict):
            return
        ab = self.indrajala_ml / "scripts/ab.py"
        env = {"PYTHONPATH": str(self.indrajala_ml), "PATH": "/usr/bin:/bin"}
        brief = subprocess.run(
            [sys.executable, str(ab), "report", str(run), "--brief"],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
        if brief.returncode:
            self.problem(run, f"ab.py report failed: {brief.stderr.strip()[-300:]}")
            return
        if brief.stdout != (run / "brief.txt").read_text():
            self.problem(run / "brief.txt", "doesn't reproduce with indrajala-ml's current ab.py")
        rendered = {"report.md": "--md"} | ({"pooled.md": "--pooled"} if _is_aa(manifest) else {})
        with tempfile.TemporaryDirectory() as tmp:
            for name, option in rendered.items():
                out = Path(tmp) / name
                subprocess.run(
                    [sys.executable, str(ab), "report", str(run), option, str(out), "--brief"],
                    capture_output=True,
                    env=env,
                    check=False,
                )
                if not out.is_file() or out.read_text() != (run / name).read_text():
                    self.problem(run / name, "doesn't reproduce with indrajala-ml's current ab.py")

    # ---- golden runs

    def check_golden(self, host_dir: Path) -> None:
        stems: dict[str, set[str]] = {}
        for path in host_dir.iterdir():
            match = GOLDEN.match(path.name)
            if not match:
                self.problem(path, "not named <date>-<commit7>.json.gz or .md")
                continue
            stems.setdefault(f"{match[1]}-{match[2]}", set()).add(match[3])
        for stem, suffixes in sorted(stems.items()):
            if suffixes != {"json.gz", "md"}:
                self.problem(host_dir / stem, "needs both .json.gz and .md")
                continue
            note = (host_dir / f"{stem}.md").read_text()
            blocks = re.findall(r"```json\n(.*?)\n```", note, re.DOTALL)
            if not blocks:
                self.problem(host_dir / f"{stem}.md", "no fenced json block")
                continue
            meta = json.loads(blocks[-1])
            where = host_dir / f"{stem}.md"
            if set(meta) != GOLDEN_FIELDS:
                self.problem(where, f"fields {sorted(set(meta) ^ GOLDEN_FIELDS)} missing or unknown")
                continue
            if meta["format"] != FORMAT or meta["kind"] != "golden" or meta["host"] != host_dir.name:
                self.problem(where, "not a format 1 golden record of this host")
            if f"{meta['date']}-{meta['commit'][:7]}" != stem:
                self.problem(where, "date or commit doesn't match its name")
            if meta["reason"] not in ("material", "new-functionality"):
                self.problem(where, f"reason {meta['reason']!r}")
            if meta["reason"] == "new-functionality" and (meta["moved"] or meta["removed"]):
                self.problem(where, "new-functionality, but entries moved or were removed")
            if meta["previous"] is not None and not (ROOT / meta["previous"]).is_file():
                self.problem(where, f"previous {meta['previous']!r} doesn't exist")
            self.check_cited(where, meta, host_dir.name)
            raw = gzip.decompress((host_dir / f"{stem}.json.gz").read_bytes())
            if hashlib.sha256(raw).hexdigest() != meta["sha256"]:
                self.problem(host_dir / f"{stem}.json.gz", "sha256 doesn't match its note")
            elif len(json.loads(raw)) != meta["networks"]:
                self.problem(host_dir / f"{stem}.json.gz", "entry count doesn't match its note")
            self.index_entries[str((host_dir / f"{stem}.json.gz").relative_to(ROOT))] = (
                meta["date"],
                host_dir.name,
                "golden",
            )

    # ---- the whole archive

    def check_layout(self) -> None:
        for path in ROOT.iterdir():
            if path.name not in TOP_LEVEL | set(RECORD_DIRS):
                self.problem(path, "not part of the archive's layout")
        for kind in RECORD_DIRS:
            base = ROOT / kind
            for host_dir in sorted(base.iterdir()) if base.is_dir() else []:
                if not host_dir.is_dir():
                    self.problem(host_dir, "expected a host directory")
                elif kind == "machines":
                    for path in sorted(host_dir.iterdir()):
                        self.check_profile(path)
                elif kind == "runs":
                    for run in sorted(host_dir.iterdir()):
                        self.check_run(run) if run.is_dir() else self.problem(run, "expected a run directory")
                else:
                    self.check_golden(host_dir)

    def check_index(self) -> None:
        lines = [line for line in (ROOT / "INDEX.md").read_text().splitlines() if line.startswith("- ")]
        listed: dict[str, int] = {}
        dates: list[str] = []
        for line in lines:
            match = INDEX_LINE.match(line)
            if not match:
                self.problem("INDEX.md", f"malformed line: {line}")
                continue
            path = match[5]
            listed[path] = listed.get(path, 0) + 1
            dates.append(match[1])
            entry = self.index_entries.get(path)
            if entry is None:
                self.problem("INDEX.md", f"lists {path}, which isn't a record")
            elif entry != (match[1], match[2], match[3]):
                self.problem("INDEX.md", f"{path}: date, host or kind should be {' · '.join(entry)}")
        for path in self.index_entries:
            if listed.get(path) != 1:
                self.problem("INDEX.md", f"{path} listed {listed.get(path, 0)} times, not once")
        if dates != sorted(dates, reverse=True):
            self.problem("INDEX.md", "not newest first")

    def check_unchanged(self, base: str) -> None:
        """Against base, records are only added, and INDEX.md only gains lines."""
        diff = subprocess.run(
            ["git", "-C", str(ROOT), "diff", "--name-status", "--no-renames", base, "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        for line in diff.stdout.splitlines():
            status, path = line.split("\t", 1)
            if path.split("/")[0] in RECORD_DIRS and status != "A":
                self.problem(path, f"a merged record changed ({status}); a correction is a new record")
        shown = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{base}:INDEX.md"], capture_output=True, text=True, check=False
        )
        current = set((ROOT / "INDEX.md").read_text().splitlines())
        for line in shown.stdout.splitlines():
            if line.startswith("- ") and line not in current:
                self.problem("INDEX.md", f"a merged line was changed or removed: {line}")


def _is_aa(manifest: dict[str, Any]) -> bool:
    """One commit and one crate on both sides: ab.py renders a pooled report for it."""
    old, new = manifest.get("old", {}), manifest.get("new", {})
    return old.get("commit") == new.get("commit") and old.get("crate") == new.get("crate")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--indrajala-ml", required=True, type=Path)
    parser.add_argument("--base", help="the commit the change is checked against (a PR's base)")
    parser.add_argument("--reproduce", action="store_true", help="re-render every run's reports")
    args = parser.parse_args()
    checker = Checker(args.indrajala_ml.resolve())
    checker.check_layout()
    checker.check_index()
    if args.base:
        checker.check_unchanged(args.base)
    if args.reproduce:
        for run in sorted((ROOT / "runs").glob("*/*")):
            checker.reproduce(run)
    for problem in checker.problems:
        print(problem)
    records = len(checker.index_entries)
    print(f"{records} records, {len(checker.problems)} problems" + (" (reports reproduced)" if args.reproduce else ""))
    return 1 if checker.problems else 0


if __name__ == "__main__":
    sys.exit(main())
