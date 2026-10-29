Old `6dcd34c` against new `6dcd34c`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `10dfec9` (extension sha256 `7d70efbe6dbd`) and new crate `3b5ccd7` (extension sha256 `32ad9eba76b4`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 2.57 (HIGH); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / dense 10 x 30 forward_batch b512 / rust +33.1% (58.92 -> 78.43 µs)
- consistent: per call / pool 6x6, 8 ch downstream_batch b512 / rust -32.3% (180.1 -> 121.9 µs)
- consistent: per call / pool 6x6, 8 ch downstream_batch b32 / rust -31.5% (11.34 -> 7.764 µs)
- consistent: per call / pool 6x6, 8 ch downstream / rust -22.3% (0.5762 -> 0.4478 µs)
- consistent: per call / pool 26x26, 8 ch downstream / rust -19.6% (5.148 -> 4.14 µs)
- consistent: per call / pool 26x26, 8 ch forward_batch b32 / rust -18.5% (112.1 -> 91.41 µs)
- consistent: per call / pool 26x26, 8 ch forward / rust -18.2% (3.708 -> 3.032 µs)
- consistent: per call / dense 30 x 784 forward_batch b512 / rust +18.0% (364.9 -> 430.4 µs)
- consistent: per call / pool 26x26, 8 ch downstream_batch b32 / rust -16.7% (159.3 -> 132.7 µs)
- consistent: per call / pool 6x6, 8 ch forward_batch b32 / rust -16.5% (8.297 -> 6.931 µs)
- ... 27 more consistent rows (report --md)
- 233 rows within noise (42 separated inside their spread), max |Δ| 31.4%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 27.57 (26.89-28.34) | 28.49 (27.43-29.84) | +3.3% | 28.03, 27.03, 27.66 / 27.93, 29.25, 28.19 | within noise |
| conv tail 32 x 5408 forward / rust | 20.69 (19.07-22.83) | 21.81 (19.36-22.73) | +5.4% | 19.14, 21.76, 21.74 / 21.12, 21.81, 21.03 | within noise |
| conv tail 32 x 5408 downstream / numpy | 23.47 (23.4-25.7) | 23.52 (23.45-25.82) | +0.2% | 23.89, 23.44, 24.56 / 23.49, 24.03, 24.64 | within noise |
| conv tail 32 x 5408 downstream / rust | 21.93 (20.76-23.31) | 22.1 (20.73-23.7) | +0.7% | 20.79, 22, 22.59 / 21.29, 22.8, 22.95 | within noise |
| conv tail 32 x 5408 hidden_delta / numpy | 31.48 (31.31-33.95) | 32.5 (31.41-33.97) | +3.2% | 31.88, 31.48, 32.67 / 31.47, 32.5, 33.89 | within noise |
| conv tail 32 x 5408 hidden_delta / rust | 24.18 (23.01-24.48) | 24.31 (22.84-26.24) | +0.5% | 23.75, 24.31, 24.03 / 23.51, 24.71, 25.18 | within noise |
| conv tail 32 x 5408 accumulate_gradient / numpy | 88.77 (87.9-93.97) | 88.26 (86.54-91.33) | -0.6% | 89.12, 88.02, 91.56 / 87.07, 88.46, 89.77 | within noise |
| conv tail 32 x 5408 accumulate_gradient / rust | 55.92 (54.92-57.18) | 54.54 (53.4-56.7) | -2.5% | 55.32, 55.86, 56.73 / 54.03, 55.56, 54.83 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 179.1 (177.1-184.4) | 180.6 (177-184.4) | +0.9% | 179.1, 179.2, 180.8 / 177.1, 180.6, 184.2 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 109.6 (107-111) | 110.6 (107-111.6) | +0.9% | 109, 109, 110.5 / 109.9, 108.7, 111.2 | within noise |
| conv tail 32 x 5408 sgd step / numpy | 263.9 (263.1-276.1) | 267.4 (263.9-275.7) | +1.3% | 264.2, 263.7, 270 / 264.5, 269.9, 269.8 | within noise |
| conv tail 32 x 5408 sgd step / rust | 60.1 (58.97-62.32) | 60.44 (59.08-63.59) | +0.6% | 59.65, 59.66, 61.78 / 61.38, 60.68, 60.44 | within noise |
| conv tail 32 x 5408 forward_batch b32 / numpy | 152.9 (146.3-158.7) | 156.1 (147.1-158.6) | +2.1% | 147.5, 156.2, 154.2 / 151.2, 155.9, 158.1 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 349 (338.7-382.9) | 358.7 (346.8-389.9) | +2.8% | 341, 349, 375 / 348.9, 374.2, 361 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1164 (1054-1170) | 1166 (1162-1173) | +0.2% | 1110, 1167, 1164 / 1164, 1167, 1170 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1885 (1786-1906) | 1954 (1905-1980) | +3.6% | 1845, 1885, 1892 / 1970, 1934, 1928 | separated, inside spread |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 79.55 (78.89-80.26) | 79.77 (78.86-80.26) | +0.3% | 79.08, 79.61, 80.02 / 79.56, 79.74, 79.86 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 253.3 (244-257) | 252.3 (248-254.9) | -0.4% | 249.2, 251.5, 253.8 / 250.2, 251.2, 254.2 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3103 (3046-3112) | 3098 (3092-3105) | -0.2% | 3107, 3072, 3105 / 3093, 3102, 3100 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2401 (2394-2425) | 2434 (2430-2471) | +1.4% | 2397, 2410, 2402 / 2432, 2453, 2433 | consistent, small |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 620.5 (609.7-628.7) | 618.2 (612.2-632.6) | -0.4% | 614.7, 618.8, 625 / 614.9, 626.3, 617.3 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 321.5 (315.5-329.4) | 316 (306.1-325.5) | -1.7% | 318, 321.5, 328.3 / 312.3, 314.8, 320.6 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 1.212e+04 (1.209e+04-1.235e+04) | 1.218e+04 (1.212e+04-1.245e+04) | +0.5% | 1.212e+04, 1.222e+04, 1.216e+04 / 1.229e+04, 1.223e+04, 1.216e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 5942 (5912-6026) | 5822 (5787-5888) | -2.0% | 5933, 5922, 6004 / 5823, 5853, 5814 | separated, inside spread |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 165.2 (161.9-170.3) | 164.5 (163.5-165.5) | -0.4% | 163.4, 167.9, 167 / 164.8, 164.2, 164.5 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 282.8 (270.4-285.3) | 280.2 (273.7-288.5) | -0.9% | 276.6, 280.4, 283.6 / 275.8, 285.5, 279.7 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 1836 (1817-1891) | 1844 (1814-1858) | +0.5% | 1854, 1840, 1836 / 1852, 1847, 1824 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 2361 (2322-2382) | 2350 (2251-2373) | -0.5% | 2335, 2372, 2370 / 2321, 2305, 2350 | within noise |
| dense 30 x 784 forward / numpy | 8.073 (7.816-8.51) | 8.082 (7.79-8.34) | +0.1% | 8.139, 7.984, 8.252 / 7.899, 8.248, 8.059 | within noise |
| dense 30 x 784 forward / rust | 2.736 (2.649-2.818) | 2.921 (2.813-3.054) | +6.8% | 2.73, 2.703, 2.766 / 2.87, 2.988, 2.882 | separated, inside spread |
| dense 30 x 784 downstream / numpy | 3.994 (3.856-4.068) | 3.911 (3.867-4.219) | -2.1% | 3.928, 4.028, 4.008 / 4.062, 3.868, 3.927 | within noise |
| dense 30 x 784 downstream / rust | 2.107 (2.023-2.186) | 2.05 (1.967-2.275) | -2.7% | 2.108, 2.057, 2.153 / 1.997, 2.236, 2.028 | within noise |
| dense 30 x 784 hidden_delta / numpy | 6.718 (6.641-6.868) | 6.894 (6.757-7.047) | +2.6% | 6.7, 6.754, 6.748 / 6.879, 6.934, 6.902 | consistent |
| dense 30 x 784 hidden_delta / rust | 2.774 (2.674-3.31) | 2.705 (2.473-2.779) | -2.5% | 2.706, 3.143, 2.774 / 2.626, 2.764, 2.641 | within noise |
| dense 30 x 784 accumulate_gradient / numpy | 27.64 (27.35-28.65) | 27.84 (27.3-28.46) | +0.7% | 28.06, 28, 27.49 / 27.58, 28.22, 27.61 | within noise |
| dense 30 x 784 accumulate_gradient / rust | 6.897 (6.795-7.376) | 7.017 (6.738-7.14) | +1.7% | 6.828, 7.309, 6.897 / 6.971, 7.104, 6.857 | within noise |
| dense 30 x 784 apply_accumulated_gradient / numpy | 30.84 (30.79-32.63) | 31.08 (30.76-31.76) | +0.8% | 30.95, 31.73, 30.79 / 30.97, 31.37, 31.33 | within noise |
| dense 30 x 784 apply_accumulated_gradient / rust | 16.63 (16.46-17.24) | 16.57 (16.46-17.22) | -0.4% | 16.58, 17.1, 16.57 / 16.55, 16.9, 16.54 | within noise |
| dense 30 x 784 sgd step / numpy | 59.5 (59.04-60.63) | 60.44 (58.53-62.3) | +1.6% | 60.1, 59.99, 59.11 / 60.41, 60.44, 60.07 | within noise |
| dense 30 x 784 sgd step / rust | 7.413 (7.144-7.623) | 7.389 (7.306-7.96) | -0.3% | 7.352, 7.487, 7.413 / 7.32, 7.683, 7.439 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 38.1 (37.56-38.64) | 38.49 (37.83-39.01) | +1.0% | 37.79, 38.44, 38.09 / 38.27, 38.66, 38.42 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 50.58 (49.51-51.45) | 54.67 (53.8-55.25) | +8.1% | 50.04, 51.2, 50.55 / 54.02, 54.91, 55 | consistent |
| dense 30 x 784 forward_batch b512 / numpy | 267.5 (229.4-268.2) | 267.8 (266.9-270.8) | +0.1% | 248.8, 265.9, 267.9 / 267, 267.8, 269.7 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 364.9 (358.9-366.5) | 430.4 (427.7-432.6) | +18.0% | 361.9, 365.7, 363.7 / 430.4, 427.8, 432.1 | consistent |
| dense 30 x 784 downstream_batch b32 / numpy | 23.97 (23.55-24.34) | 23.89 (23.57-24.12) | -0.3% | 23.97, 23.93, 23.95 / 23.89, 23.83, 23.85 | separated, inside spread |
| dense 30 x 784 downstream_batch b32 / rust | 32.45 (31.79-33.37) | 33.24 (32.89-33.89) | +2.4% | 32.34, 32.17, 32.85 / 33.24, 33.31, 33.39 | separated, inside spread |
| dense 30 x 784 downstream_batch b512 / numpy | 131.3 (130.6-133.5) | 131.6 (130.7-132.2) | +0.2% | 132.1, 131.1, 131.4 / 131.1, 131.7, 131.9 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 243.3 (239.8-246.6) | 246.2 (241.9-249.5) | +1.2% | 242.1, 246.6, 241.6 / 246.9, 244.1, 247.7 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 62.24 (61.55-63.69) | 62.57 (61.85-65.1) | +0.5% | 62, 63.43, 61.83 / 63.17, 64.14, 61.94 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / rust | 42.78 (41.32-44.09) | 43.49 (42.98-43.77) | +1.6% | 41.6, 43.39, 42.98 / 43.49, 43.42, 43.32 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 1693 (1678-1732) | 1710 (1709-1725) | +1.0% | 1688, 1694, 1705 / 1709, 1712, 1717 | separated, inside spread |
| dense 30 x 784 hidden_delta_batch b512 / rust | 496 (488.1-504.5) | 496 (492-556.1) | +0.0% | 496.2, 501.6, 488.3 / 497.3, 495.3, 524.7 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 40.45 (39.84-41.56) | 40.35 (39.22-40.85) | -0.3% | 40.22, 41.44, 40.21 / 40.54, 40.07, 39.71 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 38.53 (37.6-39.17) | 40.8 (39.71-41.38) | +5.9% | 37.89, 38.48, 38.95 / 40.55, 41.26, 40.07 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 224 (222.4-227.7) | 223.5 (220.7-226.9) | -0.2% | 222.5, 225.4, 225 / 225.2, 223.2, 223.2 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 313.6 (308.5-315.3) | 309.9 (306-319) | -1.2% | 312.4, 311.9, 314.8 / 309.9, 312.5, 312 | within noise |
| dense 10 x 30 forward / numpy | 4.539 (4.387-4.796) | 4.523 (4.376-4.763) | -0.3% | 4.518, 4.472, 4.668 / 4.611, 4.607, 4.46 | within noise |
| dense 10 x 30 forward / rust | 0.3491 (0.3359-0.3582) | 0.3953 (0.3842-0.4076) | +13.2% | 0.3471, 0.3527, 0.3455 / 0.3935, 0.3959, 0.3997 | consistent |
| dense 10 x 30 downstream / numpy | 0.8262 (0.7968-0.8618) | 0.8366 (0.8332-0.842) | +1.3% | 0.8293, 0.8324, 0.8236 / 0.8376, 0.8377, 0.8366 | separated, inside spread |
| dense 10 x 30 downstream / rust | 0.2034 (0.1944-0.2112) | 0.2021 (0.1965-0.2218) | -0.6% | 0.2028, 0.2034, 0.2049 / 0.1983, 0.2118, 0.2026 | within noise |
| dense 10 x 30 hidden_delta / numpy | 2.258 (2.197-2.306) | 2.233 (2.198-2.538) | -1.1% | 2.223, 2.305, 2.236 / 2.265, 2.391, 2.21 | within noise |
| dense 10 x 30 hidden_delta / rust | 0.4324 (0.4223-0.4555) | 0.4362 (0.4259-0.4472) | +0.9% | 0.4391, 0.4281, 0.4336 / 0.4283, 0.4366, 0.4416 | within noise |
| dense 10 x 30 accumulate_gradient / numpy | 2.876 (2.783-2.904) | 2.919 (2.882-3.003) | +1.5% | 2.841, 2.855, 2.896 / 2.924, 2.951, 2.919 | separated, inside spread |
| dense 10 x 30 accumulate_gradient / rust | 0.4244 (0.4132-0.4448) | 0.4014 (0.395-0.4137) | -5.4% | 0.4226, 0.4244, 0.4337 / 0.4014, 0.4007, 0.4052 | consistent |
| dense 10 x 30 apply_accumulated_gradient / numpy | 4.672 (4.598-4.719) | 4.711 (4.554-4.919) | +0.8% | 4.654, 4.689, 4.65 / 4.631, 4.724, 4.737 | within noise |
| dense 10 x 30 apply_accumulated_gradient / rust | 2.223 (2.197-2.337) | 2.196 (2.176-2.271) | -1.2% | 2.204, 2.268, 2.274 / 2.182, 2.238, 2.21 | within noise |
| dense 10 x 30 sgd step / numpy | 8.45 (8.224-8.785) | 8.395 (8.152-8.802) | -0.6% | 8.45, 8.579, 8.47 / 8.349, 8.629, 8.271 | within noise |
| dense 10 x 30 sgd step / rust | 0.4672 (0.4607-0.4887) | 0.4626 (0.451-0.4739) | -1.0% | 0.4672, 0.4774, 0.4694 / 0.4589, 0.4587, 0.4701 | within noise |
| dense 10 x 30 forward_batch b32 / numpy | 9.848 (9.692-10.04) | 9.802 (9.646-10.21) | -0.5% | 9.812, 9.829, 9.915 / 9.849, 9.956, 9.711 | within noise |
| dense 10 x 30 forward_batch b32 / rust | 4.034 (3.984-4.05) | 5.301 (5.203-8.699) | +31.4% | 4.002, 4.029, 4.049 / 6.951, 5.382, 5.288 | separated, inside spread |
| dense 10 x 30 forward_batch b512 / numpy | 55.29 (54.43-56.05) | 55.01 (54.19-55.45) | -0.5% | 54.85, 55.67, 55.13 / 55.07, 55.23, 54.49 | within noise |
| dense 10 x 30 forward_batch b512 / rust | 58.92 (57.93-59.93) | 78.43 (77.94-79.02) | +33.1% | 58.5, 59.18, 58.92 / 78.18, 78.73, 78.48 | consistent |
| dense 10 x 30 downstream_batch b32 / numpy | 1.837 (1.816-1.862) | 1.819 (1.789-1.844) | -1.0% | 1.834, 1.836, 1.842 / 1.816, 1.832, 1.809 | separated, inside spread |
| dense 10 x 30 downstream_batch b32 / rust | 1.142 (1.115-1.181) | 1.18 (1.151-1.199) | +3.3% | 1.128, 1.159, 1.161 / 1.173, 1.189, 1.173 | separated, inside spread |
| dense 10 x 30 downstream_batch b512 / numpy | 12.38 (12.11-12.78) | 12.47 (12.37-12.56) | +0.8% | 12.34, 12.45, 12.46 / 12.42, 12.47, 12.5 | within noise |
| dense 10 x 30 downstream_batch b512 / rust | 15.7 (14.93-15.85) | 15.62 (15.27-15.84) | -0.5% | 15.29, 15.7, 15.82 / 15.46, 15.61, 15.72 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 4.957 (4.743-5.059) | 4.941 (4.714-5.095) | -0.3% | 4.886, 4.962, 4.96 / 4.861, 4.867, 5.057 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 1.727 (1.667-1.774) | 1.703 (1.677-1.741) | -1.4% | 1.679, 1.727, 1.77 / 1.7, 1.729, 1.685 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 35.63 (34.56-36.38) | 35.26 (34.57-35.92) | -1.1% | 35.47, 34.84, 36.23 / 34.96, 35.12, 35.68 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / rust | 22.85 (22.4-23.03) | 22.58 (22.48-23.29) | -1.2% | 22.56, 22.99, 22.87 / 22.94, 22.92, 22.48 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 4.478 (4.399-4.748) | 4.465 (4.455-4.794) | -0.3% | 4.405, 4.639, 4.516 / 4.464, 4.625, 4.578 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 1.976 (1.934-2.001) | 1.939 (1.905-1.972) | -1.8% | 1.949, 1.976, 1.995 / 1.928, 1.96, 1.925 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 24.64 (24.4-25.9) | 24.83 (24.51-25.06) | +0.8% | 24.63, 25.15, 24.84 / 24.79, 24.77, 24.92 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 32.48 (32.33-32.85) | 32.65 (32.34-33.27) | +0.5% | 32.59, 32.57, 32.45 / 32.95, 32.83, 32.47 | within noise |
| conv 28x28, 8 ch forward / numpy | 55.06 (54.7-56.37) | 55.15 (54.69-55.99) | +0.2% | 54.99, 54.95, 55.69 / 54.91, 55.5, 55.28 | within noise |
| conv 28x28, 8 ch forward / rust | 19.1 (18.34-19.35) | 19.49 (19.21-19.83) | +2.0% | 18.76, 18.89, 19.3 / 19.21, 19.76, 19.49 | within noise |
| conv 28x28, 8 ch downstream / numpy | 39.43 (38-41.03) | 39.02 (38.73-41.01) | -1.0% | 39.51, 39.9, 39.23 / 39.06, 39.89, 38.95 | within noise |
| conv 28x28, 8 ch downstream / rust | 17.27 (16.75-17.72) | 17.42 (17.11-17.48) | +0.9% | 16.9, 17.45, 17.43 / 17.3, 17.29, 17.43 | within noise |
| conv 28x28, 8 ch accumulate_gradient / numpy | 36.09 (35.32-36.34) | 35.85 (35.37-36.29) | -0.7% | 35.38, 36.09, 36.33 / 36.15, 35.85, 35.48 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 16.09 (16-16.17) | 15.76 (15.72-15.8) | -2.0% | 16.08, 16.04, 16.14 / 15.77, 15.75, 15.77 | consistent |
| conv 28x28, 8 ch forward_batch b32 / numpy | 989.3 (972.7-1004) | 981.9 (965.2-991) | -0.7% | 983.4, 998, 986.7 / 987.3, 971.1, 978.9 | within noise |
| conv 28x28, 8 ch forward_batch b32 / rust | 566.3 (558.7-579) | 572.8 (566.7-588.6) | +1.1% | 559.8, 565.7, 578.4 / 567.2, 583.3, 576.9 | within noise |
| conv 28x28, 8 ch forward_batch b512 / numpy | 1.847e+04 (1.821e+04-1.854e+04) | 1.846e+04 (1.809e+04-1.864e+04) | -0.0% | 1.834e+04, 1.84e+04, 1.847e+04 / 1.823e+04, 1.857e+04, 1.841e+04 | within noise |
| conv 28x28, 8 ch forward_batch b512 / rust | 9231 (8949-9413) | 9450 (9364-9605) | +2.4% | 9117, 9231, 9292 / 9427, 9508, 9485 | separated, inside spread |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 586.8 (579.2-615.1) | 580.7 (578-595.3) | -1.0% | 597.4, 586.7, 586.7 / 578.8, 588.1, 586.7 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / rust | 508.1 (495.7-524.1) | 505.6 (495.3-522) | -0.5% | 508.1, 509.9, 507.4 / 503.7, 504.3, 511 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 1.623e+04 (1.61e+04-1.642e+04) | 1.619e+04 (1.61e+04-1.647e+04) | -0.3% | 1.625e+04, 1.62e+04, 1.63e+04 / 1.614e+04, 1.616e+04, 1.643e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / rust | 1438 (1424-1459) | 1435 (1424-1439) | -0.2% | 1428, 1441, 1451 / 1436, 1433, 1431 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 1321 (1291-1347) | 1220 (1188-1227) | -7.7% | 1291, 1332, 1326 / 1210, 1224, 1203 | consistent |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 535 (529.8-537) | 523.3 (520.3-528.4) | -2.2% | 533.4, 533.4, 535 / 520.6, 526.7, 524.9 | consistent |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 2.03e+04 (1.966e+04-2.166e+04) | 2.033e+04 (2.023e+04-2.039e+04) | +0.1% | 2.066e+04, 2.018e+04, 2.038e+04 / 2.028e+04, 2.036e+04, 2.036e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 1.162e+04 (1.158e+04-1.166e+04) | 1.148e+04 (1.146e+04-1.152e+04) | -1.2% | 1.159e+04, 1.165e+04, 1.162e+04 / 1.146e+04, 1.148e+04, 1.15e+04 | consistent, small |
| conv 8x8, 8 ch forward / numpy | 28.31 (27.86-29.66) | 28.75 (28.25-29.31) | +1.6% | 28.76, 28.63, 28.24 / 28.73, 28.78, 28.75 | within noise |
| conv 8x8, 8 ch forward / rust | 1.526 (1.456-1.615) | 1.523 (1.499-1.609) | -0.2% | 1.484, 1.55, 1.566 / 1.505, 1.535, 1.566 | within noise |
| conv 8x8, 8 ch downstream / numpy | 21.88 (21.63-22.26) | 22.06 (21.77-23.3) | +0.8% | 21.91, 21.85, 22.05 / 22.57, 22.13, 22.01 | within noise |
| conv 8x8, 8 ch downstream / rust | 1.195 (1.185-1.285) | 1.208 (1.191-1.25) | +1.0% | 1.192, 1.203, 1.24 / 1.204, 1.197, 1.232 | within noise |
| conv 8x8, 8 ch accumulate_gradient / numpy | 7.43 (7.264-7.577) | 7.266 (7.135-7.522) | -2.2% | 7.418, 7.323, 7.535 / 7.358, 7.177, 7.345 | within noise |
| conv 8x8, 8 ch accumulate_gradient / rust | 1.174 (1.163-1.192) | 1.159 (1.142-1.182) | -1.3% | 1.178, 1.168, 1.183 / 1.169, 1.152, 1.156 | within noise |
| conv 8x8, 8 ch forward_batch b32 / numpy | 75.04 (74.05-77.06) | 75.92 (74.83-76.52) | +1.2% | 75.14, 75.04, 75.6 / 75.56, 75.93, 75.87 | within noise |
| conv 8x8, 8 ch forward_batch b32 / rust | 31.69 (30.75-32.54) | 31.97 (31.22-32.38) | +0.9% | 30.94, 31.58, 32.46 / 31.59, 32.19, 31.87 | within noise |
| conv 8x8, 8 ch forward_batch b512 / numpy | 893.1 (885.2-901.6) | 886.6 (871-905.8) | -0.7% | 886.4, 899.3, 893.4 / 881.6, 889.5, 888.4 | within noise |
| conv 8x8, 8 ch forward_batch b512 / rust | 485.6 (474.1-494.5) | 501 (485.8-508) | +3.2% | 478.3, 488.5, 489 / 493.2, 506.6, 498.1 | separated, inside spread |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 64.38 (64.09-66.83) | 65.82 (65.03-66.62) | +2.2% | 64.22, 65.58, 64.43 / 65.63, 66.12, 65.82 | separated, inside spread |
| conv 8x8, 8 ch downstream_batch b32 / rust | 27.88 (27.29-29.68) | 27.76 (27.26-28.53) | -0.4% | 28.48, 28.28, 27.78 / 27.49, 27.97, 27.97 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 712.2 (685.8-722.7) | 699.3 (696.9-723.8) | -1.8% | 711.6, 717.4, 699.9 / 697.7, 711.1, 706.7 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / rust | 448.5 (433.9-476.8) | 443.6 (441.7-466.1) | -1.1% | 439.4, 459.6, 455.3 / 453.9, 445.5, 443.6 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 97.15 (94.99-98) | 94.08 (93.07-98.7) | -3.2% | 95.54, 97.89, 97.2 / 94.08, 95.63, 95.89 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 28.37 (28.24-28.46) | 27.1 (27.06-27.32) | -4.5% | 28.39, 28.34, 28.34 / 27.1, 27.1, 27.19 | consistent |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 1462 (1378-1477) | 1402 (1391-1418) | -4.1% | 1417, 1471, 1465 / 1391, 1410, 1407 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 467.4 (459.7-470.5) | 453.9 (450.7-457.1) | -2.9% | 464.7, 469, 465.1 / 452.1, 456.8, 452.5 | consistent |
| conv 13x13x8, 8 ch forward / numpy | 51.21 (50.79-51.4) | 50.65 (49.54-52.55) | -1.1% | 51.21, 51.08, 51.24 / 50.56, 50.66, 51.05 | separated, inside spread |
| conv 13x13x8, 8 ch forward / rust | 20.55 (20.33-20.76) | 20.15 (19.78-20.4) | -2.0% | 20.37, 20.55, 20.73 / 20.07, 20.09, 20.16 | separated, inside spread |
| conv 13x13x8, 8 ch downstream / numpy | 52.18 (50.47-53.69) | 53.04 (51.4-54.75) | +1.7% | 52.85, 51.93, 51.41 / 52.19, 53.93, 52.76 | within noise |
| conv 13x13x8, 8 ch downstream / rust | 12.3 (12.08-12.64) | 12.68 (12.47-12.77) | +3.0% | 12.14, 12.41, 12.45 / 12.54, 12.72, 12.7 | separated, inside spread |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 23.45 (22.99-23.63) | 23.51 (23.22-24.13) | +0.3% | 23.4, 23.52, 23.31 / 23.31, 23.82, 23.52 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 5.451 (5.347-5.653) | 5.049 (4.943-5.381) | -7.4% | 5.466, 5.5, 5.437 / 4.979, 5.273, 5.049 | separated, inside spread |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 1021 (1002-1030) | 1017 (1012-1025) | -0.4% | 1009, 1024, 1027 / 1021, 1018, 1015 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 608.7 (604.6-624.9) | 609.9 (600.2-618.2) | +0.2% | 604.8, 617.7, 611.4 / 604.4, 616.6, 609 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 1.426e+04 (1.406e+04-1.435e+04) | 1.42e+04 (1.41e+04-1.424e+04) | -0.5% | 1.414e+04, 1.433e+04, 1.423e+04 / 1.414e+04, 1.422e+04, 1.421e+04 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 1.832e+04 (1.809e+04-1.843e+04) | 1.822e+04 (1.795e+04-1.823e+04) | -0.5% | 1.826e+04, 1.838e+04, 1.822e+04 / 1.823e+04, 1.809e+04, 1.811e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 923.4 (864.5-933) | 904.8 (853.8-934.8) | -2.0% | 925.1, 928.3, 893.8 / 894.3, 893.3, 904.8 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 353.5 (340-357.9) | 352.4 (345.2-361.9) | -0.3% | 348.4, 350.2, 355.9 / 358.5, 347.4, 351.8 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 2.586e+04 (2.562e+04-2.603e+04) | 2.566e+04 (2.559e+04-2.642e+04) | -0.8% | 2.588e+04, 2.595e+04, 2.569e+04 / 2.58e+04, 2.56e+04, 2.605e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 1055 (1046-1062) | 1049 (1041-1057) | -0.6% | 1051, 1059, 1054 / 1046, 1045, 1054 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 602.9 (588.8-616) | 610.6 (594.6-622.3) | +1.3% | 595.3, 610.9, 601 / 608.1, 611.7, 608.4 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 169.8 (166.2-172.7) | 168.1 (166.3-172.8) | -1.0% | 169.8, 169.9, 169.3 / 168.1, 168.1, 169.6 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.037e+04 (1.021e+04-1.049e+04) | 1.047e+04 (1.036e+04-1.057e+04) | +0.9% | 1.026e+04, 1.041e+04, 1.042e+04 / 1.053e+04, 1.042e+04, 1.046e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 2587 (2518-2613) | 2602 (2526-2617) | +0.6% | 2563, 2561, 2593 / 2571, 2609, 2564 | within noise |
| conv 26x26x8/2, 8 ch forward / numpy | 54.88 (53.65-55.91) | 54.13 (53.25-55.93) | -1.4% | 54.11, 55.55, 54.74 / 53.85, 54.5, 54.59 | within noise |
| conv 26x26x8/2, 8 ch forward / rust | 24.17 (24.03-24.61) | 23.99 (23.63-24.26) | -0.8% | 24.12, 24.36, 24.32 / 23.79, 23.96, 24.14 | within noise |
| conv 26x26x8/2, 8 ch downstream / numpy | 61.96 (61.23-63.49) | 60.88 (60.2-61.81) | -1.8% | 61.65, 63.27, 61.68 / 61.11, 61.42, 60.29 | separated, inside spread |
| conv 26x26x8/2, 8 ch downstream / rust | 15.04 (14.69-15.49) | 15.49 (15.44-15.95) | +3.0% | 14.79, 15.38, 15.04 / 15.49, 15.69, 15.57 | separated, inside spread |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 26.49 (25.94-27.03) | 26.83 (26.43-27.04) | +1.3% | 26.21, 26.5, 26.58 / 26.75, 26.89, 26.68 | separated, inside spread |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 5.835 (5.727-6.022) | 5.905 (5.709-5.976) | +1.2% | 5.901, 5.855, 5.806 / 5.861, 5.944, 5.816 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 1242 (1223-1267) | 1238 (1222-1240) | -0.3% | 1239, 1235, 1251 / 1235, 1231, 1238 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 729.8 (720.2-738.3) | 732.8 (718.9-742.8) | +0.4% | 727.3, 727.9, 734.2 / 729.3, 738.2, 725.5 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 1.727e+04 (1.708e+04-1.742e+04) | 1.731e+04 (1.721e+04-1.751e+04) | +0.2% | 1.722e+04, 1.718e+04, 1.742e+04 / 1.731e+04, 1.732e+04, 1.737e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 2.258e+04 (2.252e+04-2.267e+04) | 2.271e+04 (2.257e+04-2.277e+04) | +0.6% | 2.26e+04, 2.259e+04, 2.257e+04 / 2.273e+04, 2.263e+04, 2.272e+04 | separated, inside spread |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 1201 (1153-1271) | 1197 (1163-1225) | -0.3% | 1212, 1189, 1223 / 1198, 1197, 1193 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 432 (425.9-443.2) | 435.9 (430.5-438.7) | +0.9% | 429.7, 436.6, 436.9 / 432, 438.4, 435.9 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 4.235e+04 (4.203e+04-4.276e+04) | 4.246e+04 (4.209e+04-4.289e+04) | +0.3% | 4.233e+04, 4.239e+04, 4.244e+04 / 4.265e+04, 4.218e+04, 4.269e+04 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 2323 (2308-2342) | 2322 (2314-2331) | -0.0% | 2325, 2327, 2318 / 2321, 2323, 2323 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 717 (701.6-727.2) | 717.7 (707.9-724.7) | +0.1% | 710.4, 710.9, 726.9 / 713.2, 719.9, 717.7 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 201.2 (200.1-208.5) | 203.2 (201.3-205.1) | +1.0% | 204.4, 202.6, 200.8 / 203.2, 203.2, 202.9 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 1.226e+04 (1.209e+04-1.25e+04) | 1.231e+04 (1.227e+04-1.246e+04) | +0.5% | 1.21e+04, 1.235e+04, 1.233e+04 / 1.232e+04, 1.237e+04, 1.231e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 3012 (2974-3076) | 3038 (3001-3084) | +0.9% | 3011, 2991, 3068 / 3006, 3074, 3038 | within noise |
| conv 26x26x8, 8 ch forward / numpy | 126.6 (126.2-128) | 127.3 (126-128.8) | +0.6% | 126.5, 126.8, 127.1 / 127.2, 126.8, 128 | within noise |
| conv 26x26x8, 8 ch forward / rust | 93.88 (92.72-94.83) | 91.78 (90.85-94.34) | -2.2% | 94.19, 92.82, 94.29 / 91.2, 93.14, 91.78 | within noise |
| conv 26x26x8, 8 ch downstream / numpy | 144.7 (144.2-150.4) | 147.6 (144.3-155.4) | +2.0% | 144.8, 147.6, 144.4 / 150.4, 146.5, 148.5 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 59.19 (58.43-61.35) | 61.22 (60.05-62.26) | +3.4% | 58.65, 59.31, 60.53 / 61.16, 61.15, 61.25 | separated, inside spread |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 89.27 (87.45-91.29) | 89.55 (88.76-90.95) | +0.3% | 89.37, 90, 89.27 / 90.09, 90.1, 88.92 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 25.23 (24.86-25.41) | 25.13 (24.8-25.49) | -0.4% | 25.37, 25.08, 25.02 / 25.14, 25.13, 25.07 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 4269 (4178-4389) | 4314 (4270-4402) | +1.1% | 4238, 4322, 4265 / 4335, 4308, 4340 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 2963 (2950-3018) | 2953 (2939-2965) | -0.4% | 2963, 2969, 2984 / 2952, 2953, 2953 | separated, inside spread |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 6.76e+04 (6.699e+04-6.77e+04) | 6.773e+04 (6.747e+04-6.825e+04) | +0.2% | 6.727e+04, 6.747e+04, 6.769e+04 / 6.759e+04, 6.786e+04, 6.786e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 8.548e+04 (8.501e+04-8.563e+04) | 8.507e+04 (8.478e+04-8.583e+04) | -0.5% | 8.545e+04, 8.549e+04, 8.525e+04 / 8.533e+04, 8.527e+04, 8.507e+04 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 4762 (4635-4837) | 4858 (4672-4994) | +2.0% | 4787, 4794, 4701 / 4866, 4876, 4766 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 397.3 (384.6-417) | 391.1 (389.6-424.1) | -1.6% | 395.7, 393.3, 404.9 / 406.9, 390.3, 391.8 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 1.129e+05 (1.121e+05-1.146e+05) | 1.13e+05 (1.125e+05-1.152e+05) | +0.1% | 1.122e+05, 1.129e+05, 1.143e+05 / 1.126e+05, 1.13e+05, 1.141e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 5013 (4996-5076) | 5010 (4939-5083) | -0.1% | 5013, 5024, 5038 / 5001, 5044, 4977 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 3011 (2950-3114) | 3048 (3018-3080) | +1.2% | 2981, 3023, 3061 / 3035, 3052, 3059 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 662.8 (653.8-681.2) | 668.5 (666.3-692) | +0.9% | 659.3, 657.9, 673.5 / 677.6, 679.2, 666.9 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 5.149e+04 (5.076e+04-5.222e+04) | 5.175e+04 (5.134e+04-5.238e+04) | +0.5% | 5.14e+04, 5.185e+04, 5.13e+04 / 5.196e+04, 5.174e+04, 5.171e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 1.2e+04 (1.168e+04-1.205e+04) | 1.204e+04 (1.2e+04-1.21e+04) | +0.3% | 1.187e+04, 1.186e+04, 1.201e+04 / 1.206e+04, 1.203e+04, 1.206e+04 | separated, inside spread |
| pool 26x26, 8 ch forward / numpy | 69.98 (69.44-71.72) | 70.68 (69.94-71.28) | +1.0% | 69.91, 70.83, 69.84 / 70.44, 70.82, 70.83 | within noise |
| pool 26x26, 8 ch forward / rust | 3.708 (3.686-3.758) | 3.032 (2.982-3.079) | -18.2% | 3.701, 3.727, 3.725 / 3.045, 3.038, 3.016 | consistent |
| pool 26x26, 8 ch downstream / numpy | 35.15 (34.73-35.98) | 34.98 (34.08-37.66) | -0.5% | 34.85, 35.87, 35.14 / 36.03, 34.41, 35.94 | within noise |
| pool 26x26, 8 ch downstream / rust | 5.148 (5.102-5.237) | 4.14 (4.074-4.229) | -19.6% | 5.11, 5.19, 5.169 / 4.148, 4.161, 4.119 | consistent |
| pool 26x26, 8 ch forward_batch b32 / numpy | 1240 (1220-1245) | 1225 (1220-1251) | -1.2% | 1232, 1235, 1240 / 1237, 1224, 1231 | within noise |
| pool 26x26, 8 ch forward_batch b32 / rust | 112.1 (110.6-113.3) | 91.41 (90.28-92.57) | -18.5% | 111, 112.2, 112.9 / 90.84, 91.55, 92 | consistent |
| pool 26x26, 8 ch forward_batch b512 / numpy | 2.029e+04 (2.013e+04-2.048e+04) | 2.023e+04 (2.015e+04-2.037e+04) | -0.3% | 2.021e+04, 2.027e+04, 2.046e+04 / 2.029e+04, 2.019e+04, 2.025e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 2409 (2396-2421) | 2218 (2201-2239) | -7.9% | 2408, 2404, 2410 / 2213, 2220, 2220 | consistent |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 485.8 (478.1-491.1) | 494.8 (476.5-501) | +1.9% | 484.3, 490.1, 480.5 / 493.2, 495.9, 487.3 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / rust | 159.3 (157.6-161.2) | 132.7 (132.3-135) | -16.7% | 157.6, 160.2, 159.8 / 132.6, 133.6, 133.7 | consistent |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 1.368e+04 (1.362e+04-1.388e+04) | 1.372e+04 (1.364e+04-1.388e+04) | +0.3% | 1.367e+04, 1.375e+04, 1.369e+04 / 1.376e+04, 1.369e+04, 1.379e+04 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / rust | 3004 (3000-3010) | 2610 (2606-2626) | -13.1% | 3004, 3005, 3004 / 2618, 2608, 2614 | consistent |
| pool 6x6, 8 ch forward / numpy | 33.77 (33.17-34.38) | 33.82 (33.53-34.95) | +0.2% | 34.16, 33.9, 33.23 / 34.15, 33.82, 34.24 | within noise |
| pool 6x6, 8 ch forward / rust | 0.4973 (0.4808-0.5022) | 0.4584 (0.4568-0.4674) | -7.8% | 0.4883, 0.4967, 0.5004 / 0.4581, 0.4619, 0.4622 | consistent |
| pool 6x6, 8 ch downstream / numpy | 19.06 (18.81-19.23) | 19.58 (18.81-19.99) | +2.7% | 19.17, 18.86, 19.09 / 19.4, 19.61, 19.33 | separated, inside spread |
| pool 6x6, 8 ch downstream / rust | 0.5762 (0.56-0.5791) | 0.4478 (0.4457-0.4579) | -22.3% | 0.5685, 0.5773, 0.576 / 0.4478, 0.4459, 0.4531 | consistent |
| pool 6x6, 8 ch forward_batch b32 / numpy | 108.1 (107.5-111) | 108.7 (108-110.1) | +0.6% | 108.5, 107.9, 109.5 / 108.4, 109.3, 109.2 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 8.297 (8.195-8.423) | 6.931 (6.822-6.995) | -16.5% | 8.203, 8.373, 8.323 / 6.872, 6.968, 6.931 | consistent |
| pool 6x6, 8 ch forward_batch b512 / numpy | 1226 (1210-1238) | 1215 (1206-1228) | -0.9% | 1216, 1222, 1234 / 1215, 1209, 1225 | within noise |
| pool 6x6, 8 ch forward_batch b512 / rust | 129.4 (127.5-131) | 108.4 (106.9-109.3) | -16.2% | 127.9, 129.4, 130.7 / 107.4, 108.9, 108.6 | consistent |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 59.85 (59.48-60.77) | 60.75 (59.52-61.99) | +1.5% | 59.81, 60.3, 59.68 / 60.76, 60.75, 60.66 | separated, inside spread |
| pool 6x6, 8 ch downstream_batch b32 / rust | 11.34 (11.18-11.49) | 7.764 (7.601-7.819) | -31.5% | 11.19, 11.42, 11.38 / 7.675, 7.799, 7.728 | consistent |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 598.7 (588.1-611.7) | 600.9 (591.6-604.1) | +0.4% | 594.7, 603.9, 597.7 / 602.6, 593, 602.3 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 180.1 (176.7-183.1) | 121.9 (120.5-123) | -32.3% | 176.7, 180.5, 182.3 / 122.3, 121.5, 121.5 | consistent |
| conv tail 32 x 5408 bare downstream b32 / numpy | 78.68 (66.42-78.8) | 71.94 (70.73-78.68) | -8.6% | 72.54, 78.74, 75.02 / 75.2, 74.53, 71.46 | within noise |
| conv tail 32 x 5408 bare downstream b32 / rust | 252.3 (249-259.3) | 248.3 (245.9-254.7) | -1.6% | 251.5, 249.9, 257.3 / 252.1, 247.5, 247.1 | within noise |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3206 (3181-3234) | 3198 (3086-3222) | -0.3% | 3209, 3194, 3207 / 3192, 3221, 3139 | within noise |
| conv tail 32 x 5408 bare downstream b512 / rust | 2422 (2408-2441) | 2278 (2257-2303) | -6.0% | 2435, 2410, 2426 / 2278, 2280, 2278 | consistent |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 78.97 (77.95-79.79) | 79.49 (78.93-80.05) | +0.7% | 78.36, 79.53, 78.97 / 79.36, 79.49, 79.54 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / rust | 239.7 (235.7-246.9) | 228.5 (221.8-234.6) | -4.6% | 237.4, 242.8, 241.5 / 231, 224.1, 231.3 | separated, inside spread |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 1613 (1605-1637) | 1640 (1611-1672) | +1.6% | 1610, 1610, 1634 / 1650, 1634, 1640 | separated, inside spread |
| conv tail 32 x 5408 bare accumulate b512 / rust | 2237 (2183-2266) | 2227 (2181-2235) | -0.5% | 2208, 2254, 2238 / 2208, 2216, 2230 | within noise |
| conv tail 32 x 5408 transpose b32 / numpy | 0.7217 (0.7054-0.7377) | 0.7195 (0.7115-0.7308) | -0.3% | 0.7215, 0.7265, 0.7167 / 0.7179, 0.7195, 0.7211 | within noise |
| conv tail 32 x 5408 transpose b32 / rust | 0.8354 (0.8271-0.8596) | 0.8633 (0.8553-0.868) | +3.4% | 0.8433, 0.8329, 0.8354 / 0.8605, 0.8633, 0.8637 | consistent |
| conv tail 32 x 5408 transpose b512 / numpy | 11.71 (11.08-13.16) | 13.04 (11.16-13.6) | +11.4% | 12.56, 11.27, 11.83 / 13.12, 13.27, 11.31 | within noise |
| conv tail 32 x 5408 transpose b512 / rust | 12.64 (12.36-12.79) | 14.11 (13.68-14.53) | +11.6% | 12.46, 12.68, 12.73 / 13.75, 14.31, 14.23 | consistent |
| conv tail 32 x 5408 add b32 / numpy | 95.33 (95.1-98.16) | 96.72 (94.93-100.9) | +1.5% | 96.63, 95.26, 95.49 / 99.37, 95.26, 97.84 | within noise |
| conv tail 32 x 5408 add b32 / rust | 63.14 (63-66.16) | 63.14 (62.99-69.43) | -0.0% | 63.06, 64.58, 64.61 / 64.57, 63.08, 66.27 | within noise |
| conv tail 32 x 5408 add b512 / numpy | 95.73 (94.02-97.1) | 96.91 (94.5-99.98) | +1.2% | 95.78, 95.75, 95.4 / 97.09, 94.72, 98.42 | within noise |
| conv tail 32 x 5408 add b512 / rust | 63.1 (62.82-65.95) | 62.44 (62.25-65.63) | -1.1% | 62.99, 63.24, 64.5 / 65.55, 62.32, 62.44 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 1.438 (1.369-1.491) | 1.462 (1.422-1.494) | +1.7% | 1.402, 1.477, 1.426 / 1.47, 1.458, 1.462 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.4406 (0.429-0.4482) | 0.4115 (0.4058-0.4249) | -6.6% | 0.4381, 0.4385, 0.4438 / 0.4073, 0.4195, 0.4161 | consistent |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 11.38 (11.32-11.53) | 10.48 (10.4-10.63) | -8.0% | 11.34, 11.46, 11.43 / 10.43, 10.56, 10.51 | consistent |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 4.877 (4.815-4.978) | 4.592 (4.487-4.641) | -5.8% | 4.843, 4.929, 4.912 / 4.592, 4.489, 4.634 | consistent |
| dense 30 x 784 bare downstream b32 / numpy | 23.68 (23.21-23.9) | 23.16 (22.61-23.39) | -2.2% | 23.52, 23.56, 23.77 / 22.86, 23.01, 23.32 | separated, inside spread |
| dense 30 x 784 bare downstream b32 / rust | 30.14 (28.84-30.67) | 29.04 (28.19-29.77) | -3.7% | 29.87, 30.16, 29.75 / 29.04, 28.83, 29.19 | consistent |
| dense 30 x 784 bare downstream b512 / numpy | 138.5 (136.7-142.7) | 140.3 (136.4-143.6) | +1.3% | 138.3, 138.6, 140.1 / 141.2, 140, 140.2 | within noise |
| dense 30 x 784 bare downstream b512 / rust | 245.4 (242.9-249.9) | 245.8 (242.7-247.9) | +0.2% | 246.8, 245.4, 246.4 / 245.8, 243.6, 247.5 | within noise |
| dense 30 x 784 bare accumulate b32 / numpy | 28.81 (28.22-29.39) | 29.17 (29.01-29.73) | +1.2% | 28.81, 28.85, 28.8 / 29.37, 29.17, 29.38 | consistent, small |
| dense 30 x 784 bare accumulate b32 / rust | 33.12 (31.97-33.52) | 32.17 (31.16-33.15) | -2.9% | 32.86, 33.18, 32.55 / 32.47, 31.7, 32.52 | separated, inside spread |
| dense 30 x 784 bare accumulate b512 / numpy | 195.4 (194.7-196.5) | 195.4 (194-200.6) | -0.0% | 195.3, 196, 195.1 / 196.2, 194.7, 197.3 | within noise |
| dense 30 x 784 bare accumulate b512 / rust | 281.1 (275.6-297.1) | 283.9 (275.1-289.7) | +1.0% | 282.6, 279.6, 286.3 / 281.2, 289.7, 279.2 | within noise |
| dense 30 x 784 transpose b32 / numpy | 0.6908 (0.6828-0.7073) | 0.6957 (0.6864-0.7089) | +0.7% | 0.6835, 0.7045, 0.6908 / 0.6919, 0.6918, 0.7022 | within noise |
| dense 30 x 784 transpose b32 / rust | 0.8105 (0.791-0.8186) | 0.8285 (0.8251-0.8432) | +2.2% | 0.8048, 0.8105, 0.8111 / 0.8339, 0.8269, 0.8347 | consistent |
| dense 30 x 784 transpose b512 / numpy | 7.23 (7.101-7.279) | 7.237 (7.147-7.471) | +0.1% | 7.272, 7.153, 7.199 / 7.182, 7.363, 7.27 | within noise |
| dense 30 x 784 transpose b512 / rust | 13.32 (12.83-13.58) | 14.46 (13.34-14.94) | +8.5% | 13.32, 13.47, 12.91 / 14.03, 14.82, 13.77 | separated, inside spread |
| dense 30 x 784 add b32 / numpy | 11.07 (10.64-11.39) | 9.589 (8.996-10.71) | -13.3% | 10.88, 11.2, 10.9 / 9.855, 9.122, 9.985 | consistent |
| dense 30 x 784 add b32 / rust | 8.77 (8.495-9.087) | 9.131 (8.707-9.598) | +4.1% | 8.608, 8.881, 8.951 / 8.867, 9.144, 9.417 | within noise |
| dense 30 x 784 add b512 / numpy | 12.4 (12.29-12.62) | 12.35 (12.24-13.14) | -0.4% | 12.53, 12.48, 12.32 / 12.28, 12.35, 13.05 | within noise |
| dense 30 x 784 add b512 / rust | 8.638 (8.487-9.516) | 8.87 (8.525-9.14) | +2.7% | 8.638, 8.499, 9.267 / 8.717, 8.818, 9.013 | within noise |
| dense 30 x 784 sum_axis0 b32 / numpy | 1.494 (1.46-1.525) | 1.482 (1.443-1.508) | -0.8% | 1.493, 1.494, 1.485 / 1.455, 1.483, 1.502 | within noise |
| dense 30 x 784 sum_axis0 b32 / rust | 0.3973 (0.392-0.4011) | 0.3869 (0.3833-0.4063) | -2.6% | 0.396, 0.398, 0.3964 / 0.3861, 0.3993, 0.3848 | within noise |
| dense 30 x 784 sum_axis0 b512 / numpy | 10.96 (10.7-11.05) | 10.9 (10.76-11.14) | -0.6% | 10.8, 10.87, 11.03 / 10.93, 10.81, 11.04 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 4.231 (4.146-4.301) | 4.222 (4.032-4.238) | -0.2% | 4.181, 4.287, 4.203 / 4.126, 4.2, 4.225 | within noise |
| dense 10 x 30 bare downstream b32 / numpy | 1.828 (1.78-1.842) | 1.842 (1.792-1.947) | +0.7% | 1.809, 1.839, 1.804 / 1.818, 1.875, 1.879 | within noise |
| dense 10 x 30 bare downstream b32 / rust | 1.169 (1.147-1.189) | 1.117 (1.107-1.195) | -4.5% | 1.156, 1.182, 1.169 / 1.151, 1.123, 1.115 | separated, inside spread |
| dense 10 x 30 bare downstream b512 / numpy | 11.88 (11.79-12.11) | 12 (11.81-12.34) | +1.0% | 11.86, 11.91, 11.95 / 11.95, 11.98, 12.17 | separated, inside spread |
| dense 10 x 30 bare downstream b512 / rust | 15.97 (15.5-16.07) | 16.04 (15.7-16.41) | +0.4% | 15.69, 15.93, 16.07 / 15.77, 16.14, 16.23 | within noise |
| dense 10 x 30 bare accumulate b32 / numpy | 1.784 (1.768-1.882) | 1.829 (1.787-1.978) | +2.5% | 1.776, 1.833, 1.802 / 1.806, 1.905, 1.827 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 1.209 (1.205-1.219) | 1.196 (1.189-1.213) | -1.0% | 1.208, 1.216, 1.206 / 1.201, 1.191, 1.206 | separated, inside spread |
| dense 10 x 30 bare accumulate b512 / numpy | 13.51 (13.3-13.65) | 13.54 (13.33-13.73) | +0.2% | 13.39, 13.58, 13.47 / 13.43, 13.54, 13.59 | within noise |
| dense 10 x 30 bare accumulate b512 / rust | 25.31 (25.14-25.95) | 25.23 (25.17-26.88) | -0.3% | 25.23, 25.63, 25.39 / 25.2, 25.48, 26.06 | within noise |
| dense 10 x 30 transpose b32 / numpy | 0.4463 (0.4434-0.4621) | 0.4473 (0.4455-0.4654) | +0.2% | 0.4451, 0.4492, 0.4541 / 0.4476, 0.4557, 0.4471 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.3824 (0.3792-0.3877) | 0.3856 (0.3827-0.3878) | +0.8% | 0.3835, 0.3838, 0.3807 / 0.3827, 0.3872, 0.386 | within noise |
| dense 10 x 30 transpose b512 / numpy | 2.962 (2.895-3.019) | 2.931 (2.91-2.995) | -1.1% | 2.962, 2.977, 2.94 / 2.941, 2.931, 2.959 | within noise |
| dense 10 x 30 transpose b512 / rust | 4.154 (4.111-4.224) | 4.01 (3.961-4.184) | -3.5% | 4.124, 4.172, 4.172 / 4.002, 3.997, 4.085 | separated, inside spread |
| dense 10 x 30 add b32 / numpy | 0.4105 (0.4092-0.4186) | 0.4104 (0.4065-0.4189) | -0.0% | 0.4099, 0.4139, 0.4106 / 0.4076, 0.4142, 0.4145 | within noise |
| dense 10 x 30 add b32 / rust | 0.1938 (0.1931-0.1991) | 0.1939 (0.1902-0.1977) | +0.1% | 0.194, 0.1961, 0.1938 / 0.1942, 0.1961, 0.1909 | within noise |
| dense 10 x 30 add b512 / numpy | 0.4199 (0.4164-0.4229) | 0.4235 (0.4219-0.4308) | +0.9% | 0.418, 0.4224, 0.4183 / 0.4243, 0.4263, 0.4235 | separated, inside spread |
| dense 10 x 30 add b512 / rust | 0.2031 (0.1996-0.2202) | 0.2037 (0.2016-0.2188) | +0.3% | 0.2099, 0.2041, 0.2031 / 0.2102, 0.2053, 0.2025 | within noise |
| dense 10 x 30 sum_axis0 b32 / numpy | 1.298 (1.282-1.348) | 1.322 (1.278-1.351) | +1.9% | 1.286, 1.326, 1.296 / 1.347, 1.32, 1.292 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.2864 (0.2822-0.2896) | 0.2848 (0.2809-0.2885) | -0.5% | 0.2847, 0.2881, 0.2862 / 0.2835, 0.2864, 0.2837 | within noise |
| dense 10 x 30 sum_axis0 b512 / numpy | 9.2 (8.959-9.268) | 9.107 (9.068-9.247) | -1.0% | 9.077, 9.261, 9.134 / 9.167, 9.127, 9.098 | within noise |
| dense 10 x 30 sum_axis0 b512 / rust | 2.567 (2.542-2.603) | 2.639 (2.617-2.664) | +2.8% | 2.545, 2.567, 2.596 / 2.627, 2.635, 2.652 | separated, inside spread |
| attention 16 x 32 forward_batch b32 / numpy | 289.3 (287.1-294.4) | 287.7 (286.9-291.3) | -0.6% | 287.3, 291, 291.1 / 287, 289.6, 289.3 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 364.6 (360.2-367.9) | 391.8 (390.3-404.3) | +7.5% | 361.5, 366.8, 365.5 / 391.7, 390.7, 400.3 | consistent |
| attention 16 x 32 forward_batch b512 / numpy | 5146 (5107-5212) | 5085 (5060-5143) | -1.2% | 5125, 5130, 5211 / 5087, 5112, 5074 | separated, inside spread |
| attention 16 x 32 forward_batch b512 / rust | 5632 (5546-5735) | 6101 (6036-6143) | +8.3% | 5588, 5651, 5685 / 6101, 6097, 6072 | consistent |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 265.4 (262.7-270.4) | 263.1 (261-264.7) | -0.9% | 263.2, 266.6, 268.6 / 263.8, 262.9, 262.5 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / rust | 251.3 (246.3-254) | 249.4 (245.9-252.9) | -0.7% | 249.2, 251.5, 252.3 / 247.6, 249.7, 250.4 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 4558 (4537-4645) | 4597 (4548-4639) | +0.9% | 4556, 4553, 4601 / 4569, 4639, 4585 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / rust | 4727 (4613-4757) | 4689 (4603-4755) | -0.8% | 4687, 4685, 4727 / 4648, 4721, 4658 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 251.4 (242.9-284.3) | 246.9 (242.9-259.5) | -1.8% | 249.1, 268.6, 248.3 / 245.6, 247.1, 251.2 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 216.7 (209-220.5) | 219 (209.5-231.3) | +1.1% | 214.8, 214.5, 218.9 / 220.4, 219, 217.1 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5520 (5457-5680) | 5492 (5455-5681) | -0.5% | 5506, 5485, 5625 / 5471, 5516, 5589 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 4047 (4009-4132) | 4034 (4013-4054) | -0.3% | 4070, 4047, 4080 / 4036, 4024, 4041 | separated, inside spread |
