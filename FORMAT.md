# Record formats

Format 1. `tools/check_archive.py` enforces everything below; CI runs it on every PR.

## Profile snapshots: `machines/<hostname>/<captured>-profile.json`

A byte-for-byte copy of an indrajala-ml machine profile (`docs/machine_profiles/*.json`).
`<captured>` is its `state.captured_at` as `YYYYMMDDTHHMMSSZ`. A profile edited by hand after
capture (its `noise_rules`) is a different snapshot with the same capture time: it takes the next
free name, `<captured>-2-profile.json`, and so on.

Checks: `state.hostname` is the directory's name, and the profile validates against the newest
`machine_profile.schema.json` in indrajala-ml's history whose `schema_version` is the profile's (a
profile migrated to a newer schema keeps its capture time and commit).

## Runs: `runs/<hostname>/<date>-<name>/`

The run directory `ab.py run` wrote, with only the files it wrote: `manifest.json`,
`progress.jsonl`, and `<stem>.json`, `<stem>.stdout` and `<stem>.stderr` for each pass and smoke
stem in the manifest (the `data` symlink is not copied). Runs archived from indrajala-ml's test
fixtures may lack some of them. Beside them, written at archive time:

- `brief.txt`: `ab.py report --brief`;
- `report.md`: `ab.py report --md`;
- `pooled.md`: `ab.py report --pooled`, for an A/A only (one commit and one crate on both sides);
- `record.json`:

| field | |
| --- | --- |
| `format` | 1 |
| `kind` | `"run"` |
| `host` | the hostname, as the directory |
| `name` | the directory's name |
| `archived_at` | ISO 8601 time of archiving |
| `reason` | why it was archived (the PR, the milestone) |
| `replaces` | `null`, or the path of the record this one corrects |
| `profile` | the profile snapshot's path |
| `profile_source` | `"checked"`: the run recorded its profile's identity hash and the snapshot matches it; `"assigned"`: named at archive time, for a run from before identity hashes or without a machine check |
| `formats` | `{"ab_manifest": <manifest version>, "profile_schema": <schema_version>}` |
| `rendered_by` | `{"indrajala_ml": <commit whose ab.py rendered the reports>}` |
| `files` | the raw files copied, sorted |
| `reports` | the rendered files, sorted |

## Golden runs: `golden/<hostname>/<date>-<commit7>.json.gz` and `.md`

The golden file `scripts/golden_training_run.py record` wrote, gzipped without a timestamp. The
`.md` is its note: the commit pair it was recorded at (indrajala-ml and its `rust/` crate), why
(`material`: an owner-approved correctness change moved entries; `new-functionality`: entries were
added and none moved), what moved against the previous version on that host, and at the end a
fenced `json` block:

| field | |
| --- | --- |
| `format` | 1 |
| `kind` | `"golden"` |
| `host`, `date`, `commit`, `crate` | |
| `reason` | `"material"` or `"new-functionality"` |
| `note` | free text |
| `previous` | the previous version's path on this host, or `null` |
| `added`, `moved`, `removed` | entry names against `previous` (all `added` for a first version) |
| `networks` | entry count |
| `sha256` | of the uncompressed JSON |
| `profile` | the profile snapshot's path |
| `replaces` | `null`, or the path of the record this one corrects |

## INDEX.md

One line per record (profile snapshots included), newest first by date:

```
- <date> · <host> · <kind> · [<name>](<path>) · <reason>
```
