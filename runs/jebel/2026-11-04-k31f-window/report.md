Old `515849f` against new `515849f`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/window_recurrent_timing.py --repeats 3` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `cba601e` (extension sha256 `bc8a4a1fc83d`) and new crate `480cebc` (extension sha256 `5b3d1d17cea4`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.52; busy processes: gnome-shell. Each row pools 9 runs per side.

- controls: 1 rows, all within noise
- consistent, small: per step / forward linear k1 s16 m16 n1024 +0.4% (0.959 -> 0.962 s)
- 5 rows within noise (3 separated inside their spread), max |Δ| 5.8%

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| k1 s4 m16 B32 W12 | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | -5.8% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | separated, inside spread |
| k4 s4 m16 B32 W5 | 0.004 (0.003-0.004) | 0.003 (0.003-0.003) | -4.9% | 0.004, 0.003, 0.004 / 0.003, 0.003, 0.003 | separated, inside spread |
| learn linear k1 s16 m16 B64 W19 | 0.002 (0.002-0.002) | 0.002 (0.002-0.002) | -1.3% | 0.002, 0.002, 0.002 / 0.002, 0.002, 0.002 | within noise |
| learn family p7 f32 B64 W16 | 0.018 (0.018-0.018) | 0.018 (0.018-0.018) | -1.2% | 0.018, 0.018, 0.018 / 0.018, 0.018, 0.018 | separated, inside spread |
| forward linear k1 s16 m16 n1024 | 0.959 (0.958-0.960) | 0.962 (0.962-0.964) | +0.4% | 0.959, 0.959, 0.959 / 0.962, 0.964, 0.962 | consistent, small |
| forward family p7 f32 n1024 | 2.448 (2.446-2.455) | 2.446 (2.441-2.450) | -0.1% | 2.447, 2.455, 2.447 / 2.446, 2.448, 2.442 | within noise |
| matmul 256 | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | +0.6% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise (control) |
