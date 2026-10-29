Old `19bea85` against new `fe99369`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `10dfec9` (extension sha256 `7d70efbe6dbd`) and new crate `37da6f1` (extension sha256 `7cbf8ede1ba5`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.79 (HIGH) (measured just after this run's crate builds); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / dense 10 x 30 transpose b512 / rust +52.0% (3.993 -> 6.069 µs)
- consistent: per call / conv tail 32 x 5408 transpose b32 / rust -35.9% (0.8518 -> 0.546 µs)
- consistent: per call / dense 30 x 784 transpose b32 / rust -32.9% (0.8312 -> 0.5575 µs)
- consistent: per call / dense 10 x 30 sum_axis0 b512 / rust +27.6% (2.577 -> 3.288 µs)
- consistent: per call / attention 16 x 32 accumulate_gradient_batch b32 / rust +21.6% (202.6 -> 246.3 µs)
- consistent: per call / pool 26x26, 8 ch forward / rust -19.0% (3.787 -> 3.069 µs)
- consistent: per call / pool 26x26, 8 ch forward_batch b32 / rust -18.1% (112.2 -> 91.84 µs)
- consistent: per call / dense 30 x 784 add b32 / numpy +18.1% (9.026 -> 10.66 µs)
- consistent: per call / dense 10 x 30 transpose b32 / rust -18.1% (0.3867 -> 0.3166 µs)
- consistent: per call / conv 8x8, 8 ch forward_batch b512 / rust +15.3% (487.7 -> 562.6 µs)
- ... 34 more consistent rows (report --md)
- 226 rows within noise (41 separated inside their spread), max |Δ| 10.1%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 28.14 (27.5-28.53) | 28.07 (26.9-28.2) | -0.3% | 27.93, 28.15, 28.05 / 27.55, 27.56, 28.1 | within noise |
| conv tail 32 x 5408 forward / rust | 20.87 (19.1-22.61) | 19.15 (19.03-20.78) | -8.2% | 21.68, 20.04, 20.93 / 19.91, 19.91, 19.13 | separated, inside spread |
| conv tail 32 x 5408 downstream / numpy | 24.12 (24.03-26.32) | 23.91 (23.3-25.88) | -0.9% | 24.07, 24.51, 25.21 / 23.37, 23.9, 25.18 | within noise |
| conv tail 32 x 5408 downstream / rust | 20.96 (20.7-23.71) | 20.9 (20.76-21.92) | -0.3% | 20.78, 22.31, 22.33 / 20.85, 21.11, 21.4 | within noise |
| conv tail 32 x 5408 hidden_delta / numpy | 32.06 (31.83-34.51) | 32.51 (31.3-33.92) | +1.4% | 32.06, 32.44, 33.25 / 32.61, 32.05, 33.13 | within noise |
| conv tail 32 x 5408 hidden_delta / rust | 23.84 (23-26.12) | 23.02 (22.9-24.68) | -3.4% | 23.84, 24.56, 24.47 / 22.99, 23.13, 23.85 | within noise |
| conv tail 32 x 5408 accumulate_gradient / numpy | 83.93 (83.59-88.66) | 92.74 (88.11-93.98) | +10.5% | 83.93, 84.95, 86.13 / 93.09, 89.98, 93.51 | consistent |
| conv tail 32 x 5408 accumulate_gradient / rust | 55.01 (52.99-62.35) | 54.66 (53.1-56.02) | -0.6% | 54.53, 55.39, 58.68 / 54.17, 53.69, 55.9 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 177.5 (177.2-184.7) | 181 (177.2-184.4) | +2.0% | 177.9, 177.2, 181.2 / 181, 179.1, 182.7 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 109 (106.9-113.5) | 107 (106.2-109.2) | -1.9% | 109, 110.4, 110.2 / 106.5, 106.8, 108.1 | separated, inside spread |
| conv tail 32 x 5408 sgd step / numpy | 264.9 (264.5-276.7) | 266.8 (262.8-276.1) | +0.7% | 264.6, 270.5, 270.9 / 270, 268.3, 266.3 | within noise |
| conv tail 32 x 5408 sgd step / rust | 59.42 (58.08-60.21) | 59.4 (58.07-60.9) | -0.0% | 58.62, 58.95, 59.96 / 60.7, 58.23, 59.36 | within noise |
| conv tail 32 x 5408 forward_batch b32 / numpy | 157.2 (149.4-158.1) | 153.2 (145.5-158.7) | -2.5% | 149.5, 157.8, 157.3 / 147.9, 151.1, 158.1 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 362.7 (339.8-385.7) | 363.4 (341.6-385.5) | +0.2% | 362.7, 362.7, 364.7 / 353.8, 352.9, 378.4 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1168 (1053-1178) | 1165 (1164-1169) | -0.2% | 1110, 1172, 1173 / 1164, 1165, 1167 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1883 (1702-1900) | 1904 (1894-1906) | +1.1% | 1767, 1883, 1900 / 1898, 1905, 1900 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 79 (78.34-79.94) | 79.65 (78.72-80.11) | +0.8% | 78.53, 79.6, 79.02 / 78.97, 79.83, 79.84 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 258.4 (247.4-267.5) | 242.5 (238.5-246.9) | -6.2% | 248.1, 262.5, 261.9 / 240.1, 245.1, 243.5 | separated, inside spread |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3109 (3100-3128) | 3088 (3068-3109) | -0.7% | 3109, 3109, 3114 / 3079, 3092, 3091 | consistent, small |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2403 (2393-2444) | 2392 (2382-2413) | -0.5% | 2418, 2397, 2410 / 2386, 2398, 2393 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 639.8 (619.3-653.4) | 628.4 (616.4-632.9) | -1.8% | 627.5, 649.3, 635.8 / 631.4, 621, 629.4 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 317.4 (309.1-326.2) | 312.5 (302.7-319.2) | -1.5% | 313.9, 317.9, 319.9 / 307.1, 314.3, 313.7 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 1.227e+04 (1.211e+04-1.233e+04) | 1.22e+04 (1.205e+04-1.24e+04) | -0.6% | 1.224e+04, 1.227e+04, 1.222e+04 / 1.214e+04, 1.236e+04, 1.217e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 5748 (5723-5949) | 5934 (5904-5952) | +3.2% | 5753, 5739, 5849 / 5928, 5937, 5927 | separated, inside spread |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 159.5 (154.9-161) | 164.6 (163.5-168.1) | +3.2% | 156.5, 160.6, 159.8 / 163.5, 166.3, 165.4 | separated, inside spread |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 302.2 (288.6-309) | 277.6 (272.8-285.4) | -8.1% | 294.1, 305.6, 304.9 / 276.7, 277.8, 279.1 | consistent |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 1852 (1831-1876) | 1848 (1822-1864) | -0.2% | 1843, 1871, 1846 / 1848, 1836, 1855 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 2356 (2271-2381) | 2366 (2323-2577) | +0.4% | 2356, 2320, 2364 / 2464, 2383, 2327 | within noise |
| dense 30 x 784 forward / numpy | 7.977 (7.805-8.671) | 8.221 (7.917-8.704) | +3.1% | 8.071, 7.977, 8.238 / 8.33, 8.221, 8.139 | within noise |
| dense 30 x 784 forward / rust | 2.77 (2.716-2.796) | 2.746 (2.678-3.012) | -0.9% | 2.756, 2.77, 2.769 / 2.873, 2.795, 2.716 | within noise |
| dense 30 x 784 downstream / numpy | 3.875 (3.817-3.934) | 4.071 (3.956-4.16) | +5.1% | 3.892, 3.821, 3.916 / 4.027, 4.102, 4.058 | consistent |
| dense 30 x 784 downstream / rust | 2.155 (2.011-2.25) | 2.208 (2.055-2.346) | +2.4% | 2.131, 2.136, 2.181 / 2.265, 2.076, 2.273 | within noise |
| dense 30 x 784 hidden_delta / numpy | 6.796 (6.651-7.013) | 6.911 (6.666-7.089) | +1.7% | 6.917, 6.735, 6.832 / 6.834, 6.906, 6.911 | within noise |
| dense 30 x 784 hidden_delta / rust | 2.704 (2.56-2.784) | 2.727 (2.626-2.991) | +0.8% | 2.672, 2.686, 2.718 / 2.868, 2.667, 2.74 | within noise |
| dense 30 x 784 accumulate_gradient / numpy | 28.16 (27.58-29.13) | 28.37 (27.9-29.35) | +0.7% | 28.09, 28.07, 28.65 / 28.62, 28.54, 28.31 | within noise |
| dense 30 x 784 accumulate_gradient / rust | 6.87 (6.808-7.159) | 7.205 (6.951-7.27) | +4.9% | 6.81, 6.993, 6.964 / 7.24, 7.076, 7.215 | separated, inside spread |
| dense 30 x 784 apply_accumulated_gradient / numpy | 31.77 (30.93-32.74) | 31.99 (31.26-32.48) | +0.7% | 31.77, 30.99, 32.61 / 31.51, 32.46, 31.78 | within noise |
| dense 30 x 784 apply_accumulated_gradient / rust | 16.6 (16.28-17.16) | 17.02 (16.6-17.33) | +2.5% | 16.95, 16.37, 16.74 / 17.21, 16.86, 16.82 | within noise |
| dense 30 x 784 sgd step / numpy | 58.53 (58.2-59.58) | 60.77 (59.09-61.98) | +3.8% | 58.53, 58.52, 58.92 / 60.56, 60.49, 61.4 | consistent |
| dense 30 x 784 sgd step / rust | 7.463 (7.245-7.762) | 7.423 (7.282-7.609) | -0.5% | 7.347, 7.438, 7.669 / 7.305, 7.479, 7.513 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 37.99 (37.67-38.91) | 38.55 (37.82-39.03) | +1.5% | 38.44, 37.74, 38.3 / 38.69, 38.42, 38.54 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 50.65 (49.32-51.39) | 50.88 (49.75-51.35) | +0.5% | 49.54, 50.65, 51.3 / 50.38, 51, 51.05 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 267.3 (225.9-270) | 267.9 (265.4-268.4) | +0.2% | 245.2, 267.3, 268.9 / 266.2, 267.9, 268.4 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 363 (355.1-369.8) | 374.1 (368.3-377) | +3.1% | 355.7, 365.5, 366.9 / 370.1, 374.9, 375.8 | separated, inside spread |
| dense 30 x 784 downstream_batch b32 / numpy | 23.93 (23.47-24.08) | 23.67 (23.5-24.25) | -1.1% | 23.77, 23.93, 23.88 / 23.57, 23.73, 24 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 32.17 (31.26-33.24) | 32.3 (29.51-32.63) | +0.4% | 31.43, 32.43, 32.9 / 32.17, 32.48, 31.01 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 131.6 (130.3-132) | 131.7 (130.4-132.2) | +0.1% | 131, 131.4, 131.8 / 131.1, 131.7, 131.8 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 242.7 (238.9-244.7) | 241.9 (237.4-244.4) | -0.3% | 239.9, 244.6, 242.2 / 240.5, 239.7, 244 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 62.28 (60.97-64.67) | 62.03 (56.9-63.31) | -0.4% | 63.44, 61.43, 62.4 / 59.47, 62.41, 62.63 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / rust | 42.63 (41.01-43.29) | 42.3 (41.51-42.63) | -0.8% | 41.43, 42.89, 42.78 / 41.96, 42.41, 42.2 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 1722 (1700-1745) | 1719 (1700-1749) | -0.2% | 1706, 1722, 1744 / 1712, 1723, 1732 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / rust | 501.9 (485.6-511.1) | 505.6 (488.7-515.5) | +0.7% | 507, 500.5, 493.1 / 512.9, 505.6, 494.4 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 39.88 (39.23-40.46) | 40.51 (39.72-41.07) | +1.6% | 40.42, 39.55, 39.65 / 40.57, 40.4, 40.51 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 40.37 (39.39-41.1) | 37.7 (37-38.48) | -6.6% | 39.61, 40.37, 41.04 / 37.23, 38.04, 37.93 | consistent |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 222.3 (213.6-225.3) | 224.7 (219.8-225.3) | +1.1% | 216.5, 222.4, 224.4 / 225.2, 220.9, 224.8 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 312.6 (307.9-316.4) | 325.2 (318.3-327.5) | +4.0% | 312.3, 312.6, 310.8 / 326.3, 322.9, 324.8 | consistent |
| dense 10 x 30 forward / numpy | 4.478 (4.399-4.537) | 4.564 (4.324-4.642) | +1.9% | 4.504, 4.44, 4.506 / 4.532, 4.433, 4.615 | within noise |
| dense 10 x 30 forward / rust | 0.3549 (0.337-0.3731) | 0.3518 (0.3443-0.3604) | -0.9% | 0.3459, 0.3556, 0.3599 / 0.3552, 0.3523, 0.3481 | within noise |
| dense 10 x 30 downstream / numpy | 0.8309 (0.8034-0.8521) | 0.8331 (0.8151-0.9005) | +0.3% | 0.8248, 0.8384, 0.8309 / 0.8906, 0.8192, 0.8331 | within noise |
| dense 10 x 30 downstream / rust | 0.2076 (0.1956-0.2112) | 0.2063 (0.1978-0.2107) | -0.6% | 0.2034, 0.2078, 0.2038 / 0.2044, 0.2091, 0.202 | within noise |
| dense 10 x 30 hidden_delta / numpy | 2.236 (2.171-2.3) | 2.238 (2.197-2.25) | +0.1% | 2.185, 2.254, 2.279 / 2.217, 2.225, 2.241 | within noise |
| dense 10 x 30 hidden_delta / rust | 0.4377 (0.4192-0.4647) | 0.4276 (0.4224-0.4881) | -2.3% | 0.4243, 0.4516, 0.4501 / 0.4237, 0.4276, 0.4674 | within noise |
| dense 10 x 30 accumulate_gradient / numpy | 2.925 (2.872-3.015) | 2.839 (2.748-2.904) | -2.9% | 2.903, 2.953, 2.966 / 2.777, 2.831, 2.902 | separated, inside spread |
| dense 10 x 30 accumulate_gradient / rust | 0.4252 (0.4066-0.4361) | 0.421 (0.4151-0.4295) | -1.0% | 0.4113, 0.4304, 0.4306 / 0.421, 0.4295, 0.4169 | within noise |
| dense 10 x 30 apply_accumulated_gradient / numpy | 4.587 (4.49-4.713) | 4.584 (4.492-4.652) | -0.1% | 4.657, 4.564, 4.563 / 4.546, 4.547, 4.639 | within noise |
| dense 10 x 30 apply_accumulated_gradient / rust | 2.244 (2.208-2.274) | 2.267 (2.173-2.319) | +1.0% | 2.246, 2.237, 2.241 / 2.226, 2.287, 2.255 | within noise |
| dense 10 x 30 sgd step / numpy | 8.323 (8.109-8.551) | 8.456 (8.278-8.543) | +1.6% | 8.283, 8.25, 8.434 / 8.391, 8.473, 8.456 | within noise |
| dense 10 x 30 sgd step / rust | 0.4735 (0.4567-0.4924) | 0.4577 (0.4516-0.4692) | -3.3% | 0.4659, 0.4753, 0.4819 / 0.4534, 0.4664, 0.4577 | within noise |
| dense 10 x 30 forward_batch b32 / numpy | 9.949 (9.811-10.2) | 9.884 (9.692-9.939) | -0.7% | 9.97, 9.854, 10.12 / 9.795, 9.905, 9.865 | within noise |
| dense 10 x 30 forward_batch b32 / rust | 4.078 (3.973-4.103) | 4.204 (4.158-4.263) | +3.1% | 3.976, 4.096, 4.078 / 4.169, 4.204, 4.254 | separated, inside spread |
| dense 10 x 30 forward_batch b512 / numpy | 54.4 (53.69-55.35) | 54.5 (54.24-55.32) | +0.2% | 53.73, 54.42, 55.16 / 54.47, 54.74, 54.87 | within noise |
| dense 10 x 30 forward_batch b512 / rust | 59.41 (57.99-59.81) | 61.94 (60.93-62.82) | +4.3% | 58.18, 59.45, 59.71 / 61.27, 61.94, 62.63 | consistent |
| dense 10 x 30 downstream_batch b32 / numpy | 1.781 (1.745-1.862) | 1.825 (1.797-1.862) | +2.5% | 1.753, 1.836, 1.775 / 1.817, 1.829, 1.835 | within noise |
| dense 10 x 30 downstream_batch b32 / rust | 1.2 (1.167-1.253) | 1.15 (1.124-1.189) | -4.2% | 1.21, 1.193, 1.201 / 1.133, 1.165, 1.157 | separated, inside spread |
| dense 10 x 30 downstream_batch b512 / numpy | 12.43 (12.24-12.6) | 12.4 (12.12-12.43) | -0.2% | 12.35, 12.43, 12.47 / 12.17, 12.41, 12.42 | within noise |
| dense 10 x 30 downstream_batch b512 / rust | 15.51 (15.01-15.68) | 15.58 (15.13-15.85) | +0.4% | 15.17, 15.63, 15.54 / 15.42, 15.36, 15.79 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 4.883 (4.588-4.945) | 4.893 (4.822-5.053) | +0.2% | 4.696, 4.93, 4.884 / 4.87, 4.882, 4.967 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 1.668 (1.617-1.737) | 1.695 (1.675-1.7) | +1.6% | 1.619, 1.668, 1.708 / 1.68, 1.695, 1.698 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 36.14 (34.81-36.92) | 34.99 (34.75-36.16) | -3.2% | 35.65, 35.87, 36.17 / 35.46, 35.21, 34.99 | separated, inside spread |
| dense 10 x 30 hidden_delta_batch b512 / rust | 22.65 (21.96-23) | 22.65 (22-22.92) | +0.0% | 22.19, 22.77, 22.87 / 22.46, 22.65, 22.65 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 4.561 (4.493-5.281) | 4.569 (4.47-4.631) | +0.2% | 4.557, 4.918, 4.534 / 4.507, 4.613, 4.576 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 1.976 (1.924-1.989) | 1.913 (1.889-1.95) | -3.1% | 1.929, 1.986, 1.976 / 1.913, 1.914, 1.93 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 24.85 (24.77-25.48) | 24.96 (24.81-25.09) | +0.5% | 24.8, 25.12, 24.98 / 25.06, 24.87, 24.94 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 32.74 (32.47-32.94) | 34.49 (33.8-34.66) | +5.3% | 32.47, 32.86, 32.79 / 34.22, 34.44, 34.49 | consistent |
| conv 28x28, 8 ch forward / numpy | 55.46 (54.46-55.84) | 55.23 (54.31-57.31) | -0.4% | 55.7, 54.65, 55.56 / 56.02, 55.74, 54.63 | within noise |
| conv 28x28, 8 ch forward / rust | 19.53 (18.62-20.25) | 21.01 (20.77-21.53) | +7.5% | 18.66, 19.61, 19.94 / 20.9, 20.97, 21.36 | separated, inside spread |
| conv 28x28, 8 ch downstream / numpy | 38.83 (38.47-40.29) | 38.9 (38.3-39.34) | +0.2% | 38.9, 38.83, 39.54 / 39, 38.53, 39.08 | within noise |
| conv 28x28, 8 ch downstream / rust | 17.83 (16.93-18.1) | 17.27 (17.09-17.74) | -3.2% | 16.94, 18.08, 17.83 / 17.15, 17.48, 17.41 | within noise |
| conv 28x28, 8 ch accumulate_gradient / numpy | 35.97 (34.91-36.36) | 35.54 (35.39-36.03) | -1.2% | 35.05, 36.16, 36.12 / 35.48, 35.8, 35.71 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 16.05 (16.01-16.19) | 15.78 (15.63-15.89) | -1.7% | 16.09, 16.13, 16.02 / 15.71, 15.78, 15.83 | consistent, small |
| conv 28x28, 8 ch forward_batch b32 / numpy | 982.9 (968.5-999) | 981.4 (965.9-993.6) | -0.2% | 982.1, 987.6, 981.9 / 972.5, 983.2, 988.6 | within noise |
| conv 28x28, 8 ch forward_batch b32 / rust | 567.2 (542-573.4) | 638.5 (624.8-654.3) | +12.6% | 545.7, 568.1, 571.4 / 631, 646.6, 645.7 | consistent |
| conv 28x28, 8 ch forward_batch b512 / numpy | 1.853e+04 (1.803e+04-1.857e+04) | 1.832e+04 (1.813e+04-1.845e+04) | -1.1% | 1.827e+04, 1.856e+04, 1.853e+04 / 1.835e+04, 1.838e+04, 1.817e+04 | within noise |
| conv 28x28, 8 ch forward_batch b512 / rust | 9409 (9046-9891) | 1.036e+04 (1.02e+04-1.076e+04) | +10.1% | 9054, 9698, 9409 / 1.031e+04, 1.053e+04, 1.039e+04 | separated, inside spread |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 605.4 (579-617.7) | 580.2 (575.7-614.3) | -4.2% | 605.2, 595.4, 605.6 / 588.4, 596, 577.7 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / rust | 508.2 (493.7-535.1) | 507 (500.4-514.7) | -0.2% | 493.9, 508.2, 531.9 / 509.5, 510.6, 502.2 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 1.632e+04 (1.611e+04-1.647e+04) | 1.609e+04 (1.595e+04-1.655e+04) | -1.4% | 1.632e+04, 1.643e+04, 1.616e+04 / 1.631e+04, 1.613e+04, 1.598e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / rust | 1428 (1406-1447) | 1427 (1420-1468) | -0.1% | 1419, 1444, 1423 / 1426, 1429, 1445 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 1218 (1177-1223) | 1306 (1293-1336) | +7.2% | 1182, 1218, 1222 / 1299, 1320, 1321 | consistent |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 535.8 (530-538) | 521.4 (521.2-528.5) | -2.7% | 535.8, 534, 534.2 / 523, 524.9, 521.3 | consistent |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 2.028e+04 (1.932e+04-2.045e+04) | 2.02e+04 (2.014e+04-2.033e+04) | -0.4% | 1.959e+04, 2.038e+04, 2.034e+04 / 2.023e+04, 2.023e+04, 2.019e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 1.162e+04 (1.156e+04-1.166e+04) | 1.151e+04 (1.148e+04-1.154e+04) | -0.9% | 1.164e+04, 1.159e+04, 1.162e+04 / 1.153e+04, 1.151e+04, 1.15e+04 | consistent, small |
| conv 8x8, 8 ch forward / numpy | 29.08 (28.39-29.94) | 28.62 (27.82-28.98) | -1.6% | 29.16, 28.78, 29.42 / 28.39, 28.62, 28.63 | separated, inside spread |
| conv 8x8, 8 ch forward / rust | 1.517 (1.48-1.554) | 1.578 (1.567-1.635) | +4.0% | 1.496, 1.515, 1.552 / 1.569, 1.577, 1.615 | separated, inside spread |
| conv 8x8, 8 ch downstream / numpy | 21.73 (21.39-22.63) | 22.07 (21.45-23.31) | +1.5% | 21.43, 21.84, 22.24 / 21.77, 22.86, 21.96 | within noise |
| conv 8x8, 8 ch downstream / rust | 1.208 (1.158-1.329) | 1.185 (1.166-1.227) | -1.9% | 1.173, 1.276, 1.208 / 1.196, 1.183, 1.192 | within noise |
| conv 8x8, 8 ch accumulate_gradient / numpy | 7.425 (7.036-7.495) | 7.323 (7.241-7.731) | -1.4% | 7.423, 7.425, 7.265 / 7.425, 7.486, 7.313 | within noise |
| conv 8x8, 8 ch accumulate_gradient / rust | 1.174 (1.168-1.189) | 1.168 (1.15-1.207) | -0.5% | 1.172, 1.179, 1.175 / 1.154, 1.179, 1.182 | within noise |
| conv 8x8, 8 ch forward_batch b32 / numpy | 75.57 (75.18-75.89) | 75.18 (74.06-76.39) | -0.5% | 75.49, 75.44, 75.69 / 75.44, 75.23, 75.18 | within noise |
| conv 8x8, 8 ch forward_batch b32 / rust | 31.46 (30.11-32.55) | 36.28 (35.08-38.45) | +15.3% | 30.41, 31.75, 31.97 / 35.38, 37.35, 36.39 | consistent |
| conv 8x8, 8 ch forward_batch b512 / numpy | 887.7 (874.5-893.2) | 890.4 (876.5-905.2) | +0.3% | 883.8, 886.5, 887.7 / 885, 895.8, 891.4 | within noise |
| conv 8x8, 8 ch forward_batch b512 / rust | 487.7 (469.5-497.5) | 562.6 (550.4-572.8) | +15.3% | 474.4, 496.1, 487.7 / 559.3, 564.2, 562.6 | consistent |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 66.58 (64.99-67.52) | 63.96 (63.42-65.29) | -3.9% | 66.72, 65.09, 67.14 / 63.81, 63.61, 65.22 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / rust | 28.45 (27.11-28.79) | 27.89 (27.63-28.25) | -1.9% | 27.81, 28.58, 28.41 / 27.64, 27.89, 28.2 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 699.9 (696.9-713.3) | 697.5 (682-712.8) | -0.3% | 706.2, 697.6, 706.5 / 697.4, 697.5, 698.4 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / rust | 448.6 (425.7-477.8) | 437 (431.1-440.9) | -2.6% | 437.9, 451.4, 461.1 / 432.9, 436.6, 440.1 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 93.61 (91.46-94.86) | 97.65 (94.75-100.1) | +4.3% | 91.94, 94.23, 93.81 / 95.35, 98.69, 98.11 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 27.56 (27.46-27.69) | 27.82 (27.74-27.85) | +1.0% | 27.51, 27.54, 27.62 / 27.81, 27.78, 27.84 | consistent, small |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 1395 (1374-1414) | 1467 (1451-1569) | +5.2% | 1381, 1399, 1405 / 1466, 1469, 1511 | consistent |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 464.6 (459.2-470.4) | 457.1 (452.2-463.9) | -1.6% | 468.7, 464.1, 462 / 455.5, 460.9, 454.2 | separated, inside spread |
| conv 13x13x8, 8 ch forward / numpy | 50.87 (49.8-51.53) | 49.87 (49.66-51.9) | -2.0% | 50.86, 50.33, 51.21 / 50.89, 50.46, 49.67 | within noise |
| conv 13x13x8, 8 ch forward / rust | 20.14 (19.94-20.43) | 21.35 (21.3-21.61) | +6.0% | 19.97, 20.39, 20.11 / 21.33, 21.44, 21.48 | consistent |
| conv 13x13x8, 8 ch downstream / numpy | 51.26 (51.05-52.72) | 52.16 (50.64-53.01) | +1.7% | 51.52, 51.08, 52.07 / 51.47, 52.39, 52.45 | within noise |
| conv 13x13x8, 8 ch downstream / rust | 12 (11.64-12.4) | 12.1 (11.98-12.37) | +0.8% | 11.72, 12.1, 12.24 / 12.04, 12.23, 12.07 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 23.22 (22.65-23.43) | 23.06 (22.89-23.48) | -0.7% | 22.7, 23.33, 23.27 / 23.19, 23.06, 23.15 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 5.012 (4.971-5.144) | 5.458 (5.411-5.501) | +8.9% | 4.977, 5.1, 5.009 / 5.432, 5.452, 5.492 | consistent |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 1019 (998.5-1034) | 1015 (1005-1025) | -0.3% | 1005, 1017, 1029 / 1017, 1010, 1019 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 622.4 (616.1-630) | 637.5 (635.8-643.6) | +2.4% | 616.5, 628.8, 622.8 / 641.3, 635.9, 637.7 | separated, inside spread |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 1.417e+04 (1.406e+04-1.431e+04) | 1.424e+04 (1.413e+04-1.433e+04) | +0.5% | 1.41e+04, 1.417e+04, 1.426e+04 / 1.417e+04, 1.426e+04, 1.428e+04 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 1.848e+04 (1.839e+04-1.859e+04) | 1.881e+04 (1.865e+04-1.897e+04) | +1.8% | 1.853e+04, 1.844e+04, 1.847e+04 / 1.873e+04, 1.876e+04, 1.896e+04 | separated, inside spread |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 925.4 (877.7-967.8) | 896.2 (889.9-941.8) | -3.2% | 938.8, 889.4, 940.7 / 909, 916.1, 892.9 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 350.5 (335.5-363.9) | 353.4 (344.1-355.9) | +0.8% | 337.7, 357.4, 351.4 / 348.3, 353.8, 354.4 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 2.612e+04 (2.548e+04-2.635e+04) | 2.587e+04 (2.548e+04-2.636e+04) | -0.9% | 2.595e+04, 2.612e+04, 2.592e+04 / 2.569e+04, 2.616e+04, 2.575e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 1039 (1019-1052) | 1060 (1047-1071) | +2.1% | 1028, 1042, 1045 / 1055, 1062, 1064 | separated, inside spread |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 603.3 (591.2-613.8) | 605 (597-612.4) | +0.3% | 592, 603.8, 611.8 / 602.7, 600.3, 610.9 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 170.6 (168-173.8) | 169.1 (166.2-172.5) | -0.9% | 170.6, 169.4, 171.1 / 167.8, 169.3, 169.1 | separated, inside spread |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.044e+04 (1.003e+04-1.056e+04) | 1.05e+04 (1.034e+04-1.063e+04) | +0.6% | 1.011e+04, 1.051e+04, 1.048e+04 / 1.041e+04, 1.059e+04, 1.05e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 2569 (2533-2609) | 2604 (2599-2608) | +1.4% | 2570, 2575, 2569 / 2606, 2604, 2604 | consistent, small |
| conv 26x26x8/2, 8 ch forward / numpy | 54.83 (54.52-55.14) | 54.36 (53.47-55.68) | -0.9% | 54.63, 55.09, 54.78 / 54.69, 54.57, 54.05 | within noise |
| conv 26x26x8/2, 8 ch forward / rust | 23.99 (23.7-24.23) | 25.31 (25.11-25.66) | +5.5% | 23.75, 24.23, 23.96 / 25.18, 25.38, 25.48 | consistent |
| conv 26x26x8/2, 8 ch downstream / numpy | 61.83 (59.3-64.15) | 60.93 (59.22-62.48) | -1.4% | 63.06, 62.31, 60.09 / 60.96, 60.85, 60.85 | within noise |
| conv 26x26x8/2, 8 ch downstream / rust | 15.02 (14.57-15.52) | 15.14 (14.6-15.29) | +0.8% | 14.57, 15.3, 15.08 / 14.92, 15.2, 15.14 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 26.49 (26.14-27.25) | 26.35 (26.07-26.74) | -0.5% | 26.3, 26.53, 26.91 / 26.54, 26.15, 26.51 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 5.932 (5.713-6.39) | 5.908 (5.78-5.974) | -0.4% | 5.823, 6.161, 5.936 / 5.877, 5.884, 5.944 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 1245 (1222-1282) | 1237 (1219-1264) | -0.6% | 1226, 1262, 1249 / 1234, 1241, 1240 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 750.3 (744.2-767.9) | 762.2 (758.7-785.8) | +1.6% | 745.3, 750.3, 764.5 / 770.3, 760.2, 773.8 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 1.73e+04 (1.709e+04-1.752e+04) | 1.736e+04 (1.715e+04-1.765e+04) | +0.3% | 1.71e+04, 1.738e+04, 1.737e+04 / 1.724e+04, 1.741e+04, 1.752e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 2.3e+04 (2.278e+04-2.312e+04) | 2.318e+04 (2.294e+04-2.334e+04) | +0.8% | 2.298e+04, 2.306e+04, 2.292e+04 / 2.318e+04, 2.314e+04, 2.318e+04 | separated, inside spread |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 1254 (1201-1327) | 1207 (1169-1280) | -3.8% | 1267, 1279, 1222 / 1226, 1207, 1198 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 430.9 (410.7-438.9) | 433.4 (423.1-441) | +0.6% | 412, 436.5, 430.9 / 427.9, 432.5, 437.6 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 4.234e+04 (4.183e+04-4.259e+04) | 4.233e+04 (4.189e+04-4.266e+04) | -0.0% | 4.221e+04, 4.235e+04, 4.234e+04 / 4.232e+04, 4.228e+04, 4.233e+04 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 2328 (2302-2337) | 2326 (2304-2345) | -0.1% | 2304, 2330, 2333 / 2335, 2307, 2335 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 723 (696.6-726) | 705.7 (702.1-725.7) | -2.4% | 698, 724, 724.8 / 706.7, 704.2, 713.9 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 204.4 (200.6-208.2) | 202.9 (201-207.9) | -0.7% | 204.4, 204.5, 204.3 / 205.9, 202.9, 201.5 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 1.234e+04 (1.184e+04-1.252e+04) | 1.23e+04 (1.217e+04-1.249e+04) | -0.3% | 1.192e+04, 1.245e+04, 1.234e+04 / 1.221e+04, 1.236e+04, 1.241e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 3048 (3010-3094) | 3079 (3001-3109) | +1.0% | 3025, 3075, 3042 / 3004, 3101, 3086 | within noise |
| conv 26x26x8, 8 ch forward / numpy | 126.2 (124.2-130.8) | 126 (124.9-128.9) | -0.2% | 126.8, 124.4, 128.5 / 125.2, 127.6, 126.6 | within noise |
| conv 26x26x8, 8 ch forward / rust | 93.54 (91.38-95.87) | 97.54 (97.15-99.21) | +4.3% | 93.62, 92.44, 94.06 / 97.54, 97.23, 98.99 | consistent |
| conv 26x26x8, 8 ch downstream / numpy | 148.8 (145-157.4) | 146.1 (144.2-155.4) | -1.8% | 148.8, 151.4, 149.8 / 149.1, 149.8, 145.6 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 59.9 (56.32-64.09) | 59.03 (57.6-60.25) | -1.4% | 56.79, 60.75, 61.97 / 58.52, 59.03, 59.38 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 90.65 (88.81-92.2) | 89.99 (89.03-91.74) | -0.7% | 89.1, 91.1, 91.58 / 89.76, 90.71, 89.99 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 25.28 (24.99-25.83) | 25.31 (24.92-25.64) | +0.1% | 25.26, 25.55, 25.38 / 25.28, 25.4, 25.14 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 4321 (4137-4406) | 4263 (4184-4395) | -1.3% | 4203, 4333, 4374 / 4289, 4263, 4293 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 3059 (3031-3065) | 3111 (3082-3177) | +1.7% | 3048, 3048, 3061 / 3084, 3116, 3156 | separated, inside spread |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 6.75e+04 (6.715e+04-6.8e+04) | 6.748e+04 (6.701e+04-6.798e+04) | -0.0% | 6.722e+04, 6.769e+04, 6.779e+04 / 6.734e+04, 6.747e+04, 6.769e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 8.672e+04 (8.602e+04-8.705e+04) | 8.815e+04 (8.779e+04-8.896e+04) | +1.7% | 8.68e+04, 8.637e+04, 8.675e+04 / 8.802e+04, 8.854e+04, 8.809e+04 | consistent, small |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 4860 (4794-4966) | 4643 (4597-4832) | -4.5% | 4837, 4927, 4832 / 4694, 4756, 4602 | separated, inside spread |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 388.5 (383.5-420.9) | 392.8 (378.8-427.8) | +1.1% | 395.1, 388.5, 403.1 / 410.4, 380.6, 395.9 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 1.116e+05 (1.103e+05-1.128e+05) | 1.14e+05 (1.123e+05-1.154e+05) | +2.2% | 1.125e+05, 1.104e+05, 1.118e+05 / 1.138e+05, 1.129e+05, 1.15e+05 | separated, inside spread |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 5000 (4979-5013) | 5010 (4956-5045) | +0.2% | 5008, 4986, 4997 / 4995, 5028, 5001 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 3035 (2957-3105) | 3095 (2991-3117) | +2.0% | 2974, 3064, 3073 / 3040, 3088, 3109 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 670.8 (666.9-673.6) | 666.4 (661.4-671.2) | -0.7% | 667, 672.7, 671.6 / 667.8, 664.5, 666.5 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 5.138e+04 (5.026e+04-5.179e+04) | 5.154e+04 (5.093e+04-5.174e+04) | +0.3% | 5.074e+04, 5.152e+04, 5.155e+04 / 5.119e+04, 5.149e+04, 5.169e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 1.202e+04 (1.169e+04-1.208e+04) | 1.205e+04 (1.172e+04-1.211e+04) | +0.3% | 1.206e+04, 1.175e+04, 1.202e+04 / 1.185e+04, 1.207e+04, 1.209e+04 | within noise |
| pool 26x26, 8 ch forward / numpy | 71.03 (69.79-72.04) | 69.96 (69.49-71.31) | -1.5% | 71.74, 69.9, 71.29 / 70.72, 70.17, 69.63 | within noise |
| pool 26x26, 8 ch forward / rust | 3.787 (3.711-3.843) | 3.069 (3.018-3.127) | -19.0% | 3.721, 3.792, 3.823 / 3.024, 3.065, 3.124 | consistent |
| pool 26x26, 8 ch downstream / numpy | 35.03 (34.46-36.52) | 35.03 (34.66-36.48) | -0.0% | 35.04, 34.61, 35.82 / 35.74, 35.7, 34.77 | within noise |
| pool 26x26, 8 ch downstream / rust | 5.051 (4.926-5.12) | 5.28 (5.18-5.329) | +4.5% | 4.932, 5.077, 5.078 / 5.189, 5.304, 5.301 | separated, inside spread |
| pool 26x26, 8 ch forward_batch b32 / numpy | 1227 (1218-1250) | 1233 (1218-1252) | +0.5% | 1220, 1233, 1241 / 1221, 1238, 1244 | within noise |
| pool 26x26, 8 ch forward_batch b32 / rust | 112.2 (110.5-113.4) | 91.84 (90.65-94.13) | -18.1% | 111.2, 111.9, 112.9 / 90.71, 92.04, 93.02 | consistent |
| pool 26x26, 8 ch forward_batch b512 / numpy | 2.029e+04 (2.017e+04-2.055e+04) | 2.033e+04 (2.014e+04-2.05e+04) | +0.2% | 2.017e+04, 2.031e+04, 2.044e+04 / 2.015e+04, 2.033e+04, 2.043e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 2410 (2393-2418) | 2224 (2209-2259) | -7.7% | 2413, 2405, 2403 / 2243, 2234, 2212 | consistent |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 483.6 (477.7-502.9) | 478.8 (478.5-485.1) | -1.0% | 498.6, 483.6, 479.8 / 478.8, 481.8, 479.2 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / rust | 159 (157.8-163.3) | 162.2 (159.3-163.8) | +2.1% | 158.4, 160, 160.8 / 160, 162.5, 163.4 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 1.372e+04 (1.362e+04-1.38e+04) | 1.371e+04 (1.364e+04-1.42e+04) | -0.1% | 1.376e+04, 1.369e+04, 1.368e+04 / 1.371e+04, 1.371e+04, 1.392e+04 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / rust | 3003 (2999-3117) | 3018 (3013-3114) | +0.5% | 3000, 3026, 3061 / 3060, 3016, 3064 | within noise |
| pool 6x6, 8 ch forward / numpy | 34 (33.25-35.28) | 34.03 (33.05-34.66) | +0.1% | 34.01, 34, 34.26 / 33.86, 34.4, 33.65 | within noise |
| pool 6x6, 8 ch forward / rust | 0.4941 (0.4832-0.4985) | 0.4806 (0.4745-0.4854) | -2.7% | 0.4835, 0.4979, 0.4941 / 0.4829, 0.4752, 0.4828 | separated, inside spread |
| pool 6x6, 8 ch downstream / numpy | 19.3 (19.03-20.15) | 19.18 (18.92-19.84) | -0.6% | 19.67, 19.18, 19.42 / 19.3, 19.38, 19.17 | within noise |
| pool 6x6, 8 ch downstream / rust | 0.5817 (0.5751-0.5914) | 0.5767 (0.571-0.5976) | -0.9% | 0.5752, 0.587, 0.5823 / 0.5722, 0.5843, 0.584 | within noise |
| pool 6x6, 8 ch forward_batch b32 / numpy | 109.5 (108.3-111) | 108.9 (108.2-109.8) | -0.6% | 109.1, 109, 110.5 / 108.5, 109, 109.2 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 8.336 (8.177-8.401) | 7.241 (7.191-7.347) | -13.1% | 8.216, 8.336, 8.392 / 7.235, 7.241, 7.272 | consistent |
| pool 6x6, 8 ch forward_batch b512 / numpy | 1222 (1205-1238) | 1217 (1205-1234) | -0.4% | 1206, 1222, 1236 / 1207, 1218, 1229 | within noise |
| pool 6x6, 8 ch forward_batch b512 / rust | 129.2 (128.1-131.2) | 112.7 (111.2-114.1) | -12.8% | 128.4, 129.7, 129.9 / 111.4, 112.7, 114 | consistent |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 59.26 (58.44-60.09) | 59.62 (59.28-61.9) | +0.6% | 59.25, 59.43, 59.2 / 59.59, 60.59, 59.62 | separated, inside spread |
| pool 6x6, 8 ch downstream_batch b32 / rust | 11.43 (11.2-11.75) | 11.27 (11.17-11.52) | -1.5% | 11.23, 11.43, 11.66 / 11.2, 11.35, 11.42 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 598.8 (587.3-611.9) | 595.8 (590-609.1) | -0.5% | 593.2, 603.3, 599.6 / 599.6, 601.1, 595.5 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 181.2 (180.2-184.7) | 178.8 (176.6-181.6) | -1.3% | 180.6, 181, 184.4 / 176.7, 179.3, 180.7 | within noise |
| conv tail 32 x 5408 bare downstream b32 / numpy | 73.51 (66.48-79.53) | 73.71 (67.43-78.65) | +0.3% | 66.5, 76.39, 76.01 / 71.44, 70.13, 76.62 | within noise |
| conv tail 32 x 5408 bare downstream b32 / rust | 250.5 (247.9-255.6) | 244.6 (236.9-249.7) | -2.3% | 250.5, 251.8, 252.1 / 238.3, 245.3, 246.8 | separated, inside spread |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3191 (3182-3211) | 3207 (3192-3229) | +0.5% | 3200, 3184, 3197 / 3205, 3221, 3198 | within noise |
| conv tail 32 x 5408 bare downstream b512 / rust | 2263 (2260-2295) | 2403 (2389-2452) | +6.2% | 2278, 2263, 2275 / 2425, 2415, 2392 | consistent |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 79.29 (78.26-79.83) | 79.27 (78.29-79.83) | -0.0% | 78.71, 79.11, 79.62 / 78.78, 79.04, 79.58 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / rust | 243.6 (231.8-247.9) | 226 (221.3-231.8) | -7.2% | 234.4, 243.6, 246.7 / 225.2, 226.6, 226.6 | separated, inside spread |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 1619 (1602-1669) | 1652 (1612-1690) | +2.0% | 1613, 1632, 1636 / 1620, 1678, 1653 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / rust | 2215 (2129-2269) | 2210 (2190-2232) | -0.2% | 2187, 2253, 2173 / 2230, 2203, 2199 | within noise |
| conv tail 32 x 5408 transpose b32 / numpy | 0.708 (0.7041-0.7239) | 0.7163 (0.7005-0.7209) | +1.2% | 0.7049, 0.7076, 0.7228 / 0.7074, 0.7183, 0.7179 | within noise |
| conv tail 32 x 5408 transpose b32 / rust | 0.8518 (0.8329-0.8737) | 0.546 (0.5313-0.551) | -35.9% | 0.836, 0.8518, 0.8683 / 0.5403, 0.5443, 0.546 | consistent |
| conv tail 32 x 5408 transpose b512 / numpy | 12.36 (11.29-13.69) | 12.28 (11.02-13.72) | -0.7% | 11.52, 13.22, 12.38 / 12.28, 12.48, 12.31 | within noise |
| conv tail 32 x 5408 transpose b512 / rust | 12.66 (12.4-12.96) | 12.09 (11.72-12.31) | -4.5% | 12.53, 12.8, 12.72 / 12.22, 11.82, 12.11 | separated, inside spread |
| conv tail 32 x 5408 add b32 / numpy | 98.73 (98.42-101.1) | 96.64 (94.88-98.15) | -2.1% | 99.89, 98.6, 98.63 / 98.03, 96.52, 95.17 | separated, inside spread |
| conv tail 32 x 5408 add b32 / rust | 63.19 (63.03-69.39) | 63.21 (63.09-69.39) | +0.0% | 66.28, 63.12, 63.22 / 63.17, 66.27, 63.21 | within noise |
| conv tail 32 x 5408 add b512 / numpy | 97.08 (96.86-99.63) | 95.65 (94.11-99.88) | -1.5% | 98.27, 96.89, 98.37 / 97.14, 95.54, 95.57 | within noise |
| conv tail 32 x 5408 add b512 / rust | 65.34 (64.25-71.32) | 63.35 (62.92-69.75) | -3.0% | 66.92, 64.46, 67.9 / 66.22, 66.36, 63.35 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 1.464 (1.407-1.558) | 1.431 (1.395-1.519) | -2.2% | 1.448, 1.454, 1.507 / 1.406, 1.482, 1.426 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.4343 (0.4224-0.4471) | 0.4393 (0.4373-0.4454) | +1.1% | 0.4245, 0.4384, 0.4412 / 0.439, 0.4438, 0.4379 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 11.18 (11.02-11.27) | 11.36 (11.21-11.54) | +1.7% | 11.18, 11.09, 11.25 / 11.29, 11.47, 11.29 | separated, inside spread |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 4.901 (4.738-5.009) | 5.14 (5.062-5.214) | +4.9% | 4.757, 4.961, 4.939 / 5.073, 5.14, 5.204 | separated, inside spread |
| dense 30 x 784 bare downstream b32 / numpy | 23.51 (23.18-23.8) | 23.59 (23.07-23.87) | +0.3% | 23.51, 23.47, 23.49 / 23.61, 23.38, 23.6 | within noise |
| dense 30 x 784 bare downstream b32 / rust | 29.57 (29-30.58) | 28.91 (28.63-29.8) | -2.2% | 29.07, 30.03, 30.08 / 28.82, 29.03, 29.22 | within noise |
| dense 30 x 784 bare downstream b512 / numpy | 137.4 (112.9-137.9) | 138.8 (136.8-143) | +1.0% | 125.2, 137.6, 137.5 / 139.8, 140.2, 137.5 | within noise |
| dense 30 x 784 bare downstream b512 / rust | 246.2 (239.1-248.1) | 245.6 (239.8-248.9) | -0.3% | 243.6, 246.6, 245.3 / 244.4, 245.9, 245.1 | within noise |
| dense 30 x 784 bare accumulate b32 / numpy | 28.32 (27.84-29.02) | 28.64 (27.92-29.11) | +1.1% | 28.31, 28.47, 28.34 / 29.01, 28.4, 28.16 | within noise |
| dense 30 x 784 bare accumulate b32 / rust | 32.06 (31.38-33.52) | 31.51 (30.68-32.37) | -1.7% | 31.58, 32.06, 33.09 / 31.16, 31.15, 32 | within noise |
| dense 30 x 784 bare accumulate b512 / numpy | 195.5 (192.3-198.4) | 194.5 (192.5-196.9) | -0.5% | 194.2, 196.3, 195.6 / 193.4, 193.8, 195.8 | within noise |
| dense 30 x 784 bare accumulate b512 / rust | 280.7 (274-288.3) | 286.8 (282.2-291.3) | +2.1% | 277, 284.9, 282.4 / 288.6, 282.6, 288.7 | within noise |
| dense 30 x 784 transpose b32 / numpy | 0.6917 (0.6809-0.7089) | 0.7048 (0.6803-0.7573) | +1.9% | 0.6817, 0.6917, 0.7079 / 0.6915, 0.7247, 0.7239 | within noise |
| dense 30 x 784 transpose b32 / rust | 0.8312 (0.8098-0.8545) | 0.5575 (0.5516-0.5629) | -32.9% | 0.8118, 0.8312, 0.8476 / 0.5519, 0.5575, 0.5609 | consistent |
| dense 30 x 784 transpose b512 / numpy | 7.218 (7.159-7.574) | 7.165 (7.128-7.394) | -0.7% | 7.18, 7.413, 7.22 / 7.272, 7.205, 7.154 | within noise |
| dense 30 x 784 transpose b512 / rust | 13.65 (13.15-14.37) | 12.96 (12.01-13.83) | -5.1% | 13.64, 13.73, 13.76 / 12.5, 13.09, 13.2 | separated, inside spread |
| dense 30 x 784 add b32 / numpy | 9.026 (8.873-9.605) | 10.66 (10.39-11.11) | +18.1% | 8.959, 9.183, 9.296 / 10.82, 10.86, 10.55 | consistent |
| dense 30 x 784 add b32 / rust | 8.679 (8.511-8.919) | 9.034 (8.605-9.734) | +4.1% | 8.759, 8.601, 8.679 / 9.4, 9.047, 8.886 | separated, inside spread |
| dense 30 x 784 add b512 / numpy | 12.28 (12.24-12.56) | 12.53 (12.21-12.94) | +2.1% | 12.27, 12.38, 12.41 / 12.8, 12.56, 12.23 | within noise |
| dense 30 x 784 add b512 / rust | 8.587 (8.422-8.858) | 8.723 (8.397-9.319) | +1.6% | 8.64, 8.587, 8.588 / 8.815, 8.96, 8.666 | separated, inside spread |
| dense 30 x 784 sum_axis0 b32 / numpy | 1.603 (1.532-1.692) | 1.463 (1.429-1.506) | -8.7% | 1.582, 1.6, 1.633 / 1.455, 1.46, 1.485 | consistent |
| dense 30 x 784 sum_axis0 b32 / rust | 0.3956 (0.3802-0.4056) | 0.4094 (0.4036-0.4113) | +3.5% | 0.3824, 0.3978, 0.4029 / 0.4057, 0.4105, 0.4094 | separated, inside spread |
| dense 30 x 784 sum_axis0 b512 / numpy | 12.26 (12.23-12.4) | 10.91 (10.73-11.06) | -11.0% | 12.25, 12.24, 12.37 / 10.8, 10.9, 11.01 | consistent |
| dense 30 x 784 sum_axis0 b512 / rust | 4.146 (4.036-4.219) | 4.536 (4.389-4.573) | +9.4% | 4.072, 4.133, 4.214 / 4.405, 4.561, 4.544 | consistent |
| dense 10 x 30 bare downstream b32 / numpy | 1.81 (1.721-1.861) | 1.806 (1.792-1.913) | -0.2% | 1.744, 1.849, 1.81 / 1.835, 1.803, 1.853 | within noise |
| dense 10 x 30 bare downstream b32 / rust | 1.144 (1.109-1.169) | 1.152 (1.133-1.193) | +0.7% | 1.125, 1.14, 1.158 / 1.145, 1.172, 1.151 | within noise |
| dense 10 x 30 bare downstream b512 / numpy | 12.05 (11.66-12.21) | 11.94 (11.75-12.18) | -0.8% | 11.73, 12.08, 12.12 / 11.8, 12.14, 11.94 | within noise |
| dense 10 x 30 bare downstream b512 / rust | 15.82 (15.48-16.39) | 15.9 (15.49-16.21) | +0.5% | 15.61, 16.05, 15.91 / 15.62, 15.8, 16.13 | within noise |
| dense 10 x 30 bare accumulate b32 / numpy | 1.797 (1.761-1.843) | 1.846 (1.795-1.88) | +2.7% | 1.812, 1.782, 1.818 / 1.862, 1.853, 1.796 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 1.2 (1.194-1.226) | 1.207 (1.197-1.23) | +0.6% | 1.195, 1.212, 1.21 / 1.197, 1.226, 1.207 | within noise |
| dense 10 x 30 bare accumulate b512 / numpy | 13.38 (13.27-13.7) | 13.45 (13.35-13.76) | +0.6% | 13.32, 13.36, 13.61 / 13.41, 13.51, 13.59 | within noise |
| dense 10 x 30 bare accumulate b512 / rust | 25.3 (25.25-25.37) | 25.36 (25.2-25.94) | +0.2% | 25.26, 25.3, 25.36 / 25.28, 25.59, 25.36 | within noise |
| dense 10 x 30 transpose b32 / numpy | 0.4519 (0.4442-0.4668) | 0.4462 (0.4373-0.4556) | -1.3% | 0.4447, 0.4519, 0.4616 / 0.4462, 0.4459, 0.45 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.3867 (0.3707-0.3952) | 0.3166 (0.3085-0.3255) | -18.1% | 0.3728, 0.3914, 0.3885 / 0.3128, 0.3203, 0.3194 | consistent |
| dense 10 x 30 transpose b512 / numpy | 2.966 (2.941-2.983) | 2.989 (2.899-3.004) | +0.8% | 2.981, 2.967, 2.943 / 2.994, 2.976, 2.951 | within noise |
| dense 10 x 30 transpose b512 / rust | 3.993 (3.905-4.056) | 6.069 (5.998-6.353) | +52.0% | 3.94, 4.013, 4.032 / 6.109, 6.047, 6.175 | consistent |
| dense 10 x 30 add b32 / numpy | 0.4098 (0.4031-0.4204) | 0.4073 (0.4037-0.4171) | -0.6% | 0.4037, 0.4179, 0.4098 / 0.4061, 0.4073, 0.4119 | within noise |
| dense 10 x 30 add b32 / rust | 0.1933 (0.1894-0.1987) | 0.1906 (0.1863-0.1983) | -1.4% | 0.1903, 0.1933, 0.1982 / 0.1871, 0.1948, 0.1922 | within noise |
| dense 10 x 30 add b512 / numpy | 0.4232 (0.4146-0.4292) | 0.418 (0.4138-0.4386) | -1.2% | 0.4172, 0.4262, 0.4244 / 0.416, 0.4386, 0.4174 | within noise |
| dense 10 x 30 add b512 / rust | 0.2052 (0.198-0.2093) | 0.2081 (0.202-0.2128) | +1.4% | 0.199, 0.2052, 0.2088 / 0.2043, 0.2076, 0.212 | within noise |
| dense 10 x 30 sum_axis0 b32 / numpy | 1.294 (1.277-1.318) | 1.31 (1.293-1.318) | +1.3% | 1.28, 1.294, 1.311 / 1.299, 1.316, 1.306 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.2859 (0.2763-0.2928) | 0.3224 (0.3191-0.3327) | +12.7% | 0.2764, 0.2862, 0.2893 / 0.3204, 0.3264, 0.3257 | consistent |
| dense 10 x 30 sum_axis0 b512 / numpy | 9.067 (8.915-9.315) | 9.099 (8.984-9.757) | +0.4% | 8.929, 9.067, 9.226 / 9.028, 9.442, 9.093 | within noise |
| dense 10 x 30 sum_axis0 b512 / rust | 2.577 (2.488-2.624) | 3.288 (3.253-3.326) | +27.6% | 2.493, 2.58, 2.606 / 3.266, 3.276, 3.325 | consistent |
| attention 16 x 32 forward_batch b32 / numpy | 287.3 (286.1-291) | 289.2 (286.9-294.2) | +0.7% | 288.6, 286.9, 287.7 / 290.1, 290.6, 288.8 | separated, inside spread |
| attention 16 x 32 forward_batch b32 / rust | 365.1 (357.4-373.8) | 401.1 (398.1-408) | +9.9% | 358.4, 365.1, 369.8 / 401.1, 398.6, 406.5 | consistent |
| attention 16 x 32 forward_batch b512 / numpy | 5048 (4691-5180) | 5083 (4989-5177) | +0.7% | 4831, 5078, 5137 / 5034, 5123, 5110 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 5611 (5487-5743) | 6216 (6177-6350) | +10.8% | 5562, 5632, 5632 / 6183, 6232, 6282 | consistent |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 263 (262.6-270) | 267.9 (261.7-269.1) | +1.8% | 266.5, 262.7, 264.7 / 268.6, 264.7, 265.7 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / rust | 251.2 (246.2-253.8) | 238.5 (230.2-241) | -5.1% | 247.9, 252.7, 251.5 / 230.7, 239.3, 240 | separated, inside spread |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 4577 (4355-4587) | 4575 (4537-4718) | -0.0% | 4448, 4586, 4577 / 4575, 4569, 4649 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / rust | 4805 (4746-4868) | 4547 (4409-4601) | -5.4% | 4789, 4838, 4807 / 4546, 4551, 4502 | consistent |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 245 (242.8-247.4) | 242 (241.4-252.5) | -1.3% | 246.1, 244.5, 244.1 / 249.8, 241.9, 241.6 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 202.6 (187.8-229.3) | 246.3 (235.5-262) | +21.6% | 206.1, 192.7, 214.4 / 251.5, 239.9, 248.4 | consistent |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5532 (5392-5625) | 5612 (5452-5662) | +1.4% | 5508, 5538, 5532 / 5551, 5653, 5539 | separated, inside spread |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 4041 (4011-4098) | 4085 (4057-4155) | +1.1% | 4063, 4041, 4033 / 4141, 4059, 4085 | within noise |
