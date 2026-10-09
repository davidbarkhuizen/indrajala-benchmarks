Old `0afa901` against new `5c85b3e`, run with `scripts/ab.py`: passes in the order ONNO. Each pass ran `python scripts/prepared_dataset_timing.py time --repeats 5 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree. Machine check: profile: not recorded; busy processes: none. Each row pools 10 runs per side.

- CONTROL MOVED: 1 of 8 control rows consistent, e.g. prepare / conv B=32 / rust +0.3%: changes about that size can't be resolved here (next: epoch_op_profile.py)
- consistent: epoch, loader / dense single / numpy +10.2% (8.462 -> 9.328 s)
- consistent: epoch, loader / dense single / rust +5.4% (1.633 -> 1.721 s)
- consistent: epoch / dense single / rust +5.4% (2.057 -> 2.167 s)
- consistent: epoch, loader / conv single / numpy +2.9% (3.229 -> 3.324 s)
- consistent: epoch / conv single / numpy +2.4% (3.346 -> 3.426 s)
- consistent: epoch / dense B=32 / numpy +1.7% (2.306 -> 2.344 s)
- consistent: epoch / conv B=32 / rust +0.7% (0.568 -> 0.572 s)
- 9 rows within noise (7 separated inside their spread), max |Δ| 8.1%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 2.306 (2.088-2.457) | 2.344 (2.321-2.848) | +1.7% | 2.304, 2.306 / 2.336, 2.353 | consistent |
| dense B=32 / rust | 1.296 (1.259-1.316) | 1.308 (1.298-1.435) | +1.0% | 1.290, 1.302 / 1.308, 1.308 | separated, inside spread |
| dense single / numpy | 9.914 (9.693-10.822) | 10.717 (10.125-11.542) | +8.1% | 9.960, 9.869 / 10.762, 10.268 | separated, inside spread |
| dense single / rust | 2.057 (1.827-2.293) | 2.167 (2.093-2.373) | +5.4% | 2.064, 2.051 / 2.228, 2.151 | consistent |
| conv B=32 / numpy | 1.187 (1.032-1.276) | 1.202 (1.190-1.264) | +1.3% | 1.194, 1.187 / 1.199, 1.204 | separated, inside spread |
| conv B=32 / rust | 0.568 (0.518-0.605) | 0.572 (0.568-0.593) | +0.7% | 0.567, 0.568 / 0.573, 0.572 | consistent |
| conv single / numpy | 3.346 (3.234-3.961) | 3.426 (3.405-3.722) | +2.4% | 3.346, 3.346 / 3.418, 3.463 | consistent |
| conv single / rust | 0.671 (0.625-0.768) | 0.686 (0.658-0.828) | +2.2% | 0.666, 0.672 / 0.664, 0.688 | within noise |

### prepare

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 1.251 (1.144-1.648) | 1.255 (1.245-1.455) | +0.3% | 1.253, 1.249 / 1.255, 1.255 | separated, inside spread (control) |
| dense B=32 / rust | 0.411 (0.405-0.418) | 0.411 (0.407-0.473) | +0.1% | 0.411, 0.408 / 0.409, 0.412 | within noise (control) |
| dense single / numpy | 1.249 (1.174-1.438) | 1.248 (1.229-1.799) | -0.1% | 1.248, 1.251 / 1.245, 1.248 | separated, inside spread (control) |
| dense single / rust | 0.408 (0.388-0.413) | 0.409 (0.406-0.449) | +0.1% | 0.409, 0.407 / 0.408, 0.409 | within noise (control) |
| conv B=32 / numpy | 0.056 (0.045-0.058) | 0.056 (0.054-0.057) | +0.5% | 0.056, 0.056 / 0.056, 0.056 | separated, inside spread (control) |
| conv B=32 / rust | 0.011 (0.010-0.012) | 0.011 (0.011-0.012) | +0.3% | 0.011, 0.011 / 0.011, 0.011 | consistent (control) |
| conv single / numpy | 0.051 (0.045-0.079) | 0.051 (0.051-0.057) | +0.7% | 0.051, 0.050 / 0.051, 0.051 | separated, inside spread (control) |
| conv single / rust | 0.013 (0.012-0.014) | 0.013 (0.013-0.017) | +0.5% | 0.013, 0.013 / 0.013, 0.013 | separated, inside spread (control) |

### epoch, loader

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 1.073 (0.988-1.092) | 1.094 (1.088-1.348) | +2.0% | 1.066, 1.082 / 1.093, 1.098 | separated, inside spread |
| dense B=32 / rust | 0.879 (0.878-0.964) | 0.894 (0.884-1.005) | +1.7% | 0.880, 0.879 / 0.890, 0.902 | separated, inside spread |
| dense single / numpy | 8.462 (8.284-10.355) | 9.328 (8.880-10.604) | +10.2% | 8.449, 8.491 / 9.113, 9.543 | consistent |
| dense single / rust | 1.633 (1.428-1.881) | 1.721 (1.663-1.935) | +5.4% | 1.632, 1.651 / 1.716, 1.726 | consistent |
| conv B=32 / numpy | 1.057 (0.895-1.091) | 1.062 (1.053-1.302) | +0.5% | 1.053, 1.059 / 1.061, 1.068 | separated, inside spread |
| conv B=32 / rust | 0.548 (0.499-0.561) | 0.553 (0.550-0.595) | +0.9% | 0.546, 0.550 / 0.553, 0.557 | separated, inside spread |
| conv single / numpy | 3.229 (3.120-3.593) | 3.324 (3.301-3.647) | +2.9% | 3.230, 3.229 / 3.319, 3.335 | consistent |
| conv single / rust | 0.650 (0.602-0.835) | 0.650 (0.627-0.853) | -0.1% | 0.672, 0.645 / 0.643, 0.661 | within noise |
