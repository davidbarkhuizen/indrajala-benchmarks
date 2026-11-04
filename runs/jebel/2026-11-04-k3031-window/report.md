Old `515849f` against new `515849f`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/window_recurrent_timing.py --repeats 3` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `cba601e` (extension sha256 `bc8a4a1fc83d`) and new crate `362e34c` (extension sha256 `7a3f0df0ecd3`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.22 (measured just after this run's crate builds); busy processes: none. Each row pools 9 runs per side.

- controls: 1 rows, all within noise
- consistent: per step / forward linear k1 s16 m16 n1024 -8.0% (0.970 -> 0.893 s)
- consistent: per step / learn linear k1 s16 m16 B64 W19 -5.0% (0.002 -> 0.002 s)
- consistent: per step / forward family p7 f32 n1024 -3.9% (2.459 -> 2.363 s)
- consistent, small: per step / learn family p7 f32 B64 W16 -1.7% (0.018 -> 0.017 s)
- 2 rows within noise, max |Δ| 1.1%

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| k1 s4 m16 B32 W12 | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | -1.1% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | within noise |
| k4 s4 m16 B32 W5 | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | -0.9% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | within noise |
| learn linear k1 s16 m16 B64 W19 | 0.002 (0.002-0.002) | 0.002 (0.002-0.002) | -5.0% | 0.002, 0.002, 0.002 / 0.002, 0.002, 0.002 | consistent |
| learn family p7 f32 B64 W16 | 0.018 (0.018-0.018) | 0.017 (0.017-0.017) | -1.7% | 0.018, 0.018, 0.018 / 0.017, 0.017, 0.017 | consistent, small |
| forward linear k1 s16 m16 n1024 | 0.970 (0.960-0.973) | 0.893 (0.889-0.894) | -8.0% | 0.973, 0.963, 0.970 / 0.893, 0.893, 0.889 | consistent |
| forward family p7 f32 n1024 | 2.459 (2.449-2.474) | 2.363 (2.357-2.368) | -3.9% | 2.459, 2.449, 2.466 / 2.365, 2.358, 2.363 | consistent |
| matmul 256 | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -4.0% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise (control) |
