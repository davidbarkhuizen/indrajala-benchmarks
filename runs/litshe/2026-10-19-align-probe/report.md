Old `b900778` against new `504a1f6`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `a722c7c` (extension sha256 `2d514ad229dc`) and new crate `18e195a` (extension sha256 `b9c70f113d09`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (raspberry-pi-5.json); passes peaked at 52.9-58.4 C; max 1-min load 3.47 (HIGH) (measured just after this run's crate builds); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / conv 13x13x8, 8 ch downstream_batch b512 / rust -86.9% (4.932e+04 -> 6474 µs)
- consistent: per call / conv 28x28, 8 ch downstream_batch b512 / rust -80.8% (5.284e+04 -> 1.014e+04 µs)
- consistent: per call / conv 26x26x8, 8 ch downstream_batch b512 / rust -76.0% (2.423e+05 -> 5.813e+04 µs)
- consistent: per call / conv 26x26x8, 8 ch downstream_batch b32 / rust -72.7% (1.286e+04 -> 3514 µs)
- consistent: per call / conv 26x26x8/2, 8 ch downstream_batch b512 / rust -67.5% (6.924e+04 -> 2.25e+04 µs)
- consistent: per call / conv 26x26x8/2, 8 ch downstream_batch b32 / rust -63.3% (3417 -> 1254 µs)
- consistent: per call / pool 6x6, 8 ch downstream_batch b32 / rust -35.2% (12.12 -> 7.851 µs)
- consistent: per call / conv 8x8, 8 ch downstream_batch b512 / rust -35.2% (1879 -> 1218 µs)
- consistent: per call / conv 13x13x8, 8 ch downstream_batch b32 / rust -22.4% (1320 -> 1024 µs)
- consistent: per call / pool 6x6, 8 ch downstream / rust -21.2% (0.8267 -> 0.6516 µs)
- ... 28 more consistent rows (report --md)
- 232 rows within noise (24 separated inside their spread), max |Δ| 195.3%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 79.1 (76.96-79.78) | 78.46 (77.34-80.19) | -0.8% | 79.66, 79.1, 77.8 / 77.83, 78.83, 78.84 | within noise |
| conv tail 32 x 5408 forward / rust | 65.5 (53.62-75.52) | 73.05 (56.63-77.09) | +11.5% | 65.69, 75.2, 54.47 / 74.74, 64.99, 67.07 | within noise |
| conv tail 32 x 5408 downstream / numpy | 92.23 (91.24-92.97) | 93.59 (91-93.7) | +1.5% | 91.66, 92.87, 92.17 / 93.61, 92.33, 92.65 | within noise |
| conv tail 32 x 5408 downstream / rust | 74.98 (74.24-91) | 78.1 (74.34-92.31) | +4.2% | 82.48, 74.98, 82.62 / 83.32, 76.83, 84.97 | within noise |
| conv tail 32 x 5408 hidden_delta / numpy | 104.4 (103-105.5) | 105 (104.4-105.7) | +0.6% | 104.9, 103.7, 104.4 / 105, 105, 105 | separated, inside spread |
| conv tail 32 x 5408 hidden_delta / rust | 79.99 (78.65-86.82) | 80.36 (78.5-98.3) | +0.5% | 79.55, 80.77, 83.18 / 79.02, 89.74, 80.31 | within noise |
| conv tail 32 x 5408 accumulate_gradient / numpy | 815.9 (319.8-967) | 401.8 (318.7-789.5) | -50.8% | 373.9, 883.3, 898.5 / 401.8, 554.1, 377.6 | within noise |
| conv tail 32 x 5408 accumulate_gradient / rust | 91.36 (88.86-108.1) | 91.5 (89.73-109.5) | +0.2% | 90.88, 98.48, 94.98 / 99.87, 91.5, 94.11 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 1661 (1523-1844) | 1556 (1468-2082) | -6.3% | 1677, 1789, 1555 / 1494, 1837, 1650 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 504.1 (377.8-815.1) | 560.4 (374.2-813) | +11.2% | 502.2, 596.4, 517 / 662.4, 491.6, 554.4 | within noise |
| conv tail 32 x 5408 sgd step / numpy | 2779 (2230-2823) | 2322 (1918-3032) | -16.4% | 2526, 2531, 2779 / 2322, 1940, 2870 | within noise |
| conv tail 32 x 5408 sgd step / rust | 116.6 (116.1-122) | 120.6 (115.2-282.6) | +3.4% | 118.2, 119.1, 116.3 / 198.9, 118, 198.9 | within noise |
| conv tail 32 x 5408 forward_batch b32 / numpy | 525.8 (504.4-537.8) | 525.1 (509.6-547) | -0.1% | 508, 527.9, 535.3 / 519.5, 536, 517.4 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 1114 (1094-1131) | 1110 (1098-1123) | -0.4% | 1112, 1127, 1104 / 1110, 1109, 1115 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1.659e+04 (1.573e+04-1.916e+04) | 1.588e+04 (1.525e+04-1.722e+04) | -4.3% | 1.857e+04, 1.62e+04, 1.631e+04 / 1.576e+04, 1.554e+04, 1.668e+04 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1.125e+04 (1.021e+04-1.211e+04) | 1.104e+04 (1.048e+04-1.189e+04) | -1.9% | 1.149e+04, 1.109e+04, 1.092e+04 / 1.136e+04, 1.118e+04, 1.09e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 1538 (974-1665) | 1406 (1071-1575) | -8.6% | 1258, 1453, 1599 / 1378, 1436, 1323 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 1158 (1140-1498) | 1218 (1125-1366) | +5.2% | 1334, 1150, 1148 / 1289, 1174, 1259 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3.35e+04 (2.876e+04-3.803e+04) | 3.435e+04 (2.437e+04-4.57e+04) | +2.5% | 3.24e+04, 3.35e+04, 3.5e+04 / 4.093e+04, 2.72e+04, 3.639e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 1.874e+04 (1.148e+04-2.377e+04) | 1.884e+04 (1.404e+04-2.542e+04) | +0.5% | 2.045e+04, 1.592e+04, 1.905e+04 / 2.218e+04, 1.418e+04, 2.065e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 3279 (3020-4042) | 3464 (2792-4113) | +5.7% | 3512, 3674, 3247 / 3294, 3453, 3572 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 1881 (1611-2111) | 1945 (1537-2002) | +3.4% | 1870, 1750, 1881 / 1945, 1945, 1768 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 6.328e+04 (5.8e+04-6.479e+04) | 6.576e+04 (6.06e+04-6.987e+04) | +3.9% | 6.238e+04, 6.454e+04, 6.097e+04 / 6.738e+04, 6.342e+04, 6.523e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 2.708e+04 (2.328e+04-3.193e+04) | 2.779e+04 (2.306e+04-3.568e+04) | +2.6% | 2.374e+04, 2.956e+04, 2.72e+04 / 3.227e+04, 2.966e+04, 2.31e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 1691 (1536-2055) | 1882 (1616-2190) | +11.3% | 1936, 1619, 1674 / 1882, 2166, 1662 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 2217 (2024-2373) | 2238 (2018-2387) | +1.0% | 2209, 2217, 2199 / 2152, 2202, 2301 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 2.681e+04 (2.217e+04-2.744e+04) | 2.296e+04 (2.042e+04-2.386e+04) | -14.4% | 2.696e+04, 2.282e+04, 2.722e+04 / 2.346e+04, 2.21e+04, 2.225e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 1.975e+04 (1.908e+04-2.032e+04) | 1.958e+04 (1.821e+04-2.008e+04) | -0.9% | 1.965e+04, 1.975e+04, 1.97e+04 / 1.885e+04, 1.983e+04, 1.959e+04 | within noise |
| dense 30 x 784 forward / numpy | 16.25 (15.94-16.53) | 16.3 (16.18-16.42) | +0.3% | 16.31, 16.17, 16.23 / 16.34, 16.34, 16.24 | within noise |
| dense 30 x 784 forward / rust | 6.444 (6.357-6.537) | 6.507 (6.446-6.68) | +1.0% | 6.422, 6.498, 6.433 / 6.519, 6.571, 6.478 | within noise |
| dense 30 x 784 downstream / numpy | 12.67 (12.65-12.7) | 12.69 (12.64-12.83) | +0.1% | 12.69, 12.66, 12.66 / 12.66, 12.73, 12.71 | within noise |
| dense 30 x 784 downstream / rust | 6.627 (6.304-6.641) | 6.463 (6.302-6.78) | -2.5% | 6.627, 6.638, 6.454 / 6.541, 6.476, 6.463 | within noise |
| dense 30 x 784 hidden_delta / numpy | 17.15 (17.08-17.24) | 17.04 (16.92-17.08) | -0.6% | 17.19, 17.17, 17.12 / 17.04, 17.03, 17 | consistent, small |
| dense 30 x 784 hidden_delta / rust | 7.468 (7.22-7.534) | 7.315 (7.189-7.59) | -2.1% | 7.469, 7.468, 7.377 / 7.335, 7.473, 7.238 | within noise |
| dense 30 x 784 accumulate_gradient / numpy | 42.78 (42.59-42.97) | 42.62 (42.56-42.68) | -0.4% | 42.59, 42.9, 42.85 / 42.62, 42.62, 42.62 | within noise |
| dense 30 x 784 accumulate_gradient / rust | 9.801 (9.618-10.06) | 9.88 (9.842-9.933) | +0.8% | 9.726, 9.939, 9.739 / 9.913, 9.868, 9.868 | within noise |
| dense 30 x 784 apply_accumulated_gradient / numpy | 61.16 (61.02-61.45) | 61.16 (61.08-61.35) | -0.0% | 61.16, 61.05, 61.33 / 61.1, 61.21, 61.25 | within noise |
| dense 30 x 784 apply_accumulated_gradient / rust | 36.3 (36.12-36.48) | 36.32 (36.25-36.62) | +0.1% | 36.25, 36.3, 36.34 / 36.49, 36.31, 36.28 | within noise |
| dense 30 x 784 sgd step / numpy | 108.1 (107.9-108.4) | 108 (107.8-108.5) | -0.1% | 108.1, 108.2, 108 / 108.2, 108.1, 107.8 | within noise |
| dense 30 x 784 sgd step / rust | 15.78 (15.62-15.81) | 15.71 (15.66-15.75) | -0.5% | 15.79, 15.62, 15.79 / 15.68, 15.74, 15.7 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 92.37 (90.94-459.3) | 272.8 (91.04-466.8) | +195.3% | 275.1, 92.37, 271.9 / 455.1, 279.1, 91.16 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 115.8 (115.7-119.1) | 117.4 (115.8-120) | +1.4% | 115.7, 118.6, 115.7 / 117.4, 119.5, 115.8 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 2404 (2330-2758) | 2579 (2131-2689) | +7.3% | 2528, 2385, 2544 / 2579, 2511, 2410 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 1027 (989.3-1046) | 1003 (957.2-1069) | -2.4% | 1012, 1031, 1033 / 981.9, 1034, 1004 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 220.5 (57.49-400.3) | 381.6 (57.43-400.1) | +73.0% | 228.9, 220.5, 223.2 / 393.8, 223.4, 216.9 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 125.7 (125.7-126.9) | 128.1 (125.9-128.1) | +1.9% | 126.3, 125.7, 125.8 / 127, 127.1, 128.1 | separated, inside spread |
| dense 30 x 784 downstream_batch b512 / numpy | 3494 (2614-4312) | 3247 (2759-3438) | -7.1% | 4279, 2775, 3494 / 3025, 3252, 3287 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 1886 (1559-2004) | 2173 (1600-2573) | +15.2% | 1796, 1886, 1781 / 2508, 2173, 1782 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 105.3 (104.5-298.3) | 200.1 (104.6-300.7) | +90.0% | 199.5, 201.4, 105 / 200.1, 202.6, 199.4 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / rust | 156.1 (151.7-303.9) | 153.4 (148.9-156.2) | -1.7% | 158.5, 228.8, 152.6 / 155.1, 153, 150.8 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 8903 (7680-1.266e+04) | 8018 (7292-9473) | -9.9% | 1.1e+04, 8148, 8898 / 8723, 7679, 8612 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / rust | 3167 (2648-3951) | 2826 (2573-3117) | -10.8% | 3504, 3249, 2963 / 2826, 2845, 2744 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 86.96 (86.68-448.7) | 87.6 (86.6-448.6) | +0.7% | 267, 86.86, 267.8 / 446.3, 87.26, 87.21 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 139.6 (139-141.1) | 140.6 (139.9-141.2) | +0.7% | 140.2, 139.5, 140 / 140.1, 140.7, 141.1 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 2175 (1959-1.714e+04) | 1846 (1769-2093) | -15.2% | 2166, 9647, 2089 / 1931, 1934, 1839 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 2403 (2230-2779) | 2587 (2410-2779) | +7.7% | 2356, 2671, 2311 / 2569, 2632, 2595 | within noise |
| dense 10 x 30 forward / numpy | 8.197 (8.167-8.254) | 8.112 (8.088-8.151) | -1.0% | 8.195, 8.179, 8.23 / 8.102, 8.118, 8.13 | separated, inside spread |
| dense 10 x 30 forward / rust | 0.6226 (0.6211-0.6371) | 0.629 (0.6244-0.6525) | +1.0% | 0.6294, 0.6237, 0.6217 / 0.6299, 0.6421, 0.6245 | within noise |
| dense 10 x 30 downstream / numpy | 1.826 (1.802-1.869) | 1.816 (1.803-1.838) | -0.5% | 1.814, 1.849, 1.818 / 1.82, 1.816, 1.814 | within noise |
| dense 10 x 30 downstream / rust | 0.3844 (0.381-0.3863) | 0.3835 (0.3817-0.3898) | -0.2% | 0.3826, 0.386, 0.3831 / 0.3826, 0.3863, 0.3857 | within noise |
| dense 10 x 30 hidden_delta / numpy | 4.558 (4.514-4.592) | 4.547 (4.505-4.606) | -0.2% | 4.536, 4.575, 4.564 / 4.547, 4.539, 4.56 | within noise |
| dense 10 x 30 hidden_delta / rust | 0.7975 (0.7874-0.811) | 0.7925 (0.7857-0.7968) | -0.6% | 0.7975, 0.7903, 0.8108 / 0.7879, 0.7965, 0.7925 | within noise |
| dense 10 x 30 accumulate_gradient / numpy | 5.28 (5.258-5.305) | 5.264 (5.254-5.289) | -0.3% | 5.296, 5.286, 5.26 / 5.275, 5.255, 5.268 | within noise |
| dense 10 x 30 accumulate_gradient / rust | 0.7805 (0.7707-0.7891) | 0.7845 (0.7741-0.7934) | +0.5% | 0.7724, 0.7805, 0.7886 / 0.7848, 0.7888, 0.7755 | within noise |
| dense 10 x 30 apply_accumulated_gradient / numpy | 8.962 (8.862-9.075) | 8.932 (8.877-9.161) | -0.3% | 9.055, 8.917, 8.913 / 8.932, 9.003, 9.019 | within noise |
| dense 10 x 30 apply_accumulated_gradient / rust | 4.083 (4.057-4.114) | 4.051 (4.018-4.082) | -0.8% | 4.089, 4.096, 4.068 / 4.018, 4.051, 4.071 | within noise |
| dense 10 x 30 sgd step / numpy | 15.03 (14.94-15.06) | 15 (14.95-15.31) | -0.2% | 15, 15, 15.05 / 15.06, 14.98, 15.16 | within noise |
| dense 10 x 30 sgd step / rust | 0.9311 (0.9269-1.021) | 0.9319 (0.9302-0.9343) | +0.1% | 0.9306, 0.974, 0.9311 / 0.9342, 0.931, 0.9312 | within noise |
| dense 10 x 30 forward_batch b32 / numpy | 19.45 (19.38-19.51) | 19.42 (19.31-19.58) | -0.1% | 19.45, 19.45, 19.45 / 19.49, 19.44, 19.39 | within noise |
| dense 10 x 30 forward_batch b32 / rust | 7.287 (7.283-7.292) | 7.352 (7.337-7.362) | +0.9% | 7.286, 7.287, 7.288 / 7.355, 7.349, 7.351 | consistent, small |
| dense 10 x 30 forward_batch b512 / numpy | 151.5 (151.1-151.8) | 151.5 (150.7-153.5) | +0.0% | 151.6, 151.3, 151.5 / 151.5, 153.1, 150.8 | within noise |
| dense 10 x 30 forward_batch b512 / rust | 107.5 (107.3-107.7) | 108.5 (108.3-108.6) | +1.0% | 107.7, 107.3, 107.5 / 108.4, 108.6, 108.5 | consistent, small |
| dense 10 x 30 downstream_batch b32 / numpy | 5.948 (5.927-5.977) | 5.936 (5.915-5.981) | -0.2% | 5.974, 5.935, 5.948 / 5.95, 5.931, 5.954 | within noise |
| dense 10 x 30 downstream_batch b32 / rust | 3.224 (3.222-3.233) | 3.22 (3.213-3.231) | -0.1% | 3.233, 3.223, 3.223 / 3.223, 3.221, 3.22 | within noise |
| dense 10 x 30 downstream_batch b512 / numpy | 64.59 (64.43-64.71) | 64.61 (64.47-64.78) | +0.0% | 64.52, 64.66, 64.54 / 64.55, 64.66, 64.68 | within noise |
| dense 10 x 30 downstream_batch b512 / rust | 46.05 (45.89-46.46) | 46.23 (45.77-46.35) | +0.4% | 45.98, 46.1, 46.24 / 46.33, 45.97, 46.06 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 10.49 (10.38-10.6) | 10.46 (10.38-10.6) | -0.3% | 10.54, 10.44, 10.53 / 10.41, 10.55, 10.44 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 4.103 (4.092-4.123) | 4.099 (4.085-4.107) | -0.1% | 4.113, 4.102, 4.107 / 4.1, 4.092, 4.097 | separated, inside spread |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 94.28 (93.12-94.99) | 93.95 (92.73-95.14) | -0.3% | 94.24, 94.28, 93.94 / 93.9, 93.93, 94.47 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / rust | 54.98 (54.39-55.1) | 54.86 (54.41-55.16) | -0.2% | 55.09, 54.68, 54.95 / 55.1, 54.85, 54.63 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 9.614 (9.52-9.707) | 9.605 (9.501-9.782) | -0.1% | 9.619, 9.54, 9.671 / 9.67, 9.557, 9.608 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 4.246 (4.219-4.261) | 4.575 (4.572-4.594) | +7.7% | 4.248, 4.234, 4.252 / 4.577, 4.572, 4.584 | consistent |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 47.69 (47.44-48.21) | 47.69 (47.5-47.8) | +0.0% | 47.6, 47.73, 47.82 / 47.63, 47.59, 47.77 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 59.01 (58.8-59.1) | 59.23 (59.01-59.3) | +0.4% | 58.83, 59.03, 59.05 / 59.25, 59.02, 59.27 | within noise |
| conv 28x28, 8 ch forward / numpy | 85.51 (84.94-86.65) | 85.69 (84.79-85.96) | +0.2% | 85.21, 85.93, 85.99 / 85.4, 85.7, 85.37 | within noise |
| conv 28x28, 8 ch forward / rust | 46.77 (46.76-46.81) | 46.78 (46.76-46.8) | +0.0% | 46.78, 46.77, 46.77 / 46.78, 46.79, 46.77 | within noise |
| conv 28x28, 8 ch downstream / numpy | 70.98 (70.65-71.08) | 71.23 (70.71-72.13) | +0.4% | 70.96, 70.99, 70.87 / 71.14, 71.42, 71.23 | separated, inside spread |
| conv 28x28, 8 ch downstream / rust | 42.07 (41.89-42.16) | 46.52 (46.49-46.65) | +10.6% | 42.01, 42.15, 42.01 / 46.51, 46.62, 46.5 | consistent |
| conv 28x28, 8 ch accumulate_gradient / numpy | 60.18 (57.79-60.61) | 57.97 (57.74-61.65) | -3.7% | 60.5, 58.95, 59.08 / 57.87, 59.19, 59.85 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 30.23 (30.2-30.29) | 31.54 (31.52-31.62) | +4.3% | 30.25, 30.21, 30.26 / 31.57, 31.54, 31.54 | consistent |
| conv 28x28, 8 ch forward_batch b32 / numpy | 4420 (3859-4712) | 4478 (3629-6006) | +1.3% | 4296, 4420, 4220 / 4817, 4356, 4779 | within noise |
| conv 28x28, 8 ch forward_batch b32 / rust | 1590 (1533-1761) | 1623 (1500-1954) | +2.0% | 1590, 1636, 1647 / 1814, 1679, 1556 | within noise |
| conv 28x28, 8 ch forward_batch b512 / numpy | 6.847e+04 (6.649e+04-7.05e+04) | 6.746e+04 (6.66e+04-7.084e+04) | -1.5% | 6.966e+04, 6.895e+04, 6.663e+04 / 6.931e+04, 6.687e+04, 6.755e+04 | within noise |
| conv 28x28, 8 ch forward_batch b512 / rust | 3.202e+04 (3.137e+04-3.265e+04) | 3.244e+04 (3.123e+04-3.336e+04) | +1.3% | 3.237e+04, 3.17e+04, 3.192e+04 / 3.217e+04, 3.282e+04, 3.219e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 1513 (1476-1611) | 1546 (1455-1949) | +2.1% | 1543, 1507, 1540 / 1770, 1496, 1526 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / rust | 2525 (2074-3191) | 1423 (1420-1425) | -43.6% | 3034, 2611, 2075 / 1423, 1423, 1423 | separated, inside spread |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 5.306e+04 (5.003e+04-5.619e+04) | 5.299e+04 (5.065e+04-5.578e+04) | -0.1% | 5.306e+04, 5.175e+04, 5.451e+04 / 5.414e+04, 5.293e+04, 5.321e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / rust | 5.284e+04 (5.02e+04-5.937e+04) | 1.014e+04 (9593-1.137e+04) | -80.8% | 5.502e+04, 5.134e+04, 5.432e+04 / 1.031e+04, 9599, 1.068e+04 | consistent |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 2283 (2242-2322) | 2250 (2244-2316) | -1.4% | 2320, 2245, 2283 / 2281, 2278, 2248 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 1149 (1111-1466) | 1200 (1176-1501) | +4.5% | 1165, 1289, 1127 / 1346, 1182, 1220 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 3.815e+04 (3.711e+04-3.871e+04) | 3.768e+04 (3.717e+04-3.828e+04) | -1.3% | 3.845e+04, 3.716e+04, 3.815e+04 / 3.824e+04, 3.767e+04, 3.721e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 2.848e+04 (2.673e+04-3.12e+04) | 2.919e+04 (2.742e+04-3.2e+04) | +2.5% | 2.946e+04, 2.681e+04, 2.988e+04 / 2.84e+04, 3.004e+04, 3.001e+04 | within noise |
| conv 8x8, 8 ch forward / numpy | 34.82 (34.55-36.38) | 34.78 (34.58-36.21) | -0.1% | 35.59, 34.7, 34.88 / 34.78, 34.7, 35.4 | within noise |
| conv 8x8, 8 ch forward / rust | 3.407 (3.402-3.425) | 3.397 (3.389-3.404) | -0.3% | 3.415, 3.405, 3.412 / 3.397, 3.396, 3.399 | separated, inside spread |
| conv 8x8, 8 ch downstream / numpy | 39.98 (39.62-40.84) | 39.81 (39.36-40.93) | -0.4% | 40.23, 39.94, 40.25 / 40.29, 40.14, 39.5 | within noise |
| conv 8x8, 8 ch downstream / rust | 2.805 (2.803-2.812) | 2.927 (2.917-2.94) | +4.3% | 2.805, 2.804, 2.811 / 2.924, 2.921, 2.936 | consistent |
| conv 8x8, 8 ch accumulate_gradient / numpy | 12.54 (12.49-12.8) | 12.45 (12.37-12.87) | -0.7% | 12.55, 12.65, 12.53 / 12.65, 12.62, 12.43 | within noise |
| conv 8x8, 8 ch accumulate_gradient / rust | 2.322 (2.306-2.338) | 2.41 (2.405-2.425) | +3.8% | 2.318, 2.317, 2.331 / 2.414, 2.415, 2.41 | consistent |
| conv 8x8, 8 ch forward_batch b32 / numpy | 129.4 (127.7-131.6) | 130.5 (129.8-131.2) | +0.9% | 129.4, 128.8, 129.8 / 130.1, 130.6, 130.8 | separated, inside spread |
| conv 8x8, 8 ch forward_batch b32 / rust | 80.15 (79.98-80.35) | 80.14 (79.98-83.16) | -0.0% | 80.07, 80.15, 80.25 / 80.05, 80.15, 81.57 | within noise |
| conv 8x8, 8 ch forward_batch b512 / numpy | 3576 (3294-4148) | 3678 (3455-3900) | +2.9% | 3576, 3486, 3824 / 3678, 3703, 3678 | within noise |
| conv 8x8, 8 ch forward_batch b512 / rust | 1780 (1468-1948) | 1496 (1393-1623) | -16.0% | 1726, 1899, 1581 / 1550, 1496, 1457 | separated, inside spread |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 116.4 (114.8-125) | 116.9 (114.8-118) | +0.4% | 115.9, 116.4, 120.4 / 115.2, 117.1, 117.6 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / rust | 74.23 (74.14-74.77) | 76.45 (76.33-76.59) | +3.0% | 74.23, 74.5, 74.17 / 76.56, 76.35, 76.45 | consistent |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 1900 (1586-2014) | 1618 (1595-2032) | -14.8% | 1746, 1742, 1962 / 1828, 1618, 1604 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / rust | 1879 (1604-2204) | 1218 (1215-1221) | -35.2% | 2117, 1778, 1774 / 1217, 1220, 1218 | consistent |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 150.8 (148.6-153.6) | 148.5 (148.2-149.1) | -1.5% | 151.3, 150.6, 151 / 148.8, 148.4, 148.5 | consistent |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 51.96 (51.87-52.04) | 54.25 (54.19-54.31) | +4.4% | 51.97, 51.96, 51.96 / 54.27, 54.28, 54.2 | consistent |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 2304 (2294-2400) | 2339 (2290-2362) | +1.5% | 2330, 2353, 2301 / 2340, 2328, 2326 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 1131 (986.3-1290) | 1011 (1001-1341) | -10.6% | 1143, 986.6, 1271 / 1178, 1003, 1148 | within noise |
| conv 13x13x8, 8 ch forward / numpy | 79.83 (79.14-80.89) | 79.72 (79.19-81.19) | -0.1% | 79.83, 79.8, 80.01 / 79.42, 80.74, 79.52 | within noise |
| conv 13x13x8, 8 ch forward / rust | 48.22 (48.15-48.25) | 49.05 (48.18-49.28) | +1.7% | 48.19, 48.21, 48.24 / 49.05, 48.81, 48.73 | consistent |
| conv 13x13x8, 8 ch downstream / numpy | 89.21 (88.8-89.63) | 89.66 (88.62-90.85) | +0.5% | 89.25, 89.21, 89.19 / 88.67, 90.08, 90.15 | within noise |
| conv 13x13x8, 8 ch downstream / rust | 32.35 (31.97-32.46) | 33.72 (33.42-33.8) | +4.2% | 32.38, 32.21, 32.17 / 33.6, 33.72, 33.72 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 40.5 (40.19-40.86) | 40.49 (40.09-41.04) | -0.0% | 40.38, 40.39, 40.76 / 40.49, 40.38, 40.59 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 14.87 (14.85-14.9) | 16.35 (16.32-16.38) | +9.9% | 14.89, 14.86, 14.86 / 16.37, 16.33, 16.35 | consistent |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 2507 (2382-3203) | 2454 (2376-2645) | -2.1% | 2935, 2507, 2384 / 2463, 2438, 2510 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 2284 (2164-2446) | 2097 (1973-2190) | -8.2% | 2278, 2330, 2284 / 2130, 2091, 2082 | consistent |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 4.948e+04 (4.89e+04-4.976e+04) | 4.895e+04 (4.835e+04-4.951e+04) | -1.1% | 4.942e+04, 4.913e+04, 4.966e+04 / 4.913e+04, 4.863e+04, 4.92e+04 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 5.269e+04 (4.838e+04-5.324e+04) | 4.902e+04 (4.794e+04-5.479e+04) | -7.0% | 5.269e+04, 5.173e+04, 5.081e+04 / 4.824e+04, 5.019e+04, 5.195e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 4336 (3908-4399) | 4085 (3910-4404) | -5.8% | 4364, 3959, 4360 / 3939, 4242, 4246 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 1320 (1274-1347) | 1024 (1015-1027) | -22.4% | 1300, 1333, 1301 / 1023, 1021, 1024 | consistent |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 1.126e+05 (1.081e+05-1.154e+05) | 1.1e+05 (1.062e+05-1.133e+05) | -2.3% | 1.132e+05, 1.117e+05, 1.121e+05 / 1.102e+05, 1.082e+05, 1.111e+05 | separated, inside spread |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 4.932e+04 (4.631e+04-5.338e+04) | 6474 (5999-7719) | -86.9% | 5.198e+04, 5.002e+04, 4.654e+04 / 6859, 6764, 6474 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 1136 (1125-1141) | 1137 (1134-1149) | +0.1% | 1133, 1137, 1136 / 1134, 1137, 1149 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 605.6 (596.2-615) | 639.9 (636-644.4) | +5.7% | 611.4, 601.1, 602.7 / 643.2, 637.4, 639.6 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.837e+04 (1.829e+04-1.869e+04) | 1.837e+04 (1.829e+04-1.841e+04) | +0.0% | 1.849e+04, 1.837e+04, 1.848e+04 / 1.833e+04, 1.838e+04, 1.839e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 1.164e+04 (1.103e+04-1.274e+04) | 1.209e+04 (1.15e+04-1.254e+04) | +3.9% | 1.207e+04, 1.187e+04, 1.143e+04 / 1.221e+04, 1.202e+04, 1.208e+04 | within noise |
| conv 26x26x8/2, 8 ch forward / numpy | 90.25 (89.71-92.24) | 91.13 (90.07-99.63) | +1.0% | 90.98, 90.25, 90.72 / 95.54, 91.02, 90.44 | within noise |
| conv 26x26x8/2, 8 ch forward / rust | 57.04 (57.02-57.33) | 58.07 (58.02-58.16) | +1.8% | 57.18, 57.03, 57.06 / 58.06, 58.11, 58.07 | consistent |
| conv 26x26x8/2, 8 ch downstream / numpy | 103.6 (102.9-105.1) | 103.5 (103.4-103.9) | -0.1% | 103.4, 104.4, 103.1 / 103.4, 103.7, 103.6 | within noise |
| conv 26x26x8/2, 8 ch downstream / rust | 38.69 (38.1-38.74) | 39.78 (39.72-40.19) | +2.8% | 38.65, 38.73, 38.42 / 39.98, 39.97, 39.74 | consistent |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 47.92 (47.33-48.31) | 47.81 (47.24-48.44) | -0.2% | 48.07, 47.82, 47.7 / 48.14, 47.51, 47.77 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 17.46 (17.4-17.51) | 19.28 (19.22-19.33) | +10.4% | 17.49, 17.43, 17.43 / 19.27, 19.32, 19.24 | consistent |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 3443 (3176-3943) | 3322 (2992-3683) | -3.5% | 3632, 3371, 3540 / 3255, 3161, 3498 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 2804 (2754-3239) | 2597 (2533-2755) | -7.4% | 3028, 2766, 2869 / 2564, 2646, 2649 | separated, inside spread |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 6.23e+04 (6.177e+04-6.386e+04) | 6.349e+04 (6.228e+04-6.462e+04) | +1.9% | 6.348e+04, 6.186e+04, 6.223e+04 / 6.345e+04, 6.411e+04, 6.281e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 5.893e+04 (5.644e+04-6.343e+04) | 5.828e+04 (5.701e+04-6.201e+04) | -1.1% | 5.993e+04, 6.092e+04, 5.824e+04 / 6.059e+04, 5.922e+04, 5.739e+04 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 8930 (8195-9804) | 8678 (7521-1.036e+04) | -2.8% | 9083, 8533, 9222 / 9279, 8942, 8247 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 3417 (2572-4095) | 1254 (1232-1257) | -63.3% | 3417, 3445, 3317 / 1254, 1257, 1242 | consistent |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 1.81e+05 (1.768e+05-1.953e+05) | 1.807e+05 (1.723e+05-1.885e+05) | -0.2% | 1.791e+05, 1.878e+05, 1.823e+05 / 1.865e+05, 1.76e+05, 1.772e+05 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 6.924e+04 (6.821e+04-7.215e+04) | 2.25e+04 (2.089e+04-2.45e+04) | -67.5% | 7.042e+04, 6.924e+04, 6.906e+04 / 2.129e+04, 2.331e+04, 2.313e+04 | consistent |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 1388 (1379-1397) | 1397 (1387-1404) | +0.6% | 1388, 1388, 1388 / 1397, 1402, 1391 | separated, inside spread |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 725.6 (677.3-785) | 774.1 (740.8-834.3) | +6.7% | 773.8, 680.3, 732.8 / 787.6, 759.8, 774.1 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 2.221e+04 (2.217e+04-2.229e+04) | 2.254e+04 (2.205e+04-2.298e+04) | +1.5% | 2.224e+04, 2.22e+04, 2.223e+04 / 2.212e+04, 2.293e+04, 2.249e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 1.551e+04 (1.393e+04-1.765e+04) | 1.53e+04 (1.417e+04-1.757e+04) | -1.4% | 1.66e+04, 1.502e+04, 1.476e+04 / 1.611e+04, 1.447e+04, 1.661e+04 | within noise |
| conv 26x26x8, 8 ch forward / numpy | 245.5 (244.3-413.8) | 245.1 (244.3-403.8) | -0.2% | 329.1, 245.5, 245.8 / 324, 245.7, 245.1 | within noise |
| conv 26x26x8, 8 ch forward / rust | 222.1 (222-223.1) | 226.3 (226-227.6) | +1.9% | 223.1, 222, 222 / 226.3, 226.9, 226.1 | consistent |
| conv 26x26x8, 8 ch downstream / numpy | 254.6 (254-259.5) | 256.7 (252.3-258.9) | +0.8% | 254.6, 255.1, 256.8 / 256.9, 255.7, 255.6 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 145.2 (145-147.1) | 154.4 (154.3-155.9) | +6.3% | 145.5, 146.1, 145.2 / 154.7, 154.3, 155.1 | consistent |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 159.6 (158.8-160.6) | 160.6 (156.9-162.7) | +0.7% | 159.6, 159.7, 159.8 / 161.5, 161.5, 157.8 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 65.12 (64.78-66.43) | 72.2 (71.93-72.57) | +10.9% | 64.97, 65.14, 65.69 / 72.06, 72.2, 72.49 | consistent |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 1.373e+04 (1.238e+04-1.536e+04) | 1.434e+04 (1.317e+04-1.501e+04) | +4.5% | 1.461e+04, 1.382e+04, 1.311e+04 / 1.35e+04, 1.483e+04, 1.434e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 1.213e+04 (1.132e+04-1.322e+04) | 1.168e+04 (1.09e+04-1.328e+04) | -3.7% | 1.24e+04, 1.166e+04, 1.227e+04 / 1.174e+04, 1.168e+04, 1.209e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 2.426e+05 (2.41e+05-2.565e+05) | 2.451e+05 (2.344e+05-2.582e+05) | +1.1% | 2.432e+05, 2.419e+05, 2.488e+05 / 2.53e+05, 2.37e+05, 2.451e+05 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 2.227e+05 (2.199e+05-2.277e+05) | 2.247e+05 (2.23e+05-2.275e+05) | +0.9% | 2.249e+05, 2.218e+05, 2.238e+05 / 2.239e+05, 2.243e+05, 2.264e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 2.524e+04 (2.475e+04-2.67e+04) | 2.509e+04 (2.43e+04-2.908e+04) | -0.6% | 2.573e+04, 2.491e+04, 2.611e+04 / 2.669e+04, 2.521e+04, 2.503e+04 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 1.286e+04 (1.131e+04-1.582e+04) | 3514 (2928-4000) | -72.7% | 1.36e+04, 1.403e+04, 1.186e+04 / 3163, 3656, 3751 | consistent |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 4.953e+05 (4.82e+05-5.167e+05) | 4.965e+05 (4.912e+05-5.093e+05) | +0.3% | 4.892e+05, 5.128e+05, 4.931e+05 / 4.952e+05, 4.936e+05, 5.052e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 2.423e+05 (2.382e+05-2.463e+05) | 5.813e+04 (4.945e+04-6.256e+04) | -76.0% | 2.435e+05, 2.417e+05, 2.417e+05 / 5.373e+04, 6.107e+04, 5.519e+04 | consistent |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 5643 (5605-5670) | 5650 (5633-5672) | +0.1% | 5636, 5661, 5620 / 5651, 5663, 5641 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 3258 (3099-3664) | 3565 (3308-4011) | +9.4% | 3476, 3329, 3164 / 3367, 3697, 3724 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 8.879e+04 (8.835e+04-8.966e+04) | 8.905e+04 (8.875e+04-8.987e+04) | +0.3% | 8.876e+04, 8.923e+04, 8.871e+04 / 8.905e+04, 8.938e+04, 8.919e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 5.46e+04 (5.029e+04-5.727e+04) | 5.667e+04 (5.376e+04-6.071e+04) | +3.8% | 5.238e+04, 5.487e+04, 5.414e+04 / 5.879e+04, 5.512e+04, 5.68e+04 | separated, inside spread |
| pool 26x26, 8 ch forward / numpy | 105.5 (105.1-105.9) | 106.4 (105-107.7) | +0.8% | 105.6, 105.4, 105.5 / 105.8, 106.4, 107 | separated, inside spread |
| pool 26x26, 8 ch forward / rust | 5.308 (5.297-5.331) | 5.225 (5.212-5.233) | -1.6% | 5.301, 5.321, 5.314 / 5.226, 5.227, 5.219 | consistent |
| pool 26x26, 8 ch downstream / numpy | 55.35 (54.93-56.48) | 55.37 (54.91-56.12) | +0.0% | 55.05, 56.27, 55.28 / 55.75, 54.96, 55.43 | within noise |
| pool 26x26, 8 ch downstream / rust | 4.296 (4.282-4.312) | 4.138 (4.115-4.164) | -3.7% | 4.295, 4.297, 4.296 / 4.121, 4.138, 4.153 | consistent |
| pool 26x26, 8 ch forward_batch b32 / numpy | 2419 (2401-2506) | 2404 (2387-3328) | -0.6% | 2488, 2405, 2418 / 2398, 2402, 2867 | within noise |
| pool 26x26, 8 ch forward_batch b32 / rust | 231.5 (197.9-236) | 231.3 (201.8-447.8) | -0.1% | 231.2, 234.1, 214.3 / 218.4, 221.4, 338.6 | within noise |
| pool 26x26, 8 ch forward_batch b512 / numpy | 4.03e+04 (3.924e+04-4.175e+04) | 3.932e+04 (3.891e+04-4.083e+04) | -2.4% | 4.119e+04, 4.006e+04, 3.961e+04 / 3.954e+04, 3.906e+04, 4.017e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 8245 (7777-8813) | 8852 (8005-9724) | +7.4% | 8497, 8031, 8295 / 8884, 8518, 9178 | separated, inside spread |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 981.7 (950-1505) | 968.1 (951.8-1428) | -1.4% | 1242, 1228, 966.9 / 1213, 965.8, 954.6 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / rust | 472.6 (133.9-477.2) | 264.2 (129.6-479.4) | -44.1% | 474.6, 303.6, 305.1 / 477.5, 130.1, 264 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 5.537e+04 (5.178e+04-6.347e+04) | 5.476e+04 (5.018e+04-5.91e+04) | -1.1% | 5.521e+04, 5.537e+04, 5.836e+04 / 5.352e+04, 5.298e+04, 5.693e+04 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / rust | 2.088e+04 (1.994e+04-2.27e+04) | 2.132e+04 (1.917e+04-2.293e+04) | +2.1% | 2.205e+04, 2.092e+04, 2.01e+04 / 2.011e+04, 2.129e+04, 2.226e+04 | within noise |
| pool 6x6, 8 ch forward / numpy | 39.62 (39.46-40.95) | 40.08 (39.54-40.88) | +1.2% | 39.58, 39.53, 40.58 / 39.87, 39.8, 40.6 | within noise |
| pool 6x6, 8 ch forward / rust | 0.7949 (0.7885-0.8059) | 0.7593 (0.7545-0.7696) | -4.5% | 0.7972, 0.7941, 0.7949 / 0.762, 0.7608, 0.7584 | consistent |
| pool 6x6, 8 ch downstream / numpy | 32.62 (32.33-32.71) | 32.59 (32.33-32.86) | -0.1% | 32.39, 32.66, 32.64 / 32.67, 32.53, 32.59 | within noise |
| pool 6x6, 8 ch downstream / rust | 0.8267 (0.8109-0.8402) | 0.6516 (0.6475-0.6566) | -21.2% | 0.8276, 0.8255, 0.8251 / 0.653, 0.6544, 0.6492 | consistent |
| pool 6x6, 8 ch forward_batch b32 / numpy | 168.5 (167.8-294.3) | 167.9 (167.2-227.9) | -0.4% | 168.1, 168.7, 231.5 / 197.5, 167.9, 167.8 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 10.6 (10.55-10.63) | 10.55 (10.52-10.6) | -0.5% | 10.61, 10.61, 10.57 / 10.56, 10.58, 10.55 | within noise |
| pool 6x6, 8 ch forward_batch b512 / numpy | 2206 (2167-2537) | 2225 (2178-2303) | +0.9% | 2192, 2184, 2384 / 2186, 2249, 2265 | within noise |
| pool 6x6, 8 ch forward_batch b512 / rust | 170 (165.5-172.2) | 165.5 (164.2-169.7) | -2.6% | 171, 167.9, 168.5 / 167.5, 164.8, 167.1 | separated, inside spread |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 85.39 (85.09-86.44) | 85.64 (84.75-86.41) | +0.3% | 85.6, 85.87, 85.22 / 85.64, 85.58, 85.45 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / rust | 12.12 (12.09-12.14) | 7.851 (7.821-7.925) | -35.2% | 12.13, 12.11, 12.12 / 7.826, 7.851, 7.9 | consistent |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 939.5 (935.7-941.8) | 939 (936.5-940.4) | -0.0% | 941.1, 937.2, 938.7 / 939.9, 938, 937.7 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 198.6 (196.1-455.3) | 129.1 (128.8-333.3) | -35.0% | 327.9, 196.6, 303.7 / 129.1, 129.2, 231 | within noise |
| conv tail 32 x 5408 bare downstream b32 / numpy | 1450 (1123-1610) | 1449 (1245-1704) | -0.1% | 1460, 1429, 1315 / 1257, 1545, 1595 | within noise |
| conv tail 32 x 5408 bare downstream b32 / rust | 1346 (1156-1613) | 1434 (1138-1660) | +6.5% | 1391, 1185, 1541 / 1441, 1414, 1397 | within noise |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3.469e+04 (3.007e+04-3.862e+04) | 3.272e+04 (2.681e+04-3.591e+04) | -5.7% | 3.682e+04, 3.447e+04, 3.221e+04 / 3.35e+04, 3.443e+04, 2.865e+04 | within noise |
| conv tail 32 x 5408 bare downstream b512 / rust | 1.912e+04 (1.473e+04-2.417e+04) | 1.957e+04 (1.287e+04-2.388e+04) | +2.3% | 2.235e+04, 1.823e+04, 1.728e+04 / 2.196e+04, 1.841e+04, 1.67e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 1350 (930-1546) | 1267 (807.5-1517) | -6.1% | 1416, 964.4, 1430 / 1102, 1033, 1425 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / rust | 1285 (1156-1383) | 1190 (1092-1246) | -7.3% | 1259, 1371, 1197 / 1135, 1172, 1245 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 2.258e+04 (2.011e+04-2.727e+04) | 2.131e+04 (2.059e+04-2.512e+04) | -5.6% | 2.419e+04, 2.389e+04, 2.131e+04 / 2.078e+04, 2.357e+04, 2.131e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / rust | 1.862e+04 (1.822e+04-2.778e+04) | 1.838e+04 (1.745e+04-1.938e+04) | -1.3% | 1.861e+04, 1.859e+04, 2.308e+04 / 1.913e+04, 1.809e+04, 1.791e+04 | within noise |
| conv tail 32 x 5408 transpose b32 / numpy | 1.464 (1.452-1.479) | 1.476 (1.47-1.487) | +0.8% | 1.464, 1.466, 1.464 / 1.476, 1.478, 1.478 | consistent, small |
| conv tail 32 x 5408 transpose b32 / rust | 1.877 (1.872-1.88) | 1.877 (1.874-1.883) | +0.0% | 1.876, 1.875, 1.878 / 1.876, 1.88, 1.878 | within noise |
| conv tail 32 x 5408 transpose b512 / numpy | 30.06 (30.02-30.09) | 30.01 (29.78-30.11) | -0.1% | 30.03, 30.08, 30.05 / 30.04, 29.89, 30.01 | within noise |
| conv tail 32 x 5408 transpose b512 / rust | 26.84 (26.78-27.22) | 26.74 (26.67-27.06) | -0.3% | 26.87, 26.84, 27.01 / 26.88, 26.75, 26.74 | within noise |
| conv tail 32 x 5408 add b32 / numpy | 304.7 (290.1-315.1) | 315 (278.3-356.6) | +3.4% | 307.5, 304.7, 302.6 / 331.6, 317.4, 315 | separated, inside spread |
| conv tail 32 x 5408 add b32 / rust | 361.8 (286.6-412.8) | 330.9 (259.2-360.4) | -8.6% | 409.8, 331.9, 321.9 / 317, 356.5, 295.9 | within noise |
| conv tail 32 x 5408 add b512 / numpy | 363 (262-429.4) | 317.7 (269.9-385.1) | -12.5% | 367.7, 344.4, 352.9 / 359.5, 272.1, 317.7 | within noise |
| conv tail 32 x 5408 add b512 / rust | 331.6 (300.9-363.9) | 372 (310.7-425.8) | +12.2% | 349.5, 323.2, 315 / 419.8, 314, 377.3 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 2.851 (2.822-2.899) | 2.823 (2.809-2.85) | -1.0% | 2.838, 2.843, 2.897 / 2.823, 2.81, 2.842 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.7774 (0.7744-0.7808) | 0.7758 (0.7742-0.7785) | -0.2% | 0.7783, 0.7793, 0.7757 / 0.7748, 0.7779, 0.7752 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 15.91 (15.8-16.17) | 16.08 (15.77-16.26) | +1.1% | 15.98, 15.81, 16.05 / 16.11, 15.99, 16.01 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 8.675 (8.665-8.694) | 8.703 (8.681-8.731) | +0.3% | 8.682, 8.682, 8.667 / 8.711, 8.703, 8.7 | consistent, small |
| dense 30 x 784 bare downstream b32 / numpy | 57.98 (56.9-58.29) | 57.98 (57.53-58.29) | -0.0% | 58.19, 57.59, 57.42 / 57.98, 57.57, 58.21 | within noise |
| dense 30 x 784 bare downstream b32 / rust | 126.4 (125.5-127.7) | 126.7 (125.7-126.9) | +0.2% | 126.5, 127.1, 126.4 / 126.3, 126.8, 126.2 | within noise |
| dense 30 x 784 bare downstream b512 / numpy | 3011 (2736-4134) | 3201 (2758-3989) | +6.3% | 2995, 3539, 3078 / 3536, 2932, 3396 | within noise |
| dense 30 x 784 bare downstream b512 / rust | 2119 (1831-2667) | 2488 (2044-2581) | +17.4% | 2327, 2274, 1916 / 2488, 2371, 2313 | within noise |
| dense 30 x 784 bare accumulate b32 / numpy | 66.23 (65.46-66.6) | 66.84 (65.93-402.5) | +0.9% | 66.55, 66.23, 65.47 / 66.54, 234.5, 66.79 | within noise |
| dense 30 x 784 bare accumulate b32 / rust | 125.8 (124.7-126.9) | 124.8 (124.7-126.6) | -0.8% | 126.3, 126.4, 124.8 / 125.2, 124.7, 125.8 | within noise |
| dense 30 x 784 bare accumulate b512 / numpy | 1787 (1614-1986) | 1904 (1704-2085) | +6.5% | 1777, 1869, 1746 / 1944, 1774, 1983 | within noise |
| dense 30 x 784 bare accumulate b512 / rust | 2620 (2352-2764) | 2487 (2279-2588) | -5.0% | 2701, 2620, 2459 / 2437, 2354, 2567 | within noise |
| dense 30 x 784 transpose b32 / numpy | 1.404 (1.389-1.689) | 1.406 (1.399-1.415) | +0.2% | 1.408, 1.39, 1.545 / 1.405, 1.413, 1.402 | within noise |
| dense 30 x 784 transpose b32 / rust | 1.818 (1.814-1.823) | 1.818 (1.815-1.821) | -0.0% | 1.817, 1.82, 1.818 / 1.819, 1.817, 1.818 | within noise |
| dense 30 x 784 transpose b512 / numpy | 9.01 (8.97-9.063) | 9.005 (8.968-9.231) | -0.1% | 9.044, 8.989, 8.997 / 8.998, 8.996, 9.118 | within noise |
| dense 30 x 784 transpose b512 / rust | 24.89 (24.84-25.13) | 24.92 (24.91-25.31) | +0.1% | 25.1, 24.88, 24.86 / 24.91, 25, 25.11 | within noise |
| dense 30 x 784 add b32 / numpy | 10.34 (10.09-10.56) | 10.4 (10.14-10.56) | +0.6% | 10.28, 10.2, 10.46 / 10.37, 10.34, 10.48 | within noise |
| dense 30 x 784 add b32 / rust | 9.83 (9.561-11.62) | 10.4 (9.411-12.41) | +5.8% | 9.671, 9.732, 11.27 / 10.56, 10.34, 10.95 | within noise |
| dense 30 x 784 add b512 / numpy | 11.65 (11.52-12.07) | 11.42 (11.25-11.63) | -2.0% | 11.58, 11.6, 11.91 / 11.49, 11.42, 11.4 | separated, inside spread |
| dense 30 x 784 add b512 / rust | 9.582 (9.376-9.878) | 9.586 (9.421-9.73) | +0.0% | 9.508, 9.702, 9.632 / 9.558, 9.626, 9.575 | within noise |
| dense 30 x 784 sum_axis0 b32 / numpy | 2.816 (2.79-2.823) | 2.79 (2.779-2.816) | -0.9% | 2.812, 2.804, 2.822 / 2.784, 2.804, 2.797 | separated, inside spread |
| dense 30 x 784 sum_axis0 b32 / rust | 0.7031 (0.6992-0.7037) | 0.7023 (0.6972-0.7086) | -0.1% | 0.7014, 0.7034, 0.7031 / 0.7056, 0.7022, 0.6996 | within noise |
| dense 30 x 784 sum_axis0 b512 / numpy | 15.51 (15.3-15.65) | 15.37 (15.32-15.63) | -0.9% | 15.34, 15.64, 15.5 / 15.46, 15.35, 15.5 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 7.435 (7.43-7.443) | 7.422 (7.415-7.443) | -0.2% | 7.438, 7.435, 7.435 / 7.435, 7.418, 7.419 | within noise |
| dense 10 x 30 bare downstream b32 / numpy | 5.874 (5.863-5.913) | 5.882 (5.834-5.913) | +0.1% | 5.866, 5.888, 5.891 / 5.851, 5.904, 5.889 | within noise |
| dense 10 x 30 bare downstream b32 / rust | 3.182 (3.179-3.187) | 3.178 (3.174-3.182) | -0.1% | 3.18, 3.182, 3.184 / 3.18, 3.178, 3.177 | separated, inside spread |
| dense 10 x 30 bare downstream b512 / numpy | 64.6 (64.5-64.87) | 64.62 (64.47-64.78) | +0.0% | 64.64, 64.58, 64.69 / 64.53, 64.58, 64.71 | within noise |
| dense 10 x 30 bare downstream b512 / rust | 46.24 (46.06-46.26) | 46.16 (45.72-46.27) | -0.2% | 46.15, 46.24, 46.24 / 46.13, 46.25, 45.9 | within noise |
| dense 10 x 30 bare accumulate b32 / numpy | 5.057 (5.049-5.072) | 5.045 (5-5.089) | -0.2% | 5.061, 5.05, 5.066 / 5.044, 5.038, 5.06 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 2.877 (2.873-2.881) | 2.878 (2.875-2.881) | +0.0% | 2.877, 2.878, 2.877 / 2.878, 2.878, 2.877 | within noise |
| dense 10 x 30 bare accumulate b512 / numpy | 32.57 (32.5-32.82) | 32.62 (32.42-32.74) | +0.2% | 32.55, 32.56, 32.68 / 32.63, 32.58, 32.59 | within noise |
| dense 10 x 30 bare accumulate b512 / rust | 45.17 (45.13-45.21) | 45.08 (45.05-45.1) | -0.2% | 45.17, 45.2, 45.14 / 45.06, 45.09, 45.09 | separated, inside spread |
| dense 10 x 30 transpose b32 / numpy | 0.8916 (0.8856-0.9825) | 0.8921 (0.8849-0.9939) | +0.1% | 0.9353, 0.8922, 0.891 / 0.891, 0.8879, 0.9436 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.8023 (0.7952-0.813) | 0.7982 (0.7955-0.8066) | -0.5% | 0.8016, 0.8023, 0.8041 / 0.8021, 0.7972, 0.7985 | within noise |
| dense 10 x 30 transpose b512 / numpy | 3.382 (3.365-3.4) | 3.395 (3.363-3.589) | +0.4% | 3.386, 3.382, 3.383 / 3.544, 3.388, 3.377 | within noise |
| dense 10 x 30 transpose b512 / rust | 8.586 (8.582-8.591) | 8.586 (8.575-8.606) | +0.0% | 8.584, 8.584, 8.588 / 8.579, 8.591, 8.589 | within noise |
| dense 10 x 30 add b32 / numpy | 0.8942 (0.8911-0.8999) | 0.8917 (0.8868-0.8996) | -0.3% | 0.8942, 0.8976, 0.8923 / 0.8885, 0.8964, 0.8933 | within noise |
| dense 10 x 30 add b32 / rust | 0.3848 (0.3833-0.3876) | 0.3841 (0.3816-0.3891) | -0.2% | 0.3854, 0.3857, 0.3846 / 0.3856, 0.3857, 0.3822 | within noise |
| dense 10 x 30 add b512 / numpy | 0.9219 (0.9111-0.9436) | 0.9188 (0.9162-0.9338) | -0.3% | 0.9119, 0.9317, 0.9241 / 0.925, 0.9187, 0.9208 | within noise |
| dense 10 x 30 add b512 / rust | 0.4062 (0.4048-0.4091) | 0.4058 (0.4041-0.4196) | -0.1% | 0.4062, 0.4054, 0.4078 / 0.4067, 0.4124, 0.4049 | within noise |
| dense 10 x 30 sum_axis0 b32 / numpy | 2.468 (2.452-2.485) | 2.47 (2.449-2.48) | +0.1% | 2.483, 2.465, 2.457 / 2.46, 2.461, 2.476 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.5475 (0.5445-0.5505) | 0.5444 (0.5416-0.5504) | -0.6% | 0.5452, 0.5494, 0.5482 / 0.547, 0.5427, 0.546 | within noise |
| dense 10 x 30 sum_axis0 b512 / numpy | 12.18 (12.16-12.22) | 12.58 (12.16-12.65) | +3.3% | 12.18, 12.18, 12.19 / 12.62, 12.4, 12.38 | separated, inside spread |
| dense 10 x 30 sum_axis0 b512 / rust | 4.959 (4.95-4.961) | 4.96 (4.957-4.966) | +0.0% | 4.958, 4.961, 4.954 / 4.96, 4.96, 4.962 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 753.1 (745.4-1137) | 747.6 (745.2-759.9) | -0.7% | 942.6, 945.1, 745.9 / 753.4, 747, 752.3 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 829.5 (828.4-830.4) | 831.6 (830.7-833.7) | +0.3% | 829.7, 828.7, 829.9 / 832.2, 831.6, 832.6 | consistent, small |
| attention 16 x 32 forward_batch b512 / numpy | 2.414e+04 (2.212e+04-2.673e+04) | 2.383e+04 (2.225e+04-2.613e+04) | -1.3% | 2.571e+04, 2.336e+04, 2.435e+04 / 2.371e+04, 2.356e+04, 2.453e+04 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 1.755e+04 (1.619e+04-1.809e+04) | 1.749e+04 (1.673e+04-1.821e+04) | -0.3% | 1.769e+04, 1.776e+04, 1.653e+04 / 1.744e+04, 1.74e+04, 1.788e+04 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 769.8 (755-1008) | 758.8 (753.9-780.7) | -1.4% | 884.8, 766.8, 766.3 / 758.8, 758.3, 768.5 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / rust | 794 (790.6-798.3) | 797 (790.8-799.7) | +0.4% | 793.6, 793.3, 795.2 / 795.3, 797.7, 794.5 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 2.768e+04 (2.527e+04-3.557e+04) | 2.735e+04 (2.582e+04-2.834e+04) | -1.2% | 3.229e+04, 2.742e+04, 2.627e+04 / 2.708e+04, 2.624e+04, 2.82e+04 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / rust | 1.884e+04 (1.812e+04-2.263e+04) | 1.947e+04 (1.871e+04-2.111e+04) | +3.4% | 2.037e+04, 1.937e+04, 1.884e+04 / 2.052e+04, 1.982e+04, 1.886e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 584.5 (581.1-595.6) | 589.1 (586-2086) | +0.8% | 584.9, 590.5, 582.5 / 587.5, 1335, 1337 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 513.7 (505.7-516.3) | 509.9 (504.7-514.8) | -0.7% | 510.3, 512.3, 513.8 / 510.8, 505.2, 513.5 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 3.618e+04 (3.196e+04-4.286e+04) | 3.459e+04 (3.29e+04-4.202e+04) | -4.4% | 3.606e+04, 3.897e+04, 3.511e+04 / 3.807e+04, 3.398e+04, 3.617e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 2.049e+04 (2.017e+04-3.564e+04) | 2.879e+04 (2.248e+04-3.339e+04) | +40.5% | 2.804e+04, 2.097e+04, 2.033e+04 / 2.6e+04, 2.743e+04, 3.073e+04 | within noise |
