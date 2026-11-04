Old `f59388b` against new `f59388b`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/window_recurrent_timing.py --repeats 3` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `4dba70e` (extension sha256 `f5c8b6404a1d`) and new crate `ce5a267` (extension sha256 `24bdf26aceef`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.29; busy processes: none. Each row pools 9 runs per side.

- controls: 1 rows, all within noise
- 6 rows within noise (2 separated inside their spread), max |Δ| 4.4%

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| k1 s4 m16 B32 W12 | 0.003 (0.003-0.004) | 0.003 (0.003-0.003) | -4.4% | 0.004, 0.003, 0.003 / 0.003, 0.003, 0.003 | separated, inside spread |
| k4 s4 m16 B32 W5 | 0.004 (0.004-0.004) | 0.004 (0.004-0.004) | -3.2% | 0.004, 0.004, 0.004 / 0.004, 0.004, 0.004 | within noise |
| learn linear k1 s16 m16 B64 W19 | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | -0.1% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | within noise |
| learn family p7 f32 B64 W16 | 0.021 (0.021-0.021) | 0.020 (0.020-0.021) | -1.0% | 0.021, 0.021, 0.021 / 0.020, 0.020, 0.020 | separated, inside spread |
| forward linear k1 s16 m16 n1024 | 1.136 (1.133-1.149) | 1.132 (1.127-1.138) | -0.4% | 1.149, 1.133, 1.136 / 1.131, 1.131, 1.138 | within noise |
| forward family p7 f32 n1024 | 3.147 (3.135-3.154) | 3.153 (3.146-3.166) | +0.2% | 3.153, 3.137, 3.147 / 3.153, 3.147, 3.164 | within noise |
| matmul 256 | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | +5.9% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise (control) |
