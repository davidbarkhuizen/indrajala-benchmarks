Old `501f6b1` against new `7df5e03`, run with `scripts/ab.py`: passes in the order ONNO, then passes 5-6 (NO), which balances pass 1, whose control column (prepare) ran fast in every config. Each pass ran `python scripts/prepared_dataset_timing.py time --repeats 5 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree. Machine check: profile: not recorded; busy processes: none. Each row pools 15 runs per side.

- controls: 8 rows, all within noise
- shifted: pass 1 (old, fast -8.5%), pass 5 (new, fast -8.0%); balanced
- 16 rows within noise, max |Δ| 1.5%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 2.312 (2.061-2.362) | 2.306 (1.994-2.413) | -0.3% | 2.163, 2.319, 2.312 / 2.306, 2.306, 2.097 | within noise |
| dense B=32 / rust | 1.289 (1.177-1.658) | 1.290 (1.176-1.305) | +0.0% | 1.207, 1.296, 1.293 / 1.297, 1.298, 1.187 | within noise |
| dense single / numpy | 9.760 (8.861-11.034) | 9.682 (8.612-10.811) | -0.8% | 9.305, 9.886, 10.380 / 9.723, 9.803, 8.911 | within noise |
| dense single / rust | 2.088 (1.855-2.354) | 2.092 (1.855-2.375) | +0.2% | 1.893, 2.088, 2.091 / 2.092, 2.188, 2.067 | within noise |
| conv B=32 / numpy | 1.181 (1.013-1.205) | 1.189 (1.001-1.239) | +0.7% | 1.016, 1.184, 1.184 / 1.191, 1.188, 1.065 | within noise |
| conv B=32 / rust | 0.567 (0.514-0.581) | 0.567 (0.514-0.582) | -0.0% | 0.516, 0.567, 0.569 / 0.568, 0.568, 0.520 | within noise |
| conv single / numpy | 3.346 (3.191-3.690) | 3.339 (3.246-3.876) | -0.2% | 3.240, 3.346, 3.326 / 3.343, 3.338, 3.324 | within noise |
| conv single / rust | 0.691 (0.536-0.927) | 0.680 (0.568-0.808) | -1.5% | 0.620, 0.691, 0.694 / 0.680, 0.680, 0.673 | within noise |

### prepare

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 1.247 (1.133-1.265) | 1.246 (1.132-1.270) | -0.1% | 1.173, 1.247, 1.250 / 1.245, 1.251, 1.163 | within noise (control) |
| dense B=32 / rust | 0.411 (0.385-0.441) | 0.413 (0.381-0.429) | +0.7% | 0.395, 0.415, 0.412 / 0.415, 0.413, 0.389 | within noise (control) |
| dense single / numpy | 1.240 (1.125-1.792) | 1.245 (1.125-1.295) | +0.4% | 1.132, 1.243, 1.243 / 1.246, 1.245, 1.132 | within noise (control) |
| dense single / rust | 0.411 (0.385-0.439) | 0.409 (0.387-0.462) | -0.4% | 0.388, 0.411, 0.415 / 0.409, 0.409, 0.402 | within noise (control) |
| conv B=32 / numpy | 0.056 (0.044-0.057) | 0.056 (0.045-0.059) | +0.2% | 0.045, 0.056, 0.056 / 0.056, 0.056, 0.048 | within noise (control) |
| conv B=32 / rust | 0.011 (0.010-0.012) | 0.011 (0.010-0.012) | +0.4% | 0.010, 0.011, 0.011 / 0.011, 0.011, 0.010 | within noise (control) |
| conv single / numpy | 0.051 (0.045-0.064) | 0.051 (0.045-0.069) | -0.2% | 0.046, 0.051, 0.051 / 0.050, 0.051, 0.045 | within noise (control) |
| conv single / rust | 0.013 (0.012-0.029) | 0.013 (0.012-0.013) | -0.3% | 0.012, 0.013, 0.013 / 0.013, 0.013, 0.013 | within noise (control) |

### epoch, loader

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 1.073 (0.960-1.100) | 1.070 (0.850-1.094) | -0.2% | 0.964, 1.073, 1.073 / 1.070, 1.072, 1.031 | within noise |
| dense B=32 / rust | 0.877 (0.794-1.051) | 0.878 (0.795-0.897) | +0.1% | 0.834, 0.881, 0.878 / 0.880, 0.879, 0.797 | within noise |
| dense single / numpy | 8.461 (7.492-9.320) | 8.445 (7.481-9.249) | -0.2% | 7.728, 8.477, 8.477 / 8.496, 8.491, 7.664 | within noise |
| dense single / rust | 1.681 (1.457-1.914) | 1.667 (1.466-1.914) | -0.9% | 1.575, 1.692, 1.760 / 1.667, 1.677, 1.646 | within noise |
| conv B=32 / numpy | 1.052 (0.878-1.099) | 1.052 (0.879-1.089) | -0.1% | 0.883, 1.054, 1.053 / 1.059, 1.050, 0.923 | within noise |
| conv B=32 / rust | 0.546 (0.499-0.590) | 0.547 (0.499-0.561) | +0.2% | 0.500, 0.547, 0.556 / 0.547, 0.550, 0.500 | within noise |
| conv single / numpy | 3.214 (3.106-3.396) | 3.234 (3.122-3.268) | +0.6% | 3.128, 3.227, 3.218 / 3.234, 3.248, 3.147 | within noise |
| conv single / rust | 0.658 (0.509-0.812) | 0.656 (0.601-0.793) | -0.4% | 0.631, 0.686, 0.643 / 0.675, 0.655, 0.642 | within noise |
