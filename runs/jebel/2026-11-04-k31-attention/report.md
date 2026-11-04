Old `515849f` against new `515849f`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/attention_timing.py --no-memory --repeats 2 --masks causal --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `cba601e` (extension sha256 `bc8a4a1fc83d`) and new crate `db91879` (extension sha256 `5b3d1d17cea4`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.29 (measured just after this run's crate builds); busy processes: none. Each row pools 3 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- 12 rows within noise, max |Δ| 1.6%

### forward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| T=64 B=32 causal / numpy | 0.012 (0.012-0.012) | 0.012 (0.012-0.012) | -0.2% | 0.012, 0.012, 0.012 / 0.012, 0.012, 0.012 | within noise |
| T=256 B=8 causal / numpy | 0.032 (0.032-0.032) | 0.032 (0.032-0.032) | -0.1% | 0.032, 0.032, 0.032 / 0.032, 0.032, 0.032 | within noise |
| T=1024 B=2 causal / numpy | 0.103 (0.103-0.103) | 0.103 (0.103-0.103) | -0.1% | 0.103, 0.103, 0.103 / 0.103, 0.103, 0.103 | within noise |
| T=64 B=32 causal / rust | 0.006 (0.006-0.006) | 0.006 (0.006-0.006) | +0.7% | 0.006, 0.006, 0.006 / 0.006, 0.006, 0.006 | within noise |
| T=256 B=8 causal / rust | 0.016 (0.016-0.016) | 0.016 (0.016-0.016) | +1.1% | 0.016, 0.016, 0.016 / 0.016, 0.016, 0.016 | within noise |
| T=1024 B=2 causal / rust | 0.054 (0.053-0.054) | 0.054 (0.053-0.054) | +0.5% | 0.054, 0.054, 0.053 / 0.054, 0.054, 0.053 | within noise |

### backward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| T=64 B=32 causal / numpy | 0.018 (0.018-0.018) | 0.018 (0.018-0.018) | -0.7% | 0.018, 0.018, 0.018 / 0.018, 0.018, 0.018 | within noise |
| T=256 B=8 causal / numpy | 0.038 (0.038-0.038) | 0.038 (0.038-0.038) | -0.3% | 0.038, 0.038, 0.038 / 0.038, 0.038, 0.038 | within noise |
| T=1024 B=2 causal / numpy | 0.117 (0.117-0.117) | 0.117 (0.116-0.117) | -0.1% | 0.117, 0.117, 0.117 / 0.117, 0.117, 0.116 | within noise |
| T=64 B=32 causal / rust | 0.009 (0.009-0.009) | 0.009 (0.009-0.010) | +1.6% | 0.009, 0.009, 0.009 / 0.009, 0.009, 0.010 | within noise |
| T=256 B=8 causal / rust | 0.023 (0.022-0.023) | 0.023 (0.022-0.023) | +0.4% | 0.023, 0.023, 0.022 / 0.023, 0.022, 0.023 | within noise |
| T=1024 B=2 causal / rust | 0.073 (0.072-0.073) | 0.073 (0.073-0.073) | -0.4% | 0.073, 0.073, 0.072 / 0.073, 0.073, 0.073 | within noise |
