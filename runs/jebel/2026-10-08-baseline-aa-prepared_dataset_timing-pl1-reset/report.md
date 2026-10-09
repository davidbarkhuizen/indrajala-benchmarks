Old `6f0e9de` against new `6f0e9de`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/prepared_dataset_timing.py time --repeats 5 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `f31e318a10d7`) on both sides. Machine check: profile: identity matches; max 1-min load 0.16; busy processes: claude. Each row pools 10 runs per side.

- controls: 8 rows, all within noise
- 16 rows within noise, max |Δ| 3.7%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 1.671 (1.660-1.701) | 1.680 (1.660-1.712) | +0.5% | 1.684, 1.666 / 1.678, 1.681 | within noise |
| dense B=32 / rust | 0.749 (0.744-0.766) | 0.755 (0.746-0.779) | +0.8% | 0.760, 0.745 / 0.755, 0.756 | within noise |
| dense single / numpy | 7.057 (6.839-7.247) | 6.983 (6.877-7.228) | -1.1% | 7.100, 6.949 / 7.143, 6.898 | within noise |
| dense single / rust | 1.416 (1.392-1.446) | 1.435 (1.380-1.479) | +1.3% | 1.441, 1.397 / 1.432, 1.437 | within noise |
| conv B=32 / numpy | 0.401 (0.398-0.409) | 0.400 (0.394-0.403) | -0.4% | 0.403, 0.400 / 0.400, 0.399 | within noise |
| conv B=32 / rust | 0.327 (0.324-0.357) | 0.332 (0.324-0.349) | +1.5% | 0.339, 0.327 / 0.328, 0.335 | within noise |
| conv single / numpy | 1.189 (1.166-1.258) | 1.184 (1.170-1.231) | -0.4% | 1.212, 1.180 / 1.186, 1.178 | within noise |
| conv single / rust | 0.478 (0.474-0.490) | 0.496 (0.477-0.516) | +3.6% | 0.486, 0.477 / 0.498, 0.482 | within noise |

### prepare

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 1.080 (1.075-1.090) | 1.081 (1.077-1.094) | +0.0% | 1.081, 1.080 / 1.082, 1.080 | within noise (control) |
| dense B=32 / rust | 0.200 (0.198-0.215) | 0.200 (0.198-0.201) | -0.2% | 0.200, 0.200 / 0.200, 0.200 | separated, inside spread (control) |
| dense single / numpy | 1.079 (1.071-1.091) | 1.078 (1.074-1.084) | -0.1% | 1.083, 1.074 / 1.079, 1.076 | within noise (control) |
| dense single / rust | 0.201 (0.199-0.205) | 0.200 (0.197-0.201) | -0.4% | 0.202, 0.199 / 0.200, 0.200 | within noise (control) |
| conv B=32 / numpy | 0.037 (0.037-0.039) | 0.037 (0.037-0.038) | +0.4% | 0.037, 0.037 / 0.037, 0.037 | separated, inside spread (control) |
| conv B=32 / rust | 0.006 (0.006-0.006) | 0.006 (0.006-0.006) | -0.2% | 0.006, 0.006 / 0.006, 0.006 | within noise (control) |
| conv single / numpy | 0.037 (0.037-0.039) | 0.037 (0.037-0.038) | +0.1% | 0.038, 0.037 / 0.037, 0.037 | within noise (control) |
| conv single / rust | 0.006 (0.006-0.007) | 0.006 (0.006-0.007) | +0.6% | 0.006, 0.006 / 0.006, 0.006 | within noise (control) |

### epoch, loader

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 0.595 (0.585-0.608) | 0.601 (0.587-0.625) | +1.0% | 0.601, 0.590 / 0.600, 0.602 | within noise |
| dense B=32 / rust | 0.554 (0.543-0.568) | 0.555 (0.547-0.570) | +0.3% | 0.555, 0.553 / 0.557, 0.554 | within noise |
| dense single / numpy | 6.186 (5.997-6.394) | 6.138 (6.030-6.362) | -0.8% | 6.215, 6.086 / 6.277, 6.073 | within noise |
| dense single / rust | 1.209 (1.187-1.249) | 1.227 (1.208-1.276) | +1.5% | 1.230, 1.203 / 1.232, 1.222 | within noise |
| conv B=32 / numpy | 0.365 (0.358-0.386) | 0.363 (0.359-0.372) | -0.5% | 0.362, 0.367 / 0.362, 0.363 | within noise |
| conv B=32 / rust | 0.321 (0.319-0.342) | 0.324 (0.317-0.343) | +1.0% | 0.327, 0.319 / 0.321, 0.327 | within noise |
| conv single / numpy | 1.129 (1.117-1.203) | 1.128 (1.110-1.169) | -0.1% | 1.158, 1.122 / 1.132, 1.116 | within noise |
| conv single / rust | 0.468 (0.464-0.482) | 0.485 (0.465-0.508) | +3.7% | 0.472, 0.467 / 0.487, 0.472 | within noise |
