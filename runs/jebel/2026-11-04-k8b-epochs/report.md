Old `f59388b` against new `f59388b`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/prepared_dataset_timing.py time --configs conv B=32 conv B=512 dense B=32 dense B=512 --repeats 2 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `4dba70e` (extension sha256 `f5c8b6404a1d`) and new crate `ce5a267` (extension sha256 `24bdf26aceef`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 3.29 (HIGH); busy processes: none. Each row pools 6 runs per side.

- CONTROL MOVED: 4 of 8 control rows consistent, e.g. prepare / conv B=32 / rust -6.3%: changes about that size can't be resolved here (next: epoch_op_profile.py)
- consistent: epoch, loader / dense B=512 / rust -8.6% (0.429 -> 0.392 s)
- consistent: epoch, loader / dense B=32 / rust -8.5% (0.556 -> 0.509 s)
- consistent: epoch / dense B=32 / rust -7.8% (0.763 -> 0.703 s)
- consistent: epoch / dense B=512 / rust -6.0% (0.640 -> 0.602 s)
- 12 rows within noise (3 separated inside their spread), max |Δ| 1.7%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.409 (0.408-0.412) | 0.407 (0.402-0.410) | -0.5% | 0.408, 0.409, 0.411 / 0.406, 0.407, 0.406 | separated, inside spread |
| conv B=32 / rust | 0.313 (0.308-0.332) | 0.310 (0.304-0.329) | -0.9% | 0.320, 0.312, 0.321 / 0.322, 0.305, 0.309 | within noise |
| conv B=512 / numpy | 0.399 (0.395-0.411) | 0.402 (0.393-0.412) | +0.9% | 0.396, 0.404, 0.404 / 0.401, 0.401, 0.407 | within noise |
| conv B=512 / rust | 0.354 (0.350-0.358) | 0.352 (0.345-0.355) | -0.7% | 0.354, 0.356, 0.352 / 0.353, 0.352, 0.347 | within noise |
| dense B=32 / numpy | 1.684 (1.667-1.692) | 1.672 (1.667-1.687) | -0.7% | 1.679, 1.677, 1.687 / 1.674, 1.668, 1.679 | within noise |
| dense B=32 / rust | 0.763 (0.759-0.768) | 0.703 (0.702-0.711) | -7.8% | 0.760, 0.766, 0.764 / 0.707, 0.702, 0.706 | consistent |
| dense B=512 / numpy | 1.442 (1.438-1.444) | 1.435 (1.430-1.439) | -0.5% | 1.442, 1.442, 1.441 / 1.438, 1.432, 1.435 | separated, inside spread |
| dense B=512 / rust | 0.640 (0.637-0.642) | 0.602 (0.597-0.605) | -6.0% | 0.639, 0.639, 0.642 / 0.602, 0.600, 0.603 | consistent |

### prepare

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.037 (0.037-0.038) | 0.037 (0.037-0.038) | -0.1% | 0.037, 0.037, 0.038 / 0.037, 0.038, 0.038 | within noise (control) |
| conv B=32 / rust | 0.006 (0.006-0.006) | 0.006 (0.006-0.006) | -6.3% | 0.006, 0.006, 0.006 / 0.006, 0.006, 0.006 | consistent (control) |
| conv B=512 / numpy | 0.038 (0.037-0.038) | 0.038 (0.037-0.038) | +0.0% | 0.038, 0.038, 0.038 / 0.038, 0.038, 0.038 | within noise (control) |
| conv B=512 / rust | 0.007 (0.007-0.007) | 0.006 (0.006-0.007) | -5.8% | 0.007, 0.007, 0.007 / 0.007, 0.006, 0.006 | consistent (control) |
| dense B=32 / numpy | 1.078 (1.076-1.079) | 1.079 (1.075-1.090) | +0.1% | 1.078, 1.077, 1.079 / 1.080, 1.083, 1.077 | within noise (control) |
| dense B=32 / rust | 0.208 (0.208-0.211) | 0.198 (0.197-0.200) | -4.9% | 0.208, 0.209, 0.209 / 0.198, 0.199, 0.198 | consistent (control) |
| dense B=512 / numpy | 1.076 (1.069-1.078) | 1.078 (1.071-1.088) | +0.2% | 1.073, 1.076, 1.075 / 1.075, 1.079, 1.083 | within noise (control) |
| dense B=512 / rust | 0.210 (0.208-0.216) | 0.199 (0.198-0.200) | -5.2% | 0.213, 0.210, 0.209 / 0.199, 0.199, 0.198 | consistent (control) |

### epoch, loader

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.380 (0.365-0.385) | 0.377 (0.372-0.381) | -0.7% | 0.370, 0.380, 0.382 / 0.374, 0.378, 0.378 | within noise |
| conv B=32 / rust | 0.305 (0.303-0.324) | 0.300 (0.294-0.316) | -1.6% | 0.314, 0.305, 0.313 / 0.312, 0.295, 0.300 | within noise |
| conv B=512 / numpy | 0.368 (0.361-0.376) | 0.367 (0.366-0.372) | -0.3% | 0.364, 0.368, 0.374 / 0.366, 0.367, 0.370 | within noise |
| conv B=512 / rust | 0.324 (0.313-0.330) | 0.326 (0.317-0.334) | +0.6% | 0.322, 0.328, 0.320 / 0.331, 0.326, 0.318 | within noise |
| dense B=32 / numpy | 0.606 (0.595-0.615) | 0.598 (0.592-0.613) | -1.4% | 0.604, 0.599, 0.612 / 0.599, 0.594, 0.605 | within noise |
| dense B=32 / rust | 0.556 (0.553-0.564) | 0.509 (0.507-0.517) | -8.5% | 0.556, 0.557, 0.559 / 0.511, 0.508, 0.513 | consistent |
| dense B=512 / numpy | 0.361 (0.357-0.363) | 0.355 (0.353-0.361) | -1.7% | 0.360, 0.362, 0.360 / 0.358, 0.354, 0.357 | separated, inside spread |
| dense B=512 / rust | 0.429 (0.428-0.431) | 0.392 (0.389-0.396) | -8.6% | 0.430, 0.430, 0.429 / 0.393, 0.391, 0.394 | consistent |
