Old `0afa901` against new `5c85b3e`, run with `scripts/ab.py`: passes in the order ONNO. Each pass ran `python scripts/prepared_dataset_timing.py time --repeats 5 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree. Machine check: profile: not recorded; busy processes: none. Each row pools 10 runs per side.

- controls: 8 rows, all within noise
- consistent: epoch / dense B=32 / numpy -0.4% (2.325 -> 2.314 s)
- 15 rows within noise (4 separated inside their spread), max |Δ| 3.4%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 2.325 (2.210-2.583) | 2.314 (2.300-2.393) | -0.4% | 2.325, 2.324 / 2.314, 2.318 | consistent |
| dense B=32 / rust | 1.341 (1.290-1.488) | 1.299 (1.289-1.350) | -3.1% | 1.397, 1.292 / 1.305, 1.298 | within noise |
| dense single / numpy | 9.850 (9.337-11.040) | 10.135 (9.667-11.200) | +2.9% | 10.411, 9.712 / 10.725, 9.812 | within noise |
| dense single / rust | 2.123 (2.042-2.507) | 2.111 (2.102-2.341) | -0.6% | 2.122, 2.270 / 2.113, 2.105 | separated, inside spread |
| conv B=32 / numpy | 1.191 (1.180-1.348) | 1.195 (1.180-1.336) | +0.3% | 1.192, 1.186 / 1.199, 1.191 | within noise |
| conv B=32 / rust | 0.569 (0.564-0.622) | 0.569 (0.566-0.588) | +0.0% | 0.593, 0.569 / 0.568, 0.571 | within noise |
| conv single / numpy | 3.353 (3.293-3.973) | 3.344 (3.318-3.387) | -0.3% | 3.559, 3.328 / 3.341, 3.344 | within noise |
| conv single / rust | 0.687 (0.650-1.091) | 0.681 (0.664-0.774) | -0.9% | 0.794, 0.677 / 0.681, 0.681 | within noise |

### prepare

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 1.258 (1.217-1.383) | 1.254 (1.252-1.293) | -0.3% | 1.338, 1.252 / 1.255, 1.254 | within noise (control) |
| dense B=32 / rust | 0.417 (0.405-0.441) | 0.410 (0.406-0.433) | -1.8% | 0.432, 0.408 / 0.410, 0.409 | within noise (control) |
| dense single / numpy | 1.264 (1.224-1.403) | 1.250 (1.239-1.290) | -1.1% | 1.316, 1.250 / 1.263, 1.247 | within noise (control) |
| dense single / rust | 0.413 (0.406-0.452) | 0.412 (0.408-0.449) | -0.2% | 0.431, 0.408 / 0.412, 0.412 | within noise (control) |
| conv B=32 / numpy | 0.056 (0.055-0.060) | 0.056 (0.055-0.059) | +0.1% | 0.056, 0.056 / 0.057, 0.056 | within noise (control) |
| conv B=32 / rust | 0.011 (0.011-0.013) | 0.011 (0.011-0.012) | +0.2% | 0.012, 0.011 / 0.011, 0.011 | within noise (control) |
| conv single / numpy | 0.051 (0.050-0.066) | 0.051 (0.050-0.063) | -0.2% | 0.052, 0.051 / 0.051, 0.051 | within noise (control) |
| conv single / rust | 0.013 (0.013-0.017) | 0.013 (0.013-0.014) | +0.5% | 0.014, 0.013 / 0.013, 0.013 | within noise (control) |

### epoch, loader

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 1.110 (1.065-1.260) | 1.072 (1.067-1.134) | -3.4% | 1.148, 1.086 / 1.074, 1.071 | separated, inside spread |
| dense B=32 / rust | 0.914 (0.882-1.015) | 0.884 (0.878-0.932) | -3.3% | 0.924, 0.890 / 0.883, 0.886 | separated, inside spread |
| dense single / numpy | 8.746 (8.361-10.391) | 8.731 (8.421-9.525) | -0.2% | 9.355, 8.629 / 8.705, 8.757 | within noise |
| dense single / rust | 1.657 (1.617-1.782) | 1.712 (1.678-1.986) | +3.3% | 1.661, 1.653 / 1.699, 1.791 | separated, inside spread |
| conv B=32 / numpy | 1.067 (1.055-1.364) | 1.057 (1.048-1.221) | -0.9% | 1.092, 1.066 / 1.074, 1.054 | within noise |
| conv B=32 / rust | 0.549 (0.547-0.631) | 0.550 (0.547-0.562) | +0.1% | 0.599, 0.549 / 0.549, 0.550 | within noise |
| conv single / numpy | 3.264 (3.182-3.720) | 3.234 (3.205-3.262) | -0.9% | 3.551, 3.233 / 3.239, 3.229 | within noise |
| conv single / rust | 0.660 (0.616-1.040) | 0.662 (0.630-0.728) | +0.3% | 0.828, 0.649 / 0.650, 0.664 | within noise |
