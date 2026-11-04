Old `515849f` against new `515849f`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/sequence_training_timing.py --windows 256 --repeats 1 --features 512 --heads 8` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `cba601e` (extension sha256 `bc8a4a1fc83d`) and new crate `480cebc` (extension sha256 `5b3d1d17cea4`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.29 (measured just after this run's crate builds); busy processes: none. Each row pools 3 runs per side.

- controls: none (a probe row can carry "control": true)
- 4 rows within noise, max |Δ| 0.7%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| 2-layer rotary d=512 numpy W=256 | 13.896 (13.810-13.979) | 13.988 (13.835-14.049) | +0.7% | 13.810, 13.896, 13.979 / 14.049, 13.835, 13.988 | within noise |
| 2-layer rotary d=512 rust W=256 | 7.225 (7.109-7.253) | 7.246 (7.152-7.293) | +0.3% | 7.225, 7.253, 7.109 / 7.246, 7.152, 7.293 | within noise |

### held-out nats

| case | old median (min-max) nats | new median (min-max) nats | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| 2-layer rotary d=512 numpy W=256 | 3.365 (3.365-3.365) | 3.365 (3.365-3.365) | +0.0% | 3.365, 3.365, 3.365 / 3.365, 3.365, 3.365 | within noise |
| 2-layer rotary d=512 rust W=256 | 3.365 (3.365-3.365) | 3.365 (3.365-3.365) | +0.0% | 3.365, 3.365, 3.365 / 3.365, 3.365, 3.365 | within noise |
