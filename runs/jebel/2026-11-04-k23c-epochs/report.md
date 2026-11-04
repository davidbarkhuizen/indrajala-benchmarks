Old `bb60c11` against new `bb60c11`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/prepared_dataset_timing.py time --configs conv B=32 conv B=512 dense B=32 dense B=512 --repeats 2 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `10aa3e5` (extension sha256 `24bdf26aceef`) and new crate `3bb2a40` (extension sha256 `bb3d5611c37d`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 3.22 (HIGH); busy processes: none. Each row pools 6 runs per side.

- controls: 8 rows, all within noise
- consistent: epoch, loader / dense B=512 / rust +3.4% (0.389 -> 0.402 s)
- consistent: epoch, loader / conv B=512 / rust +2.5% (0.319 -> 0.328 s)
- 14 rows within noise (2 separated inside their spread), max |Δ| 2.0%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.409 (0.405-0.422) | 0.408 (0.406-0.414) | -0.3% | 0.416, 0.406, 0.413 / 0.408, 0.407, 0.411 | within noise |
| conv B=32 / rust | 0.306 (0.305-0.314) | 0.310 (0.305-0.328) | +1.5% | 0.306, 0.306, 0.310 / 0.314, 0.307, 0.317 | within noise |
| conv B=512 / numpy | 0.400 (0.397-0.409) | 0.402 (0.396-0.408) | +0.4% | 0.398, 0.404, 0.404 / 0.401, 0.403, 0.402 | within noise |
| conv B=512 / rust | 0.344 (0.341-0.348) | 0.351 (0.346-0.357) | +2.0% | 0.344, 0.346, 0.343 / 0.354, 0.351, 0.349 | separated, inside spread |
| dense B=32 / numpy | 1.671 (1.662-1.674) | 1.674 (1.669-1.681) | +0.2% | 1.668, 1.672, 1.671 / 1.676, 1.676, 1.671 | within noise |
| dense B=32 / rust | 0.702 (0.699-0.704) | 0.705 (0.701-0.709) | +0.5% | 0.701, 0.702, 0.702 / 0.709, 0.704, 0.702 | separated, inside spread |
| dense B=512 / numpy | 1.433 (1.430-1.447) | 1.434 (1.427-1.442) | +0.1% | 1.433, 1.433, 1.439 / 1.432, 1.437, 1.434 | within noise |
| dense B=512 / rust | 0.600 (0.596-0.607) | 0.603 (0.597-0.608) | +0.5% | 0.603, 0.599, 0.600 / 0.606, 0.602, 0.599 | within noise |

### prepare

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.038 (0.037-0.038) | 0.037 (0.037-0.038) | -0.5% | 0.037, 0.038, 0.038 / 0.037, 0.037, 0.038 | within noise (control) |
| conv B=32 / rust | 0.006 (0.006-0.006) | 0.006 (0.006-0.006) | +0.8% | 0.006, 0.006, 0.006 / 0.006, 0.006, 0.006 | within noise (control) |
| conv B=512 / numpy | 0.038 (0.038-0.039) | 0.038 (0.037-0.038) | -0.2% | 0.038, 0.038, 0.038 / 0.038, 0.038, 0.038 | within noise (control) |
| conv B=512 / rust | 0.006 (0.006-0.007) | 0.006 (0.006-0.007) | +0.8% | 0.006, 0.006, 0.006 / 0.006, 0.006, 0.006 | within noise (control) |
| dense B=32 / numpy | 1.079 (1.077-1.086) | 1.078 (1.072-1.081) | -0.1% | 1.078, 1.083, 1.080 / 1.079, 1.075, 1.080 | within noise (control) |
| dense B=32 / rust | 0.197 (0.196-0.198) | 0.197 (0.196-0.199) | +0.2% | 0.198, 0.197, 0.198 / 0.198, 0.197, 0.198 | within noise (control) |
| dense B=512 / numpy | 1.077 (1.075-1.093) | 1.079 (1.077-1.094) | +0.1% | 1.075, 1.079, 1.086 / 1.079, 1.077, 1.091 | within noise (control) |
| dense B=512 / rust | 0.198 (0.196-0.200) | 0.198 (0.197-0.199) | -0.1% | 0.198, 0.199, 0.198 / 0.198, 0.198, 0.199 | within noise (control) |

### epoch, loader

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.379 (0.373-0.390) | 0.382 (0.377-0.383) | +0.6% | 0.381, 0.379, 0.382 / 0.379, 0.381, 0.383 | within noise |
| conv B=32 / rust | 0.297 (0.294-0.303) | 0.300 (0.296-0.314) | +1.1% | 0.298, 0.296, 0.298 / 0.303, 0.298, 0.307 | within noise |
| conv B=512 / numpy | 0.369 (0.362-0.374) | 0.368 (0.366-0.373) | -0.1% | 0.365, 0.371, 0.372 / 0.367, 0.371, 0.369 | within noise |
| conv B=512 / rust | 0.319 (0.316-0.326) | 0.328 (0.321-0.336) | +2.5% | 0.317, 0.320, 0.321 / 0.331, 0.328, 0.326 | consistent |
| dense B=32 / numpy | 0.595 (0.591-0.617) | 0.598 (0.595-0.602) | +0.6% | 0.592, 0.606, 0.597 / 0.598, 0.599, 0.596 | within noise |
| dense B=32 / rust | 0.507 (0.505-0.509) | 0.508 (0.505-0.514) | +0.2% | 0.507, 0.508, 0.506 / 0.510, 0.508, 0.508 | within noise |
| dense B=512 / numpy | 0.356 (0.353-0.360) | 0.355 (0.353-0.364) | -0.2% | 0.357, 0.356, 0.357 / 0.356, 0.360, 0.354 | within noise |
| dense B=512 / rust | 0.389 (0.387-0.393) | 0.402 (0.399-0.407) | +3.4% | 0.389, 0.388, 0.393 / 0.406, 0.401, 0.401 | consistent |
