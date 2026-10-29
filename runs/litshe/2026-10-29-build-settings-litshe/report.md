Old `6dcd34c` against new `6dcd34c`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `10dfec9` (extension sha256 `dd311e7a023b`) and new crate `a9862b5` (extension sha256 `6fc32a9e1378`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (raspberry-pi-5.json); passes peaked at 57.3-58.4 C; max 1-min load 0.61 (measured just after this run's crate builds); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / dense 10 x 30 sum_axis0 b512 / rust +15.9% (4.648 -> 5.389 µs)
- consistent: per call / dense 10 x 30 transpose b512 / rust +14.7% (3.791 -> 4.347 µs)
- consistent: per call / pool 6x6, 8 ch forward_batch b512 / rust +13.1% (165.7 -> 187.5 µs)
- consistent: per call / pool 6x6, 8 ch forward_batch b32 / rust +11.6% (10.55 -> 11.78 µs)
- consistent: per call / dense 30 x 784 sum_axis0 b512 / rust +10.1% (7.445 -> 8.201 µs)
- consistent: per call / conv tail 32 x 5408 transpose b32 / rust +9.7% (0.8 -> 0.8778 µs)
- consistent: per call / dense 10 x 30 bare accumulate b32 / rust -9.0% (3.253 -> 2.961 µs)
- consistent: per call / dense 10 x 30 sum_axis0 b32 / rust +8.6% (0.5275 -> 0.5731 µs)
- consistent: per call / dense 30 x 784 transpose b32 / rust +8.1% (0.8253 -> 0.8924 µs)
- consistent: per call / conv 26x26x8, 8 ch accumulate_gradient / rust -7.7% (70.31 -> 64.88 µs)
- ... 47 more consistent rows (report --md)
- 213 rows within noise (29 separated inside their spread), max |Δ| 85.1%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 79.19 (78.37-80.06) | 79.13 (77.97-82.32) | -0.1% | 79.56, 79.4, 78.84 / 80.32, 79.13, 79.13 | within noise |
| conv tail 32 x 5408 forward / rust | 56.55 (52.62-75.03) | 64.12 (53.48-76.88) | +13.4% | 64.78, 64.73, 54.78 / 54.84, 74.97, 63.09 | within noise |
| conv tail 32 x 5408 downstream / numpy | 91.88 (91.59-92.67) | 92.09 (91.03-92.83) | +0.2% | 92.27, 92.06, 91.75 / 91.94, 91.93, 92.4 | within noise |
| conv tail 32 x 5408 downstream / rust | 76.65 (74.05-106.5) | 91.52 (75.12-106.4) | +19.4% | 90.52, 90.52, 76.32 / 83.73, 89.83, 99.15 | within noise |
| conv tail 32 x 5408 hidden_delta / numpy | 105.1 (103.6-105.8) | 105.1 (103.3-108.8) | -0.0% | 104.7, 104.7, 105.3 / 105, 103.9, 107.3 | within noise |
| conv tail 32 x 5408 hidden_delta / rust | 92.06 (79.19-110.5) | 103.5 (78.95-110.8) | +12.4% | 83.17, 103.9, 94.58 / 110.8, 103.5, 87.71 | within noise |
| conv tail 32 x 5408 accumulate_gradient / numpy | 796.6 (256-877) | 536.8 (302.1-838.3) | -32.6% | 262.8, 853.4, 796.6 / 791.8, 316.6, 547.4 | within noise |
| conv tail 32 x 5408 accumulate_gradient / rust | 97.6 (89.82-99.74) | 90.84 (87.52-99.53) | -6.9% | 98.74, 94.78, 94.09 / 94.92, 93.53, 89.89 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 1507 (1442-1997) | 1592 (1478-1902) | +5.7% | 1746, 1541, 1490 / 1719, 1644, 1564 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 452.9 (364.8-805.7) | 636.7 (364.9-664.1) | +40.6% | 733.8, 450.3, 374.5 / 507.1, 514.5, 645.5 | within noise |
| conv tail 32 x 5408 sgd step / numpy | 2232 (1918-2515) | 2315 (1938-2699) | +3.7% | 2308, 2076, 2332 / 2318, 2315, 2272 | within noise |
| conv tail 32 x 5408 sgd step / rust | 120.4 (116.4-276.7) | 117.7 (115.6-262.1) | -2.3% | 198.6, 120.3, 118.9 / 116, 190, 118.4 | within noise |
| conv tail 32 x 5408 forward_batch b32 / numpy | 511.6 (495.8-520.4) | 529 (509.8-541.3) | +3.4% | 507.9, 506.1, 514.4 / 529, 528.8, 520.9 | separated, inside spread |
| conv tail 32 x 5408 forward_batch b32 / rust | 1115 (1083-1128) | 1108 (1086-1130) | -0.7% | 1099, 1122, 1117 / 1113, 1113, 1098 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1.422e+04 (1.369e+04-1.667e+04) | 1.498e+04 (1.414e+04-1.609e+04) | +5.3% | 1.406e+04, 1.527e+04, 1.43e+04 / 1.491e+04, 1.544e+04, 1.498e+04 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1.093e+04 (1.035e+04-1.222e+04) | 1.063e+04 (9566-1.222e+04) | -2.8% | 1.137e+04, 1.125e+04, 1.051e+04 / 1.112e+04, 1.138e+04, 9738 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 1268 (1027-1413) | 1359 (777.4-1420) | +7.2% | 1082, 1392, 1268 / 1075, 1165, 1359 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 1304 (1174-1623) | 1275 (1125-1642) | -2.2% | 1309, 1304, 1408 / 1421, 1242, 1275 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3.634e+04 (2.752e+04-3.932e+04) | 3.032e+04 (2.772e+04-4.062e+04) | -16.6% | 3.206e+04, 3.53e+04, 3.787e+04 / 3.545e+04, 3.289e+04, 3.028e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 1.93e+04 (1.566e+04-2.453e+04) | 1.763e+04 (1.232e+04-2.257e+04) | -8.7% | 2.01e+04, 1.93e+04, 1.985e+04 / 1.471e+04, 2.08e+04, 1.567e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 3190 (2727-4039) | 3350 (3054-3742) | +5.0% | 3786, 3103, 2970 / 3503, 3249, 3305 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 1822 (1550-2204) | 1763 (1557-1987) | -3.3% | 1877, 1946, 1685 / 1647, 1845, 1888 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 6.486e+04 (6.169e+04-7.108e+04) | 6.564e+04 (6.337e+04-7.018e+04) | +1.2% | 6.676e+04, 6.353e+04, 6.642e+04 / 6.743e+04, 6.612e+04, 6.441e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 2.788e+04 (2.276e+04-3.556e+04) | 2.825e+04 (2.114e+04-2.995e+04) | +1.3% | 2.788e+04, 2.916e+04, 2.738e+04 / 2.825e+04, 2.709e+04, 2.533e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 1835 (1687-1957) | 1817 (1417-2127) | -0.9% | 1943, 1771, 1765 / 2029, 1591, 1783 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 2202 (2036-2398) | 2167 (2099-2345) | -1.6% | 2095, 2284, 2251 / 2267, 2215, 2132 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 2.297e+04 (1.98e+04-2.473e+04) | 2.298e+04 (2.175e+04-2.343e+04) | +0.0% | 2.2e+04, 2.385e+04, 2.147e+04 / 2.274e+04, 2.319e+04, 2.238e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 1.909e+04 (1.828e+04-1.925e+04) | 1.939e+04 (1.86e+04-2.061e+04) | +1.5% | 1.909e+04, 1.877e+04, 1.903e+04 / 1.906e+04, 1.992e+04, 1.956e+04 | within noise |
| dense 30 x 784 forward / numpy | 16.3 (16.19-16.6) | 16.32 (16.12-16.45) | +0.1% | 16.3, 16.39, 16.27 / 16.25, 16.41, 16.27 | within noise |
| dense 30 x 784 forward / rust | 6.438 (6.411-6.556) | 6.461 (6.432-6.556) | +0.4% | 6.539, 6.438, 6.42 / 6.455, 6.506, 6.464 | within noise |
| dense 30 x 784 downstream / numpy | 12.7 (12.67-12.72) | 12.7 (12.67-12.72) | -0.0% | 12.69, 12.69, 12.71 / 12.69, 12.69, 12.71 | within noise |
| dense 30 x 784 downstream / rust | 6.632 (6.48-6.699) | 6.668 (6.273-6.693) | +0.5% | 6.667, 6.567, 6.573 / 6.671, 6.648, 6.483 | within noise |
| dense 30 x 784 hidden_delta / numpy | 17 (16.92-17.16) | 17.02 (16.88-17.14) | +0.1% | 16.98, 17.1, 16.95 / 16.96, 17.02, 17.07 | within noise |
| dense 30 x 784 hidden_delta / rust | 7.408 (7.194-7.481) | 7.208 (7.189-7.494) | -2.7% | 7.305, 7.297, 7.458 / 7.205, 7.198, 7.351 | within noise |
| dense 30 x 784 accumulate_gradient / numpy | 42.67 (42.57-42.88) | 42.68 (42.61-42.73) | +0.0% | 42.74, 42.76, 42.57 / 42.67, 42.68, 42.66 | within noise |
| dense 30 x 784 accumulate_gradient / rust | 9.882 (9.836-9.999) | 9.876 (9.841-9.919) | -0.1% | 9.883, 9.861, 9.939 / 9.889, 9.856, 9.882 | within noise |
| dense 30 x 784 apply_accumulated_gradient / numpy | 61.19 (61.11-61.4) | 61.16 (61.06-61.5) | -0.1% | 61.25, 61.13, 61.28 / 61.29, 61.13, 61.3 | within noise |
| dense 30 x 784 apply_accumulated_gradient / rust | 36.99 (36.68-37.05) | 36.4 (36.15-36.59) | -1.6% | 36.99, 36.86, 36.95 / 36.49, 36.37, 36.3 | consistent |
| dense 30 x 784 sgd step / numpy | 107.9 (107.8-108.3) | 107.9 (107.8-108) | -0.0% | 107.9, 108, 108.1 / 107.9, 108, 107.9 | within noise |
| dense 30 x 784 sgd step / rust | 15.72 (15.64-15.76) | 15.69 (15.64-15.81) | -0.2% | 15.74, 15.73, 15.67 / 15.76, 15.68, 15.68 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 455.8 (452.2-458.5) | 91.82 (90.67-454) | -79.9% | 455.4, 456.6, 455.8 / 91.24, 91.64, 453.3 | separated, inside spread |
| dense 30 x 784 forward_batch b32 / rust | 117.1 (114.6-119.4) | 115.5 (115.2-118.7) | -1.3% | 117.1, 117, 116.9 / 116.8, 115.5, 117 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 2139 (1932-2360) | 2201 (2094-2291) | +2.9% | 2253, 2225, 2008 / 2142, 2252, 2212 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 999.1 (922-1025) | 1023 (956.7-1082) | +2.3% | 973.3, 1010, 968.4 / 1077, 1012, 987.4 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 392.4 (57.72-398.7) | 58.3 (56.58-387.2) | -85.1% | 385.8, 398.3, 225.2 / 221.6, 57.13, 222.8 | separated, inside spread |
| dense 30 x 784 downstream_batch b32 / rust | 125.9 (125.6-126.3) | 127.1 (126.9-127.5) | +1.0% | 125.9, 126.1, 125.7 / 127.3, 127.2, 127 | consistent, small |
| dense 30 x 784 downstream_batch b512 / numpy | 3364 (2356-4122) | 3416 (3230-3893) | +1.5% | 3501, 3382, 2853 / 3654, 3326, 3546 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 1848 (1582-2529) | 1850 (1642-2550) | +0.1% | 2507, 1712, 1828 / 2258, 1721, 1850 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 105.7 (105.2-105.9) | 105.4 (104.7-304.9) | -0.3% | 105.9, 105.5, 105.5 / 203.4, 205.1, 104.9 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / rust | 150.6 (147.4-334.7) | 152.2 (149.8-323.7) | +1.0% | 241, 148.8, 154.6 / 239.6, 151.1, 151.8 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 8900 (8003-9751) | 9549 (7657-1.158e+04) | +7.3% | 8423, 9094, 9194 / 9063, 8651, 1.066e+04 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / rust | 3573 (2553-3712) | 3482 (3189-3821) | -2.6% | 3671, 3296, 3057 / 3468, 3542, 3505 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 431 (86.53-443) | 441.4 (86.74-443.8) | +2.4% | 437.6, 434.7, 87.06 / 86.82, 443.2, 441.4 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 138.4 (137.4-138.8) | 138.8 (138.6-140.6) | +0.3% | 138.5, 138.6, 137.8 / 138.7, 139.6, 138.9 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 1850 (1721-1993) | 1783 (1667-1962) | -3.6% | 1866, 1873, 1777 / 1714, 1900, 1763 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 2575 (2432-2659) | 2479 (2058-2601) | -3.7% | 2465, 2576, 2636 / 2305, 2503, 2379 | within noise |
| dense 10 x 30 forward / numpy | 8.112 (8.092-8.149) | 8.148 (8.067-8.303) | +0.4% | 8.103, 8.122, 8.116 / 8.094, 8.238, 8.184 | within noise |
| dense 10 x 30 forward / rust | 0.6322 (0.6248-0.6512) | 0.6282 (0.6263-0.6449) | -0.6% | 0.6329, 0.6404, 0.631 / 0.6297, 0.6266, 0.6356 | within noise |
| dense 10 x 30 downstream / numpy | 1.832 (1.809-1.849) | 1.834 (1.81-1.88) | +0.1% | 1.832, 1.824, 1.835 / 1.829, 1.83, 1.857 | within noise |
| dense 10 x 30 downstream / rust | 0.4071 (0.4056-0.4124) | 0.3967 (0.3939-0.4044) | -2.5% | 0.4107, 0.4071, 0.406 / 0.3957, 0.3995, 0.3973 | consistent |
| dense 10 x 30 hidden_delta / numpy | 4.535 (4.513-4.567) | 4.565 (4.503-4.6) | +0.7% | 4.554, 4.537, 4.521 / 4.554, 4.537, 4.594 | within noise |
| dense 10 x 30 hidden_delta / rust | 0.8532 (0.8365-0.8586) | 0.8042 (0.8012-0.8289) | -5.7% | 0.854, 0.8475, 0.8507 / 0.8071, 0.8038, 0.815 | consistent |
| dense 10 x 30 accumulate_gradient / numpy | 5.314 (5.263-5.401) | 5.272 (5.239-5.445) | -0.8% | 5.314, 5.309, 5.339 / 5.365, 5.244, 5.279 | within noise |
| dense 10 x 30 accumulate_gradient / rust | 0.776 (0.7724-0.797) | 0.77 (0.7627-0.7829) | -0.8% | 0.7905, 0.7746, 0.7741 / 0.7664, 0.7762, 0.7728 | within noise |
| dense 10 x 30 apply_accumulated_gradient / numpy | 8.91 (8.829-9.064) | 8.891 (8.813-9.119) | -0.2% | 8.983, 8.9, 8.914 / 8.858, 9.007, 8.882 | within noise |
| dense 10 x 30 apply_accumulated_gradient / rust | 4.109 (4.093-4.129) | 4.042 (4.003-4.077) | -1.6% | 4.114, 4.116, 4.099 / 4.025, 4.043, 4.042 | consistent |
| dense 10 x 30 sgd step / numpy | 14.99 (14.97-15.08) | 14.98 (14.89-15.02) | -0.1% | 15.05, 14.98, 14.98 / 14.98, 14.98, 14.95 | separated, inside spread |
| dense 10 x 30 sgd step / rust | 0.9305 (0.9263-0.9392) | 0.9347 (0.9278-1.002) | +0.5% | 0.9269, 0.9307, 0.9362 / 0.9647, 0.933, 0.9375 | within noise |
| dense 10 x 30 forward_batch b32 / numpy | 19.47 (19.33-19.64) | 19.38 (19.31-19.43) | -0.4% | 19.49, 19.45, 19.47 / 19.32, 19.41, 19.38 | separated, inside spread |
| dense 10 x 30 forward_batch b32 / rust | 7.256 (7.25-7.317) | 7.525 (7.501-7.535) | +3.7% | 7.285, 7.254, 7.273 / 7.524, 7.525, 7.515 | consistent |
| dense 10 x 30 forward_batch b512 / numpy | 151.4 (150.8-151.5) | 151.5 (150.9-151.7) | +0.1% | 151.2, 151.2, 151.4 / 151.2, 151.5, 151.6 | within noise |
| dense 10 x 30 forward_batch b512 / rust | 107.2 (106.9-107.9) | 111.6 (111.3-111.8) | +4.1% | 107.7, 107, 107.1 / 111.7, 111.4, 111.6 | consistent |
| dense 10 x 30 downstream_batch b32 / numpy | 5.92 (5.9-5.93) | 5.918 (5.894-6.016) | -0.0% | 5.919, 5.915, 5.924 / 5.91, 5.916, 5.967 | within noise |
| dense 10 x 30 downstream_batch b32 / rust | 3.759 (3.751-3.765) | 3.624 (3.622-3.637) | -3.6% | 3.761, 3.759, 3.756 / 3.624, 3.622, 3.633 | consistent |
| dense 10 x 30 downstream_batch b512 / numpy | 64.6 (64.45-64.79) | 64.76 (64.52-64.89) | +0.2% | 64.53, 64.64, 64.69 / 64.86, 64.76, 64.61 | within noise |
| dense 10 x 30 downstream_batch b512 / rust | 54.71 (54.53-54.94) | 52.65 (52.44-52.81) | -3.8% | 54.57, 54.82, 54.74 / 52.55, 52.65, 52.65 | consistent |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 10.42 (10.34-10.45) | 10.42 (10.38-10.48) | -0.0% | 10.39, 10.42, 10.44 / 10.44, 10.41, 10.43 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 4.643 (4.629-4.67) | 4.503 (4.486-4.51) | -3.0% | 4.668, 4.643, 4.631 / 4.507, 4.506, 4.488 | consistent |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 93.22 (92.02-93.72) | 93.89 (93.14-95.24) | +0.7% | 93.36, 93.45, 92.64 / 94.19, 94.83, 93.26 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / rust | 63.33 (63.07-63.74) | 61.28 (61.09-62.23) | -3.2% | 63.4, 63.25, 63.34 / 61.13, 61.81, 61.36 | consistent |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 9.602 (9.563-9.684) | 9.61 (9.488-9.709) | +0.1% | 9.624, 9.602, 9.612 / 9.598, 9.643, 9.575 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 4.277 (4.257-4.299) | 4.016 (4.005-4.035) | -6.1% | 4.283, 4.293, 4.257 / 4.028, 4.014, 4.01 | consistent |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 47.91 (47.59-48.17) | 47.85 (47.56-48.16) | -0.1% | 47.91, 48.1, 47.68 / 47.72, 47.9, 47.86 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 54.04 (54.01-54.1) | 55.23 (55.19-55.37) | +2.2% | 54.02, 54.08, 54.05 / 55.28, 55.23, 55.27 | consistent |
| conv 28x28, 8 ch forward / numpy | 85.09 (84.86-85.84) | 85.23 (84.85-86.37) | +0.2% | 84.99, 85.24, 85.45 / 85.33, 85.84, 84.91 | within noise |
| conv 28x28, 8 ch forward / rust | 50.73 (50.71-50.8) | 51.66 (51.61-51.68) | +1.8% | 50.73, 50.75, 50.73 / 51.61, 51.66, 51.68 | consistent |
| conv 28x28, 8 ch downstream / numpy | 71.26 (70.62-72.37) | 70.83 (70.47-72.23) | -0.6% | 71.01, 71.69, 71.69 / 70.56, 70.95, 71.57 | within noise |
| conv 28x28, 8 ch downstream / rust | 47.66 (47.64-47.7) | 48.67 (48.64-48.71) | +2.1% | 47.65, 47.7, 47.64 / 48.69, 48.67, 48.65 | consistent |
| conv 28x28, 8 ch accumulate_gradient / numpy | 59.64 (57.79-74.85) | 60.3 (57.94-61.58) | +1.1% | 59.75, 59.12, 66.36 / 60.96, 57.99, 60.41 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 30.39 (30.32-30.43) | 29.71 (29.65-29.8) | -2.2% | 30.36, 30.37, 30.4 / 29.73, 29.69, 29.74 | consistent |
| conv 28x28, 8 ch forward_batch b32 / numpy | 4172 (3994-5696) | 4426 (3712-5461) | +6.1% | 4904, 4152, 4764 / 5235, 4365, 3943 | within noise |
| conv 28x28, 8 ch forward_batch b32 / rust | 1871 (1700-2218) | 2003 (1687-2181) | +7.1% | 1854, 2085, 1772 / 1852, 2084, 1916 | within noise |
| conv 28x28, 8 ch forward_batch b512 / numpy | 6.857e+04 (6.759e+04-7.031e+04) | 6.89e+04 (6.706e+04-7.062e+04) | +0.5% | 6.857e+04, 6.915e+04, 6.894e+04 / 6.762e+04, 6.89e+04, 7.011e+04 | within noise |
| conv 28x28, 8 ch forward_batch b512 / rust | 3.731e+04 (3.536e+04-4.107e+04) | 3.582e+04 (3.516e+04-3.617e+04) | -4.0% | 3.642e+04, 3.7e+04, 3.993e+04 / 3.54e+04, 3.589e+04, 3.596e+04 | separated, inside spread |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 1527 (1486-2012) | 1563 (1462-1924) | +2.4% | 1775, 1501, 1745 / 1849, 1512, 1516 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / rust | 1469 (1468-1471) | 1501 (1498-1503) | +2.2% | 1469, 1469, 1470 / 1500, 1501, 1501 | consistent |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 5.292e+04 (5.175e+04-5.724e+04) | 5.292e+04 (5.161e+04-5.742e+04) | +0.0% | 5.353e+04, 5.271e+04, 5.449e+04 / 5.451e+04, 5.227e+04, 5.506e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / rust | 1.044e+04 (9907-1.137e+04) | 1.049e+04 (9408-1.155e+04) | +0.4% | 9965, 1.047e+04, 1.107e+04 / 1.048e+04, 1.042e+04, 1.071e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 2318 (2250-2323) | 2285 (2247-2321) | -1.4% | 2284, 2321, 2314 / 2318, 2252, 2284 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 1298 (1136-1464) | 1146 (1114-1443) | -11.7% | 1300, 1295, 1300 / 1150, 1279, 1146 | separated, inside spread |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 3.733e+04 (3.72e+04-3.783e+04) | 3.723e+04 (3.714e+04-3.818e+04) | -0.3% | 3.755e+04, 3.726e+04, 3.755e+04 / 3.716e+04, 3.769e+04, 3.771e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 3.14e+04 (2.667e+04-3.49e+04) | 3.14e+04 (2.716e+04-3.531e+04) | +0.0% | 3.032e+04, 2.895e+04, 3.324e+04 / 3.031e+04, 3.209e+04, 3.123e+04 | within noise |
| conv 8x8, 8 ch forward / numpy | 34.85 (34.41-36.25) | 34.82 (34.43-35.11) | -0.1% | 34.56, 35.3, 35.63 / 34.81, 34.82, 34.77 | within noise |
| conv 8x8, 8 ch forward / rust | 3.554 (3.543-3.63) | 3.64 (3.625-3.647) | +2.4% | 3.55, 3.55, 3.596 / 3.625, 3.644, 3.64 | separated, inside spread |
| conv 8x8, 8 ch downstream / numpy | 39.87 (39.54-41.17) | 40.37 (39.75-41.33) | +1.3% | 40.46, 39.99, 39.64 / 41.05, 39.83, 40.6 | within noise |
| conv 8x8, 8 ch downstream / rust | 3.129 (3.095-3.137) | 3.188 (3.176-3.225) | +1.9% | 3.134, 3.111, 3.127 / 3.179, 3.189, 3.208 | consistent |
| conv 8x8, 8 ch accumulate_gradient / numpy | 12.5 (12.35-12.56) | 12.51 (12.41-12.56) | +0.0% | 12.5, 12.53, 12.43 / 12.53, 12.47, 12.48 | within noise |
| conv 8x8, 8 ch accumulate_gradient / rust | 2.328 (2.323-2.338) | 2.241 (2.221-2.248) | -3.7% | 2.328, 2.326, 2.332 / 2.242, 2.235, 2.234 | consistent |
| conv 8x8, 8 ch forward_batch b32 / numpy | 129.5 (127.8-170.7) | 128.9 (127.6-169.3) | -0.5% | 129.6, 128.3, 150.4 / 127.8, 148.4, 130 | within noise |
| conv 8x8, 8 ch forward_batch b32 / rust | 87.27 (86.84-87.47) | 88.6 (88.32-89.37) | +1.5% | 87.26, 87.05, 87.37 / 88.33, 89, 88.6 | consistent |
| conv 8x8, 8 ch forward_batch b512 / numpy | 3542 (3113-3984) | 3978 (3372-4372) | +12.3% | 3465, 3336, 3917 / 3978, 3750, 4051 | within noise |
| conv 8x8, 8 ch forward_batch b512 / rust | 1820 (1600-1977) | 1652 (1509-1902) | -9.2% | 1788, 1739, 1848 / 1777, 1585, 1635 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 116 (115-117.3) | 115.7 (115.4-116.8) | -0.3% | 116.8, 115.6, 116.1 / 116.6, 115.7, 115.5 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / rust | 82.73 (82.62-82.89) | 84.33 (84.2-84.48) | +1.9% | 82.71, 82.8, 82.75 / 84.41, 84.34, 84.25 | consistent |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 2000 (1611-2057) | 1630 (1598-2052) | -18.5% | 1988, 2023, 1810 / 1801, 1630, 1825 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / rust | 1319 (1318-1320) | 1345 (1344-1347) | +1.9% | 1320, 1318, 1320 / 1346, 1345, 1345 | consistent |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 148.8 (148.7-153.5) | 148.8 (148.2-155.4) | -0.0% | 148.7, 151.1, 148.9 / 148.3, 153.1, 148.7 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 52.15 (52.11-52.37) | 50.87 (50.78-50.95) | -2.5% | 52.11, 52.25, 52.16 / 50.92, 50.82, 50.86 | consistent |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 2370 (2343-2415) | 2305 (2276-2384) | -2.8% | 2394, 2356, 2367 / 2297, 2329, 2331 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 1260 (986.2-1308) | 1114 (977.5-1256) | -11.6% | 1269, 1279, 1120 / 1115, 1117, 1114 | separated, inside spread |
| conv 13x13x8, 8 ch forward / numpy | 80.31 (79.59-81.39) | 79.84 (79.43-80.53) | -0.6% | 81.04, 80.61, 79.6 / 80.23, 79.95, 79.57 | within noise |
| conv 13x13x8, 8 ch forward / rust | 50.37 (50.33-50.5) | 48.44 (48.32-48.47) | -3.8% | 50.44, 50.37, 50.33 / 48.44, 48.46, 48.38 | consistent |
| conv 13x13x8, 8 ch downstream / numpy | 89.34 (88.8-91.14) | 89.57 (89.03-89.79) | +0.3% | 90.23, 90.19, 89.08 / 89.4, 89.36, 89.63 | within noise |
| conv 13x13x8, 8 ch downstream / rust | 33.37 (33.21-33.54) | 34.3 (34.07-34.39) | +2.8% | 33.51, 33.21, 33.39 / 34.23, 34.31, 34.22 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 40.33 (40.15-40.64) | 40.47 (40.13-40.73) | +0.3% | 40.26, 40.33, 40.46 / 40.53, 40.47, 40.43 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 15.89 (15.88-15.91) | 14.79 (14.77-14.82) | -6.9% | 15.89, 15.9, 15.9 / 14.8, 14.8, 14.77 | consistent |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 2524 (2429-3000) | 2421 (2299-3094) | -4.1% | 2656, 2524, 2737 / 2773, 2345, 2426 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 2179 (2111-2648) | 2209 (1926-2479) | +1.4% | 2402, 2211, 2156 / 2212, 2072, 2275 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 4.935e+04 (4.855e+04-5.034e+04) | 4.987e+04 (4.854e+04-5.19e+04) | +1.1% | 4.946e+04, 4.894e+04, 4.965e+04 / 4.957e+04, 5.087e+04, 4.922e+04 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 5.229e+04 (4.946e+04-5.642e+04) | 5.101e+04 (5.014e+04-5.221e+04) | -2.5% | 5.229e+04, 5.171e+04, 5.361e+04 / 5.108e+04, 5.101e+04, 5.146e+04 | separated, inside spread |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 4029 (3915-4380) | 4166 (3944-4374) | +3.4% | 4210, 4032, 3966 / 4218, 3945, 4296 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 1017 (1009-1021) | 1048 (1036-1048) | +3.0% | 1015, 1013, 1017 / 1043, 1042, 1048 | consistent |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 1.118e+05 (1.103e+05-1.17e+05) | 1.103e+05 (1.1e+05-1.187e+05) | -1.4% | 1.136e+05, 1.114e+05, 1.122e+05 / 1.144e+05, 1.119e+05, 1.103e+05 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 6439 (6106-6957) | 7067 (6350-8103) | +9.8% | 6346, 6586, 6532 / 6788, 6773, 7526 | separated, inside spread |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 1132 (1126-1138) | 1132 (1123-1141) | +0.0% | 1133, 1130, 1133 / 1133, 1133, 1130 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 624 (618.3-628.1) | 605.9 (604.6-614.3) | -2.9% | 623.7, 622.4, 625.1 / 604.7, 609.9, 607.3 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.837e+04 (1.83e+04-1.847e+04) | 1.835e+04 (1.829e+04-1.867e+04) | -0.1% | 1.833e+04, 1.843e+04, 1.837e+04 / 1.837e+04, 1.834e+04, 1.85e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 1.277e+04 (1.19e+04-1.385e+04) | 1.127e+04 (1.09e+04-1.288e+04) | -11.7% | 1.211e+04, 1.363e+04, 1.282e+04 / 1.11e+04, 1.245e+04, 1.112e+04 | within noise |
| conv 26x26x8/2, 8 ch forward / numpy | 90.47 (90.24-91.48) | 90.55 (90.08-91.53) | +0.1% | 91.03, 90.24, 90.5 / 90.36, 90.33, 91.42 | within noise |
| conv 26x26x8/2, 8 ch forward / rust | 60.18 (60.08-60.61) | 57.64 (57.55-57.73) | -4.2% | 60.34, 60.33, 60.16 / 57.66, 57.56, 57.68 | consistent |
| conv 26x26x8/2, 8 ch downstream / numpy | 103.6 (102.9-104.1) | 104.2 (102.8-104.8) | +0.6% | 103.4, 103.4, 103.8 / 103.8, 104.4, 103.8 | within noise |
| conv 26x26x8/2, 8 ch downstream / rust | 40.05 (39.48-40.16) | 41.1 (40.55-41.29) | +2.6% | 40.14, 39.79, 39.97 / 41.09, 40.91, 41.16 | consistent |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 47.91 (46.95-48.39) | 47.73 (47.22-48.15) | -0.4% | 47.69, 48.08, 47.67 / 47.85, 47.44, 47.91 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 18.73 (18.68-18.77) | 17.37 (17.33-17.46) | -7.3% | 18.71, 18.73, 18.73 / 17.4, 17.39, 17.37 | consistent |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 3205 (2964-3486) | 3227 (3014-3443) | +0.7% | 3147, 3252, 3225 / 3322, 3135, 3145 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 2997 (2711-3220) | 2796 (2550-3250) | -6.7% | 3047, 3001, 2899 / 3184, 2692, 2718 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 6.436e+04 (6.189e+04-6.603e+04) | 6.376e+04 (6.191e+04-6.528e+04) | -0.9% | 6.584e+04, 6.316e+04, 6.366e+04 / 6.368e+04, 6.399e+04, 6.336e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 6.524e+04 (6.222e+04-6.641e+04) | 5.924e+04 (5.666e+04-6.369e+04) | -9.2% | 6.567e+04, 6.441e+04, 6.432e+04 / 6.052e+04, 6.143e+04, 5.674e+04 | separated, inside spread |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 8330 (7599-8967) | 8904 (7655-1.001e+04) | +6.9% | 8770, 8283, 7877 / 8904, 8833, 8822 | separated, inside spread |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 1241 (1228-1243) | 1260 (1258-1279) | +1.5% | 1234, 1235, 1242 / 1268, 1259, 1269 | consistent |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 1.832e+05 (1.736e+05-1.888e+05) | 1.827e+05 (1.77e+05-1.897e+05) | -0.3% | 1.877e+05, 1.829e+05, 1.768e+05 / 1.807e+05, 1.862e+05, 1.834e+05 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 2.209e+04 (1.997e+04-2.413e+04) | 2.15e+04 (2.05e+04-2.464e+04) | -2.7% | 2.374e+04, 2.011e+04, 2.209e+04 / 2.257e+04, 2.269e+04, 2.149e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 1375 (1370-1399) | 1377 (1364-1387) | +0.2% | 1386, 1377, 1372 / 1386, 1371, 1372 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 757.6 (725.7-818.4) | 782.8 (655.7-789.6) | +3.3% | 787.7, 760.5, 740.4 / 722.6, 780.1, 787.2 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 2.246e+04 (2.211e+04-2.25e+04) | 2.232e+04 (2.208e+04-2.261e+04) | -0.6% | 2.212e+04, 2.246e+04, 2.25e+04 / 2.214e+04, 2.249e+04, 2.238e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 1.494e+04 (1.391e+04-1.754e+04) | 1.481e+04 (1.327e+04-1.653e+04) | -0.8% | 1.603e+04, 1.516e+04, 1.494e+04 / 1.556e+04, 1.481e+04, 1.469e+04 | within noise |
| conv 26x26x8, 8 ch forward / numpy | 245.4 (244.2-246.2) | 245.3 (244.4-245.5) | -0.0% | 245.6, 245.1, 245.2 / 245.4, 245.4, 244.7 | within noise |
| conv 26x26x8, 8 ch forward / rust | 235.4 (235-236.7) | 226.6 (225.1-364.9) | -3.8% | 235.1, 236.2, 235.9 / 295.2, 226.6, 226.5 | within noise |
| conv 26x26x8, 8 ch downstream / numpy | 254.4 (252.5-260.8) | 255.3 (253.2-256.6) | +0.3% | 253.9, 254, 257.4 / 254.9, 255.4, 255.2 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 152 (151.8-153.5) | 155.6 (154.5-155.7) | +2.3% | 152, 151.8, 153.1 / 155, 155.6, 155.6 | consistent |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 160.2 (158.9-162.2) | 159.8 (157.6-161.2) | -0.3% | 160.6, 160.2, 160.5 / 160.6, 159.3, 159.2 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 70.31 (69.96-70.41) | 64.88 (64.79-65.06) | -7.7% | 70.38, 70.32, 70.11 / 64.82, 64.87, 65.04 | consistent |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 1.25e+04 (1.169e+04-1.378e+04) | 1.391e+04 (1.282e+04-1.5e+04) | +11.3% | 1.25e+04, 1.264e+04, 1.294e+04 / 1.358e+04, 1.425e+04, 1.391e+04 | separated, inside spread |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 1.249e+04 (1.207e+04-1.34e+04) | 1.159e+04 (1.149e+04-1.254e+04) | -7.2% | 1.315e+04, 1.237e+04, 1.223e+04 / 1.181e+04, 1.202e+04, 1.151e+04 | separated, inside spread |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 2.488e+05 (2.353e+05-2.6e+05) | 2.408e+05 (2.31e+05-2.564e+05) | -3.2% | 2.475e+05, 2.436e+05, 2.556e+05 / 2.408e+05, 2.401e+05, 2.476e+05 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 2.347e+05 (2.321e+05-2.416e+05) | 2.255e+05 (2.235e+05-2.317e+05) | -3.9% | 2.379e+05, 2.384e+05, 2.325e+05 / 2.259e+05, 2.276e+05, 2.246e+05 | separated, inside spread |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 2.617e+04 (2.409e+04-2.822e+04) | 2.553e+04 (2.307e+04-2.702e+04) | -2.4% | 2.451e+04, 2.65e+04, 2.728e+04 / 2.54e+04, 2.666e+04, 2.396e+04 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 3865 (2923-4796) | 3669 (3200-4471) | -5.1% | 4302, 3537, 3489 / 3346, 3632, 4221 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 5.029e+05 (4.818e+05-5.264e+05) | 5.142e+05 (4.916e+05-5.27e+05) | +2.2% | 4.952e+05, 4.906e+05, 5.166e+05 / 5.227e+05, 5.019e+05, 5.059e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 6.411e+04 (4.914e+04-7.9e+04) | 7.175e+04 (4.592e+04-8.104e+04) | +11.9% | 6.129e+04, 5.77e+04, 7.047e+04 / 4.823e+04, 8.059e+04, 7.175e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 5631 (5598-5679) | 5637 (5597-5662) | +0.1% | 5659, 5611, 5631 / 5637, 5600, 5654 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 3574 (3316-3754) | 3478 (3283-3650) | -2.7% | 3641, 3662, 3417 / 3301, 3532, 3562 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 8.856e+04 (8.812e+04-8.936e+04) | 8.909e+04 (8.794e+04-8.996e+04) | +0.6% | 8.829e+04, 8.879e+04, 8.874e+04 / 8.872e+04, 8.975e+04, 8.852e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 5.811e+04 (5.272e+04-6.086e+04) | 5.418e+04 (4.569e+04-5.803e+04) | -6.8% | 5.646e+04, 5.646e+04, 5.905e+04 / 4.879e+04, 5.482e+04, 5.596e+04 | separated, inside spread |
| pool 26x26, 8 ch forward / numpy | 105.8 (105-107.3) | 105.8 (105.3-106.1) | -0.0% | 106.6, 105.3, 106.2 / 105.6, 105.8, 105.8 | within noise |
| pool 26x26, 8 ch forward / rust | 5.215 (5.206-5.236) | 5.365 (5.344-5.38) | +2.9% | 5.218, 5.224, 5.209 / 5.358, 5.361, 5.374 | consistent |
| pool 26x26, 8 ch downstream / numpy | 55.19 (54.94-55.6) | 55.12 (54.95-56.06) | -0.1% | 55, 55.41, 55.3 / 55.14, 55.57, 55.04 | within noise |
| pool 26x26, 8 ch downstream / rust | 4.132 (4.103-4.154) | 4.123 (4.097-4.154) | -0.2% | 4.153, 4.132, 4.111 / 4.13, 4.129, 4.107 | within noise |
| pool 26x26, 8 ch forward_batch b32 / numpy | 2424 (2411-2448) | 2403 (2391-2442) | -0.9% | 2418, 2431, 2432 / 2403, 2417, 2416 | separated, inside spread |
| pool 26x26, 8 ch forward_batch b32 / rust | 223 (191.6-229.8) | 212.8 (199.1-229) | -4.6% | 199.3, 227.6, 223.5 / 206.1, 221.7, 206.5 | within noise |
| pool 26x26, 8 ch forward_batch b512 / numpy | 4.062e+04 (3.99e+04-4.146e+04) | 4.003e+04 (3.915e+04-4.178e+04) | -1.4% | 4.071e+04, 4.022e+04, 4.078e+04 / 3.96e+04, 4.09e+04, 4.037e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 9062 (7609-9484) | 8713 (7797-9993) | -3.9% | 8829, 8409, 9341 / 9086, 9380, 8179 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 968.7 (953.2-1517) | 972.6 (955.1-1517) | +0.4% | 973.4, 959.6, 1243 / 958, 972.6, 1502 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / rust | 304.1 (129.8-489.3) | 130.2 (129.6-469.9) | -57.2% | 304.7, 129.9, 483.7 / 299.9, 299.8, 129.9 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 5.999e+04 (5.704e+04-6.192e+04) | 5.68e+04 (5.171e+04-6.129e+04) | -5.3% | 5.853e+04, 5.988e+04, 6.088e+04 / 5.516e+04, 5.857e+04, 5.65e+04 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / rust | 2.076e+04 (1.983e+04-2.141e+04) | 2.092e+04 (1.993e+04-2.171e+04) | +0.8% | 2.086e+04, 2.062e+04, 2.063e+04 / 2.088e+04, 2.04e+04, 2.134e+04 | within noise |
| pool 6x6, 8 ch forward / numpy | 39.77 (39.59-39.95) | 39.63 (39.37-41.61) | -0.4% | 39.94, 39.67, 39.75 / 39.47, 39.55, 40.79 | within noise |
| pool 6x6, 8 ch forward / rust | 0.7643 (0.758-0.7759) | 0.8003 (0.7986-0.8051) | +4.7% | 0.7714, 0.7631, 0.7613 / 0.8005, 0.8003, 0.8019 | consistent |
| pool 6x6, 8 ch downstream / numpy | 32.43 (32.25-32.58) | 32.68 (32.42-33.22) | +0.8% | 32.32, 32.44, 32.51 / 32.91, 32.77, 32.47 | within noise |
| pool 6x6, 8 ch downstream / rust | 0.6649 (0.6608-0.6659) | 0.6368 (0.6339-0.638) | -4.2% | 0.6652, 0.6632, 0.6644 / 0.6363, 0.6378, 0.6349 | consistent |
| pool 6x6, 8 ch forward_batch b32 / numpy | 168.8 (167.2-171.7) | 168 (167.6-169.3) | -0.5% | 167.9, 169.1, 170.2 / 168.5, 167.9, 168.6 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 10.55 (10.51-10.58) | 11.78 (11.75-11.8) | +11.6% | 10.57, 10.53, 10.53 / 11.77, 11.77, 11.79 | consistent |
| pool 6x6, 8 ch forward_batch b512 / numpy | 2196 (2183-2449) | 2238 (2176-2533) | +1.9% | 2191, 2207, 2321 / 2217, 2199, 2433 | within noise |
| pool 6x6, 8 ch forward_batch b512 / rust | 165.7 (165.2-170.3) | 187.5 (185.6-191.6) | +13.1% | 168.1, 167.5, 165.4 / 187.5, 188.5, 188.6 | consistent |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 85.48 (84.91-86.26) | 85.26 (84.63-87.11) | -0.3% | 85.53, 85.21, 85.87 / 85.11, 84.97, 86.33 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / rust | 7.85 (7.832-7.878) | 7.692 (7.67-7.732) | -2.0% | 7.866, 7.853, 7.839 / 7.681, 7.712, 7.699 | consistent |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 940.8 (932.4-954.2) | 942.5 (937.3-957.1) | +0.2% | 947.9, 936.9, 939.3 / 942.3, 949.2, 942 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 129.2 (129-333.3) | 126.7 (126.3-127.6) | -1.9% | 129.3, 129.2, 231.1 / 126.7, 127.1, 126.6 | separated, inside spread |
| conv tail 32 x 5408 bare downstream b32 / numpy | 1254 (936.7-1380) | 1225 (999.5-1360) | -2.3% | 1206, 1158, 1260 / 1297, 1066, 1267 | within noise |
| conv tail 32 x 5408 bare downstream b32 / rust | 1401 (1140-1617) | 1314 (1150-1594) | -6.2% | 1401, 1556, 1146 / 1380, 1315, 1314 | within noise |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3.115e+04 (2.289e+04-4.071e+04) | 3.2e+04 (2.408e+04-4.892e+04) | +2.7% | 3.796e+04, 3.002e+04, 2.748e+04 / 4.163e+04, 3.2e+04, 2.676e+04 | within noise |
| conv tail 32 x 5408 bare downstream b512 / rust | 2.29e+04 (1.881e+04-2.618e+04) | 1.728e+04 (1.211e+04-2.139e+04) | -24.5% | 2.249e+04, 2.356e+04, 2.12e+04 / 1.637e+04, 1.638e+04, 1.942e+04 | separated, inside spread |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 1352 (912.5-1537) | 1257 (886.5-1375) | -7.0% | 1377, 1268, 1225 / 1073, 1288, 1311 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / rust | 1168 (1135-1373) | 1186 (1084-1230) | +1.5% | 1178, 1274, 1148 / 1186, 1220, 1117 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 2.146e+04 (1.939e+04-2.284e+04) | 2.169e+04 (1.881e+04-2.423e+04) | +1.1% | 2.215e+04, 1.984e+04, 2.183e+04 / 2.074e+04, 2.264e+04, 2.084e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / rust | 1.856e+04 (1.834e+04-1.944e+04) | 1.933e+04 (1.846e+04-2.012e+04) | +4.2% | 1.896e+04, 1.852e+04, 1.856e+04 / 1.963e+04, 1.929e+04, 1.933e+04 | separated, inside spread |
| conv tail 32 x 5408 transpose b32 / numpy | 1.463 (1.453-1.479) | 1.47 (1.46-1.759) | +0.4% | 1.459, 1.469, 1.463 / 1.586, 1.465, 1.613 | within noise |
| conv tail 32 x 5408 transpose b32 / rust | 0.8 (0.7973-0.803) | 0.8778 (0.8708-0.8951) | +9.7% | 0.8001, 0.802, 0.7974 / 0.8829, 0.8834, 0.877 | consistent |
| conv tail 32 x 5408 transpose b512 / numpy | 30.01 (29.98-30.09) | 30.01 (29.84-30.06) | +0.0% | 30.08, 29.98, 30.01 / 29.91, 30.05, 29.95 | within noise |
| conv tail 32 x 5408 transpose b512 / rust | 11.6 (11.48-11.81) | 12.06 (11.71-12.13) | +4.0% | 11.56, 11.66, 11.65 / 11.82, 12.06, 12.11 | separated, inside spread |
| conv tail 32 x 5408 add b32 / numpy | 337.2 (333.6-410.5) | 333.5 (265-425.3) | -1.1% | 374.7, 339, 335.4 / 383.5, 302.7, 324 | within noise |
| conv tail 32 x 5408 add b32 / rust | 350 (302.7-459.8) | 328 (309.8-381.7) | -6.3% | 336.7, 332.8, 439.1 / 328, 351.7, 322.4 | within noise |
| conv tail 32 x 5408 add b512 / numpy | 401.1 (307.9-428.5) | 339 (309.3-412.9) | -15.5% | 373.4, 354.2, 415.1 / 327.8, 373.7, 328.8 | within noise |
| conv tail 32 x 5408 add b512 / rust | 332.6 (299.6-450.2) | 337.1 (309.2-447.3) | +1.4% | 313.8, 399.8, 364.5 / 380.1, 321.3, 389 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 2.82 (2.813-2.864) | 2.846 (2.815-2.876) | +0.9% | 2.838, 2.835, 2.817 / 2.834, 2.862, 2.836 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.776 (0.7736-0.78) | 0.8207 (0.8147-0.825) | +5.8% | 0.7758, 0.777, 0.776 / 0.817, 0.8205, 0.8235 | consistent |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 15.9 (15.81-16.17) | 15.93 (15.82-16.11) | +0.2% | 15.82, 15.95, 16.04 / 15.93, 15.89, 16.01 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 8.698 (8.676-8.761) | 9.316 (9.303-9.39) | +7.1% | 8.732, 8.698, 8.683 / 9.326, 9.311, 9.348 | consistent |
| dense 30 x 784 bare downstream b32 / numpy | 58 (57.33-58.24) | 57.91 (56.68-58.21) | -0.2% | 57.88, 57.75, 58 / 57.74, 58.1, 57.43 | within noise |
| dense 30 x 784 bare downstream b32 / rust | 126.2 (125.6-128) | 127.2 (126.4-128.2) | +0.8% | 126, 126.9, 126.2 / 126.8, 126.9, 128.1 | within noise |
| dense 30 x 784 bare downstream b512 / numpy | 3048 (2688-4030) | 2964 (2795-3940) | -2.8% | 2976, 3366, 3227 / 3842, 2907, 2907 | within noise |
| dense 30 x 784 bare downstream b512 / rust | 1665 (1587-2522) | 1917 (1557-2543) | +15.1% | 2097, 1591, 1736 / 2200, 2216, 1713 | within noise |
| dense 30 x 784 bare accumulate b32 / numpy | 66.56 (66.11-66.84) | 66.43 (65.58-66.9) | -0.2% | 66.38, 66.71, 66.47 / 66.33, 66.19, 66.71 | within noise |
| dense 30 x 784 bare accumulate b32 / rust | 125.8 (124.7-126.9) | 126.8 (126-127.4) | +0.8% | 126.7, 124.9, 125.8 / 126.8, 126.3, 127.2 | within noise |
| dense 30 x 784 bare accumulate b512 / numpy | 1688 (1612-1800) | 1670 (1626-1814) | -1.1% | 1794, 1639, 1688 / 1738, 1720, 1655 | within noise |
| dense 30 x 784 bare accumulate b512 / rust | 2245 (1964-2606) | 2449 (2005-2585) | +9.1% | 2541, 1995, 2258 / 2521, 2222, 2283 | within noise |
| dense 30 x 784 transpose b32 / numpy | 1.407 (1.392-1.444) | 1.42 (1.393-1.629) | +0.9% | 1.422, 1.405, 1.414 / 1.476, 1.527, 1.396 | within noise |
| dense 30 x 784 transpose b32 / rust | 0.8253 (0.7836-0.8307) | 0.8924 (0.8862-0.9072) | +8.1% | 0.8217, 0.8065, 0.8285 / 0.8971, 0.8986, 0.8899 | consistent |
| dense 30 x 784 transpose b512 / numpy | 9.014 (8.958-9.034) | 8.994 (8.963-9.028) | -0.2% | 9.032, 8.985, 8.994 / 8.996, 8.983, 9.004 | within noise |
| dense 30 x 784 transpose b512 / rust | 10.63 (10.1-10.97) | 11.07 (10.72-11.49) | +4.2% | 10.4, 10.8, 10.36 / 10.92, 11.24, 11.11 | separated, inside spread |
| dense 30 x 784 add b32 / numpy | 10.3 (10.11-10.65) | 10.37 (10.21-10.64) | +0.6% | 10.16, 10.3, 10.48 / 10.51, 10.34, 10.29 | within noise |
| dense 30 x 784 add b32 / rust | 9.561 (9.327-10.87) | 9.635 (9.367-10.91) | +0.8% | 9.67, 9.409, 10.19 / 10.35, 9.568, 9.526 | within noise |
| dense 30 x 784 add b512 / numpy | 11.31 (11.03-11.37) | 11.49 (11.05-11.56) | +1.6% | 11.36, 11.24, 11.18 / 11.49, 11.31, 11.44 | within noise |
| dense 30 x 784 add b512 / rust | 9.703 (9.453-9.912) | 9.657 (9.451-9.775) | -0.5% | 9.63, 9.608, 9.89 / 9.489, 9.729, 9.657 | within noise |
| dense 30 x 784 sum_axis0 b32 / numpy | 2.806 (2.798-2.831) | 2.803 (2.786-2.871) | -0.1% | 2.814, 2.818, 2.805 / 2.8, 2.826, 2.829 | within noise |
| dense 30 x 784 sum_axis0 b32 / rust | 0.7045 (0.6905-0.7115) | 0.7478 (0.7434-0.7517) | +6.2% | 0.7069, 0.6985, 0.7043 / 0.7498, 0.7481, 0.7455 | consistent |
| dense 30 x 784 sum_axis0 b512 / numpy | 15.37 (15.33-15.44) | 15.4 (15.35-15.43) | +0.2% | 15.41, 15.33, 15.39 / 15.41, 15.36, 15.41 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 7.445 (7.424-7.483) | 8.201 (8.145-8.227) | +10.1% | 7.469, 7.428, 7.454 / 8.202, 8.188, 8.186 | consistent |
| dense 10 x 30 bare downstream b32 / numpy | 5.876 (5.86-5.903) | 5.882 (5.861-5.907) | +0.1% | 5.876, 5.874, 5.882 / 5.889, 5.896, 5.87 | within noise |
| dense 10 x 30 bare downstream b32 / rust | 3.711 (3.706-3.737) | 3.576 (3.543-3.581) | -3.7% | 3.72, 3.707, 3.725 / 3.576, 3.559, 3.578 | consistent |
| dense 10 x 30 bare downstream b512 / numpy | 64.66 (64.58-64.81) | 64.6 (64.53-64.84) | -0.1% | 64.71, 64.73, 64.59 / 64.67, 64.53, 64.7 | within noise |
| dense 10 x 30 bare downstream b512 / rust | 54.62 (54.41-54.78) | 52.31 (52.11-52.73) | -4.2% | 54.57, 54.62, 54.63 / 52.42, 52.31, 52.42 | consistent |
| dense 10 x 30 bare accumulate b32 / numpy | 5.036 (5.023-5.115) | 5.055 (5.037-5.181) | +0.4% | 5.027, 5.074, 5.041 / 5.117, 5.053, 5.052 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 3.253 (3.24-3.257) | 2.961 (2.95-2.969) | -9.0% | 3.255, 3.252, 3.248 / 2.957, 2.967, 2.958 | consistent |
| dense 10 x 30 bare accumulate b512 / numpy | 32.58 (32.51-32.69) | 32.63 (32.57-32.84) | +0.2% | 32.57, 32.54, 32.64 / 32.66, 32.6, 32.74 | within noise |
| dense 10 x 30 bare accumulate b512 / rust | 45.34 (45.3-45.38) | 45.22 (45.16-45.26) | -0.3% | 45.33, 45.35, 45.34 / 45.22, 45.21, 45.22 | consistent, small |
| dense 10 x 30 transpose b32 / numpy | 0.8854 (0.8833-0.8952) | 0.8869 (0.8847-0.8912) | +0.2% | 0.8841, 0.8897, 0.8895 / 0.8889, 0.8869, 0.886 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.5023 (0.4991-0.5075) | 0.5375 (0.5323-0.5482) | +7.0% | 0.5047, 0.5036, 0.4998 / 0.5375, 0.5412, 0.535 | consistent |
| dense 10 x 30 transpose b512 / numpy | 3.423 (3.374-3.513) | 3.384 (3.353-3.568) | -1.1% | 3.392, 3.444, 3.459 / 3.377, 3.431, 3.468 | within noise |
| dense 10 x 30 transpose b512 / rust | 3.791 (3.764-3.899) | 4.347 (4.302-4.369) | +14.7% | 3.786, 3.845, 3.822 / 4.349, 4.324, 4.347 | consistent |
| dense 10 x 30 add b32 / numpy | 0.8998 (0.8919-0.9249) | 0.8916 (0.8853-0.9029) | -0.9% | 0.8941, 0.9149, 0.8998 / 0.8967, 0.8967, 0.8885 | within noise |
| dense 10 x 30 add b32 / rust | 0.3848 (0.3817-0.3888) | 0.378 (0.376-0.3815) | -1.8% | 0.3844, 0.3853, 0.3848 / 0.3801, 0.3787, 0.3763 | consistent |
| dense 10 x 30 add b512 / numpy | 0.9186 (0.9104-0.9416) | 0.9182 (0.9131-0.9402) | -0.0% | 0.9314, 0.9139, 0.9154 / 0.9287, 0.9176, 0.9176 | within noise |
| dense 10 x 30 add b512 / rust | 0.408 (0.4006-0.4136) | 0.3998 (0.3983-0.404) | -2.0% | 0.408, 0.4113, 0.404 / 0.4011, 0.4006, 0.3993 | separated, inside spread |
| dense 10 x 30 sum_axis0 b32 / numpy | 2.487 (2.453-2.554) | 2.466 (2.448-2.507) | -0.8% | 2.53, 2.467, 2.49 / 2.456, 2.502, 2.461 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.5275 (0.5254-0.531) | 0.5731 (0.565-0.5813) | +8.6% | 0.5275, 0.5284, 0.5273 / 0.5701, 0.5731, 0.5754 | consistent |
| dense 10 x 30 sum_axis0 b512 / numpy | 12.2 (12.17-12.73) | 12.21 (12.15-12.26) | +0.0% | 12.19, 12.19, 12.47 / 12.18, 12.23, 12.2 | within noise |
| dense 10 x 30 sum_axis0 b512 / rust | 4.648 (4.642-4.653) | 5.389 (5.387-5.427) | +15.9% | 4.648, 4.645, 4.65 / 5.407, 5.393, 5.388 | consistent |
| attention 16 x 32 forward_batch b32 / numpy | 749.5 (744.1-757.9) | 746.2 (742.9-747.1) | -0.4% | 747.9, 751, 752.7 / 747.1, 744.3, 746.2 | separated, inside spread |
| attention 16 x 32 forward_batch b32 / rust | 801.5 (798.8-802.6) | 794.2 (789.3-795.2) | -0.9% | 800.4, 800.2, 802.5 / 792.1, 794.4, 792.4 | consistent, small |
| attention 16 x 32 forward_batch b512 / numpy | 2.229e+04 (2.103e+04-2.415e+04) | 2.294e+04 (2.186e+04-2.41e+04) | +2.9% | 2.167e+04, 2.299e+04, 2.302e+04 / 2.253e+04, 2.277e+04, 2.343e+04 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 1.621e+04 (1.581e+04-1.799e+04) | 1.67e+04 (1.554e+04-1.841e+04) | +3.0% | 1.596e+04, 1.695e+04, 1.636e+04 / 1.672e+04, 1.636e+04, 1.698e+04 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 759 (753.7-777.3) | 762.6 (754.6-1226) | +0.5% | 760.8, 753.9, 768.2 / 994.1, 758.6, 768.7 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / rust | 759.1 (755.6-762.1) | 763.4 (760.6-765.1) | +0.6% | 757.5, 761.7, 757.6 / 763, 763.4, 762.2 | separated, inside spread |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 2.704e+04 (2.634e+04-2.766e+04) | 2.814e+04 (2.507e+04-3.059e+04) | +4.1% | 2.7e+04, 2.733e+04, 2.689e+04 / 2.909e+04, 2.783e+04, 2.741e+04 | separated, inside spread |
| attention 16 x 32 hidden_delta_batch b512 / rust | 1.922e+04 (1.792e+04-2.014e+04) | 1.865e+04 (1.721e+04-2.135e+04) | -2.9% | 1.805e+04, 1.957e+04, 1.969e+04 / 2.025e+04, 1.86e+04, 1.791e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 592.3 (581.3-594.3) | 587 (579.9-599.8) | -0.9% | 593.4, 586.8, 591.8 / 584.6, 593.9, 583.7 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 455.2 (448.3-462.6) | 464.9 (461.2-468.4) | +2.1% | 455.9, 454.4, 455.8 / 464.4, 466.4, 463.9 | consistent |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 3.664e+04 (3.321e+04-4.412e+04) | 3.446e+04 (3.323e+04-4.445e+04) | -6.0% | 3.878e+04, 3.636e+04, 3.763e+04 / 3.515e+04, 3.356e+04, 3.957e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 3.646e+04 (2.824e+04-3.706e+04) | 3.534e+04 (3.093e+04-3.566e+04) | -3.1% | 3.31e+04, 3.233e+04, 3.666e+04 / 3.519e+04, 3.539e+04, 3.329e+04 | within noise |
