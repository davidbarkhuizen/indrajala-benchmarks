Old `bb60c11` against new `bb60c11`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/window_recurrent_timing.py --repeats 3` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `10aa3e5` (extension sha256 `24bdf26aceef`) and new crate `3bb2a40` (extension sha256 `bb3d5611c37d`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.31; busy processes: none. Each row pools 9 runs per side.

- controls: 1 rows, all within noise
- consistent: per step / learn linear k1 s16 m16 B64 W19 -6.0% (0.003 -> 0.002 s)
- consistent: per step / learn family p7 f32 B64 W16 -5.2% (0.021 -> 0.019 s)
- 4 rows within noise (3 separated inside their spread), max |Δ| 9.4%

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| k1 s4 m16 B32 W12 | 0.003 (0.003-0.004) | 0.003 (0.003-0.003) | -8.4% | 0.003, 0.004, 0.003 / 0.003, 0.003, 0.003 | separated, inside spread |
| k4 s4 m16 B32 W5 | 0.004 (0.004-0.004) | 0.004 (0.004-0.004) | -9.4% | 0.004, 0.004, 0.004 / 0.004, 0.004, 0.004 | separated, inside spread |
| learn linear k1 s16 m16 B64 W19 | 0.003 (0.003-0.003) | 0.002 (0.002-0.002) | -6.0% | 0.003, 0.003, 0.003 / 0.002, 0.002, 0.002 | consistent |
| learn family p7 f32 B64 W16 | 0.021 (0.020-0.021) | 0.019 (0.019-0.020) | -5.2% | 0.021, 0.021, 0.020 / 0.019, 0.019, 0.019 | consistent |
| forward linear k1 s16 m16 n1024 | 1.136 (1.133-1.140) | 1.133 (1.132-1.140) | -0.3% | 1.139, 1.136, 1.133 / 1.140, 1.133, 1.133 | within noise |
| forward family p7 f32 n1024 | 3.153 (3.144-3.156) | 3.164 (3.157-3.167) | +0.4% | 3.153, 3.153, 3.147 / 3.164, 3.157, 3.167 | separated, inside spread |
| matmul 256 | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | +2.4% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise (control) |
