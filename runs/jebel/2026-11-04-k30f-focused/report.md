Old `515849f` against new `515849f`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --shape 5408 --shape 784 --shape attention --op forward_batch --op downstream_batch --op accumulate_gradient_batch --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `cba601e` (extension sha256 `bc8a4a1fc83d`) and new crate `dc571a0` (extension sha256 `1cebe6ff7934`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.23; busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent, small: per call / attention 16 x 32 forward_batch b32 / numpy +0.8% (364.6 -> 367.4 µs)
- 35 rows within noise (2 separated inside their spread), max |Δ| 2.7%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward_batch b32 / numpy | 153.6 (147-159.9) | 153.7 (146.4-160) | +0.1% | 153.6, 153.3, 153.6 / 154.4, 152.9, 153.2 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 239.7 (232.9-242.6) | 239.9 (236.3-241.3) | +0.1% | 237.9, 236.9, 240.6 / 238.2, 240.5, 239.2 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1172 (1096-1176) | 1173 (1163-1183) | +0.1% | 1136, 1172, 1174 / 1168, 1169, 1182 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1126 (1124-1129) | 1128 (1115-1139) | +0.1% | 1128, 1125, 1126 / 1118, 1128, 1136 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 78 (77.85-79.6) | 78.25 (78.04-78.93) | +0.3% | 77.85, 78, 79.02 / 78.14, 78.79, 78.18 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 247.1 (243.5-254.5) | 250.3 (245.8-253) | +1.3% | 247.1, 244.9, 251 / 246.6, 250.7, 252.5 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3180 (3172-3185) | 3192 (3179-3222) | +0.4% | 3178, 3179, 3182 / 3186, 3201, 3192 | separated, inside spread |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2405 (2392-2431) | 2400 (2382-2425) | -0.2% | 2415, 2411, 2403 / 2404, 2400, 2404 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 162.2 (161.5-163.6) | 162.7 (160.6-165.1) | +0.3% | 162, 162.4, 162.9 / 162.6, 163.6, 162.7 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 281.4 (278.4-286.9) | 285.1 (280.7-316.2) | +1.3% | 279.4, 284, 283.7 / 282.7, 297.9, 300.8 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 1848 (1782-1903) | 1841 (1824-1871) | -0.4% | 1793, 1848, 1887 / 1855, 1834, 1845 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 1997 (1962-2172) | 1975 (1891-1994) | -1.1% | 1995, 1981, 2082 / 1976, 1987, 1930 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 38.82 (37.72-39.11) | 38.41 (37.6-39.22) | -1.1% | 38.34, 38.89, 38.73 / 37.82, 38.41, 38.85 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 35.34 (34.89-35.95) | 35.29 (34.23-35.86) | -0.1% | 35.17, 35.34, 35.54 / 35.1, 34.99, 35.66 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 269.8 (265.3-271) | 267.9 (266.8-269.6) | -0.7% | 267, 270.6, 269.8 / 267.4, 267.9, 268.7 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 248.1 (246.9-249.9) | 249.3 (245.8-250.3) | +0.5% | 247.6, 249.8, 247.8 / 246.3, 250.1, 249.5 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 24.13 (24.06-24.65) | 24.33 (24.16-24.52) | +0.8% | 24.12, 24.09, 24.56 / 24.34, 24.33, 24.32 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 33.41 (33.09-34.77) | 33.92 (33.29-34.44) | +1.5% | 33.33, 34.07, 33.86 / 33.77, 34.15, 33.86 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 132.3 (131.4-133.2) | 131.8 (131.2-134) | -0.3% | 131.5, 132.3, 133.2 / 131.3, 131.9, 133 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 245.2 (240.3-247) | 243.9 (241.7-246.7) | -0.5% | 243.2, 246.9, 243.6 / 244.2, 244.7, 243.4 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 40.32 (39.46-41.15) | 40.22 (40.14-41.13) | -0.2% | 40.72, 40.31, 40.15 / 40.41, 40.68, 40.18 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 40.76 (39.98-42.41) | 41.71 (40.59-42.39) | +2.3% | 40.91, 41.2, 40.59 / 41.31, 42.22, 41.35 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 223.8 (221.4-229.3) | 225.5 (223.2-226.6) | +0.8% | 222.2, 223.2, 228.6 / 223.3, 225.8, 226.1 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 259.4 (256.5-263.1) | 259.4 (255.1-266.8) | -0.0% | 258.7, 260.4, 259.8 / 260.9, 259.3, 259.4 | within noise |
| relu 30 x 784 forward_batch b32 / numpy | 30.41 (30.11-30.78) | 30.52 (30.31-31.04) | +0.4% | 30.52, 30.44, 30.29 / 30.67, 30.61, 30.52 | within noise |
| relu 30 x 784 forward_batch b32 / rust | 32.78 (31.75-33.46) | 32.78 (32.26-33.17) | +0.0% | 32.4, 32.46, 33.11 / 32.78, 32.77, 32.66 | within noise |
| relu 30 x 784 forward_batch b512 / numpy | 157.9 (157.4-160.1) | 159 (156.3-159.8) | +0.7% | 158, 159, 157.7 / 159.3, 157, 159.4 | within noise |
| relu 30 x 784 forward_batch b512 / rust | 200.2 (196.7-204.6) | 199 (197.1-202.6) | -0.6% | 202.9, 200.6, 198.2 / 197.4, 201.4, 199.8 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 364.6 (360.8-366.9) | 367.4 (364.1-370.8) | +0.8% | 365.1, 364.9, 363.1 / 367.4, 367.4, 367.3 | consistent, small |
| attention 16 x 32 forward_batch b32 / rust | 271.3 (266.5-278.1) | 273.2 (270.4-277.3) | +0.7% | 269.2, 269.8, 277.1 / 271.6, 272.3, 275.5 | within noise |
| attention 16 x 32 forward_batch b512 / numpy | 5680 (5645-5718) | 5664 (5601-5708) | -0.3% | 5647, 5694, 5703 / 5682, 5682, 5621 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 4259 (4169-4314) | 4224 (4171-4334) | -0.8% | 4243, 4218, 4296 / 4214, 4256, 4246 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 256.4 (239.7-262.2) | 250.7 (245.9-264.7) | -2.2% | 258.3, 254.8, 248.5 / 247.8, 256.4, 256.7 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 119.4 (116.5-121.5) | 120.4 (118.6-122.7) | +0.8% | 118.1, 120.3, 119.4 / 119.1, 120.3, 121.9 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5513 (5382-6024) | 5362 (5349-5528) | -2.7% | 5715, 5573, 5420 / 5442, 5405, 5362 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 1611 (1596-1621) | 1622 (1592-1635) | +0.7% | 1599, 1608, 1620 / 1605, 1630, 1622 | within noise |
