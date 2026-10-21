Old `69bf104` against new `69bf104`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `5d47987e03dd`) on both sides. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.08; busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / conv 28x28, 8 ch downstream_batch b32 / numpy -5.6% (615.3 -> 580.7 µs)
- consistent: per call / dense 10 x 30 forward / rust +3.1% (0.3456 -> 0.3564 µs)
- consistent, small: per call / dense 10 x 30 accumulate_gradient_batch b512 / rust -1.8% (33.48 -> 32.86 µs)
- 267 rows within noise (31 separated inside their spread), max |Δ| 9.1%
- spread of per-pass medians over 270 rows: median 3.2%, 90th percentile 6.8%, max 33.6%
- pass shifts (median over rows of pass median / pooled median): 1 -0.3%, 2 -0.3%, 3 -0.2%, 4 +0.3%, 5 +0.2%, 6 +0.5%

### per call

| case | median (min-max) µs | per-pass medians (1, 2, 3, 4, 5, 6) | spread |
|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 28.38 (27.26-29.94) | 28.58, 28.36, 27.89, 28.02, 27.83, 29.21 | 4.9% |
| conv tail 32 x 5408 forward / rust | 20.81 (18.84-22.72) | 20.84, 19.11, 20.93, 20.93, 21.14, 20.18 | 9.8% |
| conv tail 32 x 5408 downstream / numpy | 24.89 (24.06-26.2) | 26.15, 24.83, 24.52, 24.86, 24.47, 25.59 | 6.7% |
| conv tail 32 x 5408 downstream / rust | 21.59 (20.59-24) | 21.28, 22.14, 22.58, 22.42, 22.12, 21.54 | 6.0% |
| conv tail 32 x 5408 hidden_delta / numpy | 32.69 (31.32-34.19) | 32.54, 32.04, 32.71, 33.46, 32.03, 33.33 | 4.4% |
| conv tail 32 x 5408 hidden_delta / rust | 24.32 (22.87-26.33) | 23.81, 23.51, 24.15, 26.2, 23.74, 24.23 | 11.0% |
| conv tail 32 x 5408 accumulate_gradient / numpy | 85.45 (82.88-90.03) | 87.63, 84.26, 86.65, 85.62, 84.39, 85.94 | 3.9% |
| conv tail 32 x 5408 accumulate_gradient / rust | 53.99 (51.99-56.81) | 53.16, 52.75, 55, 56.06, 54.43, 54.47 | 6.1% |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 181.1 (177-189.6) | 182.8, 180.8, 182.4, 185.3, 180.6, 181 | 2.6% |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 109.1 (107-113.4) | 109.3, 108, 109.3, 110.5, 109.1, 111.4 | 3.1% |
| conv tail 32 x 5408 sgd step / numpy | 270.4 (265-277.4) | 269.9, 269.7, 270.6, 273.5, 271.2, 273.6 | 1.5% |
| conv tail 32 x 5408 sgd step / rust | 58.97 (57.84-62.97) | 59, 58.02, 58.68, 59.56, 59.5, 60.92 | 4.9% |
| conv tail 32 x 5408 forward_batch b32 / numpy | 149 (146.7-160.2) | 148.2, 147.8, 150.4, 148.7, 155.1, 155.8 | 5.4% |
| conv tail 32 x 5408 forward_batch b32 / rust | 390.9 (373-415.8) | 392.8, 378.7, 401, 394.2, 392.1, 397.2 | 5.7% |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1167 (1051-1175) | 1109, 1165, 1167, 1172, 1169, 1167 | 5.3% |
| conv tail 32 x 5408 forward_batch b512 / rust | 1829 (1666-1927) | 1707, 1714, 1892, 1840, 1856, 1831 | 10.1% |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 79.11 (78.2-79.93) | 78.24, 78.8, 79.27, 79.32, 79.15, 79.52 | 1.6% |
| conv tail 32 x 5408 downstream_batch b32 / rust | 245.1 (238.3-249.9) | 241.8, 243.5, 244.1, 245.2, 242.6, 249.7 | 3.2% |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3114 (3077-3240) | 3098, 3086, 3116, 3118, 3191, 3120 | 3.4% |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2254 (2251-2273) | 2272, 2252, 2259, 2254, 2252, 2260 | 0.9% |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 613.9 (601.7-643.6) | 612.5, 611, 620.1, 607.4, 627.5, 616.5 | 3.3% |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 312 (302-323.4) | 306, 307.6, 313.6, 313.2, 314.2, 313.8 | 2.6% |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 1.214e+04 (1.203e+04-1.244e+04) | 1.208e+04, 1.217e+04, 1.212e+04, 1.217e+04, 1.232e+04, 1.215e+04 | 2.0% |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 5674 (5606-5714) | 5679, 5655, 5615, 5696, 5674, 5698 | 1.5% |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 163.6 (159.8-167.9) | 161.5, 163.1, 164.8, 164.2, 162.9, 165.7 | 2.6% |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 291.2 (283.8-298.1) | 290.6, 288.7, 291, 287.8, 291.6, 294.6 | 2.3% |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 1842 (1757-1916) | 1789, 1836, 1844, 1870, 1866, 1851 | 4.4% |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 2332 (2239-2391) | 2297, 2304, 2336, 2322, 2318, 2356 | 2.6% |
| dense 30 x 784 forward / numpy | 8.634 (8.249-8.951) | 8.592, 8.877, 8.56, 8.602, 8.454, 8.595 | 4.9% |
| dense 30 x 784 forward / rust | 2.382 (2.23-2.659) | 2.346, 2.322, 2.523, 2.432, 2.329, 2.519 | 8.4% |
| dense 30 x 784 downstream / numpy | 3.57 (3.212-3.765) | 3.32, 3.484, 3.557, 3.568, 3.628, 3.658 | 9.5% |
| dense 30 x 784 downstream / rust | 2.857 (2.817-2.931) | 2.827, 2.822, 2.884, 2.873, 2.863, 2.892 | 2.5% |
| dense 30 x 784 hidden_delta / numpy | 6.464 (6.208-7.218) | 6.422, 6.351, 6.592, 6.484, 6.713, 6.506 | 5.6% |
| dense 30 x 784 hidden_delta / rust | 3.44 (3.367-3.576) | 3.493, 3.415, 3.491, 3.448, 3.414, 3.389 | 3.0% |
| dense 30 x 784 accumulate_gradient / numpy | 28.28 (26.92-29.02) | 28.32, 28.33, 28.39, 28.02, 28.52, 27.83 | 2.4% |
| dense 30 x 784 accumulate_gradient / rust | 6.999 (6.7-7.264) | 7.115, 6.915, 6.812, 7.043, 7.082, 7.054 | 4.3% |
| dense 30 x 784 apply_accumulated_gradient / numpy | 31.38 (30.77-32.5) | 31.81, 31.23, 30.88, 31.61, 31.59, 31.73 | 3.0% |
| dense 30 x 784 apply_accumulated_gradient / rust | 17.18 (16.5-17.47) | 17.03, 17.1, 17.16, 17.24, 16.98, 16.94 | 1.7% |
| dense 30 x 784 sgd step / numpy | 60.11 (58.07-61.85) | 61.4, 59.36, 59.03, 60.46, 59.64, 60.46 | 3.9% |
| dense 30 x 784 sgd step / rust | 7.508 (7.306-7.779) | 7.388, 7.595, 7.508, 7.632, 7.599, 7.569 | 3.3% |
| dense 30 x 784 forward_batch b32 / numpy | 38.04 (37.74-38.67) | 38.17, 38.37, 38.1, 37.98, 38.1, 37.84 | 1.4% |
| dense 30 x 784 forward_batch b32 / rust | 48 (46.45-49.08) | 47.03, 47.91, 47.93, 48.94, 48, 48.57 | 4.0% |
| dense 30 x 784 forward_batch b512 / numpy | 267.1 (223.6-268.7) | 244.8, 264.8, 265.8, 267.8, 268.2, 268.1 | 8.8% |
| dense 30 x 784 forward_batch b512 / rust | 379.1 (366.5-389.8) | 371.6, 376.4, 380.8, 378.3, 385.1, 383.5 | 3.6% |
| dense 30 x 784 downstream_batch b32 / numpy | 23.36 (22.98-23.86) | 23.26, 23.21, 23.41, 23.42, 23.61, 23.18 | 1.8% |
| dense 30 x 784 downstream_batch b32 / rust | 29.65 (28.45-30.31) | 29.05, 29.08, 29.99, 29.96, 29.5, 29.46 | 3.2% |
| dense 30 x 784 downstream_batch b512 / numpy | 131.5 (128.9-132.7) | 129.7, 131.4, 131.2, 131.9, 131.6, 132.1 | 1.8% |
| dense 30 x 784 downstream_batch b512 / rust | 242.9 (238.2-247.6) | 240.5, 243.4, 241.3, 244.3, 241.6, 246.1 | 2.3% |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 58.75 (57.26-60.23) | 58.62, 58.97, 57.59, 59.62, 57.95, 59.06 | 3.5% |
| dense 30 x 784 hidden_delta_batch b32 / rust | 40.12 (38.49-42.15) | 39.26, 40.55, 40.61, 41.09, 39.67, 40.41 | 4.6% |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 1696 (1610-1748) | 1655, 1650, 1717, 1724, 1690, 1703 | 4.4% |
| dense 30 x 784 hidden_delta_batch b512 / rust | 501.9 (484.5-514.1) | 505.3, 501.9, 500.9, 499.4, 499.3, 493.4 | 2.4% |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 39.8 (38.94-41.18) | 40.56, 40.37, 39.55, 40.04, 39.8, 39.52 | 2.6% |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 40.44 (39.19-41.54) | 39.67, 40.44, 40.58, 41.52, 39.94, 40.1 | 4.6% |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 222.8 (213.6-226.4) | 215.8, 222, 224.3, 223.3, 223.1, 222.5 | 3.8% |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 308.2 (295.2-322.5) | 308.1, 301, 315.8, 316.3, 309.2, 306.8 | 5.0% |
| dense 10 x 30 forward / numpy | 4.429 (4.345-4.814) | 4.404, 4.394, 4.39, 4.619, 4.401, 4.437 | 5.2% |
| dense 10 x 30 forward / rust | 0.3494 (0.3414-0.3667) | 0.3456, 0.3554, 0.3542, 0.345, 0.3583, 0.346 | 3.8% |
| dense 10 x 30 downstream / numpy | 0.8263 (0.7986-0.9204) | 0.8246, 0.854, 0.8043, 0.8695, 0.8299, 0.8385 | 7.9% |
| dense 10 x 30 downstream / rust | 0.2062 (0.2003-0.2432) | 0.2078, 0.2131, 0.2228, 0.2062, 0.2097, 0.2034 | 9.4% |
| dense 10 x 30 hidden_delta / numpy | 2.209 (2.165-2.357) | 2.201, 2.288, 2.185, 2.18, 2.232, 2.239 | 4.9% |
| dense 10 x 30 hidden_delta / rust | 0.4424 (0.4359-0.4814) | 0.4382, 0.4504, 0.4429, 0.4471, 0.4609, 0.4446 | 5.1% |
| dense 10 x 30 accumulate_gradient / numpy | 2.737 (2.648-2.806) | 2.705, 2.677, 2.724, 2.716, 2.793, 2.778 | 4.2% |
| dense 10 x 30 accumulate_gradient / rust | 0.4321 (0.4207-0.4408) | 0.4236, 0.4376, 0.4298, 0.433, 0.4335, 0.4321 | 3.2% |
| dense 10 x 30 apply_accumulated_gradient / numpy | 4.444 (4.354-4.561) | 4.499, 4.443, 4.381, 4.453, 4.435, 4.477 | 2.6% |
| dense 10 x 30 apply_accumulated_gradient / rust | 2.277 (2.229-2.404) | 2.236, 2.249, 2.294, 2.325, 2.295, 2.336 | 4.4% |
| dense 10 x 30 sgd step / numpy | 8.186 (7.899-8.444) | 8.143, 8.334, 8.106, 8.198, 8.156, 8.068 | 3.3% |
| dense 10 x 30 sgd step / rust | 0.4645 (0.4472-0.5134) | 0.4552, 0.4806, 0.4631, 0.4627, 0.4663, 0.5007 | 9.8% |
| dense 10 x 30 forward_batch b32 / numpy | 9.667 (9.54-10.02) | 9.721, 9.667, 9.841, 10.01, 9.546, 9.598 | 4.8% |
| dense 10 x 30 forward_batch b32 / rust | 4.238 (4.184-4.357) | 4.217, 4.203, 4.238, 4.259, 4.292, 4.291 | 2.1% |
| dense 10 x 30 forward_batch b512 / numpy | 53.99 (53.3-55.22) | 53.96, 53.49, 53.67, 54.82, 54.14, 54.63 | 2.5% |
| dense 10 x 30 forward_batch b512 / rust | 62.02 (61.28-63.28) | 61.4, 61.96, 61.92, 62.12, 62.27, 62.84 | 2.3% |
| dense 10 x 30 downstream_batch b32 / numpy | 1.775 (1.712-1.84) | 1.753, 1.751, 1.743, 1.755, 1.772, 1.822 | 4.5% |
| dense 10 x 30 downstream_batch b32 / rust | 1.182 (1.149-1.241) | 1.157, 1.167, 1.196, 1.176, 1.183, 1.21 | 4.5% |
| dense 10 x 30 downstream_batch b512 / numpy | 12.02 (11.77-12.31) | 12.06, 11.9, 11.99, 12.24, 11.94, 12.01 | 2.8% |
| dense 10 x 30 downstream_batch b512 / rust | 15.78 (15.37-16.22) | 15.44, 15.66, 15.73, 15.85, 15.9, 16.18 | 4.7% |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 4.704 (4.533-4.812) | 4.677, 4.663, 4.699, 4.719, 4.563, 4.722 | 3.4% |
| dense 10 x 30 hidden_delta_batch b32 / rust | 1.703 (1.644-1.768) | 1.677, 1.663, 1.7, 1.717, 1.702, 1.759 | 5.6% |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 33.92 (32.97-37.78) | 34.37, 36.33, 33.63, 34.65, 33.05, 33.49 | 9.7% |
| dense 10 x 30 hidden_delta_batch b512 / rust | 22.24 (21.45-22.85) | 21.82, 22.22, 22.1, 22.49, 22.3, 22.51 | 3.1% |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 4.462 (4.364-4.647) | 4.479, 4.618, 4.406, 4.614, 4.462, 4.39 | 5.1% |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 1.982 (1.956-2.088) | 1.961, 1.984, 1.972, 2.036, 1.991, 2.003 | 3.8% |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 24.81 (24.57-25.14) | 24.93, 24.84, 24.63, 24.89, 24.69, 24.98 | 1.4% |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 33.12 (32.65-34.32) | 33.39, 32.87, 32.9, 33.83, 32.79, 33.47 | 3.1% |
| conv 28x28, 8 ch forward / numpy | 54.85 (53.79-57.75) | 55.17, 55.77, 54.69, 55.27, 54.32, 54.66 | 2.6% |
| conv 28x28, 8 ch forward / rust | 19.02 (18.5-23.07) | 18.69, 19.05, 18.93, 21.14, 19.2, 19.19 | 12.9% |
| conv 28x28, 8 ch downstream / numpy | 38.23 (37.28-40.04) | 39.03, 38.09, 38.08, 39.63, 37.78, 37.69 | 5.1% |
| conv 28x28, 8 ch downstream / rust | 17.32 (16.77-17.9) | 17.03, 17.15, 17.17, 17.56, 17.38, 17.66 | 3.7% |
| conv 28x28, 8 ch accumulate_gradient / numpy | 35.39 (34.69-35.86) | 35.09, 35.16, 35.2, 35.64, 35.53, 35.72 | 1.8% |
| conv 28x28, 8 ch accumulate_gradient / rust | 16.04 (15.95-16.19) | 16.18, 16.07, 16.07, 16.02, 16.03, 16.05 | 1.0% |
| conv 28x28, 8 ch forward_batch b32 / numpy | 960.9 (949.2-974.7) | 969, 955.3, 957.4, 973.4, 949.6, 962.2 | 2.5% |
| conv 28x28, 8 ch forward_batch b32 / rust | 557.4 (541-572.7) | 541.1, 557.4, 557.3, 557.9, 562.2, 569.2 | 5.0% |
| conv 28x28, 8 ch forward_batch b512 / numpy | 1.833e+04 (1.812e+04-1.858e+04) | 1.842e+04, 1.83e+04, 1.823e+04, 1.836e+04, 1.824e+04, 1.841e+04 | 1.0% |
| conv 28x28, 8 ch forward_batch b512 / rust | 9253 (9001-9481) | 9372, 9042, 9207, 9253, 9295, 9391 | 3.8% |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 596.1 (577.3-620.8) | 615.4, 587.5, 578, 616.7, 587.5, 605.3 | 6.5% |
| conv 28x28, 8 ch downstream_batch b32 / rust | 500.3 (480.5-505.4) | 484.1, 492, 504.8, 502.4, 502.5, 497 | 4.1% |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 1.616e+04 (1.59e+04-1.645e+04) | 1.64e+04, 1.611e+04, 1.604e+04, 1.607e+04, 1.607e+04, 1.628e+04 | 2.2% |
| conv 28x28, 8 ch downstream_batch b512 / rust | 1420 (1376-1430) | 1400, 1419, 1422, 1425, 1416, 1416 | 1.8% |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 1304 (1280-1332) | 1281, 1295, 1315, 1305, 1302, 1318 | 2.8% |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 533.2 (528.1-541.9) | 531.5, 531.5, 530.4, 538.4, 531.7, 531.5 | 1.5% |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 2.011e+04 (1.941e+04-2.033e+04) | 1.954e+04, 1.992e+04, 2.007e+04, 2.024e+04, 2.019e+04, 2.016e+04 | 3.5% |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 1.16e+04 (1.153e+04-1.163e+04) | 1.162e+04, 1.155e+04, 1.159e+04, 1.158e+04, 1.156e+04, 1.163e+04 | 0.6% |
| conv 8x8, 8 ch forward / numpy | 28.81 (27.64-30.11) | 28.81, 28.51, 28.76, 28.86, 28.73, 28.87 | 1.3% |
| conv 8x8, 8 ch forward / rust | 1.511 (1.475-1.582) | 1.483, 1.488, 1.491, 1.533, 1.552, 1.526 | 4.6% |
| conv 8x8, 8 ch downstream / numpy | 21.1 (20.8-21.84) | 21.14, 21.05, 20.91, 21.31, 21.59, 21.09 | 3.2% |
| conv 8x8, 8 ch downstream / rust | 1.201 (1.164-1.302) | 1.233, 1.181, 1.215, 1.219, 1.206, 1.201 | 4.3% |
| conv 8x8, 8 ch accumulate_gradient / numpy | 7.229 (6.989-7.484) | 7.333, 7.18, 7.11, 7.296, 7.362, 7.147 | 3.5% |
| conv 8x8, 8 ch accumulate_gradient / rust | 1.173 (1.165-1.226) | 1.171, 1.195, 1.171, 1.193, 1.192, 1.17 | 2.2% |
| conv 8x8, 8 ch forward_batch b32 / numpy | 74.68 (73.48-76.28) | 75.46, 75.22, 74.58, 74.69, 73.64, 74.19 | 2.4% |
| conv 8x8, 8 ch forward_batch b32 / rust | 31.17 (30.22-34.53) | 30.55, 30.9, 31.17, 31.82, 33.16, 31.49 | 8.4% |
| conv 8x8, 8 ch forward_batch b512 / numpy | 884.6 (874.2-901.9) | 882.7, 886.9, 881.9, 900.2, 876.3, 884.6 | 2.7% |
| conv 8x8, 8 ch forward_batch b512 / rust | 481.6 (469.5-498.6) | 472.3, 481.1, 481.6, 495.6, 489.9, 483.4 | 4.9% |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 64.35 (63.33-67.4) | 63.96, 65.87, 64.13, 64.4, 65.2, 65.01 | 3.0% |
| conv 8x8, 8 ch downstream_batch b32 / rust | 27.85 (26.99-30.17) | 27, 28.82, 27.7, 28.96, 27.96, 27.99 | 7.0% |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 694.9 (682.3-724.5) | 696.5, 700.2, 693.9, 723.1, 702, 687.3 | 5.2% |
| conv 8x8, 8 ch downstream_batch b512 / rust | 438.9 (425.5-443.8) | 425.6, 433, 436.4, 440, 441.5, 439 | 3.6% |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 97.37 (96.11-99.39) | 96.47, 96.32, 96.94, 99.01, 97.98, 98.33 | 2.8% |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 28.24 (28.17-28.48) | 28.29, 28.19, 28.24, 28.32, 28.2, 28.36 | 0.6% |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 1466 (1396-1525) | 1450, 1493, 1419, 1483, 1465, 1482 | 5.0% |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 461.2 (457.6-464.2) | 461.4, 460.7, 458.1, 461.8, 460.9, 462.7 | 1.0% |
| conv 13x13x8, 8 ch forward / numpy | 50.6 (49.27-51.77) | 50.94, 51, 50.6, 51.27, 50.08, 50.21 | 2.4% |
| conv 13x13x8, 8 ch forward / rust | 20.06 (19.91-20.53) | 20, 19.99, 20.15, 20.12, 20.25, 20.17 | 1.3% |
| conv 13x13x8, 8 ch downstream / numpy | 50.91 (49.55-52.15) | 51.67, 50.22, 50.49, 51.82, 51.24, 50.85 | 3.1% |
| conv 13x13x8, 8 ch downstream / rust | 12.26 (11.89-12.49) | 11.92, 12.19, 12.22, 12.39, 12.32, 12.25 | 3.9% |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 23 (22.64-23.6) | 22.96, 22.78, 23.3, 23.27, 23.07, 22.85 | 2.3% |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 4.982 (4.926-5.169) | 5.048, 4.931, 4.973, 5.042, 5.072, 5.03 | 2.8% |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 1002 (983.6-1023) | 998.1, 991.8, 995.8, 1013, 1010, 1007 | 2.1% |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 615.1 (614.1-630.7) | 616.1, 614.5, 615.3, 622.3, 615.5, 622.8 | 1.4% |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 1.418e+04 (1.405e+04-1.436e+04) | 1.416e+04, 1.407e+04, 1.421e+04, 1.421e+04, 1.424e+04, 1.423e+04 | 1.2% |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 1.799e+04 (1.779e+04-1.828e+04) | 1.801e+04, 1.81e+04, 1.799e+04, 1.791e+04, 1.797e+04, 1.804e+04 | 1.0% |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 917.6 (853.7-937.2) | 917.6, 887, 869.4, 930.1, 908.4, 895.4 | 6.6% |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 348.9 (335.7-359.2) | 338.6, 340.9, 348.9, 356.5, 352.3, 348.3 | 5.1% |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 2.578e+04 (2.541e+04-2.603e+04) | 2.573e+04, 2.564e+04, 2.583e+04, 2.564e+04, 2.59e+04, 2.58e+04 | 1.0% |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 1052 (1037-1089) | 1045, 1050, 1071, 1050, 1057, 1054 | 2.5% |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 596.3 (581.8-613) | 584.2, 594.1, 594.9, 602.1, 597.3, 607.4 | 3.9% |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 169 (166.8-173.6) | 171.9, 170, 167.5, 170.7, 166.9, 171.9 | 3.0% |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.031e+04 (1.004e+04-1.044e+04) | 1.013e+04, 1.015e+04, 1.039e+04, 1.025e+04, 1.039e+04, 1.034e+04 | 2.6% |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 2579 (2507-2606) | 2528, 2603, 2550, 2594, 2569, 2547 | 2.9% |
| conv 26x26x8/2, 8 ch forward / numpy | 53.55 (52.95-55.4) | 54.24, 53.44, 53.56, 54.04, 53.48, 53.4 | 1.6% |
| conv 26x26x8/2, 8 ch forward / rust | 23.85 (23.67-24.73) | 23.87, 23.77, 23.77, 23.99, 24.35, 23.79 | 2.5% |
| conv 26x26x8/2, 8 ch downstream / numpy | 60.92 (59.08-62.99) | 60.35, 61.03, 60.68, 61.55, 61, 61.64 | 2.1% |
| conv 26x26x8/2, 8 ch downstream / rust | 14.43 (14.22-14.97) | 14.27, 14.26, 14.33, 14.73, 14.45, 14.72 | 3.2% |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 26.23 (25.71-26.66) | 26.36, 25.92, 26.33, 26.38, 26.25, 26 | 1.8% |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 5.878 (5.698-5.992) | 5.858, 5.848, 5.837, 5.969, 5.817, 5.82 | 2.6% |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 1226 (1187-1242) | 1234, 1206, 1223, 1225, 1228, 1235 | 2.3% |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 746.8 (744.1-760.9) | 752.5, 745.6, 745.3, 749.2, 751.7, 747.7 | 1.0% |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 1.729e+04 (1.71e+04-1.748e+04) | 1.726e+04, 1.725e+04, 1.724e+04, 1.723e+04, 1.739e+04, 1.736e+04 | 0.9% |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 2.207e+04 (2.174e+04-2.249e+04) | 2.207e+04, 2.225e+04, 2.212e+04, 2.209e+04, 2.188e+04, 2.21e+04 | 1.7% |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 1214 (1156-1263) | 1255, 1190, 1164, 1222, 1161, 1245 | 7.7% |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 430 (419.3-436.9) | 421.4, 426.6, 430.6, 433.2, 431.7, 435.3 | 3.2% |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 4.273e+04 (4.165e+04-4.357e+04) | 4.279e+04, 4.282e+04, 4.282e+04, 4.259e+04, 4.223e+04, 4.261e+04 | 1.4% |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 2323 (2309-2339) | 2322, 2330, 2324, 2321, 2314, 2333 | 0.8% |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 704 (689.2-718.9) | 696.5, 696.4, 701, 709.1, 712.2, 703.6 | 2.2% |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 204.4 (200.3-208.3) | 208.2, 200.6, 202.3, 206.3, 204.5, 206.2 | 3.7% |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 1.218e+04 (1.191e+04-1.273e+04) | 1.2e+04, 1.218e+04, 1.214e+04, 1.207e+04, 1.239e+04, 1.252e+04 | 4.3% |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 3021 (2966-3096) | 3046, 3007, 3003, 3071, 2978, 3032 | 3.1% |
| conv 26x26x8, 8 ch forward / numpy | 125.5 (123.7-129.5) | 125.1, 124.1, 124.5, 126, 127, 128.9 | 3.8% |
| conv 26x26x8, 8 ch forward / rust | 92.18 (91.51-93.74) | 91.98, 92.07, 92.13, 92.62, 92.33, 92.95 | 1.1% |
| conv 26x26x8, 8 ch downstream / numpy | 148.8 (144.7-157.3) | 155.5, 150, 145.6, 147.9, 150.3, 152.6 | 6.6% |
| conv 26x26x8, 8 ch downstream / rust | 56.71 (54.69-63.48) | 55.39, 55.19, 56.01, 61.58, 57.9, 57.28 | 11.3% |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 89.14 (86.8-91.06) | 87.86, 88.98, 88.65, 89.67, 90.77, 89.55 | 3.3% |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 25.61 (25-25.92) | 25.27, 25.42, 25.14, 25.78, 25.46, 25.89 | 2.9% |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 4205 (4096-4328) | 4243, 4097, 4149, 4245, 4274, 4246 | 4.2% |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 3037 (3027-3053) | 3036, 3035, 3044, 3035, 3040, 3043 | 0.3% |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 6.761e+04 (6.7e+04-6.773e+04) | 6.754e+04, 6.734e+04, 6.734e+04, 6.743e+04, 6.761e+04, 6.747e+04 | 0.4% |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 8.381e+04 (8.247e+04-8.437e+04) | 8.383e+04, 8.39e+04, 8.381e+04, 8.378e+04, 8.399e+04, 8.338e+04 | 0.7% |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 4755 (4607-4977) | 4796, 4705, 4692, 4861, 4667, 4895 | 4.8% |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 390.7 (380.7-409.8) | 387, 398, 393.6, 393.9, 397.4, 383.3 | 3.8% |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 1.133e+05 (1.122e+05-1.152e+05) | 1.139e+05, 1.134e+05, 1.137e+05, 1.135e+05, 1.137e+05, 1.124e+05 | 1.3% |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 5002 (4915-5124) | 4979, 5063, 4995, 5044, 5019, 5020 | 1.7% |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 3037 (2951-3106) | 2961, 3024, 3043, 3000, 3059, 3059 | 3.2% |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 660.9 (643.9-677.4) | 645.3, 674.6, 656.1, 659, 659.4, 665.8 | 4.4% |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 5.092e+04 (5.026e+04-5.218e+04) | 5.052e+04, 5.059e+04, 5.055e+04, 5.126e+04, 5.169e+04, 5.155e+04 | 2.3% |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 1.19e+04 (1.146e+04-1.197e+04) | 1.191e+04, 1.187e+04, 1.193e+04, 1.175e+04, 1.175e+04, 1.167e+04 | 2.2% |
| pool 26x26, 8 ch forward / numpy | 70.64 (69.09-73.26) | 71.3, 71.79, 69.47, 69.47, 69.74, 72.21 | 3.9% |
| pool 26x26, 8 ch forward / rust | 3.733 (3.69-3.82) | 3.709, 3.743, 3.726, 3.745, 3.767, 3.807 | 2.6% |
| pool 26x26, 8 ch downstream / numpy | 34.91 (33.49-36.11) | 34.86, 34.83, 34.4, 34.6, 34.26, 35.68 | 4.1% |
| pool 26x26, 8 ch downstream / rust | 4.091 (4.039-4.237) | 4.154, 4.041, 4.14, 4.068, 4.127, 4.122 | 2.8% |
| pool 26x26, 8 ch forward_batch b32 / numpy | 1225 (1219-1240) | 1224, 1223, 1220, 1225, 1223, 1233 | 1.0% |
| pool 26x26, 8 ch forward_batch b32 / rust | 111.4 (110.3-113.9) | 111.6, 110.9, 111.6, 111.7, 111.4, 112.2 | 1.2% |
| pool 26x26, 8 ch forward_batch b512 / numpy | 2.016e+04 (1.999e+04-2.035e+04) | 2.009e+04, 2.009e+04, 2.01e+04, 2.02e+04, 2.027e+04, 2.018e+04 | 0.9% |
| pool 26x26, 8 ch forward_batch b512 / rust | 2430 (2416-2457) | 2429, 2430, 2432, 2437, 2429, 2427 | 0.4% |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 532.5 (514.1-543.8) | 532.8, 535, 529, 527.2, 529.6, 533.7 | 1.5% |
| pool 26x26, 8 ch downstream_batch b32 / rust | 129.6 (128.3-132.5) | 129.9, 128.7, 129.4, 129.2, 131.2, 131.2 | 1.9% |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 1.416e+04 (1.402e+04-1.43e+04) | 1.417e+04, 1.416e+04, 1.416e+04, 1.424e+04, 1.423e+04, 1.406e+04 | 1.3% |
| pool 26x26, 8 ch downstream_batch b512 / rust | 2611 (2587-2621) | 2604, 2605, 2614, 2603, 2611, 2597 | 0.6% |
| pool 6x6, 8 ch forward / numpy | 33.94 (33.03-34.67) | 34.11, 33.88, 34.11, 33.82, 34.34, 33.35 | 2.9% |
| pool 6x6, 8 ch forward / rust | 0.4989 (0.485-0.5267) | 0.4851, 0.4909, 0.4991, 0.5119, 0.5023, 0.5065 | 5.4% |
| pool 6x6, 8 ch downstream / numpy | 18.32 (18.04-19.48) | 18.9, 18.29, 18.22, 18.31, 18.25, 18.75 | 3.7% |
| pool 6x6, 8 ch downstream / rust | 0.4593 (0.4489-0.4822) | 0.4629, 0.4535, 0.4526, 0.4792, 0.4642, 0.4623 | 5.8% |
| pool 6x6, 8 ch forward_batch b32 / numpy | 109.3 (108.6-110.7) | 110.7, 108.8, 109.3, 109.2, 109.4, 109.3 | 1.7% |
| pool 6x6, 8 ch forward_batch b32 / rust | 8.259 (8.162-8.334) | 8.172, 8.259, 8.258, 8.25, 8.245, 8.308 | 1.7% |
| pool 6x6, 8 ch forward_batch b512 / numpy | 1210 (1207-1233) | 1211, 1208, 1208, 1209, 1228, 1210 | 1.7% |
| pool 6x6, 8 ch forward_batch b512 / rust | 128.9 (127.7-131.7) | 128.7, 128.3, 128.5, 128.8, 130.4, 130.8 | 1.9% |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 59.38 (58.48-60.75) | 59.77, 58.96, 58.65, 59.42, 59.84, 59.66 | 2.0% |
| pool 6x6, 8 ch downstream_batch b32 / rust | 7.443 (7.336-7.601) | 7.385, 7.394, 7.508, 7.43, 7.443, 7.549 | 2.2% |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 627.1 (593.2-638.2) | 614.7, 627.5, 622.9, 633, 628.5, 630 | 2.9% |
| pool 6x6, 8 ch downstream_batch b512 / rust | 120.8 (119.5-122.9) | 120.6, 120.7, 120.7, 121.8, 120.7, 121.7 | 0.9% |
| conv tail 32 x 5408 bare downstream b32 / numpy | 66.66 (65.54-75.72) | 66.15, 66.48, 65.86, 66.99, 73.98, 71.53 | 12.2% |
| conv tail 32 x 5408 bare downstream b32 / rust | 243.8 (237.7-254.2) | 237.9, 241.9, 246.2, 248, 247.8, 243.1 | 4.2% |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3186 (3160-3215) | 3175, 3181, 3204, 3172, 3187, 3197 | 1.0% |
| conv tail 32 x 5408 bare downstream b512 / rust | 2257 (2248-2394) | 2287, 2251, 2283, 2269, 2324, 2250 | 3.3% |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 78.86 (78.24-79.88) | 78.53, 78.66, 79.48, 78.84, 79.19, 79.13 | 1.2% |
| conv tail 32 x 5408 bare accumulate b32 / rust | 232.3 (226.1-237.6) | 227.7, 231.5, 232.1, 232.3, 233.2, 235.2 | 3.2% |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 1630 (1590-1679) | 1613, 1620, 1645, 1624, 1660, 1651 | 2.8% |
| conv tail 32 x 5408 bare accumulate b512 / rust | 2173 (2025-2418) | 2119, 2245, 2198, 2156, 2146, 2202 | 5.8% |
| conv tail 32 x 5408 transpose b32 / numpy | 0.7133 (0.7002-0.731) | 0.7047, 0.7043, 0.7063, 0.7233, 0.7179, 0.7206 | 2.7% |
| conv tail 32 x 5408 transpose b32 / rust | 0.8552 (0.839-0.8689) | 0.846, 0.8588, 0.851, 0.8579, 0.8622, 0.8602 | 1.9% |
| conv tail 32 x 5408 transpose b512 / numpy | 11.46 (10.57-16.26) | 12.2, 11.48, 11.49, 10.62, 11.38, 14.48 | 33.6% |
| conv tail 32 x 5408 transpose b512 / rust | 14.75 (14.44-15.66) | 15.47, 15.26, 14.6, 14.56, 14.89, 14.45 | 6.9% |
| conv tail 32 x 5408 add b32 / numpy | 80.85 (77.42-84.02) | 82.48, 80.96, 80.92, 80.11, 78.02, 79.42 | 5.5% |
| conv tail 32 x 5408 add b32 / rust | 66.08 (63.1-69.39) | 69.35, 64.62, 66.3, 66.27, 64.58, 66.28 | 7.2% |
| conv tail 32 x 5408 add b512 / numpy | 80.78 (77.57-84.18) | 82.47, 80.81, 80.67, 82.46, 80.93, 79.08 | 4.2% |
| conv tail 32 x 5408 add b512 / rust | 65.61 (62.32-69.72) | 68.73, 66.05, 65.59, 65.54, 62.42, 65.62 | 9.6% |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 1.434 (1.392-1.612) | 1.412, 1.433, 1.402, 1.463, 1.511, 1.473 | 7.6% |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.4427 (0.4264-0.4498) | 0.4284, 0.4457, 0.4481, 0.4414, 0.442, 0.4444 | 4.5% |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 10 (9.876-10.39) | 9.914, 10.05, 10.03, 10.1, 9.985, 10.19 | 2.8% |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 5.099 (4.972-5.207) | 4.997, 5.046, 5.14, 5.087, 5.167, 5.185 | 3.7% |
| dense 30 x 784 bare downstream b32 / numpy | 23.84 (23.51-24.21) | 23.9, 24.13, 24.01, 23.67, 23.79, 23.56 | 2.4% |
| dense 30 x 784 bare downstream b32 / rust | 32.79 (32.2-33.87) | 32.42, 32.89, 32.32, 33.26, 33.27, 33.34 | 3.1% |
| dense 30 x 784 bare downstream b512 / numpy | 138.6 (111.6-146.2) | 125.3, 136.6, 140.5, 137.1, 138.9, 142.4 | 12.3% |
| dense 30 x 784 bare downstream b512 / rust | 244.4 (235.9-248) | 239.7, 244.1, 246.7, 244.4, 243.7, 242.3 | 2.9% |
| dense 30 x 784 bare accumulate b32 / numpy | 29.19 (28.67-29.92) | 29.81, 29.01, 29, 29.05, 29.26, 29.32 | 2.8% |
| dense 30 x 784 bare accumulate b32 / rust | 30.48 (29.62-31.44) | 29.64, 30.2, 30.7, 30.83, 30.13, 31.01 | 4.5% |
| dense 30 x 784 bare accumulate b512 / numpy | 191.8 (189.8-194.9) | 190.6, 193, 193.2, 192.1, 194.1, 191.7 | 1.8% |
| dense 30 x 784 bare accumulate b512 / rust | 281.8 (254.4-293.3) | 279.8, 280.9, 280.3, 279.5, 283.7, 273.9 | 3.5% |
| dense 30 x 784 transpose b32 / numpy | 0.6958 (0.677-0.7276) | 0.6817, 0.6894, 0.6864, 0.7012, 0.6974, 0.7116 | 4.3% |
| dense 30 x 784 transpose b32 / rust | 0.8296 (0.8101-0.8339) | 0.8106, 0.8239, 0.8335, 0.8303, 0.8279, 0.8303 | 2.8% |
| dense 30 x 784 transpose b512 / numpy | 7.232 (7.188-7.29) | 7.277, 7.248, 7.21, 7.239, 7.25, 7.212 | 0.9% |
| dense 30 x 784 transpose b512 / rust | 13.5 (12.9-14.16) | 13.7, 13.67, 13.35, 13.38, 13.13, 13.86 | 5.4% |
| dense 30 x 784 add b32 / numpy | 11.15 (10.44-11.72) | 11.43, 11.11, 11.28, 11.12, 10.81, 11.38 | 5.6% |
| dense 30 x 784 add b32 / rust | 8.948 (8.666-9.432) | 9.254, 8.749, 9.027, 9.098, 8.783, 9.228 | 5.6% |
| dense 30 x 784 add b512 / numpy | 11.36 (10.73-12.03) | 11.81, 11.55, 11.75, 11.34, 10.99, 11.11 | 7.2% |
| dense 30 x 784 add b512 / rust | 8.907 (8.316-9.552) | 9.176, 8.766, 8.745, 8.934, 8.608, 9.213 | 6.8% |
| dense 30 x 784 sum_axis0 b32 / numpy | 1.463 (1.404-1.498) | 1.472, 1.438, 1.41, 1.454, 1.47, 1.483 | 5.0% |
| dense 30 x 784 sum_axis0 b32 / rust | 0.4016 (0.3926-0.4145) | 0.394, 0.4052, 0.4026, 0.4009, 0.4014, 0.4076 | 3.4% |
| dense 30 x 784 sum_axis0 b512 / numpy | 10.85 (10.63-10.95) | 10.9, 10.67, 10.78, 10.65, 10.92, 10.87 | 2.5% |
| dense 30 x 784 sum_axis0 b512 / rust | 4.452 (4.302-4.569) | 4.348, 4.438, 4.471, 4.437, 4.489, 4.525 | 4.0% |
| dense 10 x 30 bare downstream b32 / numpy | 1.765 (1.704-1.823) | 1.739, 1.768, 1.751, 1.782, 1.78, 1.765 | 2.4% |
| dense 10 x 30 bare downstream b32 / rust | 1.123 (1.1-1.171) | 1.108, 1.125, 1.123, 1.122, 1.123, 1.153 | 4.0% |
| dense 10 x 30 bare downstream b512 / numpy | 12.23 (12.08-12.51) | 12.22, 12.09, 12.26, 12.15, 12.42, 12.42 | 2.7% |
| dense 10 x 30 bare downstream b512 / rust | 15.36 (14.95-16.02) | 15.01, 15.35, 15.51, 15.39, 15.3, 15.86 | 5.5% |
| dense 10 x 30 bare accumulate b32 / numpy | 1.798 (1.742-1.829) | 1.794, 1.768, 1.815, 1.818, 1.777, 1.796 | 2.7% |
| dense 10 x 30 bare accumulate b32 / rust | 1.204 (1.197-1.225) | 1.199, 1.206, 1.202, 1.208, 1.207, 1.217 | 1.5% |
| dense 10 x 30 bare accumulate b512 / numpy | 13.46 (13.3-13.77) | 13.62, 13.34, 13.33, 13.51, 13.44, 13.63 | 2.2% |
| dense 10 x 30 bare accumulate b512 / rust | 25.48 (25.15-29.19) | 27.82, 25.39, 25.71, 25.36, 25.53, 25.36 | 9.7% |
| dense 10 x 30 transpose b32 / numpy | 0.4439 (0.4328-0.4564) | 0.433, 0.4416, 0.4493, 0.4432, 0.4475, 0.4475 | 3.7% |
| dense 10 x 30 transpose b32 / rust | 0.3807 (0.3725-0.3931) | 0.3827, 0.3756, 0.3746, 0.3867, 0.3823, 0.3854 | 3.2% |
| dense 10 x 30 transpose b512 / numpy | 2.948 (2.881-3.033) | 2.998, 2.934, 2.931, 2.947, 2.997, 2.94 | 2.3% |
| dense 10 x 30 transpose b512 / rust | 3.895 (3.793-3.951) | 3.817, 3.851, 3.85, 3.929, 3.928, 3.922 | 2.9% |
| dense 10 x 30 add b32 / numpy | 0.4066 (0.3976-0.415) | 0.3997, 0.401, 0.4096, 0.4039, 0.4087, 0.4123 | 3.1% |
| dense 10 x 30 add b32 / rust | 0.1893 (0.1843-0.1947) | 0.1877, 0.1907, 0.1898, 0.1894, 0.1882, 0.1907 | 1.6% |
| dense 10 x 30 add b512 / numpy | 0.4161 (0.4061-0.4265) | 0.4074, 0.4099, 0.4152, 0.4185, 0.4215, 0.4251 | 4.3% |
| dense 10 x 30 add b512 / rust | 0.2004 (0.195-0.2151) | 0.1952, 0.1984, 0.212, 0.2003, 0.2002, 0.2076 | 8.4% |
| dense 10 x 30 sum_axis0 b32 / numpy | 1.309 (1.287-1.364) | 1.332, 1.306, 1.294, 1.309, 1.318, 1.338 | 3.4% |
| dense 10 x 30 sum_axis0 b32 / rust | 0.3206 (0.3115-0.3368) | 0.3146, 0.3181, 0.3276, 0.3293, 0.3216, 0.3211 | 4.6% |
| dense 10 x 30 sum_axis0 b512 / numpy | 8.985 (8.903-9.305) | 8.949, 8.985, 9.043, 8.943, 9.2, 9.211 | 3.0% |
| dense 10 x 30 sum_axis0 b512 / rust | 3.255 (3.201-3.302) | 3.21, 3.226, 3.223, 3.29, 3.291, 3.266 | 2.5% |
| attention 16 x 32 forward_batch b32 / numpy | 290.7 (286-294) | 293.2, 288.4, 289.3, 289.2, 289.7, 288.9 | 1.7% |
| attention 16 x 32 forward_batch b32 / rust | 404.1 (399.1-411.1) | 403.2, 404.5, 403.1, 407.2, 404.7, 406.3 | 1.0% |
| attention 16 x 32 forward_batch b512 / numpy | 4911 (4660-4969) | 4669, 4920, 4917, 4932, 4929, 4912 | 5.4% |
| attention 16 x 32 forward_batch b512 / rust | 6361 (6261-6591) | 6361, 6316, 6492, 6290, 6343, 6473 | 3.2% |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 263.7 (259.9-272.2) | 270.6, 263.6, 259.9, 262.4, 263.6, 265.8 | 4.1% |
| attention 16 x 32 hidden_delta_batch b32 / rust | 244.2 (240.9-251.7) | 243.4, 241.9, 242.7, 247.7, 250, 248.9 | 3.3% |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 4495 (4372-4539) | 4431, 4483, 4486, 4507, 4514, 4505 | 1.9% |
| attention 16 x 32 hidden_delta_batch b512 / rust | 4630 (4493-4804) | 4670, 4574, 4669, 4624, 4692, 4583 | 2.5% |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 247.9 (236.7-262) | 251.9, 246.3, 247.5, 251.4, 248.9, 243.4 | 3.5% |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 212.3 (199.3-231.8) | 218.2, 214.9, 205.7, 213.9, 205.3, 219.8 | 6.8% |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5551 (5469-5679) | 5577, 5526, 5565, 5670, 5579, 5513 | 2.8% |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 3989 (3928-4009) | 3988, 3999, 3972, 4002, 3976, 3940 | 1.6% |

