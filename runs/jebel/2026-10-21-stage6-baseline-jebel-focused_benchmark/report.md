Old `69bf104` against new `69bf104`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `5d47987e03dd`) on both sides. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.08; busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / conv 28x28, 8 ch downstream_batch b32 / numpy -5.6% (615.3 -> 580.7 µs)
- consistent: per call / dense 10 x 30 forward / rust +3.1% (0.3456 -> 0.3564 µs)
- consistent, small: per call / dense 10 x 30 accumulate_gradient_batch b512 / rust -1.8% (33.48 -> 32.86 µs)
- 267 rows within noise (31 separated inside their spread), max |Δ| 9.1%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 28.5 (27.53-29.94) | 28.36 (27.26-28.47) | -0.5% | 28.58, 28.02, 29.21 / 28.36, 27.89, 27.83 | within noise |
| conv tail 32 x 5408 forward / rust | 20.84 (19.31-22.54) | 20.22 (18.84-22.72) | -3.0% | 20.84, 20.93, 20.18 / 19.11, 20.93, 21.14 | within noise |
| conv tail 32 x 5408 downstream / numpy | 25.56 (24.84-26.2) | 24.81 (24.06-24.97) | -3.0% | 26.15, 24.86, 25.59 / 24.83, 24.52, 24.47 | separated, inside spread |
| conv tail 32 x 5408 downstream / rust | 21.52 (20.59-24) | 22.33 (20.63-23.95) | +3.8% | 21.28, 22.42, 21.54 / 22.14, 22.58, 22.12 | within noise |
| conv tail 32 x 5408 hidden_delta / numpy | 32.64 (32.52-34.19) | 32.69 (31.32-32.74) | +0.1% | 32.54, 33.46, 33.33 / 32.04, 32.71, 32.03 | within noise |
| conv tail 32 x 5408 hidden_delta / rust | 24.87 (22.95-26.33) | 23.73 (22.87-24.99) | -4.6% | 23.81, 26.2, 24.23 / 23.51, 24.15, 23.74 | within noise |
| conv tail 32 x 5408 accumulate_gradient / numpy | 86.64 (83.2-90.03) | 85.45 (82.88-88.01) | -1.4% | 87.63, 85.62, 85.94 / 84.26, 86.65, 84.39 | within noise |
| conv tail 32 x 5408 accumulate_gradient / rust | 54.81 (51.99-56.81) | 53.35 (52.4-56.58) | -2.7% | 53.16, 56.06, 54.47 / 52.75, 55, 54.43 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 182.8 (177-189.6) | 180.8 (177-184.3) | -1.1% | 182.8, 185.3, 181 / 180.8, 182.4, 180.6 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 110.8 (107.5-113.4) | 108.5 (107-111.7) | -2.1% | 109.3, 110.5, 111.4 / 108, 109.3, 109.1 | within noise |
| conv tail 32 x 5408 sgd step / numpy | 271 (269.5-276.8) | 269.7 (265-277.4) | -0.5% | 269.9, 273.5, 273.6 / 269.7, 270.6, 271.2 | within noise |
| conv tail 32 x 5408 sgd step / rust | 59 (58.78-62.97) | 58.68 (57.84-59.69) | -0.5% | 59, 59.56, 60.92 / 58.02, 58.68, 59.5 | within noise |
| conv tail 32 x 5408 forward_batch b32 / numpy | 148.8 (148-160.2) | 150.2 (146.7-158.8) | +1.0% | 148.2, 148.7, 155.8 / 147.8, 150.4, 155.1 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 392.8 (378.6-415.8) | 390.9 (373-412.2) | -0.5% | 392.8, 394.2, 397.2 / 378.7, 401, 392.1 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1168 (1051-1175) | 1166 (1165-1171) | -0.1% | 1109, 1172, 1167 / 1165, 1167, 1169 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1829 (1666-1852) | 1843 (1679-1927) | +0.7% | 1707, 1840, 1831 / 1714, 1892, 1856 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 79.04 (78.2-79.93) | 79.11 (78.53-79.52) | +0.1% | 78.24, 79.32, 79.52 / 78.8, 79.27, 79.15 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 245.4 (238.3-249.9) | 242.6 (238.5-249.7) | -1.1% | 241.8, 245.2, 249.7 / 243.5, 244.1, 242.6 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3113 (3095-3127) | 3116 (3077-3240) | +0.1% | 3098, 3118, 3120 / 3086, 3116, 3191 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2261 (2252-2273) | 2253 (2251-2259) | -0.3% | 2272, 2254, 2260 / 2252, 2259, 2252 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 613.9 (601.7-618.2) | 615.7 (601.9-643.6) | +0.3% | 612.5, 607.4, 616.5 / 611, 620.1, 627.5 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 309.4 (302.6-323.4) | 312.8 (302-316.7) | +1.1% | 306, 313.2, 313.8 / 307.6, 313.6, 314.2 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 1.214e+04 (1.203e+04-1.224e+04) | 1.217e+04 (1.211e+04-1.244e+04) | +0.3% | 1.208e+04, 1.217e+04, 1.215e+04 / 1.217e+04, 1.212e+04, 1.232e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 5684 (5672-5714) | 5655 (5606-5676) | -0.5% | 5679, 5696, 5698 / 5655, 5615, 5674 | separated, inside spread |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 163.3 (159.8-167.9) | 163.7 (162.1-165.2) | +0.2% | 161.5, 164.2, 165.7 / 163.1, 164.8, 162.9 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 291.2 (284.7-297.6) | 291.6 (283.8-298.1) | +0.2% | 290.6, 287.8, 294.6 / 288.7, 291, 291.6 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 1823 (1757-1916) | 1855 (1817-1877) | +1.7% | 1789, 1870, 1851 / 1836, 1844, 1866 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 2351 (2239-2391) | 2321 (2294-2344) | -1.2% | 2297, 2322, 2356 / 2304, 2336, 2318 | within noise |
| dense 30 x 784 forward / numpy | 8.592 (8.472-8.719) | 8.708 (8.249-8.951) | +1.3% | 8.592, 8.602, 8.595 / 8.877, 8.56, 8.454 | within noise |
| dense 30 x 784 forward / rust | 2.457 (2.23-2.585) | 2.356 (2.278-2.659) | -4.1% | 2.346, 2.432, 2.519 / 2.322, 2.523, 2.329 | within noise |
| dense 30 x 784 downstream / numpy | 3.532 (3.212-3.765) | 3.601 (3.278-3.691) | +1.9% | 3.32, 3.568, 3.658 / 3.484, 3.557, 3.628 | within noise |
| dense 30 x 784 downstream / rust | 2.855 (2.822-2.931) | 2.861 (2.817-2.901) | +0.2% | 2.827, 2.873, 2.892 / 2.822, 2.884, 2.863 | within noise |
| dense 30 x 784 hidden_delta / numpy | 6.451 (6.338-6.631) | 6.464 (6.208-7.218) | +0.2% | 6.422, 6.484, 6.506 / 6.351, 6.592, 6.713 | within noise |
| dense 30 x 784 hidden_delta / rust | 3.426 (3.367-3.576) | 3.445 (3.377-3.543) | +0.6% | 3.493, 3.448, 3.389 / 3.415, 3.491, 3.414 | within noise |
| dense 30 x 784 accumulate_gradient / numpy | 28.02 (26.92-28.88) | 28.52 (27.75-29.02) | +1.8% | 28.32, 28.02, 27.83 / 28.33, 28.39, 28.52 | separated, inside spread |
| dense 30 x 784 accumulate_gradient / rust | 7.092 (6.843-7.264) | 6.919 (6.7-7.207) | -2.4% | 7.115, 7.043, 7.054 / 6.915, 6.812, 7.082 | within noise |
| dense 30 x 784 apply_accumulated_gradient / numpy | 31.73 (30.77-32.5) | 30.89 (30.77-32.37) | -2.7% | 31.81, 31.61, 31.73 / 31.23, 30.88, 31.59 | separated, inside spread |
| dense 30 x 784 apply_accumulated_gradient / rust | 17.19 (16.63-17.25) | 17.13 (16.5-17.47) | -0.3% | 17.03, 17.24, 16.94 / 17.1, 17.16, 16.98 | within noise |
| dense 30 x 784 sgd step / numpy | 60.92 (59.67-61.85) | 59.24 (58.07-61.22) | -2.8% | 61.4, 60.46, 60.46 / 59.36, 59.03, 59.64 | separated, inside spread |
| dense 30 x 784 sgd step / rust | 7.477 (7.306-7.779) | 7.525 (7.43-7.767) | +0.6% | 7.388, 7.632, 7.569 / 7.595, 7.508, 7.599 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 37.85 (37.74-38.59) | 38.12 (37.93-38.67) | +0.7% | 38.17, 37.98, 37.84 / 38.37, 38.1, 38.1 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 48.57 (46.45-49.08) | 47.99 (47.18-48.64) | -1.2% | 47.03, 48.94, 48.57 / 47.91, 47.93, 48 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 267.5 (223.6-268.7) | 266.3 (264.2-268.3) | -0.4% | 244.8, 267.8, 268.1 / 264.8, 265.8, 268.2 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 378.3 (366.5-386.3) | 380.1 (375.1-389.8) | +0.5% | 371.6, 378.3, 383.5 / 376.4, 380.8, 385.1 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 23.35 (22.98-23.5) | 23.38 (23.17-23.86) | +0.1% | 23.26, 23.42, 23.18 / 23.21, 23.41, 23.61 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 29.65 (28.45-30.27) | 29.57 (28.69-30.31) | -0.3% | 29.05, 29.96, 29.46 / 29.08, 29.99, 29.5 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 131.6 (128.9-132.7) | 131.5 (130.2-132.6) | -0.0% | 129.7, 131.9, 132.1 / 131.4, 131.2, 131.6 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 244.2 (238.2-247.6) | 242.2 (240.6-243.9) | -0.8% | 240.5, 244.3, 246.1 / 243.4, 241.3, 241.6 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 59.5 (57.26-60.23) | 58.18 (57.27-59.07) | -2.2% | 58.62, 59.62, 59.06 / 58.97, 57.59, 57.95 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / rust | 40.53 (38.49-41.14) | 40.12 (39.07-42.15) | -1.0% | 39.26, 41.09, 40.41 / 40.55, 40.61, 39.67 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 1700 (1610-1748) | 1684 (1648-1746) | -1.0% | 1655, 1724, 1703 / 1650, 1717, 1690 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / rust | 502.1 (485.8-507.5) | 501.9 (484.5-514.1) | -0.0% | 505.3, 499.4, 493.4 / 501.9, 500.9, 499.3 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 39.89 (39.3-41.18) | 39.62 (38.94-41.13) | -0.7% | 40.56, 40.04, 39.52 / 40.37, 39.55, 39.8 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 40.41 (39.19-41.54) | 40.44 (39.84-40.59) | +0.1% | 39.67, 41.52, 40.1 / 40.44, 40.58, 39.94 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 222.3 (213.6-223.6) | 223.1 (220.1-226.4) | +0.4% | 215.8, 223.3, 222.5 / 222, 224.3, 223.1 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 308.6 (306.3-316.9) | 307.9 (295.2-322.5) | -0.2% | 308.1, 316.3, 306.8 / 301, 315.8, 309.2 | within noise |
| dense 10 x 30 forward / numpy | 4.437 (4.345-4.814) | 4.39 (4.351-4.441) | -1.0% | 4.404, 4.619, 4.437 / 4.394, 4.39, 4.401 | separated, inside spread |
| dense 10 x 30 forward / rust | 0.3456 (0.3414-0.3503) | 0.3564 (0.3442-0.3667) | +3.1% | 0.3456, 0.345, 0.346 / 0.3554, 0.3542, 0.3583 | consistent |
| dense 10 x 30 downstream / numpy | 0.8367 (0.7986-0.9204) | 0.825 (0.8001-0.8784) | -1.4% | 0.8246, 0.8695, 0.8385 / 0.854, 0.8043, 0.8299 | within noise |
| dense 10 x 30 downstream / rust | 0.2042 (0.2003-0.2153) | 0.2121 (0.2024-0.2432) | +3.9% | 0.2078, 0.2062, 0.2034 / 0.2131, 0.2228, 0.2097 | separated, inside spread |
| dense 10 x 30 hidden_delta / numpy | 2.2 (2.165-2.267) | 2.212 (2.172-2.357) | +0.6% | 2.201, 2.18, 2.239 / 2.288, 2.185, 2.232 | within noise |
| dense 10 x 30 hidden_delta / rust | 0.4424 (0.4359-0.4501) | 0.4432 (0.4401-0.4814) | +0.2% | 0.4382, 0.4471, 0.4446 / 0.4504, 0.4429, 0.4609 | within noise |
| dense 10 x 30 accumulate_gradient / numpy | 2.741 (2.648-2.783) | 2.726 (2.659-2.806) | -0.6% | 2.705, 2.716, 2.778 / 2.677, 2.724, 2.793 | within noise |
| dense 10 x 30 accumulate_gradient / rust | 0.4281 (0.4221-0.4398) | 0.4362 (0.4207-0.4408) | +1.9% | 0.4236, 0.433, 0.4321 / 0.4376, 0.4298, 0.4335 | within noise |
| dense 10 x 30 apply_accumulated_gradient / numpy | 4.455 (4.392-4.561) | 4.404 (4.354-4.523) | -1.1% | 4.499, 4.453, 4.477 / 4.443, 4.381, 4.435 | separated, inside spread |
| dense 10 x 30 apply_accumulated_gradient / rust | 2.277 (2.229-2.404) | 2.281 (2.248-2.32) | +0.2% | 2.236, 2.325, 2.336 / 2.249, 2.294, 2.295 | within noise |
| dense 10 x 30 sgd step / numpy | 8.186 (7.899-8.237) | 8.169 (8.02-8.444) | -0.2% | 8.143, 8.198, 8.068 / 8.334, 8.106, 8.156 | within noise |
| dense 10 x 30 sgd step / rust | 0.4645 (0.4472-0.5134) | 0.4656 (0.4502-0.511) | +0.2% | 0.4552, 0.4627, 0.5007 / 0.4806, 0.4631, 0.4663 | within noise |
| dense 10 x 30 forward_batch b32 / numpy | 9.763 (9.551-10.02) | 9.667 (9.54-9.867) | -1.0% | 9.721, 10.01, 9.598 / 9.667, 9.841, 9.546 | within noise |
| dense 10 x 30 forward_batch b32 / rust | 4.257 (4.184-4.319) | 4.229 (4.184-4.357) | -0.7% | 4.217, 4.259, 4.291 / 4.203, 4.238, 4.292 | within noise |
| dense 10 x 30 forward_batch b512 / numpy | 54.52 (53.3-55.22) | 53.67 (53.45-54.37) | -1.6% | 53.96, 54.82, 54.63 / 53.49, 53.67, 54.14 | within noise |
| dense 10 x 30 forward_batch b512 / rust | 61.96 (61.33-63.28) | 62.02 (61.28-62.85) | +0.1% | 61.4, 62.12, 62.84 / 61.96, 61.92, 62.27 | within noise |
| dense 10 x 30 downstream_batch b32 / numpy | 1.78 (1.722-1.84) | 1.769 (1.712-1.781) | -0.6% | 1.753, 1.755, 1.822 / 1.751, 1.743, 1.772 | within noise |
| dense 10 x 30 downstream_batch b32 / rust | 1.173 (1.155-1.241) | 1.185 (1.149-1.207) | +1.0% | 1.157, 1.176, 1.21 / 1.167, 1.196, 1.183 | within noise |
| dense 10 x 30 downstream_batch b512 / numpy | 12.13 (11.88-12.31) | 11.96 (11.77-12.07) | -1.4% | 12.06, 12.24, 12.01 / 11.9, 11.99, 11.94 | separated, inside spread |
| dense 10 x 30 downstream_batch b512 / rust | 15.85 (15.37-16.22) | 15.74 (15.59-15.93) | -0.7% | 15.44, 15.85, 16.18 / 15.66, 15.73, 15.9 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 4.71 (4.642-4.736) | 4.59 (4.533-4.812) | -2.5% | 4.677, 4.719, 4.722 / 4.663, 4.699, 4.563 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 1.721 (1.647-1.768) | 1.688 (1.644-1.722) | -1.9% | 1.677, 1.717, 1.759 / 1.663, 1.7, 1.702 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 34.29 (33.1-34.79) | 33.63 (32.97-37.78) | -1.9% | 34.37, 34.65, 33.49 / 36.33, 33.63, 33.05 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / rust | 22.18 (21.45-22.85) | 22.3 (21.8-22.39) | +0.6% | 21.82, 22.49, 22.51 / 22.22, 22.1, 22.3 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 4.479 (4.364-4.645) | 4.462 (4.38-4.647) | -0.4% | 4.479, 4.614, 4.39 / 4.618, 4.406, 4.462 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 1.982 (1.959-2.088) | 1.984 (1.956-2.008) | +0.1% | 1.961, 2.036, 2.003 / 1.984, 1.972, 1.991 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 24.96 (24.63-25.14) | 24.72 (24.57-24.93) | -1.0% | 24.93, 24.89, 24.98 / 24.84, 24.63, 24.69 | separated, inside spread |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 33.48 (33.15-34.32) | 32.86 (32.65-33.09) | -1.8% | 33.39, 33.83, 33.47 / 32.87, 32.9, 32.79 | consistent, small |
| conv 28x28, 8 ch forward / numpy | 55.14 (54.07-55.68) | 54.32 (53.79-57.75) | -1.5% | 55.17, 55.27, 54.66 / 55.77, 54.69, 54.32 | within noise |
| conv 28x28, 8 ch forward / rust | 19.04 (18.5-23.07) | 19.02 (18.85-19.39) | -0.1% | 18.69, 21.14, 19.19 / 19.05, 18.93, 19.2 | within noise |
| conv 28x28, 8 ch downstream / numpy | 38.7 (37.61-40.04) | 38.01 (37.28-38.65) | -1.8% | 39.03, 39.63, 37.69 / 38.09, 38.08, 37.78 | within noise |
| conv 28x28, 8 ch downstream / rust | 17.47 (16.77-17.9) | 17.19 (17.13-17.4) | -1.6% | 17.03, 17.56, 17.66 / 17.15, 17.17, 17.38 | within noise |
| conv 28x28, 8 ch accumulate_gradient / numpy | 35.52 (35.02-35.86) | 35.3 (34.69-35.71) | -0.6% | 35.09, 35.64, 35.72 / 35.16, 35.2, 35.53 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 16.1 (15.95-16.19) | 16.04 (16.02-16.11) | -0.4% | 16.18, 16.02, 16.05 / 16.07, 16.07, 16.03 | within noise |
| conv 28x28, 8 ch forward_batch b32 / numpy | 971.7 (953.3-974.7) | 951.8 (949.2-961.7) | -2.0% | 969, 973.4, 962.2 / 955.3, 957.4, 949.6 | separated, inside spread |
| conv 28x28, 8 ch forward_batch b32 / rust | 557.9 (541-572.7) | 557.3 (552.6-570.2) | -0.1% | 541.1, 557.9, 569.2 / 557.4, 557.3, 562.2 | within noise |
| conv 28x28, 8 ch forward_batch b512 / numpy | 1.841e+04 (1.813e+04-1.858e+04) | 1.824e+04 (1.812e+04-1.849e+04) | -0.9% | 1.842e+04, 1.836e+04, 1.841e+04 / 1.83e+04, 1.823e+04, 1.824e+04 | separated, inside spread |
| conv 28x28, 8 ch forward_batch b512 / rust | 9315 (9242-9481) | 9193 (9001-9377) | -1.3% | 9372, 9253, 9391 / 9042, 9207, 9295 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 615.3 (595.2-620.8) | 580.7 (577.3-597) | -5.6% | 615.4, 616.7, 605.3 / 587.5, 578, 587.5 | consistent |
| conv 28x28, 8 ch downstream_batch b32 / rust | 497 (480.5-503.7) | 502.5 (490.6-505.4) | +1.1% | 484.1, 502.4, 497 / 492, 504.8, 502.5 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 1.628e+04 (1.596e+04-1.645e+04) | 1.604e+04 (1.59e+04-1.631e+04) | -1.5% | 1.64e+04, 1.607e+04, 1.628e+04 / 1.611e+04, 1.604e+04, 1.607e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / rust | 1421 (1376-1427) | 1419 (1402-1430) | -0.2% | 1400, 1425, 1416 / 1419, 1422, 1416 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 1304 (1280-1332) | 1302 (1292-1318) | -0.1% | 1281, 1305, 1318 / 1295, 1315, 1302 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 534.9 (528.1-541.9) | 530.4 (528.2-535.1) | -0.8% | 531.5, 538.4, 531.5 / 531.5, 530.4, 531.7 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 2.014e+04 (1.941e+04-2.033e+04) | 2.005e+04 (1.991e+04-2.028e+04) | -0.4% | 1.954e+04, 2.024e+04, 2.016e+04 / 1.992e+04, 2.007e+04, 2.019e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 1.161e+04 (1.154e+04-1.163e+04) | 1.157e+04 (1.153e+04-1.16e+04) | -0.3% | 1.162e+04, 1.158e+04, 1.163e+04 / 1.155e+04, 1.159e+04, 1.156e+04 | within noise |
| conv 8x8, 8 ch forward / numpy | 28.81 (27.64-30.11) | 28.73 (27.97-29.4) | -0.3% | 28.81, 28.86, 28.87 / 28.51, 28.76, 28.73 | separated, inside spread |
| conv 8x8, 8 ch forward / rust | 1.522 (1.481-1.537) | 1.502 (1.475-1.582) | -1.3% | 1.483, 1.533, 1.526 / 1.488, 1.491, 1.552 | within noise |
| conv 8x8, 8 ch downstream / numpy | 21.14 (20.87-21.66) | 21.09 (20.8-21.84) | -0.2% | 21.14, 21.31, 21.09 / 21.05, 20.91, 21.59 | within noise |
| conv 8x8, 8 ch downstream / rust | 1.203 (1.164-1.302) | 1.191 (1.172-1.24) | -1.0% | 1.233, 1.219, 1.201 / 1.181, 1.215, 1.206 | within noise |
| conv 8x8, 8 ch accumulate_gradient / numpy | 7.204 (7.143-7.484) | 7.266 (6.989-7.4) | +0.9% | 7.333, 7.296, 7.147 / 7.18, 7.11, 7.362 | within noise |
| conv 8x8, 8 ch accumulate_gradient / rust | 1.172 (1.168-1.213) | 1.18 (1.165-1.226) | +0.7% | 1.171, 1.193, 1.17 / 1.195, 1.171, 1.192 | within noise |
| conv 8x8, 8 ch forward_batch b32 / numpy | 74.7 (73.54-76.22) | 74.09 (73.48-76.28) | -0.8% | 75.46, 74.69, 74.19 / 75.22, 74.58, 73.64 | within noise |
| conv 8x8, 8 ch forward_batch b32 / rust | 31.42 (30.22-31.92) | 31.17 (30.75-34.53) | -0.8% | 30.55, 31.82, 31.49 / 30.9, 31.17, 33.16 | within noise |
| conv 8x8, 8 ch forward_batch b512 / numpy | 886.7 (877.3-901.9) | 878.2 (874.2-897.6) | -1.0% | 882.7, 900.2, 884.6 / 886.9, 881.9, 876.3 | within noise |
| conv 8x8, 8 ch forward_batch b512 / rust | 483.4 (469.5-496.8) | 481.6 (480.1-498.6) | -0.4% | 472.3, 495.6, 483.4 / 481.1, 481.6, 489.9 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 64.26 (63.42-66) | 64.35 (63.33-67.4) | +0.1% | 63.96, 64.4, 65.01 / 65.87, 64.13, 65.2 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / rust | 27.99 (26.99-29.47) | 27.76 (27.47-30.17) | -0.8% | 27, 28.96, 27.99 / 28.82, 27.7, 27.96 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 700.9 (682.3-724.5) | 694.9 (684.2-719.8) | -0.9% | 696.5, 723.1, 687.3 / 700.2, 693.9, 702 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / rust | 439 (425.5-440.3) | 438.9 (427.4-443.8) | -0.0% | 425.6, 440, 439 / 433, 436.4, 441.5 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 97.99 (96.11-99.39) | 96.94 (96.32-98.18) | -1.1% | 96.47, 99.01, 98.33 / 96.32, 96.94, 97.98 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 28.31 (28.2-28.48) | 28.21 (28.17-28.25) | -0.4% | 28.29, 28.32, 28.36 / 28.19, 28.24, 28.2 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 1475 (1440-1492) | 1459 (1396-1525) | -1.1% | 1450, 1483, 1482 / 1493, 1419, 1465 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 462.2 (458.6-464.2) | 458.3 (457.6-463.7) | -0.8% | 461.4, 461.8, 462.7 / 460.7, 458.1, 460.9 | separated, inside spread |
| conv 13x13x8, 8 ch forward / numpy | 50.59 (50.03-51.77) | 50.6 (49.27-51.7) | +0.0% | 50.94, 51.27, 50.21 / 51, 50.6, 50.08 | within noise |
| conv 13x13x8, 8 ch forward / rust | 20.02 (19.91-20.44) | 20.09 (19.91-20.53) | +0.4% | 20, 20.12, 20.17 / 19.99, 20.15, 20.25 | within noise |
| conv 13x13x8, 8 ch downstream / numpy | 51.82 (49.55-52.15) | 50.51 (49.82-52.01) | -2.5% | 51.67, 51.82, 50.85 / 50.22, 50.49, 51.24 | within noise |
| conv 13x13x8, 8 ch downstream / rust | 12.25 (11.89-12.49) | 12.3 (12.04-12.4) | +0.4% | 11.92, 12.39, 12.25 / 12.19, 12.22, 12.32 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 23 (22.8-23.33) | 23 (22.64-23.6) | -0.0% | 22.96, 23.27, 22.85 / 22.78, 23.3, 23.07 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 5.04 (4.962-5.134) | 4.963 (4.926-5.169) | -1.5% | 5.048, 5.042, 5.03 / 4.931, 4.973, 5.072 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 1005 (991.2-1022) | 997.1 (983.6-1023) | -0.8% | 998.1, 1013, 1007 / 991.8, 995.8, 1010 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 616.1 (614.8-630.7) | 615.1 (614.1-615.8) | -0.2% | 616.1, 622.3, 622.8 / 614.5, 615.3, 615.5 | separated, inside spread |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 1.418e+04 (1.405e+04-1.436e+04) | 1.414e+04 (1.406e+04-1.436e+04) | -0.3% | 1.416e+04, 1.421e+04, 1.423e+04 / 1.407e+04, 1.421e+04, 1.424e+04 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 1.799e+04 (1.782e+04-1.814e+04) | 1.799e+04 (1.779e+04-1.828e+04) | +0.0% | 1.801e+04, 1.791e+04, 1.804e+04 / 1.81e+04, 1.799e+04, 1.797e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 920.7 (863.4-937.2) | 883.2 (853.7-932.1) | -4.1% | 917.6, 930.1, 895.4 / 887, 869.4, 908.4 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 348.3 (335.7-359.2) | 348.9 (338.7-353.1) | +0.2% | 338.6, 356.5, 348.3 / 340.9, 348.9, 352.3 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 2.568e+04 (2.554e+04-2.603e+04) | 2.583e+04 (2.541e+04-2.6e+04) | +0.6% | 2.573e+04, 2.564e+04, 2.58e+04 / 2.564e+04, 2.583e+04, 2.59e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 1050 (1037-1063) | 1052 (1044-1089) | +0.2% | 1045, 1050, 1054 / 1050, 1071, 1057 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 601.5 (581.8-613) | 595 (592.1-600.8) | -1.1% | 584.2, 602.1, 607.4 / 594.1, 594.9, 597.3 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 171.9 (167.9-173.6) | 167.2 (166.8-173.1) | -2.7% | 171.9, 170.7, 171.9 / 170, 167.5, 166.9 | separated, inside spread |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.025e+04 (1.004e+04-1.035e+04) | 1.036e+04 (1.015e+04-1.044e+04) | +1.1% | 1.013e+04, 1.025e+04, 1.034e+04 / 1.015e+04, 1.039e+04, 1.039e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 2550 (2524-2598) | 2596 (2507-2606) | +1.8% | 2528, 2594, 2547 / 2603, 2550, 2569 | within noise |
| conv 26x26x8/2, 8 ch forward / numpy | 53.86 (52.95-55.4) | 53.48 (53.22-53.89) | -0.7% | 54.24, 54.04, 53.4 / 53.44, 53.56, 53.48 | within noise |
| conv 26x26x8/2, 8 ch forward / rust | 23.9 (23.67-24.09) | 23.8 (23.72-24.73) | -0.4% | 23.87, 23.99, 23.79 / 23.77, 23.77, 24.35 | within noise |
| conv 26x26x8/2, 8 ch downstream / numpy | 61.04 (59.98-62.17) | 60.87 (59.08-62.99) | -0.3% | 60.35, 61.55, 61.64 / 61.03, 60.68, 61 | within noise |
| conv 26x26x8/2, 8 ch downstream / rust | 14.58 (14.22-14.97) | 14.33 (14.22-14.5) | -1.7% | 14.27, 14.73, 14.72 / 14.26, 14.33, 14.45 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 26.27 (25.71-26.66) | 26.2 (25.77-26.46) | -0.3% | 26.36, 26.38, 26 / 25.92, 26.33, 26.25 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 5.92 (5.725-5.992) | 5.848 (5.698-5.936) | -1.2% | 5.858, 5.969, 5.82 / 5.848, 5.837, 5.817 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 1230 (1223-1240) | 1223 (1187-1242) | -0.6% | 1234, 1225, 1235 / 1206, 1223, 1228 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 748.2 (744.1-760.9) | 745.3 (744.6-758.5) | -0.4% | 752.5, 749.2, 747.7 / 745.6, 745.3, 751.7 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 1.727e+04 (1.71e+04-1.748e+04) | 1.732e+04 (1.713e+04-1.741e+04) | +0.3% | 1.726e+04, 1.723e+04, 1.736e+04 / 1.725e+04, 1.724e+04, 1.739e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 2.207e+04 (2.199e+04-2.221e+04) | 2.206e+04 (2.174e+04-2.249e+04) | -0.0% | 2.207e+04, 2.209e+04, 2.21e+04 / 2.225e+04, 2.212e+04, 2.188e+04 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 1238 (1220-1263) | 1167 (1156-1209) | -5.7% | 1255, 1222, 1245 / 1190, 1164, 1161 | separated, inside spread |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 432.3 (419.3-436.9) | 428.6 (426.2-435) | -0.8% | 421.4, 433.2, 435.3 / 426.6, 430.6, 431.7 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 4.273e+04 (4.165e+04-4.357e+04) | 4.263e+04 (4.22e+04-4.318e+04) | -0.2% | 4.279e+04, 4.259e+04, 4.261e+04 / 4.282e+04, 4.282e+04, 4.223e+04 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 2325 (2309-2339) | 2321 (2312-2338) | -0.2% | 2322, 2321, 2333 / 2330, 2324, 2314 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 703.6 (696.5-712) | 704 (689.2-718.9) | +0.1% | 696.5, 709.1, 703.6 / 696.4, 701, 712.2 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 208 (204.4-208.3) | 200.7 (200.3-208.3) | -3.5% | 208.2, 206.3, 206.2 / 200.6, 202.3, 204.5 | separated, inside spread |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 1.212e+04 (1.191e+04-1.273e+04) | 1.221e+04 (1.208e+04-1.252e+04) | +0.7% | 1.2e+04, 1.207e+04, 1.252e+04 / 1.218e+04, 1.214e+04, 1.239e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 3058 (2995-3096) | 2981 (2966-3040) | -2.5% | 3046, 3071, 3032 / 3007, 3003, 2978 | separated, inside spread |
| conv 26x26x8, 8 ch forward / numpy | 127.2 (123.7-129.5) | 124.5 (123.7-127.3) | -2.1% | 125.1, 126, 128.9 / 124.1, 124.5, 127 | within noise |
| conv 26x26x8, 8 ch forward / rust | 92.25 (91.89-93.74) | 92.07 (91.51-93.15) | -0.2% | 91.98, 92.62, 92.95 / 92.07, 92.13, 92.33 | within noise |
| conv 26x26x8, 8 ch downstream / numpy | 152.2 (146.2-157.3) | 146.4 (144.7-154.9) | -3.8% | 155.5, 147.9, 152.6 / 150, 145.6, 150.3 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 57.28 (54.69-63.48) | 56.01 (55.04-58.39) | -2.2% | 55.39, 61.58, 57.28 / 55.19, 56.01, 57.9 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 89.15 (86.8-90.17) | 89 (88.45-91.06) | -0.2% | 87.86, 89.67, 89.55 / 88.98, 88.65, 90.77 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 25.78 (25.09-25.92) | 25.19 (25-25.83) | -2.3% | 25.27, 25.78, 25.89 / 25.42, 25.14, 25.46 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 4243 (4161-4328) | 4149 (4096-4321) | -2.2% | 4243, 4245, 4246 / 4097, 4149, 4274 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 3036 (3031-3053) | 3040 (3027-3052) | +0.1% | 3036, 3035, 3043 / 3035, 3044, 3040 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 6.754e+04 (6.712e+04-6.773e+04) | 6.761e+04 (6.7e+04-6.769e+04) | +0.1% | 6.754e+04, 6.743e+04, 6.747e+04 / 6.734e+04, 6.734e+04, 6.761e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 8.378e+04 (8.247e+04-8.437e+04) | 8.381e+04 (8.347e+04-8.433e+04) | +0.0% | 8.383e+04, 8.378e+04, 8.338e+04 / 8.39e+04, 8.381e+04, 8.399e+04 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 4881 (4705-4977) | 4667 (4607-4804) | -4.4% | 4796, 4861, 4895 / 4705, 4692, 4667 | separated, inside spread |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 385.5 (380.7-402.6) | 395.8 (386.2-409.8) | +2.7% | 387, 393.9, 383.3 / 398, 393.6, 397.4 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 1.132e+05 (1.124e+05-1.144e+05) | 1.134e+05 (1.122e+05-1.152e+05) | +0.2% | 1.139e+05, 1.135e+05, 1.124e+05 / 1.134e+05, 1.137e+05, 1.137e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 4997 (4915-5124) | 5019 (4992-5070) | +0.4% | 4979, 5044, 5020 / 5063, 4995, 5019 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 3007 (2951-3070) | 3040 (2998-3106) | +1.1% | 2961, 3000, 3059 / 3024, 3043, 3059 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 652.7 (644.1-676.9) | 670.1 (643.9-677.4) | +2.7% | 645.3, 659, 665.8 / 674.6, 656.1, 659.4 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 5.105e+04 (5.05e+04-5.218e+04) | 5.077e+04 (5.026e+04-5.18e+04) | -0.5% | 5.052e+04, 5.126e+04, 5.155e+04 / 5.059e+04, 5.055e+04, 5.169e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 1.188e+04 (1.146e+04-1.191e+04) | 1.193e+04 (1.155e+04-1.197e+04) | +0.4% | 1.191e+04, 1.175e+04, 1.167e+04 / 1.187e+04, 1.193e+04, 1.175e+04 | within noise |
| pool 26x26, 8 ch forward / numpy | 71.03 (69.42-73.26) | 69.97 (69.09-72.13) | -1.5% | 71.3, 69.47, 72.21 / 71.79, 69.47, 69.74 | within noise |
| pool 26x26, 8 ch forward / rust | 3.745 (3.69-3.815) | 3.728 (3.715-3.82) | -0.5% | 3.709, 3.745, 3.807 / 3.743, 3.726, 3.767 | within noise |
| pool 26x26, 8 ch downstream / numpy | 35 (34.15-36.11) | 34.83 (33.49-35.16) | -0.5% | 34.86, 34.6, 35.68 / 34.83, 34.4, 34.26 | within noise |
| pool 26x26, 8 ch downstream / rust | 4.122 (4.064-4.173) | 4.046 (4.039-4.237) | -1.8% | 4.154, 4.068, 4.122 / 4.041, 4.14, 4.127 | within noise |
| pool 26x26, 8 ch forward_batch b32 / numpy | 1225 (1222-1240) | 1222 (1219-1226) | -0.3% | 1224, 1225, 1233 / 1223, 1220, 1223 | separated, inside spread |
| pool 26x26, 8 ch forward_batch b32 / rust | 111.6 (110.4-113.9) | 111.3 (110.3-112.5) | -0.3% | 111.6, 111.7, 112.2 / 110.9, 111.6, 111.4 | separated, inside spread |
| pool 26x26, 8 ch forward_batch b512 / numpy | 2.016e+04 (2.001e+04-2.027e+04) | 2.016e+04 (1.999e+04-2.035e+04) | +0.0% | 2.009e+04, 2.02e+04, 2.018e+04 / 2.009e+04, 2.01e+04, 2.027e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 2429 (2416-2457) | 2430 (2418-2447) | +0.0% | 2429, 2437, 2427 / 2430, 2432, 2429 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 532.8 (514.1-540.5) | 532.5 (515.3-543.8) | -0.0% | 532.8, 527.2, 533.7 / 535, 529, 529.6 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / rust | 129.9 (129.2-132.5) | 129.4 (128.3-132.4) | -0.4% | 129.9, 129.2, 131.2 / 128.7, 129.4, 131.2 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 1.416e+04 (1.402e+04-1.425e+04) | 1.416e+04 (1.409e+04-1.43e+04) | +0.0% | 1.417e+04, 1.424e+04, 1.406e+04 / 1.416e+04, 1.416e+04, 1.423e+04 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / rust | 2597 (2587-2621) | 2613 (2597-2615) | +0.6% | 2604, 2603, 2597 / 2605, 2614, 2611 | separated, inside spread |
| pool 6x6, 8 ch forward / numpy | 33.71 (33.03-34.63) | 34.11 (33.39-34.67) | +1.2% | 34.11, 33.82, 33.35 / 33.88, 34.11, 34.34 | within noise |
| pool 6x6, 8 ch forward / rust | 0.5013 (0.485-0.5267) | 0.4969 (0.4887-0.5075) | -0.9% | 0.4851, 0.5119, 0.5065 / 0.4909, 0.4991, 0.5023 | within noise |
| pool 6x6, 8 ch downstream / numpy | 18.39 (18.3-19.48) | 18.22 (18.04-18.45) | -0.9% | 18.9, 18.31, 18.75 / 18.29, 18.22, 18.25 | separated, inside spread |
| pool 6x6, 8 ch downstream / rust | 0.4718 (0.4489-0.4822) | 0.4559 (0.4499-0.4672) | -3.4% | 0.4629, 0.4792, 0.4623 / 0.4535, 0.4526, 0.4642 | within noise |
| pool 6x6, 8 ch forward_batch b32 / numpy | 109.6 (108.6-110.7) | 109 (108.6-109.7) | -0.5% | 110.7, 109.2, 109.3 / 108.8, 109.3, 109.4 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 8.234 (8.162-8.334) | 8.259 (8.197-8.293) | +0.3% | 8.172, 8.25, 8.308 / 8.259, 8.258, 8.245 | within noise |
| pool 6x6, 8 ch forward_batch b512 / numpy | 1210 (1208-1212) | 1209 (1207-1233) | -0.2% | 1211, 1209, 1210 / 1208, 1208, 1228 | within noise |
| pool 6x6, 8 ch forward_batch b512 / rust | 128.9 (128.5-131.5) | 128.7 (127.7-131.7) | -0.1% | 128.7, 128.8, 130.8 / 128.3, 128.5, 130.4 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 59.63 (59.17-59.96) | 58.94 (58.48-60.75) | -1.2% | 59.77, 59.42, 59.66 / 58.96, 58.65, 59.84 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / rust | 7.43 (7.379-7.601) | 7.451 (7.336-7.567) | +0.3% | 7.385, 7.43, 7.549 / 7.394, 7.508, 7.443 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 633 (593.2-638.2) | 623.3 (622.8-634.1) | -1.5% | 614.7, 633, 630 / 627.5, 622.9, 628.5 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 120.9 (120.3-122.9) | 120.7 (119.5-121.9) | -0.2% | 120.6, 121.8, 121.7 / 120.7, 120.7, 120.7 | within noise |
| conv tail 32 x 5408 bare downstream b32 / numpy | 66.99 (66.15-75.25) | 66.48 (65.54-75.72) | -0.8% | 66.15, 66.99, 71.53 / 66.48, 65.86, 73.98 | within noise |
| conv tail 32 x 5408 bare downstream b32 / rust | 242.8 (237.7-252.5) | 245.1 (239.7-254.2) | +0.9% | 237.9, 248, 243.1 / 241.9, 246.2, 247.8 | within noise |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3182 (3160-3208) | 3191 (3168-3215) | +0.3% | 3175, 3172, 3197 / 3181, 3204, 3187 | within noise |
| conv tail 32 x 5408 bare downstream b512 / rust | 2262 (2248-2309) | 2254 (2248-2394) | -0.4% | 2287, 2269, 2250 / 2251, 2283, 2324 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 78.85 (78.24-79.4) | 78.95 (78.59-79.88) | +0.1% | 78.53, 78.84, 79.13 / 78.66, 79.48, 79.19 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / rust | 232.3 (226.1-237.2) | 232.1 (227.8-237.6) | -0.0% | 227.7, 232.3, 235.2 / 231.5, 232.1, 233.2 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 1625 (1595-1679) | 1648 (1590-1676) | +1.4% | 1613, 1624, 1651 / 1620, 1645, 1660 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / rust | 2183 (2025-2222) | 2159 (2072-2418) | -1.1% | 2119, 2156, 2202 / 2245, 2198, 2146 | within noise |
| conv tail 32 x 5408 transpose b32 / numpy | 0.7163 (0.702-0.731) | 0.7097 (0.7002-0.7216) | -0.9% | 0.7047, 0.7233, 0.7206 / 0.7043, 0.7063, 0.7179 | within noise |
| conv tail 32 x 5408 transpose b32 / rust | 0.8546 (0.8408-0.8655) | 0.8592 (0.839-0.8689) | +0.5% | 0.846, 0.8579, 0.8602 / 0.8588, 0.851, 0.8622 | within noise |
| conv tail 32 x 5408 transpose b512 / numpy | 12.03 (10.57-16.26) | 11.46 (11.14-11.85) | -4.7% | 12.2, 10.62, 14.48 / 11.48, 11.49, 11.38 | within noise |
| conv tail 32 x 5408 transpose b512 / rust | 14.56 (14.44-15.54) | 14.85 (14.57-15.66) | +2.0% | 15.47, 14.56, 14.45 / 15.26, 14.6, 14.89 | within noise |
| conv tail 32 x 5408 add b32 / numpy | 80.92 (77.42-83.95) | 79.51 (77.88-84.02) | -1.7% | 82.48, 80.11, 79.42 / 80.96, 80.92, 78.02 | within noise |
| conv tail 32 x 5408 add b32 / rust | 69.33 (63.18-69.39) | 64.64 (63.1-69.39) | -6.8% | 69.35, 66.27, 66.28 / 64.62, 66.3, 64.58 | within noise |
| conv tail 32 x 5408 add b512 / numpy | 80.81 (77.57-84.15) | 80.72 (77.67-84.18) | -0.1% | 82.47, 82.46, 79.08 / 80.81, 80.67, 80.93 | within noise |
| conv tail 32 x 5408 add b512 / rust | 68.72 (62.37-68.8) | 62.49 (62.32-69.72) | -9.1% | 68.73, 65.54, 65.62 / 66.05, 65.59, 62.42 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 1.444 (1.392-1.51) | 1.408 (1.396-1.612) | -2.5% | 1.412, 1.463, 1.473 / 1.433, 1.402, 1.511 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.44 (0.4264-0.4478) | 0.4461 (0.4389-0.4498) | +1.4% | 0.4284, 0.4414, 0.4444 / 0.4457, 0.4481, 0.442 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 9.977 (9.902-10.39) | 10.01 (9.876-10.23) | +0.4% | 9.914, 10.1, 10.19 / 10.05, 10.03, 9.985 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 5.087 (4.972-5.207) | 5.132 (5.021-5.179) | +0.9% | 4.997, 5.087, 5.185 / 5.046, 5.14, 5.167 | within noise |
| dense 30 x 784 bare downstream b32 / numpy | 23.69 (23.51-24.04) | 24.05 (23.53-24.21) | +1.5% | 23.9, 23.67, 23.56 / 24.13, 24.01, 23.79 | within noise |
| dense 30 x 784 bare downstream b32 / rust | 32.74 (32.34-33.87) | 32.89 (32.2-33.36) | +0.5% | 32.42, 33.26, 33.34 / 32.89, 32.32, 33.27 | within noise |
| dense 30 x 784 bare downstream b512 / numpy | 138 (111.6-146.2) | 139.1 (134.8-141) | +0.8% | 125.3, 137.1, 142.4 / 136.6, 140.5, 138.9 | within noise |
| dense 30 x 784 bare downstream b512 / rust | 243.9 (235.9-245.9) | 246 (239.3-248) | +0.9% | 239.7, 244.4, 242.3 / 244.1, 246.7, 243.7 | within noise |
| dense 30 x 784 bare accumulate b32 / numpy | 29.42 (28.67-29.92) | 29.04 (28.89-29.51) | -1.3% | 29.81, 29.05, 29.32 / 29.01, 29, 29.26 | within noise |
| dense 30 x 784 bare accumulate b32 / rust | 30.65 (29.62-31.44) | 30.35 (29.76-31.07) | -1.0% | 29.64, 30.83, 31.01 / 30.2, 30.7, 30.13 | within noise |
| dense 30 x 784 bare accumulate b512 / numpy | 191.4 (189.8-192.8) | 194 (191.5-194.9) | +1.4% | 190.6, 192.1, 191.7 / 193, 193.2, 194.1 | separated, inside spread |
| dense 30 x 784 bare accumulate b512 / rust | 279.8 (254.4-293.3) | 282.5 (272.2-288.4) | +1.0% | 279.8, 279.5, 273.9 / 280.9, 280.3, 283.7 | separated, inside spread |
| dense 30 x 784 transpose b32 / numpy | 0.698 (0.677-0.7276) | 0.6923 (0.6827-0.6986) | -0.8% | 0.6817, 0.7012, 0.7116 / 0.6894, 0.6864, 0.6974 | within noise |
| dense 30 x 784 transpose b32 / rust | 0.8296 (0.8101-0.8312) | 0.8305 (0.8199-0.8339) | +0.1% | 0.8106, 0.8303, 0.8303 / 0.8239, 0.8335, 0.8279 | within noise |
| dense 30 x 784 transpose b512 / numpy | 7.239 (7.21-7.284) | 7.229 (7.188-7.29) | -0.1% | 7.277, 7.239, 7.212 / 7.248, 7.21, 7.25 | within noise |
| dense 30 x 784 transpose b512 / rust | 13.64 (13.25-13.94) | 13.25 (12.9-14.16) | -2.9% | 13.7, 13.38, 13.86 / 13.67, 13.35, 13.13 | within noise |
| dense 30 x 784 add b32 / numpy | 11.43 (10.53-11.72) | 11.11 (10.44-11.59) | -2.8% | 11.43, 11.12, 11.38 / 11.11, 11.28, 10.81 | within noise |
| dense 30 x 784 add b32 / rust | 9.234 (8.771-9.432) | 8.808 (8.666-9.267) | -4.6% | 9.254, 9.098, 9.228 / 8.749, 9.027, 8.783 | separated, inside spread |
| dense 30 x 784 add b512 / numpy | 11.44 (10.73-11.94) | 11.36 (10.93-12.03) | -0.7% | 11.81, 11.34, 11.11 / 11.55, 11.75, 10.99 | within noise |
| dense 30 x 784 add b512 / rust | 9.213 (8.316-9.552) | 8.639 (8.523-9.008) | -6.2% | 9.176, 8.934, 9.213 / 8.766, 8.745, 8.608 | separated, inside spread |
| dense 30 x 784 sum_axis0 b32 / numpy | 1.466 (1.447-1.498) | 1.438 (1.404-1.474) | -1.9% | 1.472, 1.454, 1.483 / 1.438, 1.41, 1.47 | within noise |
| dense 30 x 784 sum_axis0 b32 / rust | 0.4002 (0.3926-0.4139) | 0.4021 (0.3959-0.4145) | +0.5% | 0.394, 0.4009, 0.4076 / 0.4052, 0.4026, 0.4014 | within noise |
| dense 30 x 784 sum_axis0 b512 / numpy | 10.85 (10.64-10.93) | 10.79 (10.63-10.95) | -0.5% | 10.9, 10.65, 10.87 / 10.67, 10.78, 10.92 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 4.437 (4.302-4.565) | 4.466 (4.408-4.569) | +0.7% | 4.348, 4.437, 4.525 / 4.438, 4.471, 4.489 | within noise |
| dense 10 x 30 bare downstream b32 / numpy | 1.756 (1.73-1.823) | 1.78 (1.704-1.799) | +1.3% | 1.739, 1.782, 1.765 / 1.768, 1.751, 1.78 | within noise |
| dense 10 x 30 bare downstream b32 / rust | 1.123 (1.102-1.171) | 1.123 (1.1-1.15) | +0.0% | 1.108, 1.122, 1.153 / 1.125, 1.123, 1.123 | within noise |
| dense 10 x 30 bare downstream b512 / numpy | 12.22 (12.14-12.51) | 12.26 (12.08-12.5) | +0.4% | 12.22, 12.15, 12.42 / 12.09, 12.26, 12.42 | within noise |
| dense 10 x 30 bare downstream b512 / rust | 15.39 (14.95-16.02) | 15.36 (15.19-15.65) | -0.2% | 15.01, 15.39, 15.86 / 15.35, 15.51, 15.3 | within noise |
| dense 10 x 30 bare accumulate b32 / numpy | 1.816 (1.769-1.821) | 1.792 (1.742-1.829) | -1.4% | 1.794, 1.818, 1.796 / 1.768, 1.815, 1.777 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 1.205 (1.197-1.225) | 1.204 (1.199-1.21) | -0.1% | 1.199, 1.208, 1.217 / 1.206, 1.202, 1.207 | within noise |
| dense 10 x 30 bare accumulate b512 / numpy | 13.57 (13.44-13.77) | 13.36 (13.3-13.48) | -1.6% | 13.62, 13.51, 13.63 / 13.34, 13.33, 13.44 | separated, inside spread |
| dense 10 x 30 bare accumulate b512 / rust | 25.52 (25.15-29.19) | 25.47 (25.15-26.27) | -0.2% | 27.82, 25.36, 25.36 / 25.39, 25.71, 25.53 | within noise |
| dense 10 x 30 transpose b32 / numpy | 0.4432 (0.4328-0.4509) | 0.4456 (0.4371-0.4564) | +0.5% | 0.433, 0.4432, 0.4475 / 0.4416, 0.4493, 0.4475 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.3854 (0.3741-0.3931) | 0.3772 (0.3725-0.3835) | -2.1% | 0.3827, 0.3867, 0.3854 / 0.3756, 0.3746, 0.3823 | separated, inside spread |
| dense 10 x 30 transpose b512 / numpy | 2.956 (2.881-3.033) | 2.945 (2.92-3.03) | -0.4% | 2.998, 2.947, 2.94 / 2.934, 2.931, 2.997 | within noise |
| dense 10 x 30 transpose b512 / rust | 3.91 (3.793-3.947) | 3.87 (3.817-3.951) | -1.0% | 3.817, 3.929, 3.922 / 3.851, 3.85, 3.928 | within noise |
| dense 10 x 30 add b32 / numpy | 0.4039 (0.3996-0.415) | 0.4087 (0.3976-0.4097) | +1.2% | 0.3997, 0.4039, 0.4123 / 0.401, 0.4096, 0.4087 | within noise |
| dense 10 x 30 add b32 / rust | 0.19 (0.1843-0.1919) | 0.1887 (0.1868-0.1947) | -0.7% | 0.1877, 0.1894, 0.1907 / 0.1907, 0.1898, 0.1882 | within noise |
| dense 10 x 30 add b512 / numpy | 0.4185 (0.4073-0.4256) | 0.415 (0.4061-0.4265) | -0.8% | 0.4074, 0.4185, 0.4251 / 0.4099, 0.4152, 0.4215 | within noise |
| dense 10 x 30 add b512 / rust | 0.2003 (0.195-0.2115) | 0.2004 (0.1974-0.2151) | +0.0% | 0.1952, 0.2003, 0.2076 / 0.1984, 0.212, 0.2002 | within noise |
| dense 10 x 30 sum_axis0 b32 / numpy | 1.322 (1.287-1.364) | 1.302 (1.288-1.331) | -1.5% | 1.332, 1.309, 1.338 / 1.306, 1.294, 1.318 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.3206 (0.3115-0.3368) | 0.3206 (0.315-0.3355) | +0.0% | 0.3146, 0.3293, 0.3211 / 0.3181, 0.3276, 0.3216 | within noise |
| dense 10 x 30 sum_axis0 b512 / numpy | 8.971 (8.903-9.248) | 9.04 (8.974-9.305) | +0.8% | 8.949, 8.943, 9.211 / 8.985, 9.043, 9.2 | within noise |
| dense 10 x 30 sum_axis0 b512 / rust | 3.266 (3.207-3.298) | 3.248 (3.201-3.302) | -0.5% | 3.21, 3.29, 3.266 / 3.226, 3.223, 3.291 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 291.6 (286.5-294) | 288.5 (286-292.8) | -1.1% | 293.2, 289.2, 288.9 / 288.4, 289.3, 289.7 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 406 (399.1-411.1) | 403.3 (401.4-407.5) | -0.7% | 403.2, 407.2, 406.3 / 404.5, 403.1, 404.7 | within noise |
| attention 16 x 32 forward_batch b512 / numpy | 4896 (4660-4969) | 4920 (4906-4949) | +0.5% | 4669, 4932, 4912 / 4920, 4917, 4929 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 6361 (6261-6474) | 6365 (6283-6591) | +0.1% | 6361, 6290, 6473 / 6316, 6492, 6343 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 265.8 (261-272.2) | 262.5 (259.9-265.8) | -1.2% | 270.6, 262.4, 265.8 / 263.6, 259.9, 263.6 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / rust | 245.4 (242.3-251.5) | 243.1 (240.9-251.7) | -0.9% | 243.4, 247.7, 248.9 / 241.9, 242.7, 250 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 4494 (4372-4524) | 4495 (4442-4539) | +0.0% | 4431, 4507, 4505 / 4483, 4486, 4514 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / rust | 4624 (4571-4670) | 4636 (4493-4804) | +0.3% | 4670, 4624, 4583 / 4574, 4669, 4692 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 248.6 (236.7-262) | 247.9 (243.1-252) | -0.3% | 251.9, 251.4, 243.4 / 246.3, 247.5, 248.9 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 218.2 (203.6-231.8) | 208.8 (199.3-216.3) | -4.3% | 218.2, 213.9, 219.8 / 214.9, 205.7, 205.3 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5593 (5469-5679) | 5526 (5481-5655) | -1.2% | 5577, 5670, 5513 / 5526, 5565, 5579 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 3985 (3928-4009) | 3989 (3958-4000) | +0.1% | 3988, 4002, 3940 / 3999, 3972, 3976 | within noise |
