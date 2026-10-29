Old `6dcd34c` against new `6dcd34c`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `10dfec9` (extension sha256 `7d70efbe6dbd`) and new crate `13fe89a` (extension sha256 `8223780c5791`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.69 (measured just after this run's crate builds); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / dense 10 x 30 forward_batch b512 / rust +37.3% (59.62 -> 81.85 µs)
- consistent: per call / dense 10 x 30 forward_batch b32 / rust +34.7% (4.049 -> 5.456 µs)
- consistent: per call / pool 6x6, 8 ch downstream_batch b512 / rust -32.3% (178.5 -> 120.9 µs)
- consistent: per call / pool 6x6, 8 ch downstream_batch b32 / rust -32.3% (11.3 -> 7.658 µs)
- consistent: per call / pool 6x6, 8 ch downstream / rust -22.7% (0.5728 -> 0.4429 µs)
- consistent: per call / dense 30 x 784 forward_batch b512 / rust +21.5% (363.5 -> 441.5 µs)
- consistent: per call / pool 26x26, 8 ch downstream / rust -18.1% (5.119 -> 4.194 µs)
- consistent: per call / dense 10 x 30 sum_axis0 b512 / rust +17.4% (2.565 -> 3.012 µs)
- consistent: per call / pool 26x26, 8 ch downstream_batch b32 / rust -17.0% (159.5 -> 132.4 µs)
- consistent: per call / attention 16 x 32 forward_batch b32 / rust +15.6% (364.1 -> 420.8 µs)
- ... 27 more consistent rows (report --md)
- 233 rows within noise (52 separated inside their spread), max |Δ| 14.1%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 27.14 (27.07-30.07) | 27.83 (27.55-28.64) | +2.5% | 27.1, 28.62, 27.13 / 28.24, 27.68, 28.08 | within noise |
| conv tail 32 x 5408 forward / rust | 19.12 (18.94-22.64) | 20.15 (19.32-22.94) | +5.4% | 19.07, 19.2, 20.79 / 21.11, 21.93, 19.34 | within noise |
| conv tail 32 x 5408 downstream / numpy | 23.5 (23.44-26.01) | 23.58 (23.47-24.46) | +0.3% | 23.47, 24.77, 23.49 / 23.92, 23.58, 23.96 | within noise |
| conv tail 32 x 5408 downstream / rust | 20.8 (20.62-23.65) | 20.7 (20.5-20.73) | -0.5% | 20.72, 22.21, 20.79 / 20.59, 20.7, 20.73 | within noise |
| conv tail 32 x 5408 hidden_delta / numpy | 31.43 (31.18-34.09) | 31.29 (31.16-31.32) | -0.4% | 32.81, 32.5, 31.33 / 31.22, 31.29, 31.31 | separated, inside spread |
| conv tail 32 x 5408 hidden_delta / rust | 22.89 (22.87-25.88) | 23.1 (22.92-25.78) | +0.9% | 22.89, 24.37, 23.02 / 24.44, 23.06, 23.01 | within noise |
| conv tail 32 x 5408 accumulate_gradient / numpy | 88.3 (87.96-93.99) | 85.56 (85.16-93.75) | -3.1% | 88.13, 91.21, 90.96 / 85.52, 85.32, 89.7 | within noise |
| conv tail 32 x 5408 accumulate_gradient / rust | 53.62 (52.85-56.08) | 53.89 (53.27-55.8) | +0.5% | 53.06, 54.79, 53.88 / 54.62, 53.58, 54.68 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 177.5 (177.3-184.2) | 176.8 (176.6-177.8) | -0.4% | 177.5, 180.8, 177.5 / 176.9, 176.7, 177.2 | separated, inside spread |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 107.9 (106.7-113.1) | 108.3 (106.2-112.8) | +0.4% | 107.9, 111.6, 106.9 / 108.3, 108.6, 109.8 | within noise |
| conv tail 32 x 5408 sgd step / numpy | 264.1 (262.9-275.5) | 265.1 (263.8-271.5) | +0.4% | 263.2, 270.1, 266.2 / 266, 265, 268 | within noise |
| conv tail 32 x 5408 sgd step / rust | 59.74 (59.08-61.34) | 59.92 (59.13-60.36) | +0.3% | 59.63, 60.21, 59.88 / 59.79, 59.99, 59.74 | within noise |
| conv tail 32 x 5408 forward_batch b32 / numpy | 156.9 (145.4-158.3) | 156.1 (151.9-158.2) | -0.5% | 146, 158.1, 156.9 / 153.7, 157, 156.8 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 344.9 (343-379) | 359.7 (345.7-364.9) | +4.3% | 343.2, 361.8, 349 / 361.3, 356.5, 352.3 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1163 (1140-1166) | 1167 (1165-1177) | +0.4% | 1153, 1164, 1163 / 1167, 1167, 1171 | separated, inside spread |
| conv tail 32 x 5408 forward_batch b512 / rust | 1883 (1799-1905) | 1947 (1941-1975) | +3.4% | 1841, 1892, 1891 / 1943, 1958, 1957 | separated, inside spread |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 79.36 (78.91-79.53) | 79.63 (78.92-79.94) | +0.3% | 79.13, 79.46, 79.43 / 79.31, 79.92, 79.55 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 247.6 (242.6-256.5) | 249 (245.3-255.5) | +0.6% | 244.3, 254.7, 247.6 / 250.4, 249, 248.6 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3081 (3065-3092) | 3099 (3081-3113) | +0.6% | 3080, 3081, 3078 / 3107, 3093, 3094 | separated, inside spread |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2394 (2390-2401) | 2435 (2289-2444) | +1.7% | 2395, 2394, 2396 / 2435, 2436, 2365 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 622.7 (616.2-631.7) | 621.9 (613.1-632.8) | -0.1% | 620.9, 619.4, 627.5 / 624, 626.9, 617 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 321.9 (318.6-328) | 313.4 (307.6-322.7) | -2.6% | 320.3, 323.8, 322.1 / 310.1, 313.1, 320.5 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 1.216e+04 (1.207e+04-1.23e+04) | 1.226e+04 (1.218e+04-1.242e+04) | +0.9% | 1.213e+04, 1.219e+04, 1.222e+04 / 1.22e+04, 1.231e+04, 1.231e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 5909 (5895-6010) | 5815 (5790-5918) | -1.6% | 5931, 5957, 5909 / 5854, 5792, 5863 | separated, inside spread |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 163.9 (160.7-167.2) | 165.3 (163.8-168.3) | +0.9% | 163.8, 165.8, 162 / 165.3, 167, 164.2 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 280 (276.1-286) | 285.1 (278.5-291.4) | +1.8% | 281.7, 276.9, 282.5 / 278.6, 286.7, 288.2 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 1838 (1791-1885) | 1862 (1834-1878) | +1.3% | 1845, 1806, 1864 / 1856, 1863, 1849 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 2351 (2332-2390) | 2386 (2341-2396) | +1.5% | 2353, 2344, 2369 / 2385, 2368, 2388 | within noise |
| dense 30 x 784 forward / numpy | 8.016 (7.939-8.14) | 8.504 (7.933-8.711) | +6.1% | 8.013, 8.033, 8.04 / 8.283, 8.322, 8.515 | consistent |
| dense 30 x 784 forward / rust | 2.715 (2.649-2.837) | 2.963 (2.876-3.03) | +9.1% | 2.7, 2.684, 2.812 / 2.911, 2.943, 3.007 | separated, inside spread |
| dense 30 x 784 downstream / numpy | 3.967 (3.896-4.083) | 3.919 (3.843-4.154) | -1.2% | 3.989, 3.967, 3.985 / 3.894, 3.998, 3.919 | within noise |
| dense 30 x 784 downstream / rust | 2.165 (2.109-2.189) | 2.076 (1.978-2.253) | -4.1% | 2.157, 2.176, 2.143 / 2.093, 2.036, 2.145 | within noise |
| dense 30 x 784 hidden_delta / numpy | 6.768 (6.67-7.253) | 6.812 (6.657-7.13) | +0.7% | 7.215, 6.765, 6.713 / 6.815, 6.894, 6.812 | within noise |
| dense 30 x 784 hidden_delta / rust | 2.671 (2.566-2.838) | 2.739 (2.571-3.04) | +2.6% | 2.74, 2.702, 2.663 / 2.633, 2.806, 2.808 | within noise |
| dense 30 x 784 accumulate_gradient / numpy | 28.08 (27.44-28.38) | 27.87 (27.46-28.76) | -0.8% | 27.96, 27.68, 28.31 / 27.69, 28.11, 28.09 | within noise |
| dense 30 x 784 accumulate_gradient / rust | 6.979 (6.805-7.17) | 7.126 (6.857-7.169) | +2.1% | 6.949, 6.926, 7.089 / 6.996, 7.128, 7.126 | within noise |
| dense 30 x 784 apply_accumulated_gradient / numpy | 31.34 (30.89-32.46) | 31.49 (30.93-32.57) | +0.5% | 32.06, 30.96, 31.44 / 32.04, 31.64, 31.23 | within noise |
| dense 30 x 784 apply_accumulated_gradient / rust | 16.81 (16.49-17.64) | 16.68 (16.52-17.24) | -0.8% | 17.12, 17.06, 16.59 / 16.62, 16.95, 16.78 | within noise |
| dense 30 x 784 sgd step / numpy | 61.13 (59.25-62.25) | 59.53 (59.05-60.21) | -2.6% | 61.95, 60.71, 59.93 / 60, 59.16, 59.72 | within noise |
| dense 30 x 784 sgd step / rust | 7.426 (7.302-7.676) | 7.465 (7.192-7.882) | +0.5% | 7.397, 7.557, 7.396 / 7.512, 7.465, 7.663 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 38.14 (37.58-38.62) | 38.39 (38.04-39.37) | +0.6% | 38.24, 37.9, 38.1 / 38.39, 39.08, 38.14 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 50.1 (49.51-51.15) | 55.48 (54.92-56.4) | +10.7% | 49.56, 50.65, 50.3 / 55.81, 55.17, 55.72 | consistent |
| dense 30 x 784 forward_batch b512 / numpy | 267 (227.4-269.2) | 267.3 (265.4-270) | +0.1% | 246.5, 268.4, 267.4 / 266.2, 268.8, 267.9 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 363.5 (356.1-366.9) | 441.5 (435.5-444.3) | +21.5% | 359.2, 363.5, 365.8 / 438.6, 439.1, 443 | consistent |
| dense 30 x 784 downstream_batch b32 / numpy | 23.98 (23.85-24.34) | 24.01 (23.51-24.65) | +0.1% | 24.19, 23.86, 24.1 / 24.01, 24.07, 24.08 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 31.9 (31.66-32.72) | 33.02 (32.7-33.42) | +3.5% | 32.04, 31.79, 32.31 / 33.02, 33.12, 33.06 | consistent |
| dense 30 x 784 downstream_batch b512 / numpy | 130.9 (129.8-131.8) | 131 (130.2-132.2) | +0.1% | 130.4, 131.3, 130.9 / 130.5, 131.8, 131 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 242.3 (238.5-244.2) | 245.2 (242.3-249.2) | +1.2% | 240.1, 243.1, 242.6 / 246.5, 243.9, 246.7 | separated, inside spread |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 62.26 (61.71-64.22) | 62.98 (61.64-64.85) | +1.2% | 62.93, 63.44, 61.79 / 62.98, 62.9, 63.44 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / rust | 42.88 (41.44-43.81) | 44.36 (43.35-45.01) | +3.5% | 42.09, 42.92, 43.17 / 44.36, 43.91, 44.32 | separated, inside spread |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 1713 (1693-1722) | 1720 (1702-1733) | +0.4% | 1705, 1705, 1721 / 1712, 1723, 1722 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / rust | 498.2 (490.6-516.7) | 500 (496.2-509.8) | +0.4% | 506.5, 494.2, 499.7 / 500, 502.7, 503 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 41.01 (39.84-42.02) | 40.01 (39.23-41.04) | -2.4% | 40.93, 41.07, 40.63 / 40.44, 39.55, 40.13 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 38.88 (36.97-39.13) | 40.71 (40.08-41.32) | +4.7% | 37.88, 39.02, 38.95 / 40.23, 41.21, 40.69 | consistent |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 224 (221.8-226.2) | 222.5 (220.6-223.8) | -0.6% | 222.8, 224.6, 224.1 / 222.1, 223.1, 221.7 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 310.8 (308.5-315.1) | 318.7 (309.2-323.7) | +2.6% | 312.8, 312, 309.4 / 317, 315.4, 320.5 | separated, inside spread |
| dense 10 x 30 forward / numpy | 4.538 (4.441-4.57) | 4.519 (4.408-4.649) | -0.4% | 4.521, 4.506, 4.538 / 4.506, 4.472, 4.58 | within noise |
| dense 10 x 30 forward / rust | 0.3466 (0.3362-0.3524) | 0.3875 (0.3755-0.4032) | +11.8% | 0.3395, 0.3482, 0.3499 / 0.3827, 0.3977, 0.3834 | consistent |
| dense 10 x 30 downstream / numpy | 0.8294 (0.8097-0.8462) | 0.8458 (0.8294-0.8585) | +2.0% | 0.8178, 0.8343, 0.8348 / 0.8439, 0.8569, 0.8357 | separated, inside spread |
| dense 10 x 30 downstream / rust | 0.2012 (0.1945-0.2095) | 0.203 (0.1994-0.2081) | +0.9% | 0.198, 0.2007, 0.2082 / 0.2015, 0.2056, 0.2025 | within noise |
| dense 10 x 30 hidden_delta / numpy | 2.245 (2.216-2.336) | 2.251 (2.198-2.314) | +0.3% | 2.22, 2.245, 2.332 / 2.211, 2.277, 2.272 | within noise |
| dense 10 x 30 hidden_delta / rust | 0.4293 (0.4211-0.4449) | 0.4329 (0.4279-0.4412) | +0.8% | 0.426, 0.4299, 0.4362 / 0.4326, 0.4369, 0.4306 | within noise |
| dense 10 x 30 accumulate_gradient / numpy | 2.835 (2.756-2.861) | 2.928 (2.884-2.991) | +3.3% | 2.796, 2.84, 2.846 / 2.958, 2.938, 2.908 | consistent |
| dense 10 x 30 accumulate_gradient / rust | 0.43 (0.4151-0.4403) | 0.4032 (0.3948-0.4266) | -6.2% | 0.4339, 0.4233, 0.4277 / 0.4124, 0.4032, 0.4001 | separated, inside spread |
| dense 10 x 30 apply_accumulated_gradient / numpy | 4.632 (4.409-4.838) | 4.669 (4.512-4.758) | +0.8% | 4.458, 4.663, 4.72 / 4.573, 4.726, 4.698 | within noise |
| dense 10 x 30 apply_accumulated_gradient / rust | 2.241 (2.178-2.42) | 2.227 (2.205-2.252) | -0.6% | 2.243, 2.314, 2.232 / 2.227, 2.227, 2.228 | separated, inside spread |
| dense 10 x 30 sgd step / numpy | 8.341 (8.224-8.505) | 8.445 (8.174-8.915) | +1.2% | 8.33, 8.341, 8.381 / 8.353, 8.711, 8.348 | within noise |
| dense 10 x 30 sgd step / rust | 0.468 (0.4524-0.4965) | 0.4713 (0.4619-0.4865) | +0.7% | 0.4612, 0.4636, 0.4852 / 0.4713, 0.4742, 0.4723 | within noise |
| dense 10 x 30 forward_batch b32 / numpy | 9.734 (9.531-10.56) | 9.801 (9.578-9.894) | +0.7% | 10.05, 9.821, 9.705 / 9.688, 9.796, 9.863 | within noise |
| dense 10 x 30 forward_batch b32 / rust | 4.049 (3.975-4.154) | 5.456 (5.383-5.698) | +34.7% | 4, 4.091, 4.085 / 5.422, 5.541, 5.501 | consistent |
| dense 10 x 30 forward_batch b512 / numpy | 54.54 (53.26-55.4) | 54.32 (53.89-55.45) | -0.4% | 53.85, 54.51, 55.03 / 53.9, 54.46, 54.89 | within noise |
| dense 10 x 30 forward_batch b512 / rust | 59.62 (58.01-59.86) | 81.85 (80.59-82.16) | +37.3% | 58.23, 59.62, 59.83 / 82.05, 81.32, 81.33 | consistent |
| dense 10 x 30 downstream_batch b32 / numpy | 1.816 (1.795-1.877) | 1.794 (1.733-1.832) | -1.2% | 1.838, 1.805, 1.839 / 1.762, 1.815, 1.788 | within noise |
| dense 10 x 30 downstream_batch b32 / rust | 1.161 (1.123-1.231) | 1.182 (1.159-1.234) | +1.9% | 1.14, 1.187, 1.174 / 1.182, 1.182, 1.197 | within noise |
| dense 10 x 30 downstream_batch b512 / numpy | 12.29 (12.04-12.62) | 12.32 (12.18-12.48) | +0.3% | 12.27, 12.37, 12.29 / 12.25, 12.32, 12.43 | within noise |
| dense 10 x 30 downstream_batch b512 / rust | 15.54 (14.91-16.21) | 15.75 (15.41-16) | +1.3% | 15.17, 15.87, 15.84 / 15.82, 15.64, 15.79 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 4.889 (4.816-4.977) | 4.908 (4.87-5.01) | +0.4% | 4.854, 4.924, 4.923 / 4.89, 4.941, 4.928 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 1.728 (1.674-1.76) | 1.784 (1.756-1.809) | +3.2% | 1.7, 1.715, 1.757 / 1.784, 1.78, 1.792 | separated, inside spread |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 35.19 (34.76-36.26) | 34.87 (34.75-36.37) | -0.9% | 35.15, 35.55, 35.23 / 35.57, 34.83, 35.11 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / rust | 22.87 (21.99-23.15) | 23.13 (22.36-23.44) | +1.2% | 22.29, 22.94, 23.02 / 22.99, 22.82, 23.15 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 4.505 (4.459-4.829) | 4.499 (4.364-4.654) | -0.1% | 4.644, 4.54, 4.502 / 4.431, 4.466, 4.577 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 1.97 (1.951-1.995) | 1.98 (1.957-2.002) | +0.5% | 1.952, 1.99, 1.974 / 1.964, 1.98, 1.996 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 24.71 (24.45-24.86) | 24.81 (24.49-25.23) | +0.4% | 24.57, 24.63, 24.79 / 24.61, 24.9, 24.87 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 32.71 (32.27-33.53) | 33.47 (33.1-35.06) | +2.3% | 33.07, 33.13, 32.41 / 34.36, 33.47, 33.22 | separated, inside spread |
| conv 28x28, 8 ch forward / numpy | 55.69 (54.32-56.98) | 55 (54.37-55.58) | -1.3% | 55.65, 55.4, 55.69 / 55.06, 55.09, 54.89 | consistent, small |
| conv 28x28, 8 ch forward / rust | 18.84 (18.52-19.25) | 18.75 (18.27-19.06) | -0.5% | 18.72, 18.84, 19.01 / 18.28, 18.75, 19.03 | within noise |
| conv 28x28, 8 ch downstream / numpy | 38.8 (37.82-40.95) | 38.98 (38.4-40.23) | +0.5% | 38.53, 38.22, 40.21 / 39.57, 39.02, 38.73 | within noise |
| conv 28x28, 8 ch downstream / rust | 17.42 (16.82-17.9) | 17.57 (17.23-17.88) | +0.9% | 17.06, 17.4, 17.72 / 17.27, 17.67, 17.72 | within noise |
| conv 28x28, 8 ch accumulate_gradient / numpy | 36.37 (34.74-37.36) | 35.93 (35.65-36.33) | -1.2% | 35.21, 36.28, 37.21 / 35.74, 36.29, 35.86 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 16.05 (15.98-16.11) | 15.74 (15.65-16.37) | -1.9% | 16.08, 16.06, 16.01 / 16.06, 15.66, 15.74 | within noise |
| conv 28x28, 8 ch forward_batch b32 / numpy | 980.3 (965-992) | 982.7 (976.9-993.3) | +0.2% | 978.5, 981.8, 980.3 / 980.6, 984.8, 987.1 | within noise |
| conv 28x28, 8 ch forward_batch b32 / rust | 567.3 (545.6-590.5) | 549.8 (539.5-562.3) | -3.1% | 556.1, 577, 579.2 / 543.1, 549.4, 557.6 | within noise |
| conv 28x28, 8 ch forward_batch b512 / numpy | 1.85e+04 (1.835e+04-1.868e+04) | 1.838e+04 (1.812e+04-1.855e+04) | -0.7% | 1.842e+04, 1.86e+04, 1.849e+04 / 1.84e+04, 1.834e+04, 1.833e+04 | separated, inside spread |
| conv 28x28, 8 ch forward_batch b512 / rust | 9243 (8976-9494) | 9190 (8939-9276) | -0.6% | 9074, 9234, 9490 / 9051, 9179, 9247 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 579.3 (577.4-614.2) | 614.9 (579-616.8) | +6.2% | 590.8, 596.6, 578.2 / 615.7, 597.1, 597.6 | separated, inside spread |
| conv 28x28, 8 ch downstream_batch b32 / rust | 507.3 (501-522.1) | 503.6 (495.7-513.5) | -0.7% | 501.3, 507.1, 518 / 499.8, 513.4, 500.9 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 1.621e+04 (1.596e+04-1.631e+04) | 1.628e+04 (1.591e+04-1.653e+04) | +0.4% | 1.623e+04, 1.628e+04, 1.598e+04 / 1.643e+04, 1.621e+04, 1.62e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / rust | 1435 (1422-1439) | 1428 (1425-1438) | -0.5% | 1436, 1437, 1429 / 1426, 1433, 1429 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 1300 (1290-1336) | 1223 (1214-1225) | -6.0% | 1295, 1333, 1298 / 1224, 1216, 1223 | consistent |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 531.6 (529.6-537.6) | 521.4 (521-528.4) | -1.9% | 533.6, 531.8, 531.5 / 524.9, 521.2, 522.6 | consistent, small |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 2.044e+04 (1.978e+04-2.166e+04) | 2.02e+04 (2.004e+04-2.035e+04) | -1.1% | 2.072e+04, 2.044e+04, 2.039e+04 / 2.013e+04, 2.033e+04, 2.017e+04 | separated, inside spread |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 1.162e+04 (1.159e+04-1.19e+04) | 1.15e+04 (1.147e+04-1.152e+04) | -1.0% | 1.178e+04, 1.161e+04, 1.161e+04 / 1.15e+04, 1.149e+04, 1.151e+04 | separated, inside spread |
| conv 8x8, 8 ch forward / numpy | 28.43 (27.69-28.87) | 28.59 (28.13-29.18) | +0.6% | 28.25, 28.1, 28.71 / 28.46, 28.52, 28.83 | within noise |
| conv 8x8, 8 ch forward / rust | 1.477 (1.465-1.525) | 1.492 (1.464-1.567) | +1.0% | 1.47, 1.494, 1.501 / 1.491, 1.475, 1.535 | within noise |
| conv 8x8, 8 ch downstream / numpy | 22.23 (22.02-22.56) | 22.28 (21.97-22.44) | +0.2% | 22.34, 22.13, 22.3 / 22.35, 22.18, 22.13 | within noise |
| conv 8x8, 8 ch downstream / rust | 1.194 (1.162-1.259) | 1.203 (1.187-1.265) | +0.8% | 1.172, 1.193, 1.24 / 1.196, 1.2, 1.235 | within noise |
| conv 8x8, 8 ch accumulate_gradient / numpy | 7.341 (7.269-7.434) | 7.285 (7.128-7.408) | -0.8% | 7.296, 7.426, 7.325 / 7.214, 7.353, 7.225 | within noise |
| conv 8x8, 8 ch accumulate_gradient / rust | 1.174 (1.164-1.21) | 1.163 (1.146-1.169) | -0.9% | 1.166, 1.193, 1.181 / 1.157, 1.16, 1.163 | separated, inside spread |
| conv 8x8, 8 ch forward_batch b32 / numpy | 75.33 (73.97-75.85) | 75.31 (74.13-75.56) | -0.0% | 75.25, 74.62, 75.73 / 74.8, 74.86, 75.31 | within noise |
| conv 8x8, 8 ch forward_batch b32 / rust | 31.73 (30.39-32.75) | 31.12 (30.43-31.37) | -1.9% | 30.82, 32.28, 31.73 / 30.94, 31.29, 30.79 | within noise |
| conv 8x8, 8 ch forward_batch b512 / numpy | 882.2 (876.6-894.4) | 885.9 (868.7-912.8) | +0.4% | 883.1, 879.3, 886.1 / 877.7, 882.2, 902.3 | within noise |
| conv 8x8, 8 ch forward_batch b512 / rust | 492 (478-497.9) | 481.8 (472.6-490.9) | -2.1% | 481.1, 495.1, 493.7 / 472.6, 490.7, 481.8 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 65.23 (62.89-66.41) | 63.87 (63.06-66.6) | -2.1% | 65.34, 65.67, 64.12 / 63.84, 63.41, 66.27 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / rust | 28.39 (27.7-28.71) | 29.6 (28.18-33.14) | +4.2% | 27.97, 28.52, 28.54 / 28.29, 29.62, 31.56 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 702.2 (686-708.2) | 693.8 (683.2-709.5) | -1.2% | 699.7, 707.6, 694.1 / 692.5, 688.9, 702.7 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / rust | 446.2 (431.5-452.5) | 446.2 (439-470.2) | +0.0% | 438.7, 442.5, 449.5 / 440, 463.3, 445.4 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 97.45 (94.86-98.35) | 93 (92.04-96.04) | -4.6% | 95.86, 98.11, 97.45 / 92.62, 92.77, 95.35 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 28.43 (28.26-28.66) | 27.11 (27-27.32) | -4.6% | 28.59, 28.41, 28.32 / 27.21, 27.06, 27.12 | consistent |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 1465 (1421-1494) | 1395 (1387-1421) | -4.7% | 1430, 1465, 1483 / 1389, 1394, 1415 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 464.9 (459.5-468.2) | 454.5 (450.5-457.2) | -2.2% | 468, 462.2, 462.8 / 454.5, 452.2, 456.8 | separated, inside spread |
| conv 13x13x8, 8 ch forward / numpy | 50.7 (49.84-52.22) | 50.57 (49.95-51.2) | -0.2% | 51.91, 50.29, 50.59 / 50.54, 51.06, 50.15 | within noise |
| conv 13x13x8, 8 ch forward / rust | 20.37 (20.31-20.84) | 19.48 (19.24-20) | -4.4% | 20.37, 20.32, 20.81 / 19.48, 19.63, 19.48 | consistent |
| conv 13x13x8, 8 ch downstream / numpy | 51.82 (50.8-53.05) | 52.29 (51.26-53.37) | +0.9% | 52.38, 52.3, 50.92 / 52.89, 51.71, 52.05 | within noise |
| conv 13x13x8, 8 ch downstream / rust | 12.2 (11.71-12.43) | 12.48 (12.39-12.65) | +2.3% | 11.95, 12.2, 12.33 / 12.55, 12.55, 12.43 | separated, inside spread |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 23.29 (22.95-23.78) | 23.55 (23.15-23.94) | +1.1% | 23.36, 23.2, 23.37 / 23.44, 23.54, 23.6 | separated, inside spread |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 5.404 (5.333-5.51) | 5.028 (4.931-5.154) | -7.0% | 5.351, 5.439, 5.431 / 5.15, 4.973, 5.013 | consistent |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 1009 (999.1-1027) | 1014 (996.2-1023) | +0.6% | 1009, 1013, 1013 / 1012, 1006, 1019 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 613.1 (605.8-618.3) | 586.4 (582-594) | -4.4% | 608.2, 616.5, 614.5 / 586.1, 588, 587.7 | consistent |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 1.419e+04 (1.411e+04-1.433e+04) | 1.429e+04 (1.407e+04-1.433e+04) | +0.7% | 1.419e+04, 1.425e+04, 1.422e+04 / 1.412e+04, 1.43e+04, 1.431e+04 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 1.817e+04 (1.812e+04-1.827e+04) | 1.798e+04 (1.776e+04-1.815e+04) | -1.1% | 1.825e+04, 1.817e+04, 1.812e+04 / 1.793e+04, 1.789e+04, 1.814e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 898.9 (872.3-918.2) | 896.2 (868.5-931.9) | -0.3% | 898.9, 895.2, 896.7 / 897.1, 900.2, 896.2 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 350.5 (335.4-354.6) | 355.4 (346.9-359.3) | +1.4% | 342.8, 350.9, 352.1 / 352.1, 352.8, 358.9 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 2.572e+04 (2.566e+04-2.6e+04) | 2.575e+04 (2.557e+04-2.61e+04) | +0.1% | 2.58e+04, 2.587e+04, 2.568e+04 / 2.575e+04, 2.568e+04, 2.587e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 1057 (1040-1064) | 1056 (1042-1085) | -0.0% | 1049, 1055, 1060 / 1067, 1051, 1065 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 607.5 (599.3-620.8) | 609.9 (603.7-624.6) | +0.4% | 601.1, 609.8, 614.1 / 609.9, 609.6, 614.1 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 169.5 (166.7-172.6) | 171.1 (167-172.7) | +0.9% | 169.7, 168.4, 169.6 / 169.9, 172.6, 168.4 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.046e+04 (1.014e+04-1.066e+04) | 1.044e+04 (1.039e+04-1.06e+04) | -0.2% | 1.015e+04, 1.059e+04, 1.047e+04 / 1.052e+04, 1.04e+04, 1.051e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 2602 (2565-2610) | 2604 (2526-2614) | +0.1% | 2604, 2603, 2583 / 2607, 2531, 2610 | within noise |
| conv 26x26x8/2, 8 ch forward / numpy | 54.9 (53.4-55.66) | 54.38 (53.64-56.38) | -0.9% | 53.54, 55.45, 55.06 / 54.2, 54.43, 55.41 | within noise |
| conv 26x26x8/2, 8 ch forward / rust | 24.25 (24.04-24.84) | 23.34 (22.95-23.6) | -3.8% | 24.11, 24.39, 24.45 / 23.03, 23.49, 23.34 | consistent |
| conv 26x26x8/2, 8 ch downstream / numpy | 61.09 (59.67-62.27) | 61.88 (59.49-63.55) | +1.3% | 60.24, 61.82, 61.44 / 62.6, 62.08, 60.8 | within noise |
| conv 26x26x8/2, 8 ch downstream / rust | 15.1 (14-15.49) | 15.5 (15.03-15.66) | +2.7% | 14.58, 15.05, 15.26 / 15.3, 15.5, 15.54 | separated, inside spread |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 26.7 (25.86-27.1) | 26.96 (26.45-27.52) | +1.0% | 25.89, 26.7, 27.01 / 26.79, 27.15, 26.94 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 5.79 (5.721-5.88) | 5.779 (5.717-5.946) | -0.2% | 5.743, 5.79, 5.877 / 5.743, 5.853, 5.844 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 1269 (1228-1282) | 1243 (1233-1261) | -2.0% | 1236, 1269, 1277 / 1237, 1248, 1250 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 735.2 (724-740.8) | 703.3 (700.5-716.8) | -4.3% | 726.9, 735.2, 740.2 / 700.6, 706.4, 710.6 | consistent |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 1.742e+04 (1.712e+04-1.749e+04) | 1.732e+04 (1.714e+04-1.757e+04) | -0.6% | 1.716e+04, 1.749e+04, 1.742e+04 / 1.725e+04, 1.733e+04, 1.743e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 2.247e+04 (2.226e+04-2.266e+04) | 2.24e+04 (2.221e+04-2.247e+04) | -0.3% | 2.245e+04, 2.257e+04, 2.241e+04 / 2.24e+04, 2.234e+04, 2.235e+04 | separated, inside spread |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 1169 (1150-1197) | 1239 (1162-1280) | +6.0% | 1158, 1182, 1172 / 1214, 1253, 1214 | separated, inside spread |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 432.5 (425-439.1) | 435.8 (425.1-438.1) | +0.8% | 426.8, 434, 436.4 / 429.7, 435.9, 437.8 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 4.237e+04 (4.217e+04-4.323e+04) | 4.276e+04 (4.223e+04-4.33e+04) | +0.9% | 4.247e+04, 4.277e+04, 4.22e+04 / 4.281e+04, 4.244e+04, 4.299e+04 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 2336 (2330-2366) | 2331 (2324-2343) | -0.2% | 2335, 2335, 2351 / 2331, 2334, 2328 | separated, inside spread |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 710.3 (700.1-720.3) | 722.7 (705.2-727.2) | +1.7% | 703.1, 717.4, 709.5 / 712.5, 719.2, 726.8 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 202.5 (200.8-207.7) | 207.9 (204.3-208.3) | +2.7% | 200.9, 204.1, 204.3 / 204.3, 207.9, 208.2 | separated, inside spread |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 1.234e+04 (1.2e+04-1.242e+04) | 1.238e+04 (1.23e+04-1.249e+04) | +0.3% | 1.206e+04, 1.234e+04, 1.242e+04 / 1.247e+04, 1.231e+04, 1.237e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 3073 (3005-3090) | 3032 (2989-3085) | -1.3% | 3077, 3070, 3047 / 3040, 3025, 3032 | separated, inside spread |
| conv 26x26x8, 8 ch forward / numpy | 126.2 (124.3-129.9) | 128.9 (125.7-129.6) | +2.2% | 125.6, 127.7, 125.9 / 127.7, 128.9, 127.8 | within noise |
| conv 26x26x8, 8 ch forward / rust | 92.99 (92.68-94) | 88.62 (88.04-89.46) | -4.7% | 92.91, 93.67, 92.85 / 88.2, 88.58, 89.4 | consistent |
| conv 26x26x8, 8 ch downstream / numpy | 147.4 (143.5-158.2) | 150 (142.1-155.4) | +1.8% | 153.6, 146.5, 145.2 / 147.5, 153.1, 148.3 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 59.44 (57.53-62.42) | 61.05 (60.51-61.56) | +2.7% | 58.05, 61.77, 59.44 / 61.23, 61.26, 60.71 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 89.17 (88.33-90.7) | 89.97 (87.91-91.71) | +0.9% | 88.66, 89.14, 90.09 / 88.46, 91.57, 89.97 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 25.29 (24.95-25.71) | 25.22 (24.83-25.92) | -0.3% | 25.33, 25.29, 25.18 / 24.93, 25.71, 25.25 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 4227 (4179-4398) | 4299 (4171-4433) | +1.7% | 4191, 4227, 4327 / 4335, 4340, 4231 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 2967 (2956-3043) | 2871 (2862-2942) | -3.2% | 2965, 2962, 3028 / 2871, 2905, 2882 | separated, inside spread |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 6.754e+04 (6.731e+04-6.782e+04) | 6.766e+04 (6.739e+04-6.794e+04) | +0.2% | 6.738e+04, 6.777e+04, 6.751e+04 / 6.746e+04, 6.766e+04, 6.786e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 8.585e+04 (8.561e+04-8.699e+04) | 8.387e+04 (8.355e+04-8.412e+04) | -2.3% | 8.583e+04, 8.631e+04, 8.59e+04 / 8.402e+04, 8.38e+04, 8.368e+04 | consistent |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 4871 (4591-4935) | 4893 (4585-4990) | +0.4% | 4909, 4870, 4726 / 4779, 4900, 4800 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 395.1 (387.3-424.5) | 397.4 (385.9-407.9) | +0.6% | 392.7, 392.1, 409.9 / 403.2, 389.1, 398.1 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 1.126e+05 (1.125e+05-1.148e+05) | 1.138e+05 (1.125e+05-1.155e+05) | +1.1% | 1.138e+05, 1.125e+05, 1.135e+05 / 1.148e+05, 1.129e+05, 1.14e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 5006 (4978-5043) | 5045 (5006-5102) | +0.8% | 4995, 5011, 5016 / 5059, 5014, 5081 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 3055 (2993-3094) | 3073 (3042-3111) | +0.6% | 2996, 3074, 3069 / 3087, 3073, 3071 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 671.2 (667.3-687.7) | 683.7 (662.7-693.7) | +1.9% | 670.2, 679.9, 672 / 682.6, 672.7, 686.6 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 5.214e+04 (5.07e+04-5.248e+04) | 5.182e+04 (5.117e+04-5.309e+04) | -0.6% | 5.08e+04, 5.239e+04, 5.214e+04 / 5.214e+04, 5.23e+04, 5.153e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 1.202e+04 (1.171e+04-1.205e+04) | 1.202e+04 (1.172e+04-1.213e+04) | +0.0% | 1.203e+04, 1.201e+04, 1.188e+04 / 1.19e+04, 1.192e+04, 1.202e+04 | within noise |
| pool 26x26, 8 ch forward / numpy | 71.3 (69.95-72.3) | 71.03 (70.4-71.36) | -0.4% | 71.06, 70.71, 71.86 / 70.51, 71.13, 71.17 | within noise |
| pool 26x26, 8 ch forward / rust | 3.706 (3.682-3.803) | 3.61 (3.554-3.63) | -2.6% | 3.685, 3.735, 3.751 / 3.589, 3.614, 3.603 | consistent |
| pool 26x26, 8 ch downstream / numpy | 34.94 (34.61-35.84) | 34.72 (34.35-35.75) | -0.6% | 35.68, 34.86, 34.78 / 35.44, 34.59, 34.49 | within noise |
| pool 26x26, 8 ch downstream / rust | 5.119 (5.109-5.245) | 4.194 (4.135-4.321) | -18.1% | 5.116, 5.18, 5.166 / 4.207, 4.269, 4.153 | consistent |
| pool 26x26, 8 ch forward_batch b32 / numpy | 1240 (1219-1251) | 1225 (1220-1241) | -1.2% | 1222, 1244, 1245 / 1221, 1234, 1232 | within noise |
| pool 26x26, 8 ch forward_batch b32 / rust | 111.7 (110.8-113.5) | 106.6 (105.3-109.1) | -4.6% | 111.9, 112.7, 110.8 / 105.7, 106.7, 107.8 | consistent |
| pool 26x26, 8 ch forward_batch b512 / numpy | 2.033e+04 (1.996e+04-2.048e+04) | 2.029e+04 (2.021e+04-2.038e+04) | -0.2% | 2.005e+04, 2.035e+04, 2.04e+04 / 2.024e+04, 2.033e+04, 2.03e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 2422 (2407-2433) | 2357 (2349-2363) | -2.7% | 2421, 2428, 2414 / 2355, 2359, 2356 | consistent |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 488.1 (474.8-503.1) | 491.6 (477.1-498.4) | +0.7% | 492.9, 483, 489.6 / 491.6, 487.7, 490.9 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / rust | 159.5 (157.9-161.2) | 132.4 (130.6-135.8) | -17.0% | 158.5, 160.6, 159.7 / 131.1, 133.2, 134.1 | consistent |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 1.364e+04 (1.36e+04-1.37e+04) | 1.375e+04 (1.365e+04-1.386e+04) | +0.8% | 1.366e+04, 1.367e+04, 1.361e+04 / 1.369e+04, 1.381e+04, 1.375e+04 | separated, inside spread |
| pool 26x26, 8 ch downstream_batch b512 / rust | 3003 (2997-3093) | 2623 (2610-2636) | -12.7% | 3003, 3002, 3048 / 2623, 2618, 2631 | consistent |
| pool 6x6, 8 ch forward / numpy | 34.26 (34.04-34.5) | 34.53 (34.33-34.99) | +0.8% | 34.07, 34.31, 34.4 / 34.76, 34.52, 34.43 | separated, inside spread |
| pool 6x6, 8 ch forward / rust | 0.4934 (0.4865-0.4989) | 0.4969 (0.4879-0.5002) | +0.7% | 0.4897, 0.4927, 0.4986 / 0.4944, 0.499, 0.492 | within noise |
| pool 6x6, 8 ch downstream / numpy | 19.36 (19.03-20.38) | 19.24 (18.72-20.29) | -0.6% | 19.44, 19.17, 19.88 / 19.23, 19.52, 19.5 | within noise |
| pool 6x6, 8 ch downstream / rust | 0.5728 (0.5588-0.5852) | 0.4429 (0.4377-0.4609) | -22.7% | 0.5594, 0.582, 0.5728 / 0.4378, 0.4452, 0.4519 | consistent |
| pool 6x6, 8 ch forward_batch b32 / numpy | 108.9 (108.5-109.9) | 109.6 (108.3-110.2) | +0.6% | 109.4, 108.8, 108.7 / 110.2, 109.3, 108.7 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 8.221 (8.171-8.381) | 8.392 (8.185-8.466) | +2.1% | 8.203, 8.234, 8.276 / 8.267, 8.436, 8.402 | within noise |
| pool 6x6, 8 ch forward_batch b512 / numpy | 1227 (1206-1230) | 1225 (1207-1232) | -0.2% | 1207, 1228, 1228 / 1218, 1219, 1225 | within noise |
| pool 6x6, 8 ch forward_batch b512 / rust | 128.5 (127.8-130.9) | 129.9 (128-132.2) | +1.0% | 128.2, 128.3, 129.8 / 128.4, 130.8, 130.5 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 59.64 (58.96-60.96) | 60.63 (59.3-62.38) | +1.7% | 59.91, 59.49, 59.96 / 60.63, 60.22, 61.12 | separated, inside spread |
| pool 6x6, 8 ch downstream_batch b32 / rust | 11.3 (11.21-11.49) | 7.658 (7.628-7.772) | -32.3% | 11.3, 11.26, 11.4 / 7.641, 7.675, 7.716 | consistent |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 601.9 (591-612.3) | 606.7 (592.5-614) | +0.8% | 607.2, 596.6, 597 / 600.8, 608.4, 603.2 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 178.5 (177.3-181.7) | 120.9 (119.6-123.2) | -32.3% | 177.5, 180.4, 179.7 / 119.6, 120.9, 122.6 | consistent |
| conv tail 32 x 5408 bare downstream b32 / numpy | 77.03 (66.2-79.94) | 72.5 (66.62-79.07) | -5.9% | 66.48, 77.03, 79.6 / 72.84, 71.23, 75.71 | within noise |
| conv tail 32 x 5408 bare downstream b32 / rust | 253.1 (244.3-260.4) | 248.2 (245-254.4) | -1.9% | 247.4, 257.1, 253.2 / 245, 252.1, 248.2 | within noise |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3208 (3206-3220) | 3219 (3194-3228) | +0.3% | 3214, 3208, 3207 / 3211, 3226, 3208 | within noise |
| conv tail 32 x 5408 bare downstream b512 / rust | 2411 (2403-2441) | 2263 (2257-2283) | -6.1% | 2426, 2408, 2421 / 2263, 2262, 2271 | consistent |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 79.34 (78.76-79.92) | 79.02 (78.52-79.64) | -0.4% | 78.96, 79.27, 79.72 / 79.31, 79.04, 78.77 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / rust | 240.6 (235.5-247.1) | 228.6 (224.4-233.2) | -5.0% | 239.4, 238.1, 243.8 / 226.8, 228.4, 230.9 | consistent |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 1618 (1604-1633) | 1636 (1629-1680) | +1.1% | 1618, 1615, 1623 / 1657, 1634, 1641 | separated, inside spread |
| conv tail 32 x 5408 bare accumulate b512 / rust | 2198 (2168-2238) | 2221 (2176-2233) | +1.0% | 2198, 2219, 2180 / 2226, 2200, 2203 | within noise |
| conv tail 32 x 5408 transpose b32 / numpy | 0.715 (0.7017-0.7264) | 0.7148 (0.7075-0.7217) | -0.0% | 0.7081, 0.7174, 0.7202 / 0.7102, 0.7214, 0.7146 | within noise |
| conv tail 32 x 5408 transpose b32 / rust | 0.8359 (0.8127-0.8532) | 0.8712 (0.8508-0.8881) | +4.2% | 0.8199, 0.8416, 0.8451 / 0.8611, 0.8773, 0.8791 | separated, inside spread |
| conv tail 32 x 5408 transpose b512 / numpy | 12.19 (11.04-13.43) | 11.57 (11.25-12.34) | -5.1% | 11.09, 12.82, 12.7 / 11.43, 12.06, 11.41 | within noise |
| conv tail 32 x 5408 transpose b512 / rust | 12.66 (12.52-15) | 14.44 (13.91-15.09) | +14.1% | 12.52, 12.66, 13.87 / 14.39, 14.31, 14.7 | separated, inside spread |
| conv tail 32 x 5408 add b32 / numpy | 97.77 (95.26-101) | 97.81 (95.73-101.1) | +0.0% | 100.8, 97.5, 96.59 / 97.81, 99.35, 98.12 | within noise |
| conv tail 32 x 5408 add b32 / rust | 64.65 (63.11-69.3) | 64.87 (63.09-69.33) | +0.3% | 67.69, 63.17, 64.66 / 63.13, 66.23, 67.95 | within noise |
| conv tail 32 x 5408 add b512 / numpy | 96.74 (94.3-96.87) | 96.9 (94.25-100) | +0.2% | 96.7, 96.77, 95.58 / 97.22, 97.13, 96.86 | separated, inside spread |
| conv tail 32 x 5408 add b512 / rust | 67.73 (62.81-69.53) | 66.02 (62.39-68.83) | -2.5% | 67.77, 66.13, 66.21 / 62.4, 67.22, 67.61 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 1.423 (1.385-1.522) | 1.461 (1.443-1.502) | +2.7% | 1.413, 1.404, 1.484 / 1.468, 1.485, 1.446 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.4387 (0.4245-0.4501) | 0.4248 (0.4193-0.4324) | -3.2% | 0.431, 0.4426, 0.4439 / 0.4228, 0.4255, 0.4258 | separated, inside spread |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 11.42 (11.38-11.57) | 10.5 (10.46-11.02) | -8.1% | 11.46, 11.41, 11.47 / 10.49, 10.74, 10.64 | consistent |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 4.857 (4.752-5.054) | 4.813 (4.704-4.916) | -0.9% | 4.808, 4.952, 4.917 / 4.705, 4.837, 4.872 | within noise |
| dense 30 x 784 bare downstream b32 / numpy | 23.73 (23.04-23.95) | 23.16 (22.9-23.56) | -2.4% | 23.64, 23.47, 23.83 / 23.15, 23.4, 23 | separated, inside spread |
| dense 30 x 784 bare downstream b32 / rust | 29.77 (29.09-33.57) | 28.76 (28.5-29.81) | -3.4% | 29.32, 31.78, 29.87 / 28.6, 29.23, 29.15 | separated, inside spread |
| dense 30 x 784 bare downstream b512 / numpy | 136.8 (135.7-140.6) | 138.9 (137.8-143.4) | +1.5% | 138.1, 136.8, 137.2 / 138.8, 140.6, 138.9 | separated, inside spread |
| dense 30 x 784 bare downstream b512 / rust | 247 (243.5-248.4) | 243.7 (241.7-250) | -1.3% | 245.9, 246.3, 247.8 / 242.2, 244.3, 247.4 | within noise |
| dense 30 x 784 bare accumulate b32 / numpy | 28.72 (27.91-29.73) | 29.18 (28.62-29.43) | +1.6% | 28.94, 28.28, 29.21 / 29.03, 29.18, 29.17 | within noise |
| dense 30 x 784 bare accumulate b32 / rust | 32.67 (31.5-33.52) | 32.39 (31.4-33.3) | -0.9% | 32.36, 32.35, 33.13 / 31.5, 32.39, 33.18 | within noise |
| dense 30 x 784 bare accumulate b512 / numpy | 196.3 (193.8-197.5) | 194.5 (192.9-195.8) | -0.9% | 195.7, 195.7, 196.5 / 193.9, 194.4, 195.1 | separated, inside spread |
| dense 30 x 784 bare accumulate b512 / rust | 286.1 (278.4-292.5) | 283.5 (279.4-285.8) | -0.9% | 286.6, 289.5, 280.9 / 282.6, 282.7, 284.5 | within noise |
| dense 30 x 784 transpose b32 / numpy | 0.6961 (0.6818-0.7036) | 0.6955 (0.6873-0.7027) | -0.1% | 0.6829, 0.6999, 0.6975 / 0.6941, 0.6995, 0.6943 | within noise |
| dense 30 x 784 transpose b32 / rust | 0.8097 (0.7859-0.8268) | 0.8429 (0.8331-0.8504) | +4.1% | 0.797, 0.8097, 0.8261 / 0.8338, 0.8451, 0.8476 | separated, inside spread |
| dense 30 x 784 transpose b512 / numpy | 7.301 (6.997-7.416) | 7.225 (7.137-7.53) | -1.0% | 7.319, 7.207, 7.253 / 7.225, 7.334, 7.292 | within noise |
| dense 30 x 784 transpose b512 / rust | 13.15 (12.8-14.15) | 13.29 (12.14-14.47) | +1.1% | 12.82, 13.32, 13.71 / 13.23, 13.35, 13.3 | within noise |
| dense 30 x 784 add b32 / numpy | 10.71 (8.977-11.82) | 9.383 (9.345-9.895) | -12.4% | 11.06, 10.4, 10.71 / 9.438, 9.62, 9.383 | consistent |
| dense 30 x 784 add b32 / rust | 8.884 (8.756-9.137) | 8.773 (8.669-9.591) | -1.3% | 8.972, 9.02, 8.788 / 8.768, 9.13, 9.055 | within noise |
| dense 30 x 784 add b512 / numpy | 12.38 (12.25-13.07) | 12.7 (12.2-12.88) | +2.5% | 12.68, 12.63, 12.31 / 12.37, 12.76, 12.76 | within noise |
| dense 30 x 784 add b512 / rust | 8.641 (8.499-8.939) | 8.74 (8.363-9.532) | +1.2% | 8.78, 8.718, 8.585 / 8.74, 8.953, 8.948 | within noise |
| dense 30 x 784 sum_axis0 b32 / numpy | 1.458 (1.435-1.592) | 1.492 (1.436-1.579) | +2.3% | 1.514, 1.47, 1.446 / 1.47, 1.496, 1.509 | within noise |
| dense 30 x 784 sum_axis0 b32 / rust | 0.3961 (0.3884-0.4047) | 0.4017 (0.3942-0.4121) | +1.4% | 0.3908, 0.3961, 0.4035 / 0.3987, 0.4064, 0.4031 | within noise |
| dense 30 x 784 sum_axis0 b512 / numpy | 10.89 (10.69-11.03) | 11.01 (10.91-11.09) | +1.1% | 10.81, 10.99, 10.78 / 11.02, 11.06, 10.94 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 4.191 (4.102-4.273) | 4.327 (4.241-4.445) | +3.3% | 4.169, 4.189, 4.191 / 4.257, 4.337, 4.413 | separated, inside spread |
| dense 10 x 30 bare downstream b32 / numpy | 1.787 (1.776-1.881) | 1.799 (1.729-1.855) | +0.6% | 1.777, 1.839, 1.787 / 1.798, 1.819, 1.772 | within noise |
| dense 10 x 30 bare downstream b32 / rust | 1.183 (1.159-1.205) | 1.119 (1.105-1.187) | -5.4% | 1.164, 1.183, 1.197 / 1.119, 1.161, 1.109 | separated, inside spread |
| dense 10 x 30 bare downstream b512 / numpy | 12.05 (11.91-12.13) | 12.03 (11.83-12.24) | -0.2% | 11.93, 12.11, 12.07 / 11.96, 12.11, 12.07 | within noise |
| dense 10 x 30 bare downstream b512 / rust | 15.96 (15.52-16.15) | 16.13 (15.84-16.5) | +1.1% | 15.72, 15.83, 16.13 / 15.98, 16.05, 16.32 | within noise |
| dense 10 x 30 bare accumulate b32 / numpy | 1.818 (1.788-1.878) | 1.803 (1.783-1.87) | -0.8% | 1.79, 1.832, 1.849 / 1.795, 1.792, 1.857 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 1.221 (1.208-1.234) | 1.205 (1.193-1.223) | -1.3% | 1.221, 1.221, 1.222 / 1.198, 1.208, 1.213 | separated, inside spread |
| dense 10 x 30 bare accumulate b512 / numpy | 13.55 (13.39-13.65) | 13.63 (13.21-13.97) | +0.6% | 13.44, 13.55, 13.65 / 13.51, 13.45, 13.84 | within noise |
| dense 10 x 30 bare accumulate b512 / rust | 25.34 (25.16-25.59) | 25.61 (25.5-26.74) | +1.1% | 25.5, 25.34, 25.21 / 26.12, 25.87, 25.59 | separated, inside spread |
| dense 10 x 30 transpose b32 / numpy | 0.448 (0.4337-0.4589) | 0.458 (0.4418-0.473) | +2.2% | 0.4386, 0.448, 0.4578 / 0.4508, 0.4646, 0.4558 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.3832 (0.3743-0.3887) | 0.3851 (0.3792-0.3879) | +0.5% | 0.3753, 0.386, 0.3853 / 0.3834, 0.3861, 0.3851 | within noise |
| dense 10 x 30 transpose b512 / numpy | 2.951 (2.912-3.05) | 2.95 (2.54-2.996) | -0.0% | 2.981, 2.964, 2.935 / 2.945, 2.741, 2.984 | within noise |
| dense 10 x 30 transpose b512 / rust | 4.159 (4.092-4.205) | 4.032 (4.018-4.12) | -3.1% | 4.12, 4.161, 4.188 / 4.049, 4.021, 4.077 | separated, inside spread |
| dense 10 x 30 add b32 / numpy | 0.4104 (0.4048-0.4178) | 0.4093 (0.4072-0.4172) | -0.3% | 0.4082, 0.4113, 0.4137 / 0.4078, 0.4126, 0.4129 | within noise |
| dense 10 x 30 add b32 / rust | 0.1935 (0.1926-0.1996) | 0.1913 (0.1894-0.1927) | -1.1% | 0.1929, 0.1963, 0.1958 / 0.1909, 0.19, 0.1925 | separated, inside spread |
| dense 10 x 30 add b512 / numpy | 0.4174 (0.413-0.4487) | 0.4226 (0.4184-0.4382) | +1.3% | 0.4133, 0.4366, 0.4174 / 0.4226, 0.4232, 0.43 | within noise |
| dense 10 x 30 add b512 / rust | 0.208 (0.2028-0.2188) | 0.2041 (0.2021-0.2221) | -1.8% | 0.2108, 0.2075, 0.2085 / 0.203, 0.2034, 0.2138 | within noise |
| dense 10 x 30 sum_axis0 b32 / numpy | 1.321 (1.285-1.367) | 1.327 (1.282-1.395) | +0.5% | 1.301, 1.338, 1.331 / 1.287, 1.332, 1.37 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.2876 (0.2825-0.2935) | 0.3109 (0.3038-0.3165) | +8.1% | 0.2846, 0.2905, 0.288 / 0.3068, 0.3142, 0.3099 | consistent |
| dense 10 x 30 sum_axis0 b512 / numpy | 9.104 (8.953-9.264) | 9.194 (8.964-9.245) | +1.0% | 8.962, 9.152, 9.197 / 9.104, 9.133, 9.209 | within noise |
| dense 10 x 30 sum_axis0 b512 / rust | 2.565 (2.545-2.632) | 3.012 (2.981-3.028) | +17.4% | 2.564, 2.545, 2.626 / 2.999, 3.003, 3.02 | consistent |
| attention 16 x 32 forward_batch b32 / numpy | 288.5 (285.6-294) | 290.1 (286.5-293.7) | +0.6% | 289.5, 289.8, 288.5 / 289.2, 289.8, 291.8 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 364.1 (362.3-370.3) | 420.8 (416-421.8) | +15.6% | 363.8, 365, 366.7 / 420.1, 418.2, 421.5 | consistent |
| attention 16 x 32 forward_batch b512 / numpy | 5112 (5027-5208) | 5146 (5115-5202) | +0.7% | 5042, 5172, 5128 / 5127, 5146, 5184 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 5665 (5643-5675) | 6474 (6449-6587) | +14.3% | 5651, 5664, 5673 / 6532, 6493, 6469 | consistent |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 261.7 (261-271.2) | 266.6 (262.4-270.9) | +1.9% | 266.2, 265.7, 261.5 / 266.9, 262.9, 268.9 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / rust | 250.6 (244.6-252.3) | 249.5 (247.7-253.4) | -0.4% | 250, 247.9, 251.2 / 249.5, 250.5, 249.5 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 4558 (4522-4595) | 4579 (4536-4636) | +0.5% | 4532, 4574, 4563 / 4579, 4562, 4587 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / rust | 4670 (4541-4741) | 4637 (4579-4770) | -0.7% | 4641, 4670, 4653 / 4681, 4715, 4591 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 245.9 (244-251.6) | 247.3 (245.4-252.6) | +0.6% | 247.8, 246.7, 244.8 / 247.2, 247.3, 249 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 213.5 (212.5-220.3) | 220.6 (211.1-229.2) | +3.3% | 213.7, 212.9, 217 / 215.8, 225, 219.3 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5512 (5426-5667) | 5480 (5471-5555) | -0.6% | 5532, 5613, 5463 / 5473, 5480, 5552 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 4083 (4006-4168) | 4064 (4028-4099) | -0.5% | 4062, 4100, 4083 / 4086, 4041, 4063 | within noise |
