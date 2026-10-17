Old `4139229` against new `a9891b0`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/window_recurrent_timing.py --cases learn-linear-k1-s16-m16-B64-W19 learn-family-p7-f32-B64-W16 long-test-family-p7-f32-U1-n1024-c1023` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `2eb0b2a` (extension sha256 `6a7c33aaa894`) and new crate `ddc5e42` (extension sha256 `147d423f2b89`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.22 (measured just after this run's crate builds); busy processes: none. Each row pools 15 runs per side.

- controls: 1 rows, all within noise
- consistent: per step / learn linear k1 s16 m16 B64 W19 -46.0% (0.005 -> 0.003 s)
- consistent: per step / learn family p7 f32 B64 W16 -30.8% (0.035 -> 0.024 s)
- consistent: per step / long test family p7 f32 U1 n1024 c1023 -5.0% (11.671 -> 11.082 s)
- 0 rows within noise

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| learn linear k1 s16 m16 B64 W19 | 0.005 (0.005-0.005) | 0.003 (0.003-0.003) | -46.0% | 0.005, 0.005, 0.005 / 0.003, 0.003, 0.003 | consistent |
| learn family p7 f32 B64 W16 | 0.035 (0.035-0.036) | 0.024 (0.024-0.024) | -30.8% | 0.036, 0.035, 0.035 / 0.024, 0.024, 0.024 | consistent |
| long test family p7 f32 U1 n1024 c1023 | 11.671 (11.638-11.808) | 11.082 (11.057-11.131) | -5.0% | 11.797, 11.643, 11.671 / 11.121, 11.077, 11.078 | consistent |
| matmul 256 | 0.001 (0.000-0.001) | 0.001 (0.001-0.001) | +0.6% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise (control) |
