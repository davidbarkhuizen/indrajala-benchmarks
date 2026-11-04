Old `515849f` against new `515849f`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/prepared_dataset_timing.py time --configs conv B=32 conv B=512 dense B=32 dense B=512 --repeats 2 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `cba601e` (extension sha256 `bc8a4a1fc83d`) and new crate `480cebc` (extension sha256 `5b3d1d17cea4`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 4.64 (HIGH); busy processes: none. Each row pools 6 runs per side.

- controls: 8 rows, all within noise
- 16 rows within noise, max |Δ| 3.7%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.411 (0.408-0.419) | 0.411 (0.401-0.414) | +0.1% | 0.410, 0.413, 0.413 / 0.407, 0.411, 0.410 | within noise |
| conv B=32 / rust | 0.320 (0.307-0.328) | 0.309 (0.306-0.325) | -3.6% | 0.312, 0.316, 0.327 / 0.308, 0.307, 0.320 | within noise |
| conv B=512 / numpy | 0.400 (0.397-0.415) | 0.404 (0.396-0.415) | +1.0% | 0.398, 0.407, 0.407 / 0.402, 0.406, 0.406 | within noise |
| conv B=512 / rust | 0.354 (0.348-0.360) | 0.349 (0.343-0.360) | -1.4% | 0.350, 0.356, 0.358 / 0.349, 0.344, 0.356 | within noise |
| dense B=32 / numpy | 1.685 (1.682-1.702) | 1.677 (1.670-1.692) | -0.5% | 1.684, 1.683, 1.700 / 1.675, 1.673, 1.687 | within noise |
| dense B=32 / rust | 0.712 (0.700-0.716) | 0.699 (0.696-0.709) | -1.8% | 0.702, 0.715, 0.713 / 0.702, 0.698, 0.704 | within noise |
| dense B=512 / numpy | 1.437 (1.431-1.443) | 1.435 (1.430-1.441) | -0.1% | 1.434, 1.438, 1.439 / 1.434, 1.433, 1.439 | within noise |
| dense B=512 / rust | 0.598 (0.594-0.604) | 0.596 (0.587-0.601) | -0.3% | 0.595, 0.600, 0.599 / 0.598, 0.592, 0.597 | within noise |

### prepare

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.037 (0.037-0.038) | 0.037 (0.037-0.038) | +0.2% | 0.037, 0.037, 0.038 / 0.037, 0.038, 0.037 | within noise (control) |
| conv B=32 / rust | 0.006 (0.006-0.006) | 0.006 (0.006-0.006) | -1.0% | 0.006, 0.006, 0.006 / 0.006, 0.006, 0.006 | within noise (control) |
| conv B=512 / numpy | 0.038 (0.037-0.039) | 0.038 (0.038-0.038) | -0.2% | 0.038, 0.038, 0.038 / 0.038, 0.038, 0.038 | within noise (control) |
| conv B=512 / rust | 0.006 (0.006-0.006) | 0.006 (0.006-0.007) | +0.2% | 0.006, 0.006, 0.006 / 0.006, 0.006, 0.006 | within noise (control) |
| dense B=32 / numpy | 1.081 (1.075-1.092) | 1.078 (1.075-1.091) | -0.3% | 1.078, 1.080, 1.087 / 1.076, 1.080, 1.084 | within noise (control) |
| dense B=32 / rust | 0.200 (0.198-0.203) | 0.198 (0.197-0.199) | -1.1% | 0.199, 0.200, 0.200 / 0.197, 0.197, 0.199 | separated, inside spread (control) |
| dense B=512 / numpy | 1.081 (1.070-1.096) | 1.078 (1.075-1.083) | -0.3% | 1.074, 1.080, 1.090 / 1.081, 1.076, 1.080 | within noise (control) |
| dense B=512 / rust | 0.199 (0.197-0.201) | 0.199 (0.197-0.200) | -0.0% | 0.198, 0.200, 0.199 / 0.199, 0.199, 0.199 | within noise (control) |

### epoch, loader

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv B=32 / numpy | 0.384 (0.369-0.388) | 0.381 (0.375-0.386) | -0.8% | 0.374, 0.384, 0.387 / 0.378, 0.384, 0.381 | within noise |
| conv B=32 / rust | 0.308 (0.297-0.314) | 0.297 (0.294-0.315) | -3.7% | 0.300, 0.305, 0.314 / 0.297, 0.295, 0.310 | within noise |
| conv B=512 / numpy | 0.370 (0.363-0.373) | 0.370 (0.368-0.371) | +0.0% | 0.364, 0.370, 0.372 / 0.369, 0.370, 0.371 | within noise |
| conv B=512 / rust | 0.325 (0.320-0.330) | 0.320 (0.317-0.336) | -1.7% | 0.325, 0.325, 0.325 / 0.325, 0.318, 0.329 | within noise |
| dense B=32 / numpy | 0.606 (0.599-0.619) | 0.598 (0.596-0.616) | -1.3% | 0.609, 0.606, 0.609 / 0.603, 0.597, 0.608 | within noise |
| dense B=32 / rust | 0.504 (0.492-0.512) | 0.493 (0.491-0.501) | -2.2% | 0.495, 0.509, 0.504 / 0.497, 0.492, 0.492 | within noise |
| dense B=512 / numpy | 0.360 (0.356-0.364) | 0.355 (0.354-0.363) | -1.2% | 0.357, 0.363, 0.360 / 0.357, 0.355, 0.359 | within noise |
| dense B=512 / rust | 0.397 (0.394-0.402) | 0.398 (0.384-0.403) | +0.2% | 0.395, 0.396, 0.399 / 0.397, 0.391, 0.400 | within noise |
