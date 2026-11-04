Old `5cf590a` against new `5cf590a`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --shape 5408 --shape 784 --shape attention --op forward_batch --op downstream_batch --op accumulate_gradient_batch --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `238a017` (extension sha256 `bb3d5611c37d`) and new crate `18ce111` (extension sha256 `bc8a4a1fc83d`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.85; busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / attention 16 x 32 forward_batch b512 / rust -17.6% (5091 -> 4193 µs)
- consistent: per call / attention 16 x 32 forward_batch b32 / rust -17.5% (325.5 -> 268.5 µs)
- consistent: per call / relu 30 x 784 forward_batch b512 / rust -5.9% (212.7 -> 200.1 µs)
- consistent: per call / dense 30 x 784 forward_batch b512 / rust -5.2% (262.7 -> 249 µs)
- 32 rows within noise (3 separated inside their spread), max |Δ| 3.9%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward_batch b32 / numpy | 153.3 (147.1-160.4) | 153 (146.9-160.5) | -0.2% | 153.2, 152.1, 154.9 / 151.8, 152.9, 155.1 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 236.3 (227.5-239.5) | 236.4 (231.9-239) | +0.1% | 229.9, 236.3, 239.1 / 235.4, 236.4, 235.8 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1169 (1068-1173) | 1160 (1074-1179) | -0.7% | 1118, 1168, 1172 / 1126, 1152, 1162 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1140 (1133-1152) | 1127 (1109-1137) | -1.1% | 1135, 1139, 1147 / 1126, 1121, 1131 | separated, inside spread |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 77.99 (77.49-78.49) | 77.91 (77.64-78.27) | -0.1% | 77.73, 78.03, 78.11 / 78.01, 77.68, 78.05 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 247.2 (240.5-254.1) | 248 (246-250.9) | +0.3% | 243.8, 248.2, 248.6 / 246.5, 247.7, 250.8 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3185 (3171-3196) | 3177 (3168-3201) | -0.2% | 3190, 3179, 3190 / 3186, 3171, 3185 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2405 (2385-2421) | 2401 (2383-2449) | -0.2% | 2407, 2403, 2405 / 2392, 2426, 2404 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 160.9 (158.2-165.4) | 162.9 (161.2-166.8) | +1.2% | 159.2, 160.9, 163.3 / 162.7, 164.2, 162.7 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 277.4 (269.4-285.7) | 280.5 (276.4-288.1) | +1.1% | 270.8, 277.9, 284.1 / 280.5, 277.7, 285.4 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 1843 (1813-1877) | 1823 (1793-1848) | -1.1% | 1815, 1849, 1858 / 1805, 1837, 1828 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 1971 (1945-1987) | 1970 (1902-2195) | -0.1% | 1983, 1955, 1973 / 2077, 1965, 1941 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 38.72 (37.56-40.15) | 38.39 (37.79-39.01) | -0.9% | 38.46, 38.57, 39.46 / 38.16, 38.22, 38.9 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 35.82 (34.22-37.83) | 35.25 (33.68-36.23) | -1.6% | 34.71, 35.82, 37.14 / 34.99, 34.5, 35.82 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 267.4 (264.1-270.4) | 267.4 (264.2-269) | -0.0% | 265.2, 268, 268.7 / 266, 267.8, 268 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 262.7 (259.5-272.2) | 249 (243-250.1) | -5.2% | 260.8, 268.1, 261.8 / 246.5, 247.9, 249.6 | consistent |
| dense 30 x 784 downstream_batch b32 / numpy | 24.25 (24.11-24.48) | 24.39 (23.8-24.46) | +0.6% | 24.23, 24.37, 24.24 / 24.08, 24.12, 24.45 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 33.7 (32.5-34.64) | 33.15 (32.45-34.44) | -1.6% | 33, 33.62, 34.27 / 32.88, 32.88, 33.98 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 131.1 (129.9-131.8) | 131.2 (130.4-131.9) | +0.1% | 130.2, 131.1, 131.5 / 131.5, 130.8, 131.2 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 243.4 (241.8-244.9) | 241.9 (240.2-244.9) | -0.6% | 242.8, 244.1, 243.3 / 241.1, 241.2, 244.3 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 40.13 (39.59-41.19) | 40.5 (39.3-41.34) | +0.9% | 40, 40.2, 40.66 / 40.14, 39.79, 41.12 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 40.77 (40.01-42.66) | 40.79 (40.04-42.5) | +0.1% | 40.51, 41.33, 41.08 / 40.73, 40.32, 42.36 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 223.6 (222-226.3) | 224.8 (220.7-226.7) | +0.5% | 222.8, 225, 223.6 / 222.9, 223.8, 225.5 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 256.1 (252.8-261.6) | 257.2 (255-262.6) | +0.5% | 253, 256.1, 260.1 / 258.8, 256.2, 258.2 | within noise |
| relu 30 x 784 forward_batch b32 / numpy | 30.27 (29.88-30.51) | 29.91 (29.58-30.54) | -1.2% | 30.12, 30.45, 30.15 / 30.03, 29.91, 30.11 | separated, inside spread |
| relu 30 x 784 forward_batch b32 / rust | 33.21 (32.13-34.12) | 32.31 (31.63-33.17) | -2.7% | 32.23, 33.26, 34.03 / 31.91, 32.71, 32.4 | within noise |
| relu 30 x 784 forward_batch b512 / numpy | 157.7 (155.4-159.5) | 157.3 (156.1-158.5) | -0.3% | 155.9, 157.7, 158.8 / 157.6, 156.9, 157.3 | within noise |
| relu 30 x 784 forward_batch b512 / rust | 212.7 (209.5-213.5) | 200.1 (197.3-201.6) | -5.9% | 211.9, 211.1, 213.3 / 199.1, 201.2, 198.7 | consistent |
| attention 16 x 32 forward_batch b32 / numpy | 368.6 (363-373.1) | 368.3 (361.6-371.9) | -0.1% | 368.6, 373, 364.5 / 361.7, 369.5, 369.6 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 325.5 (321.1-328.9) | 268.5 (266.3-274.2) | -17.5% | 321.2, 325.5, 328.4 / 267.9, 267.5, 272.1 | consistent |
| attention 16 x 32 forward_batch b512 / numpy | 5661 (5570-5696) | 5631 (5597-5673) | -0.5% | 5613, 5665, 5678 / 5600, 5638, 5657 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 5091 (5005-5170) | 4193 (4162-4269) | -17.6% | 5066, 5105, 5102 / 4172, 4184, 4248 | consistent |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 253.1 (247.6-265.9) | 250.2 (245.6-257.3) | -1.1% | 263.7, 249.7, 253.1 / 251, 251.5, 249.5 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 113.7 (108.7-115.6) | 118.1 (116.5-122.4) | +3.9% | 110.4, 113.7, 114.7 / 118.3, 116.5, 120.9 | separated, inside spread |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5399 (5347-5461) | 5361 (5305-5444) | -0.7% | 5406, 5362, 5442 / 5310, 5373, 5416 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 1619 (1603-1635) | 1614 (1608-1642) | -0.3% | 1610, 1616, 1634 / 1611, 1628, 1625 | within noise |
