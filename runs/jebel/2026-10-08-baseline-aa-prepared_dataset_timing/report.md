Old `6f0e9de` against new `6f0e9de`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/prepared_dataset_timing.py time --repeats 5 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `f31e318a10d7`) on both sides. Machine check: profile: identity matches; max 1-min load 0.15; busy processes: claude. Each row pools 15 runs per side.

- controls: 8 rows, all within noise
- 16 rows within noise, max |Δ| 1.4%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 1.674 (1.662-1.683) | 1.679 (1.666-1.690) | +0.3% | 1.665, 1.674, 1.681 / 1.679, 1.688, 1.672 | within noise |
| dense B=32 / rust | 0.756 (0.744-0.767) | 0.759 (0.746-0.788) | +0.5% | 0.750, 0.752, 0.762 / 0.759, 0.762, 0.754 | within noise |
| dense single / numpy | 7.038 (6.878-7.342) | 7.027 (6.849-7.335) | -0.1% | 7.038, 7.204, 7.018 / 7.120, 7.027, 6.939 | within noise |
| dense single / rust | 1.439 (1.398-1.482) | 1.429 (1.386-1.473) | -0.7% | 1.420, 1.439, 1.451 / 1.429, 1.424, 1.433 | within noise |
| conv B=32 / numpy | 0.402 (0.396-0.512) | 0.402 (0.399-0.405) | -0.0% | 0.403, 0.399, 0.403 / 0.402, 0.402, 0.402 | within noise |
| conv B=32 / rust | 0.339 (0.325-0.347) | 0.334 (0.324-0.346) | -1.3% | 0.327, 0.339, 0.343 / 0.334, 0.344, 0.328 | within noise |
| conv single / numpy | 1.198 (1.175-1.224) | 1.202 (1.173-1.230) | +0.3% | 1.178, 1.218, 1.198 / 1.217, 1.221, 1.200 | within noise |
| conv single / rust | 0.498 (0.476-0.517) | 0.498 (0.479-0.519) | +0.0% | 0.478, 0.492, 0.516 / 0.497, 0.515, 0.496 | within noise |

### prepare

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 1.080 (1.075-1.083) | 1.080 (1.076-1.081) | -0.0% | 1.081, 1.078, 1.082 / 1.080, 1.080, 1.080 | within noise (control) |
| dense B=32 / rust | 0.199 (0.197-0.203) | 0.200 (0.198-0.228) | +0.4% | 0.199, 0.199, 0.202 / 0.200, 0.200, 0.199 | within noise (control) |
| dense single / numpy | 1.079 (1.073-1.085) | 1.076 (1.072-1.083) | -0.3% | 1.077, 1.079, 1.079 / 1.076, 1.075, 1.077 | within noise (control) |
| dense single / rust | 0.199 (0.198-0.218) | 0.200 (0.198-0.204) | +0.2% | 0.199, 0.200, 0.200 / 0.199, 0.200, 0.200 | within noise (control) |
| conv B=32 / numpy | 0.037 (0.037-0.038) | 0.038 (0.037-0.038) | +0.2% | 0.037, 0.038, 0.037 / 0.038, 0.038, 0.037 | within noise (control) |
| conv B=32 / rust | 0.006 (0.006-0.006) | 0.006 (0.006-0.006) | +0.7% | 0.006, 0.006, 0.006 / 0.006, 0.006, 0.006 | within noise (control) |
| conv single / numpy | 0.037 (0.037-0.038) | 0.037 (0.037-0.038) | +0.0% | 0.037, 0.037, 0.037 / 0.038, 0.037, 0.037 | within noise (control) |
| conv single / rust | 0.006 (0.006-0.006) | 0.006 (0.006-0.006) | +0.1% | 0.006, 0.006, 0.006 / 0.006, 0.006, 0.006 | within noise (control) |

### epoch, loader

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 0.600 (0.589-0.609) | 0.606 (0.592-0.618) | +1.0% | 0.590, 0.600, 0.605 / 0.607, 0.611, 0.595 | within noise |
| dense B=32 / rust | 0.559 (0.542-0.572) | 0.560 (0.547-0.572) | +0.2% | 0.556, 0.560, 0.560 / 0.567, 0.557, 0.557 | within noise |
| dense single / numpy | 6.234 (6.011-6.573) | 6.146 (6.024-6.411) | -1.4% | 6.234, 6.372, 6.156 / 6.227, 6.162, 6.073 | within noise |
| dense single / rust | 1.234 (1.208-1.274) | 1.233 (1.206-1.274) | -0.1% | 1.232, 1.232, 1.264 / 1.232, 1.229, 1.243 | within noise |
| conv B=32 / numpy | 0.365 (0.351-0.377) | 0.366 (0.360-0.372) | +0.4% | 0.358, 0.364, 0.369 / 0.362, 0.363, 0.368 | within noise |
| conv B=32 / rust | 0.331 (0.318-0.343) | 0.327 (0.319-0.340) | -1.1% | 0.320, 0.332, 0.338 / 0.329, 0.338, 0.321 | within noise |
| conv single / numpy | 1.150 (1.111-1.179) | 1.156 (1.114-1.173) | +0.5% | 1.116, 1.164, 1.150 / 1.165, 1.166, 1.145 | within noise |
| conv single / rust | 0.487 (0.467-0.505) | 0.489 (0.466-0.509) | +0.4% | 0.469, 0.482, 0.504 / 0.488, 0.506, 0.488 | within noise |
