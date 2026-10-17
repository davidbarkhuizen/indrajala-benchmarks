Old `e19f36b` against new `57a7d13`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/window_recurrent_timing.py --cases long-test-family-p7-f32-U1-n1024-c1023 forward-linear-k1-s16-m16-n1024 forward-family-p7-f32-n1024 learn-linear-k1-s16-m16-B64-W19` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `81ab9a6` (extension sha256 `abcba3d7a30e`) and new crate `2eb0b2a` (extension sha256 `6a7c33aaa894`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.08 (measured just after this run's crate builds); busy processes: none. Each row pools 15 runs per side.

- controls: 1 rows, all within noise
- consistent: per step / forward linear k1 s16 m16 n1024 -24.6% (1.651 -> 1.245 s)
- consistent: per step / forward family p7 f32 n1024 -14.2% (4.318 -> 3.705 s)
- consistent: per step / long test family p7 f32 U1 n1024 c1023 -14.1% (13.610 -> 11.689 s)
- consistent, small: per step / learn linear k1 s16 m16 B64 W19 +1.0% (0.005 -> 0.005 s)
- 0 rows within noise

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| long test family p7 f32 U1 n1024 c1023 | 13.610 (13.520-13.633) | 11.689 (11.666-11.709) | -14.1% | 13.613, 13.526, 13.616 / 11.671, 11.689, 11.703 | consistent |
| forward linear k1 s16 m16 n1024 | 1.651 (1.623-1.656) | 1.245 (1.240-1.252) | -24.6% | 1.653, 1.626, 1.651 / 1.242, 1.245, 1.245 | consistent |
| forward family p7 f32 n1024 | 4.318 (4.303-4.331) | 3.705 (3.692-3.719) | -14.2% | 4.318, 4.305, 4.327 / 3.693, 3.708, 3.705 | consistent |
| learn linear k1 s16 m16 B64 W19 | 0.005 (0.005-0.005) | 0.005 (0.005-0.005) | +1.0% | 0.005, 0.005, 0.005 / 0.005, 0.005, 0.005 | consistent, small |
| matmul 256 | 0.000 (0.000-0.001) | 0.001 (0.000-0.001) | +1.8% | 0.000, 0.000, 0.000 / 0.000, 0.001, 0.001 | within noise (control) |
