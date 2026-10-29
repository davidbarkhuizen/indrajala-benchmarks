Old `89e88d7` against new `89e88d7`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --op accumulate --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `be14eac` (extension sha256 `44f6a8e617ba`) and new crate `9a448ba` (extension sha256 `d6a56fdf3074`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (raspberry-pi-5.json); passes peaked at 56.2-58.4 C; max 1-min load 1.40 (measured just after this run's crate builds); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust -12.8% (6.543e+04 -> 5.706e+04 µs)
- consistent: per call / conv 26x26x8, 8 ch accumulate_gradient / rust -10.0% (72.27 -> 65.02 µs)
- consistent: per call / conv 26x26x8/2, 8 ch accumulate_gradient / rust -9.7% (19.3 -> 17.42 µs)
- consistent: per call / conv 13x13x8, 8 ch accumulate_gradient / rust -9.1% (16.32 -> 14.83 µs)
- consistent: per call / conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust -5.9% (1.32e+04 -> 1.243e+04 µs)
- consistent: per call / conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust -5.2% (639.5 -> 606.3 µs)
- consistent: per call / conv 8x8, 8 ch accumulate_gradient / rust -4.8% (2.42 -> 2.304 µs)
- consistent: per call / conv 8x8, 8 ch accumulate_gradient_batch b32 / rust -4.4% (54.29 -> 51.88 µs)
- consistent: per call / conv 28x28, 8 ch accumulate_gradient / rust -4.2% (31.56 -> 30.23 µs)
- 61 rows within noise (9 separated inside their spread), max |Δ| 245.3%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 accumulate_gradient / numpy | 347.4 (294.3-380.2) | 322.9 (303.6-758.5) | -7.0% | 375.9, 306.7, 345 / 310, 538.7, 353.4 | within noise |
| conv tail 32 x 5408 accumulate_gradient / rust | 97.69 (87.66-99.99) | 96 (91.35-99.32) | -1.7% | 97.71, 94.4, 92.88 / 98.22, 91.76, 96.48 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 1630 (1440-1880) | 1528 (1344-1859) | -6.3% | 1843, 1586, 1519 / 1449, 1573, 1667 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 574 (381.7-770.5) | 460.3 (379.3-772.7) | -19.8% | 452.8, 508.7, 705.1 / 518.4, 382.8, 644.7 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 1832 (1619-2047) | 1953 (1694-2208) | +6.6% | 1934, 1848, 1708 / 1898, 1951, 1953 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 2161 (2012-2348) | 2143 (2075-2258) | -0.8% | 2205, 2136, 2186 / 2176, 2204, 2099 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 2.271e+04 (2.203e+04-2.375e+04) | 2.273e+04 (2.195e+04-2.352e+04) | +0.1% | 2.213e+04, 2.271e+04, 2.357e+04 / 2.326e+04, 2.214e+04, 2.286e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 1.891e+04 (1.867e+04-1.974e+04) | 1.933e+04 (1.883e+04-1.998e+04) | +2.3% | 1.921e+04, 1.884e+04, 1.927e+04 / 1.915e+04, 1.933e+04, 1.953e+04 | within noise |
| dense 30 x 784 accumulate_gradient / numpy | 42.77 (42.72-42.99) | 42.61 (42.58-42.74) | -0.4% | 42.86, 42.73, 42.83 / 42.6, 42.66, 42.64 | separated, inside spread |
| dense 30 x 784 accumulate_gradient / rust | 9.92 (9.873-9.979) | 9.908 (9.88-10.05) | -0.1% | 9.943, 9.903, 9.922 / 9.963, 9.908, 9.926 | within noise |
| dense 30 x 784 apply_accumulated_gradient / numpy | 61.17 (61.09-61.5) | 61.14 (61.11-61.55) | -0.0% | 61.13, 61.45, 61.16 / 61.39, 61.12, 61.13 | within noise |
| dense 30 x 784 apply_accumulated_gradient / rust | 36.29 (36.17-36.69) | 36.19 (36.15-36.38) | -0.3% | 36.43, 36.21, 36.4 / 36.17, 36.23, 36.29 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 433.6 (86.19-441.7) | 440.1 (87.92-446.2) | +1.5% | 439.7, 257.8, 264.2 / 267, 437.1, 440.9 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 138.4 (138.2-139.4) | 138.3 (138.1-139.4) | -0.1% | 138.4, 138.6, 138.8 / 138.2, 138.7, 138.7 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 1934 (1857-2005) | 1894 (1713-2157) | -2.1% | 1919, 1942, 1931 / 1824, 2039, 1837 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 2499 (2132-2561) | 2559 (2202-2790) | +2.4% | 2553, 2499, 2231 / 2371, 2668, 2592 | within noise |
| dense 10 x 30 accumulate_gradient / numpy | 5.329 (5.28-5.415) | 5.299 (5.255-5.441) | -0.6% | 5.348, 5.317, 5.345 / 5.317, 5.285, 5.362 | within noise |
| dense 10 x 30 accumulate_gradient / rust | 0.7793 (0.7718-0.8005) | 0.7823 (0.7616-0.7883) | +0.4% | 0.7739, 0.7839, 0.791 / 0.7826, 0.775, 0.7745 | within noise |
| dense 10 x 30 apply_accumulated_gradient / numpy | 8.916 (8.894-8.975) | 8.898 (8.877-9.146) | -0.2% | 8.913, 8.919, 8.939 / 8.928, 9.011, 8.894 | within noise |
| dense 10 x 30 apply_accumulated_gradient / rust | 4.019 (4.012-4.045) | 4.015 (3.995-4.031) | -0.1% | 4.016, 4.03, 4.019 / 4.018, 4.009, 4.015 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 9.627 (9.564-9.834) | 9.579 (9.482-9.635) | -0.5% | 9.627, 9.607, 9.722 / 9.592, 9.557, 9.579 | separated, inside spread |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 4.288 (4.275-4.294) | 4.296 (4.281-4.314) | +0.2% | 4.283, 4.281, 4.291 / 4.298, 4.292, 4.302 | separated, inside spread |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 47.86 (47.63-48.11) | 47.84 (47.59-48.27) | -0.0% | 47.78, 48.08, 47.71 / 47.98, 48.03, 47.71 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 54.37 (54.32-54.41) | 54.43 (54.31-54.47) | +0.1% | 54.4, 54.36, 54.33 / 54.44, 54.39, 54.39 | within noise |
| conv 28x28, 8 ch accumulate_gradient / numpy | 60.46 (58-61.76) | 58.14 (57.94-60.45) | -3.8% | 58.5, 61.65, 60.46 / 58.55, 58.08, 59.2 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 31.56 (31.53-31.7) | 30.23 (30.17-30.25) | -4.2% | 31.61, 31.63, 31.54 / 30.23, 30.2, 30.24 | consistent |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 2252 (2240-2324) | 2283 (2240-2604) | +1.4% | 2252, 2320, 2245 / 2242, 2426, 2321 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 1204 (1183-1500) | 1146 (1136-1464) | -4.8% | 1346, 1204, 1211 / 1302, 1156, 1143 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 3.769e+04 (3.713e+04-3.82e+04) | 3.731e+04 (3.717e+04-3.829e+04) | -1.0% | 3.81e+04, 3.767e+04, 3.722e+04 / 3.785e+04, 3.719e+04, 3.774e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 2.909e+04 (2.746e+04-3.296e+04) | 2.984e+04 (2.755e+04-3.218e+04) | +2.5% | 3.117e+04, 2.819e+04, 3.021e+04 / 2.995e+04, 3.057e+04, 2.913e+04 | within noise |
| conv 8x8, 8 ch accumulate_gradient / numpy | 12.42 (12.36-12.6) | 12.6 (12.46-12.88) | +1.4% | 12.43, 12.48, 12.42 / 12.73, 12.64, 12.55 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient / rust | 2.42 (2.407-2.455) | 2.304 (2.296-2.326) | -4.8% | 2.421, 2.42, 2.433 / 2.299, 2.311, 2.314 | consistent |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 148.9 (148.3-153.5) | 148.9 (148.3-151.6) | +0.0% | 148.6, 150, 151.2 / 148.9, 148.7, 150 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 54.29 (54.25-54.33) | 51.88 (51.76-51.92) | -4.4% | 54.25, 54.32, 54.29 / 51.9, 51.8, 51.9 | consistent |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 2366 (2286-2380) | 2313 (2279-2367) | -2.3% | 2332, 2374, 2332 / 2351, 2323, 2286 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 1282 (1012-1294) | 1253 (986.5-1307) | -2.3% | 1282, 1149, 1155 / 1283, 993.3, 1256 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 40.41 (40.01-40.73) | 40.51 (40.19-40.86) | +0.2% | 40.34, 40.43, 40.37 / 40.36, 40.65, 40.54 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 16.32 (16.3-16.37) | 14.83 (14.79-14.85) | -9.1% | 16.3, 16.36, 16.32 / 14.83, 14.82, 14.82 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 1132 (1125-1139) | 1128 (1126-1136) | -0.3% | 1138, 1131, 1127 / 1131, 1131, 1128 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 639.5 (637.8-641.9) | 606.3 (598.8-611.1) | -5.2% | 638.9, 639.8, 639.7 / 605.3, 609.9, 601.3 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.86e+04 (1.838e+04-1.867e+04) | 1.838e+04 (1.824e+04-1.847e+04) | -1.2% | 1.861e+04, 1.865e+04, 1.839e+04 / 1.836e+04, 1.837e+04, 1.842e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 1.32e+04 (1.217e+04-1.396e+04) | 1.243e+04 (1.119e+04-1.312e+04) | -5.9% | 1.326e+04, 1.32e+04, 1.293e+04 / 1.248e+04, 1.211e+04, 1.216e+04 | consistent |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 47.52 (47.28-48.9) | 47.56 (47.22-48.37) | +0.1% | 48.27, 47.56, 47.34 / 47.37, 47.86, 47.98 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 19.3 (19.26-19.35) | 17.42 (17.31-17.46) | -9.7% | 19.28, 19.33, 19.3 / 17.33, 17.43, 17.44 | consistent |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 1377 (1371-1398) | 1379 (1372-1393) | +0.2% | 1386, 1378, 1377 / 1383, 1376, 1385 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 764.8 (744.1-833.5) | 725.8 (665.2-784.7) | -5.1% | 793.9, 764.8, 788.7 / 778.6, 681.7, 716.4 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 2.248e+04 (2.233e+04-2.271e+04) | 2.239e+04 (2.222e+04-2.256e+04) | -0.4% | 2.252e+04, 2.248e+04, 2.247e+04 / 2.239e+04, 2.235e+04, 2.247e+04 | separated, inside spread |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 1.652e+04 (1.471e+04-1.808e+04) | 1.646e+04 (1.464e+04-1.731e+04) | -0.3% | 1.55e+04, 1.628e+04, 1.783e+04 / 1.58e+04, 1.598e+04, 1.71e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 158.1 (156.6-162.5) | 161 (156.8-162.5) | +1.9% | 159.9, 159.9, 157.1 / 159, 161.6, 160.9 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 72.27 (72.18-72.46) | 65.02 (64.77-66.47) | -10.0% | 72.21, 72.24, 72.38 / 65, 64.99, 65.66 | consistent |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 5633 (5593-5671) | 5631 (5611-5674) | -0.0% | 5656, 5618, 5617 / 5644, 5642, 5629 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 3526 (3230-3663) | 3270 (3172-3560) | -7.3% | 3573, 3388, 3517 / 3421, 3238, 3365 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 8.884e+04 (8.824e+04-8.984e+04) | 8.989e+04 (8.888e+04-9.002e+04) | +1.2% | 8.903e+04, 8.93e+04, 8.834e+04 / 8.995e+04, 8.942e+04, 8.956e+04 | separated, inside spread |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 6.543e+04 (6.348e+04-6.905e+04) | 5.706e+04 (5.493e+04-6.381e+04) | -12.8% | 6.713e+04, 6.377e+04, 6.628e+04 / 5.631e+04, 5.937e+04, 5.789e+04 | consistent |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 1165 (886.3-1359) | 1351 (1132-1469) | +16.0% | 1096, 1191, 1141 / 1246, 1434, 1337 | separated, inside spread |
| conv tail 32 x 5408 bare accumulate b32 / rust | 1301 (1185-1385) | 1155 (1080-1232) | -11.3% | 1369, 1285, 1217 / 1189, 1122, 1126 | separated, inside spread |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 2.216e+04 (2.174e+04-2.312e+04) | 2.217e+04 (2.146e+04-2.293e+04) | +0.1% | 2.206e+04, 2.205e+04, 2.26e+04 / 2.217e+04, 2.186e+04, 2.247e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / rust | 1.885e+04 (1.773e+04-2e+04) | 1.929e+04 (1.901e+04-2.003e+04) | +2.3% | 1.841e+04, 1.932e+04, 1.887e+04 / 1.952e+04, 1.962e+04, 1.916e+04 | within noise |
| dense 30 x 784 bare accumulate b32 / numpy | 66.64 (65.65-399.9) | 230.1 (66.4-400.7) | +245.3% | 233.2, 66.85, 66.02 / 233.5, 397.1, 66.7 | within noise |
| dense 30 x 784 bare accumulate b32 / rust | 126.3 (124.8-127.1) | 125.6 (124.7-127.2) | -0.5% | 127, 126.3, 124.8 / 125.2, 126.4, 125.8 | within noise |
| dense 30 x 784 bare accumulate b512 / numpy | 1676 (1600-1822) | 1775 (1579-1813) | +5.9% | 1676, 1711, 1693 / 1732, 1807, 1664 | within noise |
| dense 30 x 784 bare accumulate b512 / rust | 2135 (2071-2565) | 2514 (2079-2576) | +17.8% | 2135, 2161, 2318 / 2291, 2513, 2551 | within noise |
| dense 10 x 30 bare accumulate b32 / numpy | 5.053 (5.027-5.068) | 5.048 (5.016-5.088) | -0.1% | 5.053, 5.049, 5.044 / 5.063, 5.054, 5.033 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 2.881 (2.868-2.908) | 2.881 (2.875-2.886) | -0.0% | 2.874, 2.896, 2.881 / 2.878, 2.879, 2.884 | within noise |
| dense 10 x 30 bare accumulate b512 / numpy | 32.55 (32.39-32.73) | 32.59 (32.46-32.93) | +0.1% | 32.47, 32.55, 32.64 / 32.53, 32.52, 32.78 | within noise |
| dense 10 x 30 bare accumulate b512 / rust | 45.09 (45.05-45.18) | 45.09 (45.05-45.21) | +0.0% | 45.07, 45.13, 45.09 / 45.06, 45.16, 45.11 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 590.7 (580.4-599.1) | 591.4 (590.2-2084) | +0.1% | 584.3, 598.3, 587.3 / 591.4, 1337, 591.9 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 461 (448.4-463.3) | 462.7 (450-463.8) | +0.4% | 455.3, 463.1, 454.2 / 462.7, 462.6, 456.8 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 4.438e+04 (4.22e+04-4.507e+04) | 4.113e+04 (3.369e+04-4.236e+04) | -7.3% | 4.504e+04, 4.337e+04, 4.398e+04 / 3.954e+04, 4.147e+04, 3.802e+04 | separated, inside spread |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 3.353e+04 (2.451e+04-3.706e+04) | 3.535e+04 (2.887e+04-3.723e+04) | +5.4% | 3.307e+04, 3.078e+04, 3.402e+04 / 3.396e+04, 3.29e+04, 3.535e+04 | within noise |
