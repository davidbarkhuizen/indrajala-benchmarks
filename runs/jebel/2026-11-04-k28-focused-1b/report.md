Old `5cf590a` against new `5cf590a`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --shape attention --op accumulate_gradient_batch --op forward_batch --rust-threads 1 --openblas-threads 1 --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `238a017` (extension sha256 `bb3d5611c37d`) and new crate `18ce111` (extension sha256 `bc8a4a1fc83d`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.95; busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / attention 16 x 32 forward_batch b32 / rust -17.1% (315.3 -> 261.5 µs)
- consistent: per call / attention 16 x 32 forward_batch b512 / rust -13.0% (5829 -> 5070 µs)
- consistent: per call / attention 16 x 32 accumulate_gradient_batch b32 / rust +5.3% (108.2 -> 114 µs)
- consistent: per call / attention 16 x 32 accumulate_gradient_batch b512 / rust -3.1% (2135 -> 2069 µs)
- 4 rows within noise, max |Δ| 1.3%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| attention 16 x 32 forward_batch b32 / numpy | 402 (397.9-408.7) | 399.2 (396.8-406.9) | -0.7% | 405.1, 400.4, 403.3 / 403.5, 397.5, 400 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 315.3 (312.4-317.3) | 261.5 (261-263.9) | -17.1% | 316.9, 314.6, 314 / 262.7, 261.2, 261.6 | consistent |
| attention 16 x 32 forward_batch b512 / numpy | 6138 (6096-6228) | 6123 (6115-6199) | -0.2% | 6213, 6125, 6115 / 6139, 6157, 6120 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 5829 (5805-5870) | 5070 (5036-5088) | -13.0% | 5863, 5814, 5821 / 5074, 5060, 5070 | consistent |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 278.9 (270.4-284.7) | 282.6 (275.2-301.6) | +1.3% | 284.1, 274.2, 277.1 / 289.9, 281.1, 285.1 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 108.2 (107.8-109.6) | 114 (113.7-117.1) | +5.3% | 109.4, 108, 108.1 / 115.6, 113.9, 114 | consistent |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5602 (5587-5808) | 5587 (5553-5602) | -0.3% | 5759, 5602, 5589 / 5573, 5580, 5600 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 2135 (2127-2144) | 2069 (2049-2076) | -3.1% | 2137, 2140, 2131 / 2063, 2060, 2071 | consistent |
