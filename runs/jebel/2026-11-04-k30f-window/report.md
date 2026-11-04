Old `515849f` against new `515849f`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/window_recurrent_timing.py --repeats 3` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `cba601e` (extension sha256 `bc8a4a1fc83d`) and new crate `dc571a0` (extension sha256 `1cebe6ff7934`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.26; busy processes: python. Each row pools 9 runs per side.

- controls: 1 rows, all within noise
- consistent: per step / forward linear k1 s16 m16 n1024 -7.3% (0.960 -> 0.890 s)
- consistent: per step / learn linear k1 s16 m16 B64 W19 -3.3% (0.002 -> 0.002 s)
- consistent: per step / forward family p7 f32 n1024 -3.1% (2.448 -> 2.372 s)
- 3 rows within noise (1 separated inside their spread), max |Δ| 3.5%

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| k1 s4 m16 B32 W12 | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | +3.5% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | within noise |
| k4 s4 m16 B32 W5 | 0.003 (0.003-0.003) | 0.003 (0.003-0.004) | +2.8% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.004 | separated, inside spread |
| learn linear k1 s16 m16 B64 W19 | 0.002 (0.002-0.002) | 0.002 (0.002-0.002) | -3.3% | 0.002, 0.002, 0.002 / 0.002, 0.002, 0.002 | consistent |
| learn family p7 f32 B64 W16 | 0.018 (0.018-0.018) | 0.018 (0.017-0.018) | -0.6% | 0.018, 0.018, 0.018 / 0.018, 0.017, 0.018 | within noise |
| forward linear k1 s16 m16 n1024 | 0.960 (0.957-0.966) | 0.890 (0.882-0.891) | -7.3% | 0.957, 0.965, 0.960 / 0.890, 0.883, 0.891 | consistent |
| forward family p7 f32 n1024 | 2.448 (2.437-2.481) | 2.372 (2.356-2.377) | -3.1% | 2.448, 2.442, 2.479 / 2.373, 2.356, 2.375 | consistent |
| matmul 256 | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | +0.7% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise (control) |
