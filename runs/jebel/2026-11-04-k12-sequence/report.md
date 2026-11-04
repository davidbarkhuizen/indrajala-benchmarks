Old `3332480` against new `3332480`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/sequence_training_timing.py --windows 1024 --repeats 2` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `7fffc49` (extension sha256 `21b07c2bef84`) and new crate `a4c4379` (extension sha256 `ccd720475df3`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.83; busy processes: none. Each row pools 3 runs per side.

- controls: none (a probe row can carry "control": true)
- consistent: epoch / 2-layer rotary rust W=1024 -2.8% (1.797 -> 1.746 s)
- 3 rows within noise, max |Δ| 0.2%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| 2-layer rotary numpy W=1024 | 2.826 (2.822-2.831) | 2.831 (2.826-2.835) | +0.2% | 2.822, 2.826, 2.831 / 2.835, 2.826, 2.831 | within noise |
| 2-layer rotary rust W=1024 | 1.797 (1.795-1.798) | 1.746 (1.745-1.746) | -2.8% | 1.795, 1.798, 1.797 / 1.746, 1.745, 1.746 | consistent |

### held-out nats

| case | old median (min-max) nats | new median (min-max) nats | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| 2-layer rotary numpy W=1024 | 2.925 (2.925-2.925) | 2.925 (2.925-2.925) | +0.0% | 2.925, 2.925, 2.925 / 2.925, 2.925, 2.925 | within noise |
| 2-layer rotary rust W=1024 | 2.925 (2.925-2.925) | 2.925 (2.925-2.925) | +0.0% | 2.925, 2.925, 2.925 / 2.925, 2.925, 2.925 | within noise |
