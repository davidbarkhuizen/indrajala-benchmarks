Old `515849f` against new `515849f`, run with `scripts/measurement/ab.py`: passes in the order ONNONO, then passes 7-8 (NO), which balances shifted pass 6 (old, slow +3.0%). Each pass ran `python scripts/measurement/window_recurrent_timing.py --repeats 3` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `cba601e` (extension sha256 `bc8a4a1fc83d`) and new crate `dc571a0` (extension sha256 `1cebe6ff7934`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.65 (measured just after this run's crate builds); busy processes: none. Each row pools 12 runs per side.

- controls: 1 rows, all within noise
- shifted: pass 6 (old, slow +2.9%); unbalanced, next: ab.py extend --order NO
- consistent: per step / forward linear k1 s16 m16 n1024 -8.2% (0.964 -> 0.884 s)
- consistent: per step / learn linear k1 s16 m16 B64 W19 -4.9% (0.002 -> 0.002 s)
- consistent: per step / forward family p7 f32 n1024 -4.4% (2.468 -> 2.359 s)
- 3 rows within noise (1 separated inside their spread), max |Δ| 1.8%

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6, 8) / new (2, 3, 5, 7) | verdict |
|---|---|---|---|---|---|
| k1 s4 m16 B32 W12 | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | -1.5% | 0.003, 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003, 0.003 | within noise |
| k4 s4 m16 B32 W5 | 0.003 (0.003-0.004) | 0.003 (0.003-0.004) | -1.4% | 0.003, 0.003, 0.004, 0.003 / 0.004, 0.003, 0.003, 0.003 | within noise |
| learn linear k1 s16 m16 B64 W19 | 0.002 (0.002-0.002) | 0.002 (0.002-0.002) | -4.9% | 0.002, 0.002, 0.002, 0.002 / 0.002, 0.002, 0.002, 0.002 | consistent |
| learn family p7 f32 B64 W16 | 0.018 (0.018-0.018) | 0.017 (0.017-0.018) | -1.8% | 0.018, 0.018, 0.018, 0.018 / 0.018, 0.017, 0.017, 0.017 | separated, inside spread |
| forward linear k1 s16 m16 n1024 | 0.964 (0.958-0.987) | 0.884 (0.882-0.888) | -8.2% | 0.962, 0.959, 0.986, 0.965 / 0.884, 0.886, 0.883, 0.888 | consistent |
| forward family p7 f32 n1024 | 2.468 (2.447-2.474) | 2.359 (2.355-2.362) | -4.4% | 2.448, 2.474, 2.473, 2.462 / 2.362, 2.357, 2.356, 2.362 | consistent |
| matmul 256 | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | +3.0% | 0.000, 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000, 0.000 | within noise (control) |
