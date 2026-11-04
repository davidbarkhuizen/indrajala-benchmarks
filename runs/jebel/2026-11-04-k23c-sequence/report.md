Old `bb60c11` against new `bb60c11`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/sequence_training_timing.py --windows 1024 --repeats 2` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `10aa3e5` (extension sha256 `24bdf26aceef`) and new crate `3bb2a40` (extension sha256 `bb3d5611c37d`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.98 (HIGH); busy processes: none. Each row pools 3 runs per side.

- controls: none (a probe row can carry "control": true)
- consistent: epoch / 2-layer rotary rust W=1024 -8.2% (1.749 -> 1.607 s)
- 3 rows within noise, max |Δ| 0.1%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| 2-layer rotary numpy W=1024 | 2.831 (2.825-2.833) | 2.830 (2.823-2.832) | -0.1% | 2.825, 2.833, 2.831 / 2.832, 2.830, 2.823 | within noise |
| 2-layer rotary rust W=1024 | 1.749 (1.747-1.749) | 1.607 (1.606-1.612) | -8.2% | 1.749, 1.749, 1.747 / 1.606, 1.612, 1.607 | consistent |

### held-out nats

| case | old median (min-max) nats | new median (min-max) nats | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| 2-layer rotary numpy W=1024 | 2.925 (2.925-2.925) | 2.925 (2.925-2.925) | +0.0% | 2.925, 2.925, 2.925 / 2.925, 2.925, 2.925 | within noise |
| 2-layer rotary rust W=1024 | 2.925 (2.925-2.925) | 2.925 (2.925-2.925) | +0.0% | 2.925, 2.925, 2.925 / 2.925, 2.925, 2.925 | within noise |
