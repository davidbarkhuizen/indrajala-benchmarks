Old `f59388b` against new `f59388b`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/sequence_training_timing.py --windows 1024 --repeats 2` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `4dba70e` (extension sha256 `f5c8b6404a1d`) and new crate `ce5a267` (extension sha256 `24bdf26aceef`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 3.00 (HIGH); busy processes: none. Each row pools 3 runs per side.

- controls: none (a probe row can carry "control": true)
- 4 rows within noise, max |Δ| 0.2%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| 2-layer rotary numpy W=1024 | 2.834 (2.827-2.872) | 2.829 (2.823-2.832) | -0.2% | 2.834, 2.872, 2.827 / 2.829, 2.832, 2.823 | within noise |
| 2-layer rotary rust W=1024 | 1.748 (1.738-1.757) | 1.744 (1.743-1.749) | -0.2% | 1.738, 1.757, 1.748 / 1.743, 1.749, 1.744 | within noise |

### held-out nats

| case | old median (min-max) nats | new median (min-max) nats | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| 2-layer rotary numpy W=1024 | 2.925 (2.925-2.925) | 2.925 (2.925-2.925) | +0.0% | 2.925, 2.925, 2.925 / 2.925, 2.925, 2.925 | within noise |
| 2-layer rotary rust W=1024 | 2.925 (2.925-2.925) | 2.925 (2.925-2.925) | +0.0% | 2.925, 2.925, 2.925 / 2.925, 2.925, 2.925 | within noise |
