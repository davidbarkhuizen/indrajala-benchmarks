Old `0b17d22` against new `0b17d22`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/prepared_dataset_timing.py time --configs conv B=32 conv B=512 dense B=32 dense B=512 --repeats 2 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `edce2de` (extension sha256 `f72612f402e8`) and new crate `51a2baf` (extension sha256 `7194f34f6ce9`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 3.94 (HIGH); busy processes: none. Each row pools 6 runs per side.

- CONTROL MOVED: 3 of 8 control rows consistent, e.g. prepare / conv B=32 / rust +5.1%: changes about that size can't be resolved here (next: epoch_op_profile.py)
- consistent: epoch, loader / dense B=512 / rust -4.9% (0.407 -> 0.387 s)
- 15 rows within noise (3 separated inside their spread), max |Δ| 5.8%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.414 (0.409-0.421) | 0.415 (0.407-0.419) | +0.3% | 0.412, 0.414, 0.416 / 0.411, 0.417, 0.417 | within noise |
| conv B=32 / rust | 0.326 (0.304-0.328) | 0.307 (0.306-0.326) | -5.8% | 0.320, 0.327, 0.316 / 0.306, 0.317, 0.312 | within noise |
| conv B=512 / numpy | 0.406 (0.395-0.414) | 0.406 (0.398-0.410) | -0.1% | 0.405, 0.408, 0.404 / 0.402, 0.407, 0.406 | within noise |
| conv B=512 / rust | 0.356 (0.352-0.362) | 0.337 (0.325-0.345) | -5.4% | 0.356, 0.354, 0.361 / 0.335, 0.344, 0.331 | separated, inside spread |
| dense B=32 / numpy | 1.672 (1.661-1.684) | 1.666 (1.657-1.683) | -0.4% | 1.672, 1.673, 1.671 / 1.660, 1.673, 1.671 | within noise |
| dense B=32 / rust | 0.716 (0.708-0.720) | 0.713 (0.709-0.736) | -0.4% | 0.713, 0.713, 0.719 / 0.710, 0.724, 0.720 | within noise |
| dense B=512 / numpy | 1.439 (1.434-1.443) | 1.432 (1.431-1.446) | -0.5% | 1.436, 1.441, 1.439 / 1.432, 1.432, 1.442 | within noise |
| dense B=512 / rust | 0.604 (0.600-0.607) | 0.593 (0.589-0.602) | -1.9% | 0.606, 0.604, 0.602 / 0.592, 0.591, 0.598 | separated, inside spread |

### prepare

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.037 (0.037-0.038) | 0.037 (0.037-0.038) | +0.1% | 0.037, 0.038, 0.038 / 0.037, 0.037, 0.038 | within noise (control) |
| conv B=32 / rust | 0.006 (0.006-0.006) | 0.006 (0.006-0.006) | +5.1% | 0.006, 0.006, 0.006 / 0.006, 0.006, 0.006 | consistent (control) |
| conv B=512 / numpy | 0.038 (0.037-0.038) | 0.038 (0.038-0.038) | +0.8% | 0.038, 0.038, 0.038 / 0.038, 0.038, 0.038 | separated, inside spread (control) |
| conv B=512 / rust | 0.006 (0.006-0.007) | 0.007 (0.007-0.007) | +2.5% | 0.007, 0.006, 0.006 / 0.007, 0.007, 0.007 | separated, inside spread (control) |
| dense B=32 / numpy | 1.077 (1.075-1.081) | 1.081 (1.078-1.082) | +0.3% | 1.078, 1.078, 1.077 / 1.082, 1.078, 1.081 | within noise (control) |
| dense B=32 / rust | 0.198 (0.197-0.198) | 0.207 (0.206-0.209) | +4.8% | 0.197, 0.198, 0.198 / 0.208, 0.207, 0.208 | consistent (control) |
| dense B=512 / numpy | 1.078 (1.076-1.083) | 1.079 (1.076-1.090) | +0.1% | 1.077, 1.078, 1.080 / 1.081, 1.077, 1.084 | within noise (control) |
| dense B=512 / rust | 0.199 (0.197-0.201) | 0.207 (0.205-0.209) | +4.0% | 0.199, 0.199, 0.199 / 0.207, 0.205, 0.209 | consistent (control) |

### epoch, loader

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.382 (0.367-0.390) | 0.387 (0.382-0.388) | +1.4% | 0.372, 0.385, 0.386 / 0.384, 0.385, 0.387 | within noise |
| conv B=32 / rust | 0.316 (0.300-0.318) | 0.301 (0.299-0.318) | -4.9% | 0.312, 0.318, 0.309 / 0.299, 0.310, 0.303 | within noise |
| conv B=512 / numpy | 0.370 (0.365-0.372) | 0.370 (0.367-0.371) | +0.0% | 0.367, 0.370, 0.369 / 0.368, 0.370, 0.371 | within noise |
| conv B=512 / rust | 0.320 (0.314-0.331) | 0.308 (0.298-0.315) | -3.7% | 0.322, 0.315, 0.327 / 0.308, 0.315, 0.302 | separated, inside spread |
| dense B=32 / numpy | 0.611 (0.599-0.622) | 0.607 (0.598-0.618) | -0.7% | 0.611, 0.611, 0.613 / 0.601, 0.612, 0.608 | within noise |
| dense B=32 / rust | 0.507 (0.500-0.510) | 0.496 (0.492-0.515) | -2.2% | 0.504, 0.505, 0.509 / 0.492, 0.505, 0.501 | within noise |
| dense B=512 / numpy | 0.361 (0.359-0.364) | 0.360 (0.355-0.365) | -0.0% | 0.361, 0.362, 0.359 / 0.360, 0.357, 0.365 | within noise |
| dense B=512 / rust | 0.407 (0.399-0.410) | 0.387 (0.383-0.397) | -4.9% | 0.404, 0.405, 0.407 / 0.385, 0.387, 0.392 | consistent |
