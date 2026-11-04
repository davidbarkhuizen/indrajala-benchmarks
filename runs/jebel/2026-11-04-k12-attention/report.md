Old `0d91d1a` against new `0d91d1a`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/attention_timing.py --no-memory --repeats 3 --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `7fffc49` (extension sha256 `21b07c2bef84`) and new crate `a4c4379` (extension sha256 `ccd720475df3`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.88; busy processes: none. Each row pools 3 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: backward / T=64 B=32 causal / rust -5.5% (0.011 -> 0.010 s)
- consistent: forward / T=64 B=32 causal / rust -4.1% (0.007 -> 0.007 s)
- consistent: backward / T=256 B=8 causal / rust -3.1% (0.023 -> 0.023 s)
- consistent: forward / T=256 B=8 causal / rust -2.0% (0.017 -> 0.016 s)
- 20 rows within noise (5 separated inside their spread), max |Δ| 4.5%

### forward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| T=64 B=32 causal / numpy | 0.012 (0.012-0.012) | 0.012 (0.012-0.012) | -0.3% | 0.012, 0.012, 0.012 / 0.012, 0.012, 0.012 | within noise |
| T=64 B=32 packed / numpy | 0.013 (0.013-0.013) | 0.013 (0.013-0.013) | -0.2% | 0.013, 0.013, 0.013 / 0.013, 0.013, 0.013 | within noise |
| T=256 B=8 causal / numpy | 0.030 (0.030-0.031) | 0.030 (0.030-0.031) | -0.2% | 0.031, 0.030, 0.030 / 0.030, 0.031, 0.030 | within noise |
| T=256 B=8 packed / numpy | 0.032 (0.032-0.033) | 0.032 (0.032-0.032) | +0.1% | 0.033, 0.032, 0.032 / 0.032, 0.032, 0.032 | within noise |
| T=1024 B=2 causal / numpy | 0.104 (0.104-0.106) | 0.104 (0.104-0.105) | -0.4% | 0.106, 0.104, 0.104 / 0.104, 0.105, 0.104 | within noise |
| T=1024 B=2 packed / numpy | 0.105 (0.104-0.107) | 0.105 (0.105-0.105) | -0.1% | 0.107, 0.105, 0.104 / 0.105, 0.105, 0.105 | within noise |
| T=64 B=32 causal / rust | 0.007 (0.007-0.007) | 0.007 (0.006-0.007) | -4.1% | 0.007, 0.007, 0.007 / 0.006, 0.007, 0.007 | consistent |
| T=64 B=32 packed / rust | 0.007 (0.007-0.007) | 0.007 (0.007-0.007) | -4.5% | 0.007, 0.007, 0.007 / 0.007, 0.007, 0.007 | separated, inside spread |
| T=256 B=8 causal / rust | 0.017 (0.017-0.017) | 0.016 (0.016-0.016) | -2.0% | 0.017, 0.017, 0.017 / 0.016, 0.016, 0.016 | consistent |
| T=256 B=8 packed / rust | 0.017 (0.016-0.017) | 0.016 (0.016-0.016) | -1.7% | 0.017, 0.017, 0.016 / 0.016, 0.016, 0.016 | separated, inside spread |
| T=1024 B=2 causal / rust | 0.054 (0.054-0.054) | 0.055 (0.054-0.055) | +1.6% | 0.054, 0.054, 0.054 / 0.055, 0.055, 0.054 | separated, inside spread |
| T=1024 B=2 packed / rust | 0.047 (0.047-0.048) | 0.048 (0.047-0.048) | +0.6% | 0.047, 0.048, 0.047 / 0.047, 0.048, 0.048 | within noise |

### backward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| T=64 B=32 causal / numpy | 0.018 (0.018-0.019) | 0.018 (0.018-0.018) | -0.2% | 0.018, 0.019, 0.018 / 0.018, 0.018, 0.018 | within noise |
| T=64 B=32 packed / numpy | 0.019 (0.019-0.019) | 0.019 (0.019-0.019) | -0.3% | 0.019, 0.019, 0.019 / 0.019, 0.019, 0.019 | within noise |
| T=256 B=8 causal / numpy | 0.038 (0.038-0.039) | 0.039 (0.038-0.039) | +0.4% | 0.038, 0.039, 0.038 / 0.039, 0.039, 0.038 | within noise |
| T=256 B=8 packed / numpy | 0.040 (0.040-0.040) | 0.040 (0.040-0.040) | +0.2% | 0.040, 0.040, 0.040 / 0.040, 0.040, 0.040 | within noise |
| T=1024 B=2 causal / numpy | 0.120 (0.119-0.120) | 0.120 (0.119-0.120) | +0.3% | 0.120, 0.120, 0.119 / 0.120, 0.120, 0.119 | within noise |
| T=1024 B=2 packed / numpy | 0.117 (0.116-0.117) | 0.117 (0.116-0.118) | -0.0% | 0.117, 0.117, 0.116 / 0.117, 0.118, 0.116 | within noise |
| T=64 B=32 causal / rust | 0.011 (0.010-0.011) | 0.010 (0.010-0.010) | -5.5% | 0.010, 0.011, 0.011 / 0.010, 0.010, 0.010 | consistent |
| T=64 B=32 packed / rust | 0.011 (0.010-0.011) | 0.010 (0.010-0.011) | -4.2% | 0.010, 0.011, 0.011 / 0.010, 0.011, 0.010 | within noise |
| T=256 B=8 causal / rust | 0.023 (0.023-0.024) | 0.023 (0.023-0.023) | -3.1% | 0.024, 0.023, 0.023 / 0.023, 0.023, 0.023 | consistent |
| T=256 B=8 packed / rust | 0.023 (0.022-0.023) | 0.022 (0.022-0.022) | -2.6% | 0.023, 0.023, 0.022 / 0.022, 0.022, 0.022 | separated, inside spread |
| T=1024 B=2 causal / rust | 0.074 (0.074-0.074) | 0.072 (0.072-0.073) | -1.7% | 0.074, 0.074, 0.074 / 0.072, 0.073, 0.072 | separated, inside spread |
| T=1024 B=2 packed / rust | 0.062 (0.062-0.063) | 0.062 (0.062-0.062) | -0.7% | 0.062, 0.063, 0.062 / 0.062, 0.062, 0.062 | within noise |
