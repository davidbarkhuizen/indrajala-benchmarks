Old `0d91d1a` against new `0d91d1a`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/attention_timing.py --no-memory --repeats 3 --backends rust --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `6a8190c` (extension sha256 `84ec4e85d91b`) and new crate `7b9878f` (extension sha256 `21b07c2bef84`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.83 (HIGH); busy processes: none. Each row pools 3 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- 12 rows within noise (2 separated inside their spread), max |Δ| 3.2%

### forward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| T=64 B=32 causal / rust | 0.007 (0.007-0.007) | 0.007 (0.007-0.007) | +3.2% | 0.007, 0.007, 0.007 / 0.007, 0.007, 0.007 | within noise |
| T=64 B=32 packed / rust | 0.007 (0.007-0.007) | 0.007 (0.007-0.007) | +0.1% | 0.007, 0.007, 0.007 / 0.007, 0.007, 0.007 | within noise |
| T=256 B=8 causal / rust | 0.016 (0.016-0.016) | 0.017 (0.016-0.017) | +0.9% | 0.016, 0.016, 0.016 / 0.017, 0.017, 0.016 | within noise |
| T=256 B=8 packed / rust | 0.016 (0.016-0.017) | 0.016 (0.016-0.017) | +0.6% | 0.017, 0.016, 0.016 / 0.017, 0.016, 0.016 | within noise |
| T=1024 B=2 causal / rust | 0.054 (0.053-0.054) | 0.055 (0.054-0.056) | +1.7% | 0.053, 0.054, 0.054 / 0.056, 0.055, 0.054 | within noise |
| T=1024 B=2 packed / rust | 0.048 (0.048-0.048) | 0.048 (0.048-0.049) | +1.0% | 0.048, 0.048, 0.048 / 0.049, 0.048, 0.048 | separated, inside spread |

### backward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| T=64 B=32 causal / rust | 0.010 (0.010-0.010) | 0.010 (0.010-0.011) | +1.0% | 0.010, 0.010, 0.010 / 0.010, 0.011, 0.010 | separated, inside spread |
| T=64 B=32 packed / rust | 0.011 (0.011-0.011) | 0.011 (0.011-0.011) | -1.7% | 0.011, 0.011, 0.011 / 0.011, 0.011, 0.011 | within noise |
| T=256 B=8 causal / rust | 0.023 (0.023-0.023) | 0.023 (0.023-0.024) | +0.7% | 0.023, 0.023, 0.023 / 0.024, 0.023, 0.023 | within noise |
| T=256 B=8 packed / rust | 0.023 (0.023-0.023) | 0.023 (0.023-0.023) | -0.3% | 0.023, 0.023, 0.023 / 0.023, 0.023, 0.023 | within noise |
| T=1024 B=2 causal / rust | 0.074 (0.073-0.074) | 0.074 (0.074-0.075) | +0.3% | 0.074, 0.073, 0.074 / 0.074, 0.075, 0.074 | within noise |
| T=1024 B=2 packed / rust | 0.063 (0.062-0.063) | 0.063 (0.063-0.063) | +0.5% | 0.063, 0.063, 0.062 / 0.063, 0.063, 0.063 | within noise |
