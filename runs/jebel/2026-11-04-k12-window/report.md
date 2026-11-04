Old `0d91d1a` against new `0d91d1a`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/window_recurrent_timing.py --repeats 3` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `7fffc49` (extension sha256 `21b07c2bef84`) and new crate `a4c4379` (extension sha256 `ccd720475df3`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.41 (measured just after this run's crate builds); busy processes: none. Each row pools 9 runs per side.

- controls: 1 rows, all within noise
- consistent: per step / k1 s4 m16 B32 W12 -20.7% (0.004 -> 0.003 s)
- consistent: per step / k4 s4 m16 B32 W5 -11.1% (0.004 -> 0.004 s)
- consistent: per step / learn family p7 f32 B64 W16 -9.7% (0.023 -> 0.020 s)
- consistent: per step / forward family p7 f32 n1024 -8.1% (3.407 -> 3.131 s)
- 2 rows within noise, max |Δ| 1.0%

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| k1 s4 m16 B32 W12 | 0.004 (0.004-0.004) | 0.003 (0.003-0.003) | -20.7% | 0.004, 0.004, 0.004 / 0.003, 0.003, 0.003 | consistent |
| k4 s4 m16 B32 W5 | 0.004 (0.004-0.005) | 0.004 (0.004-0.004) | -11.1% | 0.004, 0.004, 0.005 / 0.004, 0.004, 0.004 | consistent |
| learn linear k1 s16 m16 B64 W19 | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | -1.0% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | within noise |
| learn family p7 f32 B64 W16 | 0.023 (0.022-0.023) | 0.020 (0.020-0.020) | -9.7% | 0.023, 0.022, 0.023 / 0.020, 0.020, 0.020 | consistent |
| forward linear k1 s16 m16 n1024 | 1.133 (1.127-1.136) | 1.129 (1.128-1.141) | -0.4% | 1.136, 1.128, 1.133 / 1.129, 1.141, 1.129 | within noise |
| forward family p7 f32 n1024 | 3.407 (3.397-3.422) | 3.131 (3.120-3.149) | -8.1% | 3.422, 3.406, 3.398 / 3.149, 3.131, 3.120 | consistent |
| matmul 256 | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -1.3% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise (control) |
