Old `5cf590a` against new `5cf590a`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/sequence_training_timing.py --windows 256 --repeats 1 --features 512 --heads 8` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `238a017` (extension sha256 `bb3d5611c37d`) and new crate `18ce111` (extension sha256 `bc8a4a1fc83d`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.60 (measured just after this run's crate builds); busy processes: none. Each row pools 3 runs per side.

- controls: none (a probe row can carry "control": true)
- consistent: epoch / 2-layer rotary d=512 rust W=256 -2.9% (7.597 -> 7.378 s)
- 3 rows within noise, max |Δ| 0.0%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| 2-layer rotary d=512 numpy W=256 | 14.026 (13.899-14.230) | 14.025 (13.894-14.092) | -0.0% | 13.899, 14.026, 14.230 / 13.894, 14.025, 14.092 | within noise |
| 2-layer rotary d=512 rust W=256 | 7.597 (7.593-7.649) | 7.378 (7.373-7.384) | -2.9% | 7.593, 7.649, 7.597 / 7.378, 7.384, 7.373 | consistent |

### held-out nats

| case | old median (min-max) nats | new median (min-max) nats | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| 2-layer rotary d=512 numpy W=256 | 3.365 (3.365-3.365) | 3.365 (3.365-3.365) | +0.0% | 3.365, 3.365, 3.365 / 3.365, 3.365, 3.365 | within noise |
| 2-layer rotary d=512 rust W=256 | 3.365 (3.365-3.365) | 3.365 (3.365-3.365) | +0.0% | 3.365, 3.365, 3.365 / 3.365, 3.365, 3.365 | within noise |
