Old `5cf590a` against new `5cf590a`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/prepared_dataset_timing.py time --configs conv B=32 conv B=512 dense B=32 dense B=512 --repeats 2 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `238a017` (extension sha256 `bb3d5611c37d`) and new crate `18ce111` (extension sha256 `bc8a4a1fc83d`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 5.08 (HIGH); busy processes: none. Each row pools 6 runs per side.

- controls: 8 rows, all within noise
- 16 rows within noise (3 separated inside their spread), max |Δ| 2.5%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.409 (0.407-0.412) | 0.409 (0.406-0.410) | -0.2% | 0.407, 0.409, 0.411 / 0.407, 0.408, 0.410 | within noise |
| conv B=32 / rust | 0.309 (0.306-0.317) | 0.307 (0.305-0.322) | -0.6% | 0.312, 0.309, 0.311 / 0.314, 0.306, 0.313 | within noise |
| conv B=512 / numpy | 0.398 (0.396-0.412) | 0.402 (0.396-0.411) | +0.9% | 0.398, 0.404, 0.404 / 0.400, 0.404, 0.405 | within noise |
| conv B=512 / rust | 0.351 (0.346-0.366) | 0.347 (0.345-0.353) | -1.3% | 0.349, 0.359, 0.350 / 0.346, 0.347, 0.350 | within noise |
| dense B=32 / numpy | 1.677 (1.662-1.695) | 1.675 (1.666-1.677) | -0.1% | 1.677, 1.666, 1.694 / 1.676, 1.671, 1.673 | within noise |
| dense B=32 / rust | 0.703 (0.700-0.709) | 0.707 (0.694-0.712) | +0.5% | 0.706, 0.703, 0.703 / 0.707, 0.694, 0.712 | within noise |
| dense B=512 / numpy | 1.433 (1.428-1.436) | 1.434 (1.431-1.440) | +0.1% | 1.431, 1.433, 1.433 / 1.431, 1.434, 1.439 | within noise |
| dense B=512 / rust | 0.606 (0.603-0.609) | 0.595 (0.593-0.609) | -1.9% | 0.606, 0.605, 0.607 / 0.602, 0.596, 0.593 | separated, inside spread |

### prepare

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.037 (0.037-0.038) | 0.037 (0.037-0.038) | +0.0% | 0.037, 0.037, 0.038 / 0.037, 0.037, 0.037 | within noise (control) |
| conv B=32 / rust | 0.006 (0.006-0.007) | 0.006 (0.006-0.006) | -0.1% | 0.006, 0.006, 0.006 / 0.006, 0.006, 0.006 | within noise (control) |
| conv B=512 / numpy | 0.038 (0.038-0.039) | 0.038 (0.037-0.038) | -0.5% | 0.038, 0.038, 0.038 / 0.038, 0.038, 0.038 | within noise (control) |
| conv B=512 / rust | 0.006 (0.006-0.006) | 0.006 (0.006-0.007) | +0.8% | 0.006, 0.006, 0.006 / 0.006, 0.006, 0.007 | separated, inside spread (control) |
| dense B=32 / numpy | 1.081 (1.077-1.087) | 1.077 (1.076-1.080) | -0.3% | 1.077, 1.081, 1.086 / 1.077, 1.077, 1.079 | within noise (control) |
| dense B=32 / rust | 0.198 (0.197-0.200) | 0.198 (0.198-0.201) | +0.1% | 0.197, 0.198, 0.199 / 0.198, 0.198, 0.200 | within noise (control) |
| dense B=512 / numpy | 1.079 (1.072-1.086) | 1.076 (1.075-1.093) | -0.2% | 1.075, 1.082, 1.080 / 1.077, 1.076, 1.084 | within noise (control) |
| dense B=512 / rust | 0.199 (0.199-0.201) | 0.200 (0.197-0.203) | +0.0% | 0.199, 0.200, 0.200 / 0.200, 0.201, 0.198 | within noise (control) |

### epoch, loader

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.381 (0.365-0.383) | 0.381 (0.376-0.385) | -0.0% | 0.369, 0.381, 0.383 / 0.378, 0.383, 0.382 | within noise |
| conv B=32 / rust | 0.299 (0.296-0.305) | 0.298 (0.296-0.315) | -0.2% | 0.303, 0.297, 0.300 / 0.306, 0.298, 0.305 | within noise |
| conv B=512 / numpy | 0.369 (0.363-0.370) | 0.369 (0.366-0.373) | +0.0% | 0.365, 0.369, 0.370 / 0.366, 0.369, 0.372 | within noise |
| conv B=512 / rust | 0.327 (0.318-0.331) | 0.323 (0.321-0.330) | -1.2% | 0.325, 0.329, 0.322 / 0.321, 0.323, 0.329 | within noise |
| dense B=32 / numpy | 0.597 (0.581-0.612) | 0.598 (0.592-0.602) | +0.2% | 0.603, 0.587, 0.605 / 0.596, 0.597, 0.599 | within noise |
| dense B=32 / rust | 0.508 (0.505-0.517) | 0.496 (0.489-0.507) | -2.5% | 0.513, 0.507, 0.507 / 0.500, 0.490, 0.502 | separated, inside spread |
| dense B=512 / numpy | 0.357 (0.352-0.360) | 0.356 (0.353-0.361) | -0.2% | 0.356, 0.355, 0.359 / 0.354, 0.356, 0.360 | within noise |
| dense B=512 / rust | 0.406 (0.402-0.409) | 0.396 (0.394-0.405) | -2.5% | 0.407, 0.406, 0.406 / 0.405, 0.395, 0.395 | separated, inside spread |
