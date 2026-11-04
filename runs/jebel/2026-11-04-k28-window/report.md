Old `5cf590a` against new `5cf590a`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/window_recurrent_timing.py --repeats 3` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `238a017` (extension sha256 `bb3d5611c37d`) and new crate `18ce111` (extension sha256 `bc8a4a1fc83d`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.69; busy processes: none. Each row pools 9 runs per side.

- controls: 1 rows, all within noise
- consistent: per step / forward family p7 f32 n1024 -22.6% (3.164 -> 2.449 s)
- consistent: per step / forward linear k1 s16 m16 n1024 -15.6% (1.144 -> 0.966 s)
- consistent: per step / learn family p7 f32 B64 W16 -8.7% (0.019 -> 0.018 s)
- consistent: per step / learn linear k1 s16 m16 B64 W19 -7.2% (0.002 -> 0.002 s)
- 2 rows within noise (1 separated inside their spread), max |Δ| 9.8%

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| k1 s4 m16 B32 W12 | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | -6.3% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | within noise |
| k4 s4 m16 B32 W5 | 0.004 (0.004-0.004) | 0.003 (0.003-0.004) | -9.8% | 0.004, 0.004, 0.004 / 0.004, 0.003, 0.003 | separated, inside spread |
| learn linear k1 s16 m16 B64 W19 | 0.002 (0.002-0.003) | 0.002 (0.002-0.002) | -7.2% | 0.002, 0.002, 0.003 / 0.002, 0.002, 0.002 | consistent |
| learn family p7 f32 B64 W16 | 0.019 (0.019-0.020) | 0.018 (0.018-0.018) | -8.7% | 0.019, 0.019, 0.020 / 0.018, 0.018, 0.018 | consistent |
| forward linear k1 s16 m16 n1024 | 1.144 (1.132-1.148) | 0.966 (0.963-0.969) | -15.6% | 1.144, 1.133, 1.148 / 0.969, 0.966, 0.963 | consistent |
| forward family p7 f32 n1024 | 3.164 (3.160-3.167) | 2.449 (2.445-2.458) | -22.6% | 3.162, 3.162, 3.167 / 2.456, 2.452, 2.446 | consistent |
| matmul 256 | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -0.8% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise (control) |
