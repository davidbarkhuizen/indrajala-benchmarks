Old `6f0e9de` against new `6f0e9de`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `f31e318a10d7`) on both sides. Machine check: profile: identity matches; max 1-min load 0.87; busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / conv 26x26x8/2, 8 ch downstream / numpy -1.7% (58.91 -> 57.93 µs)
- consistent: per call / conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy +1.6% (2980 -> 3028 µs)
- consistent: per call / conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust -1.5% (1.22e+04 -> 1.201e+04 µs)
- consistent: per call / dense 30 x 784 apply_accumulated_gradient / numpy -1.5% (31.42 -> 30.94 µs)
- consistent: per call / dense 10 x 30 bare downstream b512 / rust -1.5% (15.66 -> 15.42 µs)
- consistent: per call / dense 10 x 30 sum_axis0 b512 / numpy +1.1% (8.973 -> 9.074 µs)
- 252 rows within noise (23 separated inside their spread), max |Δ| 7.1%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 27.31 (27.08-29.6) | 27.05 (26.86-29.61) | -1.0% | 28.43, 27.19, 28.42 / 27.01, 27.59, 28.24 | within noise |
| conv tail 32 x 5408 forward / rust | 19.39 (19.09-20.86) | 20.76 (18.96-22.6) | +7.1% | 20.1, 19.39, 19.93 / 20.95, 19.95, 20.76 | within noise |
| conv tail 32 x 5408 downstream / numpy | 23.98 (23.55-24.63) | 23.57 (23.39-25.82) | -1.7% | 24.56, 23.56, 23.98 / 23.54, 24.7, 23.48 | within noise |
| conv tail 32 x 5408 downstream / rust | 20.86 (20.7-22.11) | 21.55 (20.87-23.81) | +3.3% | 20.86, 21.4, 21.32 / 21.51, 22.38, 21.61 | separated, inside spread |
| conv tail 32 x 5408 hidden_delta / numpy | 32.11 (31.17-33.04) | 31.72 (31.43-34.65) | -1.2% | 32.72, 31.38, 32.27 / 31.6, 33.32, 31.61 | within noise |
| conv tail 32 x 5408 hidden_delta / rust | 23.09 (22.75-24.53) | 23.1 (22.93-24.05) | +0.0% | 23.18, 23.64, 23.09 / 22.97, 23.29, 23.52 | within noise |
| conv tail 32 x 5408 accumulate_gradient / numpy | 85 (84.57-87.41) | 86.26 (84.21-90.1) | +1.5% | 87.28, 85, 84.65 / 86.26, 87.62, 87.07 | within noise |
| conv tail 32 x 5408 accumulate_gradient / rust | 53.62 (52.97-54.66) | 56.27 (53.92-57.08) | +4.9% | 53.62, 54.55, 53.21 / 55.09, 56.68, 56.23 | separated, inside spread |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 184.2 (180.2-184.4) | 180.3 (180.1-188) | -2.1% | 182.3, 182.2, 184.3 / 184.1, 182.5, 180.2 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 109.4 (105.7-113.2) | 108.1 (106.3-113.4) | -1.2% | 108.7, 110.3, 109.2 / 108.1, 109.1, 109.8 | within noise |
| conv tail 32 x 5408 sgd step / numpy | 264.9 (264.7-272) | 266.3 (265.1-271.3) | +0.5% | 264.8, 265.2, 268.4 / 265.8, 268.7, 266.9 | within noise |
| conv tail 32 x 5408 sgd step / rust | 58.47 (57.81-59.32) | 58.37 (57.56-60.53) | -0.2% | 58.53, 58.34, 58.7 / 59.02, 59.04, 58.37 | within noise |
| conv tail 32 x 5408 forward_batch b32 / numpy | 146.4 (145-156.6) | 146.6 (143.6-157.8) | +0.1% | 146.1, 150.2, 150.8 / 144.2, 150.1, 152.8 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 373.6 (370.4-397.1) | 375.9 (365.9-406.6) | +0.6% | 376.7, 371.2, 386.2 / 378.1, 386.2, 375.9 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1171 (1061-1174) | 1174 (1167-1176) | +0.2% | 1116, 1173, 1172 / 1175, 1171, 1173 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1812 (1770-1852) | 1818 (1786-1841) | +0.3% | 1822, 1804, 1802 / 1814, 1809, 1826 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 77.69 (77.04-78.53) | 78.13 (77.54-78.9) | +0.6% | 77.07, 77.69, 78.47 / 78.22, 78.43, 78.13 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 240.9 (236.7-243.3) | 242 (236.4-252.5) | +0.4% | 236.9, 240.9, 242.2 / 237.8, 242, 249.8 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3264 (3235-3303) | 3277 (3264-3294) | +0.4% | 3249, 3285, 3263 / 3288, 3269, 3274 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2477 (2464-2503) | 2477 (2471-2486) | -0.0% | 2468, 2497, 2477 / 2475, 2479, 2479 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 641.9 (627.7-647.3) | 643.5 (634.6-654.7) | +0.3% | 631.3, 644.3, 644 / 641.9, 638.3, 650.6 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 315.6 (306.4-317.5) | 307.6 (303.8-322.1) | -2.5% | 311.6, 310.4, 317.4 / 313.1, 306, 310.7 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 1.257e+04 (1.247e+04-1.27e+04) | 1.249e+04 (1.238e+04-1.27e+04) | -0.6% | 1.258e+04, 1.266e+04, 1.249e+04 / 1.263e+04, 1.246e+04, 1.245e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 5858 (5834-5926) | 5845 (5811-5945) | -0.2% | 5876, 5858, 5882 / 5916, 5821, 5838 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 165.1 (157.3-165.8) | 164 (161-167.3) | -0.6% | 157.7, 165.6, 165.1 / 164.1, 164, 164.2 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 270.4 (263.4-278.2) | 270.3 (263.8-278.5) | -0.0% | 266.5, 268.2, 274.7 / 270.3, 265.1, 277.8 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 1857 (1822-1879) | 1877 (1863-1890) | +1.1% | 1847, 1870, 1851 / 1882, 1865, 1884 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 2326 (2282-2420) | 2359 (2314-2384) | +1.4% | 2358, 2351, 2304 / 2351, 2344, 2364 | within noise |
| dense 30 x 784 forward / numpy | 8.482 (8.378-9.119) | 8.466 (8.32-8.999) | -0.2% | 8.409, 8.921, 8.482 / 8.573, 8.378, 8.747 | within noise |
| dense 30 x 784 forward / rust | 2.309 (2.193-2.384) | 2.27 (2.186-2.34) | -1.7% | 2.26, 2.341, 2.298 / 2.196, 2.317, 2.27 | within noise |
| dense 30 x 784 downstream / numpy | 3.542 (3.404-3.841) | 3.542 (3.443-3.699) | +0.0% | 3.514, 3.576, 3.623 / 3.502, 3.571, 3.621 | within noise |
| dense 30 x 784 downstream / rust | 2.672 (2.641-2.899) | 2.65 (2.61-2.727) | -0.8% | 2.663, 2.655, 2.794 / 2.669, 2.654, 2.65 | within noise |
| dense 30 x 784 hidden_delta / numpy | 6.568 (6.343-6.81) | 6.494 (6.368-6.743) | -1.1% | 6.447, 6.679, 6.65 / 6.395, 6.615, 6.543 | within noise |
| dense 30 x 784 hidden_delta / rust | 3.19 (3.114-3.244) | 3.167 (3.134-3.192) | -0.7% | 3.196, 3.179, 3.189 / 3.184, 3.158, 3.155 | within noise |
| dense 30 x 784 accumulate_gradient / numpy | 27.2 (26.51-27.93) | 26.41 (25.92-27.37) | -2.9% | 27.11, 27.22, 27.2 / 26.35, 26.99, 26.18 | separated, inside spread |
| dense 30 x 784 accumulate_gradient / rust | 7.067 (6.661-7.147) | 7.057 (6.891-7.209) | -0.1% | 6.713, 7.101, 7.093 / 6.981, 7.092, 7.085 | within noise |
| dense 30 x 784 apply_accumulated_gradient / numpy | 31.42 (30.87-32.18) | 30.94 (30.8-31.14) | -1.5% | 31.42, 31.52, 31.45 / 30.96, 31.08, 30.83 | consistent |
| dense 30 x 784 apply_accumulated_gradient / rust | 16.92 (16.47-17.38) | 16.73 (16.48-17.34) | -1.1% | 16.92, 16.82, 17.04 / 17.14, 16.9, 16.51 | within noise |
| dense 30 x 784 sgd step / numpy | 59.52 (58.67-61.2) | 60.17 (58.69-61.84) | +1.1% | 60.49, 60.1, 58.78 / 60.17, 60.26, 60.01 | within noise |
| dense 30 x 784 sgd step / rust | 7.397 (7.331-7.758) | 7.515 (7.298-7.704) | +1.6% | 7.333, 7.597, 7.438 / 7.467, 7.452, 7.573 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 38.53 (37.39-38.65) | 37.9 (37.66-38.44) | -1.6% | 37.94, 38.61, 38.46 / 38.05, 38.08, 37.83 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 44.32 (43.67-44.93) | 44.12 (43.81-44.79) | -0.5% | 43.78, 44.53, 44.7 / 43.92, 44.46, 44.14 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 267 (224.9-267.9) | 266.3 (264.3-267.6) | -0.3% | 244.6, 267.8, 267.1 / 264.8, 267.5, 266.1 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 327.1 (320.6-329.9) | 327.1 (323.9-328.5) | +0.0% | 323.8, 327.9, 327.8 / 327, 326.1, 327.1 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 23.75 (23.53-23.98) | 23.72 (23.02-24.11) | -0.1% | 23.63, 23.86, 23.84 / 23.88, 23.4, 23.68 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 28.72 (28.21-29.36) | 29.3 (28.88-29.73) | +2.0% | 28.22, 29.22, 28.83 / 29.3, 29.34, 29.3 | separated, inside spread |
| dense 30 x 784 downstream_batch b512 / numpy | 131.7 (130.3-132.9) | 131.4 (130.4-132) | -0.2% | 131.6, 130.8, 132.3 / 130.6, 131.7, 131.6 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 244 (240.7-248.8) | 243.4 (241.4-244.1) | -0.3% | 240.9, 245.6, 245.9 / 243.3, 243.4, 242.7 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 58.42 (56.87-59.7) | 56.92 (56.34-58.03) | -2.6% | 58.86, 57.61, 58.28 / 56.68, 56.82, 57.42 | separated, inside spread |
| dense 30 x 784 hidden_delta_batch b32 / rust | 38.99 (38.01-40.24) | 38.94 (38.15-40.32) | -0.1% | 38.11, 39.66, 39.38 / 38.83, 39.59, 38.83 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 1744 (1722-1792) | 1746 (1726-1778) | +0.1% | 1740, 1728, 1785 / 1742, 1755, 1752 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / rust | 508.4 (500.8-534.7) | 513.6 (498.3-531.5) | +1.0% | 521.9, 501.4, 513.2 / 515.8, 502.3, 523 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 40.48 (39.37-41.19) | 39.97 (39.16-40.99) | -1.3% | 40.28, 40.33, 40.59 / 39.64, 39.97, 40.29 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 39.33 (38.85-40.98) | 40 (39-40.84) | +1.7% | 39.26, 39.43, 40.14 / 39.37, 39.9, 40.55 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 221.9 (218.7-225.1) | 220.9 (219.3-222.6) | -0.5% | 220.8, 221.9, 222.8 / 220, 220.5, 222.3 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 314 (309.4-323.3) | 318.8 (314.9-322.7) | +1.5% | 313.9, 315.5, 316.4 / 316, 318.8, 322.3 | within noise |
| dense 10 x 30 forward / numpy | 4.583 (4.418-4.909) | 4.467 (4.388-4.618) | -2.5% | 4.562, 4.742, 4.573 / 4.467, 4.484, 4.503 | separated, inside spread |
| dense 10 x 30 forward / rust | 0.3207 (0.3066-0.3283) | 0.317 (0.3137-0.3205) | -1.1% | 0.3093, 0.3268, 0.3218 / 0.3155, 0.319, 0.3164 | within noise |
| dense 10 x 30 downstream / numpy | 0.8308 (0.806-0.8617) | 0.8445 (0.8248-0.8659) | +1.6% | 0.81, 0.8308, 0.8594 / 0.8511, 0.8503, 0.834 | within noise |
| dense 10 x 30 downstream / rust | 0.1981 (0.1902-0.2097) | 0.1987 (0.1949-0.201) | +0.3% | 0.1912, 0.1981, 0.2088 / 0.1966, 0.1993, 0.1991 | within noise |
| dense 10 x 30 hidden_delta / numpy | 2.235 (2.178-2.279) | 2.27 (2.217-2.302) | +1.6% | 2.194, 2.232, 2.27 / 2.241, 2.28, 2.288 | within noise |
| dense 10 x 30 hidden_delta / rust | 0.4038 (0.3972-0.4093) | 0.4089 (0.3963-0.4202) | +1.3% | 0.3979, 0.4048, 0.4082 / 0.4033, 0.4138, 0.4121 | within noise |
| dense 10 x 30 accumulate_gradient / numpy | 2.769 (2.686-2.829) | 2.733 (2.703-2.82) | -1.3% | 2.724, 2.781, 2.794 / 2.717, 2.738, 2.768 | within noise |
| dense 10 x 30 accumulate_gradient / rust | 0.4167 (0.405-0.4401) | 0.4186 (0.4037-0.4209) | +0.5% | 0.4098, 0.4154, 0.4348 / 0.4107, 0.4177, 0.4202 | within noise |
| dense 10 x 30 apply_accumulated_gradient / numpy | 4.449 (4.364-4.621) | 4.448 (4.395-4.588) | -0.0% | 4.404, 4.484, 4.527 / 4.428, 4.418, 4.523 | within noise |
| dense 10 x 30 apply_accumulated_gradient / rust | 2.219 (2.177-2.247) | 2.225 (2.189-2.286) | +0.3% | 2.207, 2.212, 2.232 / 2.262, 2.225, 2.2 | within noise |
| dense 10 x 30 sgd step / numpy | 8.225 (8.076-8.498) | 8.227 (8.124-8.265) | +0.0% | 8.352, 8.187, 8.213 / 8.24, 8.179, 8.227 | within noise |
| dense 10 x 30 sgd step / rust | 0.4655 (0.4481-0.4767) | 0.4625 (0.4555-0.4806) | -0.6% | 0.453, 0.475, 0.4622 / 0.4606, 0.468, 0.4662 | within noise |
| dense 10 x 30 forward_batch b32 / numpy | 9.748 (9.483-9.998) | 9.723 (9.464-10.09) | -0.3% | 9.74, 9.791, 9.707 / 9.568, 9.808, 9.934 | within noise |
| dense 10 x 30 forward_batch b32 / rust | 3.147 (3.065-3.31) | 3.134 (3.081-3.207) | -0.4% | 3.187, 3.148, 3.137 / 3.121, 3.185, 3.095 | within noise |
| dense 10 x 30 forward_batch b512 / numpy | 54.39 (53.65-55.09) | 54.59 (53.92-55.43) | +0.4% | 53.78, 54.5, 54.93 / 54.49, 54.53, 54.92 | within noise |
| dense 10 x 30 forward_batch b512 / rust | 43.77 (42.37-44.65) | 44.34 (43.54-48.1) | +1.3% | 42.79, 43.79, 44.3 / 44.34, 44.17, 46.06 | within noise |
| dense 10 x 30 downstream_batch b32 / numpy | 1.778 (1.757-1.845) | 1.798 (1.713-1.821) | +1.2% | 1.783, 1.778, 1.804 / 1.737, 1.812, 1.799 | within noise |
| dense 10 x 30 downstream_batch b32 / rust | 1.128 (1.104-1.174) | 1.153 (1.125-1.172) | +2.2% | 1.107, 1.157, 1.128 / 1.163, 1.157, 1.135 | within noise |
| dense 10 x 30 downstream_batch b512 / numpy | 11.91 (11.81-12.15) | 12.06 (11.89-12.14) | +1.2% | 11.86, 11.91, 12.15 / 12.01, 12.06, 12.04 | within noise |
| dense 10 x 30 downstream_batch b512 / rust | 16.08 (15.54-16.42) | 16.02 (15.65-16.1) | -0.4% | 15.72, 16.08, 16.31 / 15.86, 16.02, 16.04 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 4.74 (4.694-4.913) | 4.67 (4.58-4.845) | -1.5% | 4.74, 4.733, 4.803 / 4.619, 4.753, 4.745 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 1.686 (1.65-1.696) | 1.683 (1.667-1.695) | -0.2% | 1.672, 1.688, 1.686 / 1.677, 1.687, 1.677 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 35.36 (33.84-35.84) | 34 (33.83-35.46) | -3.8% | 34.83, 35.09, 35.36 / 33.87, 35.11, 33.96 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / rust | 22.42 (21.56-23) | 22.31 (22.06-22.73) | -0.5% | 21.82, 22.73, 22.68 / 22.53, 22.21, 22.28 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 4.57 (4.34-4.722) | 4.42 (4.37-4.66) | -3.3% | 4.577, 4.55, 4.531 / 4.412, 4.456, 4.521 | separated, inside spread |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 1.91 (1.886-1.927) | 1.926 (1.904-1.948) | +0.8% | 1.91, 1.91, 1.906 / 1.936, 1.916, 1.933 | separated, inside spread |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 24.93 (24.49-25.27) | 24.81 (24.48-25.12) | -0.5% | 24.56, 24.93, 25.27 / 24.75, 24.99, 24.62 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 33.6 (32.5-36.58) | 32.88 (32.63-33.93) | -2.1% | 32.52, 36.4, 33.6 / 32.69, 33.75, 32.88 | within noise |
| conv 28x28, 8 ch forward / numpy | 53.77 (51.29-54.49) | 52.14 (51.49-54.03) | -3.0% | 51.56, 53.85, 54.13 / 52.89, 52.91, 51.61 | within noise |
| conv 28x28, 8 ch forward / rust | 21.46 (20.93-21.79) | 21.61 (21.26-21.78) | +0.7% | 21.05, 21.57, 21.61 / 21.44, 21.65, 21.67 | within noise |
| conv 28x28, 8 ch downstream / numpy | 38.78 (37.88-39.74) | 38.36 (37.27-39.25) | -1.1% | 38.6, 38.81, 39.21 / 38.84, 38.26, 37.71 | within noise |
| conv 28x28, 8 ch downstream / rust | 16.83 (16.5-17.27) | 16.98 (16.55-17.5) | +0.9% | 16.58, 16.82, 17.2 / 16.74, 16.82, 17.33 | within noise |
| conv 28x28, 8 ch accumulate_gradient / numpy | 35.94 (34.48-36.51) | 35.63 (34.99-36.05) | -0.9% | 35.02, 36.3, 36.13 / 35.91, 35.24, 35.67 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 15.8 (15.74-15.87) | 15.79 (15.73-15.87) | -0.1% | 15.8, 15.75, 15.87 / 15.76, 15.85, 15.78 | within noise |
| conv 28x28, 8 ch forward_batch b32 / numpy | 947 (939.3-953) | 936.8 (932.1-952.7) | -1.1% | 945.4, 949.7, 946.6 / 939.7, 945.8, 933.3 | within noise |
| conv 28x28, 8 ch forward_batch b32 / rust | 654 (636.9-665.8) | 654.4 (649.1-665.7) | +0.1% | 637.7, 659.9, 656.5 / 659, 651.8, 658.7 | within noise |
| conv 28x28, 8 ch forward_batch b512 / numpy | 1.718e+04 (1.701e+04-1.749e+04) | 1.692e+04 (1.68e+04-1.718e+04) | -1.5% | 1.726e+04, 1.724e+04, 1.708e+04 / 1.687e+04, 1.697e+04, 1.705e+04 | separated, inside spread |
| conv 28x28, 8 ch forward_batch b512 / rust | 1.052e+04 (1.037e+04-1.063e+04) | 1.061e+04 (1.048e+04-1.067e+04) | +0.8% | 1.042e+04, 1.052e+04, 1.063e+04 / 1.063e+04, 1.051e+04, 1.063e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 597.3 (579.8-619.6) | 579.4 (577.7-596.4) | -3.0% | 588.7, 617.6, 596.2 / 587, 579.3, 579.4 | separated, inside spread |
| conv 28x28, 8 ch downstream_batch b32 / rust | 573.6 (566-585.1) | 575.8 (566.7-576.5) | +0.4% | 566.5, 573.6, 584.3 / 571.5, 571.6, 575.8 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 1.643e+04 (1.612e+04-1.659e+04) | 1.65e+04 (1.614e+04-1.66e+04) | +0.4% | 1.616e+04, 1.654e+04, 1.643e+04 / 1.647e+04, 1.654e+04, 1.635e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / rust | 1.123e+04 (1.119e+04-1.124e+04) | 1.122e+04 (1.12e+04-1.125e+04) | -0.1% | 1.121e+04, 1.122e+04, 1.124e+04 / 1.123e+04, 1.122e+04, 1.122e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 1198 (1178-1225) | 1203 (1180-1210) | +0.4% | 1185, 1215, 1200 / 1198, 1209, 1194 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 533.2 (528.3-535.2) | 530.1 (527.9-535.1) | -0.6% | 532.5, 534.5, 530.1 / 531.8, 531.5, 528.2 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 2.155e+04 (2.121e+04-2.179e+04) | 2.149e+04 (2.128e+04-2.178e+04) | -0.2% | 2.125e+04, 2.173e+04, 2.155e+04 / 2.145e+04, 2.139e+04, 2.166e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 1.176e+04 (1.173e+04-1.177e+04) | 1.179e+04 (1.173e+04-1.183e+04) | +0.3% | 1.174e+04, 1.175e+04, 1.176e+04 / 1.178e+04, 1.179e+04, 1.18e+04 | separated, inside spread |
| conv 8x8, 8 ch forward / numpy | 27.11 (26.38-28.16) | 26.76 (26.23-27.73) | -1.3% | 26.59, 27.53, 27.43 / 27.33, 26.43, 26.61 | within noise |
| conv 8x8, 8 ch forward / rust | 1.614 (1.607-1.662) | 1.643 (1.593-1.664) | +1.8% | 1.607, 1.614, 1.644 / 1.631, 1.615, 1.652 | within noise |
| conv 8x8, 8 ch downstream / numpy | 21.21 (20.69-22.23) | 20.89 (20.64-22.04) | -1.5% | 21.65, 21.14, 21.07 / 21.43, 21.14, 20.79 | within noise |
| conv 8x8, 8 ch downstream / rust | 1.139 (1.115-1.166) | 1.134 (1.11-1.156) | -0.4% | 1.13, 1.149, 1.136 / 1.124, 1.126, 1.15 | within noise |
| conv 8x8, 8 ch accumulate_gradient / numpy | 7.369 (7.128-7.718) | 7.346 (7.094-7.639) | -0.3% | 7.423, 7.466, 7.31 / 7.346, 7.366, 7.314 | within noise |
| conv 8x8, 8 ch accumulate_gradient / rust | 1.16 (1.157-1.171) | 1.156 (1.149-1.167) | -0.3% | 1.165, 1.164, 1.157 / 1.158, 1.154, 1.162 | within noise |
| conv 8x8, 8 ch forward_batch b32 / numpy | 72.09 (70.43-72.97) | 71.66 (70.81-73.01) | -0.6% | 71.7, 72.37, 71.48 / 71.91, 72.19, 71.54 | within noise |
| conv 8x8, 8 ch forward_batch b32 / rust | 36.44 (35.72-37.14) | 36.66 (35.78-37.24) | +0.6% | 35.75, 36.44, 36.92 / 36.44, 36.57, 36.98 | within noise |
| conv 8x8, 8 ch forward_batch b512 / numpy | 864.8 (856.4-872.9) | 858.8 (853.5-873.5) | -0.7% | 862.3, 866.3, 867.1 / 864.5, 855.6, 865.3 | within noise |
| conv 8x8, 8 ch forward_batch b512 / rust | 575.2 (561.3-588.9) | 576.5 (570.9-603) | +0.2% | 561.3, 580.9, 582.2 / 577, 586.9, 576.5 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 63.3 (62.37-65.34) | 63.64 (63.07-66.32) | +0.5% | 63.1, 63.85, 63.83 / 65.71, 63.15, 63.59 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / rust | 28.25 (27.94-29.26) | 28.5 (27.64-28.9) | +0.9% | 27.94, 28.73, 28.67 / 28.27, 28.5, 28.31 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 690.8 (679.8-709.7) | 690.6 (681-727) | -0.0% | 679.8, 700, 695.6 / 701.4, 704, 685.2 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / rust | 462.2 (453.3-474.8) | 462 (451.8-468.5) | -0.0% | 453.9, 472.5, 462.2 / 458.9, 467.8, 457.6 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 93.11 (90.6-95.16) | 93.13 (92.1-94.05) | +0.0% | 90.62, 94.06, 93.43 / 92.96, 93.29, 93.13 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 27.52 (27.36-27.59) | 27.49 (27.43-27.62) | -0.1% | 27.5, 27.54, 27.44 / 27.57, 27.45, 27.52 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 1380 (1355-1396) | 1384 (1378-1505) | +0.3% | 1362, 1380, 1392 / 1382, 1443, 1393 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 461.3 (456.9-463.4) | 462.7 (457.3-463.8) | +0.3% | 459.6, 462.9, 459.8 / 463.2, 460.5, 460.3 | within noise |
| conv 13x13x8, 8 ch forward / numpy | 48.99 (48.22-49.89) | 49.48 (48.11-50.6) | +1.0% | 48.74, 49.38, 48.96 / 50.58, 49.48, 48.17 | within noise |
| conv 13x13x8, 8 ch forward / rust | 21.44 (21.41-21.51) | 21.51 (21.45-21.55) | +0.3% | 21.44, 21.49, 21.42 / 21.53, 21.48, 21.51 | within noise |
| conv 13x13x8, 8 ch downstream / numpy | 51.21 (50.25-52.09) | 51.13 (49.84-51.67) | -0.2% | 50.45, 51.99, 51.21 / 51.56, 50.35, 51.13 | within noise |
| conv 13x13x8, 8 ch downstream / rust | 12.11 (12.01-12.42) | 12.2 (12.12-12.42) | +0.7% | 12.07, 12.27, 12.09 / 12.22, 12.2, 12.27 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 23.55 (22.84-23.63) | 23.57 (23.21-23.79) | +0.1% | 23.33, 23.6, 23.19 / 23.57, 23.5, 23.5 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 4.927 (4.89-5.04) | 4.963 (4.879-5.063) | +0.7% | 4.909, 5.035, 4.914 / 4.963, 4.971, 4.974 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 992.1 (987.3-1011) | 997.1 (987.2-1014) | +0.5% | 987.8, 1006, 992.1 / 995.7, 992.2, 1007 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 636.5 (635.5-647.4) | 641.4 (635.5-651) | +0.8% | 640.5, 641.6, 636.4 / 635.6, 641.4, 650.1 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 1.403e+04 (1.387e+04-1.413e+04) | 1.404e+04 (1.388e+04-1.429e+04) | +0.0% | 1.396e+04, 1.404e+04, 1.406e+04 / 1.402e+04, 1.409e+04, 1.405e+04 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 1.876e+04 (1.835e+04-1.889e+04) | 1.854e+04 (1.835e+04-1.875e+04) | -1.2% | 1.883e+04, 1.863e+04, 1.854e+04 / 1.854e+04, 1.852e+04, 1.855e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 917.1 (890.6-950.3) | 895.6 (887.8-945.7) | -2.3% | 894.2, 949.2, 917.1 / 891.2, 937.8, 892.5 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 399.5 (386.6-408.2) | 400.8 (393.4-408) | +0.3% | 393.8, 404.6, 395.1 / 405, 402.2, 394 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 2.562e+04 (2.537e+04-2.596e+04) | 2.543e+04 (2.507e+04-2.567e+04) | -0.7% | 2.577e+04, 2.571e+04, 2.544e+04 / 2.537e+04, 2.549e+04, 2.534e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 1.033e+04 (1.024e+04-1.041e+04) | 1.029e+04 (1.017e+04-1.03e+04) | -0.4% | 1.034e+04, 1.029e+04, 1.035e+04 / 1.023e+04, 1.029e+04, 1.03e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 598.6 (584-613.6) | 606.6 (591.8-623.8) | +1.3% | 587.6, 611.2, 598.6 / 597.8, 616.6, 608.2 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 169 (165.6-172.4) | 169.1 (165.4-172.3) | +0.1% | 167.3, 168.9, 170.9 / 170.8, 170.4, 165.5 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.027e+04 (1.018e+04-1.034e+04) | 1.04e+04 (1.016e+04-1.049e+04) | +1.3% | 1.018e+04, 1.027e+04, 1.032e+04 / 1.034e+04, 1.028e+04, 1.046e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 2637 (2559-2647) | 2598 (2548-2646) | -1.5% | 2645, 2561, 2638 / 2557, 2599, 2638 | within noise |
| conv 26x26x8/2, 8 ch forward / numpy | 53.18 (52.8-53.79) | 52.19 (51.81-52.76) | -1.9% | 53.34, 52.87, 53.47 / 51.88, 52.65, 52.19 | separated, inside spread |
| conv 26x26x8/2, 8 ch forward / rust | 25.52 (25.37-25.57) | 25.55 (25.44-25.65) | +0.1% | 25.47, 25.52, 25.5 / 25.52, 25.55, 25.55 | separated, inside spread |
| conv 26x26x8/2, 8 ch downstream / numpy | 58.91 (58.46-59.69) | 57.93 (57.03-58.51) | -1.7% | 58.75, 59.07, 59.22 / 57.77, 58.14, 57.89 | consistent |
| conv 26x26x8/2, 8 ch downstream / rust | 14.37 (13.94-14.85) | 14.53 (14.37-14.64) | +1.2% | 14.03, 14.57, 14.57 / 14.64, 14.45, 14.46 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 26.37 (25.57-27.02) | 26.31 (26.25-26.73) | -0.2% | 26.06, 26.37, 26.6 / 26.29, 26.49, 26.49 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 5.883 (5.721-6) | 5.8 (5.707-6.014) | -1.4% | 5.755, 5.95, 5.89 / 5.815, 5.874, 5.8 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 1224 (1210-1254) | 1221 (1198-1238) | -0.2% | 1211, 1232, 1240 / 1228, 1225, 1211 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 767.7 (759.7-775.3) | 765.5 (760.8-780.1) | -0.3% | 767.5, 767.8, 765.4 / 761.8, 765.5, 777 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 1.726e+04 (1.706e+04-1.739e+04) | 1.722e+04 (1.713e+04-1.732e+04) | -0.2% | 1.708e+04, 1.726e+04, 1.734e+04 / 1.724e+04, 1.719e+04, 1.723e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 2.297e+04 (2.286e+04-2.312e+04) | 2.291e+04 (2.271e+04-2.319e+04) | -0.2% | 2.301e+04, 2.292e+04, 2.303e+04 / 2.295e+04, 2.306e+04, 2.28e+04 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 1226 (1203-1294) | 1249 (1200-1321) | +1.8% | 1250, 1225, 1248 / 1249, 1316, 1221 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 494.6 (477.5-506.4) | 494.3 (485.3-499.6) | -0.1% | 484.4, 498.5, 498.8 / 497.5, 494.3, 487.6 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 4.212e+04 (4.185e+04-4.273e+04) | 4.248e+04 (4.189e+04-4.301e+04) | +0.9% | 4.193e+04, 4.249e+04, 4.216e+04 / 4.259e+04, 4.233e+04, 4.25e+04 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 1.352e+04 (1.328e+04-1.435e+04) | 1.35e+04 (1.338e+04-1.386e+04) | -0.1% | 1.361e+04, 1.391e+04, 1.337e+04 / 1.369e+04, 1.344e+04, 1.349e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 706.4 (688.5-709.4) | 704.2 (703.1-708.4) | -0.3% | 688.8, 708.1, 707.3 / 703.8, 705.7, 706 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 199.8 (198.9-206.7) | 204.9 (198.9-206.8) | +2.6% | 201.1, 203.3, 199.7 / 203, 206.8, 202.8 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 1.228e+04 (1.19e+04-1.247e+04) | 1.233e+04 (1.224e+04-1.251e+04) | +0.4% | 1.199e+04, 1.229e+04, 1.245e+04 / 1.231e+04, 1.237e+04, 1.239e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 3117 (3025-3140) | 3128 (3019-3137) | +0.4% | 3137, 3066, 3117 / 3128, 3021, 3137 | within noise |
| conv 26x26x8, 8 ch forward / numpy | 125.2 (124.1-126.6) | 123.6 (122.2-126.1) | -1.2% | 124.5, 125.9, 124.8 / 123.1, 124.7, 124.2 | within noise |
| conv 26x26x8, 8 ch forward / rust | 98.14 (97.9-98.25) | 98.27 (98.04-98.47) | +0.1% | 98.08, 98.15, 98.07 / 98.33, 98.36, 98.06 | within noise |
| conv 26x26x8, 8 ch downstream / numpy | 143.3 (137.3-149.4) | 143.7 (139.2-152.4) | +0.3% | 139.1, 147.6, 145 / 148, 147, 139.5 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 58.02 (56.32-59.16) | 58.61 (57.54-58.92) | +1.0% | 57.48, 58.02, 58.31 / 58.47, 58.62, 58.1 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 90.37 (87.8-92.18) | 89.18 (87.86-91.14) | -1.3% | 88.98, 90.65, 90.62 / 88.29, 89.18, 90.65 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 25.22 (24.8-25.54) | 25.09 (24.81-25.57) | -0.5% | 25.17, 25.21, 25.22 / 25.45, 25.18, 24.83 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 4270 (4205-4311) | 4210 (4064-4303) | -1.4% | 4260, 4242, 4308 / 4288, 4195, 4106 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 3122 (3102-3145) | 3117 (3099-3166) | -0.2% | 3117, 3124, 3122 / 3144, 3108, 3108 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 6.649e+04 (6.632e+04-6.678e+04) | 6.612e+04 (6.602e+04-6.637e+04) | -0.6% | 6.644e+04, 6.638e+04, 6.672e+04 / 6.623e+04, 6.612e+04, 6.607e+04 | separated, inside spread |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 8.654e+04 (8.599e+04-8.748e+04) | 8.67e+04 (8.612e+04-8.727e+04) | +0.2% | 8.698e+04, 8.64e+04, 8.629e+04 / 8.686e+04, 8.67e+04, 8.648e+04 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 4551 (4460-4662) | 4613 (4511-4691) | +1.4% | 4495, 4578, 4594 / 4653, 4614, 4561 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 2510 (2485-2525) | 2494 (2470-2510) | -0.6% | 2506, 2523, 2497 / 2497, 2482, 2497 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 1.152e+05 (1.146e+05-1.177e+05) | 1.149e+05 (1.148e+05-1.161e+05) | -0.2% | 1.161e+05, 1.154e+05, 1.152e+05 / 1.149e+05, 1.155e+05, 1.149e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 4.412e+04 (4.364e+04-4.522e+04) | 4.5e+04 (4.225e+04-4.626e+04) | +2.0% | 4.428e+04, 4.367e+04, 4.471e+04 / 4.571e+04, 4.478e+04, 4.366e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 2980 (2961-3018) | 3028 (3001-3042) | +1.6% | 2990, 2980, 2982 / 3017, 3037, 3020 | consistent |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 677.1 (667.9-696.8) | 682.2 (652.7-699.9) | +0.8% | 688.9, 677.1, 668.3 / 672.4, 673.7, 693.5 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 5.091e+04 (5.077e+04-5.126e+04) | 5.05e+04 (5.012e+04-5.091e+04) | -0.8% | 5.078e+04, 5.113e+04, 5.091e+04 / 5.035e+04, 5.037e+04, 5.073e+04 | separated, inside spread |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 1.22e+04 (1.216e+04-1.235e+04) | 1.201e+04 (1.187e+04-1.221e+04) | -1.5% | 1.226e+04, 1.218e+04, 1.227e+04 / 1.205e+04, 1.201e+04, 1.201e+04 | consistent |
| pool 26x26, 8 ch forward / numpy | 70.2 (69.47-72.24) | 70.03 (69.19-70.54) | -0.2% | 70.8, 70.85, 69.77 / 70.03, 70.15, 69.76 | within noise |
| pool 26x26, 8 ch forward / rust | 3.692 (3.683-3.813) | 3.707 (3.677-3.726) | +0.4% | 3.687, 3.702, 3.753 / 3.683, 3.712, 3.716 | within noise |
| pool 26x26, 8 ch downstream / numpy | 35.83 (34.87-36.55) | 35.63 (34.96-35.91) | -0.6% | 36.31, 35.38, 35.71 / 35.43, 35.48, 35.72 | within noise |
| pool 26x26, 8 ch downstream / rust | 5.111 (5.099-5.142) | 5.133 (5.096-5.207) | +0.4% | 5.11, 5.101, 5.133 / 5.146, 5.122, 5.16 | within noise |
| pool 26x26, 8 ch forward_batch b32 / numpy | 1223 (1222-1244) | 1223 (1219-1237) | +0.0% | 1223, 1223, 1233 / 1220, 1230, 1224 | within noise |
| pool 26x26, 8 ch forward_batch b32 / rust | 111.7 (110.5-112) | 110.9 (110.4-112) | -0.6% | 111.7, 111.9, 111 / 111.2, 111.4, 110.4 | within noise |
| pool 26x26, 8 ch forward_batch b512 / numpy | 2.024e+04 (2.015e+04-2.052e+04) | 2.024e+04 (2.018e+04-2.029e+04) | -0.0% | 2.024e+04, 2.018e+04, 2.039e+04 / 2.021e+04, 2.028e+04, 2.021e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 2432 (2421-2461) | 2433 (2423-2459) | +0.0% | 2422, 2460, 2432 / 2430, 2433, 2442 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 522.1 (514.3-535.9) | 522.7 (514-536.9) | +0.1% | 524, 525.2, 522.1 / 527.3, 531.5, 514.8 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / rust | 157.4 (155.7-158.1) | 155.8 (155.6-157.6) | -1.0% | 157.4, 157.8, 156.4 / 155.7, 156.6, 156.4 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 1.424e+04 (1.398e+04-1.442e+04) | 1.432e+04 (1.416e+04-1.437e+04) | +0.6% | 1.416e+04, 1.433e+04, 1.411e+04 / 1.419e+04, 1.432e+04, 1.434e+04 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / rust | 3027 (3024-3031) | 3030 (3022-3034) | +0.1% | 3027, 3025, 3030 / 3027, 3027, 3031 | within noise |
| pool 6x6, 8 ch forward / numpy | 33.81 (33.1-35.24) | 33.88 (33.23-35.06) | +0.2% | 33.81, 34.71, 33.18 / 33.59, 34.43, 33.82 | within noise |
| pool 6x6, 8 ch forward / rust | 0.4923 (0.4848-0.4959) | 0.4895 (0.4851-0.499) | -0.6% | 0.4855, 0.4948, 0.4926 / 0.4857, 0.4895, 0.4967 | within noise |
| pool 6x6, 8 ch downstream / numpy | 18.48 (18.05-18.94) | 18.63 (18.02-19.07) | +0.8% | 18.12, 18.56, 18.74 / 18.53, 18.55, 18.78 | within noise |
| pool 6x6, 8 ch downstream / rust | 0.5623 (0.5568-0.5749) | 0.5635 (0.5554-0.5696) | +0.2% | 0.5611, 0.5637, 0.5664 / 0.5596, 0.5598, 0.5664 | within noise |
| pool 6x6, 8 ch forward_batch b32 / numpy | 110 (107.7-110.6) | 109 (108.3-110.2) | -0.8% | 109.4, 110.4, 108.8 / 109.7, 109, 108.5 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 8.205 (8.151-8.372) | 8.199 (8.17-8.262) | -0.1% | 8.177, 8.297, 8.196 / 8.194, 8.216, 8.199 | within noise |
| pool 6x6, 8 ch forward_batch b512 / numpy | 1208 (1205-1223) | 1207 (1205-1211) | -0.1% | 1207, 1209, 1214 / 1208, 1209, 1207 | within noise |
| pool 6x6, 8 ch forward_batch b512 / rust | 128.1 (127.7-129) | 128.8 (127.7-129.9) | +0.6% | 128.3, 128.6, 127.7 / 128.8, 128.1, 129.6 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 58.18 (57.47-58.92) | 58.34 (57.35-59.38) | +0.3% | 57.82, 58.6, 57.95 / 57.88, 58.53, 58.36 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / rust | 11 (10.87-11.31) | 11.01 (10.94-11.14) | +0.1% | 10.9, 11.14, 11.05 / 11.05, 10.95, 11.08 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 629.9 (622.7-634.5) | 626.5 (623.5-635) | -0.6% | 623.8, 631.8, 632.4 / 626.5, 629.2, 627 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 178.2 (176.8-178.8) | 178.2 (176.9-178.8) | +0.0% | 177.6, 178.7, 177.4 / 177.9, 178.4, 177.7 | within noise |
| conv tail 32 x 5408 bare downstream b32 / numpy | 66.24 (64.97-75.69) | 66.81 (65.92-69.6) | +0.9% | 65.07, 66.24, 72.19 / 66.14, 68.08, 67.78 | within noise |
| conv tail 32 x 5408 bare downstream b32 / rust | 241.6 (237-247.6) | 244 (241.2-246.7) | +1.0% | 238.1, 245.4, 243 / 245.5, 241.8, 244.7 | within noise |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3190 (3184-3210) | 3200 (3181-3234) | +0.3% | 3190, 3190, 3199 / 3208, 3187, 3215 | within noise |
| conv tail 32 x 5408 bare downstream b512 / rust | 2504 (2475-2531) | 2514 (2481-2529) | +0.4% | 2527, 2480, 2502 / 2518, 2509, 2505 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 78.03 (77.43-78.25) | 77.97 (77.87-79.17) | -0.1% | 77.78, 77.86, 78.2 / 78.71, 77.93, 77.91 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / rust | 243.6 (239.3-248.4) | 243 (223.7-249.6) | -0.2% | 240.1, 246.5, 244.8 / 236.7, 244.4, 242.5 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 1643 (1627-1676) | 1654 (1640-1691) | +0.7% | 1637, 1660, 1652 / 1665, 1653, 1660 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / rust | 2224 (2211-2254) | 2241 (2196-2261) | +0.8% | 2214, 2239, 2225 / 2248, 2210, 2253 | within noise |
| conv tail 32 x 5408 transpose b32 / numpy | 0.7076 (0.6989-0.7209) | 0.7138 (0.7016-0.7178) | +0.9% | 0.7008, 0.7134, 0.7099 / 0.7094, 0.7133, 0.7138 | within noise |
| conv tail 32 x 5408 transpose b32 / rust | 0.8371 (0.8088-0.8513) | 0.8368 (0.8218-0.8414) | -0.0% | 0.8176, 0.8384, 0.8482 / 0.8368, 0.8316, 0.8359 | within noise |
| conv tail 32 x 5408 transpose b512 / numpy | 12.44 (10.86-24.93) | 12.3 (10.88-14.05) | -1.1% | 11.76, 12.44, 18.44 / 11.85, 12.66, 12.62 | within noise |
| conv tail 32 x 5408 transpose b512 / rust | 14.51 (14.3-15.16) | 14.65 (13.89-15.28) | +1.0% | 14.96, 14.4, 14.43 / 14.39, 15, 14.4 | within noise |
| conv tail 32 x 5408 add b32 / numpy | 84.13 (78.36-84.21) | 79.53 (78.04-81) | -5.5% | 84.13, 84.16, 81.29 / 79.53, 80.97, 78.05 | separated, inside spread |
| conv tail 32 x 5408 add b32 / rust | 66.1 (63.17-69.43) | 63.21 (63.14-63.28) | -4.4% | 67.82, 64.78, 64.63 / 63.17, 63.22, 63.22 | separated, inside spread |
| conv tail 32 x 5408 add b512 / numpy | 80.95 (77.64-84.47) | 80.78 (77.69-80.88) | -0.2% | 77.64, 82.48, 82.82 / 79.28, 79.34, 80.78 | within noise |
| conv tail 32 x 5408 add b512 / rust | 67.61 (62.65-69.35) | 62.81 (62.61-62.93) | -7.1% | 67.61, 69.33, 62.69 / 62.69, 62.83, 62.89 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 1.363 (1.344-1.399) | 1.392 (1.362-1.403) | +2.1% | 1.363, 1.373, 1.369 / 1.379, 1.392, 1.396 | separated, inside spread |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.4153 (0.4075-0.4307) | 0.416 (0.4133-0.4211) | +0.2% | 0.4118, 0.4226, 0.4188 / 0.417, 0.4183, 0.4153 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 10.26 (10.14-10.51) | 10.26 (10.18-10.55) | -0.0% | 10.32, 10.21, 10.33 / 10.24, 10.22, 10.42 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 4.721 (4.665-4.839) | 4.752 (4.687-4.801) | +0.7% | 4.687, 4.786, 4.755 / 4.763, 4.781, 4.692 | within noise |
| dense 30 x 784 bare downstream b32 / numpy | 23.77 (23.65-24.15) | 23.8 (23.46-24.31) | +0.1% | 23.96, 23.76, 23.76 / 23.49, 23.91, 24.11 | within noise |
| dense 30 x 784 bare downstream b32 / rust | 32.69 (32.11-33.24) | 33.26 (32.82-33.97) | +1.7% | 32.64, 32.69, 32.74 / 33.52, 32.95, 33.41 | separated, inside spread |
| dense 30 x 784 bare downstream b512 / numpy | 139.4 (115.8-142.7) | 139 (135.9-140.9) | -0.3% | 127.9, 137.6, 141.6 / 138.3, 139.9, 138 | within noise |
| dense 30 x 784 bare downstream b512 / rust | 242.9 (240.3-244) | 244 (242.9-245.6) | +0.5% | 241, 243.2, 243.4 / 244.7, 244.3, 243.2 | within noise |
| dense 30 x 784 bare accumulate b32 / numpy | 29.28 (28.87-29.7) | 29.26 (28.87-29.76) | -0.1% | 29.29, 29.38, 29.23 / 29.46, 29.32, 29.21 | within noise |
| dense 30 x 784 bare accumulate b32 / rust | 29.46 (28.6-30.91) | 30.01 (29.25-30.48) | +1.9% | 28.99, 29.95, 30.01 / 29.76, 29.82, 30.32 | within noise |
| dense 30 x 784 bare accumulate b512 / numpy | 193.3 (190.9-198.3) | 194.2 (192.1-197.3) | +0.4% | 190.9, 193.3, 196.1 / 196.2, 193.1, 194.1 | within noise |
| dense 30 x 784 bare accumulate b512 / rust | 291.7 (279.9-296.5) | 287.6 (282.7-294.2) | -1.4% | 285.2, 292.8, 293.6 / 291.7, 284.4, 287 | within noise |
| dense 30 x 784 transpose b32 / numpy | 0.6884 (0.6853-0.7178) | 0.6914 (0.6837-0.6969) | +0.4% | 0.6879, 0.7017, 0.6948 / 0.695, 0.6883, 0.6876 | within noise |
| dense 30 x 784 transpose b32 / rust | 0.8021 (0.7824-0.8159) | 0.805 (0.7946-0.8265) | +0.4% | 0.7829, 0.8094, 0.8064 / 0.8024, 0.8111, 0.805 | within noise |
| dense 30 x 784 transpose b512 / numpy | 7.235 (7.122-7.368) | 7.246 (7.15-7.313) | +0.2% | 7.164, 7.214, 7.367 / 7.287, 7.198, 7.244 | within noise |
| dense 30 x 784 transpose b512 / rust | 13.13 (12.58-13.49) | 12.99 (12.8-13.2) | -1.1% | 13.03, 13.09, 13.13 / 12.99, 12.98, 13.02 | separated, inside spread |
| dense 30 x 784 add b32 / numpy | 13.81 (13.5-14.46) | 13.79 (13.52-14.63) | -0.1% | 13.93, 14.08, 13.65 / 13.8, 14.18, 13.66 | within noise |
| dense 30 x 784 add b32 / rust | 8.922 (8.789-9.542) | 8.826 (8.722-9.471) | -1.1% | 8.937, 9.191, 8.906 / 8.782, 9.032, 9.114 | within noise |
| dense 30 x 784 add b512 / numpy | 9.251 (8.9-9.692) | 8.956 (8.775-9.373) | -3.2% | 9.143, 9.403, 9.25 / 8.916, 9.161, 8.899 | within noise |
| dense 30 x 784 add b512 / rust | 8.576 (8.427-9.377) | 8.706 (8.594-9.374) | +1.5% | 8.77, 8.988, 8.462 / 8.631, 8.769, 9.065 | within noise |
| dense 30 x 784 sum_axis0 b32 / numpy | 1.429 (1.406-1.441) | 1.424 (1.395-1.491) | -0.4% | 1.423, 1.437, 1.416 / 1.398, 1.428, 1.465 | within noise |
| dense 30 x 784 sum_axis0 b32 / rust | 0.3925 (0.3862-0.3954) | 0.3975 (0.3952-0.4017) | +1.3% | 0.3892, 0.394, 0.3931 / 0.3994, 0.3975, 0.3972 | separated, inside spread |
| dense 30 x 784 sum_axis0 b512 / numpy | 10.85 (10.56-11.09) | 10.78 (10.66-10.87) | -0.7% | 10.68, 10.92, 10.92 / 10.74, 10.74, 10.86 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 4.309 (4.157-4.442) | 4.32 (4.295-4.337) | +0.3% | 4.228, 4.381, 4.295 / 4.33, 4.312, 4.312 | within noise |
| dense 10 x 30 bare downstream b32 / numpy | 1.781 (1.756-1.812) | 1.771 (1.714-1.859) | -0.6% | 1.791, 1.784, 1.773 / 1.756, 1.82, 1.761 | within noise |
| dense 10 x 30 bare downstream b32 / rust | 1.13 (1.106-1.158) | 1.133 (1.126-1.149) | +0.2% | 1.132, 1.13, 1.135 / 1.146, 1.129, 1.132 | within noise |
| dense 10 x 30 bare downstream b512 / numpy | 12.16 (12.02-12.42) | 12.22 (12.1-12.43) | +0.5% | 12.16, 12.24, 12.16 / 12.19, 12.21, 12.3 | within noise |
| dense 10 x 30 bare downstream b512 / rust | 15.66 (15.37-15.86) | 15.42 (15.28-15.52) | -1.5% | 15.6, 15.73, 15.66 / 15.35, 15.46, 15.45 | consistent |
| dense 10 x 30 bare accumulate b32 / numpy | 1.754 (1.744-1.795) | 1.77 (1.747-1.842) | +0.9% | 1.776, 1.747, 1.765 / 1.798, 1.77, 1.766 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 1.189 (1.186-1.236) | 1.184 (1.182-1.188) | -0.5% | 1.187, 1.189, 1.213 / 1.183, 1.185, 1.184 | separated, inside spread |
| dense 10 x 30 bare accumulate b512 / numpy | 13.37 (13.34-13.59) | 13.43 (13.3-13.51) | +0.4% | 13.39, 13.46, 13.36 / 13.36, 13.48, 13.41 | within noise |
| dense 10 x 30 bare accumulate b512 / rust | 25.33 (25.19-25.71) | 25.5 (25.18-28.43) | +0.7% | 25.33, 25.47, 25.35 / 25.58, 25.27, 27.04 | within noise |
| dense 10 x 30 transpose b32 / numpy | 0.4453 (0.4413-0.482) | 0.452 (0.4391-0.4619) | +1.5% | 0.4617, 0.4487, 0.4448 / 0.4527, 0.4505, 0.452 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.3759 (0.3667-0.3922) | 0.3764 (0.3709-0.3882) | +0.1% | 0.3692, 0.3857, 0.3759 / 0.3715, 0.3814, 0.3816 | within noise |
| dense 10 x 30 transpose b512 / numpy | 2.971 (2.931-3.017) | 2.942 (2.93-3.024) | -1.0% | 2.955, 2.987, 2.986 / 2.955, 2.98, 2.942 | within noise |
| dense 10 x 30 transpose b512 / rust | 4.102 (4.042-4.132) | 4.044 (4.004-4.141) | -1.4% | 4.072, 4.132, 4.075 / 4.091, 4.078, 4.026 | within noise |
| dense 10 x 30 add b32 / numpy | 0.4073 (0.3973-0.4213) | 0.4077 (0.3997-0.4193) | +0.1% | 0.3984, 0.415, 0.4084 / 0.4095, 0.4075, 0.4085 | within noise |
| dense 10 x 30 add b32 / rust | 0.1898 (0.1866-0.2039) | 0.1927 (0.1872-0.1941) | +1.5% | 0.1878, 0.1907, 0.196 / 0.1939, 0.1899, 0.1908 | within noise |
| dense 10 x 30 add b512 / numpy | 0.4153 (0.4065-0.417) | 0.4227 (0.4191-0.4348) | +1.8% | 0.411, 0.416, 0.4158 / 0.4202, 0.4219, 0.43 | separated, inside spread |
| dense 10 x 30 add b512 / rust | 0.201 (0.198-0.2052) | 0.2029 (0.199-0.2075) | +0.9% | 0.1999, 0.2043, 0.1999 / 0.2029, 0.2067, 0.1999 | within noise |
| dense 10 x 30 sum_axis0 b32 / numpy | 1.275 (1.263-1.291) | 1.294 (1.27-1.301) | +1.5% | 1.269, 1.273, 1.288 / 1.278, 1.298, 1.297 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.3078 (0.3021-0.3093) | 0.3038 (0.299-0.3078) | -1.3% | 0.3068, 0.3083, 0.3057 / 0.2995, 0.3038, 0.3067 | within noise |
| dense 10 x 30 sum_axis0 b512 / numpy | 8.973 (8.86-9.099) | 9.074 (9.013-9.154) | +1.1% | 8.936, 9.004, 8.986 / 9.083, 9.08, 9.074 | consistent |
| dense 10 x 30 sum_axis0 b512 / rust | 2.955 (2.889-2.993) | 2.948 (2.933-2.998) | -0.2% | 2.905, 2.979, 2.955 / 2.937, 2.965, 2.974 | within noise |
