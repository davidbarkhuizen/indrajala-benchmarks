Old `e958c2b` against new `62083ac`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/window_recurrent_timing.py --cases long-test-family-p7-f32-U1-n1024-c1023 forward-linear-k1-s16-m16-n1024 forward-family-p7-f32-n1024` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `abcba3d7a30e`) on both sides. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.00; busy processes: none. Each row pools 15 runs per side.

- CONTROL MOVED: 1 of 1 control rows consistent, e.g. per step / matmul 256 -4.5%: changes about that size can't be resolved here (next: epoch_op_profile.py)
- consistent: per step / long test family p7 f32 U1 n1024 c1023 -36.0% (21.241 -> 13.584 s)
- consistent: per step / forward linear k1 s16 m16 n1024 -5.9% (1.743 -> 1.640 s)
- 1 rows within noise (1 separated inside their spread), max |Δ| 1.3%

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| long test family p7 f32 U1 n1024 c1023 | 21.241 (21.183-21.289) | 13.584 (13.498-13.661) | -36.0% | 21.278, 21.207, 21.244 / 13.541, 13.639, 13.572 | consistent |
| forward linear k1 s16 m16 n1024 | 1.743 (1.723-1.765) | 1.640 (1.625-1.663) | -5.9% | 1.764, 1.725, 1.743 / 1.626, 1.662, 1.640 | consistent |
| forward family p7 f32 n1024 | 4.362 (4.342-4.396) | 4.305 (4.285-4.334) | -1.3% | 4.387, 4.347, 4.362 / 4.291, 4.320, 4.305 | separated, inside spread |
| matmul 256 | 0.001 (0.001-0.001) | 0.000 (0.000-0.001) | -4.5% | 0.001, 0.001, 0.001 / 0.000, 0.000, 0.000 | consistent (control) |
