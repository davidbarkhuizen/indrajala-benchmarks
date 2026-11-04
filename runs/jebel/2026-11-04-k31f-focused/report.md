Old `515849f` against new `515849f`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --shape 5408 --shape 784 --shape attention --op forward_batch --op downstream_batch --op accumulate_gradient_batch --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `cba601e` (extension sha256 `bc8a4a1fc83d`) and new crate `480cebc` (extension sha256 `5b3d1d17cea4`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.51 (HIGH); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- 36 rows within noise, max |Δ| 1.8%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward_batch b32 / numpy | 152.7 (146.1-159.5) | 154.3 (146.9-159.3) | +1.0% | 153.4, 152.8, 152.4 / 154.7, 154.2, 153.1 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 237.4 (224.6-239.6) | 236.4 (227.5-259.5) | -0.4% | 228.9, 237.9, 239.1 / 232.4, 235.5, 248.7 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1171 (1078-1173) | 1172 (1112-1179) | +0.1% | 1125, 1172, 1171 / 1142, 1175, 1173 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1124 (1114-1127) | 1120 (1106-1137) | -0.3% | 1120, 1120, 1126 / 1125, 1120, 1117 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 77.91 (77.18-78.57) | 78.26 (77.78-78.49) | +0.4% | 77.34, 77.91, 78.34 / 77.82, 78.33, 78.42 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 247.1 (235-253.8) | 243.5 (236.9-252) | -1.5% | 237.2, 247.1, 251.5 / 238.4, 245.3, 247.9 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3188 (3180-3203) | 3185 (3109-3218) | -0.1% | 3184, 3186, 3195 / 3198, 3164, 3156 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2399 (2384-2407) | 2414 (2386-2433) | +0.6% | 2400, 2402, 2391 / 2398, 2425, 2414 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 161.4 (159.4-163.9) | 161.4 (159.6-164.8) | +0.0% | 160.3, 163, 161.4 / 162.2, 162.2, 161 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 281.3 (266.1-288.4) | 277.2 (272.2-289.2) | -1.5% | 272.3, 285.2, 281.3 / 274.8, 275, 285.7 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 1829 (1813-1859) | 1841 (1826-1893) | +0.6% | 1840, 1828, 1829 / 1866, 1830, 1850 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 1986 (1971-2019) | 1981 (1971-1983) | -0.2% | 1979, 1984, 2002 / 1977, 1982, 1979 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 38.71 (37.78-38.99) | 38.29 (37.95-38.9) | -1.1% | 37.82, 38.89, 38.72 / 38.09, 38.17, 38.72 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 34.98 (33.81-35.65) | 35.17 (33.87-36.25) | +0.5% | 33.83, 34.98, 35.62 / 34.08, 35.17, 36.06 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 269.6 (265.6-270.9) | 267.6 (265.3-270.1) | -0.8% | 266.4, 270.2, 269.8 / 266.2, 267.2, 269.4 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 248.9 (246-249.7) | 249.5 (246-249.8) | +0.3% | 246.9, 248.9, 249.6 / 249.6, 247.2, 249.7 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 24.13 (23.84-24.71) | 24.23 (23.51-24.41) | +0.5% | 24.1, 24.06, 24.45 / 23.92, 24.2, 24.32 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 33.17 (33.03-34.36) | 33.69 (32.4-34.49) | +1.6% | 33.17, 33.03, 34.3 / 33.03, 33.45, 34.42 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 131.2 (130.1-132.8) | 131.7 (130.1-132.5) | +0.4% | 130.5, 131.1, 132.6 / 130.7, 131.3, 132.5 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 243.6 (241.5-247.6) | 246.5 (240.7-247.6) | +1.2% | 242.1, 245.7, 245.2 / 243.8, 246.8, 246.5 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 40.05 (39.38-40.89) | 40.51 (40.06-41.41) | +1.2% | 39.89, 40.32, 40.05 / 40.06, 40.51, 41.34 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 40.68 (39.88-41.41) | 41.4 (40.18-42.38) | +1.8% | 40.65, 40.16, 41.39 / 40.72, 41.21, 42.37 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 224.7 (221.6-226.2) | 224.3 (221.7-226.3) | -0.2% | 222.5, 225.3, 225.4 / 221.9, 224.3, 226 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 257 (254.3-259) | 256.1 (255.2-257.9) | -0.4% | 256.9, 255.5, 258.4 / 256.2, 255.8, 257.1 | within noise |
| relu 30 x 784 forward_batch b32 / numpy | 30.36 (29.65-31.13) | 30.33 (29.83-30.69) | -0.1% | 29.69, 30.81, 30.47 / 29.88, 30.33, 30.55 | within noise |
| relu 30 x 784 forward_batch b32 / rust | 32.29 (31.28-33.03) | 32.59 (31.06-33.48) | +0.9% | 31.71, 32.99, 32.29 / 31.53, 32.59, 33.38 | within noise |
| relu 30 x 784 forward_batch b512 / numpy | 157.6 (156.6-158.4) | 158.5 (156.7-159) | +0.6% | 157.5, 157.1, 158 / 157.7, 158.1, 158.7 | within noise |
| relu 30 x 784 forward_batch b512 / rust | 199.2 (198.3-200.2) | 197.9 (196.9-199.4) | -0.6% | 198.6, 200.1, 199 / 197.3, 198.4, 198.7 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 365.3 (363.2-368.8) | 362.3 (360.8-378) | -0.8% | 365.2, 366.3, 365.3 / 362.7, 361.4, 369.6 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 266.9 (261.8-272.6) | 269.7 (266.3-277.8) | +1.0% | 261.9, 266.9, 270.9 / 267.3, 269.7, 275.7 | within noise |
| attention 16 x 32 forward_batch b512 / numpy | 5640 (5606-5689) | 5640 (5614-5705) | -0.0% | 5645, 5640, 5662 / 5640, 5619, 5691 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 4250 (4196-4354) | 4266 (4165-4459) | +0.4% | 4218, 4240, 4345 / 4251, 4219, 4359 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 250.7 (236.3-256.7) | 249.5 (243-255.3) | -0.4% | 252.7, 246.5, 244.4 / 249.5, 249.1, 249.6 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 119.3 (118.7-120.9) | 119.6 (116.8-122.9) | +0.3% | 119.3, 118.7, 120.2 / 118.3, 121, 119.6 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5385 (5348-5576) | 5423 (5321-5562) | +0.7% | 5429, 5482, 5370 / 5370, 5436, 5460 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 1600 (1591-1625) | 1609 (1595-1627) | +0.5% | 1608, 1593, 1607 / 1614, 1602, 1618 | within noise |