### the crate over numpy

| case | crate µs | numpy µs | crate / numpy |
|---|---|---|---|
| conv tail 32 x 5408 bare downstream b32 (per call) | 243.8 | 66.66 | 3.66 |
| conv tail 32 x 5408 downstream_batch b32 (per call) | 245.1 | 79.11 | 3.10 |
| conv tail 32 x 5408 bare accumulate b32 (per call) | 232.3 | 78.86 | 2.95 |
| conv tail 32 x 5408 forward_batch b32 (per call) | 390.9 | 149 | 2.62 |
| dense 10 x 30 bare accumulate b512 (per call) | 25.48 | 13.46 | 1.89 |
| dense 30 x 784 transpose b512 (per call) | 13.5 | 7.232 | 1.87 |
| dense 30 x 784 downstream_batch b512 (per call) | 242.9 | 131.5 | 1.85 |
| conv tail 32 x 5408 accumulate_gradient_batch b32 (per call) | 291.2 | 163.6 | 1.78 |
| dense 30 x 784 bare downstream b512 (per call) | 244.4 | 138.6 | 1.76 |
| conv tail 32 x 5408 forward_batch b512 (per call) | 1829 | 1167 | 1.57 |
| dense 30 x 784 bare accumulate b512 (per call) | 281.8 | 191.8 | 1.47 |
| dense 30 x 784 forward_batch b512 (per call) | 379.1 | 267.1 | 1.42 |
| attention 16 x 32 forward_batch b32 (per call) | 404.1 | 290.7 | 1.39 |
| dense 30 x 784 accumulate_gradient_batch b512 (per call) | 308.2 | 222.8 | 1.38 |
| dense 30 x 784 bare downstream b32 (per call) | 32.79 | 23.84 | 1.38 |
| dense 10 x 30 accumulate_gradient_batch b512 (per call) | 33.12 | 24.81 | 1.34 |
| conv tail 32 x 5408 bare accumulate b512 (per call) | 2173 | 1630 | 1.33 |
| dense 10 x 30 transpose b512 (per call) | 3.895 | 2.948 | 1.32 |
| dense 10 x 30 downstream_batch b512 (per call) | 15.78 | 12.02 | 1.31 |
| attention 16 x 32 forward_batch b512 (per call) | 6361 | 4911 | 1.30 |
| conv tail 32 x 5408 transpose b512 (per call) | 14.75 | 11.46 | 1.29 |
| conv 26x26x8/2, 8 ch forward_batch b512 (per call) | 2.207e+04 | 1.729e+04 | 1.28 |
| dense 30 x 784 downstream_batch b32 (per call) | 29.65 | 23.36 | 1.27 |
| conv 13x13x8, 8 ch forward_batch b512 (per call) | 1.799e+04 | 1.418e+04 | 1.27 |
| conv tail 32 x 5408 accumulate_gradient_batch b512 (per call) | 2332 | 1842 | 1.27 |
| dense 30 x 784 forward_batch b32 (per call) | 48 | 38.04 | 1.26 |
| dense 10 x 30 bare downstream b512 (per call) | 15.36 | 12.23 | 1.26 |
| conv 26x26x8, 8 ch forward_batch b512 (per call) | 8.381e+04 | 6.761e+04 | 1.24 |
| conv tail 32 x 5408 transpose b32 (per call) | 0.8552 | 0.7133 | 1.20 |
| dense 30 x 784 transpose b32 (per call) | 0.8296 | 0.6958 | 1.19 |
| dense 10 x 30 forward_batch b512 (per call) | 62.02 | 53.99 | 1.15 |
| dense 30 x 784 bare accumulate b32 (per call) | 30.48 | 29.19 | 1.04 |
| attention 16 x 32 hidden_delta_batch b512 (per call) | 4630 | 4495 | 1.03 |
| dense 30 x 784 accumulate_gradient_batch b32 (per call) | 40.44 | 39.8 | 1.02 |
| attention 16 x 32 hidden_delta_batch b32 (per call) | 244.2 | 263.7 | 0.93 |
| conv tail 32 x 5408 downstream (per call) | 21.59 | 24.89 | 0.87 |
| dense 10 x 30 transpose b32 (per call) | 0.3807 | 0.4439 | 0.86 |
| attention 16 x 32 accumulate_gradient_batch b32 (per call) | 212.3 | 247.9 | 0.86 |
| conv 28x28, 8 ch downstream_batch b32 (per call) | 500.3 | 596.1 | 0.84 |
| conv tail 32 x 5408 add b32 (per call) | 66.08 | 80.85 | 0.82 |
| conv tail 32 x 5408 add b512 (per call) | 65.61 | 80.78 | 0.81 |
| dense 30 x 784 add b32 (per call) | 8.948 | 11.15 | 0.80 |
| dense 30 x 784 downstream (per call) | 2.857 | 3.57 | 0.80 |
| dense 30 x 784 add b512 (per call) | 8.907 | 11.36 | 0.78 |
| conv tail 32 x 5408 hidden_delta (per call) | 24.32 | 32.69 | 0.74 |
| conv 26x26x8, 8 ch forward (per call) | 92.18 | 125.5 | 0.73 |
| conv tail 32 x 5408 forward (per call) | 20.81 | 28.38 | 0.73 |
| conv tail 32 x 5408 downstream_batch b512 (per call) | 2254 | 3114 | 0.72 |
| conv 26x26x8, 8 ch forward_batch b32 (per call) | 3037 | 4205 | 0.72 |
| attention 16 x 32 accumulate_gradient_batch b512 (per call) | 3989 | 5551 | 0.72 |
| conv tail 32 x 5408 bare downstream b512 (per call) | 2257 | 3186 | 0.71 |
| dense 30 x 784 hidden_delta_batch b32 (per call) | 40.12 | 58.75 | 0.68 |
| dense 10 x 30 bare accumulate b32 (per call) | 1.204 | 1.798 | 0.67 |
| dense 10 x 30 downstream_batch b32 (per call) | 1.182 | 1.775 | 0.67 |
| dense 10 x 30 hidden_delta_batch b512 (per call) | 22.24 | 33.92 | 0.66 |
| dense 10 x 30 bare downstream b32 (per call) | 1.123 | 1.765 | 0.64 |
| conv tail 32 x 5408 accumulate_gradient (per call) | 53.99 | 85.45 | 0.63 |
| conv 8x8, 8 ch downstream_batch b512 (per call) | 438.9 | 694.9 | 0.63 |
| conv 13x13x8, 8 ch forward_batch b32 (per call) | 615.1 | 1002 | 0.61 |
| conv 26x26x8/2, 8 ch forward_batch b32 (per call) | 746.8 | 1226 | 0.61 |
| conv tail 32 x 5408 apply_accumulated_gradient (per call) | 109.1 | 181.1 | 0.60 |
| conv 28x28, 8 ch forward_batch b32 (per call) | 557.4 | 960.9 | 0.58 |
| conv 28x28, 8 ch accumulate_gradient_batch b512 (per call) | 1.16e+04 | 2.011e+04 | 0.58 |
| dense 30 x 784 apply_accumulated_gradient (per call) | 17.18 | 31.38 | 0.55 |
| conv 8x8, 8 ch forward_batch b512 (per call) | 481.6 | 884.6 | 0.54 |
| dense 30 x 784 hidden_delta (per call) | 3.44 | 6.464 | 0.53 |
| dense 10 x 30 apply_accumulated_gradient (per call) | 2.277 | 4.444 | 0.51 |
| conv tail 32 x 5408 sum_axis0 b512 (per call) | 5.099 | 10 | 0.51 |
| conv tail 32 x 5408 hidden_delta_batch b32 (per call) | 312 | 613.9 | 0.51 |
| conv 28x28, 8 ch forward_batch b512 (per call) | 9253 | 1.833e+04 | 0.50 |
| dense 10 x 30 add b512 (per call) | 0.2004 | 0.4161 | 0.48 |
| conv tail 32 x 5408 hidden_delta_batch b512 (per call) | 5674 | 1.214e+04 | 0.47 |
| dense 10 x 30 add b32 (per call) | 0.1893 | 0.4066 | 0.47 |
| conv 28x28, 8 ch accumulate_gradient (per call) | 16.04 | 35.39 | 0.45 |
| conv 28x28, 8 ch downstream (per call) | 17.32 | 38.23 | 0.45 |
| conv 26x26x8/2, 8 ch forward (per call) | 23.85 | 53.55 | 0.45 |
| dense 10 x 30 accumulate_gradient_batch b32 (per call) | 1.982 | 4.462 | 0.44 |
| dense 10 x 30 forward_batch b32 (per call) | 4.238 | 9.667 | 0.44 |
| conv 8x8, 8 ch downstream_batch b32 (per call) | 27.85 | 64.35 | 0.43 |
| conv 8x8, 8 ch forward_batch b32 (per call) | 31.17 | 74.68 | 0.42 |
| dense 30 x 784 sum_axis0 b512 (per call) | 4.452 | 10.85 | 0.41 |
| conv 28x28, 8 ch accumulate_gradient_batch b32 (per call) | 533.2 | 1304 | 0.41 |
| conv 13x13x8, 8 ch forward (per call) | 20.06 | 50.6 | 0.40 |
| conv 26x26x8, 8 ch downstream (per call) | 56.71 | 148.8 | 0.38 |
| conv 13x13x8, 8 ch downstream_batch b32 (per call) | 348.9 | 917.6 | 0.38 |
| dense 10 x 30 sum_axis0 b512 (per call) | 3.255 | 8.985 | 0.36 |
| dense 10 x 30 hidden_delta_batch b32 (per call) | 1.703 | 4.704 | 0.36 |
| conv 26x26x8/2, 8 ch downstream_batch b32 (per call) | 430 | 1214 | 0.35 |
| conv 28x28, 8 ch forward (per call) | 19.02 | 54.85 | 0.35 |
| conv 8x8, 8 ch accumulate_gradient_batch b512 (per call) | 461.2 | 1466 | 0.31 |
| conv tail 32 x 5408 sum_axis0 b32 (per call) | 0.4427 | 1.434 | 0.31 |
| dense 30 x 784 hidden_delta_batch b512 (per call) | 501.9 | 1696 | 0.30 |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 (per call) | 204.4 | 704 | 0.29 |
| conv 8x8, 8 ch accumulate_gradient_batch b32 (per call) | 28.24 | 97.37 | 0.29 |
| conv 26x26x8, 8 ch accumulate_gradient (per call) | 25.61 | 89.14 | 0.29 |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 (per call) | 169 | 596.3 | 0.28 |
| dense 30 x 784 forward (per call) | 2.382 | 8.634 | 0.28 |
| dense 30 x 784 sum_axis0 b32 (per call) | 0.4016 | 1.463 | 0.27 |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 (per call) | 2579 | 1.031e+04 | 0.25 |
| dense 10 x 30 downstream (per call) | 0.2062 | 0.8263 | 0.25 |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 (per call) | 3021 | 1.218e+04 | 0.25 |
| dense 30 x 784 accumulate_gradient (per call) | 6.999 | 28.28 | 0.25 |
| dense 10 x 30 sum_axis0 b32 (per call) | 0.3206 | 1.309 | 0.24 |
| pool 26x26, 8 ch downstream_batch b32 (per call) | 129.6 | 532.5 | 0.24 |
| conv 13x13x8, 8 ch downstream (per call) | 12.26 | 50.91 | 0.24 |
| conv 26x26x8/2, 8 ch downstream (per call) | 14.43 | 60.92 | 0.24 |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 (per call) | 1.19e+04 | 5.092e+04 | 0.23 |
| conv 26x26x8/2, 8 ch accumulate_gradient (per call) | 5.878 | 26.23 | 0.22 |
| conv tail 32 x 5408 sgd step (per call) | 58.97 | 270.4 | 0.22 |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 (per call) | 660.9 | 3037 | 0.22 |
| conv 13x13x8, 8 ch accumulate_gradient (per call) | 4.982 | 23 | 0.22 |
| dense 10 x 30 hidden_delta (per call) | 0.4424 | 2.209 | 0.20 |
| pool 6x6, 8 ch downstream_batch b512 (per call) | 120.8 | 627.1 | 0.19 |
| pool 26x26, 8 ch downstream_batch b512 (per call) | 2611 | 1.416e+04 | 0.18 |
| conv 8x8, 8 ch accumulate_gradient (per call) | 1.173 | 7.229 | 0.16 |
| dense 10 x 30 accumulate_gradient (per call) | 0.4321 | 2.737 | 0.16 |
| pool 6x6, 8 ch downstream_batch b32 (per call) | 7.443 | 59.38 | 0.13 |
| dense 30 x 784 sgd step (per call) | 7.508 | 60.11 | 0.12 |
| pool 26x26, 8 ch forward_batch b512 (per call) | 2430 | 2.016e+04 | 0.12 |
| pool 26x26, 8 ch downstream (per call) | 4.091 | 34.91 | 0.12 |
| pool 6x6, 8 ch forward_batch b512 (per call) | 128.9 | 1210 | 0.11 |
| pool 26x26, 8 ch forward_batch b32 (per call) | 111.4 | 1225 | 0.09 |
| conv 28x28, 8 ch downstream_batch b512 (per call) | 1420 | 1.616e+04 | 0.09 |
| conv 26x26x8, 8 ch downstream_batch b32 (per call) | 390.7 | 4755 | 0.08 |
| dense 10 x 30 forward (per call) | 0.3494 | 4.429 | 0.08 |
| pool 6x6, 8 ch forward_batch b32 (per call) | 8.259 | 109.3 | 0.08 |
| conv 8x8, 8 ch downstream (per call) | 1.201 | 21.1 | 0.06 |
| dense 10 x 30 sgd step (per call) | 0.4645 | 8.186 | 0.06 |
| conv 26x26x8/2, 8 ch downstream_batch b512 (per call) | 2323 | 4.273e+04 | 0.05 |
| pool 26x26, 8 ch forward (per call) | 3.733 | 70.64 | 0.05 |
| conv 8x8, 8 ch forward (per call) | 1.511 | 28.81 | 0.05 |
| conv 26x26x8, 8 ch downstream_batch b512 (per call) | 5002 | 1.133e+05 | 0.04 |
| conv 13x13x8, 8 ch downstream_batch b512 (per call) | 1052 | 2.578e+04 | 0.04 |
| pool 6x6, 8 ch downstream (per call) | 0.4593 | 18.32 | 0.03 |
| pool 6x6, 8 ch forward (per call) | 0.4989 | 33.94 | 0.01 |
