Old `515849f` against new `515849f`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/prepared_dataset_timing.py time --configs conv B=32 conv B=512 dense B=32 dense B=512 --repeats 2 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `cba601e` (extension sha256 `bc8a4a1fc83d`) and new crate `dc571a0` (extension sha256 `1cebe6ff7934`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 3.48 (HIGH); busy processes: none. Each row pools 6 runs per side.

- CONTROL MOVED: 4 of 8 control rows consistent, e.g. prepare / conv B=512 / rust +7.2%: changes about that size can't be resolved here (next: epoch_op_profile.py)
- 16 rows within noise (1 separated inside their spread), max |Δ| 2.7%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.413 (0.407-0.421) | 0.413 (0.406-0.419) | +0.1% | 0.411, 0.414, 0.415 / 0.413, 0.412, 0.415 | within noise |
| conv B=32 / rust | 0.325 (0.306-0.326) | 0.316 (0.307-0.326) | -2.6% | 0.326, 0.325, 0.306 / 0.321, 0.312, 0.313 | within noise |
| conv B=512 / numpy | 0.404 (0.398-0.414) | 0.405 (0.398-0.413) | +0.3% | 0.402, 0.407, 0.408 / 0.405, 0.404, 0.406 | within noise |
| conv B=512 / rust | 0.354 (0.347-0.359) | 0.350 (0.346-0.363) | -1.1% | 0.358, 0.354, 0.349 / 0.355, 0.358, 0.346 | within noise |
| dense B=32 / numpy | 1.692 (1.679-1.705) | 1.689 (1.678-1.709) | -0.1% | 1.684, 1.703, 1.692 / 1.678, 1.701, 1.694 | within noise |
| dense B=32 / rust | 0.713 (0.701-0.714) | 0.710 (0.706-0.727) | -0.3% | 0.713, 0.714, 0.702 / 0.709, 0.726, 0.708 | within noise |
| dense B=512 / numpy | 1.447 (1.436-1.460) | 1.445 (1.439-1.456) | -0.1% | 1.440, 1.448, 1.450 / 1.445, 1.439, 1.453 | within noise |
| dense B=512 / rust | 0.600 (0.595-0.606) | 0.610 (0.605-0.617) | +1.6% | 0.599, 0.606, 0.598 / 0.607, 0.615, 0.608 | separated, inside spread |

### prepare

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.038 (0.037-0.038) | 0.038 (0.037-0.038) | -0.6% | 0.037, 0.038, 0.038 / 0.037, 0.038, 0.038 | within noise (control) |
| conv B=32 / rust | 0.006 (0.006-0.006) | 0.006 (0.006-0.006) | +5.6% | 0.006, 0.006, 0.006 / 0.006, 0.006, 0.006 | consistent (control) |
| conv B=512 / numpy | 0.038 (0.037-0.039) | 0.038 (0.038-0.039) | +0.2% | 0.038, 0.038, 0.038 / 0.038, 0.038, 0.038 | within noise (control) |
| conv B=512 / rust | 0.006 (0.006-0.007) | 0.007 (0.007-0.007) | +7.2% | 0.006, 0.006, 0.006 / 0.007, 0.007, 0.007 | consistent (control) |
| dense B=32 / numpy | 1.095 (1.081-1.104) | 1.082 (1.078-1.100) | -1.2% | 1.083, 1.095, 1.101 / 1.082, 1.079, 1.093 | within noise (control) |
| dense B=32 / rust | 0.200 (0.200-0.203) | 0.210 (0.208-0.214) | +5.1% | 0.200, 0.200, 0.201 / 0.209, 0.213, 0.211 | consistent (control) |
| dense B=512 / numpy | 1.088 (1.077-1.108) | 1.090 (1.078-1.106) | +0.2% | 1.078, 1.095, 1.100 / 1.091, 1.081, 1.099 | within noise (control) |
| dense B=512 / rust | 0.200 (0.199-0.204) | 0.211 (0.209-0.211) | +5.2% | 0.200, 0.203, 0.200 / 0.210, 0.211, 0.210 | consistent (control) |

### epoch, loader

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.384 (0.369-0.389) | 0.384 (0.381-0.387) | +0.2% | 0.376, 0.385, 0.384 / 0.383, 0.384, 0.384 | within noise |
| conv B=32 / rust | 0.314 (0.296-0.340) | 0.305 (0.295-0.313) | -2.7% | 0.305, 0.314, 0.319 / 0.310, 0.300, 0.302 | within noise |
| conv B=512 / numpy | 0.371 (0.369-0.372) | 0.371 (0.368-0.373) | +0.1% | 0.370, 0.371, 0.371 / 0.372, 0.371, 0.369 | within noise |
| conv B=512 / rust | 0.323 (0.318-0.330) | 0.325 (0.319-0.337) | +0.7% | 0.325, 0.321, 0.324 / 0.328, 0.331, 0.320 | within noise |
| dense B=32 / numpy | 0.608 (0.596-0.617) | 0.607 (0.594-0.617) | -0.2% | 0.608, 0.616, 0.598 / 0.597, 0.617, 0.606 | within noise |
| dense B=32 / rust | 0.504 (0.491-0.507) | 0.493 (0.489-0.517) | -2.3% | 0.506, 0.504, 0.491 / 0.493, 0.512, 0.490 | within noise |
| dense B=512 / numpy | 0.360 (0.355-0.365) | 0.363 (0.359-0.367) | +1.0% | 0.360, 0.363, 0.355 / 0.365, 0.364, 0.361 | within noise |
| dense B=512 / rust | 0.400 (0.396-0.406) | 0.398 (0.397-0.404) | -0.5% | 0.397, 0.404, 0.400 / 0.397, 0.403, 0.398 | within noise |
