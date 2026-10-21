Old `69bf104` against new `69bf104`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `1f732ffd81e7`) on both sides. Machine check: profile: identity matches (raspberry-pi-5.json); passes peaked at 45.8-56.8 C; max 1-min load 1.02; busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / dense 30 x 784 hidden_delta_batch b512 / rust -14.6% (3588 -> 3065 µs)
- consistent, small: per call / conv 13x13x8, 8 ch downstream / rust -0.4% (33.54 -> 33.4 µs)
- 268 rows within noise (23 separated inside their spread), max |Δ| 283.4%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 78.8 (77.67-80.37) | 78.07 (77.52-80.31) | -0.9% | 78.8, 78.68, 79.12 / 78.98, 78.07, 78.9 | within noise |
| conv tail 32 x 5408 forward / rust | 76.21 (56.56-77.09) | 57.08 (55.03-57.68) | -25.1% | 74.61, 76.78, 66.83 / 57.21, 57.48, 55.16 | separated, inside spread |
| conv tail 32 x 5408 downstream / numpy | 92.22 (91.44-93.47) | 92.14 (92.05-92.41) | -0.1% | 92.33, 92.02, 92.85 / 92.14, 92.07, 92.35 | within noise |
| conv tail 32 x 5408 downstream / rust | 98.29 (74.2-104.6) | 76.76 (74.72-88.15) | -21.9% | 98.32, 96.39, 89.35 / 82.47, 76.77, 75.72 | separated, inside spread |
| conv tail 32 x 5408 hidden_delta / numpy | 105 (103.3-106.7) | 103.9 (102.7-105.8) | -1.1% | 104.9, 106, 104 / 104.3, 103.7, 104.7 | within noise |
| conv tail 32 x 5408 hidden_delta / rust | 87.41 (79.43-112.1) | 80.43 (79.07-111.7) | -8.0% | 86.99, 94.38, 97.14 / 95.38, 94.44, 80.43 | within noise |
| conv tail 32 x 5408 accumulate_gradient / numpy | 891.2 (421.3-1011) | 644.8 (431.1-995.7) | -27.7% | 716, 954.3, 665.7 / 716.1, 431.3, 919 | within noise |
| conv tail 32 x 5408 accumulate_gradient / rust | 96.32 (89.15-98.59) | 98.07 (88.39-100.7) | +1.8% | 93.68, 92.42, 98.18 / 94.53, 93.2, 98.52 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 1803 (1328-2313) | 1897 (1532-2018) | +5.2% | 2064, 1731, 1560 / 1722, 1984, 1863 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 509.8 (376.9-787.4) | 576.4 (413.1-804.4) | +13.1% | 509.8, 768.8, 379 / 449.5, 759.4, 576.4 | within noise |
| conv tail 32 x 5408 sgd step / numpy | 2354 (2261-2932) | 2818 (2264-2910) | +19.7% | 2896, 2354, 2270 / 2545, 2593, 2849 | within noise |
| conv tail 32 x 5408 sgd step / rust | 118.7 (115.4-277.5) | 119.8 (116.4-283.3) | +0.9% | 196.5, 118.7, 118.1 / 275.6, 118.2, 118.5 | within noise |
| conv tail 32 x 5408 forward_batch b32 / numpy | 542.8 (522.4-571) | 535 (520.4-579.8) | -1.5% | 552.4, 557.8, 524.2 / 550.1, 543.3, 528.3 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 1118 (1095-1134) | 1114 (1100-1128) | -0.3% | 1120, 1118, 1115 / 1114, 1114, 1112 | separated, inside spread |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1.874e+04 (1.696e+04-2.1e+04) | 1.924e+04 (1.679e+04-2.003e+04) | +2.7% | 2.046e+04, 1.881e+04, 1.704e+04 / 1.819e+04, 1.924e+04, 1.934e+04 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1.334e+04 (1.208e+04-1.356e+04) | 1.235e+04 (1.066e+04-1.341e+04) | -7.4% | 1.345e+04, 1.284e+04, 1.27e+04 / 1.285e+04, 1.131e+04, 1.222e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 1582 (1304-1715) | 1318 (1129-1638) | -16.7% | 1598, 1594, 1440 / 1569, 1239, 1208 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 1156 (1145-1640) | 1336 (1118-1620) | +15.5% | 1395, 1191, 1153 / 1539, 1213, 1291 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3.888e+04 (2.65e+04-5.04e+04) | 3.689e+04 (3.328e+04-4.615e+04) | -5.1% | 5.02e+04, 3.086e+04, 3.855e+04 / 4.073e+04, 3.819e+04, 3.588e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2.325e+04 (1.443e+04-2.524e+04) | 2.167e+04 (1.819e+04-2.381e+04) | -6.8% | 2.466e+04, 1.842e+04, 2.348e+04 / 2.192e+04, 1.999e+04, 2.257e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 3926 (3359-4334) | 3476 (2889-3704) | -11.4% | 3615, 4266, 3742 / 3476, 3352, 3297 | separated, inside spread |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 1867 (1643-2029) | 1954 (1510-2155) | +4.7% | 1980, 1837, 1702 / 1819, 1821, 2021 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 7.458e+04 (6.432e+04-8.559e+04) | 6.766e+04 (6.456e+04-7.604e+04) | -9.3% | 8.094e+04, 7.112e+04, 7.127e+04 / 7.397e+04, 6.725e+04, 6.55e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 3.24e+04 (2.502e+04-3.754e+04) | 2.958e+04 (2.543e+04-3.294e+04) | -8.7% | 3.515e+04, 2.853e+04, 3.255e+04 / 3.002e+04, 3.188e+04, 2.688e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 2199 (1705-2274) | 2244 (2088-2323) | +2.0% | 2262, 2199, 1784 / 2271, 2143, 2294 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 2230 (2040-2442) | 2183 (2081-2445) | -2.1% | 2280, 2190, 2240 / 2155, 2412, 2120 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 2.814e+04 (2.549e+04-3.038e+04) | 2.852e+04 (2.473e+04-3.079e+04) | +1.3% | 2.761e+04, 2.96e+04, 2.728e+04 / 2.844e+04, 2.702e+04, 2.867e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 2.013e+04 (1.927e+04-2.047e+04) | 1.961e+04 (1.893e+04-2.101e+04) | -2.6% | 2.005e+04, 1.987e+04, 2.013e+04 / 1.997e+04, 1.951e+04, 1.961e+04 | within noise |
| dense 30 x 784 forward / numpy | 16.23 (16.13-16.41) | 16.26 (16.02-16.43) | +0.2% | 16.23, 16.32, 16.19 / 16.13, 16.22, 16.35 | within noise |
| dense 30 x 784 forward / rust | 6.554 (6.424-6.6) | 6.529 (6.404-6.579) | -0.4% | 6.56, 6.554, 6.512 / 6.562, 6.485, 6.5 | within noise |
| dense 30 x 784 downstream / numpy | 12.73 (12.67-12.78) | 12.69 (12.65-12.74) | -0.3% | 12.68, 12.76, 12.73 / 12.72, 12.69, 12.69 | within noise |
| dense 30 x 784 downstream / rust | 6.516 (6.28-6.679) | 6.538 (6.47-6.657) | +0.3% | 6.48, 6.582, 6.507 / 6.608, 6.551, 6.488 | within noise |
| dense 30 x 784 hidden_delta / numpy | 17.07 (16.97-17.2) | 17 (16.95-17.1) | -0.4% | 17.12, 17.07, 17.03 / 17.01, 17.03, 16.99 | separated, inside spread |
| dense 30 x 784 hidden_delta / rust | 7.429 (7.161-7.563) | 7.505 (7.17-7.557) | +1.0% | 7.353, 7.376, 7.429 / 7.34, 7.537, 7.352 | within noise |
| dense 30 x 784 accumulate_gradient / numpy | 42.71 (42.62-42.82) | 42.81 (42.6-316.6) | +0.2% | 42.72, 42.72, 42.71 / 179.7, 42.7, 42.83 | within noise |
| dense 30 x 784 accumulate_gradient / rust | 9.835 (9.596-10.18) | 9.884 (9.725-9.908) | +0.5% | 9.984, 9.758, 9.762 / 9.806, 9.885, 9.892 | within noise |
| dense 30 x 784 apply_accumulated_gradient / numpy | 61.22 (61.14-61.33) | 61.15 (61.09-61.18) | -0.1% | 61.24, 61.19, 61.28 / 61.16, 61.15, 61.14 | separated, inside spread |
| dense 30 x 784 apply_accumulated_gradient / rust | 36.52 (36.48-36.56) | 36.57 (36.5-36.64) | +0.1% | 36.52, 36.51, 36.52 / 36.52, 36.6, 36.6 | within noise |
| dense 30 x 784 sgd step / numpy | 107.9 (107.8-108.1) | 108 (107.8-108.3) | +0.1% | 107.9, 107.9, 108 / 108.1, 108, 108 | within noise |
| dense 30 x 784 sgd step / rust | 15.7 (15.65-15.8) | 15.77 (15.66-15.8) | +0.4% | 15.7, 15.73, 15.7 / 15.72, 15.73, 15.78 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 454.3 (91.35-464.6) | 271.5 (92.01-454.1) | -40.2% | 271.8, 456.1, 458.7 / 92.28, 272.9, 452.3 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 118.4 (115.1-119.3) | 117.7 (115.1-119.2) | -0.6% | 118.6, 118.8, 115.3 / 118.7, 117.7, 115.2 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 2830 (2725-2985) | 2921 (2661-2965) | +3.2% | 2771, 2813, 2926 / 2777, 2868, 2953 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 1036 (1002-1152) | 1012 (967-1090) | -2.3% | 1014, 1030, 1136 / 1004, 1051, 1010 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 57.82 (56.77-57.99) | 221.7 (57.12-396.3) | +283.4% | 57.33, 57.63, 57.88 / 57.53, 390.7, 225.7 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 126.8 (126.5-128) | 126.8 (126.7-127.8) | +0.0% | 126.9, 126.7, 127.2 / 126.7, 126.8, 127.4 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 3867 (2914-4189) | 2948 (2456-3870) | -23.8% | 4185, 3012, 3867 / 2475, 3176, 3393 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 1949 (1710-2654) | 2408 (1880-2554) | +23.5% | 1766, 2327, 2249 / 2355, 2487, 2117 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 105.9 (104.9-292.6) | 105.9 (104.8-475.7) | +0.0% | 199.6, 105.4, 105.7 / 105.9, 104.8, 471.7 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / rust | 152.1 (148.1-157.8) | 156.1 (153.8-166.9) | +2.6% | 154.2, 153.6, 149.2 / 155.5, 162.1, 154.8 | separated, inside spread |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 9913 (9223-1.056e+04) | 8887 (8241-1.094e+04) | -10.4% | 1.007e+04, 1.009e+04, 9621 / 9593, 8887, 8758 | separated, inside spread |
| dense 30 x 784 hidden_delta_batch b512 / rust | 3588 (2973-4075) | 3065 (3002-3100) | -14.6% | 3524, 3420, 3588 / 3023, 3090, 3065 | consistent |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 264.4 (86.12-447.6) | 88.19 (87.08-452.7) | -66.6% | 86.99, 444.2, 265.9 / 270.4, 262.1, 87.63 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 139.4 (139-139.6) | 139.7 (139.3-140.2) | +0.2% | 139.2, 139.5, 139.4 / 140, 139.3, 139.8 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 2240 (1884-2346) | 2276 (2088-2337) | +1.6% | 2304, 2183, 2062 / 2212, 2296, 2243 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 2664 (2614-2716) | 2667 (2361-2822) | +0.1% | 2649, 2673, 2665 / 2717, 2592, 2647 | within noise |
| dense 10 x 30 forward / numpy | 8.163 (8.087-8.277) | 8.143 (8.104-8.306) | -0.2% | 8.182, 8.156, 8.201 / 8.237, 8.107, 8.144 | within noise |
| dense 10 x 30 forward / rust | 0.6411 (0.6333-0.7078) | 0.6355 (0.6339-0.6407) | -0.9% | 0.6345, 0.6806, 0.6411 / 0.6373, 0.6368, 0.6347 | within noise |
| dense 10 x 30 downstream / numpy | 1.822 (1.811-1.847) | 1.817 (1.797-1.832) | -0.3% | 1.834, 1.817, 1.824 / 1.805, 1.816, 1.826 | within noise |
| dense 10 x 30 downstream / rust | 0.4041 (0.3956-0.4131) | 0.4041 (0.4004-0.4111) | -0.0% | 0.4003, 0.409, 0.4024 / 0.4045, 0.4058, 0.4041 | within noise |
| dense 10 x 30 hidden_delta / numpy | 4.523 (4.479-4.535) | 4.542 (4.498-4.666) | +0.4% | 4.504, 4.528, 4.521 / 4.502, 4.595, 4.599 | within noise |
| dense 10 x 30 hidden_delta / rust | 0.8363 (0.8255-0.8462) | 0.8129 (0.8064-0.8185) | -2.8% | 0.8343, 0.843, 0.8293 / 0.8069, 0.8134, 0.8176 | separated, inside spread |
| dense 10 x 30 accumulate_gradient / numpy | 5.27 (5.231-5.398) | 5.262 (5.232-5.282) | -0.1% | 5.25, 5.26, 5.366 / 5.275, 5.261, 5.245 | within noise |
| dense 10 x 30 accumulate_gradient / rust | 0.7849 (0.7675-0.8003) | 0.7902 (0.7774-0.8218) | +0.7% | 0.7872, 0.7895, 0.7792 / 0.7835, 0.8076, 0.7849 | within noise |
| dense 10 x 30 apply_accumulated_gradient / numpy | 8.909 (8.859-9.139) | 8.944 (8.844-9.134) | +0.4% | 8.893, 9.015, 8.998 / 9.019, 9.004, 8.907 | within noise |
| dense 10 x 30 apply_accumulated_gradient / rust | 4.166 (4.147-4.206) | 4.171 (4.141-4.175) | +0.1% | 4.171, 4.159, 4.179 / 4.157, 4.175, 4.158 | within noise |
| dense 10 x 30 sgd step / numpy | 15.04 (15-15.12) | 15.12 (14.91-15.4) | +0.5% | 15.04, 15.06, 15.06 / 14.94, 15.36, 15.09 | within noise |
| dense 10 x 30 sgd step / rust | 0.9314 (0.9281-0.9424) | 0.9319 (0.9269-0.9394) | +0.1% | 0.936, 0.9325, 0.9307 / 0.9372, 0.9319, 0.9277 | within noise |
| dense 10 x 30 forward_batch b32 / numpy | 19.44 (19.36-19.59) | 19.47 (19.32-19.5) | +0.1% | 19.37, 19.5, 19.52 / 19.49, 19.45, 19.39 | within noise |
| dense 10 x 30 forward_batch b32 / rust | 7.226 (7.209-7.236) | 7.22 (7.193-7.231) | -0.1% | 7.231, 7.211, 7.226 / 7.206, 7.222, 7.222 | within noise |
| dense 10 x 30 forward_batch b512 / numpy | 151.7 (151.2-152) | 152.1 (151.6-152.5) | +0.3% | 151.4, 151.9, 151.7 / 152.1, 151.9, 152.2 | separated, inside spread |
| dense 10 x 30 forward_batch b512 / rust | 106.4 (106.2-106.5) | 106.3 (106.3-106.3) | -0.1% | 106.4, 106.2, 106.4 / 106.3, 106.3, 106.3 | within noise |
| dense 10 x 30 downstream_batch b32 / numpy | 5.922 (5.878-5.959) | 5.938 (5.903-5.947) | +0.3% | 5.933, 5.918, 5.914 / 5.944, 5.925, 5.92 | within noise |
| dense 10 x 30 downstream_batch b32 / rust | 4.303 (4.292-4.312) | 4.298 (4.297-4.31) | -0.1% | 4.307, 4.295, 4.304 / 4.304, 4.304, 4.298 | within noise |
| dense 10 x 30 downstream_batch b512 / numpy | 64.8 (64.43-64.97) | 64.8 (64.73-64.83) | -0.0% | 64.6, 64.78, 64.91 / 64.81, 64.76, 64.8 | within noise |
| dense 10 x 30 downstream_batch b512 / rust | 69.9 (69.8-70.09) | 69.91 (69.86-70.15) | +0.0% | 69.9, 69.85, 69.94 / 69.87, 70.03, 70 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 10.42 (10.38-10.51) | 10.43 (10.4-10.51) | +0.1% | 10.41, 10.47, 10.41 / 10.44, 10.42, 10.46 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 5.18 (5.165-5.19) | 5.177 (5.16-5.203) | -0.1% | 5.18, 5.184, 5.174 / 5.169, 5.191, 5.172 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 94.66 (93.96-95.21) | 93.29 (93.05-94.78) | -1.4% | 94.58, 95.11, 94.22 / 93.18, 93.55, 93.92 | separated, inside spread |
| dense 10 x 30 hidden_delta_batch b512 / rust | 78.85 (78.66-80.14) | 78.78 (78.61-79.25) | -0.1% | 78.99, 79.51, 78.74 / 78.88, 78.73, 78.93 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 9.627 (9.566-9.755) | 9.567 (9.555-9.809) | -0.6% | 9.661, 9.603, 9.65 / 9.56, 9.682, 9.607 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 4.574 (4.569-4.593) | 4.576 (4.57-4.587) | +0.0% | 4.579, 4.581, 4.571 / 4.572, 4.576, 4.583 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 47.98 (47.51-48.12) | 47.81 (47.57-48.52) | -0.4% | 47.98, 47.78, 48.02 / 48.14, 47.73, 47.83 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 58.93 (58.7-58.95) | 58.94 (58.75-59.05) | +0.0% | 58.82, 58.92, 58.94 / 58.97, 58.98, 58.85 | within noise |
| conv 28x28, 8 ch forward / numpy | 85.28 (85.08-86.46) | 85.79 (85.44-87.15) | +0.6% | 85.28, 85.97, 85.14 / 86.31, 86.34, 85.6 | within noise |
| conv 28x28, 8 ch forward / rust | 51.05 (51.04-51.15) | 51.07 (51.01-51.13) | +0.0% | 51.09, 51.05, 51.06 / 51.07, 51.07, 51.09 | within noise |
| conv 28x28, 8 ch downstream / numpy | 71.24 (71-72.57) | 71.25 (70.53-72.46) | +0.0% | 71.73, 71.13, 71.92 / 71.75, 71.23, 71.22 | within noise |
| conv 28x28, 8 ch downstream / rust | 48.28 (48.23-48.3) | 48.29 (48.28-48.37) | +0.0% | 48.28, 48.24, 48.29 / 48.33, 48.28, 48.31 | within noise |
| conv 28x28, 8 ch accumulate_gradient / numpy | 60.3 (57.83-61.66) | 58.15 (57.83-60.35) | -3.6% | 59.04, 61.2, 59.11 / 58.22, 59.09, 58.06 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 32.37 (32.35-32.39) | 32.39 (32.32-32.5) | +0.0% | 32.38, 32.36, 32.37 / 32.36, 32.39, 32.43 | within noise |
| conv 28x28, 8 ch forward_batch b32 / numpy | 4473 (4081-4798) | 4116 (3982-4781) | -8.0% | 4373, 4559, 4473 / 4116, 3988, 4676 | within noise |
| conv 28x28, 8 ch forward_batch b32 / rust | 1867 (1715-2210) | 1768 (1710-2019) | -5.3% | 1975, 1833, 1916 / 1768, 1864, 1781 | within noise |
| conv 28x28, 8 ch forward_batch b512 / numpy | 7.414e+04 (7.108e+04-7.778e+04) | 7.037e+04 (6.748e+04-7.731e+04) | -5.1% | 7.684e+04, 7.403e+04, 7.181e+04 / 7.126e+04, 7.312e+04, 6.891e+04 | within noise |
| conv 28x28, 8 ch forward_batch b512 / rust | 3.619e+04 (3.516e+04-3.927e+04) | 3.638e+04 (3.442e+04-3.828e+04) | +0.5% | 3.832e+04, 3.593e+04, 3.561e+04 / 3.561e+04, 3.602e+04, 3.727e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 1583 (1547-2032) | 1541 (1493-1576) | -2.7% | 1583, 1556, 1831 / 1535, 1541, 1528 | separated, inside spread |
| conv 28x28, 8 ch downstream_batch b32 / rust | 1489 (1488-1491) | 1489 (1489-1491) | +0.0% | 1489, 1489, 1491 / 1489, 1489, 1490 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 5.687e+04 (4.934e+04-5.97e+04) | 5.779e+04 (5.082e+04-6.004e+04) | +1.6% | 5.83e+04, 5.689e+04, 5.137e+04 / 5.432e+04, 5.891e+04, 5.689e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / rust | 9934 (9457-1.222e+04) | 1.104e+04 (9284-1.237e+04) | +11.1% | 1.087e+04, 1.102e+04, 9698 / 1.092e+04, 1.229e+04, 9839 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 2319 (2280-2320) | 2280 (2241-2351) | -1.7% | 2300, 2317, 2320 / 2302, 2263, 2293 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 1251 (1200-1266) | 1245 (1204-1572) | -0.4% | 1226, 1265, 1247 / 1222, 1402, 1403 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 3.776e+04 (3.706e+04-3.894e+04) | 3.721e+04 (3.706e+04-3.818e+04) | -1.4% | 3.791e+04, 3.803e+04, 3.776e+04 / 3.773e+04, 3.743e+04, 3.71e+04 | separated, inside spread |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 3.367e+04 (2.844e+04-4.007e+04) | 3.337e+04 (2.882e+04-3.399e+04) | -0.9% | 3.177e+04, 3.759e+04, 3.12e+04 / 3.348e+04, 3.14e+04, 3.152e+04 | within noise |
| conv 8x8, 8 ch forward / numpy | 34.87 (34.48-35.17) | 34.99 (34.45-35.62) | +0.3% | 34.79, 34.87, 34.87 / 35.31, 34.78, 34.8 | within noise |
| conv 8x8, 8 ch forward / rust | 3.664 (3.625-3.669) | 3.661 (3.651-3.67) | -0.1% | 3.658, 3.645, 3.665 / 3.666, 3.654, 3.661 | within noise |
| conv 8x8, 8 ch downstream / numpy | 39.68 (39.56-39.77) | 39.86 (39.65-40.21) | +0.4% | 39.69, 39.75, 39.58 / 39.74, 39.89, 40.06 | within noise |
| conv 8x8, 8 ch downstream / rust | 3.177 (3.164-3.179) | 3.171 (3.164-3.186) | -0.2% | 3.173, 3.172, 3.178 / 3.175, 3.168, 3.175 | within noise |
| conv 8x8, 8 ch accumulate_gradient / numpy | 12.51 (12.36-12.79) | 12.49 (12.38-12.79) | -0.1% | 12.51, 12.56, 12.58 / 12.45, 12.49, 12.61 | within noise |
| conv 8x8, 8 ch accumulate_gradient / rust | 2.488 (2.48-2.492) | 2.474 (2.468-2.503) | -0.6% | 2.482, 2.491, 2.486 / 2.47, 2.473, 2.499 | within noise |
| conv 8x8, 8 ch forward_batch b32 / numpy | 129.9 (128.2-130.5) | 130.3 (128.4-133.2) | +0.4% | 130.2, 129.8, 129 / 131.7, 128.8, 130.5 | within noise |
| conv 8x8, 8 ch forward_batch b32 / rust | 87.59 (87.48-87.86) | 87.51 (87.33-87.86) | -0.1% | 87.64, 87.67, 87.58 / 87.7, 87.53, 87.47 | within noise |
| conv 8x8, 8 ch forward_batch b512 / numpy | 4021 (3671-4271) | 3393 (3065-4182) | -15.6% | 4021, 3971, 4049 / 3387, 3167, 4069 | within noise |
| conv 8x8, 8 ch forward_batch b512 / rust | 1767 (1538-1903) | 1884 (1529-2047) | +6.7% | 1781, 1679, 1767 / 1982, 1787, 1788 | separated, inside spread |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 115.9 (115.4-117.6) | 115.9 (114.9-117.4) | -0.0% | 116.5, 115.9, 115.9 / 115.2, 116.3, 116.7 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / rust | 83.77 (83.69-84.53) | 84.28 (83.61-84.72) | +0.6% | 83.94, 83.75, 84.13 / 84.63, 84.3, 83.62 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 1955 (1623-2069) | 1793 (1591-2050) | -8.3% | 1761, 2049, 1821 / 1793, 1821, 1822 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / rust | 1337 (1334-1349) | 1337 (1332-1348) | +0.0% | 1341, 1344, 1334 / 1340, 1335, 1340 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 149.7 (148.1-155.1) | 150.9 (148-155.5) | +0.8% | 151.9, 150.6, 149.7 / 150.7, 152, 150.9 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 55.69 (55.64-55.77) | 55.78 (55.63-55.81) | +0.2% | 55.74, 55.65, 55.72 / 55.79, 55.71, 55.71 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 2333 (2283-2413) | 2354 (2293-2378) | +0.9% | 2334, 2332, 2352 / 2348, 2355, 2334 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 1039 (1013-1330) | 1307 (1029-1338) | +25.9% | 1162, 1031, 1180 / 1323, 1173, 1170 | within noise |
| conv 13x13x8, 8 ch forward / numpy | 80.28 (79.32-80.69) | 80.19 (79.63-105.3) | -0.1% | 80.5, 79.8, 80 / 80.04, 80.1, 92.7 | within noise |
| conv 13x13x8, 8 ch forward / rust | 51.49 (51.2-51.53) | 51.2 (51.14-51.49) | -0.6% | 51.34, 51.38, 51.51 / 51.17, 51.19, 51.38 | within noise |
| conv 13x13x8, 8 ch downstream / numpy | 89.01 (88.59-89.25) | 89.21 (88.73-90.21) | +0.2% | 88.8, 89.08, 89.13 / 89.47, 89.08, 89.21 | within noise |
| conv 13x13x8, 8 ch downstream / rust | 33.54 (33.52-33.67) | 33.4 (33.19-33.59) | -0.4% | 33.53, 33.61, 33.6 / 33.42, 33.42, 33.35 | consistent, small |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 40.53 (39.9-40.76) | 40.48 (40.06-40.8) | -0.1% | 40.27, 40.44, 40.53 / 40.1, 40.68, 40.53 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 16.39 (16.35-16.45) | 16.38 (16.34-16.44) | -0.1% | 16.39, 16.4, 16.4 / 16.38, 16.39, 16.39 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 2612 (2482-2655) | 2443 (2281-2788) | -6.5% | 2629, 2568, 2558 / 2560, 2385, 2575 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 2573 (2157-2636) | 2375 (2121-2611) | -7.7% | 2626, 2383, 2514 / 2443, 2326, 2322 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 5.088e+04 (4.782e+04-5.271e+04) | 5.175e+04 (4.979e+04-5.5e+04) | +1.7% | 5.138e+04, 5.091e+04, 4.976e+04 / 5.286e+04, 5.077e+04, 5.189e+04 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 5.305e+04 (5.164e+04-5.863e+04) | 5.438e+04 (5.24e+04-5.652e+04) | +2.5% | 5.537e+04, 5.305e+04, 5.269e+04 / 5.446e+04, 5.438e+04, 5.453e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 4159 (3966-4480) | 4265 (3991-4462) | +2.5% | 4159, 4242, 4165 / 4194, 4279, 4232 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 1016 (1010-1021) | 1015 (1014-1022) | -0.1% | 1014, 1019, 1014 / 1014, 1016, 1018 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 1.176e+05 (1.063e+05-1.232e+05) | 1.16e+05 (1.088e+05-1.232e+05) | -1.3% | 1.176e+05, 1.184e+05, 1.147e+05 / 1.184e+05, 1.141e+05, 1.146e+05 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 6678 (6335-8084) | 6430 (6273-6858) | -3.7% | 7449, 6378, 7302 / 6292, 6617, 6514 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 1134 (1123-1148) | 1134 (1126-1140) | -0.0% | 1126, 1137, 1138 / 1133, 1136, 1133 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 645.8 (632.1-648.9) | 644.7 (631.1-651.4) | -0.2% | 646, 645.8, 640.5 / 646.9, 640, 644.7 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.84e+04 (1.836e+04-1.848e+04) | 1.84e+04 (1.836e+04-1.847e+04) | -0.0% | 1.839e+04, 1.844e+04, 1.839e+04 / 1.839e+04, 1.843e+04, 1.838e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 1.368e+04 (1.177e+04-1.433e+04) | 1.291e+04 (1.174e+04-1.402e+04) | -5.7% | 1.33e+04, 1.39e+04, 1.267e+04 / 1.288e+04, 1.29e+04, 1.306e+04 | within noise |
| conv 26x26x8/2, 8 ch forward / numpy | 90.53 (90.06-91.82) | 90.28 (89.97-90.98) | -0.3% | 91.21, 90.57, 90.26 / 89.97, 90.52, 90.49 | within noise |
| conv 26x26x8/2, 8 ch forward / rust | 60.89 (60.83-61.28) | 61.1 (60.87-61.32) | +0.3% | 61.12, 60.89, 60.84 / 60.94, 61.06, 61.3 | within noise |
| conv 26x26x8/2, 8 ch downstream / numpy | 103.1 (102.7-104.9) | 103.4 (103-104.2) | +0.3% | 103.9, 102.9, 103.5 / 103.2, 103.7, 103.7 | within noise |
| conv 26x26x8/2, 8 ch downstream / rust | 40.17 (40.1-40.49) | 40.13 (39.64-40.26) | -0.1% | 40.33, 40.26, 40.11 / 39.89, 40.19, 39.96 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 47.89 (47.38-48.09) | 47.87 (47.62-48.22) | -0.0% | 47.89, 47.51, 48.02 / 47.89, 47.87, 47.92 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 19.36 (19.32-19.39) | 19.36 (19.34-19.39) | +0.0% | 19.36, 19.35, 19.37 / 19.36, 19.38, 19.35 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 3422 (3131-3788) | 3316 (3168-3587) | -3.1% | 3530, 3320, 3427 / 3384, 3408, 3244 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 3020 (2853-3236) | 2918 (2689-3316) | -3.4% | 3226, 2971, 2939 / 2772, 3097, 3099 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 6.655e+04 (6.29e+04-6.963e+04) | 6.54e+04 (6.43e+04-6.662e+04) | -1.7% | 6.805e+04, 6.608e+04, 6.477e+04 / 6.567e+04, 6.6e+04, 6.485e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 6.464e+04 (6.113e+04-6.939e+04) | 6.154e+04 (6.079e+04-6.639e+04) | -4.8% | 6.614e+04, 6.514e+04, 6.355e+04 / 6.379e+04, 6.203e+04, 6.115e+04 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 8906 (7556-1.016e+04) | 8922 (7700-1.017e+04) | +0.2% | 9914, 8906, 7573 / 8374, 9536, 8321 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 1245 (1243-1252) | 1238 (1231-1248) | -0.6% | 1247, 1245, 1248 / 1239, 1231, 1246 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 1.96e+05 (1.74e+05-2.058e+05) | 1.857e+05 (1.792e+05-2.016e+05) | -5.2% | 2.008e+05, 1.894e+05, 1.859e+05 / 1.904e+05, 1.906e+05, 1.847e+05 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 2.553e+04 (2.017e+04-3.074e+04) | 2.546e+04 (2.436e+04-2.898e+04) | -0.3% | 2.837e+04, 2.577e+04, 2.079e+04 / 2.562e+04, 2.672e+04, 2.54e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 1386 (1377-1403) | 1374 (1372-1390) | -0.9% | 1381, 1395, 1386 / 1373, 1374, 1387 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 830.2 (745.3-845.3) | 827 (748.2-841.9) | -0.4% | 830.2, 826.2, 795.3 / 792.7, 829.4, 806.2 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 2.238e+04 (2.221e+04-2.271e+04) | 2.234e+04 (2.209e+04-2.263e+04) | -0.2% | 2.235e+04, 2.265e+04, 2.227e+04 / 2.242e+04, 2.247e+04, 2.22e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 1.821e+04 (1.688e+04-1.854e+04) | 1.789e+04 (1.641e+04-1.844e+04) | -1.8% | 1.829e+04, 1.844e+04, 1.738e+04 / 1.789e+04, 1.742e+04, 1.739e+04 | within noise |
| conv 26x26x8, 8 ch forward / numpy | 245.4 (245-246) | 245.4 (243.9-246.2) | -0.0% | 245.7, 245.4, 245.3 / 245, 245, 245.5 | within noise |
| conv 26x26x8, 8 ch forward / rust | 237 (236.6-237.4) | 236.9 (236.8-248.9) | -0.1% | 237.3, 236.9, 236.9 / 236.9, 242.8, 237.2 | within noise |
| conv 26x26x8, 8 ch downstream / numpy | 254.9 (253.3-255.6) | 256.9 (254.6-259.1) | +0.8% | 255.3, 254.9, 254 / 258.7, 255.1, 257.1 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 153.5 (152.8-153.5) | 153.5 (152.1-154.5) | +0.0% | 153.4, 153.5, 153.2 / 153.9, 153.9, 152.8 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 160.3 (158.4-162.7) | 159.6 (158.6-162.7) | -0.5% | 158.9, 162, 160.3 / 159, 161.3, 160 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 72.38 (72.07-72.75) | 72.44 (72.24-72.5) | +0.1% | 72.23, 72.58, 72.28 / 72.39, 72.36, 72.48 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 1.411e+04 (1.216e+04-1.472e+04) | 1.459e+04 (1.269e+04-1.566e+04) | +3.4% | 1.344e+04, 1.465e+04, 1.352e+04 / 1.381e+04, 1.464e+04, 1.488e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 1.339e+04 (1.185e+04-1.421e+04) | 1.341e+04 (1.192e+04-1.403e+04) | +0.1% | 1.386e+04, 1.229e+04, 1.367e+04 / 1.377e+04, 1.284e+04, 1.277e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 2.436e+05 (2.408e+05-2.487e+05) | 2.548e+05 (2.43e+05-2.629e+05) | +4.6% | 2.436e+05, 2.434e+05, 2.453e+05 / 2.548e+05, 2.624e+05, 2.453e+05 | separated, inside spread |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 2.37e+05 (2.356e+05-2.511e+05) | 2.392e+05 (2.363e+05-2.435e+05) | +1.0% | 2.493e+05, 2.366e+05, 2.365e+05 / 2.412e+05, 2.414e+05, 2.368e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 2.507e+04 (2.462e+04-2.903e+04) | 2.662e+04 (2.493e+04-2.833e+04) | +6.2% | 2.695e+04, 2.507e+04, 2.552e+04 / 2.662e+04, 2.7e+04, 2.652e+04 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 4351 (3835-4751) | 3756 (2987-4655) | -13.7% | 4723, 4375, 3891 / 4110, 4143, 3217 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 5.111e+05 (4.907e+05-5.38e+05) | 5.187e+05 (4.795e+05-5.502e+05) | +1.5% | 5.263e+05, 5.012e+05, 5.083e+05 / 4.991e+05, 5.345e+05, 5.135e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 6.974e+04 (4.592e+04-8.29e+04) | 7.362e+04 (6.604e+04-8.167e+04) | +5.6% | 6.911e+04, 6.411e+04, 7.022e+04 / 7.048e+04, 7.333e+04, 7.699e+04 | separated, inside spread |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 5661 (5648-5703) | 5637 (5612-5685) | -0.4% | 5661, 5676, 5661 / 5637, 5665, 5622 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 3459 (3182-3766) | 3674 (3546-4007) | +6.2% | 3707, 3459, 3266 / 3697, 3639, 3813 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 8.893e+04 (8.843e+04-8.958e+04) | 8.888e+04 (8.857e+04-8.903e+04) | -0.1% | 8.922e+04, 8.89e+04, 8.884e+04 / 8.878e+04, 8.886e+04, 8.888e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 6.259e+04 (5.37e+04-6.74e+04) | 6.124e+04 (5.562e+04-6.732e+04) | -2.2% | 6.682e+04, 5.803e+04, 6.055e+04 / 6.643e+04, 5.987e+04, 5.754e+04 | within noise |
| pool 26x26, 8 ch forward / numpy | 105.6 (105.3-106) | 105.8 (105.2-113.9) | +0.2% | 105.4, 105.8, 105.6 / 109.8, 105.5, 105.7 | within noise |
| pool 26x26, 8 ch forward / rust | 5.238 (5.221-5.29) | 5.225 (5.21-5.297) | -0.2% | 5.24, 5.233, 5.255 / 5.218, 5.229, 5.259 | within noise |
| pool 26x26, 8 ch downstream / numpy | 55.18 (55.01-56.49) | 55.72 (55.15-56.79) | +1.0% | 55.03, 55.86, 55.57 / 55.59, 55.97, 55.78 | within noise |
| pool 26x26, 8 ch downstream / rust | 4.141 (4.129-4.145) | 4.145 (4.135-4.157) | +0.1% | 4.142, 4.137, 4.136 / 4.141, 4.15, 4.146 | within noise |
| pool 26x26, 8 ch forward_batch b32 / numpy | 2450 (2410-2480) | 2451 (2401-2482) | +0.0% | 2464, 2420, 2459 / 2442, 2428, 2458 | within noise |
| pool 26x26, 8 ch forward_batch b32 / rust | 226.7 (192.4-238.2) | 210.7 (195.1-241.1) | -7.0% | 235.2, 205.3, 221.7 / 220.8, 203.1, 210.7 | within noise |
| pool 26x26, 8 ch forward_batch b512 / numpy | 4.059e+04 (3.981e+04-4.136e+04) | 4.067e+04 (3.904e+04-4.142e+04) | +0.2% | 4.04e+04, 4.079e+04, 4.058e+04 / 3.983e+04, 4.114e+04, 4.005e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 9837 (7923-1.066e+04) | 8955 (8241-9697) | -9.0% | 9837, 1.048e+04, 8151 / 8859, 9207, 8881 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 969.3 (943.8-1471) | 975.6 (954.5-1571) | +0.6% | 971.1, 1227, 949.6 / 1263, 1216, 975.6 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / rust | 130.2 (129.8-474.8) | 471.7 (130-481.9) | +262.4% | 302.4, 129.9, 301.9 / 130.3, 474.8, 475.6 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 5.923e+04 (5.655e+04-6.427e+04) | 5.771e+04 (5.586e+04-6.276e+04) | -2.6% | 5.919e+04, 5.923e+04, 6.041e+04 / 5.854e+04, 5.766e+04, 5.931e+04 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / rust | 1.977e+04 (1.88e+04-2.144e+04) | 2.066e+04 (1.989e+04-2.223e+04) | +4.5% | 2.061e+04, 1.952e+04, 1.966e+04 / 2.145e+04, 2.119e+04, 2.027e+04 | within noise |
| pool 6x6, 8 ch forward / numpy | 39.7 (39.48-41.21) | 39.66 (39.49-40.99) | -0.1% | 39.7, 39.64, 40.4 / 40.24, 39.55, 40.1 | within noise |
| pool 6x6, 8 ch forward / rust | 0.7701 (0.767-0.7776) | 0.7718 (0.7678-0.7769) | +0.2% | 0.7701, 0.7734, 0.7721 / 0.7698, 0.7765, 0.7698 | within noise |
| pool 6x6, 8 ch downstream / numpy | 32.57 (32.24-32.67) | 32.54 (32.32-33.62) | -0.1% | 32.41, 32.62, 32.56 / 33.18, 32.42, 32.49 | within noise |
| pool 6x6, 8 ch downstream / rust | 0.6693 (0.659-0.6715) | 0.6677 (0.6603-0.6772) | -0.2% | 0.6693, 0.6606, 0.6705 / 0.667, 0.6721, 0.6646 | within noise |
| pool 6x6, 8 ch forward_batch b32 / numpy | 168.3 (167.5-169.7) | 168.5 (167.7-171.6) | +0.1% | 169.4, 167.6, 168.3 / 168, 169, 169.7 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 10.49 (10.45-10.56) | 10.46 (10.45-10.5) | -0.2% | 10.45, 10.51, 10.52 / 10.48, 10.45, 10.47 | within noise |
| pool 6x6, 8 ch forward_batch b512 / numpy | 2226 (2185-2484) | 2229 (2176-2269) | +0.1% | 2346, 2185, 2359 / 2222, 2219, 2229 | within noise |
| pool 6x6, 8 ch forward_batch b512 / rust | 163 (162.6-170.9) | 165.2 (162.5-170.1) | +1.4% | 166.9, 163, 162.8 / 169, 164.6, 163.2 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 85.23 (84.76-86.46) | 84.91 (84.67-85.57) | -0.4% | 85.23, 85.28, 85.64 / 84.91, 85.51, 84.74 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / rust | 7.85 (7.839-7.885) | 7.854 (7.846-7.877) | +0.1% | 7.862, 7.85, 7.861 / 7.846, 7.865, 7.856 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 940 (934.8-945.3) | 937.6 (933.3-940.3) | -0.2% | 938.1, 944.1, 936.9 / 935.5, 937, 940.2 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 129.1 (128.8-348) | 129.1 (129-129.1) | +0.0% | 231.1, 238.5, 128.9 / 129.1, 129, 129 | within noise |
| conv tail 32 x 5408 bare downstream b32 / numpy | 1500 (1136-1612) | 1211 (972.5-1655) | -19.3% | 1457, 1500, 1362 / 1305, 1503, 1051 | within noise |
| conv tail 32 x 5408 bare downstream b32 / rust | 1235 (1150-1662) | 1422 (1204-1677) | +15.2% | 1654, 1235, 1153 / 1442, 1650, 1213 | within noise |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3.045e+04 (2.318e+04-4.165e+04) | 4.415e+04 (2.757e+04-5.078e+04) | +45.0% | 3.447e+04, 2.459e+04, 3.43e+04 / 4.007e+04, 3.478e+04, 4.834e+04 | separated, inside spread |
| conv tail 32 x 5408 bare downstream b512 / rust | 1.784e+04 (1.335e+04-2.446e+04) | 2.601e+04 (2.368e+04-2.835e+04) | +45.8% | 2.359e+04, 1.564e+04, 1.763e+04 / 2.601e+04, 2.606e+04, 2.601e+04 | separated, inside spread |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 1256 (1110-1575) | 1536 (920.3-1586) | +22.3% | 1202, 1275, 1396 / 1539, 1450, 1237 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / rust | 1148 (1109-1221) | 1223 (1140-1367) | +6.5% | 1165, 1123, 1189 / 1313, 1221, 1180 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 2.803e+04 (2.513e+04-2.898e+04) | 2.695e+04 (2.318e+04-2.896e+04) | -3.9% | 2.827e+04, 2.713e+04, 2.693e+04 / 2.506e+04, 2.541e+04, 2.867e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / rust | 1.949e+04 (1.9e+04-2.018e+04) | 1.862e+04 (1.813e+04-1.96e+04) | -4.4% | 1.945e+04, 1.986e+04, 1.928e+04 / 1.924e+04, 1.844e+04, 1.845e+04 | separated, inside spread |
| conv tail 32 x 5408 transpose b32 / numpy | 1.462 (1.45-1.476) | 1.463 (1.449-1.473) | +0.0% | 1.456, 1.47, 1.459 / 1.464, 1.464, 1.459 | within noise |
| conv tail 32 x 5408 transpose b32 / rust | 1.877 (1.875-1.887) | 1.874 (1.872-1.885) | -0.2% | 1.877, 1.876, 1.883 / 1.879, 1.879, 1.873 | within noise |
| conv tail 32 x 5408 transpose b512 / numpy | 30.02 (29.61-30.08) | 29.92 (29.85-30.08) | -0.3% | 29.83, 30.02, 30.02 / 29.99, 29.97, 29.9 | within noise |
| conv tail 32 x 5408 transpose b512 / rust | 26.46 (26.39-26.72) | 26.5 (26.38-26.94) | +0.1% | 26.56, 26.51, 26.43 / 26.5, 26.67, 26.5 | within noise |
| conv tail 32 x 5408 add b32 / numpy | 319.8 (273.7-397.5) | 360.1 (285.4-422.7) | +12.6% | 335.6, 315.7, 345.6 / 358.6, 336.5, 360.1 | within noise |
| conv tail 32 x 5408 add b32 / rust | 378.5 (311-429.9) | 377.2 (306.4-473.2) | -0.4% | 338.5, 361.4, 414.9 / 348, 459.4, 349.5 | within noise |
| conv tail 32 x 5408 add b512 / numpy | 420.1 (310.5-426.4) | 333.7 (309.5-413.8) | -20.6% | 364.4, 422.9, 415.8 / 373.7, 322.5, 358.6 | within noise |
| conv tail 32 x 5408 add b512 / rust | 397.5 (303.1-465.8) | 374.3 (313.9-420) | -5.8% | 412.2, 370.6, 371.3 / 366.9, 414, 338.8 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 2.843 (2.823-2.898) | 2.834 (2.812-2.892) | -0.3% | 2.844, 2.842, 2.863 / 2.834, 2.852, 2.848 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.7812 (0.7807-0.7857) | 0.7859 (0.7802-0.7897) | +0.6% | 0.781, 0.7831, 0.7832 / 0.7877, 0.7807, 0.7873 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 16.06 (15.94-16.24) | 15.94 (15.8-16.15) | -0.8% | 16.17, 16.02, 16.03 / 15.98, 15.94, 15.94 | separated, inside spread |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 8.681 (8.667-8.835) | 8.677 (8.666-8.721) | -0.0% | 8.752, 8.683, 8.677 / 8.672, 8.683, 8.693 | within noise |
| dense 30 x 784 bare downstream b32 / numpy | 57.74 (57.6-399.8) | 57.79 (56.75-58.21) | +0.1% | 57.64, 228.9, 57.7 / 58.02, 56.76, 57.94 | within noise |
| dense 30 x 784 bare downstream b32 / rust | 127 (126.1-127.2) | 126.3 (125.7-127.1) | -0.5% | 126.6, 127.1, 126.8 / 126.4, 126.4, 126.3 | separated, inside spread |
| dense 30 x 784 bare downstream b512 / numpy | 3452 (2456-4023) | 3407 (2399-4163) | -1.3% | 3729, 2763, 3651 / 3510, 3011, 3631 | within noise |
| dense 30 x 784 bare downstream b512 / rust | 1985 (1594-2372) | 2073 (1575-2555) | +4.4% | 1912, 1983, 2057 / 1766, 2350, 2180 | within noise |
| dense 30 x 784 bare accumulate b32 / numpy | 66.52 (65.32-401.4) | 66.8 (65.89-401.6) | +0.4% | 65.42, 66.72, 234 / 233.9, 232.3, 66.49 | within noise |
| dense 30 x 784 bare accumulate b32 / rust | 125.7 (125.5-126.9) | 125.8 (124.8-126.8) | +0.1% | 125.7, 126.3, 125.7 / 125.8, 125.8, 125.3 | within noise |
| dense 30 x 784 bare accumulate b512 / numpy | 2082 (1888-2222) | 2100 (1880-2241) | +0.9% | 2124, 1995, 2063 / 2146, 2154, 1906 | within noise |
| dense 30 x 784 bare accumulate b512 / rust | 2677 (2532-2768) | 2596 (2446-2692) | -3.0% | 2747, 2580, 2650 / 2596, 2569, 2580 | within noise |
| dense 30 x 784 transpose b32 / numpy | 1.408 (1.393-1.419) | 1.399 (1.387-1.421) | -0.6% | 1.397, 1.416, 1.406 / 1.41, 1.393, 1.401 | within noise |
| dense 30 x 784 transpose b32 / rust | 1.821 (1.817-1.833) | 1.82 (1.816-1.825) | -0.1% | 1.82, 1.821, 1.825 / 1.822, 1.818, 1.82 | within noise |
| dense 30 x 784 transpose b512 / numpy | 9.013 (8.97-9.027) | 9.016 (8.972-9.051) | +0.0% | 9.013, 9.006, 8.993 / 8.988, 9.033, 9.024 | within noise |
| dense 30 x 784 transpose b512 / rust | 24.73 (24.68-24.81) | 24.74 (24.71-24.9) | +0.1% | 24.75, 24.73, 24.75 / 24.83, 24.72, 24.73 | within noise |
| dense 30 x 784 add b32 / numpy | 10.42 (9.996-10.73) | 10.31 (10.08-10.54) | -1.1% | 10.3, 10.42, 10.43 / 10.33, 10.35, 10.2 | within noise |
| dense 30 x 784 add b32 / rust | 9.665 (9.34-11.82) | 9.886 (9.582-11.84) | +2.3% | 9.783, 9.518, 10.71 / 10.71, 9.879, 9.945 | within noise |
| dense 30 x 784 add b512 / numpy | 11.67 (11-12.3) | 11.54 (11.15-11.84) | -1.1% | 11.39, 12.01, 11.33 / 11.44, 11.78, 11.29 | within noise |
| dense 30 x 784 add b512 / rust | 9.464 (9.304-9.815) | 9.554 (9.445-9.733) | +0.9% | 9.374, 9.464, 9.649 / 9.484, 9.589, 9.603 | within noise |
| dense 30 x 784 sum_axis0 b32 / numpy | 2.8 (2.795-2.806) | 2.802 (2.793-2.82) | +0.0% | 2.799, 2.804, 2.8 / 2.801, 2.814, 2.795 | within noise |
| dense 30 x 784 sum_axis0 b32 / rust | 0.7039 (0.7027-0.7092) | 0.7051 (0.7011-0.7067) | +0.2% | 0.703, 0.7065, 0.7063 / 0.7064, 0.7032, 0.7048 | within noise |
| dense 30 x 784 sum_axis0 b512 / numpy | 15.4 (15.32-15.99) | 15.41 (15.34-15.59) | +0.1% | 15.35, 15.42, 15.7 / 15.46, 15.41, 15.4 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 7.439 (7.436-7.453) | 7.434 (7.419-7.457) | -0.1% | 7.439, 7.445, 7.44 / 7.449, 7.435, 7.423 | within noise |
| dense 10 x 30 bare downstream b32 / numpy | 5.866 (5.835-5.88) | 5.872 (5.834-5.907) | +0.1% | 5.86, 5.852, 5.875 / 5.874, 5.892, 5.847 | within noise |
| dense 10 x 30 bare downstream b32 / rust | 4.253 (4.251-4.255) | 4.254 (4.253-4.259) | +0.0% | 4.253, 4.252, 4.254 / 4.253, 4.257, 4.253 | within noise |
| dense 10 x 30 bare downstream b512 / numpy | 64.73 (64.48-64.89) | 64.75 (64.53-64.88) | +0.0% | 64.61, 64.79, 64.81 / 64.75, 64.57, 64.84 | within noise |
| dense 10 x 30 bare downstream b512 / rust | 69.87 (69.81-70.13) | 69.85 (69.78-70.02) | -0.0% | 69.85, 69.98, 69.93 / 69.94, 69.92, 69.8 | within noise |
| dense 10 x 30 bare accumulate b32 / numpy | 5.029 (5.008-5.072) | 5.044 (5.008-5.07) | +0.3% | 5.051, 5.038, 5.017 / 5.044, 5.047, 5.032 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 3.261 (3.26-3.263) | 3.26 (3.256-3.263) | -0.0% | 3.26, 3.261, 3.262 / 3.257, 3.262, 3.261 | within noise |
| dense 10 x 30 bare accumulate b512 / numpy | 32.7 (32.57-32.9) | 32.56 (32.48-32.74) | -0.4% | 32.75, 32.84, 32.58 / 32.64, 32.51, 32.64 | within noise |
| dense 10 x 30 bare accumulate b512 / rust | 45.34 (45.3-45.38) | 45.39 (45.38-45.44) | +0.1% | 45.32, 45.35, 45.36 / 45.38, 45.41, 45.41 | separated, inside spread |
| dense 10 x 30 transpose b32 / numpy | 0.891 (0.8844-0.8976) | 0.8933 (0.8833-0.9016) | +0.3% | 0.8853, 0.8921, 0.8951 / 0.892, 0.894, 0.8925 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.8039 (0.7936-0.8108) | 0.806 (0.7937-0.8103) | +0.3% | 0.8071, 0.8057, 0.7991 / 0.8067, 0.798, 0.8083 | within noise |
| dense 10 x 30 transpose b512 / numpy | 3.387 (3.374-3.516) | 3.409 (3.39-3.501) | +0.6% | 3.38, 3.445, 3.397 / 3.445, 3.407, 3.411 | within noise |
| dense 10 x 30 transpose b512 / rust | 8.582 (8.505-8.591) | 8.578 (8.518-8.598) | -0.0% | 8.586, 8.513, 8.584 / 8.571, 8.596, 8.549 | within noise |
| dense 10 x 30 add b32 / numpy | 0.8994 (0.8979-0.9142) | 0.8968 (0.8892-0.9128) | -0.3% | 0.899, 0.906, 0.901 / 0.8996, 0.8893, 0.9039 | within noise |
| dense 10 x 30 add b32 / rust | 0.3763 (0.3758-0.38) | 0.3758 (0.3743-0.3781) | -0.1% | 0.3779, 0.3779, 0.376 / 0.3769, 0.3768, 0.3749 | within noise |
| dense 10 x 30 add b512 / numpy | 0.919 (0.9115-0.9425) | 0.9189 (0.9157-0.9332) | -0.0% | 0.9223, 0.919, 0.927 / 0.9232, 0.9245, 0.9189 | within noise |
| dense 10 x 30 add b512 / rust | 0.3991 (0.3976-0.4034) | 0.3977 (0.3946-0.4023) | -0.3% | 0.4018, 0.3978, 0.3997 / 0.3982, 0.3961, 0.3997 | within noise |
| dense 10 x 30 sum_axis0 b32 / numpy | 2.459 (2.448-2.488) | 2.458 (2.448-2.494) | -0.0% | 2.455, 2.474, 2.454 / 2.458, 2.471, 2.466 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.5332 (0.5316-0.5406) | 0.5344 (0.5279-0.5378) | +0.2% | 0.5324, 0.5325, 0.54 / 0.5308, 0.5364, 0.5343 | within noise |
| dense 10 x 30 sum_axis0 b512 / numpy | 12.19 (12.15-12.59) | 12.21 (12.15-12.61) | +0.2% | 12.59, 12.17, 12.18 / 12.39, 12.23, 12.17 | within noise |
| dense 10 x 30 sum_axis0 b512 / rust | 4.656 (4.652-4.667) | 4.651 (4.647-4.659) | -0.1% | 4.662, 4.653, 4.656 / 4.648, 4.656, 4.652 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 747.2 (745.5-751.4) | 748.3 (747.1-1150) | +0.2% | 749.1, 746, 747.4 / 858.9, 948.8, 747.9 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 805.6 (803.8-809.3) | 807.7 (802.2-810.1) | +0.3% | 805.5, 806.2, 806.8 / 805.8, 808.3, 807.7 | within noise |
| attention 16 x 32 forward_batch b512 / numpy | 2.452e+04 (2.365e+04-2.826e+04) | 2.518e+04 (2.319e+04-2.684e+04) | +2.7% | 2.454e+04, 2.595e+04, 2.443e+04 / 2.679e+04, 2.518e+04, 2.35e+04 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 1.763e+04 (1.675e+04-1.787e+04) | 1.701e+04 (1.625e+04-1.826e+04) | -3.5% | 1.78e+04, 1.732e+04, 1.714e+04 / 1.7e+04, 1.791e+04, 1.66e+04 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 760.4 (753.3-784.8) | 772 (758.6-781.8) | +1.5% | 772.2, 760.4, 761.6 / 774.5, 768.3, 767.6 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / rust | 792.9 (789.8-796.3) | 793.2 (790.1-796.8) | +0.0% | 795.5, 793.1, 789.9 / 793.2, 793.6, 792.4 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 3.026e+04 (2.575e+04-3.22e+04) | 2.944e+04 (2.77e+04-3.276e+04) | -2.7% | 3.067e+04, 2.766e+04, 3.114e+04 / 3.026e+04, 3.076e+04, 2.857e+04 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / rust | 2.033e+04 (1.932e+04-2.274e+04) | 2.04e+04 (1.996e+04-2.205e+04) | +0.4% | 2.123e+04, 2.033e+04, 2.011e+04 / 2.025e+04, 2.101e+04, 2.094e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 588.1 (585.3-590.4) | 590.4 (586.4-594.8) | +0.4% | 587.1, 588.8, 587.9 / 589.6, 589.3, 593 | separated, inside spread |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 512.6 (509.5-514.1) | 513.1 (508.7-515.1) | +0.1% | 509.6, 513.6, 512.7 / 513.5, 513.6, 511 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 3.638e+04 (3.358e+04-4.516e+04) | 4.144e+04 (3.368e+04-4.489e+04) | +13.9% | 4.019e+04, 3.456e+04, 4.028e+04 / 4.261e+04, 3.999e+04, 3.886e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 2.996e+04 (2.07e+04-3.799e+04) | 2.995e+04 (2.032e+04-3.368e+04) | -0.0% | 3.565e+04, 2.442e+04, 2.814e+04 / 2.632e+04, 3.063e+04, 2.778e+04 | within noise |
