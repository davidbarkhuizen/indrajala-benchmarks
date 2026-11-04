Old `0d91d1a` against new `0d91d1a`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/prepared_dataset_timing.py time --configs conv B=32 conv B=512 dense B=32 dense B=512 --repeats 2 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `6a8190c` (extension sha256 `84ec4e85d91b`) and new crate `7b9878f` (extension sha256 `21b07c2bef84`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 4.73 (HIGH); busy processes: none. Each row pools 6 runs per side.

- CONTROL MOVED: 4 of 8 control rows consistent, e.g. prepare / conv B=512 / rust -7.9%: changes about that size can't be resolved here (next: epoch_op_profile.py)
- 16 rows within noise (1 separated inside their spread), max |Δ| 2.4%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.410 (0.406-0.414) | 0.409 (0.407-0.414) | -0.3% | 0.410, 0.410, 0.412 / 0.412, 0.408, 0.410 | within noise |
| conv B=32 / rust | 0.318 (0.311-0.335) | 0.325 (0.310-0.331) | +2.4% | 0.321, 0.329, 0.312 / 0.331, 0.325, 0.311 | within noise |
| conv B=512 / numpy | 0.399 (0.395-0.408) | 0.402 (0.400-0.407) | +0.8% | 0.397, 0.404, 0.402 / 0.402, 0.402, 0.403 | within noise |
| conv B=512 / rust | 0.358 (0.342-0.366) | 0.351 (0.347-0.357) | -2.1% | 0.354, 0.361, 0.352 / 0.349, 0.350, 0.357 | within noise |
| dense B=32 / numpy | 1.676 (1.668-1.690) | 1.687 (1.664-1.699) | +0.6% | 1.682, 1.678, 1.674 / 1.682, 1.674, 1.694 | within noise |
| dense B=32 / rust | 0.763 (0.758-0.767) | 0.756 (0.747-0.768) | -0.9% | 0.763, 0.763, 0.763 / 0.764, 0.750, 0.759 | within noise |
| dense B=512 / numpy | 1.436 (1.430-1.440) | 1.436 (1.430-1.440) | -0.0% | 1.436, 1.437, 1.435 / 1.436, 1.431, 1.439 | within noise |
| dense B=512 / rust | 0.638 (0.633-0.645) | 0.631 (0.627-0.634) | -1.1% | 0.638, 0.639, 0.638 / 0.633, 0.628, 0.630 | separated, inside spread |

### prepare

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.037 (0.037-0.038) | 0.037 (0.037-0.037) | -0.1% | 0.037, 0.037, 0.037 / 0.037, 0.037, 0.037 | within noise (control) |
| conv B=32 / rust | 0.006 (0.006-0.006) | 0.006 (0.006-0.006) | -5.8% | 0.006, 0.006, 0.006 / 0.006, 0.006, 0.006 | consistent (control) |
| conv B=512 / numpy | 0.038 (0.037-0.038) | 0.038 (0.037-0.038) | +0.5% | 0.038, 0.038, 0.038 / 0.038, 0.038, 0.038 | within noise (control) |
| conv B=512 / rust | 0.007 (0.007-0.007) | 0.006 (0.006-0.006) | -7.9% | 0.007, 0.007, 0.007 / 0.006, 0.006, 0.006 | consistent (control) |
| dense B=32 / numpy | 1.078 (1.077-1.082) | 1.078 (1.074-1.081) | -0.0% | 1.079, 1.080, 1.077 / 1.081, 1.075, 1.078 | within noise (control) |
| dense B=32 / rust | 0.209 (0.208-0.210) | 0.200 (0.198-0.201) | -4.4% | 0.209, 0.209, 0.209 / 0.199, 0.200, 0.200 | consistent (control) |
| dense B=512 / numpy | 1.074 (1.071-1.081) | 1.073 (1.070-1.081) | -0.0% | 1.072, 1.074, 1.078 / 1.071, 1.078, 1.075 | within noise (control) |
| dense B=512 / rust | 0.209 (0.208-0.210) | 0.200 (0.198-0.200) | -4.2% | 0.209, 0.209, 0.209 / 0.200, 0.199, 0.200 | consistent (control) |

### epoch, loader

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.379 (0.367-0.386) | 0.377 (0.372-0.383) | -0.6% | 0.367, 0.379, 0.384 / 0.375, 0.377, 0.379 | within noise |
| conv B=32 / rust | 0.311 (0.305-0.325) | 0.317 (0.305-0.326) | +1.9% | 0.315, 0.320, 0.306 / 0.324, 0.317, 0.305 | within noise |
| conv B=512 / numpy | 0.366 (0.356-0.373) | 0.368 (0.365-0.376) | +0.5% | 0.361, 0.369, 0.366 / 0.367, 0.367, 0.372 | within noise |
| conv B=512 / rust | 0.329 (0.320-0.337) | 0.325 (0.319-0.333) | -1.3% | 0.329, 0.336, 0.324 / 0.321, 0.325, 0.330 | within noise |
| dense B=32 / numpy | 0.605 (0.596-0.614) | 0.609 (0.591-0.621) | +0.5% | 0.611, 0.604, 0.601 / 0.608, 0.598, 0.616 | within noise |
| dense B=32 / rust | 0.556 (0.548-0.561) | 0.556 (0.552-0.572) | +0.1% | 0.553, 0.557, 0.555 / 0.568, 0.555, 0.554 | within noise |
| dense B=512 / numpy | 0.359 (0.353-0.364) | 0.358 (0.356-0.364) | -0.3% | 0.357, 0.361, 0.358 / 0.361, 0.356, 0.360 | within noise |
| dense B=512 / rust | 0.431 (0.427-0.435) | 0.433 (0.422-0.435) | +0.5% | 0.433, 0.430, 0.431 / 0.434, 0.428, 0.433 | within noise |
