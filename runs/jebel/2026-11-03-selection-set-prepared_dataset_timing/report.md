Old `d2eacb9` against new `0447c1f`, run with `scripts/measurement/ab.py`: passes in the order ONNO. Each pass ran `python scripts/measurement/prepared_dataset_timing.py time --repeats 5 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `18304f7c5a63`) on both sides. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.07; busy processes: none. Each row pools 10 runs per side.

- controls: 8 rows, all within noise
- 16 rows within noise (1 separated inside their spread), max |Δ| 4.5%

### epoch

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 1.680 (1.664-1.694) | 1.681 (1.665-1.691) | +0.1% | 1.685, 1.674 / 1.682, 1.677 | within noise |
| dense B=32 / rust | 0.752 (0.740-0.760) | 0.751 (0.742-0.761) | -0.1% | 0.754, 0.751 / 0.751, 0.752 | within noise |
| dense single / numpy | 7.176 (7.137-7.430) | 7.231 (7.160-7.483) | +0.8% | 7.151, 7.292 / 7.238, 7.224 | within noise |
| dense single / rust | 1.444 (1.404-1.499) | 1.437 (1.416-1.499) | -0.5% | 1.474, 1.431 / 1.456, 1.424 | within noise |
| conv B=32 / numpy | 0.409 (0.407-0.411) | 0.409 (0.405-0.413) | +0.2% | 0.410, 0.407 / 0.410, 0.409 | within noise |
| conv B=32 / rust | 0.319 (0.309-0.330) | 0.314 (0.309-0.330) | -1.6% | 0.319, 0.318 / 0.314, 0.320 | within noise |
| conv single / numpy | 1.199 (1.168-1.224) | 1.186 (1.176-1.243) | -1.1% | 1.218, 1.199 / 1.206, 1.181 | within noise |
| conv single / rust | 0.468 (0.461-0.502) | 0.489 (0.462-0.506) | +4.5% | 0.468, 0.468 / 0.466, 0.499 | within noise |

### prepare

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 1.078 (1.075-1.095) | 1.079 (1.077-1.084) | +0.1% | 1.077, 1.078 / 1.078, 1.079 | within noise (control) |
| dense B=32 / rust | 0.198 (0.197-0.200) | 0.199 (0.197-0.199) | +0.2% | 0.198, 0.198 / 0.198, 0.199 | within noise (control) |
| dense single / numpy | 1.077 (1.074-1.087) | 1.078 (1.075-1.116) | +0.1% | 1.076, 1.077 / 1.076, 1.079 | within noise (control) |
| dense single / rust | 0.198 (0.196-0.201) | 0.198 (0.196-0.199) | +0.1% | 0.198, 0.198 / 0.198, 0.198 | within noise (control) |
| conv B=32 / numpy | 0.037 (0.037-0.038) | 0.037 (0.037-0.038) | +0.4% | 0.037, 0.037 / 0.037, 0.037 | separated, inside spread (control) |
| conv B=32 / rust | 0.006 (0.006-0.006) | 0.006 (0.006-0.006) | -0.8% | 0.006, 0.006 / 0.006, 0.006 | separated, inside spread (control) |
| conv single / numpy | 0.037 (0.037-0.037) | 0.037 (0.037-0.038) | +0.0% | 0.037, 0.037 / 0.037, 0.037 | within noise (control) |
| conv single / rust | 0.006 (0.006-0.006) | 0.006 (0.006-0.006) | -0.6% | 0.006, 0.006 / 0.006, 0.006 | separated, inside spread (control) |

### epoch, loader

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| dense B=32 / numpy | 0.606 (0.596-0.623) | 0.598 (0.582-0.609) | -1.3% | 0.614, 0.605 / 0.601, 0.593 | separated, inside spread |
| dense B=32 / rust | 0.561 (0.551-0.566) | 0.558 (0.550-0.571) | -0.4% | 0.561, 0.560 / 0.554, 0.561 | within noise |
| dense single / numpy | 5.993 (5.927-6.186) | 6.105 (5.941-6.208) | +1.9% | 5.992, 6.145 / 6.118, 6.093 | within noise |
| dense single / rust | 1.239 (1.202-1.279) | 1.244 (1.214-1.301) | +0.4% | 1.258, 1.225 / 1.255, 1.225 | within noise |
| conv B=32 / numpy | 0.370 (0.358-0.375) | 0.368 (0.361-0.375) | -0.5% | 0.364, 0.371 / 0.368, 0.373 | within noise |
| conv B=32 / rust | 0.313 (0.302-0.323) | 0.309 (0.304-0.322) | -1.3% | 0.313, 0.313 / 0.306, 0.316 | within noise |
| conv single / numpy | 1.161 (1.134-1.188) | 1.145 (1.139-1.192) | -1.4% | 1.178, 1.159 / 1.166, 1.141 | within noise |
| conv single / rust | 0.458 (0.452-0.492) | 0.477 (0.452-0.493) | +4.2% | 0.458, 0.459 / 0.457, 0.490 | within noise |
