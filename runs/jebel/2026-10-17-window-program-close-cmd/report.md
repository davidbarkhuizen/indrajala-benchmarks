Old `e958c2b` against new `95bd7a0`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/window_recurrent_timing.py --repeats 2 --cases long-test-family-p7-f32-U1-n1024-c1023 learn-linear-k1-s16-m16-B64-W19 learn-family-p7-f32-B64-W16 study-family-p5-f16-e40` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `81ab9a6` (extension sha256 `abcba3d7a30e`) and new crate `ddc5e42` (extension sha256 `147d423f2b89`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.00; busy processes: none. Each row pools 6 runs per side.

- controls: 1 rows, all within noise
- consistent: per step / long test family p7 f32 U1 n1024 c1023 -46.6% (21.071 -> 11.253 s)
- consistent: per step / learn linear k1 s16 m16 B64 W19 -43.9% (0.005 -> 0.003 s)
- consistent: per step / learn family p7 f32 B64 W16 -34.1% (0.034 -> 0.023 s)
- consistent: per step / study family p5 f16 e40 -32.9% (138.786 -> 93.146 s)
- 0 rows within noise

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| long test family p7 f32 U1 n1024 c1023 | 21.071 (20.997-21.161) | 11.253 (11.195-11.365) | -46.6% | 21.071, 21.157, 20.999 / 11.216, 11.352, 11.238 | consistent |
| learn linear k1 s16 m16 B64 W19 | 0.005 (0.005-0.005) | 0.003 (0.003-0.003) | -43.9% | 0.005, 0.005, 0.005 / 0.003, 0.003, 0.003 | consistent |
| learn family p7 f32 B64 W16 | 0.034 (0.034-0.035) | 0.023 (0.022-0.023) | -34.1% | 0.034, 0.034, 0.034 / 0.022, 0.023, 0.023 | consistent |
| study family p5 f16 e40 | 138.786 (138.390-139.527) | 93.146 (92.353-96.409) | -32.9% | 138.786, 139.450, 138.414 / 92.413, 93.146, 95.969 | consistent |
| matmul 256 | 0.000 (0.000-0.001) | 0.000 (0.000-0.001) | +3.6% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise (control) |
