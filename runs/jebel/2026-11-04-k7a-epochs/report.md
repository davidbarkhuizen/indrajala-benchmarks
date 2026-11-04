Old `cb31225` against new `cb31225`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/prepared_dataset_timing.py time --configs conv B=32 conv B=512 dense B=32 dense B=512 --repeats 2 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `690bce8` (extension sha256 `7ba3057a73f7`) and new crate `5a19b18` (extension sha256 `84ec4e85d91b`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.76 (HIGH); busy processes: none. Each row pools 6 runs per side.

- CONTROL MOVED: 3 of 8 control rows consistent, e.g. prepare / dense B=512 / rust +6.3%: changes about that size can't be resolved here (next: epoch_op_profile.py)
- 16 rows within noise (2 separated inside their spread), max |Δ| 3.0%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.409 (0.404-0.415) | 0.411 (0.410-0.420) | +0.5% | 0.405, 0.411, 0.413 / 0.410, 0.416, 0.412 | within noise |
| conv B=32 / rust | 0.317 (0.310-0.331) | 0.321 (0.311-0.330) | +1.3% | 0.311, 0.327, 0.316 / 0.321, 0.325, 0.316 | within noise |
| conv B=512 / numpy | 0.400 (0.395-0.407) | 0.402 (0.399-0.405) | +0.6% | 0.398, 0.398, 0.404 / 0.399, 0.404, 0.402 | within noise |
| conv B=512 / rust | 0.357 (0.349-0.360) | 0.355 (0.350-0.362) | -0.6% | 0.357, 0.359, 0.349 / 0.358, 0.353, 0.354 | within noise |
| dense B=32 / numpy | 1.681 (1.675-1.689) | 1.685 (1.669-1.702) | +0.3% | 1.678, 1.678, 1.687 / 1.691, 1.694, 1.672 | within noise |
| dense B=32 / rust | 0.748 (0.745-0.757) | 0.770 (0.761-0.778) | +3.0% | 0.747, 0.751, 0.752 / 0.775, 0.770, 0.761 | separated, inside spread |
| dense B=512 / numpy | 1.436 (1.427-1.442) | 1.435 (1.431-1.443) | -0.0% | 1.438, 1.431, 1.438 / 1.443, 1.434, 1.433 | within noise |
| dense B=512 / rust | 0.631 (0.627-0.638) | 0.643 (0.641-0.656) | +1.9% | 0.629, 0.631, 0.636 / 0.649, 0.645, 0.642 | separated, inside spread |

### prepare

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.038 (0.037-0.038) | 0.037 (0.037-0.038) | -0.2% | 0.038, 0.037, 0.037 / 0.037, 0.037, 0.037 | separated, inside spread (control) |
| conv B=32 / rust | 0.006 (0.006-0.006) | 0.006 (0.006-0.007) | +6.1% | 0.006, 0.006, 0.006 / 0.006, 0.006, 0.006 | separated, inside spread (control) |
| conv B=512 / numpy | 0.038 (0.037-0.038) | 0.038 (0.037-0.038) | +0.4% | 0.038, 0.038, 0.038 / 0.038, 0.038, 0.038 | within noise (control) |
| conv B=512 / rust | 0.006 (0.006-0.007) | 0.007 (0.007-0.007) | +5.6% | 0.006, 0.006, 0.006 / 0.007, 0.007, 0.007 | consistent (control) |
| dense B=32 / numpy | 1.078 (1.077-1.082) | 1.079 (1.076-1.081) | +0.1% | 1.077, 1.080, 1.079 / 1.080, 1.080, 1.076 | within noise (control) |
| dense B=32 / rust | 0.197 (0.196-0.199) | 0.209 (0.208-0.210) | +6.0% | 0.197, 0.197, 0.198 / 0.209, 0.209, 0.210 | consistent (control) |
| dense B=512 / numpy | 1.076 (1.067-1.079) | 1.074 (1.070-1.078) | -0.2% | 1.076, 1.074, 1.072 / 1.076, 1.073, 1.073 | within noise (control) |
| dense B=512 / rust | 0.199 (0.196-0.200) | 0.212 (0.209-0.219) | +6.3% | 0.199, 0.198, 0.200 / 0.212, 0.210, 0.216 | consistent (control) |

### epoch, loader

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.378 (0.362-0.383) | 0.376 (0.371-0.378) | -0.4% | 0.365, 0.378, 0.381 / 0.374, 0.377, 0.376 | within noise |
| conv B=32 / rust | 0.308 (0.302-0.323) | 0.312 (0.304-0.324) | +1.3% | 0.303, 0.319, 0.308 / 0.313, 0.319, 0.307 | within noise |
| conv B=512 / numpy | 0.364 (0.359-0.370) | 0.365 (0.364-0.371) | +0.3% | 0.362, 0.366, 0.366 / 0.365, 0.367, 0.365 | within noise |
| conv B=512 / rust | 0.325 (0.319-0.329) | 0.327 (0.319-0.340) | +0.5% | 0.325, 0.328, 0.321 / 0.336, 0.321, 0.326 | within noise |
| dense B=32 / numpy | 0.606 (0.598-0.613) | 0.610 (0.596-0.621) | +0.6% | 0.603, 0.602, 0.612 / 0.615, 0.616, 0.599 | within noise |
| dense B=32 / rust | 0.553 (0.549-0.563) | 0.563 (0.554-0.570) | +1.7% | 0.553, 0.556, 0.558 / 0.566, 0.563, 0.555 | within noise |
| dense B=512 / numpy | 0.359 (0.353-0.365) | 0.359 (0.355-0.361) | +0.0% | 0.361, 0.354, 0.362 / 0.361, 0.359, 0.357 | within noise |
| dense B=512 / rust | 0.436 (0.434-0.441) | 0.434 (0.431-0.438) | -0.4% | 0.436, 0.437, 0.437 / 0.435, 0.436, 0.432 | within noise |
