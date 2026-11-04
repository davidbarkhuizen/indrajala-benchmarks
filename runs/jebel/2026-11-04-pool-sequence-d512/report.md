Old `0b17d22` against new `0b17d22`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/sequence_training_timing.py --windows 256 --repeats 1 --features 512 --heads 8` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `edce2de` (extension sha256 `f72612f402e8`) and new crate `51a2baf` (extension sha256 `7194f34f6ce9`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.57 (measured just after this run's crate builds); busy processes: none. Each row pools 3 runs per side.

- controls: none (a probe row can carry "control": true)
- 4 rows within noise, max |Δ| 3.2%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| 2-layer rotary d=512 numpy W=256 | 13.913 (13.905-14.050) | 13.942 (13.828-13.970) | +0.2% | 13.905, 14.050, 13.913 / 13.942, 13.970, 13.828 | within noise |
| 2-layer rotary d=512 rust W=256 | 7.364 (7.172-7.365) | 7.125 (7.099-7.186) | -3.2% | 7.172, 7.364, 7.365 / 7.186, 7.099, 7.125 | within noise |

### held-out nats

| case | old median (min-max) nats | new median (min-max) nats | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| 2-layer rotary d=512 numpy W=256 | 3.365 (3.365-3.365) | 3.365 (3.365-3.365) | +0.0% | 3.365, 3.365, 3.365 / 3.365, 3.365, 3.365 | within noise |
| 2-layer rotary d=512 rust W=256 | 3.365 (3.365-3.365) | 3.365 (3.365-3.365) | +0.0% | 3.365, 3.365, 3.365 / 3.365, 3.365, 3.365 | within noise |
