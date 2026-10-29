Old `6dcd34c` against new `6dcd34c`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `3b5ccd7` (extension sha256 `32ad9eba76b4`) and new crate `f18ca4a` (extension sha256 `be447c7907d0`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.59 (measured just after this run's crate builds); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / dense 10 x 30 forward_batch b512 / rust -54.5% (77.73 -> 35.39 µs)
- consistent: per call / dense 10 x 30 forward_batch b32 / rust -52.5% (5.232 -> 2.487 µs)
- consistent: per call / dense 30 x 784 forward_batch b512 / rust -31.7% (427.7 -> 292.3 µs)
- consistent: per call / dense 10 x 30 forward / rust -18.6% (0.3841 -> 0.3126 µs)
- consistent: per call / dense 30 x 784 forward_batch b32 / rust -16.0% (54.64 -> 45.89 µs)
- consistent: per call / attention 16 x 32 forward_batch b512 / rust -10.1% (6081 -> 5466 µs)
- consistent: per call / attention 16 x 32 forward_batch b32 / rust -9.4% (387.9 -> 351.4 µs)
- 263 rows within noise (16 separated inside their spread), max |Δ| 10.3%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 28.15 (27.43-29.92) | 29.83 (28.38-29.99) | +6.0% | 27.55, 29.27, 28.74 / 28.39, 29.96, 29.83 | within noise |
| conv tail 32 x 5408 forward / rust | 21.8 (19.3-22.99) | 20.63 (18.99-22.73) | -5.4% | 19.34, 21.8, 22.9 / 20.95, 19.79, 21.55 | within noise |
| conv tail 32 x 5408 downstream / numpy | 24.25 (23.36-24.94) | 25.16 (23.31-25.96) | +3.8% | 23.74, 24.16, 24.47 / 23.99, 24.63, 25.78 | within noise |
| conv tail 32 x 5408 downstream / rust | 21.47 (20.69-23.58) | 22.86 (20.92-23.71) | +6.5% | 21.36, 22.26, 21.34 / 22.3, 23.67, 22.07 | within noise |
| conv tail 32 x 5408 hidden_delta / numpy | 33.12 (31.29-34.17) | 32.6 (32.41-34.53) | -1.6% | 31.56, 33.32, 33.84 / 32.51, 32.52, 34.17 | within noise |
| conv tail 32 x 5408 hidden_delta / rust | 23.71 (22.96-26.15) | 25.15 (22.95-26.26) | +6.1% | 22.99, 24.67, 24.41 / 24.41, 26.12, 24.33 | within noise |
| conv tail 32 x 5408 accumulate_gradient / numpy | 88.43 (85.16-95.88) | 88.18 (85.27-93.16) | -0.3% | 87.03, 92.25, 88.02 / 88.05, 88.09, 90.66 | within noise |
| conv tail 32 x 5408 accumulate_gradient / rust | 55.26 (54.51-57.25) | 56.02 (55.01-56.44) | +1.4% | 55.26, 55.37, 55.95 / 56.02, 56.31, 55.22 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 179.1 (176.5-183.8) | 180.8 (176.9-184.2) | +0.9% | 177.1, 178.9, 182.2 / 180.7, 180.8, 180.6 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 109.9 (106.8-112.3) | 112.1 (106.6-114.9) | +2.0% | 109.3, 109.5, 111.1 / 108, 112.3, 113.7 | within noise |
| conv tail 32 x 5408 sgd step / numpy | 267.3 (263.9-275.8) | 273.4 (270-276.9) | +2.3% | 264.2, 269.8, 273 / 273.5, 273.5, 273.2 | separated, inside spread |
| conv tail 32 x 5408 sgd step / rust | 59.88 (58.93-61.37) | 59.57 (58.76-61.12) | -0.5% | 59.18, 60.41, 60.73 / 58.88, 60.86, 59.57 | within noise |
| conv tail 32 x 5408 forward_batch b32 / numpy | 151.1 (145.2-159.5) | 152.3 (147.5-159.5) | +0.8% | 146.5, 150.1, 158.1 / 147.6, 152.3, 159.3 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 366.2 (348-372.8) | 357.9 (338.8-394.1) | -2.3% | 360.9, 355.8, 369.2 / 346.8, 375.9, 368.4 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1163 (1050-1165) | 1163 (1162-1174) | -0.0% | 1102, 1163, 1165 / 1163, 1162, 1171 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1940 (1838-1970) | 1816 (1798-1828) | -6.4% | 1876, 1940, 1968 / 1811, 1821, 1816 | separated, inside spread |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 79.46 (78.35-80.29) | 79.27 (78.53-80.06) | -0.2% | 78.89, 79.77, 79.62 / 78.7, 79.37, 79.62 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 247.6 (237.3-248.9) | 248.4 (240.6-252.4) | +0.3% | 239, 248, 248.6 / 244.8, 248.4, 250 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3103 (3070-3115) | 3089 (3053-3105) | -0.5% | 3099, 3109, 3089 / 3090, 3097, 3068 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2435 (2428-2477) | 2437 (2427-2470) | +0.1% | 2456, 2446, 2433 / 2448, 2451, 2437 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 624.7 (612.5-637.5) | 624 (604.9-631.8) | -0.1% | 622.6, 627.8, 622.2 / 627.4, 614.1, 626.9 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 312.4 (304.9-326) | 310.5 (305.2-324.1) | -0.6% | 305.6, 312.4, 321 / 305.4, 314.6, 317.1 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 1.212e+04 (1.208e+04-1.22e+04) | 1.227e+04 (1.212e+04-1.255e+04) | +1.3% | 1.21e+04, 1.21e+04, 1.219e+04 / 1.218e+04, 1.238e+04, 1.232e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 5799 (5755-5855) | 5818 (5787-5844) | +0.3% | 5805, 5823, 5780 / 5790, 5836, 5818 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 167.1 (160.7-172.8) | 164.7 (163.3-167.9) | -1.5% | 163.3, 170.2, 167.5 / 164.1, 166.6, 164.4 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 278.5 (269.1-284.7) | 278 (268.5-286.9) | -0.2% | 269.5, 279.4, 283.6 / 272.1, 283.7, 278.8 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 1850 (1823-1924) | 1833 (1813-1864) | -0.9% | 1837, 1845, 1890 / 1825, 1863, 1826 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 2344 (2326-2574) | 2348 (2288-2363) | +0.2% | 2345, 2459, 2334 / 2323, 2359, 2324 | within noise |
| dense 30 x 784 forward / numpy | 8.241 (7.9-8.325) | 8.084 (7.852-8.359) | -1.9% | 8.045, 8.153, 8.297 / 7.999, 8.004, 8.353 | within noise |
| dense 30 x 784 forward / rust | 2.915 (2.823-2.953) | 2.614 (2.563-2.781) | -10.3% | 2.872, 2.871, 2.934 / 2.587, 2.614, 2.759 | separated, inside spread |
| dense 30 x 784 downstream / numpy | 3.971 (3.801-4.068) | 3.966 (3.761-4.054) | -0.1% | 3.907, 3.928, 3.998 / 3.858, 3.909, 4.041 | within noise |
| dense 30 x 784 downstream / rust | 2.103 (2.04-2.38) | 2.08 (1.951-2.223) | -1.1% | 2.051, 2.102, 2.271 / 2.087, 2.059, 2.121 | within noise |
| dense 30 x 784 hidden_delta / numpy | 6.771 (6.625-6.931) | 6.94 (6.675-7.258) | +2.5% | 6.791, 6.646, 6.891 / 7.011, 6.806, 6.949 | within noise |
| dense 30 x 784 hidden_delta / rust | 2.654 (2.522-2.988) | 2.583 (2.498-2.695) | -2.7% | 2.802, 2.607, 2.686 / 2.596, 2.583, 2.598 | separated, inside spread |
| dense 30 x 784 accumulate_gradient / numpy | 27.88 (27.46-28.3) | 28.02 (27.1-29.26) | +0.5% | 27.88, 27.5, 28.28 / 27.61, 28.12, 28.58 | within noise |
| dense 30 x 784 accumulate_gradient / rust | 6.906 (6.786-7.109) | 7.006 (6.69-7.228) | +1.4% | 6.818, 6.906, 7.098 / 6.959, 7.028, 7.006 | within noise |
| dense 30 x 784 apply_accumulated_gradient / numpy | 31 (30.8-32.63) | 31.78 (31-32.98) | +2.5% | 31.86, 30.84, 31.39 / 31.42, 32.04, 32.06 | within noise |
| dense 30 x 784 apply_accumulated_gradient / rust | 16.82 (16.5-17.53) | 16.88 (16.54-17.35) | +0.3% | 16.56, 16.89, 17.26 / 16.67, 16.77, 17.31 | within noise |
| dense 30 x 784 sgd step / numpy | 59.24 (58.78-60.29) | 59.16 (58.55-60.21) | -0.1% | 59.06, 59.67, 59.6 / 59.44, 58.62, 59.81 | within noise |
| dense 30 x 784 sgd step / rust | 7.318 (7.285-7.921) | 7.438 (7.24-7.695) | +1.6% | 7.296, 7.341, 7.608 / 7.452, 7.273, 7.633 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 38.49 (37.77-39.15) | 38.31 (37.6-39.41) | -0.5% | 38.85, 38.38, 38.1 / 38.18, 38.92, 38.1 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 54.64 (53.14-55.58) | 45.89 (45.15-47.22) | -16.0% | 53.4, 54.64, 55.42 / 45.86, 45.36, 46.71 | consistent |
| dense 30 x 784 forward_batch b512 / numpy | 266.9 (223.1-270.4) | 267.2 (264.9-270.2) | +0.1% | 244.6, 266.9, 270 / 265.1, 267.2, 269.3 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 427.7 (417.7-444.2) | 292.3 (288.4-296.4) | -31.7% | 430.9, 431.7, 427.5 / 291.3, 290, 294.7 | consistent |
| dense 30 x 784 downstream_batch b32 / numpy | 23.9 (23.51-24.43) | 24.07 (23.53-24.31) | +0.7% | 23.67, 24.03, 24.08 / 23.77, 24.1, 24.13 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 33.02 (32.22-34.4) | 33.13 (32.31-34.21) | +0.3% | 32.53, 33.8, 33.48 / 32.66, 33.1, 34.19 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 131.8 (129.6-133) | 131 (130.3-131.8) | -0.6% | 131.4, 131.8, 130.7 / 130.4, 131.2, 131.3 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 245.7 (243.4-248.2) | 247.8 (243.9-249.6) | +0.8% | 244, 245.9, 246.9 / 246.9, 245.5, 248.5 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 62.37 (61.96-65.8) | 62.3 (61.71-64.49) | -0.1% | 62.35, 64.04, 63.11 / 63.26, 62.01, 62.81 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / rust | 43.16 (42.39-45.02) | 43.04 (42.14-44.18) | -0.3% | 42.65, 44.22, 43.39 / 42.47, 42.99, 44.1 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 1717 (1633-1729) | 1707 (1686-1727) | -0.6% | 1678, 1728, 1695 / 1702, 1715, 1699 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / rust | 500.6 (496.8-511.4) | 505.2 (491.7-517.8) | +0.9% | 505.6, 500.1, 499.1 / 509, 498.7, 509.8 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 40.29 (39.57-40.85) | 40.2 (39.38-40.76) | -0.2% | 39.93, 40.27, 40.79 / 39.98, 39.81, 40.71 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 40.1 (39.35-40.59) | 40.09 (39.17-41.19) | -0.0% | 39.67, 40.27, 40.33 / 39.81, 39.74, 41.12 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 222.5 (218.4-223.4) | 223.3 (220.5-224.3) | +0.4% | 219.9, 223, 222.8 / 223.8, 221.7, 223.6 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 310 (306.2-313.7) | 314.7 (308.6-318) | +1.5% | 307.8, 310.1, 312.2 / 313, 313.1, 315.9 | separated, inside spread |
| dense 10 x 30 forward / numpy | 4.457 (4.331-4.766) | 4.603 (4.435-4.822) | +3.3% | 4.532, 4.333, 4.594 / 4.663, 4.504, 4.654 | within noise |
| dense 10 x 30 forward / rust | 0.3841 (0.3716-0.3977) | 0.3126 (0.3096-0.3175) | -18.6% | 0.3749, 0.3867, 0.3901 / 0.31, 0.3126, 0.3168 | consistent |
| dense 10 x 30 downstream / numpy | 0.8338 (0.8037-0.8703) | 0.8308 (0.8214-0.8622) | -0.4% | 0.8183, 0.8317, 0.8568 / 0.8242, 0.8381, 0.8476 | within noise |
| dense 10 x 30 downstream / rust | 0.1996 (0.1957-0.2235) | 0.2017 (0.1976-0.207) | +1.0% | 0.1958, 0.2027, 0.2122 / 0.2014, 0.2022, 0.2041 | within noise |
| dense 10 x 30 hidden_delta / numpy | 2.267 (2.236-2.313) | 2.244 (2.199-2.265) | -1.0% | 2.262, 2.275, 2.276 / 2.209, 2.244, 2.262 | within noise |
| dense 10 x 30 hidden_delta / rust | 0.4322 (0.4171-0.4611) | 0.4346 (0.4239-0.449) | +0.6% | 0.4192, 0.4472, 0.433 / 0.4414, 0.4339, 0.4308 | within noise |
| dense 10 x 30 accumulate_gradient / numpy | 2.918 (2.855-2.957) | 2.884 (2.827-3.047) | -1.2% | 2.909, 2.934, 2.892 / 2.941, 2.857, 2.913 | within noise |
| dense 10 x 30 accumulate_gradient / rust | 0.3995 (0.3876-0.4089) | 0.3986 (0.3942-0.4015) | -0.2% | 0.3895, 0.4009, 0.4068 / 0.3957, 0.3991, 0.4003 | within noise |
| dense 10 x 30 apply_accumulated_gradient / numpy | 4.619 (4.505-4.796) | 4.613 (4.517-4.889) | -0.1% | 4.642, 4.619, 4.651 / 4.583, 4.554, 4.805 | within noise |
| dense 10 x 30 apply_accumulated_gradient / rust | 2.21 (2.162-2.254) | 2.193 (2.131-2.264) | -0.8% | 2.21, 2.208, 2.209 / 2.136, 2.2, 2.243 | within noise |
| dense 10 x 30 sgd step / numpy | 8.465 (8.231-9.049) | 8.568 (8.282-8.827) | +1.2% | 8.435, 8.498, 8.64 / 8.72, 8.383, 8.568 | within noise |
| dense 10 x 30 sgd step / rust | 0.4565 (0.4447-0.5017) | 0.4768 (0.45-0.5315) | +4.4% | 0.4456, 0.4803, 0.4611 / 0.4606, 0.507, 0.471 | within noise |
| dense 10 x 30 forward_batch b32 / numpy | 9.821 (9.644-9.909) | 9.737 (9.611-9.847) | -0.8% | 9.89, 9.821, 9.646 / 9.737, 9.702, 9.738 | within noise |
| dense 10 x 30 forward_batch b32 / rust | 5.232 (5.103-5.261) | 2.487 (2.445-2.543) | -52.5% | 5.113, 5.246, 5.24 / 2.45, 2.495, 2.519 | consistent |
| dense 10 x 30 forward_batch b512 / numpy | 54.46 (53.61-55.59) | 54.34 (53.29-55.58) | -0.2% | 53.78, 54.87, 54.88 / 53.72, 54.07, 55.06 | within noise |
| dense 10 x 30 forward_batch b512 / rust | 77.73 (76.28-78.25) | 35.39 (34.75-35.88) | -54.5% | 76.33, 77.73, 78.16 / 34.93, 35.39, 35.78 | consistent |
| dense 10 x 30 downstream_batch b32 / numpy | 1.803 (1.775-1.853) | 1.805 (1.754-1.869) | +0.1% | 1.807, 1.801, 1.826 / 1.778, 1.814, 1.831 | within noise |
| dense 10 x 30 downstream_batch b32 / rust | 1.175 (1.135-1.228) | 1.164 (1.146-1.197) | -0.9% | 1.138, 1.193, 1.195 / 1.151, 1.167, 1.18 | within noise |
| dense 10 x 30 downstream_batch b512 / numpy | 12.3 (12.2-12.65) | 12.31 (12.03-12.48) | +0.1% | 12.29, 12.43, 12.37 / 12.17, 12.33, 12.37 | within noise |
| dense 10 x 30 downstream_batch b512 / rust | 15.62 (15.13-16.11) | 15.52 (15.34-16.21) | -0.7% | 15.24, 15.62, 16.1 / 15.39, 15.52, 16.12 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 4.902 (4.75-5.015) | 4.895 (4.69-4.987) | -0.1% | 4.963, 4.822, 4.891 / 4.787, 4.901, 4.907 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 1.694 (1.64-1.735) | 1.707 (1.637-1.743) | +0.8% | 1.643, 1.694, 1.729 / 1.661, 1.707, 1.731 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 35.85 (34.63-36.69) | 35.67 (34.67-36.75) | -0.5% | 36.26, 35.79, 35.25 / 35.2, 35.71, 35.68 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / rust | 22.63 (22.18-23.21) | 22.81 (22.03-23.09) | +0.8% | 22.53, 22.63, 22.83 / 22.03, 22.91, 22.95 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 4.56 (4.443-4.761) | 4.544 (4.472-4.588) | -0.4% | 4.56, 4.628, 4.505 / 4.558, 4.494, 4.566 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 1.96 (1.897-1.973) | 1.907 (1.868-1.932) | -2.7% | 1.898, 1.965, 1.965 / 1.883, 1.903, 1.924 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 24.92 (24.55-25.4) | 24.91 (24.43-25.28) | -0.1% | 25.06, 25.13, 24.67 / 24.77, 24.71, 25.1 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 32.84 (32.44-34.39) | 32.84 (32.44-33.77) | -0.0% | 33.49, 33.01, 32.68 / 32.98, 33.2, 32.75 | within noise |
| conv 28x28, 8 ch forward / numpy | 55.45 (54.15-57.49) | 55.74 (53.91-57.09) | +0.5% | 55.45, 55.82, 55.41 / 54.44, 56.52, 55.78 | within noise |
| conv 28x28, 8 ch forward / rust | 19.41 (18.78-20.14) | 19.27 (18.63-19.6) | -0.7% | 18.82, 19.72, 19.66 / 18.97, 19.2, 19.43 | within noise |
| conv 28x28, 8 ch downstream / numpy | 39.18 (37.57-41.5) | 38.98 (38.26-39.84) | -0.5% | 39.28, 40.09, 38.63 / 39.25, 39.32, 38.7 | within noise |
| conv 28x28, 8 ch downstream / rust | 17.34 (17.01-17.53) | 17.35 (17.01-17.9) | +0.0% | 17.09, 17.44, 17.36 / 17.3, 17.14, 17.66 | within noise |
| conv 28x28, 8 ch accumulate_gradient / numpy | 35.61 (34.97-37.3) | 35.87 (35.01-36.32) | +0.8% | 34.98, 36.47, 35.68 / 35.32, 36.17, 35.88 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 15.83 (15.72-15.93) | 15.76 (15.7-15.81) | -0.4% | 15.83, 15.83, 15.81 / 15.76, 15.73, 15.78 | separated, inside spread |
| conv 28x28, 8 ch forward_batch b32 / numpy | 978.9 (962.2-993.3) | 966.7 (960.4-980.1) | -1.2% | 971.9, 986.2, 972.7 / 961.7, 970.4, 975.1 | within noise |
| conv 28x28, 8 ch forward_batch b32 / rust | 576.8 (555.4-588.2) | 568.6 (562.4-587.9) | -1.4% | 558.8, 576.8, 585.7 / 563.7, 568.6, 584.8 | within noise |
| conv 28x28, 8 ch forward_batch b512 / numpy | 1.833e+04 (1.815e+04-1.854e+04) | 1.843e+04 (1.812e+04-1.858e+04) | +0.6% | 1.826e+04, 1.839e+04, 1.834e+04 / 1.846e+04, 1.843e+04, 1.83e+04 | within noise |
| conv 28x28, 8 ch forward_batch b512 / rust | 9420 (9139-9777) | 9432 (9074-9958) | +0.1% | 9171, 9500, 9614 / 9173, 9432, 9813 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 597 (579.9-617.8) | 588.6 (576.8-616.4) | -1.4% | 599.4, 597, 596.4 / 580, 586.8, 606.2 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / rust | 507.1 (490.9-514.1) | 500.2 (491.8-502.1) | -1.3% | 498.7, 506.7, 511.4 / 496, 500.4, 500.4 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 1.616e+04 (1.596e+04-1.651e+04) | 1.624e+04 (1.607e+04-1.649e+04) | +0.5% | 1.64e+04, 1.617e+04, 1.6e+04 / 1.624e+04, 1.628e+04, 1.625e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / rust | 1418 (1411-1434) | 1423 (1414-1453) | +0.4% | 1415, 1417, 1425 / 1416, 1441, 1434 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 1200 (1165-1227) | 1214 (1196-1306) | +1.1% | 1170, 1202, 1222 / 1256, 1208, 1210 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 528.1 (520.4-530.9) | 524.6 (520.9-528.3) | -0.7% | 524.4, 524.9, 529.8 / 522.7, 524.6, 525.3 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 2.004e+04 (1.929e+04-2.032e+04) | 2.011e+04 (1.983e+04-2.04e+04) | +0.4% | 1.946e+04, 2.013e+04, 2.019e+04 / 1.992e+04, 2.011e+04, 2.028e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 1.149e+04 (1.146e+04-1.153e+04) | 1.15e+04 (1.146e+04-1.15e+04) | +0.1% | 1.15e+04, 1.15e+04, 1.148e+04 / 1.148e+04, 1.15e+04, 1.15e+04 | within noise |
| conv 8x8, 8 ch forward / numpy | 28.58 (27.79-30.02) | 28.58 (27.82-29.28) | +0.0% | 28.56, 29.25, 28.52 / 28.84, 28.13, 28.93 | within noise |
| conv 8x8, 8 ch forward / rust | 1.529 (1.493-1.611) | 1.508 (1.466-1.526) | -1.3% | 1.552, 1.529, 1.525 / 1.477, 1.511, 1.516 | separated, inside spread |
| conv 8x8, 8 ch downstream / numpy | 22 (21.79-22.71) | 22.15 (21.44-23.66) | +0.7% | 21.83, 22.37, 22.07 / 21.71, 22.55, 23.01 | within noise |
| conv 8x8, 8 ch downstream / rust | 1.19 (1.179-1.244) | 1.189 (1.166-1.221) | -0.0% | 1.185, 1.213, 1.19 / 1.17, 1.189, 1.21 | within noise |
| conv 8x8, 8 ch accumulate_gradient / numpy | 7.485 (7.213-7.706) | 7.323 (7.056-7.644) | -2.2% | 7.386, 7.348, 7.626 / 7.35, 7.305, 7.437 | within noise |
| conv 8x8, 8 ch accumulate_gradient / rust | 1.151 (1.14-1.166) | 1.16 (1.139-1.173) | +0.7% | 1.145, 1.153, 1.159 / 1.156, 1.16, 1.154 | within noise |
| conv 8x8, 8 ch forward_batch b32 / numpy | 75.79 (73.93-76.39) | 74.9 (74.05-76.2) | -1.2% | 76.04, 76.14, 74.72 / 74.28, 75.23, 75.73 | within noise |
| conv 8x8, 8 ch forward_batch b32 / rust | 31.6 (30.56-31.95) | 31.36 (30.91-32.33) | -0.8% | 30.56, 31.89, 31.64 / 31.17, 31.19, 31.94 | within noise |
| conv 8x8, 8 ch forward_batch b512 / numpy | 881.4 (875.9-895.8) | 874.3 (864.5-898.7) | -0.8% | 885.9, 878, 884.5 / 868.1, 873.7, 897.5 | within noise |
| conv 8x8, 8 ch forward_batch b512 / rust | 497.9 (476-501.5) | 490.1 (485.9-520.1) | -1.6% | 487.4, 491.4, 500.9 / 504.7, 499.9, 488.7 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 63.96 (63.22-66.31) | 63.68 (62.61-65.37) | -0.4% | 65.16, 63.87, 64.29 / 63.6, 62.78, 65.22 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / rust | 27.44 (26.71-27.89) | 27.54 (27.42-29.15) | +0.4% | 26.73, 27.64, 27.57 / 27.46, 28.29, 27.63 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 701.6 (682.9-716.1) | 690.9 (685.1-711) | -1.5% | 698.3, 707.1, 697.2 / 687.4, 690, 705.5 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / rust | 431.6 (423.2-440.6) | 435.7 (433-471.3) | +0.9% | 427.7, 438.7, 430.5 / 434.6, 434.2, 455.2 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 93.28 (90.56-94.22) | 93.56 (90.87-98.77) | +0.3% | 90.99, 93.75, 93.33 / 94.82, 92.94, 93.85 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 27.19 (27.02-27.24) | 27.13 (27.05-27.23) | -0.2% | 27.11, 27.22, 27.12 / 27.18, 27.09, 27.1 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 1404 (1380-1412) | 1398 (1389-1414) | -0.4% | 1383, 1411, 1404 / 1391, 1398, 1412 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 452.9 (451.1-457.5) | 451 (450.6-456.9) | -0.4% | 454.7, 455.3, 451.2 / 450.9, 452.3, 453.8 | within noise |
| conv 13x13x8, 8 ch forward / numpy | 51.13 (49.54-51.98) | 50.23 (49.54-51.05) | -1.8% | 51.55, 51.46, 50.34 / 49.64, 50.65, 50.23 | within noise |
| conv 13x13x8, 8 ch forward / rust | 19.99 (19.8-20.23) | 19.87 (19.74-20.16) | -0.6% | 20.02, 19.97, 20.05 / 19.84, 19.97, 19.95 | within noise |
| conv 13x13x8, 8 ch downstream / numpy | 51.42 (50.29-53.2) | 52.1 (51.51-52.77) | +1.3% | 50.92, 52.26, 51.27 / 52.01, 52.6, 51.7 | within noise |
| conv 13x13x8, 8 ch downstream / rust | 12.45 (12.09-12.5) | 12.47 (12.34-12.57) | +0.1% | 12.16, 12.48, 12.46 / 12.41, 12.41, 12.55 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 23.44 (22.93-23.68) | 23.3 (22.98-23.62) | -0.6% | 23.29, 23.32, 23.44 / 23.07, 23.31, 23.54 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 4.951 (4.887-5.038) | 5.061 (4.877-5.15) | +2.2% | 4.934, 4.93, 4.999 / 4.965, 5.013, 5.081 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 1013 (1002-1015) | 1013 (1002-1023) | -0.0% | 1009, 1013, 1008 / 1002, 1013, 1023 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 605.6 (600.4-608) | 606 (600.8-612.7) | +0.1% | 602.9, 606.9, 605.4 / 605.7, 606.7, 608.2 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 1.422e+04 (1.404e+04-1.431e+04) | 1.416e+04 (1.401e+04-1.439e+04) | -0.4% | 1.415e+04, 1.416e+04, 1.427e+04 / 1.405e+04, 1.415e+04, 1.432e+04 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 1.806e+04 (1.796e+04-1.826e+04) | 1.813e+04 (1.802e+04-1.837e+04) | +0.4% | 1.806e+04, 1.803e+04, 1.814e+04 / 1.81e+04, 1.807e+04, 1.827e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 897.9 (858.1-935.6) | 911.4 (878.4-943) | +1.5% | 912.8, 882, 898 / 888.3, 905.2, 938.7 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 347.9 (337.6-354.2) | 351.9 (345.6-359.2) | +1.1% | 341.7, 347.9, 354.2 / 347.7, 351, 357.4 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 2.562e+04 (2.55e+04-2.624e+04) | 2.588e+04 (2.555e+04-2.618e+04) | +1.0% | 2.591e+04, 2.574e+04, 2.562e+04 / 2.559e+04, 2.584e+04, 2.616e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 1046 (1027-1053) | 1040 (1035-1052) | -0.5% | 1042, 1037, 1049 / 1041, 1047, 1036 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 599.9 (583.1-617.4) | 602.1 (593.9-622.8) | +0.4% | 585.2, 605.1, 606.6 / 594.1, 602.1, 618.3 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 166.6 (166.3-173.1) | 166.6 (165.6-172) | -0.0% | 166.4, 171.5, 166.6 / 167.7, 165.9, 169.4 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.04e+04 (1.008e+04-1.053e+04) | 1.048e+04 (1.029e+04-1.054e+04) | +0.8% | 1.02e+04, 1.048e+04, 1.04e+04 / 1.03e+04, 1.053e+04, 1.049e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 2611 (2525-2617) | 2564 (2533-2605) | -1.8% | 2572, 2612, 2571 / 2569, 2534, 2599 | within noise |
| conv 26x26x8/2, 8 ch forward / numpy | 54.13 (53.43-55.29) | 55 (54.45-55.03) | +1.6% | 54.81, 53.58, 54.13 / 54.73, 55.02, 54.75 | within noise |
| conv 26x26x8/2, 8 ch forward / rust | 23.78 (23.59-24.26) | 23.78 (23.52-24.02) | -0.0% | 23.76, 23.64, 24.2 / 23.53, 23.78, 23.94 | within noise |
| conv 26x26x8/2, 8 ch downstream / numpy | 60.39 (59.16-63.25) | 61.36 (60.34-63.87) | +1.6% | 61.76, 60.04, 60.02 / 61.46, 60.52, 62.96 | within noise |
| conv 26x26x8/2, 8 ch downstream / rust | 15.45 (15.13-15.72) | 15.44 (15.13-15.84) | -0.1% | 15.16, 15.45, 15.68 / 15.21, 15.44, 15.72 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 26.28 (26.26-26.94) | 26.56 (26.04-27.15) | +1.1% | 26.28, 26.38, 26.61 / 26.24, 26.54, 26.92 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 5.801 (5.622-5.948) | 5.73 (5.617-5.835) | -1.2% | 5.668, 5.801, 5.931 / 5.667, 5.76, 5.79 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 1234 (1221-1240) | 1245 (1228-1256) | +0.9% | 1231, 1227, 1239 / 1235, 1241, 1252 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 725.6 (719.4-744.9) | 728.5 (724.1-732.7) | +0.4% | 737.1, 721.2, 727.7 / 726.9, 729.9, 729 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 1.729e+04 (1.709e+04-1.746e+04) | 1.721e+04 (1.707e+04-1.752e+04) | -0.5% | 1.715e+04, 1.74e+04, 1.73e+04 / 1.712e+04, 1.727e+04, 1.733e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 2.268e+04 (2.251e+04-2.28e+04) | 2.272e+04 (2.26e+04-2.278e+04) | +0.2% | 2.279e+04, 2.259e+04, 2.265e+04 / 2.264e+04, 2.274e+04, 2.274e+04 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 1180 (1161-1264) | 1228 (1160-1277) | +4.1% | 1218, 1219, 1174 / 1181, 1215, 1269 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 423.1 (414.7-436.8) | 428.3 (424.1-439.3) | +1.2% | 418.8, 426.4, 430 / 425, 429, 435 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 4.296e+04 (4.195e+04-4.356e+04) | 4.266e+04 (4.228e+04-4.308e+04) | -0.7% | 4.241e+04, 4.304e+04, 4.297e+04 / 4.236e+04, 4.268e+04, 4.29e+04 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 2326 (2300-2342) | 2319 (2306-2334) | -0.3% | 2317, 2314, 2337 / 2314, 2326, 2318 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 707.6 (694.9-721) | 709.4 (701.4-721.1) | +0.3% | 697.4, 709.4, 713.4 / 704.9, 707.9, 717.3 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 200.8 (199.4-208.2) | 203.8 (200.3-207.7) | +1.5% | 204.2, 201.5, 200.8 / 200.5, 205.8, 205.5 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 1.236e+04 (1.186e+04-1.246e+04) | 1.236e+04 (1.198e+04-1.25e+04) | -0.0% | 1.201e+04, 1.246e+04, 1.236e+04 / 1.227e+04, 1.223e+04, 1.244e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 3052 (2997-3072) | 3065 (2993-3076) | +0.4% | 3063, 3051, 3023 / 3039, 3031, 3069 | within noise |
| conv 26x26x8, 8 ch forward / numpy | 127.1 (124.6-128.6) | 128 (126.5-131.3) | +0.7% | 125.6, 127.1, 128.5 / 126.7, 127.9, 130.8 | within noise |
| conv 26x26x8, 8 ch forward / rust | 92.71 (90.64-93.39) | 91.15 (90.11-91.52) | -1.7% | 92.31, 92.01, 92.93 / 90.82, 90.97, 91.15 | separated, inside spread |
| conv 26x26x8, 8 ch downstream / numpy | 146.1 (143.4-157.2) | 148.1 (143.5-155.3) | +1.3% | 149.9, 151.7, 144.7 / 147.6, 149.4, 150 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 59.68 (59.42-62.54) | 60.04 (58.72-63.52) | +0.6% | 59.48, 61.78, 59.68 / 59.09, 59.89, 63.16 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 89.74 (88.64-92.15) | 89.36 (87.69-91.62) | -0.4% | 89.1, 90.92, 90.6 / 88.19, 89.65, 90.63 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 25.02 (24.84-25.66) | 25.29 (25.1-25.58) | +1.1% | 25.25, 25.03, 25.02 / 25.29, 25.42, 25.34 | separated, inside spread |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 4279 (4141-4390) | 4327 (4122-4453) | +1.1% | 4149, 4279, 4365 / 4229, 4363, 4356 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 2970 (2942-3006) | 2949 (2932-2982) | -0.7% | 2950, 2963, 2998 / 2976, 2949, 2935 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 6.755e+04 (6.71e+04-6.796e+04) | 6.769e+04 (6.719e+04-6.894e+04) | +0.2% | 6.723e+04, 6.755e+04, 6.785e+04 / 6.736e+04, 6.827e+04, 6.789e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 8.492e+04 (8.455e+04-8.596e+04) | 8.472e+04 (8.422e+04-8.535e+04) | -0.2% | 8.525e+04, 8.48e+04, 8.498e+04 / 8.444e+04, 8.506e+04, 8.474e+04 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 4940 (4822-5015) | 4800 (4622-4965) | -2.8% | 4987, 4909, 4908 / 4877, 4673, 4881 | separated, inside spread |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 388 (383.2-397.5) | 396.7 (393.9-399.4) | +2.2% | 386.1, 391.2, 388 / 395.1, 395.7, 399 | separated, inside spread |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 1.135e+05 (1.125e+05-1.154e+05) | 1.133e+05 (1.128e+05-1.143e+05) | -0.2% | 1.139e+05, 1.135e+05, 1.137e+05 / 1.141e+05, 1.128e+05, 1.133e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 5031 (4995-5066) | 5029 (4986-5119) | -0.0% | 4998, 5040, 5051 / 5061, 5012, 5051 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 3070 (2972-3120) | 3039 (2974-3065) | -1.0% | 2983, 3077, 3094 / 3001, 3042, 3051 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 665.7 (659.8-682.8) | 667.5 (665.7-687.8) | +0.3% | 663.4, 682.1, 663.2 / 667.2, 676.7, 668.2 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 5.07e+04 (4.979e+04-5.181e+04) | 5.061e+04 (5.046e+04-5.145e+04) | -0.2% | 5.013e+04, 5.066e+04, 5.164e+04 / 5.054e+04, 5.102e+04, 5.092e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 1.206e+04 (1.202e+04-1.209e+04) | 1.186e+04 (1.169e+04-1.201e+04) | -1.7% | 1.207e+04, 1.204e+04, 1.206e+04 / 1.17e+04, 1.199e+04, 1.187e+04 | separated, inside spread |
| pool 26x26, 8 ch forward / numpy | 70.35 (69.55-72.07) | 70.09 (69.83-72.15) | -0.4% | 71.01, 70.35, 70.42 / 71.04, 69.92, 71.08 | within noise |
| pool 26x26, 8 ch forward / rust | 2.996 (2.975-3.059) | 3.001 (2.983-3.073) | +0.2% | 2.981, 3.028, 3.013 / 2.984, 3.001, 3.057 | within noise |
| pool 26x26, 8 ch downstream / numpy | 34.65 (34.12-36.09) | 34.19 (33.52-35.56) | -1.3% | 35.35, 34.6, 34.41 / 33.72, 35.01, 34.29 | within noise |
| pool 26x26, 8 ch downstream / rust | 4.092 (4.063-4.16) | 4.081 (4.047-4.174) | -0.3% | 4.078, 4.126, 4.098 / 4.059, 4.081, 4.132 | within noise |
| pool 26x26, 8 ch forward_batch b32 / numpy | 1224 (1218-1237) | 1221 (1218-1224) | -0.2% | 1221, 1229, 1230 / 1221, 1219, 1223 | within noise |
| pool 26x26, 8 ch forward_batch b32 / rust | 90.67 (89.5-91.11) | 90.47 (89.58-92.4) | -0.2% | 90.36, 90.04, 90.94 / 89.99, 90.38, 91.9 | within noise |
| pool 26x26, 8 ch forward_batch b512 / numpy | 2.035e+04 (1.994e+04-2.054e+04) | 2.027e+04 (1.994e+04-2.087e+04) | -0.4% | 1.997e+04, 2.035e+04, 2.049e+04 / 2.002e+04, 2.027e+04, 2.069e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 2219 (2195-2257) | 2228 (2188-2249) | +0.4% | 2232, 2219, 2220 / 2226, 2235, 2211 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 481.7 (477.2-491.5) | 477.9 (476.9-487.4) | -0.8% | 480.4, 490.4, 478.8 / 477.7, 478.9, 482.1 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / rust | 132.3 (130.5-134.7) | 130.7 (130.4-134.7) | -1.2% | 131.4, 132.6, 132.9 / 130.7, 131, 132.6 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 1.372e+04 (1.363e+04-1.378e+04) | 1.374e+04 (1.361e+04-1.379e+04) | +0.2% | 1.375e+04, 1.367e+04, 1.372e+04 / 1.379e+04, 1.369e+04, 1.368e+04 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / rust | 2613 (2610-2620) | 2613 (2606-2623) | -0.0% | 2615, 2615, 2613 / 2617, 2609, 2616 | within noise |
| pool 6x6, 8 ch forward / numpy | 33.46 (33.06-34.94) | 34.14 (33.25-34.47) | +2.0% | 34.61, 33.14, 33.46 / 34.41, 33.88, 33.82 | within noise |
| pool 6x6, 8 ch forward / rust | 0.4562 (0.4489-0.4697) | 0.4587 (0.45-0.4616) | +0.5% | 0.4511, 0.4632, 0.4575 / 0.4517, 0.4588, 0.4602 | within noise |
| pool 6x6, 8 ch downstream / numpy | 19.18 (18.93-19.3) | 19.59 (19.16-20.33) | +2.1% | 19.02, 19.25, 19.21 / 19.39, 20.24, 19.37 | separated, inside spread |
| pool 6x6, 8 ch downstream / rust | 0.4498 (0.437-0.4558) | 0.4527 (0.4385-0.4697) | +0.7% | 0.4429, 0.4513, 0.4529 / 0.44, 0.4643, 0.4527 | within noise |
| pool 6x6, 8 ch forward_batch b32 / numpy | 109.1 (108.4-110.6) | 109.4 (108.3-109.6) | +0.2% | 109.3, 109.7, 109 / 108.9, 109.2, 109.4 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 6.891 (6.838-6.968) | 6.91 (6.84-7.019) | +0.3% | 6.852, 6.891, 6.944 / 6.843, 6.91, 7.01 | within noise |
| pool 6x6, 8 ch forward_batch b512 / numpy | 1207 (1205-1232) | 1209 (1206-1236) | +0.1% | 1207, 1205, 1229 / 1207, 1208, 1236 | within noise |
| pool 6x6, 8 ch forward_batch b512 / rust | 108.7 (106.6-109.5) | 108.5 (107.5-109.9) | -0.2% | 107.3, 108.8, 109.3 / 108.1, 108.3, 109.1 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 59.37 (58.95-61.16) | 60.21 (59.1-61.46) | +1.4% | 60.34, 59.07, 59.45 / 59.45, 60.87, 60.28 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / rust | 7.743 (7.675-7.839) | 7.648 (7.561-7.952) | -1.2% | 7.705, 7.733, 7.82 / 7.63, 7.597, 7.87 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 604.6 (593.9-610.2) | 600 (595.6-608.4) | -0.8% | 600.6, 606.7, 601.3 / 602.7, 598.5, 602.2 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 121.2 (119.2-122.5) | 120.4 (119.2-124.5) | -0.7% | 121.1, 120.8, 121.5 / 119.8, 122, 121.6 | within noise |
| conv tail 32 x 5408 bare downstream b32 / numpy | 69.63 (65.32-78.01) | 69.3 (66.63-76.94) | -0.5% | 65.74, 73.11, 73.53 / 66.96, 71.26, 74.29 | within noise |
| conv tail 32 x 5408 bare downstream b32 / rust | 247.4 (240.1-252.9) | 245.2 (242.4-254) | -0.9% | 242.2, 247.2, 252.8 / 246.3, 245.2, 248.7 | within noise |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3200 (3193-3215) | 3202 (3186-3234) | +0.1% | 3195, 3204, 3209 / 3206, 3214, 3202 | within noise |
| conv tail 32 x 5408 bare downstream b512 / rust | 2271 (2256-2298) | 2280 (2269-2295) | +0.4% | 2283, 2258, 2274 / 2284, 2278, 2283 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 79.13 (78.7-79.37) | 79.07 (78.49-79.59) | -0.1% | 78.87, 79.35, 79.12 / 78.89, 79.43, 78.8 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / rust | 225 (221.6-232.4) | 227.8 (219.5-233.6) | +1.2% | 225, 231, 221.6 / 223.3, 226.1, 231.1 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 1630 (1576-1678) | 1624 (1591-1687) | -0.4% | 1584, 1657, 1635 / 1624, 1639, 1631 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / rust | 2228 (2180-2243) | 2225 (2129-2249) | -0.1% | 2235, 2206, 2227 / 2236, 2214, 2178 | within noise |
| conv tail 32 x 5408 transpose b32 / numpy | 0.7129 (0.6994-0.7223) | 0.7157 (0.6966-0.7423) | +0.4% | 0.7014, 0.717, 0.7168 / 0.6971, 0.7329, 0.7157 | within noise |
| conv tail 32 x 5408 transpose b32 / rust | 0.8578 (0.8397-0.8654) | 0.8635 (0.8398-0.869) | +0.7% | 0.8413, 0.8596, 0.8633 / 0.868, 0.8449, 0.8635 | within noise |
| conv tail 32 x 5408 transpose b512 / numpy | 11.42 (11.03-13.14) | 11.69 (10.97-12.37) | +2.4% | 11.32, 12.4, 11.18 / 11.58, 12.07, 11.51 | within noise |
| conv tail 32 x 5408 transpose b512 / rust | 14.27 (13.52-15.36) | 14.19 (13.54-14.41) | -0.5% | 14.27, 14.45, 14.18 / 14.3, 13.86, 13.99 | within noise |
| conv tail 32 x 5408 add b32 / numpy | 96.44 (94.99-101) | 95.46 (95.07-95.81) | -1.0% | 97.8, 96.43, 98.08 / 95.58, 95.44, 95.42 | separated, inside spread |
| conv tail 32 x 5408 add b32 / rust | 64.65 (63-69.36) | 63.12 (62.97-69.37) | -2.4% | 66.27, 67.72, 63.11 / 63.06, 66.17, 64.6 | within noise |
| conv tail 32 x 5408 add b512 / numpy | 94.23 (93.8-100) | 94.78 (94-99.72) | +0.6% | 94.22, 94.09, 97.07 / 94.56, 95.43, 97.14 | within noise |
| conv tail 32 x 5408 add b512 / rust | 65.41 (62.39-68.78) | 64.27 (62.43-69.14) | -1.7% | 67.11, 67.07, 62.55 / 69.01, 62.46, 64.27 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 1.477 (1.439-1.498) | 1.45 (1.395-1.48) | -1.9% | 1.46, 1.476, 1.486 / 1.43, 1.458, 1.441 | separated, inside spread |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.405 (0.3963-0.4117) | 0.4093 (0.4018-0.4114) | +1.1% | 0.3973, 0.4091, 0.4051 / 0.4065, 0.4102, 0.4085 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 10.44 (10.33-10.65) | 10.42 (10.21-10.54) | -0.2% | 10.39, 10.64, 10.39 / 10.38, 10.39, 10.42 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 4.496 (4.409-4.646) | 4.531 (4.45-4.618) | +0.8% | 4.412, 4.579, 4.553 / 4.507, 4.573, 4.534 | within noise |
| dense 30 x 784 bare downstream b32 / numpy | 22.99 (22.55-23.29) | 22.8 (22.62-22.9) | -0.8% | 23.23, 23.03, 22.64 / 22.73, 22.8, 22.82 | within noise |
| dense 30 x 784 bare downstream b32 / rust | 29.02 (27.69-29.52) | 28.98 (28.67-29.33) | -0.1% | 27.72, 29.02, 29.52 / 29, 28.98, 28.97 | within noise |
| dense 30 x 784 bare downstream b512 / numpy | 138.9 (112.5-143.1) | 139.3 (135.8-141.1) | +0.2% | 125.8, 140.2, 140.5 / 138.5, 138.4, 139.8 | within noise |
| dense 30 x 784 bare downstream b512 / rust | 246.4 (235.4-247.8) | 241.8 (240.9-246.1) | -1.9% | 241.3, 244.3, 247.6 / 241.8, 242.9, 243.5 | within noise |
| dense 30 x 784 bare accumulate b32 / numpy | 28.72 (28.41-28.96) | 28.78 (28.6-29.41) | +0.2% | 28.69, 28.72, 28.72 / 28.99, 28.61, 29.1 | within noise |
| dense 30 x 784 bare accumulate b32 / rust | 32.24 (31-32.58) | 32.63 (31.29-33.72) | +1.2% | 31.44, 32.35, 32.38 / 32.63, 32.14, 32.75 | within noise |
| dense 30 x 784 bare accumulate b512 / numpy | 192.9 (191.4-196.7) | 195.1 (192.6-197.3) | +1.1% | 192.2, 193.5, 194.8 / 194.6, 193.4, 197.2 | within noise |
| dense 30 x 784 bare accumulate b512 / rust | 283.4 (276.9-288.4) | 283.4 (277.7-285.8) | +0.0% | 286, 278.1, 283.5 / 282.2, 281.6, 284.8 | within noise |
| dense 30 x 784 transpose b32 / numpy | 0.6874 (0.6811-0.7061) | 0.6887 (0.681-0.6998) | +0.2% | 0.6811, 0.6978, 0.6941 / 0.6828, 0.689, 0.6963 | within noise |
| dense 30 x 784 transpose b32 / rust | 0.8305 (0.8092-0.8402) | 0.8322 (0.8164-0.8458) | +0.2% | 0.8158, 0.8376, 0.8305 / 0.8248, 0.8266, 0.8401 | within noise |
| dense 30 x 784 transpose b512 / numpy | 7.198 (7.167-7.301) | 7.249 (7.197-7.379) | +0.7% | 7.195, 7.201, 7.234 / 7.207, 7.328, 7.249 | within noise |
| dense 30 x 784 transpose b512 / rust | 13.94 (13.43-14.77) | 13.5 (13.44-15.16) | -3.2% | 13.68, 13.94, 14.39 / 13.5, 13.85, 14.3 | within noise |
| dense 30 x 784 add b32 / numpy | 9.201 (8.984-9.432) | 9.192 (8.945-9.957) | -0.1% | 9.179, 9.201, 9.256 / 9.037, 9.486, 9.521 | within noise |
| dense 30 x 784 add b32 / rust | 8.972 (8.647-9.216) | 8.851 (8.633-9.349) | -1.3% | 8.923, 9.187, 8.761 / 8.765, 8.955, 9.05 | within noise |
| dense 30 x 784 add b512 / numpy | 12.49 (12.13-12.75) | 12.79 (12.09-13.03) | +2.4% | 12.38, 12.61, 12.36 / 12.45, 12.94, 12.52 | within noise |
| dense 30 x 784 add b512 / rust | 8.683 (8.502-9.378) | 8.683 (8.62-9.088) | +0.0% | 8.836, 8.94, 8.608 / 8.65, 8.82, 8.888 | within noise |
| dense 30 x 784 sum_axis0 b32 / numpy | 1.515 (1.442-1.585) | 1.499 (1.452-1.59) | -1.0% | 1.514, 1.515, 1.494 / 1.503, 1.491, 1.521 | within noise |
| dense 30 x 784 sum_axis0 b32 / rust | 0.3827 (0.3703-0.3899) | 0.3843 (0.3775-0.4187) | +0.4% | 0.371, 0.3872, 0.3853 / 0.3834, 0.401, 0.3815 | within noise |
| dense 30 x 784 sum_axis0 b512 / numpy | 10.97 (10.82-11.16) | 10.96 (10.65-11.13) | -0.1% | 10.93, 11.05, 10.95 / 10.7, 11.04, 11.04 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 4.091 (3.995-4.177) | 4.094 (4.059-4.214) | +0.1% | 4.016, 4.156, 4.095 / 4.062, 4.132, 4.144 | within noise |
| dense 10 x 30 bare downstream b32 / numpy | 1.799 (1.744-1.814) | 1.76 (1.709-1.919) | -2.2% | 1.796, 1.805, 1.774 / 1.76, 1.733, 1.876 | within noise |
| dense 10 x 30 bare downstream b32 / rust | 1.114 (1.076-1.156) | 1.112 (1.097-1.129) | -0.2% | 1.089, 1.114, 1.144 / 1.112, 1.113, 1.113 | within noise |
| dense 10 x 30 bare downstream b512 / numpy | 11.86 (11.77-12.16) | 11.83 (11.75-12.03) | -0.3% | 11.79, 12.13, 11.86 / 11.77, 11.83, 12.02 | within noise |
| dense 10 x 30 bare downstream b512 / rust | 15.92 (15.78-16.28) | 16.06 (15.69-16.13) | +0.8% | 15.79, 15.92, 16.21 / 15.88, 16.09, 16 | within noise |
| dense 10 x 30 bare accumulate b32 / numpy | 1.774 (1.764-1.824) | 1.804 (1.705-1.838) | +1.7% | 1.769, 1.798, 1.786 / 1.733, 1.823, 1.809 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 1.194 (1.191-1.212) | 1.194 (1.191-1.195) | -0.0% | 1.202, 1.192, 1.205 / 1.192, 1.194, 1.195 | within noise |
| dense 10 x 30 bare accumulate b512 / numpy | 13.36 (13.19-13.61) | 13.29 (13.17-13.48) | -0.5% | 13.33, 13.47, 13.33 / 13.22, 13.27, 13.4 | within noise |
| dense 10 x 30 bare accumulate b512 / rust | 25.8 (25.01-27.35) | 25.26 (25.01-26.49) | -2.1% | 26.04, 25.49, 26.61 / 25.71, 25.26, 25.84 | within noise |
| dense 10 x 30 transpose b32 / numpy | 0.4485 (0.4422-0.4652) | 0.4431 (0.4375-0.4615) | -1.2% | 0.4587, 0.4476, 0.4447 / 0.4461, 0.4403, 0.453 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.3814 (0.3748-0.385) | 0.3803 (0.3764-0.3895) | -0.3% | 0.3749, 0.3828, 0.3828 / 0.3781, 0.3856, 0.3803 | within noise |
| dense 10 x 30 transpose b512 / numpy | 2.95 (2.939-3.018) | 2.949 (2.91-3.029) | -0.0% | 2.963, 2.94, 2.984 / 2.917, 2.986, 2.973 | within noise |
| dense 10 x 30 transpose b512 / rust | 3.979 (3.91-4.06) | 3.989 (3.973-4.014) | +0.2% | 3.943, 4.018, 3.996 / 3.982, 3.993, 3.999 | within noise |
| dense 10 x 30 add b32 / numpy | 0.411 (0.3987-0.5377) | 0.4076 (0.4057-0.4176) | -0.8% | 0.4307, 0.411, 0.4723 / 0.4073, 0.4063, 0.4151 | within noise |
| dense 10 x 30 add b32 / rust | 0.1932 (0.1878-0.2043) | 0.1961 (0.1945-0.1967) | +1.5% | 0.1901, 0.1991, 0.1935 / 0.1951, 0.1961, 0.1965 | within noise |
| dense 10 x 30 add b512 / numpy | 0.4227 (0.4107-0.43) | 0.4187 (0.4177-0.4241) | -1.0% | 0.4144, 0.424, 0.4259 / 0.4182, 0.4185, 0.4229 | within noise |
| dense 10 x 30 add b512 / rust | 0.2021 (0.1967-0.2035) | 0.204 (0.2013-0.2062) | +0.9% | 0.1974, 0.2026, 0.203 / 0.203, 0.2047, 0.2042 | separated, inside spread |
| dense 10 x 30 sum_axis0 b32 / numpy | 1.323 (1.292-1.365) | 1.306 (1.272-1.464) | -1.3% | 1.337, 1.324, 1.319 / 1.293, 1.287, 1.394 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.2831 (0.2751-0.2905) | 0.2862 (0.279-0.2891) | +1.1% | 0.2776, 0.2872, 0.2842 / 0.2811, 0.2877, 0.2877 | within noise |
| dense 10 x 30 sum_axis0 b512 / numpy | 9.037 (8.941-9.286) | 9.137 (8.96-9.19) | +1.1% | 8.966, 9.164, 9.123 / 9.018, 9.137, 9.189 | within noise |
| dense 10 x 30 sum_axis0 b512 / rust | 2.632 (2.56-2.657) | 2.643 (2.566-2.652) | +0.4% | 2.562, 2.639, 2.643 / 2.583, 2.647, 2.647 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 288.8 (285.8-292.6) | 290.5 (286.9-291.6) | +0.6% | 290.2, 289.1, 287.8 / 287.6, 290.6, 291.1 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 387.9 (378.8-396.1) | 351.4 (343.7-356.6) | -9.4% | 379.3, 394.1, 387.9 / 349.1, 348.6, 356.4 | consistent |
| attention 16 x 32 forward_batch b512 / numpy | 5119 (4718-5147) | 5126 (5011-5172) | +0.1% | 4856, 5119, 5142 / 5061, 5117, 5157 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 6081 (5960-6145) | 5466 (5311-5483) | -10.1% | 6008, 6134, 6081 / 5435, 5470, 5394 | consistent |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 263.7 (262.4-270.2) | 269.4 (263.2-271.7) | +2.2% | 265.1, 266.6, 262.9 / 264.1, 269.6, 271.5 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / rust | 247 (242.5-250.7) | 247.1 (240.4-251.1) | +0.0% | 243.9, 246.8, 250.2 / 243.8, 244.4, 249.6 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 4595 (4418-4635) | 4583 (4500-4633) | -0.2% | 4526, 4620, 4579 / 4548, 4584, 4587 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / rust | 4719 (4619-4766) | 4679 (4558-4760) | -0.9% | 4710, 4687, 4719 / 4719, 4649, 4659 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 248.9 (245-252.2) | 246 (237.9-252.3) | -1.2% | 247.8, 248.8, 249.7 / 242.2, 247.8, 247.6 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 217.2 (212.8-221.1) | 212.4 (211-229.5) | -2.2% | 217.2, 217.2, 216.5 / 211.5, 221.1, 217.9 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5509 (5389-5682) | 5559 (5462-5675) | +0.9% | 5454, 5677, 5499 / 5504, 5610, 5574 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 4021 (4008-4065) | 4015 (3999-4053) | -0.2% | 4024, 4037, 4021 / 4003, 4019, 4037 | within noise |
