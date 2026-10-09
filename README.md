# indrajala-benchmarks

The benchmark archive of [indrajala-ml](https://github.com/davidbarkhuizen/indrajala-ml): the raw
timing runs, golden training runs and machine profiles behind its performance claims, kept so that
any number can be checked, re-reported under new rules, or compared across machines and over time.

Nothing here is secret. A record names hostnames, kernel and library versions and CPU details.

## What it holds

- **`runs/<hostname>/<date>-<name>/`**: an `ab.py` A/B or A/A run directory, raw: its manifest,
  progress log, and each pass's output and logs. `brief.txt`, `report.md` and, for an A/A,
  `pooled.md` are the reports `ab.py` rendered at archive time. `record.json` says why the run
  was archived and which profile snapshot it ran under.
- **`golden/<hostname>/<date>-<commit7>.json.gz`**: a golden training run (every value the
  networks produce, as `float.hex`), with a `.md` beside it naming its commit pair, why it was
  recorded, and which entries moved against the previous version.
- **`machines/<hostname>/<captured>-profile.json`**: a copy of each machine profile a record cites,
  so a record stays readable after the profile in indrajala-ml is re-recorded.
- **[INDEX.md](INDEX.md)**: one line per record, newest first.

[FORMAT.md](FORMAT.md) describes each file. indrajala-ml's `docs/measurement.md` says which changes
are archived (its benchmarking tiers: speedup claims and milestones) and how.

## How records arrive

Only by pull request, opened by indrajala-ml's archive commands (`scripts/ab.py archive` and
`scripts/golden_training_run.py archive`). The PR auto-merges when CI is green. CI is the only
reviewer, so it checks everything that can be checked:

- each record's files are exactly the ones its format allows;
- each profile snapshot matches indrajala-ml's machine profile schema of its `schema_version`;
- each golden file's hash matches its note;
- every archived run's reports re-render identically with indrajala-ml's current `ab.py`, so a
  change there that can no longer read old runs fails here (a replaced run is skipped: its
  correction is reproduced instead);
- nothing already merged changed. A record is immutable; a correction is a new record that names
  the one it replaces.

## Reading a record

Start with a run's `brief.txt`, then `report.md`. To re-report it under other rules, clone
indrajala-ml and run `python scripts/ab.py report runs/<host>/<run> --brief` against the directory.

## Licence

MIT, as indrajala-ml.
