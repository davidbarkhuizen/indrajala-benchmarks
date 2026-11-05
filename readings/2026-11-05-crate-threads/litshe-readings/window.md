Old `4176d10` against new `4176d10`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/window_recurrent_timing.py --repeats 3` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `17d1c27f71b0`) on both sides. Machine check: profile: identity matches (raspberry-pi-5.json); passes peaked at 48.0-48.5 C; max 1-min load 1.32; busy processes: none. Each row pools 3 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: 1 rows, all within noise
- 6 rows within noise, max |Δ| 7.8%
- spread of per-pass medians over 7 rows: median 4.4%, 90th percentile 11.3%, max 11.3%
- pass shifts (median over rows of pass median / pooled median): 1 +1.5%, 2 -1.3%

### per step

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| k1 s4 m16 B32 W12 | 0.007 (0.007-0.008) | 0.008, 0.007 | 4.4% |
| k4 s4 m16 B32 W5 | 0.011 (0.011-0.012) | 0.011, 0.012 | 7.5% |
| learn linear k1 s16 m16 B64 W19 | 0.006 (0.006-0.006) | 0.006, 0.006 | 4.7% |
| learn family p7 f32 B64 W16 | 0.050 (0.050-0.051) | 0.050, 0.050 | 0.2% |
| forward linear k1 s16 m16 n1024 | 2.433 (2.400-2.472) | 2.469, 2.400 | 2.8% |
| forward family p7 f32 n1024 | 5.603 (5.590-5.612) | 5.607, 5.593 | 0.3% |
| matmul 256 (control) | 0.001 (0.001-0.001) | 0.001, 0.001 | 11.3% |
