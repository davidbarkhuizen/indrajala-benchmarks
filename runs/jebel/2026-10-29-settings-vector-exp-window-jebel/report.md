Old `6dcd34c` against new `6dcd34c`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/window_recurrent_timing.py` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `a9862b5` (extension sha256 `32ad9eba76b4`) and new crate `a9bd177` (extension sha256 `be447c7907d0`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.39 (measured just after this run's crate builds); busy processes: none. Each row pools 15 runs per side.

- controls: 1 rows, all within noise
- consistent: per step / forward linear k1 s16 m16 n1024 -20.2% (1.439 -> 1.148 s)
- consistent: per step / learn linear k1 s16 m16 B64 W19 -11.4% (0.003 -> 0.003 s)
- consistent: per step / forward family p7 f32 n1024 -5.8% (3.706 -> 3.491 s)
- consistent: per step / long test family p7 f32 U1 n1024 c1023 -5.0% (11.744 -> 11.154 s)
- consistent: per step / learn family p7 f32 B64 W16 -2.4% (0.022 -> 0.021 s)
- consistent, small: per step / k4 s4 m16 B32 W5 +1.5% (0.004 -> 0.004 s)
- 1 rows within noise (1 separated inside their spread), max |Δ| 1.0%

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| k1 s4 m16 B32 W12 | 0.004 (0.004-0.004) | 0.004 (0.004-0.004) | +1.0% | 0.004, 0.004, 0.004 / 0.004, 0.004, 0.004 | separated, inside spread |
| k4 s4 m16 B32 W5 | 0.004 (0.004-0.004) | 0.004 (0.004-0.004) | +1.5% | 0.004, 0.004, 0.004 / 0.004, 0.004, 0.004 | consistent, small |
| learn linear k1 s16 m16 B64 W19 | 0.003 (0.003-0.003) | 0.003 (0.002-0.003) | -11.4% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.002 | consistent |
| learn family p7 f32 B64 W16 | 0.022 (0.022-0.022) | 0.021 (0.021-0.021) | -2.4% | 0.022, 0.022, 0.022 / 0.021, 0.021, 0.021 | consistent |
| forward linear k1 s16 m16 n1024 | 1.439 (1.437-1.448) | 1.148 (1.137-1.160) | -20.2% | 1.447, 1.439, 1.438 / 1.149, 1.149, 1.137 | consistent |
| forward family p7 f32 n1024 | 3.706 (3.694-3.731) | 3.491 (3.465-3.513) | -5.8% | 3.705, 3.711, 3.695 / 3.491, 3.507, 3.466 | consistent |
| long test family p7 f32 U1 n1024 c1023 | 11.744 (11.725-11.784) | 11.154 (11.041-11.180) | -5.0% | 11.737, 11.779, 11.739 / 11.154, 11.165, 11.056 | consistent |
| matmul 256 | 0.000 (0.000-0.001) | 0.000 (0.000-0.001) | +4.3% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.001 | within noise (control) |
