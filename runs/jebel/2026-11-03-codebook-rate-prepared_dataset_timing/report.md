Old `751d1d2` against new `675df54`, run with `scripts/measurement/ab.py`: passes in the order ONNO. Each pass ran `python scripts/measurement/prepared_dataset_timing.py time --repeats 5 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `18304f7c5a63`) on both sides. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.05; busy processes: none. Each row pools 10 runs per side.

- CONTROL MOVED: 1 of 8 control rows consistent, e.g. prepare / dense B=32 / rust +0.5%: changes about that size can't be resolved here (next: epoch_op_profile.py)
- consistent: epoch, loader / dense single / rust -2.9% (1.252 -> 1.215 s)
- consistent: epoch, loader / dense single / numpy -2.9% (6.124 -> 5.946 s)
- consistent, small: epoch / dense single / rust -2.0% (1.448 -> 1.419 s)
- consistent, small: epoch / conv B=32 / rust -0.8% (0.313 -> 0.310 s)
- consistent, small: epoch / dense single / numpy +0.8% (7.099 -> 7.156 s)
- consistent, small: epoch / conv B=32 / numpy -0.7% (0.410 -> 0.407 s)
- 10 rows within noise (1 separated inside their spread), max |Δ| 1.9%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 1.673 (1.666-1.684) | 1.668 (1.662-1.689) | -0.3% | 1.677, 1.668 / 1.665, 1.685 | within noise |
| dense B=32 / rust | 0.756 (0.749-0.771) | 0.742 (0.737-0.757) | -1.9% | 0.756, 0.757 / 0.750, 0.741 | separated, inside spread |
| dense single / numpy | 7.099 (7.029-7.191) | 7.156 (7.079-7.431) | +0.8% | 7.101, 7.098 / 7.152, 7.197 | consistent, small |
| dense single / rust | 1.448 (1.439-1.487) | 1.419 (1.411-1.443) | -2.0% | 1.457, 1.442 / 1.417, 1.422 | consistent, small |
| conv B=32 / numpy | 0.410 (0.408-0.414) | 0.407 (0.403-0.412) | -0.7% | 0.410, 0.410 / 0.407, 0.408 | consistent, small |
| conv B=32 / rust | 0.313 (0.311-0.332) | 0.310 (0.306-0.312) | -0.8% | 0.312, 0.313 / 0.310, 0.310 | consistent, small |
| conv single / numpy | 1.187 (1.174-1.204) | 1.188 (1.168-1.206) | +0.1% | 1.201, 1.178 / 1.172, 1.199 | within noise |
| conv single / rust | 0.464 (0.460-0.485) | 0.465 (0.462-0.480) | +0.1% | 0.464, 0.468 / 0.464, 0.466 | within noise |

### prepare

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 1.078 (1.075-1.079) | 1.077 (1.076-1.105) | -0.1% | 1.079, 1.078 / 1.080, 1.076 | within noise (control) |
| dense B=32 / rust | 0.197 (0.195-0.199) | 0.198 (0.196-0.199) | +0.5% | 0.197, 0.197 / 0.198, 0.198 | consistent, small (control) |
| dense single / numpy | 1.078 (1.076-1.081) | 1.077 (1.071-1.083) | -0.1% | 1.079, 1.078 / 1.078, 1.075 | separated, inside spread (control) |
| dense single / rust | 0.197 (0.195-0.199) | 0.198 (0.197-0.200) | +0.5% | 0.197, 0.198 / 0.198, 0.198 | within noise (control) |
| conv B=32 / numpy | 0.037 (0.037-0.038) | 0.037 (0.037-0.038) | +0.3% | 0.037, 0.037 / 0.037, 0.037 | within noise (control) |
| conv B=32 / rust | 0.006 (0.006-0.006) | 0.006 (0.006-0.006) | +0.4% | 0.006, 0.006 / 0.006, 0.006 | separated, inside spread (control) |
| conv single / numpy | 0.037 (0.037-0.038) | 0.037 (0.037-0.038) | +0.0% | 0.037, 0.037 / 0.037, 0.037 | within noise (control) |
| conv single / rust | 0.006 (0.006-0.006) | 0.006 (0.006-0.006) | +1.7% | 0.006, 0.006 / 0.006, 0.006 | within noise (control) |

### epoch, loader

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 0.602 (0.594-0.615) | 0.611 (0.592-0.626) | +1.5% | 0.606, 0.598 / 0.620, 0.606 | within noise |
| dense B=32 / rust | 0.549 (0.542-0.563) | 0.552 (0.547-0.566) | +0.5% | 0.553, 0.548 / 0.552, 0.552 | within noise |
| dense single / numpy | 6.124 (6.056-6.234) | 5.946 (5.905-6.229) | -2.9% | 6.119, 6.146 / 5.945, 5.970 | consistent |
| dense single / rust | 1.252 (1.235-1.283) | 1.215 (1.197-1.239) | -2.9% | 1.253, 1.247 / 1.214, 1.216 | consistent |
| conv B=32 / numpy | 0.371 (0.355-0.377) | 0.371 (0.363-0.376) | +0.1% | 0.363, 0.371 / 0.367, 0.371 | within noise |
| conv B=32 / rust | 0.304 (0.301-0.326) | 0.303 (0.300-0.308) | -0.3% | 0.304, 0.305 / 0.302, 0.304 | within noise |
| conv single / numpy | 1.139 (1.134-1.156) | 1.143 (1.130-1.170) | +0.3% | 1.152, 1.138 / 1.137, 1.156 | within noise |
| conv single / rust | 0.456 (0.453-0.470) | 0.455 (0.453-0.470) | -0.2% | 0.456, 0.456 / 0.455, 0.456 | within noise |
