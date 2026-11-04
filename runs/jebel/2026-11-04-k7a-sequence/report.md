Old `cb31225` against new `cb31225`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/sequence_training_timing.py --windows 1024 --repeats 2` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `690bce8` (extension sha256 `7ba3057a73f7`) and new crate `5a19b18` (extension sha256 `84ec4e85d91b`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.34 (measured just after this run's crate builds); busy processes: none. Each row pools 3 runs per side.

- controls: none (a probe row can carry "control": true)
- consistent: epoch / 2-layer rotary rust W=1024 -12.4% (2.048 -> 1.793 s)
- 3 rows within noise, max |Δ| 0.0%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| 2-layer rotary numpy W=1024 | 2.861 (2.837-2.877) | 2.860 (2.829-2.873) | -0.0% | 2.861, 2.877, 2.837 / 2.873, 2.829, 2.860 | within noise |
| 2-layer rotary rust W=1024 | 2.048 (2.042-2.049) | 1.793 (1.783-1.793) | -12.4% | 2.048, 2.042, 2.049 / 1.793, 1.793, 1.783 | consistent |

### held-out nats

| case | old median (min-max) nats | new median (min-max) nats | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| 2-layer rotary numpy W=1024 | 2.925 (2.925-2.925) | 2.925 (2.925-2.925) | +0.0% | 2.925, 2.925, 2.925 / 2.925, 2.925, 2.925 | within noise |
| 2-layer rotary rust W=1024 | 2.925 (2.925-2.925) | 2.925 (2.925-2.925) | +0.0% | 2.925, 2.925, 2.925 / 2.925, 2.925, 2.925 | within noise |
