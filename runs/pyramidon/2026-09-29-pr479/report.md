Old `0f85c93` against new `501f6b1`, run with `scripts/ab.py`: passes in the order ONNO. Each pass ran `python scripts/prepared_dataset_timing.py time --repeats 5 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree. Machine check: profile: not recorded; busy processes: none. Each row pools 10 runs per side.

- CONTROL MOVED: 1 of 8 control rows consistent, e.g. prepare / dense B=32 / rust +0.8%: changes about that size can't be resolved here (next: epoch_op_profile.py)
- consistent: epoch, loader / conv single / rust +2.8% (0.635 -> 0.653 s)
- consistent: epoch / dense B=32 / rust +0.5% (1.292 -> 1.299 s)
- 14 rows within noise (6 separated inside their spread), max |Δ| 3.3%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 2.339 (2.153-2.854) | 2.312 (2.298-2.424) | -1.2% | 2.349, 2.329 / 2.343, 2.309 | within noise |
| dense B=32 / rust | 1.292 (1.177-1.304) | 1.299 (1.291-1.348) | +0.5% | 1.290, 1.294 / 1.300, 1.298 | consistent |
| dense single / numpy | 9.648 (8.646-10.687) | 9.723 (9.650-10.552) | +0.8% | 9.545, 9.652 / 9.829, 9.667 | separated, inside spread |
| dense single / rust | 2.212 (1.856-2.435) | 2.139 (2.087-2.253) | -3.3% | 2.243, 2.182 / 2.179, 2.094 | separated, inside spread |
| conv B=32 / numpy | 1.184 (1.016-1.206) | 1.184 (1.177-1.195) | +0.0% | 1.163, 1.188 / 1.181, 1.186 | within noise |
| conv B=32 / rust | 0.566 (0.514-0.575) | 0.570 (0.564-0.587) | +0.6% | 0.565, 0.567 / 0.567, 0.574 | separated, inside spread |
| conv single / numpy | 3.326 (3.188-3.346) | 3.337 (3.306-3.414) | +0.3% | 3.328, 3.324 / 3.342, 3.332 | separated, inside spread |
| conv single / rust | 0.670 (0.605-0.717) | 0.681 (0.653-0.781) | +1.7% | 0.660, 0.687 / 0.677, 0.691 | within noise |

### prepare

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 1.254 (1.167-1.805) | 1.253 (1.247-1.297) | -0.1% | 1.254, 1.261 / 1.250, 1.254 | separated, inside spread (control) |
| dense B=32 / rust | 0.411 (0.387-0.417) | 0.415 (0.410-0.431) | +0.8% | 0.411, 0.411 / 0.415, 0.418 | consistent (control) |
| dense single / numpy | 1.244 (1.131-1.275) | 1.245 (1.239-1.292) | +0.1% | 1.197, 1.245 / 1.248, 1.242 | within noise (control) |
| dense single / rust | 0.411 (0.387-0.426) | 0.414 (0.410-0.418) | +0.8% | 0.408, 0.411 / 0.416, 0.413 | separated, inside spread (control) |
| conv B=32 / numpy | 0.055 (0.045-0.057) | 0.056 (0.055-0.057) | +0.8% | 0.052, 0.056 / 0.056, 0.056 | separated, inside spread (control) |
| conv B=32 / rust | 0.011 (0.010-0.011) | 0.011 (0.011-0.011) | -0.2% | 0.011, 0.011 / 0.011, 0.011 | within noise (control) |
| conv single / numpy | 0.051 (0.045-0.054) | 0.051 (0.051-0.063) | +0.4% | 0.051, 0.050 / 0.051, 0.052 | within noise (control) |
| conv single / rust | 0.013 (0.012-0.013) | 0.013 (0.013-0.013) | +0.6% | 0.013, 0.013 / 0.013, 0.013 | separated, inside spread (control) |

### epoch, loader

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 1.072 (0.912-1.155) | 1.073 (1.068-1.141) | +0.1% | 1.077, 1.071 / 1.076, 1.070 | within noise |
| dense B=32 / rust | 0.881 (0.794-0.885) | 0.880 (0.877-0.901) | -0.1% | 0.881, 0.881 / 0.880, 0.879 | separated, inside spread |
| dense single / numpy | 8.446 (7.515-8.956) | 8.450 (8.382-9.505) | +0.0% | 8.214, 8.453 / 8.424, 8.468 | within noise |
| dense single / rust | 1.699 (1.466-1.956) | 1.679 (1.660-1.905) | -1.2% | 1.700, 1.697 / 1.783, 1.666 | within noise |
| conv B=32 / numpy | 1.046 (0.874-1.069) | 1.055 (1.046-1.074) | +0.8% | 1.030, 1.048 / 1.053, 1.059 | separated, inside spread |
| conv B=32 / rust | 0.549 (0.500-0.564) | 0.548 (0.547-0.574) | -0.1% | 0.548, 0.550 / 0.548, 0.549 | within noise |
| conv single / numpy | 3.218 (3.166-3.271) | 3.218 (3.214-3.295) | -0.0% | 3.201, 3.238 / 3.217, 3.218 | within noise |
| conv single / rust | 0.635 (0.569-0.720) | 0.653 (0.623-0.744) | +2.8% | 0.629, 0.638 / 0.650, 0.656 | consistent |
