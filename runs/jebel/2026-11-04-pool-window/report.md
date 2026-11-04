Old `0b17d22` against new `0b17d22`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/window_recurrent_timing.py --repeats 3` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `edce2de` (extension sha256 `f72612f402e8`) and new crate `51a2baf` (extension sha256 `7194f34f6ce9`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.83; busy processes: python. Each row pools 9 runs per side.

- CONTROL MOVED: 1 of 1 control rows consistent, e.g. per step / matmul 256 -40.4%: changes about that size can't be resolved here (next: epoch_op_profile.py)
- 6 rows within noise, max |Δ| 2.8%

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| k1 s4 m16 B32 W12 | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | -2.5% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | within noise |
| k4 s4 m16 B32 W5 | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | -2.8% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | within noise |
| learn linear k1 s16 m16 B64 W19 | 0.002 (0.002-0.002) | 0.002 (0.002-0.002) | +0.1% | 0.002, 0.002, 0.002 / 0.002, 0.002, 0.002 | within noise |
| learn family p7 f32 B64 W16 | 0.017 (0.017-0.017) | 0.017 (0.017-0.018) | -0.2% | 0.017, 0.017, 0.017 / 0.018, 0.017, 0.017 | within noise |
| forward linear k1 s16 m16 n1024 | 0.888 (0.886-0.901) | 0.891 (0.890-0.911) | +0.3% | 0.888, 0.887, 0.901 / 0.908, 0.891, 0.890 | within noise |
| forward family p7 f32 n1024 | 2.368 (2.366-2.371) | 2.368 (2.366-2.397) | -0.0% | 2.367, 2.368, 2.371 / 2.396, 2.367, 2.367 | within noise |
| matmul 256 | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -40.4% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | consistent (control) |
