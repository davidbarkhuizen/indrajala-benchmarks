Old `6dcd34c` against new `6dcd34c`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `10dfec9` (extension sha256 `dd311e7a023b`) and new crate `4f230a4` (extension sha256 `c3a83219f593`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (raspberry-pi-5.json); passes peaked at 57.9-60.0 C; max 1-min load 1.32 (measured just after this run's crate builds); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / dense 10 x 30 bare downstream b512 / rust +28.5% (54.49 -> 70.01 µs)
- consistent: per call / dense 10 x 30 downstream_batch b512 / rust +28.0% (54.76 -> 70.12 µs)
- consistent: per call / conv 28x28, 8 ch accumulate_gradient_batch b32 / rust -21.9% (1473 -> 1150 µs)
- consistent: per call / dense 10 x 30 bare downstream b32 / rust +14.9% (3.709 -> 4.263 µs)
- consistent: per call / dense 10 x 30 downstream_batch b32 / rust +14.6% (3.759 -> 4.309 µs)
- consistent: per call / dense 10 x 30 forward_batch b512 / rust -12.6% (107.1 -> 93.62 µs)
- consistent: per call / dense 10 x 30 forward_batch b32 / rust -12.2% (7.265 -> 6.379 µs)
- consistent: per call / dense 10 x 30 hidden_delta_batch b32 / rust +11.4% (4.657 -> 5.189 µs)
- consistent: per call / conv 26x26x8, 8 ch forward / rust +10.9% (235.4 -> 261.2 µs)
- consistent: per call / conv 13x13x8, 8 ch forward / rust +10.1% (50.61 -> 55.74 µs)
- ... 30 more consistent rows (report --md)
- 230 rows within noise (38 separated inside their spread), max |Δ| 85.1%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 78.16 (77.68-79.81) | 79.14 (77.35-80.3) | +1.3% | 78.16, 78.57, 78.75 / 78.22, 79.74, 78.65 | within noise |
| conv tail 32 x 5408 forward / rust | 74.3 (54.85-77.07) | 71.95 (53.41-76.52) | -3.2% | 74.39, 65.96, 66.48 / 74.09, 64.96, 63.91 | within noise |
| conv tail 32 x 5408 downstream / numpy | 91.98 (91.45-92.85) | 91.95 (91.17-92.95) | -0.0% | 92.01, 91.98, 92.15 / 91.55, 92.46, 91.85 | within noise |
| conv tail 32 x 5408 downstream / rust | 80.62 (73.72-89.52) | 97.72 (75.71-106.4) | +21.2% | 79.78, 81.94, 82.05 / 82.9, 98.53, 105.4 | separated, inside spread |
| conv tail 32 x 5408 hidden_delta / numpy | 104.3 (103.8-105) | 104.1 (103.2-105.8) | -0.2% | 104, 104.3, 104.6 / 103.9, 105.5, 103.7 | within noise |
| conv tail 32 x 5408 hidden_delta / rust | 101 (79.42-111.1) | 93.74 (78.43-110.2) | -7.2% | 110.9, 79.52, 101 / 89.52, 86.02, 102 | within noise |
| conv tail 32 x 5408 accumulate_gradient / numpy | 604.6 (325.1-873.5) | 327.8 (294.7-392) | -45.8% | 584.7, 863.5, 362.6 / 314.1, 346.2, 343.3 | separated, inside spread |
| conv tail 32 x 5408 accumulate_gradient / rust | 94.85 (89.11-285.1) | 90.65 (87.8-97.91) | -4.4% | 89.57, 187.8, 99.46 / 89.35, 89.68, 96.03 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 1539 (1505-2060) | 1498 (1460-1552) | -2.7% | 1793, 1570, 1508 / 1532, 1472, 1514 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 582.7 (495.1-706.8) | 567 (377.6-782.6) | -2.7% | 586.6, 600.9, 582.3 / 498.8, 744, 463.5 | within noise |
| conv tail 32 x 5408 sgd step / numpy | 2315 (2086-3100) | 2239 (2139-2431) | -3.3% | 2308, 2256, 2652 / 2213, 2186, 2406 | within noise |
| conv tail 32 x 5408 sgd step / rust | 119.6 (115.4-123.1) | 121.7 (116.5-123.8) | +1.7% | 116, 123.1, 119.6 / 119.1, 122.2, 122 | within noise |
| conv tail 32 x 5408 forward_batch b32 / numpy | 514.4 (501.5-532.5) | 512.5 (497.6-526) | -0.4% | 513.7, 523.2, 512.1 / 504.7, 512.5, 521.4 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 1114 (1088-1132) | 1113 (1092-1121) | -0.1% | 1109, 1122, 1108 / 1115, 1113, 1104 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1.505e+04 (1.43e+04-1.565e+04) | 1.54e+04 (1.35e+04-1.592e+04) | +2.3% | 1.542e+04, 1.492e+04, 1.479e+04 / 1.441e+04, 1.54e+04, 1.571e+04 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1.126e+04 (1.008e+04-1.253e+04) | 1.098e+04 (1.017e+04-1.3e+04) | -2.5% | 1.119e+04, 1.126e+04, 1.13e+04 / 1.098e+04, 1.159e+04, 1.131e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 1414 (1013-1566) | 1444 (1369-1495) | +2.2% | 1480, 1265, 1242 / 1390, 1493, 1432 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 1364 (1165-1666) | 1333 (1145-1605) | -2.3% | 1257, 1357, 1526 / 1461, 1275, 1375 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3.447e+04 (2.611e+04-4.018e+04) | 3.359e+04 (2.416e+04-3.741e+04) | -2.6% | 3.773e+04, 3.196e+04, 3.145e+04 / 3.382e+04, 3.106e+04, 3.074e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2.092e+04 (1.711e+04-2.26e+04) | 2.179e+04 (1.85e+04-2.592e+04) | +4.2% | 1.908e+04, 2.13e+04, 2.12e+04 / 2.2e+04, 2.179e+04, 2.221e+04 | separated, inside spread |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 3174 (2899-3639) | 3346 (3226-3580) | +5.4% | 3439, 3004, 3269 / 3446, 3328, 3303 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 1747 (1488-2216) | 2007 (1563-2166) | +14.9% | 1661, 1892, 1852 / 1865, 1770, 2108 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 6.395e+04 (6.351e+04-6.882e+04) | 6.969e+04 (6.627e+04-7.337e+04) | +9.0% | 6.354e+04, 6.485e+04, 6.658e+04 / 6.785e+04, 7.029e+04, 6.982e+04 | separated, inside spread |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 2.232e+04 (1.993e+04-3.174e+04) | 2.795e+04 (2.448e+04-3.194e+04) | +25.2% | 2.618e+04, 2.038e+04, 2.543e+04 / 2.887e+04, 2.895e+04, 2.59e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 1858 (1605-2083) | 1845 (1716-1927) | -0.7% | 1723, 1924, 1914 / 1835, 1811, 1845 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 2207 (2117-2382) | 2292 (2094-2396) | +3.8% | 2375, 2199, 2133 / 2226, 2392, 2185 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 2.253e+04 (1.938e+04-2.559e+04) | 2.311e+04 (2.238e+04-2.323e+04) | +2.6% | 2.112e+04, 2.253e+04, 2.293e+04 / 2.286e+04, 2.311e+04, 2.28e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 1.889e+04 (1.815e+04-1.962e+04) | 1.986e+04 (1.913e+04-2.059e+04) | +5.2% | 1.889e+04, 1.822e+04, 1.949e+04 / 1.947e+04, 2.021e+04, 2.009e+04 | within noise |
| dense 30 x 784 forward / numpy | 16.24 (16.19-16.49) | 16.24 (16.05-16.32) | -0.0% | 16.24, 16.24, 16.34 / 16.26, 16.15, 16.24 | within noise |
| dense 30 x 784 forward / rust | 6.476 (6.395-6.517) | 6.387 (6.343-6.433) | -1.4% | 6.42, 6.51, 6.478 / 6.387, 6.404, 6.386 | separated, inside spread |
| dense 30 x 784 downstream / numpy | 12.75 (12.66-12.84) | 12.69 (12.67-12.72) | -0.5% | 12.75, 12.69, 12.81 / 12.69, 12.71, 12.67 | within noise |
| dense 30 x 784 downstream / rust | 6.26 (6.236-6.508) | 6.562 (6.247-6.7) | +4.8% | 6.254, 6.254, 6.387 / 6.562, 6.264, 6.669 | within noise |
| dense 30 x 784 hidden_delta / numpy | 17.15 (16.94-17.26) | 17.13 (17.02-17.2) | -0.1% | 17.18, 16.99, 17.21 / 17.12, 17.18, 17.06 | within noise |
| dense 30 x 784 hidden_delta / rust | 7.2 (7.163-7.392) | 7.459 (7.361-7.529) | +3.6% | 7.279, 7.184, 7.291 / 7.477, 7.455, 7.427 | consistent |
| dense 30 x 784 accumulate_gradient / numpy | 42.66 (42.62-42.72) | 42.65 (42.61-42.94) | -0.0% | 42.65, 42.67, 42.69 / 42.77, 42.74, 42.65 | within noise |
| dense 30 x 784 accumulate_gradient / rust | 9.889 (9.824-9.927) | 9.935 (9.841-10.06) | +0.5% | 9.854, 9.908, 9.897 / 9.962, 9.887, 9.97 | within noise |
| dense 30 x 784 apply_accumulated_gradient / numpy | 61.12 (60.98-61.17) | 61.17 (61.02-61.31) | +0.1% | 61.05, 61.13, 61.14 / 61.22, 61.21, 61.11 | within noise |
| dense 30 x 784 apply_accumulated_gradient / rust | 36.73 (36.6-37.08) | 36.23 (36.2-36.38) | -1.4% | 36.65, 36.91, 36.85 / 36.33, 36.23, 36.21 | consistent |
| dense 30 x 784 sgd step / numpy | 108 (108-108.1) | 107.9 (107.7-108.6) | -0.1% | 108, 108.1, 108 / 108.2, 108, 107.8 | within noise |
| dense 30 x 784 sgd step / rust | 15.67 (15.64-15.71) | 15.68 (15.64-15.7) | +0.1% | 15.69, 15.69, 15.64 / 15.67, 15.68, 15.68 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 449.8 (91.52-455) | 454.9 (452.4-459.1) | +1.1% | 449.8, 273.3, 273.1 / 453.6, 457.7, 454.8 | separated, inside spread |
| dense 30 x 784 forward_batch b32 / rust | 118.5 (114.9-119.3) | 114.3 (112.3-116.4) | -3.5% | 116.9, 117.1, 118.6 / 112.4, 114.4, 116.2 | separated, inside spread |
| dense 30 x 784 forward_batch b512 / numpy | 2239 (2090-2504) | 2181 (2135-2293) | -2.6% | 2323, 2345, 2123 / 2194, 2230, 2162 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 1042 (969.4-1069) | 979.4 (903.5-991.4) | -6.0% | 994.9, 1030, 1066 / 989.1, 943.1, 975.6 | separated, inside spread |
| dense 30 x 784 downstream_batch b32 / numpy | 393.3 (56.67-399.5) | 58.56 (57.87-396.5) | -85.1% | 227.6, 228.7, 393.3 / 58.32, 392.2, 58.26 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 126.4 (125.9-126.7) | 125.6 (124.5-126.3) | -0.6% | 126.3, 126.3, 126.5 / 125.3, 126, 125.4 | separated, inside spread |
| dense 30 x 784 downstream_batch b512 / numpy | 3339 (2956-4006) | 3478 (3057-4078) | +4.2% | 2969, 3615, 3718 / 3341, 3705, 3520 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 1917 (1596-2559) | 2419 (1580-2580) | +26.2% | 2233, 1941, 1727 / 2167, 1986, 2517 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 105.1 (104.2-473.6) | 105.1 (104.7-106.7) | +0.0% | 105.1, 105.2, 288.9 / 105, 105.7, 105.8 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / rust | 151 (145-159.1) | 152.9 (149.7-321.3) | +1.3% | 150.2, 149.2, 154.9 / 237.7, 152.9, 150.6 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 1.012e+04 (7955-1.147e+04) | 9131 (7679-1.164e+04) | -9.8% | 8369, 1.063e+04, 1.061e+04 / 9131, 7909, 1.09e+04 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / rust | 2912 (2710-3924) | 3179 (3039-3754) | +9.2% | 3016, 3473, 2781 / 3363, 3179, 3397 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 263.1 (86.72-444.2) | 263.8 (86.19-445.2) | +0.2% | 87.29, 265.8, 439.8 / 87.17, 265.7, 442.4 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 138.5 (138-140.2) | 139.2 (138-140.3) | +0.5% | 139.4, 138.3, 138.3 / 138.5, 139.7, 139.1 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 1829 (1721-2069) | 1793 (1706-1935) | -2.0% | 1905, 1881, 1753 / 1810, 1793, 1821 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 2112 (2079-2632) | 2535 (2080-2650) | +20.0% | 2359, 2115, 2103 / 2596, 2304, 2561 | within noise |
| dense 10 x 30 forward / numpy | 8.123 (8.075-8.193) | 8.166 (8.058-8.297) | +0.5% | 8.087, 8.126, 8.167 / 8.205, 8.116, 8.177 | within noise |
| dense 10 x 30 forward / rust | 0.6325 (0.6256-0.6391) | 0.5988 (0.5931-0.6001) | -5.3% | 0.6288, 0.6302, 0.636 / 0.5993, 0.5965, 0.5985 | consistent |
| dense 10 x 30 downstream / numpy | 1.838 (1.822-1.893) | 1.822 (1.807-1.845) | -0.8% | 1.83, 1.869, 1.836 / 1.809, 1.837, 1.825 | within noise |
| dense 10 x 30 downstream / rust | 0.4067 (0.3994-0.4101) | 0.4045 (0.3995-0.4205) | -0.6% | 0.4033, 0.405, 0.4088 / 0.4045, 0.4162, 0.4 | within noise |
| dense 10 x 30 hidden_delta / numpy | 4.522 (4.5-4.541) | 4.568 (4.51-4.662) | +1.0% | 4.522, 4.528, 4.517 / 4.52, 4.61, 4.6 | within noise |
| dense 10 x 30 hidden_delta / rust | 0.8411 (0.8336-0.8559) | 0.8186 (0.8139-0.8363) | -2.7% | 0.84, 0.8455, 0.8447 / 0.8348, 0.8155, 0.8178 | separated, inside spread |
| dense 10 x 30 accumulate_gradient / numpy | 5.294 (5.263-5.396) | 5.281 (5.268-5.301) | -0.3% | 5.274, 5.332, 5.309 / 5.281, 5.273, 5.298 | within noise |
| dense 10 x 30 accumulate_gradient / rust | 0.79 (0.7813-0.805) | 0.7692 (0.7578-0.7853) | -2.6% | 0.7989, 0.7818, 0.791 / 0.7599, 0.7754, 0.7775 | separated, inside spread |
| dense 10 x 30 apply_accumulated_gradient / numpy | 8.96 (8.814-9.112) | 8.896 (8.865-8.922) | -0.7% | 8.958, 9.055, 8.868 / 8.886, 8.908, 8.892 | within noise |
| dense 10 x 30 apply_accumulated_gradient / rust | 4.108 (4.086-4.127) | 4.11 (4.087-4.151) | +0.1% | 4.116, 4.119, 4.088 / 4.101, 4.124, 4.114 | within noise |
| dense 10 x 30 sgd step / numpy | 14.96 (14.95-15.02) | 15.05 (14.95-15.49) | +0.6% | 14.95, 14.97, 14.99 / 15.28, 14.98, 15.05 | within noise |
| dense 10 x 30 sgd step / rust | 0.9306 (0.9244-0.9339) | 0.921 (0.9152-0.9278) | -1.0% | 0.9306, 0.9248, 0.9338 / 0.9228, 0.9188, 0.9215 | separated, inside spread |
| dense 10 x 30 forward_batch b32 / numpy | 19.44 (19.38-19.54) | 19.37 (19.32-19.53) | -0.4% | 19.49, 19.41, 19.44 / 19.44, 19.41, 19.34 | within noise |
| dense 10 x 30 forward_batch b32 / rust | 7.265 (7.253-7.281) | 6.379 (6.372-6.388) | -12.2% | 7.266, 7.273, 7.255 / 6.381, 6.373, 6.386 | consistent |
| dense 10 x 30 forward_batch b512 / numpy | 151.5 (151.3-152.5) | 151.7 (151.3-151.8) | +0.2% | 151.6, 151.9, 151.4 / 151.8, 151.8, 151.6 | within noise |
| dense 10 x 30 forward_batch b512 / rust | 107.1 (107-108.1) | 93.62 (93.53-93.74) | -12.6% | 107.6, 107.4, 107 / 93.63, 93.61, 93.65 | consistent |
| dense 10 x 30 downstream_batch b32 / numpy | 5.925 (5.914-5.957) | 5.921 (5.913-5.955) | -0.1% | 5.947, 5.916, 5.923 / 5.921, 5.934, 5.924 | within noise |
| dense 10 x 30 downstream_batch b32 / rust | 3.759 (3.751-3.79) | 4.309 (4.302-4.316) | +14.6% | 3.771, 3.764, 3.759 / 4.313, 4.308, 4.306 | consistent |
| dense 10 x 30 downstream_batch b512 / numpy | 64.69 (64.44-64.9) | 64.43 (64.4-64.63) | -0.4% | 64.82, 64.61, 64.63 / 64.51, 64.52, 64.43 | separated, inside spread |
| dense 10 x 30 downstream_batch b512 / rust | 54.76 (54.54-54.91) | 70.12 (69.74-70.35) | +28.0% | 54.71, 54.63, 54.86 / 70.12, 69.95, 70.21 | consistent |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 10.54 (10.39-10.62) | 10.54 (10.46-10.59) | +0.0% | 10.54, 10.57, 10.45 / 10.48, 10.59, 10.52 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 4.657 (4.635-4.669) | 5.189 (5.178-5.191) | +11.4% | 4.65, 4.648, 4.666 / 5.185, 5.189, 5.187 | consistent |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 93.88 (93.12-95.67) | 94.2 (92.55-95.31) | +0.3% | 94.26, 94.82, 93.72 / 95.22, 92.81, 94.27 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / rust | 63.43 (63.11-92.69) | 79.48 (78.7-80.1) | +25.3% | 63.15, 63.47, 78.14 / 79.4, 79.13, 79.75 | separated, inside spread |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 9.638 (9.584-9.708) | 9.62 (9.564-9.762) | -0.2% | 9.598, 9.627, 9.704 / 9.663, 9.622, 9.62 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 4.274 (4.26-4.287) | 4.277 (4.272-4.289) | +0.1% | 4.272, 4.278, 4.273 / 4.274, 4.278, 4.282 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 47.84 (47.57-49.27) | 47.85 (47.64-48.18) | +0.0% | 48.45, 47.91, 47.82 / 47.91, 47.79, 47.95 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 54.09 (54.03-54.16) | 54.62 (54.55-54.79) | +1.0% | 54.13, 54.06, 54.06 / 54.63, 54.57, 54.72 | consistent, small |
| conv 28x28, 8 ch forward / numpy | 85.62 (84.67-85.83) | 85.46 (84.9-87.2) | -0.2% | 85.77, 85.14, 85.35 / 86.06, 86.13, 85.03 | within noise |
| conv 28x28, 8 ch forward / rust | 50.72 (50.7-50.79) | 55.85 (55.83-55.87) | +10.1% | 50.72, 50.75, 50.73 / 55.83, 55.86, 55.86 | consistent |
| conv 28x28, 8 ch downstream / numpy | 71.13 (70.73-71.64) | 71.04 (70.84-72.09) | -0.1% | 71.13, 71.58, 70.87 / 71.46, 71.2, 71.04 | within noise |
| conv 28x28, 8 ch downstream / rust | 47.65 (47.62-47.71) | 52.08 (52.05-52.11) | +9.3% | 47.68, 47.63, 47.67 / 52.08, 52.09, 52.07 | consistent |
| conv 28x28, 8 ch accumulate_gradient / numpy | 58.22 (57.73-60.38) | 57.8 (57.67-61.16) | -0.7% | 59.06, 59.11, 58.18 / 57.92, 59.48, 57.73 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 30.39 (30.3-30.54) | 30.21 (30.15-30.32) | -0.6% | 30.35, 30.41, 30.45 / 30.22, 30.24, 30.19 | consistent, small |
| conv 28x28, 8 ch forward_batch b32 / numpy | 4380 (4061-5056) | 4474 (3974-4948) | +2.1% | 4380, 4119, 4781 / 4364, 4474, 4493 | within noise |
| conv 28x28, 8 ch forward_batch b32 / rust | 1973 (1793-2159) | 1943 (1850-2371) | -1.5% | 1976, 1894, 1992 / 1939, 1865, 2293 | within noise |
| conv 28x28, 8 ch forward_batch b512 / numpy | 6.962e+04 (6.733e+04-7.28e+04) | 7.07e+04 (6.576e+04-7.397e+04) | +1.6% | 7.007e+04, 6.962e+04, 6.995e+04 / 6.971e+04, 7.07e+04, 7.183e+04 | within noise |
| conv 28x28, 8 ch forward_batch b512 / rust | 3.631e+04 (3.488e+04-3.873e+04) | 3.753e+04 (3.61e+04-3.833e+04) | +3.4% | 3.708e+04, 3.755e+04, 3.557e+04 / 3.7e+04, 3.708e+04, 3.827e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 1513 (1479-1905) | 1598 (1479-1976) | +5.6% | 1701, 1513, 1516 / 1566, 1768, 1728 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / rust | 1469 (1468-1470) | 1611 (1610-1613) | +9.6% | 1470, 1469, 1469 / 1611, 1611, 1610 | consistent |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 5.328e+04 (4.961e+04-5.455e+04) | 5.626e+04 (5.118e+04-5.818e+04) | +5.6% | 5.208e+04, 5.24e+04, 5.384e+04 / 5.446e+04, 5.797e+04, 5.465e+04 | separated, inside spread |
| conv 28x28, 8 ch downstream_batch b512 / rust | 1.009e+04 (9311-1.189e+04) | 1.098e+04 (1.025e+04-1.273e+04) | +8.8% | 1.012e+04, 9494, 1.12e+04 / 1.184e+04, 1.098e+04, 1.063e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 2302 (2242-2322) | 2314 (2246-2328) | +0.5% | 2285, 2319, 2265 / 2321, 2315, 2246 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 1473 (1446-1513) | 1150 (1134-1442) | -21.9% | 1483, 1459, 1482 / 1153, 1149, 1288 | consistent |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 3.813e+04 (3.721e+04-3.841e+04) | 3.752e+04 (3.719e+04-3.825e+04) | -1.6% | 3.764e+04, 3.821e+04, 3.807e+04 / 3.72e+04, 3.774e+04, 3.801e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 3.216e+04 (2.708e+04-3.464e+04) | 2.834e+04 (2.672e+04-2.987e+04) | -11.9% | 2.713e+04, 3.359e+04, 3.219e+04 / 2.746e+04, 2.851e+04, 2.849e+04 | within noise |
| conv 8x8, 8 ch forward / numpy | 34.78 (34.08-35.19) | 35.13 (34.57-35.8) | +1.0% | 34.94, 34.44, 34.85 / 35.29, 35.03, 35.15 | separated, inside spread |
| conv 8x8, 8 ch forward / rust | 3.555 (3.542-3.664) | 3.84 (3.834-3.919) | +8.0% | 3.555, 3.607, 3.551 / 3.845, 3.878, 3.836 | consistent |
| conv 8x8, 8 ch downstream / numpy | 39.6 (39.37-40.05) | 39.93 (39.38-40.29) | +0.8% | 39.71, 39.47, 39.74 / 39.75, 39.89, 39.93 | separated, inside spread |
| conv 8x8, 8 ch downstream / rust | 3.136 (3.127-3.143) | 3.349 (3.34-3.359) | +6.8% | 3.129, 3.142, 3.136 / 3.352, 3.344, 3.355 | consistent |
| conv 8x8, 8 ch accumulate_gradient / numpy | 12.51 (12.42-12.69) | 12.54 (12.47-13) | +0.2% | 12.51, 12.5, 12.55 / 12.53, 12.73, 12.71 | within noise |
| conv 8x8, 8 ch accumulate_gradient / rust | 2.329 (2.318-2.342) | 2.255 (2.252-2.268) | -3.2% | 2.33, 2.332, 2.329 / 2.258, 2.262, 2.254 | consistent |
| conv 8x8, 8 ch forward_batch b32 / numpy | 129 (128-130.1) | 129.3 (128.4-132.5) | +0.2% | 129.4, 129.6, 128.2 / 128.9, 131.4, 128.9 | within noise |
| conv 8x8, 8 ch forward_batch b32 / rust | 87.13 (86.87-87.41) | 95.76 (95.6-96.2) | +9.9% | 87.15, 87.15, 87.05 / 95.96, 95.76, 95.69 | consistent |
| conv 8x8, 8 ch forward_batch b512 / numpy | 3852 (3351-5015) | 3518 (3058-4188) | -8.7% | 3875, 3659, 4317 / 3959, 3191, 3518 | within noise |
| conv 8x8, 8 ch forward_batch b512 / rust | 1828 (1618-2036) | 1867 (1742-2050) | +2.2% | 1743, 1911, 1793 / 1867, 1850, 1906 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 116.2 (114.9-124.3) | 115.8 (115.6-116.3) | -0.3% | 120.3, 115.8, 115.6 / 116.2, 115.7, 115.8 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / rust | 82.64 (82.56-82.97) | 90.25 (90.06-90.66) | +9.2% | 82.64, 82.87, 82.56 / 90.15, 90.2, 90.46 | consistent |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 1748 (1602-2004) | 1823 (1596-2122) | +4.3% | 1932, 1602, 1806 / 2077, 1821, 1604 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / rust | 1319 (1316-1321) | 1443 (1436-1446) | +9.4% | 1319, 1318, 1320 / 1445, 1439, 1441 | consistent |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 148.7 (148.5-148.9) | 150.2 (148.3-155.3) | +1.0% | 148.6, 148.9, 148.7 / 150, 149.7, 152.2 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 52.14 (52.07-52.17) | 51.78 (51.71-51.88) | -0.7% | 52.15, 52.16, 52.07 / 51.79, 51.8, 51.78 | consistent, small |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 2380 (2293-2603) | 2317 (2282-2365) | -2.7% | 2448, 2373, 2411 / 2325, 2292, 2346 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 1253 (983.8-1281) | 988 (981.5-1273) | -21.1% | 1255, 1268, 1117 / 986.2, 988, 1128 | within noise |
| conv 13x13x8, 8 ch forward / numpy | 80.08 (79.39-81.25) | 79.63 (79.2-87.31) | -0.6% | 80.63, 80.3, 79.57 / 79.54, 84.7, 79.34 | within noise |
| conv 13x13x8, 8 ch forward / rust | 50.61 (50.33-50.71) | 55.74 (55.72-56.3) | +10.1% | 50.49, 50.53, 50.63 / 56.01, 55.74, 55.78 | consistent |
| conv 13x13x8, 8 ch downstream / numpy | 89.47 (89.19-90.81) | 89.8 (88.37-91.14) | +0.4% | 89.25, 90.35, 89.42 / 89.22, 90, 90.08 | within noise |
| conv 13x13x8, 8 ch downstream / rust | 33.52 (33.27-33.67) | 33.65 (33.38-33.75) | +0.4% | 33.54, 33.57, 33.42 / 33.69, 33.64, 33.57 | separated, inside spread |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 40.5 (40.14-40.6) | 40.37 (40.25-40.71) | -0.3% | 40.32, 40.6, 40.34 / 40.46, 40.57, 40.28 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 15.9 (15.86-15.94) | 14.78 (14.76-14.82) | -7.0% | 15.87, 15.92, 15.9 / 14.77, 14.8, 14.77 | consistent |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 2487 (2295-2610) | 2453 (2315-2464) | -1.4% | 2399, 2439, 2595 / 2460, 2425, 2389 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 2385 (2074-2784) | 2286 (2218-2471) | -4.1% | 2505, 2309, 2363 / 2236, 2275, 2410 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 5.022e+04 (4.917e+04-5.07e+04) | 5.001e+04 (4.785e+04-5.258e+04) | -0.4% | 5.008e+04, 5.043e+04, 4.973e+04 / 5.094e+04, 5.062e+04, 4.906e+04 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 5.408e+04 (5.049e+04-5.799e+04) | 5.469e+04 (5.1e+04-5.68e+04) | +1.1% | 5.501e+04, 5.634e+04, 5.053e+04 / 5.565e+04, 5.216e+04, 5.576e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 4077 (3992-4372) | 4209 (3923-4371) | +3.2% | 4169, 4217, 4002 / 4290, 3980, 4272 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 1018 (1011-1021) | 1026 (1014-1026) | +0.7% | 1015, 1018, 1021 / 1020, 1020, 1026 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 1.126e+05 (1.082e+05-1.264e+05) | 1.129e+05 (1.098e+05-1.229e+05) | +0.2% | 1.191e+05, 1.148e+05, 1.118e+05 / 1.142e+05, 1.108e+05, 1.178e+05 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 7286 (6118-7756) | 6609 (6486-7768) | -9.3% | 7286, 6830, 7438 / 7128, 6846, 6598 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 1127 (1122-1137) | 1136 (1126-1159) | +0.8% | 1123, 1133, 1130 / 1129, 1146, 1140 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 624.1 (619.9-628.5) | 604.1 (602.9-608.9) | -3.2% | 621, 623.5, 628 / 605.9, 604.1, 604.3 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.841e+04 (1.833e+04-1.864e+04) | 1.839e+04 (1.833e+04-1.854e+04) | -0.1% | 1.848e+04, 1.849e+04, 1.84e+04 / 1.846e+04, 1.837e+04, 1.836e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 1.23e+04 (1.156e+04-1.389e+04) | 1.127e+04 (1.111e+04-1.286e+04) | -8.4% | 1.276e+04, 1.204e+04, 1.291e+04 / 1.119e+04, 1.203e+04, 1.146e+04 | separated, inside spread |
| conv 26x26x8/2, 8 ch forward / numpy | 90.4 (89.95-130.4) | 90.33 (89.96-91.65) | -0.1% | 110.7, 90.19, 90.18 / 90.06, 90.24, 91.36 | within noise |
| conv 26x26x8/2, 8 ch forward / rust | 60.32 (60.01-60.6) | 66.27 (66.19-67.03) | +9.9% | 60.14, 60.47, 60.31 / 66.27, 66.21, 67.01 | consistent |
| conv 26x26x8/2, 8 ch downstream / numpy | 103.5 (102.9-104.6) | 104.6 (103.6-105.6) | +1.0% | 103.9, 103.2, 103.7 / 104.4, 104.6, 104.7 | separated, inside spread |
| conv 26x26x8/2, 8 ch downstream / rust | 39.81 (39.48-40.14) | 40.18 (39.65-40.47) | +0.9% | 39.82, 39.8, 39.8 / 40.06, 40.18, 40.23 | consistent, small |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 47.81 (47.53-48) | 48.11 (47.94-48.23) | +0.6% | 47.81, 47.97, 47.58 / 48.02, 48.19, 48.03 | separated, inside spread |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 18.71 (18.68-18.76) | 17.34 (17.29-17.44) | -7.3% | 18.7, 18.73, 18.72 / 17.42, 17.34, 17.3 | consistent |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 3366 (3298-3714) | 3234 (3099-3370) | -3.9% | 3401, 3324, 3537 / 3330, 3138, 3246 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 2852 (2716-2929) | 2962 (2887-3304) | +3.9% | 2882, 2794, 2838 / 3098, 3095, 2911 | separated, inside spread |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 6.339e+04 (6.251e+04-6.475e+04) | 6.325e+04 (6.133e+04-6.561e+04) | -0.2% | 6.357e+04, 6.286e+04, 6.416e+04 / 6.245e+04, 6.37e+04, 6.347e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 6.498e+04 (5.916e+04-6.67e+04) | 6.528e+04 (6.068e+04-6.692e+04) | +0.5% | 6.59e+04, 6.183e+04, 6.499e+04 / 6.351e+04, 6.406e+04, 6.59e+04 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 8669 (8349-8938) | 8302 (7241-8921) | -4.2% | 8706, 8643, 8669 / 7823, 8734, 8066 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 1240 (1226-1249) | 1241 (1232-1251) | +0.1% | 1233, 1234, 1245 / 1240, 1243, 1241 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 1.819e+05 (1.783e+05-1.877e+05) | 1.848e+05 (1.777e+05-1.881e+05) | +1.6% | 1.822e+05, 1.797e+05, 1.853e+05 / 1.866e+05, 1.848e+05, 1.811e+05 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 2.178e+04 (1.934e+04-2.897e+04) | 2.354e+04 (1.911e+04-2.82e+04) | +8.1% | 2.416e+04, 2.149e+04, 2.25e+04 / 2.411e+04, 2.533e+04, 2.173e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 1381 (1372-1391) | 1379 (1374-1385) | -0.1% | 1385, 1379, 1378 / 1380, 1381, 1379 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 797.7 (756-822.6) | 781.4 (681.5-784.7) | -2.0% | 771.2, 784.5, 815.8 / 730.9, 783.6, 773.3 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 2.242e+04 (2.226e+04-2.255e+04) | 2.224e+04 (2.216e+04-2.257e+04) | -0.8% | 2.238e+04, 2.25e+04, 2.236e+04 / 2.229e+04, 2.222e+04, 2.239e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 1.497e+04 (1.308e+04-1.772e+04) | 1.567e+04 (1.331e+04-1.653e+04) | +4.7% | 1.497e+04, 1.685e+04, 1.363e+04 / 1.492e+04, 1.454e+04, 1.622e+04 | within noise |
| conv 26x26x8, 8 ch forward / numpy | 245.3 (244-245.8) | 244.8 (243.6-247.9) | -0.2% | 245.3, 244.2, 245.5 / 246.3, 244.7, 244.4 | within noise |
| conv 26x26x8, 8 ch forward / rust | 235.4 (234.8-236.6) | 261.2 (260.5-263.2) | +10.9% | 235.4, 235.8, 235.7 / 261.9, 261.2, 261.5 | consistent |
| conv 26x26x8, 8 ch downstream / numpy | 255.1 (253.3-257.9) | 255.1 (252.1-256.4) | +0.0% | 255.9, 255.8, 254.6 / 255.8, 253.5, 255.2 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 152.8 (151.7-170.5) | 153.6 (152.9-155.2) | +0.6% | 152.5, 161.1, 152.8 / 153.6, 154.1, 154 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 160.1 (157.7-162.2) | 160.1 (158.8-162) | +0.0% | 160.1, 160.6, 159.9 / 161.4, 160.1, 158.9 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 70.17 (69.91-70.22) | 64.9 (64.7-65.14) | -7.5% | 70.2, 70.04, 70.07 / 65.04, 64.79, 64.91 | consistent |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 1.348e+04 (1.303e+04-1.52e+04) | 1.433e+04 (1.402e+04-1.598e+04) | +6.3% | 1.429e+04, 1.33e+04, 1.348e+04 / 1.421e+04, 1.419e+04, 1.565e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 1.246e+04 (1.14e+04-1.358e+04) | 1.262e+04 (1.203e+04-1.347e+04) | +1.3% | 1.188e+04, 1.306e+04, 1.279e+04 / 1.279e+04, 1.262e+04, 1.275e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 2.517e+05 (2.438e+05-2.629e+05) | 2.597e+05 (2.506e+05-2.769e+05) | +3.1% | 2.573e+05, 2.485e+05, 2.481e+05 / 2.522e+05, 2.638e+05, 2.664e+05 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 2.346e+05 (2.335e+05-2.442e+05) | 2.362e+05 (2.329e+05-2.391e+05) | +0.7% | 2.397e+05, 2.336e+05, 2.383e+05 / 2.362e+05, 2.374e+05, 2.351e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 2.495e+04 (2.403e+04-2.648e+04) | 2.539e+04 (2.42e+04-2.816e+04) | +1.8% | 2.471e+04, 2.478e+04, 2.575e+04 / 2.691e+04, 2.452e+04, 2.575e+04 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 3303 (2842-3824) | 3491 (2787-4216) | +5.7% | 3467, 3333, 3303 / 3502, 3416, 3501 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 5.105e+05 (4.902e+05-5.231e+05) | 5.169e+05 (4.814e+05-5.403e+05) | +1.3% | 4.946e+05, 5.105e+05, 5.206e+05 / 4.897e+05, 5.309e+05, 5.169e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 5.874e+04 (5.049e+04-7.594e+04) | 6.005e+04 (5.469e+04-7.788e+04) | +2.2% | 6.031e+04, 5.485e+04, 6.711e+04 / 6.009e+04, 5.907e+04, 6.756e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 5622 (5600-5721) | 5613 (5582-5715) | -0.2% | 5624, 5622, 5661 / 5613, 5590, 5682 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 3364 (3194-3557) | 3300 (2994-4149) | -1.9% | 3315, 3400, 3397 / 3067, 3300, 3786 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 8.859e+04 (8.817e+04-8.909e+04) | 8.87e+04 (8.84e+04-8.974e+04) | +0.1% | 8.859e+04, 8.854e+04, 8.881e+04 / 8.919e+04, 8.885e+04, 8.858e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 6.392e+04 (5.649e+04-6.616e+04) | 5.601e+04 (5.397e+04-6.232e+04) | -12.4% | 6.49e+04, 6.439e+04, 6e+04 / 6.151e+04, 5.511e+04, 5.496e+04 | within noise |
| pool 26x26, 8 ch forward / numpy | 105.7 (105.3-107) | 106 (105.1-106.5) | +0.3% | 105.4, 105.8, 106.5 / 106.3, 105.6, 106 | within noise |
| pool 26x26, 8 ch forward / rust | 5.235 (5.199-5.287) | 5.225 (5.217-5.234) | -0.2% | 5.265, 5.255, 5.207 / 5.225, 5.226, 5.226 | within noise |
| pool 26x26, 8 ch downstream / numpy | 55.35 (54.83-56.88) | 55.14 (55.02-56.34) | -0.4% | 55.12, 55.17, 56.1 / 55.77, 55.11, 55.08 | within noise |
| pool 26x26, 8 ch downstream / rust | 4.145 (4.131-4.159) | 4.13 (4.114-4.155) | -0.4% | 4.141, 4.158, 4.137 / 4.121, 4.136, 4.134 | separated, inside spread |
| pool 26x26, 8 ch forward_batch b32 / numpy | 2432 (2408-2460) | 2397 (2374-2415) | -1.4% | 2429, 2434, 2432 / 2400, 2383, 2406 | consistent |
| pool 26x26, 8 ch forward_batch b32 / rust | 214 (203.3-229) | 230.8 (192.6-268) | +7.9% | 224.7, 218.1, 204.1 / 209.2, 255.6, 216.7 | within noise |
| pool 26x26, 8 ch forward_batch b512 / numpy | 4.01e+04 (3.935e+04-4.079e+04) | 4.017e+04 (3.918e+04-4.109e+04) | +0.2% | 4.035e+04, 4.007e+04, 4.01e+04 / 4.017e+04, 4.074e+04, 3.921e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 8474 (8182-9455) | 8861 (7507-9440) | +4.6% | 8753, 8819, 8474 / 9142, 8472, 8712 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 973.1 (952.6-1459) | 956.7 (943.7-1489) | -1.7% | 969.9, 966.1, 1213 / 951.2, 1236, 952.8 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / rust | 263.6 (129.9-472) | 293 (130-481.1) | +11.2% | 468.3, 130.2, 263.3 / 130.1, 473.9, 292.9 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 5.548e+04 (5.246e+04-6.502e+04) | 5.894e+04 (5.666e+04-6.525e+04) | +6.2% | 5.465e+04, 5.732e+04, 6.05e+04 / 5.911e+04, 5.779e+04, 6.211e+04 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / rust | 2.036e+04 (1.892e+04-2.283e+04) | 2.114e+04 (1.936e+04-2.26e+04) | +3.8% | 1.913e+04, 2.164e+04, 2.09e+04 / 2.136e+04, 2.024e+04, 2.189e+04 | within noise |
| pool 6x6, 8 ch forward / numpy | 39.73 (39.6-41.22) | 39.68 (39.11-39.94) | -0.1% | 39.84, 40.44, 39.73 / 39.79, 39.51, 39.6 | within noise |
| pool 6x6, 8 ch forward / rust | 0.7667 (0.7633-0.7698) | 0.7618 (0.7591-0.7636) | -0.6% | 0.7679, 0.7653, 0.7655 / 0.7623, 0.7612, 0.7608 | consistent, small |
| pool 6x6, 8 ch downstream / numpy | 32.53 (32.44-33.44) | 32.64 (32.24-32.71) | +0.3% | 32.49, 32.94, 32.92 / 32.38, 32.66, 32.69 | within noise |
| pool 6x6, 8 ch downstream / rust | 0.6631 (0.6599-0.6775) | 0.6366 (0.633-0.652) | -4.0% | 0.6601, 0.6636, 0.6702 / 0.643, 0.6374, 0.6345 | consistent |
| pool 6x6, 8 ch forward_batch b32 / numpy | 168.8 (167.7-170) | 169.1 (167.5-170.2) | +0.2% | 168.5, 168.8, 168.8 / 169.8, 168.8, 168.2 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 10.53 (10.47-10.59) | 10.47 (10.43-10.51) | -0.6% | 10.53, 10.5, 10.55 / 10.5, 10.44, 10.47 | separated, inside spread |
| pool 6x6, 8 ch forward_batch b512 / numpy | 2190 (2171-2220) | 2347 (2203-2536) | +7.1% | 2201, 2208, 2177 / 2354, 2497, 2205 | within noise |
| pool 6x6, 8 ch forward_batch b512 / rust | 166.2 (165.2-168.6) | 166 (163.1-170.3) | -0.1% | 165.9, 167.2, 166.6 / 167, 165.8, 166.4 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 85.15 (84.58-85.45) | 84.9 (84.74-87.36) | -0.3% | 84.68, 85.37, 85.15 / 86.14, 84.79, 85.36 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / rust | 7.857 (7.85-7.874) | 7.695 (7.679-7.717) | -2.1% | 7.857, 7.862, 7.859 / 7.695, 7.691, 7.698 | consistent |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 939.7 (933.9-947.5) | 939 (936.2-953.7) | -0.1% | 946.3, 936.2, 938.6 / 945, 938.9, 941.1 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 251.1 (129.1-451.7) | 126.7 (126.5-366.3) | -49.5% | 129.1, 252.5, 412.1 / 126.5, 126.7, 246.7 | within noise |
| conv tail 32 x 5408 bare downstream b32 / numpy | 1365 (1213-1522) | 1272 (911.6-1587) | -6.8% | 1368, 1406, 1347 / 1378, 1157, 1249 | within noise |
| conv tail 32 x 5408 bare downstream b32 / rust | 1297 (1146-1639) | 1407 (1218-1628) | +8.4% | 1495, 1417, 1155 / 1542, 1337, 1355 | within noise |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3.343e+04 (2.581e+04-4.546e+04) | 2.809e+04 (2.322e+04-3.415e+04) | -16.0% | 3.563e+04, 3.343e+04, 3.18e+04 / 2.982e+04, 2.846e+04, 2.731e+04 | separated, inside spread |
| conv tail 32 x 5408 bare downstream b512 / rust | 1.621e+04 (1.47e+04-2.433e+04) | 1.586e+04 (1.345e+04-2.632e+04) | -2.1% | 1.987e+04, 1.558e+04, 2.014e+04 / 2.029e+04, 1.841e+04, 1.423e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 1181 (1157-1603) | 1342 (1000-1508) | +13.7% | 1257, 1396, 1165 / 1390, 1331, 1173 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / rust | 1181 (1156-1189) | 1146 (1058-1348) | -3.0% | 1169, 1189, 1171 / 1222, 1195, 1146 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 2.238e+04 (2.169e+04-2.323e+04) | 2.226e+04 (2.139e+04-2.428e+04) | -0.5% | 2.267e+04, 2.277e+04, 2.204e+04 / 2.337e+04, 2.241e+04, 2.173e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / rust | 1.893e+04 (1.777e+04-1.993e+04) | 2.002e+04 (1.972e+04-2.067e+04) | +5.8% | 1.865e+04, 1.94e+04, 1.838e+04 / 2.016e+04, 2.038e+04, 1.984e+04 | separated, inside spread |
| conv tail 32 x 5408 transpose b32 / numpy | 1.461 (1.451-1.762) | 1.46 (1.454-1.469) | -0.1% | 1.61, 1.459, 1.458 / 1.46, 1.46, 1.463 | within noise |
| conv tail 32 x 5408 transpose b32 / rust | 0.8038 (0.7965-0.8073) | 0.7943 (0.7915-0.8133) | -1.2% | 0.8013, 0.8019, 0.8058 / 0.7939, 0.8098, 0.7931 | within noise |
| conv tail 32 x 5408 transpose b512 / numpy | 29.9 (29.54-30.06) | 29.94 (29.78-30.1) | +0.1% | 29.89, 29.67, 30.03 / 29.94, 30.07, 29.81 | within noise |
| conv tail 32 x 5408 transpose b512 / rust | 11.51 (11.3-11.61) | 11.33 (11.18-11.78) | -1.6% | 11.58, 11.46, 11.45 / 11.51, 11.32, 11.42 | within noise |
| conv tail 32 x 5408 add b32 / numpy | 319.5 (303.6-351.4) | 337.6 (334-406.5) | +5.7% | 326.3, 331.9, 319.5 / 370.3, 334.1, 363.4 | separated, inside spread |
| conv tail 32 x 5408 add b32 / rust | 333.8 (311-427.5) | 334.2 (303-441.8) | +0.1% | 380.5, 314.9, 372 / 355.3, 389.2, 308.7 | within noise |
| conv tail 32 x 5408 add b512 / numpy | 412.4 (317.8-428.9) | 314.9 (300.2-431.3) | -23.6% | 368.5, 411.8, 412.4 / 307.5, 342.4, 374.7 | within noise |
| conv tail 32 x 5408 add b512 / rust | 400.8 (275.6-432.6) | 345.5 (253.3-460.4) | -13.8% | 423.4, 349.1, 354.1 / 345.5, 442.6, 272.9 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 2.826 (2.796-2.867) | 2.829 (2.807-2.948) | +0.1% | 2.831, 2.826, 2.835 / 2.829, 2.852, 2.879 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.7804 (0.7767-0.7868) | 0.785 (0.7828-0.7891) | +0.6% | 0.7781, 0.7824, 0.7816 / 0.7861, 0.786, 0.7847 | separated, inside spread |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 15.91 (15.83-16.2) | 16.08 (15.8-16.19) | +1.0% | 15.91, 15.83, 16.1 / 15.99, 16.08, 16.04 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 8.693 (8.664-8.721) | 8.783 (8.775-8.791) | +1.0% | 8.687, 8.713, 8.678 / 8.786, 8.783, 8.781 | consistent |
| dense 30 x 784 bare downstream b32 / numpy | 57.66 (57.32-58.18) | 57.41 (56.7-58.13) | -0.4% | 57.69, 58, 57.5 / 57.41, 57.4, 57.42 | separated, inside spread |
| dense 30 x 784 bare downstream b32 / rust | 126.3 (125.7-127.5) | 125.1 (122.9-125.6) | -0.9% | 125.8, 126.2, 127.2 / 124, 125.3, 124.5 | separated, inside spread |
| dense 30 x 784 bare downstream b512 / numpy | 3570 (3270-3997) | 3573 (2430-3945) | +0.1% | 3702, 3327, 3847 / 3573, 3903, 2584 | within noise |
| dense 30 x 784 bare downstream b512 / rust | 1718 (1518-2475) | 2377 (1656-2544) | +38.4% | 1654, 2061, 1718 / 2100, 2511, 2069 | separated, inside spread |
| dense 30 x 784 bare accumulate b32 / numpy | 234 (65.55-403.4) | 66.67 (65.56-400.7) | -71.5% | 233.9, 66.06, 403.1 / 66.19, 67.09, 233.6 | within noise |
| dense 30 x 784 bare accumulate b32 / rust | 125.2 (124.8-126.7) | 125.7 (125.5-125.8) | +0.4% | 124.8, 125.8, 125.6 / 125.7, 125.7, 125.6 | within noise |
| dense 30 x 784 bare accumulate b512 / numpy | 1650 (1601-1831) | 1740 (1479-1966) | +5.4% | 1625, 1738, 1717 / 1747, 1842, 1621 | within noise |
| dense 30 x 784 bare accumulate b512 / rust | 2518 (2013-2587) | 2264 (1997-2632) | -10.1% | 2029, 2572, 2518 / 2037, 2558, 2239 | within noise |
| dense 30 x 784 transpose b32 / numpy | 1.412 (1.396-1.423) | 1.404 (1.395-1.418) | -0.6% | 1.412, 1.409, 1.414 / 1.413, 1.404, 1.397 | within noise |
| dense 30 x 784 transpose b32 / rust | 0.8273 (0.82-0.8341) | 0.8169 (0.8125-0.8224) | -1.3% | 0.8271, 0.8253, 0.8273 / 0.8143, 0.818, 0.8201 | separated, inside spread |
| dense 30 x 784 transpose b512 / numpy | 8.994 (8.97-9.029) | 9.015 (8.988-9.054) | +0.2% | 8.994, 9.023, 8.97 / 9.002, 9.01, 9.039 | within noise |
| dense 30 x 784 transpose b512 / rust | 10.41 (10.07-10.97) | 10.68 (10.07-10.87) | +2.5% | 10.52, 10.57, 10.37 / 10.78, 10.68, 10.11 | within noise |
| dense 30 x 784 add b32 / numpy | 10.17 (9.939-10.53) | 10.24 (9.976-10.41) | +0.8% | 10.09, 10.31, 10.22 / 10.13, 10.38, 10.19 | within noise |
| dense 30 x 784 add b32 / rust | 9.992 (9.601-11.34) | 9.543 (9.412-9.644) | -4.5% | 10.58, 9.882, 10.12 / 9.486, 9.607, 9.5 | separated, inside spread |
| dense 30 x 784 add b512 / numpy | 11.43 (11.21-11.59) | 11.27 (11.02-11.72) | -1.3% | 11.4, 11.37, 11.43 / 11.45, 11.52, 11.09 | within noise |
| dense 30 x 784 add b512 / rust | 9.609 (9.355-9.782) | 9.601 (9.429-9.844) | -0.1% | 9.612, 9.76, 9.412 / 9.584, 9.636, 9.68 | within noise |
| dense 30 x 784 sum_axis0 b32 / numpy | 2.8 (2.791-2.805) | 2.807 (2.795-2.842) | +0.2% | 2.805, 2.8, 2.791 / 2.815, 2.824, 2.802 | within noise |
| dense 30 x 784 sum_axis0 b32 / rust | 0.7097 (0.7014-0.7117) | 0.707 (0.7054-0.7144) | -0.4% | 0.711, 0.7097, 0.7018 / 0.7108, 0.7061, 0.7075 | within noise |
| dense 30 x 784 sum_axis0 b512 / numpy | 15.42 (15.33-15.73) | 15.35 (15.32-15.8) | -0.5% | 15.71, 15.37, 15.42 / 15.33, 15.58, 15.52 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 7.438 (7.418-7.63) | 7.512 (7.505-7.668) | +1.0% | 7.439, 7.421, 7.536 / 7.515, 7.512, 7.587 | within noise |
| dense 10 x 30 bare downstream b32 / numpy | 5.864 (5.838-7.7) | 5.88 (5.854-5.941) | +0.3% | 6.769, 5.864, 5.897 / 5.869, 5.898, 5.903 | within noise |
| dense 10 x 30 bare downstream b32 / rust | 3.709 (3.703-3.729) | 4.263 (4.258-4.268) | +14.9% | 3.711, 3.707, 3.718 / 4.264, 4.26, 4.265 | consistent |
| dense 10 x 30 bare downstream b512 / numpy | 64.71 (64.49-64.79) | 64.67 (64.45-64.74) | -0.1% | 64.76, 64.72, 64.54 / 64.47, 64.7, 64.69 | within noise |
| dense 10 x 30 bare downstream b512 / rust | 54.49 (54.24-54.75) | 70.01 (69.75-70.51) | +28.5% | 54.61, 54.36, 54.61 / 70.06, 69.86, 70.15 | consistent |
| dense 10 x 30 bare accumulate b32 / numpy | 5.04 (5.02-5.075) | 5.048 (5.035-5.062) | +0.2% | 5.053, 5.049, 5.024 / 5.053, 5.052, 5.04 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 3.256 (3.25-3.262) | 3.26 (3.257-3.271) | +0.1% | 3.252, 3.256, 3.261 / 3.259, 3.266, 3.259 | within noise |
| dense 10 x 30 bare accumulate b512 / numpy | 32.54 (32.4-32.61) | 32.64 (32.58-32.79) | +0.3% | 32.54, 32.54, 32.51 / 32.7, 32.72, 32.61 | separated, inside spread |
| dense 10 x 30 bare accumulate b512 / rust | 45.34 (45.3-45.4) | 45.34 (45.3-45.38) | -0.0% | 45.31, 45.38, 45.36 / 45.35, 45.34, 45.32 | within noise |
| dense 10 x 30 transpose b32 / numpy | 0.8873 (0.8851-0.9677) | 0.8916 (0.8814-0.8997) | +0.5% | 0.8873, 0.8907, 0.9264 / 0.8991, 0.8909, 0.8867 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.5049 (0.4959-0.5094) | 0.4991 (0.4931-0.5017) | -1.1% | 0.5012, 0.4997, 0.5092 / 0.4974, 0.4983, 0.4991 | separated, inside spread |
| dense 10 x 30 transpose b512 / numpy | 3.388 (3.363-3.563) | 3.368 (3.353-3.527) | -0.6% | 3.398, 3.366, 3.474 / 3.44, 3.4, 3.364 | within noise |
| dense 10 x 30 transpose b512 / rust | 3.79 (3.767-3.906) | 3.782 (3.764-3.896) | -0.2% | 3.836, 3.835, 3.79 / 3.804, 3.838, 3.77 | within noise |
| dense 10 x 30 add b32 / numpy | 0.8893 (0.8854-0.9106) | 0.8986 (0.8963-0.9223) | +1.0% | 0.8932, 0.9012, 0.886 / 0.8986, 0.9094, 0.9001 | within noise |
| dense 10 x 30 add b32 / rust | 0.3848 (0.3833-0.3901) | 0.3856 (0.3828-0.3912) | +0.2% | 0.3847, 0.3868, 0.3867 / 0.3878, 0.3879, 0.3836 | within noise |
| dense 10 x 30 add b512 / numpy | 0.9184 (0.9079-0.9328) | 0.9239 (0.9192-0.9686) | +0.6% | 0.9144, 0.9244, 0.9183 / 0.9239, 0.9555, 0.92 | within noise |
| dense 10 x 30 add b512 / rust | 0.4072 (0.4055-0.4091) | 0.4089 (0.4036-0.4121) | +0.4% | 0.4087, 0.4072, 0.4058 / 0.4103, 0.4078, 0.4069 | within noise |
| dense 10 x 30 sum_axis0 b32 / numpy | 2.464 (2.45-2.478) | 2.463 (2.439-2.519) | -0.0% | 2.463, 2.466, 2.464 / 2.446, 2.497, 2.461 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.5312 (0.5259-0.535) | 0.5478 (0.5448-0.5492) | +3.1% | 0.5291, 0.5325, 0.5303 / 0.5477, 0.5464, 0.5484 | consistent |
| dense 10 x 30 sum_axis0 b512 / numpy | 12.18 (12.16-12.61) | 12.17 (12.16-12.24) | -0.1% | 12.4, 12.18, 12.16 / 12.19, 12.17, 12.2 | within noise |
| dense 10 x 30 sum_axis0 b512 / rust | 4.647 (4.641-4.65) | 4.965 (4.958-4.97) | +6.8% | 4.645, 4.647, 4.649 / 4.966, 4.967, 4.962 | consistent |
| attention 16 x 32 forward_batch b32 / numpy | 750.5 (745.8-1641) | 747.3 (743.1-756.2) | -0.4% | 752, 1197, 746.6 / 756, 746.8, 745.3 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 800.6 (799.6-803.7) | 750.5 (749.9-752.8) | -6.3% | 800.7, 799.6, 802.4 / 750.7, 750.1, 751.8 | consistent |
| attention 16 x 32 forward_batch b512 / numpy | 2.31e+04 (2.23e+04-2.377e+04) | 2.269e+04 (2.001e+04-2.438e+04) | -1.8% | 2.285e+04, 2.314e+04, 2.328e+04 / 2.269e+04, 2.077e+04, 2.392e+04 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 1.727e+04 (1.673e+04-1.836e+04) | 1.559e+04 (1.526e+04-1.67e+04) | -9.7% | 1.727e+04, 1.727e+04, 1.754e+04 / 1.668e+04, 1.538e+04, 1.547e+04 | separated, inside spread |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 758.3 (753.6-777.4) | 760.7 (756.4-765.9) | +0.3% | 754.3, 758.3, 769.7 / 763.5, 760.1, 759.1 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / rust | 758.5 (757-763.8) | 750.7 (746.8-755.1) | -1.0% | 758.3, 757.8, 761.1 / 750.2, 753.1, 750.9 | consistent |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 2.771e+04 (2.71e+04-2.874e+04) | 2.758e+04 (2.527e+04-2.83e+04) | -0.5% | 2.823e+04, 2.722e+04, 2.793e+04 / 2.747e+04, 2.645e+04, 2.821e+04 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / rust | 1.989e+04 (1.847e+04-2.096e+04) | 1.891e+04 (1.841e+04-2.059e+04) | -4.9% | 1.971e+04, 1.931e+04, 2.002e+04 / 2.032e+04, 1.891e+04, 1.844e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 591.1 (580.6-2101) | 591.2 (590.4-2115) | +0.0% | 588.5, 591.1, 1341 / 591.2, 1353, 1348 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 462.1 (449.9-465.6) | 459.8 (446.6-462.8) | -0.5% | 457.5, 463.5, 461.4 / 454.3, 453.9, 460.9 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 4.145e+04 (3.432e+04-4.398e+04) | 4.162e+04 (3.259e+04-4.472e+04) | +0.4% | 4.145e+04, 4.039e+04, 3.894e+04 / 3.997e+04, 3.665e+04, 4.262e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 3.431e+04 (2.817e+04-3.743e+04) | 3.066e+04 (2.453e+04-3.784e+04) | -10.6% | 3.54e+04, 3.212e+04, 3.203e+04 / 3.064e+04, 3.69e+04, 2.511e+04 | within noise |
