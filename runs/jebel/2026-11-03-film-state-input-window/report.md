Old `7837558` against new `8bb8977`, run with `scripts/measurement/ab.py`: passes in the order ONNO, then passes 5-8 (NOON). Each pass ran `python scripts/measurement/window_recurrent_timing.py` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `857aff8` (extension sha256 `18304f7c5a63`) and new crate `bb05ca1` (extension sha256 `5f29e9f8c99e`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.52; busy processes: none. Each row pools 20 runs per side.

- controls: 1 rows, all within noise
- 6 rows within noise (4 separated inside their spread), max |Δ| 4.5%

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6, 7) / new (2, 3, 5, 8) | verdict |
|---|---|---|---|---|---|
| k1 s4 m16 B32 W12 | 0.004 (0.004-0.004) | 0.004 (0.004-0.005) | +4.0% | 0.004, 0.004, 0.004, 0.004 / 0.004, 0.004, 0.004, 0.004 | separated, inside spread |
| k4 s4 m16 B32 W5 | 0.004 (0.004-0.004) | 0.004 (0.004-0.005) | +4.5% | 0.004, 0.004, 0.004, 0.004 / 0.004, 0.004, 0.004, 0.005 | separated, inside spread |
| learn linear k1 s16 m16 B64 W19 | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | +2.3% | 0.003, 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003, 0.003 | separated, inside spread |
| learn family p7 f32 B64 W16 | 0.022 (0.022-0.022) | 0.022 (0.022-0.023) | +1.1% | 0.022, 0.022, 0.022, 0.022 / 0.022, 0.022, 0.022, 0.022 | separated, inside spread |
| forward linear k1 s16 m16 n1024 | 1.126 (1.120-1.130) | 1.135 (1.126-1.142) | +0.7% | 1.127, 1.129, 1.125, 1.122 / 1.139, 1.135, 1.126, 1.134 | within noise |
| forward family p7 f32 n1024 | 3.378 (3.370-3.401) | 3.394 (3.379-3.411) | +0.5% | 3.378, 3.385, 3.396, 3.371 / 3.408, 3.383, 3.390, 3.394 | within noise |
| matmul 256 | 0.000 (0.000-0.001) | 0.000 (0.000-0.001) | +0.2% | 0.000, 0.000, 0.000, 0.001 / 0.001, 0.000, 0.000, 0.000 | within noise (control) |
