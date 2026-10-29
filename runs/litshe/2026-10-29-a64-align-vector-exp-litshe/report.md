Old `6dcd34c` against new `6dcd34c`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `0517dc2` (extension sha256 `6fc32a9e1378`) and new crate `e7a0cdd` (extension sha256 `e983c73d9b77`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (raspberry-pi-5.json); passes peaked at 57.3-58.4 C; max 1-min load 1.12 (measured just after this run's crate builds); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / dense 30 x 784 hidden_delta_batch b32 / rust -34.6% (228.8 -> 149.6 µs)
- consistent: per call / conv tail 32 x 5408 downstream_batch b32 / rust -14.0% (1435 -> 1233 µs)
- consistent: per call / dense 10 x 30 forward_batch b512 / rust -12.7% (111.6 -> 97.43 µs)
- consistent: per call / dense 10 x 30 forward_batch b32 / rust -12.2% (7.529 -> 6.609 µs)
- consistent: per call / dense 10 x 30 forward / rust -4.7% (0.6309 -> 0.6009 µs)
- consistent: per call / attention 16 x 32 forward_batch b32 / rust -2.6% (793.8 -> 773.3 µs)
- consistent: per call / dense 10 x 30 downstream / rust +2.3% (0.3944 -> 0.4035 µs)
- consistent: per call / conv 28x28, 8 ch downstream_batch b32 / rust -2.2% (1501 -> 1468 µs)
- consistent: per call / conv 28x28, 8 ch downstream / rust -2.2% (48.69 -> 47.61 µs)
- consistent: per call / dense 30 x 784 forward_batch b32 / rust -2.2% (117.1 -> 114.5 µs)
- consistent, small: per call / attention 16 x 32 hidden_delta_batch b32 / rust -0.2% (766.3 -> 764.9 µs)
- 259 rows within noise (39 separated inside their spread), max |Δ| 385.8%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 77.92 (77.08-79.44) | 79.18 (76.85-83.72) | +1.6% | 77.78, 78.79, 77.61 / 79.46, 80.52, 78.39 | within noise |
| conv tail 32 x 5408 forward / rust | 57.39 (55.05-76.92) | 64.61 (53.81-75.7) | +12.6% | 56.04, 66.99, 67.3 / 64.76, 74.06, 55.38 | within noise |
| conv tail 32 x 5408 downstream / numpy | 92.05 (91.37-92.52) | 92.45 (91.98-93.16) | +0.4% | 92.32, 92.22, 91.54 / 91.99, 92.64, 92.86 | within noise |
| conv tail 32 x 5408 downstream / rust | 92.41 (74.9-106.2) | 90.14 (78.16-106.5) | -2.5% | 105.4, 92.41, 75.94 / 88.25, 99.25, 85.23 | within noise |
| conv tail 32 x 5408 hidden_delta / numpy | 105.1 (104.5-105.8) | 103.9 (103.1-106.2) | -1.2% | 104.9, 104.9, 105.5 / 104.7, 104.6, 103.9 | separated, inside spread |
| conv tail 32 x 5408 hidden_delta / rust | 95.5 (78.7-110.9) | 82.83 (78.59-93.6) | -13.3% | 88.13, 88.34, 110 / 82.34, 93.54, 80.37 | within noise |
| conv tail 32 x 5408 accumulate_gradient / numpy | 333.5 (280.6-834.8) | 786.8 (306.7-882.2) | +135.9% | 584.7, 521.7, 327.4 / 803.6, 849.7, 325.2 | within noise |
| conv tail 32 x 5408 accumulate_gradient / rust | 99.38 (95.94-99.94) | 95.31 (88.92-98) | -4.1% | 97.69, 99.13, 99.45 / 96.61, 96.47, 89.54 | separated, inside spread |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 1574 (1380-1989) | 1515 (1298-1622) | -3.7% | 1779, 1560, 1488 / 1563, 1430, 1495 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 563.3 (375.7-725.4) | 647.4 (378-766.5) | +14.9% | 631.7, 383.1, 613.4 / 641.2, 513.6, 715.8 | within noise |
| conv tail 32 x 5408 sgd step / numpy | 2449 (1866-2484) | 2019 (1857-2427) | -17.6% | 2400, 2175, 2455 / 2019, 2036, 2142 | separated, inside spread |
| conv tail 32 x 5408 sgd step / rust | 118.5 (115.1-269.2) | 116.3 (115.5-272.2) | -1.9% | 115.6, 121.1, 192.7 / 118.4, 115.8, 194.1 | within noise |
| conv tail 32 x 5408 forward_batch b32 / numpy | 517.5 (505.1-540) | 512.6 (505.6-537.7) | -0.9% | 528.9, 515.4, 518.2 / 514.5, 511.9, 523.1 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 1107 (1096-1122) | 1116 (1084-1121) | +0.8% | 1120, 1101, 1103 / 1117, 1120, 1091 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1.428e+04 (1.382e+04-1.647e+04) | 1.538e+04 (1.46e+04-1.741e+04) | +7.7% | 1.547e+04, 1.511e+04, 1.391e+04 / 1.493e+04, 1.667e+04, 1.517e+04 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1.172e+04 (1.084e+04-1.333e+04) | 1.032e+04 (9365-1.308e+04) | -11.9% | 1.273e+04, 1.183e+04, 1.108e+04 / 1.274e+04, 1.001e+04, 9909 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 1391 (1249-1601) | 1283 (993.2-1582) | -7.7% | 1312, 1510, 1391 / 1164, 1219, 1497 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 1435 (1146-1644) | 1233 (1154-1386) | -14.0% | 1388, 1415, 1435 / 1191, 1283, 1287 | consistent |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3.519e+04 (2.509e+04-3.777e+04) | 3.557e+04 (2.229e+04-4.476e+04) | +1.1% | 3.504e+04, 3.143e+04, 3.538e+04 / 4.278e+04, 3.557e+04, 2.611e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2.159e+04 (1.717e+04-2.63e+04) | 2.205e+04 (2.031e+04-2.548e+04) | +2.1% | 2.087e+04, 2.087e+04, 2.311e+04 / 2.19e+04, 2.103e+04, 2.544e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 3493 (3190-3995) | 3321 (3037-4060) | -4.9% | 3828, 3316, 3534 / 3874, 3266, 3134 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 1827 (1510-2119) | 1914 (1614-2207) | +4.7% | 1815, 2084, 1566 / 1910, 1914, 1891 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 6.685e+04 (6.338e+04-7.365e+04) | 6.827e+04 (6.544e+04-7.675e+04) | +2.1% | 6.934e+04, 6.941e+04, 6.463e+04 / 7.027e+04, 7.333e+04, 6.625e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 2.918e+04 (2.24e+04-3.605e+04) | 2.902e+04 (2.709e+04-3.484e+04) | -0.6% | 3.066e+04, 3.209e+04, 2.467e+04 / 3.132e+04, 2.995e+04, 2.866e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 1844 (1541-1964) | 1856 (1427-2197) | +0.6% | 1677, 1920, 1807 / 1639, 1874, 2029 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 2170 (2085-2370) | 2149 (2102-2390) | -1.0% | 2364, 2145, 2127 / 2197, 2110, 2262 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 2.346e+04 (1.951e+04-2.474e+04) | 2.099e+04 (1.937e+04-2.412e+04) | -10.5% | 2.409e+04, 2.17e+04, 2.331e+04 / 2.216e+04, 2.175e+04, 2.099e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 1.925e+04 (1.856e+04-1.957e+04) | 1.912e+04 (1.863e+04-2.103e+04) | -0.7% | 1.943e+04, 1.935e+04, 1.862e+04 / 2.082e+04, 1.886e+04, 1.895e+04 | within noise |
| dense 30 x 784 forward / numpy | 16.18 (16.08-16.37) | 16.3 (16.04-16.39) | +0.8% | 16.15, 16.28, 16.16 / 16.38, 16.18, 16.23 | within noise |
| dense 30 x 784 forward / rust | 6.426 (6.405-6.464) | 6.402 (6.334-6.502) | -0.4% | 6.411, 6.438, 6.441 / 6.395, 6.418, 6.402 | within noise |
| dense 30 x 784 downstream / numpy | 12.69 (12.65-12.71) | 12.69 (12.65-12.81) | -0.0% | 12.66, 12.69, 12.7 / 12.74, 12.72, 12.68 | within noise |
| dense 30 x 784 downstream / rust | 6.588 (6.534-6.701) | 6.481 (6.312-6.676) | -1.6% | 6.666, 6.551, 6.587 / 6.318, 6.51, 6.636 | within noise |
| dense 30 x 784 hidden_delta / numpy | 17.03 (16.96-17.2) | 17.06 (17.02-17.25) | +0.2% | 16.97, 17.13, 17.04 / 17.16, 17.04, 17.1 | within noise |
| dense 30 x 784 hidden_delta / rust | 7.227 (7.198-7.533) | 7.323 (7.19-7.513) | +1.3% | 7.206, 7.225, 7.532 / 7.312, 7.21, 7.512 | within noise |
| dense 30 x 784 accumulate_gradient / numpy | 42.73 (42.63-42.99) | 42.68 (42.61-42.79) | -0.1% | 42.76, 42.81, 42.7 / 42.67, 42.73, 42.65 | within noise |
| dense 30 x 784 accumulate_gradient / rust | 9.887 (9.785-9.922) | 9.929 (9.762-9.959) | +0.4% | 9.882, 9.896, 9.834 / 9.873, 9.947, 9.846 | within noise |
| dense 30 x 784 apply_accumulated_gradient / numpy | 61.21 (61.08-61.49) | 61.18 (61.05-61.42) | -0.0% | 61.34, 61.23, 61.14 / 61.19, 61.13, 61.29 | within noise |
| dense 30 x 784 apply_accumulated_gradient / rust | 36.25 (36.15-37.01) | 36.6 (36.32-36.79) | +1.0% | 36.58, 36.36, 36.2 / 36.6, 36.72, 36.4 | within noise |
| dense 30 x 784 sgd step / numpy | 107.9 (107.7-108) | 108.1 (107.9-108.5) | +0.2% | 107.9, 107.8, 108 / 108.1, 108.2, 108 | separated, inside spread |
| dense 30 x 784 sgd step / rust | 15.7 (15.64-15.71) | 15.72 (15.68-15.76) | +0.1% | 15.69, 15.7, 15.67 / 15.76, 15.7, 15.7 | separated, inside spread |
| dense 30 x 784 forward_batch b32 / numpy | 92.7 (91.13-459.6) | 450.3 (91.17-467) | +385.8% | 275.4, 273, 92.7 / 451.5, 279.1, 273.1 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 117.1 (115.2-119.4) | 114.5 (112.4-116.7) | -2.2% | 117.3, 117.4, 117.1 / 114.4, 114.4, 114.7 | consistent |
| dense 30 x 784 forward_batch b512 / numpy | 2044 (1902-2277) | 2105 (2045-2277) | +3.0% | 2014, 2044, 2089 / 2174, 2139, 2085 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 967.2 (943-1083) | 909.2 (895-1021) | -6.0% | 945.8, 1027, 1004 / 897.5, 909.2, 975 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 58.24 (56.8-398.2) | 223.8 (58.26-413.3) | +284.4% | 57.58, 227.9, 222.7 / 228.9, 58.37, 401.3 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 127.3 (126.8-128.4) | 127 (127-128.3) | -0.2% | 127.3, 127.6, 127.2 / 127, 127, 127.7 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 2678 (2392-4065) | 3369 (2808-4057) | +25.8% | 2886, 3311, 2595 / 3414, 3072, 3730 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 1846 (1585-2508) | 2211 (1839-2479) | +19.8% | 1680, 2234, 1987 / 2219, 2114, 2248 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 105.1 (104.7-106.4) | 105.4 (103.9-106) | +0.2% | 105.1, 104.8, 106.1 / 104.8, 104.8, 105.7 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / rust | 228.8 (153.4-301.2) | 149.6 (145.7-165.4) | -34.6% | 228.8, 226.8, 227.8 / 147.9, 155.7, 149.8 | consistent |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 8727 (8291-9815) | 9582 (7844-1.142e+04) | +9.8% | 9217, 8711, 8906 / 1.098e+04, 7990, 9582 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / rust | 3243 (2851-3847) | 3191 (2799-3825) | -1.6% | 3523, 3119, 3243 / 3735, 2900, 3133 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 435.3 (86.86-446.7) | 264.1 (86.17-444.6) | -39.3% | 87.3, 435.3, 446.3 / 442.6, 86.4, 265.4 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 139 (138.1-140.8) | 138.9 (138.7-139.8) | -0.1% | 139.3, 138.5, 139.8 / 139.3, 138.8, 139 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 1846 (1628-2039) | 1774 (1709-1979) | -3.9% | 1908, 1890, 1719 / 1829, 1731, 1887 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 2614 (1990-2652) | 2137 (2038-2633) | -18.2% | 2627, 2525, 2321 / 2128, 2611, 2088 | within noise |
| dense 10 x 30 forward / numpy | 8.133 (8.123-8.255) | 8.125 (8.072-8.185) | -0.1% | 8.139, 8.13, 8.189 / 8.125, 8.129, 8.125 | separated, inside spread |
| dense 10 x 30 forward / rust | 0.6309 (0.6285-0.6402) | 0.6009 (0.5976-0.6133) | -4.7% | 0.6343, 0.6296, 0.6359 / 0.6009, 0.6054, 0.6041 | consistent |
| dense 10 x 30 downstream / numpy | 1.821 (1.801-1.847) | 1.812 (1.79-1.826) | -0.5% | 1.814, 1.825, 1.824 / 1.808, 1.813, 1.808 | separated, inside spread |
| dense 10 x 30 downstream / rust | 0.3944 (0.3929-0.3984) | 0.4035 (0.3993-0.4052) | +2.3% | 0.3973, 0.3941, 0.3937 / 0.4018, 0.4022, 0.404 | consistent |
| dense 10 x 30 hidden_delta / numpy | 4.503 (4.488-4.569) | 4.539 (4.524-4.564) | +0.8% | 4.53, 4.52, 4.5 / 4.525, 4.55, 4.549 | within noise |
| dense 10 x 30 hidden_delta / rust | 0.8115 (0.8044-0.8212) | 0.8073 (0.7969-0.8354) | -0.5% | 0.8137, 0.8054, 0.8158 / 0.8016, 0.8072, 0.8276 | within noise |
| dense 10 x 30 accumulate_gradient / numpy | 5.268 (5.258-5.294) | 5.263 (5.173-5.319) | -0.1% | 5.281, 5.272, 5.259 / 5.264, 5.216, 5.293 | within noise |
| dense 10 x 30 accumulate_gradient / rust | 0.7763 (0.7699-0.8659) | 0.7613 (0.7584-0.7727) | -1.9% | 0.8211, 0.7731, 0.7749 / 0.7609, 0.7683, 0.76 | separated, inside spread |
| dense 10 x 30 apply_accumulated_gradient / numpy | 8.92 (8.898-8.957) | 8.886 (8.812-8.901) | -0.4% | 8.918, 8.916, 8.938 / 8.893, 8.889, 8.847 | separated, inside spread |
| dense 10 x 30 apply_accumulated_gradient / rust | 4.031 (4.004-4.045) | 4.113 (4.017-4.13) | +2.0% | 4.031, 4.035, 4.024 / 4.074, 4.126, 4.1 | separated, inside spread |
| dense 10 x 30 sgd step / numpy | 15.05 (14.92-15.49) | 15.02 (14.82-15.06) | -0.2% | 15.25, 15.2, 14.95 / 14.92, 14.99, 15.03 | within noise |
| dense 10 x 30 sgd step / rust | 0.9331 (0.9289-0.9411) | 0.9366 (0.9347-0.9482) | +0.4% | 0.9366, 0.932, 0.9321 / 0.9375, 0.9358, 0.9414 | within noise |
| dense 10 x 30 forward_batch b32 / numpy | 19.51 (19.32-19.58) | 19.46 (19.35-19.5) | -0.3% | 19.33, 19.54, 19.54 / 19.4, 19.46, 19.47 | within noise |
| dense 10 x 30 forward_batch b32 / rust | 7.529 (7.493-7.54) | 6.609 (6.585-6.636) | -12.2% | 7.516, 7.536, 7.519 / 6.599, 6.596, 6.631 | consistent |
| dense 10 x 30 forward_batch b512 / numpy | 151.7 (150.7-152.1) | 151.7 (151.3-153.1) | +0.0% | 151.7, 151.7, 151.4 / 152.4, 151.5, 151.7 | within noise |
| dense 10 x 30 forward_batch b512 / rust | 111.6 (111.6-111.7) | 97.43 (97.35-97.5) | -12.7% | 111.7, 111.6, 111.6 / 97.41, 97.43, 97.43 | consistent |
| dense 10 x 30 downstream_batch b32 / numpy | 5.937 (5.905-6.015) | 5.941 (5.921-5.962) | +0.1% | 5.931, 5.92, 5.977 / 5.958, 5.941, 5.924 | within noise |
| dense 10 x 30 downstream_batch b32 / rust | 3.626 (3.624-3.637) | 3.627 (3.621-3.628) | +0.0% | 3.627, 3.625, 3.631 / 3.625, 3.624, 3.628 | within noise |
| dense 10 x 30 downstream_batch b512 / numpy | 64.83 (64.44-65.67) | 64.68 (64.6-64.9) | -0.2% | 65.06, 64.59, 64.92 / 64.77, 64.65, 64.68 | within noise |
| dense 10 x 30 downstream_batch b512 / rust | 52.66 (52.08-52.83) | 52.4 (52.23-52.43) | -0.5% | 52.24, 52.76, 52.72 / 52.33, 52.4, 52.34 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 10.45 (10.44-10.56) | 10.45 (10.36-10.48) | -0.1% | 10.44, 10.51, 10.46 / 10.48, 10.4, 10.43 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 4.486 (4.48-4.519) | 4.5 (4.493-4.519) | +0.3% | 4.486, 4.498, 4.499 / 4.495, 4.508, 4.505 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 94 (92.23-94.83) | 93.77 (92-95.21) | -0.2% | 93.91, 94.68, 92.88 / 92.57, 93.71, 94.62 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / rust | 61.21 (61.04-61.46) | 61.21 (60.82-61.85) | +0.0% | 61.17, 61.11, 61.44 / 61.04, 61.21, 61.53 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 9.576 (9.546-9.751) | 9.608 (9.559-9.642) | +0.3% | 9.664, 9.619, 9.565 / 9.588, 9.594, 9.62 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 4.033 (4.024-4.05) | 4.024 (4.008-4.057) | -0.2% | 4.032, 4.028, 4.042 / 4.042, 4.014, 4.023 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 47.79 (47.6-47.92) | 47.91 (47.75-48.24) | +0.3% | 47.73, 47.8, 47.76 / 47.84, 48.11, 47.83 | separated, inside spread |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 55.24 (55.19-55.29) | 55.22 (55.2-55.24) | -0.0% | 55.24, 55.24, 55.21 / 55.22, 55.22, 55.21 | within noise |
| conv 28x28, 8 ch forward / numpy | 85.23 (84.6-105.7) | 85.69 (84.75-86.26) | +0.5% | 95.16, 85.11, 85.37 / 85.89, 85.9, 84.88 | within noise |
| conv 28x28, 8 ch forward / rust | 51.65 (51.56-51.75) | 51.67 (51.6-51.68) | +0.0% | 51.65, 51.65, 51.65 / 51.68, 51.61, 51.67 | within noise |
| conv 28x28, 8 ch downstream / numpy | 71.21 (70.53-72.13) | 71.58 (70.51-73.36) | +0.5% | 70.62, 71.86, 71.33 / 71.58, 71.93, 71.87 | within noise |
| conv 28x28, 8 ch downstream / rust | 48.69 (48.52-48.78) | 47.61 (47.54-47.7) | -2.2% | 48.72, 48.73, 48.58 / 47.61, 47.6, 47.65 | consistent |
| conv 28x28, 8 ch accumulate_gradient / numpy | 59.45 (57.73-61.37) | 58.03 (57.71-60.51) | -2.4% | 59.45, 57.83, 61.11 / 58.03, 59.11, 59.11 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 29.69 (29.67-29.79) | 29.74 (29.56-29.79) | +0.2% | 29.69, 29.76, 29.68 / 29.76, 29.78, 29.63 | within noise |
| conv 28x28, 8 ch forward_batch b32 / numpy | 4746 (4233-5675) | 4716 (3963-5543) | -0.6% | 5311, 5074, 4245 / 4169, 5128, 4754 | within noise |
| conv 28x28, 8 ch forward_batch b32 / rust | 1899 (1839-2179) | 1790 (1721-2010) | -5.8% | 2022, 2016, 1842 / 1900, 1737, 1840 | within noise |
| conv 28x28, 8 ch forward_batch b512 / numpy | 7.014e+04 (6.86e+04-7.389e+04) | 7.045e+04 (6.762e+04-7.225e+04) | +0.4% | 7.301e+04, 7.014e+04, 6.873e+04 / 7.08e+04, 7.148e+04, 6.771e+04 | within noise |
| conv 28x28, 8 ch forward_batch b512 / rust | 3.611e+04 (3.45e+04-3.97e+04) | 3.592e+04 (3.487e+04-3.686e+04) | -0.5% | 3.611e+04, 3.71e+04, 3.649e+04 / 3.582e+04, 3.652e+04, 3.526e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 1541 (1492-1977) | 1587 (1493-1939) | +3.0% | 1759, 1600, 1510 / 1514, 1587, 1917 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / rust | 1501 (1500-1503) | 1468 (1467-1469) | -2.2% | 1501, 1502, 1501 / 1468, 1469, 1467 | consistent |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 5.601e+04 (5.174e+04-5.649e+04) | 5.471e+04 (5.098e+04-5.638e+04) | -2.3% | 5.624e+04, 5.605e+04, 5.269e+04 / 5.368e+04, 5.397e+04, 5.471e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / rust | 1.052e+04 (9611-1.322e+04) | 1.041e+04 (9104-1.108e+04) | -1.1% | 1.25e+04, 1.045e+04, 1.006e+04 / 1.075e+04, 1.033e+04, 9743 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 2247 (2239-2321) | 2290 (2247-2363) | +1.9% | 2279, 2280, 2247 / 2339, 2308, 2251 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 1280 (1115-1467) | 1126 (1097-1464) | -12.0% | 1461, 1279, 1121 / 1281, 1122, 1135 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 3.727e+04 (3.716e+04-3.831e+04) | 3.786e+04 (3.717e+04-3.826e+04) | +1.6% | 3.717e+04, 3.778e+04, 3.74e+04 / 3.774e+04, 3.786e+04, 3.771e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 3.139e+04 (2.682e+04-3.629e+04) | 3.183e+04 (2.647e+04-3.704e+04) | +1.4% | 3.386e+04, 3.03e+04, 3.073e+04 / 2.825e+04, 3.313e+04, 3.392e+04 | within noise |
| conv 8x8, 8 ch forward / numpy | 34.99 (34.52-36.8) | 35.15 (34.79-36.06) | +0.5% | 35.88, 34.82, 34.8 / 34.98, 35.67, 35.19 | within noise |
| conv 8x8, 8 ch forward / rust | 3.625 (3.61-3.645) | 3.62 (3.612-3.633) | -0.1% | 3.641, 3.613, 3.625 / 3.616, 3.625, 3.623 | within noise |
| conv 8x8, 8 ch downstream / numpy | 39.75 (39.48-41.55) | 39.86 (39.5-41.21) | +0.3% | 40.67, 39.63, 40.23 / 40.52, 39.65, 39.97 | within noise |
| conv 8x8, 8 ch downstream / rust | 3.178 (3.166-3.189) | 3.207 (3.189-3.213) | +0.9% | 3.17, 3.188, 3.178 / 3.2, 3.211, 3.198 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient / numpy | 12.54 (12.39-12.7) | 12.59 (12.48-12.82) | +0.4% | 12.58, 12.51, 12.51 / 12.6, 12.72, 12.51 | within noise |
| conv 8x8, 8 ch accumulate_gradient / rust | 2.24 (2.218-2.251) | 2.224 (2.216-2.233) | -0.7% | 2.244, 2.227, 2.244 / 2.232, 2.22, 2.222 | within noise |
| conv 8x8, 8 ch forward_batch b32 / numpy | 129.3 (128.6-130.4) | 129.6 (128.7-130.9) | +0.2% | 130, 129.5, 128.7 / 130, 129.1, 130.1 | within noise |
| conv 8x8, 8 ch forward_batch b32 / rust | 88.69 (88.23-89.41) | 88.59 (88.24-89.48) | -0.1% | 88.77, 88.82, 88.69 / 89.16, 88.89, 88.28 | within noise |
| conv 8x8, 8 ch forward_batch b512 / numpy | 4533 (3497-4875) | 3435 (3192-4504) | -24.2% | 4495, 4186, 4680 / 3443, 4012, 3249 | separated, inside spread |
| conv 8x8, 8 ch forward_batch b512 / rust | 1646 (1548-2114) | 1824 (1601-2054) | +10.8% | 1754, 1831, 1626 / 1714, 1938, 1851 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 115.6 (114.8-116.5) | 116.4 (115-117.7) | +0.7% | 115.2, 116.3, 115.2 / 116.4, 116.4, 116.4 | separated, inside spread |
| conv 8x8, 8 ch downstream_batch b32 / rust | 84.3 (84.15-84.34) | 84.35 (84.24-84.42) | +0.1% | 84.31, 84.25, 84.3 / 84.31, 84.3, 84.42 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 1749 (1601-2037) | 1812 (1597-2213) | +3.6% | 1744, 1819, 1810 / 1918, 1813, 1807 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / rust | 1345 (1343-1348) | 1345 (1344-1347) | +0.1% | 1346, 1345, 1343 / 1345, 1346, 1346 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 148.7 (148.4-149.2) | 148.7 (148.2-151.7) | -0.0% | 148.9, 148.9, 148.5 / 150.2, 148.7, 148.5 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 50.91 (50.79-51.19) | 50.91 (50.81-51.02) | +0.0% | 50.94, 50.84, 51.06 / 50.91, 50.85, 50.98 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 2299 (2283-2373) | 2288 (2282-2376) | -0.5% | 2335, 2322, 2292 / 2288, 2289, 2329 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 982.7 (975.6-1250) | 1253 (976-1270) | +27.5% | 982.7, 977.7, 1249 / 1267, 1110, 1121 | within noise |
| conv 13x13x8, 8 ch forward / numpy | 80.3 (79.48-80.76) | 79.88 (79.47-80.31) | -0.5% | 80.3, 80.12, 80.2 / 80.14, 79.61, 80.03 | within noise |
| conv 13x13x8, 8 ch forward / rust | 48.48 (48.35-49.1) | 48.52 (48.39-49.69) | +0.1% | 48.8, 48.38, 48.48 / 48.48, 49.39, 48.44 | within noise |
| conv 13x13x8, 8 ch downstream / numpy | 89.65 (88.85-91.08) | 89.47 (88.83-89.84) | -0.2% | 89.99, 90, 89.32 / 89.47, 89.47, 89.34 | within noise |
| conv 13x13x8, 8 ch downstream / rust | 34.33 (34.03-34.44) | 34.3 (33.98-34.32) | -0.1% | 34.36, 34.24, 34.33 / 34.3, 34.19, 34.15 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 40.6 (39.92-40.96) | 40.44 (40.06-41.09) | -0.4% | 40.44, 40.4, 40.66 / 40.42, 40.58, 40.45 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 14.79 (14.74-14.84) | 14.79 (14.77-14.82) | -0.0% | 14.79, 14.8, 14.77 / 14.79, 14.78, 14.8 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 2400 (2311-2721) | 2521 (2333-2628) | +5.0% | 2330, 2559, 2505 / 2589, 2549, 2379 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 2074 (2049-2565) | 2198 (2056-2645) | +6.0% | 2093, 2315, 2051 / 2351, 2196, 2198 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 4.881e+04 (4.814e+04-5.377e+04) | 5.064e+04 (4.884e+04-5.267e+04) | +3.7% | 5.157e+04, 4.82e+04, 4.897e+04 / 5.235e+04, 5.058e+04, 4.908e+04 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 5.167e+04 (4.887e+04-5.431e+04) | 5.176e+04 (5.002e+04-5.768e+04) | +0.2% | 5.064e+04, 5.262e+04, 5.167e+04 / 5.385e+04, 5.188e+04, 5.176e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 3999 (3934-4292) | 4234 (3969-4385) | +5.9% | 4043, 3973, 4145 / 4212, 4172, 4234 | separated, inside spread |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 1042 (1036-1047) | 1040 (1035-1047) | -0.1% | 1042, 1042, 1042 / 1036, 1040, 1045 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 1.115e+05 (1.057e+05-1.16e+05) | 1.143e+05 (1.083e+05-1.18e+05) | +2.5% | 1.115e+05, 1.099e+05, 1.122e+05 / 1.15e+05, 1.143e+05, 1.131e+05 | separated, inside spread |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 7061 (6078-7767) | 6863 (6098-7799) | -2.8% | 7215, 7092, 6769 / 7786, 6863, 6340 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 1130 (1124-1141) | 1135 (1122-1142) | +0.4% | 1126, 1139, 1129 / 1135, 1140, 1125 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 604.4 (594.5-607.8) | 606 (600.8-608.1) | +0.3% | 602.3, 604.4, 601.2 / 604.3, 606, 605.5 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.836e+04 (1.833e+04-1.872e+04) | 1.847e+04 (1.831e+04-1.869e+04) | +0.6% | 1.835e+04, 1.868e+04, 1.835e+04 / 1.847e+04, 1.851e+04, 1.846e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 1.151e+04 (1.064e+04-1.352e+04) | 1.183e+04 (1.099e+04-1.362e+04) | +2.8% | 1.248e+04, 1.082e+04, 1.208e+04 / 1.169e+04, 1.296e+04, 1.133e+04 | within noise |
| conv 26x26x8/2, 8 ch forward / numpy | 90.43 (89.63-91.42) | 90.75 (90.13-133) | +0.4% | 90.52, 90.16, 90.47 / 90.7, 110.2, 111.7 | separated, inside spread |
| conv 26x26x8/2, 8 ch forward / rust | 57.64 (57.52-59.42) | 57.65 (57.6-58.42) | +0.0% | 58.54, 57.55, 57.64 / 58.01, 57.64, 57.67 | within noise |
| conv 26x26x8/2, 8 ch downstream / numpy | 103.6 (102.2-104.4) | 103.8 (103-104) | +0.2% | 103.3, 103.6, 103.5 / 103.9, 103.9, 103.2 | within noise |
| conv 26x26x8/2, 8 ch downstream / rust | 41.02 (40.53-41.34) | 41.11 (40.95-41.39) | +0.2% | 40.94, 41.09, 40.97 / 41.28, 41.01, 41.07 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 47.64 (47.33-48.05) | 47.89 (47.42-48.26) | +0.5% | 47.38, 47.95, 47.65 / 47.89, 47.84, 47.94 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 17.38 (17.35-17.44) | 17.39 (17.33-17.48) | +0.0% | 17.38, 17.4, 17.39 / 17.37, 17.39, 17.42 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 3271 (3240-3303) | 3439 (3250-3609) | +5.1% | 3273, 3292, 3244 / 3359, 3343, 3566 | separated, inside spread |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 2947 (2574-3137) | 2762 (2547-3181) | -6.3% | 2934, 3110, 2693 / 2979, 2647, 2897 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 6.292e+04 (6.214e+04-6.719e+04) | 6.422e+04 (6.32e+04-6.71e+04) | +2.1% | 6.543e+04, 6.233e+04, 6.292e+04 / 6.518e+04, 6.422e+04, 6.412e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 6.226e+04 (5.852e+04-6.595e+04) | 5.907e+04 (5.752e+04-6.442e+04) | -5.1% | 6.226e+04, 6.177e+04, 6.224e+04 / 6.102e+04, 6.028e+04, 5.843e+04 | separated, inside spread |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 8341 (7500-8945) | 8313 (7530-1.021e+04) | -0.3% | 8368, 8238, 8192 / 7632, 9551, 8230 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 1276 (1259-1280) | 1276 (1257-1280) | +0.0% | 1277, 1269, 1274 / 1278, 1267, 1277 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 1.862e+05 (1.751e+05-1.902e+05) | 1.854e+05 (1.759e+05-1.972e+05) | -0.4% | 1.888e+05, 1.819e+05, 1.832e+05 / 1.865e+05, 1.861e+05, 1.854e+05 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 2.553e+04 (2.284e+04-3.19e+04) | 2.471e+04 (2.108e+04-3.156e+04) | -3.2% | 2.9e+04, 2.44e+04, 2.427e+04 / 2.632e+04, 2.74e+04, 2.397e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 1383 (1368-1398) | 1381 (1374-1390) | -0.2% | 1386, 1381, 1383 / 1379, 1379, 1385 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 774.7 (656.3-783.9) | 761 (665.8-764.8) | -1.8% | 774.7, 707.5, 783.8 / 762.9, 720.9, 713.5 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 2.237e+04 (2.214e+04-2.263e+04) | 2.247e+04 (2.22e+04-2.255e+04) | +0.5% | 2.237e+04, 2.221e+04, 2.257e+04 / 2.251e+04, 2.233e+04, 2.242e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 1.599e+04 (1.469e+04-1.709e+04) | 1.552e+04 (1.357e+04-1.713e+04) | -2.9% | 1.599e+04, 1.485e+04, 1.696e+04 / 1.451e+04, 1.571e+04, 1.602e+04 | within noise |
| conv 26x26x8, 8 ch forward / numpy | 245.1 (244.3-245.9) | 245.1 (244.3-246.9) | +0.0% | 245.8, 244.4, 245 / 244.7, 245.9, 245.3 | within noise |
| conv 26x26x8, 8 ch forward / rust | 225.4 (225.1-225.6) | 225.5 (225.4-227.9) | +0.1% | 225.3, 225.3, 225.4 / 225.5, 226.6, 226.7 | separated, inside spread |
| conv 26x26x8, 8 ch downstream / numpy | 254.7 (252.3-256.4) | 255 (254-257.1) | +0.1% | 254.1, 256.1, 253.2 / 256.9, 254.3, 255 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 155.6 (153.8-155.9) | 153.7 (153.4-155.9) | -1.2% | 155.7, 155.1, 154.8 / 153.7, 154.7, 154.6 | separated, inside spread |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 159.5 (159-163.6) | 161 (158.6-161.6) | +1.0% | 159.4, 160.1, 161.4 / 161.4, 160, 160.2 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 64.81 (64.72-65.17) | 65.02 (64.87-65.18) | +0.3% | 64.94, 64.73, 64.94 / 64.98, 65.12, 65.01 | separated, inside spread |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 1.486e+04 (1.283e+04-1.774e+04) | 1.541e+04 (1.265e+04-1.617e+04) | +3.7% | 1.619e+04, 1.481e+04, 1.444e+04 / 1.441e+04, 1.436e+04, 1.55e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 1.217e+04 (1.139e+04-1.317e+04) | 1.254e+04 (1.204e+04-1.354e+04) | +3.0% | 1.27e+04, 1.154e+04, 1.232e+04 / 1.32e+04, 1.206e+04, 1.267e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 2.542e+05 (2.38e+05-2.617e+05) | 2.477e+05 (2.357e+05-2.681e+05) | -2.6% | 2.598e+05, 2.556e+05, 2.392e+05 / 2.519e+05, 2.477e+05, 2.528e+05 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 2.318e+05 (2.23e+05-2.343e+05) | 2.256e+05 (2.233e+05-2.37e+05) | -2.7% | 2.295e+05, 2.286e+05, 2.338e+05 / 2.304e+05, 2.313e+05, 2.242e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 2.743e+04 (2.585e+04-2.834e+04) | 2.671e+04 (2.495e+04-2.875e+04) | -2.6% | 2.732e+04, 2.806e+04, 2.646e+04 / 2.846e+04, 2.635e+04, 2.58e+04 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 3882 (3301-4627) | 4601 (3582-4678) | +18.5% | 3942, 3577, 4171 / 4661, 4070, 4247 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 5.125e+05 (5.075e+05-5.435e+05) | 5.138e+05 (4.883e+05-5.185e+05) | +0.3% | 5.265e+05, 5.166e+05, 5.102e+05 / 5.176e+05, 4.996e+05, 5.106e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 7.368e+04 (5.71e+04-7.833e+04) | 7.108e+04 (5.906e+04-8.261e+04) | -3.5% | 7.522e+04, 6.879e+04, 6.772e+04 / 8.122e+04, 6.882e+04, 6.338e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 5661 (5634-5750) | 5667 (5598-5726) | +0.1% | 5712, 5656, 5641 / 5696, 5643, 5637 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 3296 (3041-3810) | 3334 (3173-3701) | +1.1% | 3587, 3425, 3133 / 3245, 3469, 3526 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 8.873e+04 (8.836e+04-8.894e+04) | 8.854e+04 (8.822e+04-8.908e+04) | -0.2% | 8.873e+04, 8.847e+04, 8.889e+04 / 8.888e+04, 8.84e+04, 8.845e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 5.674e+04 (5.382e+04-6.496e+04) | 5.388e+04 (4.753e+04-5.731e+04) | -5.0% | 6.101e+04, 5.511e+04, 5.825e+04 / 5.242e+04, 5.426e+04, 5.306e+04 | separated, inside spread |
| pool 26x26, 8 ch forward / numpy | 106 (105.2-106.7) | 105.3 (105.2-106.5) | -0.6% | 106, 106, 105.9 / 105.3, 105.5, 105.9 | separated, inside spread |
| pool 26x26, 8 ch forward / rust | 5.37 (5.359-5.379) | 5.365 (5.349-5.375) | -0.1% | 5.373, 5.369, 5.37 / 5.371, 5.356, 5.362 | within noise |
| pool 26x26, 8 ch downstream / numpy | 55.74 (55.11-56.47) | 56.53 (55.13-56.71) | +1.4% | 55.89, 55.34, 55.93 / 56.44, 56.58, 55.84 | within noise |
| pool 26x26, 8 ch downstream / rust | 4.123 (4.101-4.153) | 4.133 (4.115-4.148) | +0.2% | 4.126, 4.116, 4.137 / 4.138, 4.13, 4.126 | within noise |
| pool 26x26, 8 ch forward_batch b32 / numpy | 2456 (2373-2600) | 2461 (2398-2484) | +0.2% | 2535, 2411, 2436 / 2454, 2424, 2480 | within noise |
| pool 26x26, 8 ch forward_batch b32 / rust | 242.1 (215.1-261.6) | 229.9 (211.5-243.4) | -5.0% | 223.3, 252.5, 249.1 / 233, 222.3, 235 | within noise |
| pool 26x26, 8 ch forward_batch b512 / numpy | 4.093e+04 (3.937e+04-4.152e+04) | 4.059e+04 (4.005e+04-4.296e+04) | -0.8% | 4.131e+04, 4.013e+04, 4.062e+04 / 4.032e+04, 4.17e+04, 4.093e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 9420 (8383-9645) | 8893 (8270-1.095e+04) | -5.6% | 9180, 8998, 9562 / 9996, 9460, 8473 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 983.1 (939.5-1544) | 990.8 (936.8-1504) | +0.8% | 1261, 964.3, 1234 / 1228, 1241, 967.8 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / rust | 130.2 (129.7-480.2) | 130.3 (129.6-461.7) | +0.0% | 129.9, 305.3, 130.1 / 130.1, 129.8, 423.8 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 6.165e+04 (5.406e+04-6.491e+04) | 6.406e+04 (5.958e+04-6.822e+04) | +3.9% | 6.285e+04, 5.595e+04, 6.345e+04 / 6.406e+04, 6.084e+04, 6.682e+04 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / rust | 2.093e+04 (1.93e+04-2.197e+04) | 2.08e+04 (1.999e+04-2.161e+04) | -0.6% | 2.155e+04, 2.001e+04, 2.104e+04 / 2.102e+04, 2.053e+04, 2.08e+04 | within noise |
| pool 6x6, 8 ch forward / numpy | 39.72 (39.56-41) | 39.64 (39.33-41.36) | -0.2% | 40.92, 39.61, 39.72 / 39.47, 39.55, 40.66 | within noise |
| pool 6x6, 8 ch forward / rust | 0.8003 (0.7989-0.8703) | 0.8003 (0.7975-0.8096) | -0.0% | 0.7993, 0.8017, 0.8349 / 0.8036, 0.8003, 0.8002 | within noise |
| pool 6x6, 8 ch downstream / numpy | 32.53 (32.44-33.42) | 33.48 (32.74-33.8) | +2.9% | 32.93, 32.51, 32.62 / 33.64, 33.14, 33.14 | separated, inside spread |
| pool 6x6, 8 ch downstream / rust | 0.6365 (0.6328-0.6382) | 0.6381 (0.6366-0.6395) | +0.3% | 0.6368, 0.6366, 0.6352 / 0.6375, 0.6379, 0.6394 | separated, inside spread |
| pool 6x6, 8 ch forward_batch b32 / numpy | 168 (167.4-227.9) | 169.2 (167.3-181.6) | +0.7% | 167.7, 197.8, 168.4 / 170.2, 167.8, 175.1 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 11.76 (11.73-11.85) | 11.85 (11.74-11.86) | +0.7% | 11.73, 11.8, 11.81 / 11.79, 11.8, 11.85 | within noise |
| pool 6x6, 8 ch forward_batch b512 / numpy | 2226 (2190-2539) | 2234 (2175-2524) | +0.3% | 2250, 2379, 2211 / 2218, 2392, 2207 | within noise |
| pool 6x6, 8 ch forward_batch b512 / rust | 187.7 (184-190.9) | 185.7 (184.1-191.8) | -1.1% | 187.7, 184.7, 190.3 / 185.7, 188.8, 184.8 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 85.23 (84.74-86.67) | 85.26 (84.95-85.76) | +0.0% | 85.21, 85.5, 85.78 / 85.05, 85.49, 85.31 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / rust | 7.68 (7.658-7.718) | 7.683 (7.661-7.735) | +0.0% | 7.662, 7.687, 7.7 / 7.681, 7.669, 7.714 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 939.7 (936.7-977.5) | 939.1 (935.4-943.6) | -0.1% | 943, 957.3, 936.8 / 941.1, 935.8, 941.4 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 126.6 (126.3-127.4) | 126.8 (126.3-384.7) | +0.2% | 126.3, 126.8, 126.9 / 126.7, 241, 255.6 | within noise |
| conv tail 32 x 5408 bare downstream b32 / numpy | 1367 (1113-1558) | 1384 (1060-1448) | +1.2% | 1336, 1428, 1316 / 1254, 1384, 1393 | within noise |
| conv tail 32 x 5408 bare downstream b32 / rust | 1232 (1223-1461) | 1422 (1163-1651) | +15.4% | 1230, 1226, 1412 / 1397, 1425, 1432 | within noise |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3.668e+04 (2.998e+04-4.467e+04) | 3.288e+04 (2.262e+04-4.024e+04) | -10.4% | 3.835e+04, 3.215e+04, 4.021e+04 / 3.276e+04, 2.971e+04, 3.506e+04 | within noise |
| conv tail 32 x 5408 bare downstream b512 / rust | 2.164e+04 (1.362e+04-2.544e+04) | 2.143e+04 (1.821e+04-2.613e+04) | -1.0% | 2.153e+04, 2.399e+04, 1.718e+04 / 2.487e+04, 1.927e+04, 2.108e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 1007 (812.3-1507) | 1350 (1259-1435) | +34.1% | 937.8, 1160, 1135 / 1393, 1262, 1363 | separated, inside spread |
| conv tail 32 x 5408 bare accumulate b32 / rust | 1176 (1132-1187) | 1179 (1091-1388) | +0.2% | 1152, 1166, 1186 / 1164, 1239, 1184 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 2.22e+04 (2.063e+04-2.426e+04) | 2.283e+04 (2.115e+04-2.379e+04) | +2.9% | 2.39e+04, 2.22e+04, 2.116e+04 / 2.319e+04, 2.168e+04, 2.318e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / rust | 1.946e+04 (1.848e+04-2.007e+04) | 1.905e+04 (1.878e+04-2.068e+04) | -2.1% | 1.979e+04, 1.908e+04, 1.941e+04 / 1.912e+04, 1.975e+04, 1.897e+04 | within noise |
| conv tail 32 x 5408 transpose b32 / numpy | 1.457 (1.449-1.478) | 1.457 (1.453-1.467) | +0.1% | 1.472, 1.455, 1.454 / 1.461, 1.456, 1.46 | within noise |
| conv tail 32 x 5408 transpose b32 / rust | 0.8715 (0.8647-0.8831) | 0.87 (0.8632-0.8788) | -0.2% | 0.8734, 0.8754, 0.8693 / 0.871, 0.8697, 0.8713 | within noise |
| conv tail 32 x 5408 transpose b512 / numpy | 29.93 (29.73-30.03) | 30.01 (29.97-30.14) | +0.3% | 29.99, 29.8, 29.95 / 30.02, 30.01, 30.07 | separated, inside spread |
| conv tail 32 x 5408 transpose b512 / rust | 11.74 (10.91-12.04) | 11.75 (11.64-12.26) | +0.1% | 11.45, 11.7, 11.9 / 11.8, 11.75, 11.95 | within noise |
| conv tail 32 x 5408 add b32 / numpy | 327.1 (312.6-403.7) | 329.9 (308.1-347.5) | +0.9% | 313.6, 329.4, 368.5 / 321.9, 333.3, 330.1 | within noise |
| conv tail 32 x 5408 add b32 / rust | 334.3 (315.6-431.9) | 333.8 (317.3-338.4) | -0.1% | 382.8, 329.4, 369.5 / 324.1, 333.8, 336.8 | within noise |
| conv tail 32 x 5408 add b512 / numpy | 363.2 (295.2-428.4) | 392.6 (298.4-413.7) | +8.1% | 363.2, 426.1, 297.9 / 413.4, 352.9, 356 | within noise |
| conv tail 32 x 5408 add b512 / rust | 431.7 (362.5-457.8) | 335.8 (313.3-431.7) | -22.2% | 397, 443.8, 427.6 / 375.9, 368.6, 322.5 | separated, inside spread |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 2.848 (2.803-2.892) | 2.84 (2.81-2.855) | -0.3% | 2.83, 2.833, 2.872 / 2.81, 2.853, 2.842 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.818 (0.8151-0.8225) | 0.8263 (0.8244-0.8356) | +1.0% | 0.8179, 0.8202, 0.8166 / 0.831, 0.8249, 0.8306 | separated, inside spread |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 15.91 (15.78-16.16) | 15.86 (15.73-16.27) | -0.3% | 15.93, 15.87, 16 / 15.79, 16.14, 15.86 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 9.314 (9.301-9.327) | 9.33 (9.314-9.403) | +0.2% | 9.307, 9.319, 9.317 / 9.332, 9.328, 9.362 | separated, inside spread |
| dense 30 x 784 bare downstream b32 / numpy | 57.61 (57.3-57.98) | 58.04 (57.59-380.5) | +0.8% | 57.63, 57.79, 57.46 / 58.14, 219.1, 57.94 | separated, inside spread |
| dense 30 x 784 bare downstream b32 / rust | 127.6 (127.1-128.4) | 127.7 (126.6-128.4) | +0.1% | 127.7, 127.3, 128 / 128.1, 127.7, 127.1 | within noise |
| dense 30 x 784 bare downstream b512 / numpy | 3534 (2745-4017) | 3293 (3139-3887) | -6.8% | 4001, 3087, 3252 / 3293, 3575, 3495 | within noise |
| dense 30 x 784 bare downstream b512 / rust | 2146 (1689-2589) | 1876 (1604-2637) | -12.6% | 2146, 2222, 2082 / 2120, 2007, 1854 | within noise |
| dense 30 x 784 bare accumulate b32 / numpy | 228.2 (66.13-409.6) | 66.8 (65.67-400.6) | -70.7% | 66.21, 399.7, 233.6 / 233.2, 233, 66.62 | within noise |
| dense 30 x 784 bare accumulate b32 / rust | 126.4 (125.9-127.2) | 126.8 (126.1-127.6) | +0.3% | 126, 127, 126.4 / 126.8, 127.1, 126.5 | within noise |
| dense 30 x 784 bare accumulate b512 / numpy | 1685 (1519-1859) | 1707 (1555-1774) | +1.3% | 1683, 1658, 1755 / 1772, 1660, 1620 | within noise |
| dense 30 x 784 bare accumulate b512 / rust | 2301 (1982-2574) | 2070 (2014-2609) | -10.0% | 2513, 2336, 2001 / 2323, 2070, 2290 | within noise |
| dense 30 x 784 transpose b32 / numpy | 1.397 (1.389-1.408) | 1.394 (1.38-1.417) | -0.2% | 1.401, 1.4, 1.395 / 1.406, 1.397, 1.386 | within noise |
| dense 30 x 784 transpose b32 / rust | 0.8925 (0.8892-0.8981) | 0.8905 (0.8848-0.912) | -0.2% | 0.8925, 0.8929, 0.8947 / 0.8896, 0.9002, 0.892 | within noise |
| dense 30 x 784 transpose b512 / numpy | 9.004 (8.974-9.022) | 9.007 (8.969-9.027) | +0.0% | 8.998, 9.007, 9.004 / 8.998, 9.019, 8.996 | within noise |
| dense 30 x 784 transpose b512 / rust | 10.89 (10.66-11.15) | 10.71 (10.65-11.42) | -1.6% | 10.92, 10.87, 10.89 / 11.04, 10.71, 10.84 | within noise |
| dense 30 x 784 add b32 / numpy | 10.25 (10.09-10.45) | 10.26 (9.937-10.37) | +0.1% | 10.39, 10.19, 10.18 / 10.26, 10.37, 9.976 | within noise |
| dense 30 x 784 add b32 / rust | 9.9 (9.423-11.04) | 9.943 (9.603-11.01) | +0.4% | 10.35, 9.512, 10.55 / 10.34, 10.2, 9.93 | within noise |
| dense 30 x 784 add b512 / numpy | 11.48 (10.96-11.52) | 11.3 (10.75-12.03) | -1.5% | 11.36, 11.24, 11.49 / 11.34, 11.39, 11.3 | within noise |
| dense 30 x 784 add b512 / rust | 9.558 (9.379-9.744) | 9.722 (9.525-9.862) | +1.7% | 9.559, 9.562, 9.494 / 9.69, 9.817, 9.624 | separated, inside spread |
| dense 30 x 784 sum_axis0 b32 / numpy | 2.798 (2.788-2.816) | 2.798 (2.775-2.824) | +0.0% | 2.805, 2.797, 2.796 / 2.798, 2.8, 2.79 | within noise |
| dense 30 x 784 sum_axis0 b32 / rust | 0.7492 (0.7449-0.7531) | 0.7554 (0.7524-0.7776) | +0.8% | 0.7469, 0.7503, 0.7498 / 0.7664, 0.7552, 0.754 | separated, inside spread |
| dense 30 x 784 sum_axis0 b512 / numpy | 15.42 (15.34-15.6) | 15.36 (15.31-15.48) | -0.3% | 15.45, 15.5, 15.35 / 15.38, 15.4, 15.36 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 8.241 (8.139-8.288) | 8.186 (8.163-8.201) | -0.7% | 8.262, 8.193, 8.214 / 8.192, 8.192, 8.176 | separated, inside spread |
| dense 10 x 30 bare downstream b32 / numpy | 5.878 (5.832-5.913) | 5.858 (5.846-5.936) | -0.3% | 5.897, 5.848, 5.879 / 5.857, 5.898, 5.859 | within noise |
| dense 10 x 30 bare downstream b32 / rust | 3.576 (3.571-3.58) | 3.576 (3.573-3.581) | +0.0% | 3.578, 3.574, 3.574 / 3.577, 3.576, 3.576 | within noise |
| dense 10 x 30 bare downstream b512 / numpy | 64.62 (64.4-64.97) | 64.63 (64.56-64.89) | +0.0% | 64.47, 64.73, 64.75 / 64.72, 64.63, 64.74 | within noise |
| dense 10 x 30 bare downstream b512 / rust | 52.21 (52.11-52.67) | 52.3 (52.13-52.72) | +0.2% | 52.23, 52.39, 52.2 / 52.14, 52.33, 52.5 | within noise |
| dense 10 x 30 bare accumulate b32 / numpy | 5.056 (5.031-5.094) | 5.041 (5.015-5.077) | -0.3% | 5.052, 5.072, 5.046 / 5.042, 5.035, 5.049 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 2.96 (2.952-2.961) | 2.957 (2.955-2.961) | -0.1% | 2.96, 2.954, 2.961 / 2.959, 2.957, 2.956 | within noise |
| dense 10 x 30 bare accumulate b512 / numpy | 32.6 (32.46-32.75) | 32.55 (32.45-32.65) | -0.2% | 32.6, 32.6, 32.61 / 32.51, 32.57, 32.55 | separated, inside spread |
| dense 10 x 30 bare accumulate b512 / rust | 45.25 (45.17-45.32) | 45.25 (45.16-45.26) | -0.0% | 45.22, 45.25, 45.26 / 45.2, 45.25, 45.22 | within noise |
| dense 10 x 30 transpose b32 / numpy | 0.8903 (0.8884-0.8921) | 0.8925 (0.8852-0.9019) | +0.2% | 0.8917, 0.8891, 0.8903 / 0.8893, 0.8967, 0.8937 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.536 (0.5291-0.5381) | 0.5379 (0.5337-0.5455) | +0.3% | 0.5341, 0.5334, 0.536 / 0.5389, 0.5372, 0.5396 | separated, inside spread |
| dense 10 x 30 transpose b512 / numpy | 3.372 (3.354-3.411) | 3.395 (3.349-3.518) | +0.7% | 3.372, 3.382, 3.375 / 3.453, 3.381, 3.375 | within noise |
| dense 10 x 30 transpose b512 / rust | 4.333 (4.294-4.39) | 4.361 (4.337-4.368) | +0.6% | 4.322, 4.315, 4.375 / 4.346, 4.366, 4.358 | within noise |
| dense 10 x 30 add b32 / numpy | 0.8974 (0.8889-0.9059) | 0.8963 (0.8919-0.9033) | -0.1% | 0.8979, 0.8945, 0.8974 / 0.895, 0.8996, 0.8957 | within noise |
| dense 10 x 30 add b32 / rust | 0.3783 (0.3749-0.381) | 0.3799 (0.3764-0.4099) | +0.4% | 0.3772, 0.3792, 0.3779 / 0.3822, 0.3931, 0.3777 | within noise |
| dense 10 x 30 add b512 / numpy | 0.9165 (0.9082-0.9221) | 0.9164 (0.9084-0.922) | -0.0% | 0.9131, 0.9152, 0.9201 / 0.9124, 0.9178, 0.9191 | within noise |
| dense 10 x 30 add b512 / rust | 0.3998 (0.3961-0.4007) | 0.4009 (0.397-0.4076) | +0.3% | 0.3985, 0.3998, 0.3984 / 0.403, 0.3993, 0.4012 | within noise |
| dense 10 x 30 sum_axis0 b32 / numpy | 2.46 (2.448-2.481) | 2.451 (2.438-2.465) | -0.3% | 2.451, 2.473, 2.459 / 2.456, 2.457, 2.44 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.5733 (0.5688-0.5825) | 0.5803 (0.5782-0.583) | +1.2% | 0.5782, 0.5728, 0.5707 / 0.5792, 0.5828, 0.5794 | separated, inside spread |
| dense 10 x 30 sum_axis0 b512 / numpy | 12.2 (12.15-13.44) | 12.23 (12.16-12.59) | +0.3% | 12.16, 12.2, 13 / 12.42, 12.19, 12.4 | within noise |
| dense 10 x 30 sum_axis0 b512 / rust | 5.392 (5.384-5.402) | 5.405 (5.397-5.436) | +0.2% | 5.393, 5.391, 5.393 / 5.402, 5.418, 5.405 | separated, inside spread |
| attention 16 x 32 forward_batch b32 / numpy | 747.7 (744-1131) | 748.2 (744-1625) | +0.1% | 939.4, 748.1, 745.8 / 752.1, 1184, 748.2 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 793.8 (788.4-795.7) | 773.3 (772.2-774) | -2.6% | 794.7, 788.9, 794.1 / 773.4, 772.8, 773.1 | consistent |
| attention 16 x 32 forward_batch b512 / numpy | 2.343e+04 (2.223e+04-2.39e+04) | 2.347e+04 (2.167e+04-2.582e+04) | +0.2% | 2.333e+04, 2.304e+04, 2.343e+04 / 2.331e+04, 2.351e+04, 2.39e+04 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 1.69e+04 (1.61e+04-1.852e+04) | 1.692e+04 (1.579e+04-1.792e+04) | +0.2% | 1.828e+04, 1.69e+04, 1.614e+04 / 1.595e+04, 1.747e+04, 1.727e+04 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 758.8 (753.9-1723) | 770.9 (757.8-1717) | +1.6% | 755.7, 762.7, 1240 / 778.8, 1241, 761.1 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / rust | 766.3 (762.9-770.2) | 764.9 (762.8-766.3) | -0.2% | 767.3, 766.3, 766.3 / 765.1, 764.5, 764.5 | consistent, small |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 2.698e+04 (2.407e+04-2.893e+04) | 2.725e+04 (2.566e+04-2.814e+04) | +1.0% | 2.879e+04, 2.63e+04, 2.578e+04 / 2.776e+04, 2.75e+04, 2.639e+04 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / rust | 1.952e+04 (1.662e+04-2.009e+04) | 1.949e+04 (1.745e+04-2.01e+04) | -0.1% | 2.002e+04, 1.907e+04, 1.794e+04 / 1.849e+04, 1.911e+04, 1.998e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 596.2 (591.8-2115) | 593.5 (591.7-597.8) | -0.4% | 598.7, 592.9, 1354 / 592.5, 593.5, 597 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 465.1 (463.4-469.4) | 462.8 (453.7-468.7) | -0.5% | 467.1, 464.4, 465.3 / 458.6, 468.5, 458.4 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 4.436e+04 (3.255e+04-4.493e+04) | 4.358e+04 (3.757e+04-4.579e+04) | -1.8% | 4.461e+04, 3.976e+04, 3.855e+04 / 4.498e+04, 4.127e+04, 4.138e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 3.421e+04 (2.892e+04-3.75e+04) | 3.675e+04 (3.001e+04-3.776e+04) | +7.5% | 3.709e+04, 3.421e+04, 2.96e+04 / 3.706e+04, 3.388e+04, 3.584e+04 | within noise |
