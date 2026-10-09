Old `6f0e9de` against new `6f0e9de`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/prepared_dataset_timing.py time --repeats 5 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `f31e318a10d7`) on both sides. Machine check: profile: identity matches; max 1-min load 0.15; busy processes: claude. Each row pools 15 runs per side.

- controls: 8 rows, all within noise
- 16 rows within noise, max |Δ| 1.4%
- spread of per-pass medians over 24 rows: median 2.2%, 90th percentile 5.6%, max 7.7%
- pass shifts (median over rows of pass median / pooled median): 1 -0.6%, 2 +0.0%, 3 +0.3%, 4 -0.1%, 5 -0.2%, 6 +0.2%

### epoch

| case | median (min-max) s | per-pass medians (1, 2, 3, 4, 5, 6) | spread |
|---|---|---|---|
| dense B=32 / numpy | 1.678 (1.662-1.690) | 1.665, 1.679, 1.688, 1.674, 1.672, 1.681 | 1.4% |
| dense B=32 / rust | 0.757 (0.744-0.788) | 0.750, 0.759, 0.762, 0.752, 0.754, 0.762 | 1.7% |
| dense single / numpy | 7.032 (6.849-7.342) | 7.038, 7.120, 7.027, 7.204, 6.939, 7.018 | 3.8% |
| dense single / rust | 1.435 (1.386-1.482) | 1.420, 1.429, 1.424, 1.439, 1.433, 1.451 | 2.2% |
| conv B=32 / numpy | 0.402 (0.396-0.512) | 0.403, 0.402, 0.402, 0.399, 0.402, 0.403 | 0.9% |
| conv B=32 / rust | 0.334 (0.324-0.347) | 0.327, 0.334, 0.344, 0.339, 0.328, 0.343 | 5.2% |
| conv single / numpy | 1.200 (1.173-1.230) | 1.178, 1.217, 1.221, 1.218, 1.200, 1.198 | 3.6% |
| conv single / rust | 0.498 (0.476-0.519) | 0.478, 0.497, 0.515, 0.492, 0.496, 0.516 | 7.7% |

### prepare

| case | median (min-max) s | per-pass medians (1, 2, 3, 4, 5, 6) | spread |
|---|---|---|---|
| dense B=32 / numpy (control) | 1.080 (1.075-1.083) | 1.081, 1.080, 1.080, 1.078, 1.080, 1.082 | 0.4% |
| dense B=32 / rust (control) | 0.200 (0.197-0.228) | 0.199, 0.200, 0.200, 0.199, 0.199, 0.202 | 1.6% |
| dense single / numpy (control) | 1.078 (1.072-1.085) | 1.077, 1.076, 1.075, 1.079, 1.077, 1.079 | 0.4% |
| dense single / rust (control) | 0.200 (0.198-0.218) | 0.199, 0.199, 0.200, 0.200, 0.200, 0.200 | 0.6% |
| conv B=32 / numpy (control) | 0.037 (0.037-0.038) | 0.037, 0.038, 0.038, 0.038, 0.037, 0.037 | 0.9% |
| conv B=32 / rust (control) | 0.006 (0.006-0.006) | 0.006, 0.006, 0.006, 0.006, 0.006, 0.006 | 2.3% |
| conv single / numpy (control) | 0.037 (0.037-0.038) | 0.037, 0.038, 0.037, 0.037, 0.037, 0.037 | 0.2% |
| conv single / rust (control) | 0.006 (0.006-0.006) | 0.006, 0.006, 0.006, 0.006, 0.006, 0.006 | 2.1% |

### epoch, loader

| case | median (min-max) s | per-pass medians (1, 2, 3, 4, 5, 6) | spread |
|---|---|---|---|
| dense B=32 / numpy | 0.601 (0.589-0.618) | 0.590, 0.607, 0.611, 0.600, 0.595, 0.605 | 3.5% |
| dense B=32 / rust | 0.559 (0.542-0.572) | 0.556, 0.567, 0.557, 0.560, 0.557, 0.560 | 2.0% |
| dense single / numpy | 6.185 (6.011-6.573) | 6.234, 6.227, 6.162, 6.372, 6.073, 6.156 | 4.8% |
| dense single / rust | 1.234 (1.206-1.274) | 1.232, 1.232, 1.229, 1.232, 1.243, 1.264 | 2.9% |
| conv B=32 / numpy | 0.365 (0.351-0.377) | 0.358, 0.362, 0.363, 0.364, 0.368, 0.369 | 3.1% |
| conv B=32 / rust | 0.329 (0.318-0.343) | 0.320, 0.329, 0.338, 0.332, 0.321, 0.338 | 5.6% |
| conv single / numpy | 1.153 (1.111-1.179) | 1.116, 1.165, 1.166, 1.164, 1.145, 1.150 | 4.3% |
| conv single / rust | 0.488 (0.466-0.509) | 0.469, 0.488, 0.506, 0.482, 0.488, 0.504 | 7.5% |
