Old `6dcd34c` against new `6dcd34c`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/window_recurrent_timing.py` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `10dfec9` (extension sha256 `dd311e7a023b`) and new crate `4f230a4` (extension sha256 `c3a83219f593`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (raspberry-pi-5.json); passes peaked at 55.1-57.3 C; max 1-min load 1.42; busy processes: none. Each row pools 15 runs per side.

- controls: 1 rows, all within noise
- consistent: per step / forward linear k1 s16 m16 n1024 -10.8% (2.911 -> 2.597 s)
- consistent: per step / learn linear k1 s16 m16 B64 W19 -7.0% (0.007 -> 0.006 s)
- consistent: per step / long test family p7 f32 U1 n1024 c1023 -2.2% (21.497 -> 21.033 s)
- 4 rows within noise (1 separated inside their spread), max |Δ| 2.6%

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| k1 s4 m16 B32 W12 | 0.009 (0.009-0.009) | 0.009 (0.009-0.009) | -2.6% | 0.009, 0.009, 0.009 / 0.009, 0.009, 0.009 | separated, inside spread |
| k4 s4 m16 B32 W5 | 0.012 (0.011-0.012) | 0.012 (0.012-0.013) | -1.1% | 0.012, 0.012, 0.011 / 0.012, 0.013, 0.012 | within noise |
| learn linear k1 s16 m16 B64 W19 | 0.007 (0.007-0.007) | 0.006 (0.006-0.006) | -7.0% | 0.007, 0.007, 0.007 / 0.006, 0.006, 0.006 | consistent |
| learn family p7 f32 B64 W16 | 0.053 (0.052-0.054) | 0.053 (0.051-0.053) | -0.5% | 0.052, 0.054, 0.053 / 0.053, 0.053, 0.051 | within noise |
| forward linear k1 s16 m16 n1024 | 2.911 (2.891-2.995) | 2.597 (2.577-2.615) | -10.8% | 2.893, 2.911, 2.992 / 2.596, 2.604, 2.586 | consistent |
| forward family p7 f32 n1024 | 7.111 (6.932-7.205) | 6.944 (6.831-7.110) | -2.3% | 6.934, 7.186, 7.111 / 6.944, 7.060, 6.835 | within noise |
| long test family p7 f32 U1 n1024 c1023 | 21.497 (21.349-21.528) | 21.033 (20.916-21.130) | -2.2% | 21.358, 21.504, 21.520 / 21.033, 21.088, 20.927 | consistent |
| matmul 256 | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | +0.7% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise (control) |
