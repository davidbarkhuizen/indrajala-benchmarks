Old `6f0e9de` against new `6f0e9de`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/prepared_dataset_timing.py time --repeats 5 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `f31e318a10d7`) on both sides. Machine check: profile: identity matches; max 1-min load 0.16; busy processes: claude. Each row pools 10 runs per side.

- controls: 8 rows, all within noise
- 16 rows within noise, max |Δ| 3.7%
- spread of per-pass medians over 24 rows: median 2.0%, 90th percentile 3.9%, max 4.2%
- pass shifts (median over rows of pass median / pooled median): 1 +0.7%, 2 +0.1%, 3 +0.1%, 4 -0.4%

### epoch

| case | median (min-max) s | per-pass medians (1, 2, 3, 4) | spread |
|---|---|---|---|
| dense B=32 / numpy | 1.676 (1.660-1.712) | 1.684, 1.678, 1.681, 1.666 | 1.1% |
| dense B=32 / rust | 0.752 (0.744-0.779) | 0.760, 0.755, 0.756, 0.745 | 2.0% |
| dense single / numpy | 7.025 (6.839-7.247) | 7.100, 7.143, 6.898, 6.949 | 3.5% |
| dense single / rust | 1.428 (1.380-1.479) | 1.441, 1.432, 1.437, 1.397 | 3.1% |
| conv B=32 / numpy | 0.400 (0.394-0.409) | 0.403, 0.400, 0.399, 0.400 | 0.9% |
| conv B=32 / rust | 0.327 (0.324-0.357) | 0.339, 0.328, 0.335, 0.327 | 3.9% |
| conv single / numpy | 1.184 (1.166-1.258) | 1.212, 1.186, 1.178, 1.180 | 2.9% |
| conv single / rust | 0.481 (0.474-0.516) | 0.486, 0.498, 0.482, 0.477 | 4.2% |

### prepare

| case | median (min-max) s | per-pass medians (1, 2, 3, 4) | spread |
|---|---|---|---|
| dense B=32 / numpy (control) | 1.080 (1.075-1.094) | 1.081, 1.082, 1.080, 1.080 | 0.1% |
| dense B=32 / rust (control) | 0.200 (0.198-0.215) | 0.200, 0.200, 0.200, 0.200 | 0.3% |
| dense single / numpy (control) | 1.078 (1.071-1.091) | 1.083, 1.079, 1.076, 1.074 | 0.8% |
| dense single / rust (control) | 0.200 (0.197-0.205) | 0.202, 0.200, 0.200, 0.199 | 1.7% |
| conv B=32 / numpy (control) | 0.037 (0.037-0.039) | 0.037, 0.037, 0.037, 0.037 | 0.6% |
| conv B=32 / rust (control) | 0.006 (0.006-0.006) | 0.006, 0.006, 0.006, 0.006 | 1.0% |
| conv single / numpy (control) | 0.037 (0.037-0.039) | 0.038, 0.037, 0.037, 0.037 | 0.4% |
| conv single / rust (control) | 0.006 (0.006-0.007) | 0.006, 0.006, 0.006, 0.006 | 2.1% |

### epoch, loader

| case | median (min-max) s | per-pass medians (1, 2, 3, 4) | spread |
|---|---|---|---|
| dense B=32 / numpy | 0.597 (0.585-0.625) | 0.601, 0.600, 0.602, 0.590 | 2.0% |
| dense B=32 / rust | 0.554 (0.543-0.570) | 0.555, 0.557, 0.554, 0.553 | 0.7% |
| dense single / numpy | 6.169 (5.997-6.394) | 6.215, 6.277, 6.073, 6.086 | 3.3% |
| dense single / rust | 1.221 (1.187-1.276) | 1.230, 1.232, 1.222, 1.203 | 2.4% |
| conv B=32 / numpy | 0.363 (0.358-0.386) | 0.362, 0.362, 0.363, 0.367 | 1.4% |
| conv B=32 / rust | 0.321 (0.317-0.343) | 0.327, 0.321, 0.327, 0.319 | 2.5% |
| conv single / numpy | 1.128 (1.110-1.203) | 1.158, 1.132, 1.116, 1.122 | 3.7% |
| conv single / rust | 0.470 (0.464-0.508) | 0.472, 0.487, 0.472, 0.467 | 4.2% |
