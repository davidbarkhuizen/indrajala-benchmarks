Old `0d91d1a` against new `0d91d1a`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/window_recurrent_timing.py --repeats 3` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `6a8190c` (extension sha256 `84ec4e85d91b`) and new crate `7b9878f` (extension sha256 `21b07c2bef84`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.65 (HIGH); busy processes: none. Each row pools 9 runs per side.

- controls: 1 rows, all within noise
- 6 rows within noise, max |Δ| 0.3%

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| k1 s4 m16 B32 W12 | 0.004 (0.004-0.004) | 0.004 (0.004-0.005) | -0.1% | 0.004, 0.004, 0.004 / 0.004, 0.004, 0.004 | within noise |
| k4 s4 m16 B32 W5 | 0.004 (0.004-0.004) | 0.004 (0.004-0.004) | +0.0% | 0.004, 0.004, 0.004 / 0.004, 0.004, 0.004 | within noise |
| learn linear k1 s16 m16 B64 W19 | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | -0.3% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | within noise |
| learn family p7 f32 B64 W16 | 0.022 (0.022-0.023) | 0.022 (0.022-0.022) | +0.2% | 0.023, 0.022, 0.022 / 0.022, 0.022, 0.022 | within noise |
| forward linear k1 s16 m16 n1024 | 1.131 (1.129-1.136) | 1.134 (1.132-1.136) | +0.3% | 1.136, 1.131, 1.130 / 1.133, 1.134, 1.134 | within noise |
| forward family p7 f32 n1024 | 3.401 (3.384-3.405) | 3.391 (3.386-3.397) | -0.3% | 3.401, 3.404, 3.385 / 3.387, 3.395, 3.391 | within noise |
| matmul 256 | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -3.9% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise (control) |
