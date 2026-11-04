Old `cb31225` against new `cb31225`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/sequence_training_timing.py --windows 256 --repeats 1 --features 512 --heads 8` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `690bce8` (extension sha256 `7ba3057a73f7`) and new crate `5a19b18` (extension sha256 `84ec4e85d91b`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.00; busy processes: none. Each row pools 3 runs per side.

- controls: none (a probe row can carry "control": true)
- consistent: epoch / 2-layer rotary d=512 rust W=256 -47.9% (18.541 -> 9.662 s)
- 3 rows within noise, max |Δ| 0.1%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| 2-layer rotary d=512 numpy W=256 | 13.888 (13.753-14.018) | 13.906 (13.893-13.966) | +0.1% | 13.753, 13.888, 14.018 / 13.893, 13.966, 13.906 | within noise |
| 2-layer rotary d=512 rust W=256 | 18.541 (18.101-18.640) | 9.662 (9.500-9.665) | -47.9% | 18.101, 18.541, 18.640 / 9.500, 9.665, 9.662 | consistent |

### held-out nats

| case | old median (min-max) nats | new median (min-max) nats | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| 2-layer rotary d=512 numpy W=256 | 3.365 (3.365-3.365) | 3.365 (3.365-3.365) | +0.0% | 3.365, 3.365, 3.365 / 3.365, 3.365, 3.365 | within noise |
| 2-layer rotary d=512 rust W=256 | 3.365 (3.365-3.365) | 3.365 (3.365-3.365) | +0.0% | 3.365, 3.365, 3.365 / 3.365, 3.365, 3.365 | within noise |
