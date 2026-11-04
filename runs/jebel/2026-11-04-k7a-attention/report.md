Old `cb31225` against new `cb31225`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/attention_timing.py --no-memory --repeats 3 --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `690bce8` (extension sha256 `7ba3057a73f7`) and new crate `5a19b18` (extension sha256 `84ec4e85d91b`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 3.59 (HIGH); busy processes: none. Each row pools 3 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: backward / T=64 B=32 causal / rust -12.2% (0.012 -> 0.011 s)
- consistent: backward / T=256 B=8 packed / rust -7.3% (0.024 -> 0.023 s)
- consistent: backward / T=256 B=8 causal / rust -6.9% (0.025 -> 0.023 s)
- consistent: backward / T=1024 B=2 packed / rust -4.7% (0.065 -> 0.062 s)
- consistent: backward / T=1024 B=2 causal / rust -4.2% (0.076 -> 0.073 s)
- 19 rows within noise (4 separated inside their spread), max |Δ| 10.9%

### forward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| T=64 B=32 causal / numpy | 0.012 (0.012-0.012) | 0.012 (0.012-0.012) | -0.4% | 0.012, 0.012, 0.012 / 0.012, 0.012, 0.012 | within noise |
| T=64 B=32 packed / numpy | 0.013 (0.013-0.013) | 0.013 (0.013-0.013) | +0.4% | 0.013, 0.013, 0.013 / 0.013, 0.013, 0.013 | within noise |
| T=256 B=8 causal / numpy | 0.030 (0.030-0.030) | 0.030 (0.030-0.031) | +0.7% | 0.030, 0.030, 0.030 / 0.030, 0.030, 0.031 | within noise |
| T=256 B=8 packed / numpy | 0.032 (0.032-0.032) | 0.032 (0.032-0.032) | +0.4% | 0.032, 0.032, 0.032 / 0.032, 0.032, 0.032 | separated, inside spread |
| T=1024 B=2 causal / numpy | 0.103 (0.103-0.103) | 0.104 (0.103-0.107) | +1.1% | 0.103, 0.103, 0.103 / 0.103, 0.104, 0.107 | within noise |
| T=1024 B=2 packed / numpy | 0.104 (0.104-0.105) | 0.104 (0.104-0.105) | +0.0% | 0.104, 0.104, 0.105 / 0.104, 0.105, 0.104 | within noise |
| T=64 B=32 causal / rust | 0.007 (0.007-0.007) | 0.007 (0.007-0.007) | +2.5% | 0.007, 0.007, 0.007 / 0.007, 0.007, 0.007 | within noise |
| T=64 B=32 packed / rust | 0.007 (0.007-0.007) | 0.007 (0.007-0.007) | +2.6% | 0.007, 0.007, 0.007 / 0.007, 0.007, 0.007 | separated, inside spread |
| T=256 B=8 causal / rust | 0.017 (0.017-0.017) | 0.017 (0.017-0.017) | +0.4% | 0.017, 0.017, 0.017 / 0.017, 0.017, 0.017 | within noise |
| T=256 B=8 packed / rust | 0.017 (0.017-0.017) | 0.017 (0.016-0.017) | -0.8% | 0.017, 0.017, 0.017 / 0.017, 0.017, 0.016 | separated, inside spread |
| T=1024 B=2 causal / rust | 0.053 (0.053-0.053) | 0.053 (0.053-0.054) | +0.7% | 0.053, 0.053, 0.053 / 0.053, 0.054, 0.053 | within noise |
| T=1024 B=2 packed / rust | 0.047 (0.047-0.048) | 0.048 (0.048-0.048) | +0.2% | 0.047, 0.048, 0.047 / 0.048, 0.048, 0.048 | within noise |

### backward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| T=64 B=32 causal / numpy | 0.018 (0.018-0.018) | 0.018 (0.018-0.018) | +1.1% | 0.018, 0.018, 0.018 / 0.018, 0.018, 0.018 | within noise |
| T=64 B=32 packed / numpy | 0.019 (0.018-0.019) | 0.019 (0.019-0.019) | -0.3% | 0.018, 0.019, 0.019 / 0.019, 0.019, 0.019 | within noise |
| T=256 B=8 causal / numpy | 0.038 (0.038-0.038) | 0.038 (0.038-0.038) | +0.1% | 0.038, 0.038, 0.038 / 0.038, 0.038, 0.038 | within noise |
| T=256 B=8 packed / numpy | 0.039 (0.039-0.040) | 0.040 (0.039-0.040) | +0.9% | 0.039, 0.040, 0.039 / 0.039, 0.040, 0.040 | within noise |
| T=1024 B=2 causal / numpy | 0.118 (0.117-0.119) | 0.118 (0.117-0.119) | +0.0% | 0.117, 0.119, 0.118 / 0.117, 0.119, 0.118 | within noise |
| T=1024 B=2 packed / numpy | 0.115 (0.114-0.115) | 0.115 (0.115-0.119) | +0.4% | 0.114, 0.115, 0.115 / 0.115, 0.115, 0.119 | within noise |
| T=64 B=32 causal / rust | 0.012 (0.012-0.012) | 0.011 (0.010-0.011) | -12.2% | 0.012, 0.012, 0.012 / 0.011, 0.010, 0.011 | consistent |
| T=64 B=32 packed / rust | 0.012 (0.011-0.012) | 0.011 (0.011-0.011) | -10.9% | 0.012, 0.012, 0.011 / 0.011, 0.011, 0.011 | separated, inside spread |
| T=256 B=8 causal / rust | 0.025 (0.025-0.025) | 0.023 (0.023-0.023) | -6.9% | 0.025, 0.025, 0.025 / 0.023, 0.023, 0.023 | consistent |
| T=256 B=8 packed / rust | 0.024 (0.024-0.025) | 0.023 (0.022-0.023) | -7.3% | 0.025, 0.024, 0.024 / 0.023, 0.023, 0.022 | consistent |
| T=1024 B=2 causal / rust | 0.076 (0.075-0.076) | 0.073 (0.073-0.073) | -4.2% | 0.076, 0.075, 0.076 / 0.073, 0.073, 0.073 | consistent |
| T=1024 B=2 packed / rust | 0.065 (0.065-0.065) | 0.062 (0.062-0.063) | -4.7% | 0.065, 0.065, 0.065 / 0.062, 0.062, 0.063 | consistent |
