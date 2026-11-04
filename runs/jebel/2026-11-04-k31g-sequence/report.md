Old `515849f` against new `515849f`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/sequence_training_timing.py --windows 1024 --repeats 2` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `cba601e` (extension sha256 `bc8a4a1fc83d`) and new crate `480cebc` (extension sha256 `5b3d1d17cea4`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.16; busy processes: none. Each row pools 3 runs per side.

- controls: none (a probe row can carry "control": true)
- 4 rows within noise (1 separated inside their spread), max |Δ| 0.5%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| 2-layer rotary numpy W=1024 | 2.828 (2.817-2.829) | 2.828 (2.824-2.832) | +0.0% | 2.817, 2.829, 2.828 / 2.824, 2.828, 2.832 | within noise |
| 2-layer rotary rust W=1024 | 1.493 (1.488-1.493) | 1.500 (1.495-1.502) | +0.5% | 1.493, 1.488, 1.493 / 1.495, 1.500, 1.502 | separated, inside spread |

### held-out nats

| case | old median (min-max) nats | new median (min-max) nats | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| 2-layer rotary numpy W=1024 | 2.925 (2.925-2.925) | 2.925 (2.925-2.925) | +0.0% | 2.925, 2.925, 2.925 / 2.925, 2.925, 2.925 | within noise |
| 2-layer rotary rust W=1024 | 2.925 (2.925-2.925) | 2.925 (2.925-2.925) | +0.0% | 2.925, 2.925, 2.925 / 2.925, 2.925, 2.925 | within noise |
