Old `0d91d1a` against new `0d91d1a`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --shape 5408 --shape 784 --shape attention --op forward_batch --op downstream_batch --op accumulate_gradient_batch --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `6a8190c` (extension sha256 `84ec4e85d91b`) and new crate `7b9878f` (extension sha256 `21b07c2bef84`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.15; busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- 36 rows within noise (3 separated inside their spread), max |Δ| 2.0%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward_batch b32 / numpy | 150.9 (148.1-158.4) | 153.8 (146.4-161.7) | +1.9% | 150.9, 152.8, 153.3 / 154.7, 153.8, 153 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 345 (334.9-408.4) | 340.4 (335.4-356.4) | -1.4% | 342, 360.1, 373.7 / 345.9, 339.7, 343.4 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1170 (1058-1175) | 1172 (1130-1174) | +0.2% | 1113, 1173, 1172 / 1152, 1170, 1173 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1743 (1700-1825) | 1764 (1748-1808) | +1.2% | 1743, 1741, 1782 / 1763, 1785, 1757 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 78.2 (77.58-79.47) | 78.09 (77.46-78.73) | -0.1% | 78.26, 77.88, 78.94 / 77.6, 78.15, 78.49 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 241.2 (237.1-244.9) | 243.9 (236.4-246.3) | +1.1% | 237.1, 242.5, 243.2 / 241.1, 244.8, 242.1 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3184 (3161-3212) | 3177 (3161-3197) | -0.2% | 3184, 3186, 3189 / 3181, 3167, 3183 | separated, inside spread |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2252 (2237-2274) | 2257 (2236-2307) | +0.2% | 2264, 2252, 2239 / 2274, 2257, 2252 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 163.2 (158.9-166.9) | 163.1 (162.1-166.3) | -0.1% | 159.3, 163.2, 166.5 / 162.3, 163.1, 165 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 277.6 (268.3-282.4) | 272.7 (266.8-278.9) | -1.8% | 270.4, 278.8, 280.5 / 272.6, 276.3, 270.7 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 1855 (1807-1915) | 1842 (1832-1857) | -0.7% | 1883, 1834, 1847 / 1837, 1849, 1844 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 1976 (1909-2014) | 1973 (1937-2080) | -0.2% | 1973, 1962, 1976 / 1978, 2017, 1955 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 38.42 (37.71-39.26) | 38.24 (37.87-38.61) | -0.4% | 38.02, 38.27, 38.88 / 38.24, 38.24, 38.22 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 45.29 (44.96-46.83) | 46.15 (44.86-46.81) | +1.9% | 45.02, 45.29, 46.46 / 45.49, 46.78, 46.11 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 266.3 (262.9-268.2) | 264.8 (263.8-267.8) | -0.6% | 263.5, 266.4, 267.5 / 263.9, 264.8, 266.8 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 291.8 (285.8-304.3) | 290 (285-295.1) | -0.6% | 289.9, 291.8, 297.5 / 287.5, 290.2, 292.5 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 23.86 (23.71-24.1) | 24.05 (23.7-24.39) | +0.8% | 23.74, 23.89, 24.02 / 24.04, 23.95, 24.05 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 32.68 (32.24-33.75) | 33.15 (32.48-33.29) | +1.4% | 32.31, 32.62, 33.74 / 33.02, 32.88, 33.15 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 130.5 (129.9-131.2) | 131 (129.8-132.9) | +0.4% | 130.1, 130.8, 130.6 / 132, 130.6, 130.4 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 242.6 (238.8-245.5) | 243.4 (241.1-245.9) | +0.4% | 242.6, 244.3, 240 / 243.3, 244.1, 243 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 40.28 (39.27-40.99) | 39.86 (39.27-40.93) | -1.0% | 40.66, 39.31, 40.32 / 40.49, 39.48, 39.78 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 39.82 (39.38-40.71) | 40.43 (39.83-40.84) | +1.5% | 39.68, 40.16, 39.97 / 40.43, 40.34, 40.33 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 222.6 (220.1-224.9) | 223.4 (220.4-224.8) | +0.4% | 220.4, 224.5, 222.6 / 223.8, 222.1, 223.1 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 254.7 (251.2-258.8) | 256.7 (254.1-259.7) | +0.8% | 252.3, 253.7, 258.2 / 257.3, 256.5, 256.3 | within noise |
| relu 30 x 784 forward_batch b32 / numpy | 29.99 (29.43-30.31) | 30.19 (29.63-30.45) | +0.7% | 29.76, 29.8, 30.3 / 30.34, 30.19, 29.91 | within noise |
| relu 30 x 784 forward_batch b32 / rust | 42.7 (42-44.16) | 42.61 (42.16-43.4) | -0.2% | 42.43, 43.36, 42.66 / 42.85, 42.31, 42.99 | within noise |
| relu 30 x 784 forward_batch b512 / numpy | 156.7 (155.1-159.5) | 157 (155.5-159.1) | +0.2% | 156.2, 157.3, 157.2 / 157.3, 157, 157.3 | within noise |
| relu 30 x 784 forward_batch b512 / rust | 238.5 (235.1-241.2) | 240.4 (238.2-244) | +0.8% | 238.5, 235.7, 240.3 / 241.1, 239.3, 241.1 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 369.4 (362.1-384.1) | 363.6 (362.4-373.4) | -1.6% | 373.7, 366.4, 370.6 / 368.8, 367.5, 363 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 328.3 (321.7-330.8) | 327.5 (320.8-333.9) | -0.2% | 323, 328.6, 329.6 / 322.5, 327.5, 332.4 | within noise |
| attention 16 x 32 forward_batch b512 / numpy | 5579 (5527-5614) | 5595 (5519-5635) | +0.3% | 5537, 5579, 5613 / 5577, 5594, 5595 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 5282 (5212-5370) | 5325 (5225-5401) | +0.8% | 5328, 5282, 5245 / 5363, 5327, 5275 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 248.5 (241.7-258) | 251.8 (238.8-256.9) | +1.3% | 244.5, 251, 253.4 / 253.4, 246, 252.9 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 168.9 (163.4-173.1) | 167.7 (162.7-177.1) | -0.7% | 164.9, 169.8, 170.6 / 168.7, 165.7, 172 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5345 (5287-5442) | 5452 (5306-5531) | +2.0% | 5288, 5368, 5390 / 5495, 5419, 5362 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 2979 (2946-3027) | 2994 (2981-3088) | +0.5% | 2986, 2979, 2979 / 3004, 3038, 2987 | separated, inside spread |
