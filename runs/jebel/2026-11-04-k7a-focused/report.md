Old `1854b89` against new `1854b89`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --shape 5408 --shape 784 --shape attention --op forward_batch --op downstream_batch --op accumulate_gradient_batch --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `690bce8` (extension sha256 `7ba3057a73f7`) and new crate `5a19b18` (extension sha256 `84ec4e85d91b`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.15; busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / attention 16 x 32 accumulate_gradient_batch b512 / rust -24.6% (3975 -> 2997 µs)
- consistent: per call / dense 30 x 784 accumulate_gradient_batch b512 / rust -18.1% (312.4 -> 255.9 µs)
- consistent: per call / conv tail 32 x 5408 accumulate_gradient_batch b512 / rust -14.5% (2309 -> 1975 µs)
- consistent: per call / attention 16 x 32 accumulate_gradient_batch b32 / rust -11.5% (190.1 -> 168.3 µs)
- 32 rows within noise (1 separated inside their spread), max |Δ| 4.3%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward_batch b32 / numpy | 153 (147.8-163.4) | 154 (147.6-158.6) | +0.7% | 152.3, 153.9, 156.4 / 154, 152.9, 153.9 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 348.4 (328-380) | 362.6 (341.1-404.7) | +4.1% | 354, 339, 354.7 / 343.5, 387, 362.9 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1167 (1054-1173) | 1166 (1156-1171) | -0.1% | 1110, 1169, 1170 / 1163, 1163, 1168 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1701 (1613-1759) | 1629 (1600-1760) | -4.3% | 1678, 1650, 1752 / 1615, 1691, 1666 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 78.02 (77.72-78.27) | 78.14 (77.19-78.32) | +0.1% | 78, 78.11, 78.02 / 78.14, 77.6, 78.3 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 242.4 (232.3-249.2) | 241.2 (237.6-244.1) | -0.5% | 237.2, 243.1, 245.9 / 242.3, 239.2, 241.7 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3190 (3156-3206) | 3172 (3161-3199) | -0.5% | 3183, 3181, 3190 / 3168, 3191, 3166 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2245 (2239-2258) | 2249 (2243-2269) | +0.2% | 2245, 2256, 2240 / 2246, 2249, 2259 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 162.9 (159-164.1) | 163.2 (161.9-164.9) | +0.2% | 160.2, 163, 163.8 / 162.4, 164, 163.4 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 272.9 (269.4-275.4) | 274.5 (269.7-276.5) | +0.6% | 271.5, 273.6, 272.6 / 271.3, 276.1, 274.3 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 1847 (1802-1883) | 1841 (1795-1914) | -0.3% | 1828, 1862, 1852 / 1833, 1888, 1821 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 2309 (2260-2366) | 1975 (1939-2157) | -14.5% | 2351, 2324, 2265 / 1971, 1956, 2075 | consistent |
| dense 30 x 784 forward_batch b32 / numpy | 38.1 (37.57-38.79) | 38.64 (37.76-39.32) | +1.4% | 38.48, 38.07, 37.8 / 38.48, 39.15, 38.24 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 45.41 (45.09-46.12) | 45.65 (43.94-46.72) | +0.5% | 45.15, 45.82, 45.58 / 44.46, 45.95, 46.14 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 265.5 (263.5-267.7) | 266.1 (264-268.6) | +0.2% | 263.6, 266.5, 266.3 / 264.5, 266.8, 267.2 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 289 (286.9-290.7) | 291.5 (283.8-294) | +0.9% | 288.8, 287.7, 289.6 / 287.9, 293.5, 290 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 23.9 (23.48-24.43) | 24.05 (23.2-24.36) | +0.6% | 24.15, 23.65, 24.03 / 23.91, 24.3, 23.58 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 32.78 (31.48-33.93) | 32.65 (32.45-33.14) | -0.4% | 31.77, 33.13, 33.45 / 32.6, 32.8, 32.74 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 130.5 (129.2-130.9) | 130.7 (129.8-131.1) | +0.1% | 130, 130.5, 130.6 / 130.1, 130.8, 130.9 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 242.3 (240.1-245.7) | 242.9 (241.4-246.1) | +0.3% | 242, 242.3, 244.1 / 243.8, 242.5, 243.5 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 40.16 (39.73-41.52) | 41.07 (39.56-41.63) | +2.3% | 39.87, 41.17, 40.06 / 40.88, 41.51, 40.18 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 40.31 (39.38-40.78) | 40.1 (39.13-40.87) | -0.5% | 39.77, 40.21, 40.67 / 40.1, 39.96, 40.19 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 222.3 (219.9-226.8) | 222.8 (221.8-224.1) | +0.3% | 220.4, 222.8, 224.6 / 222.2, 223.6, 222.8 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 312.4 (305-318.1) | 255.9 (250.3-262.7) | -18.1% | 312.4, 310.7, 313.4 / 255.7, 255.9, 256.5 | consistent |
| relu 30 x 784 forward_batch b32 / numpy | 29.92 (29.46-30.85) | 30.34 (29.83-31.01) | +1.4% | 29.9, 29.64, 30.52 / 30.26, 30.42, 30.47 | within noise |
| relu 30 x 784 forward_batch b32 / rust | 42.82 (42.45-43.38) | 43.28 (42.09-44.23) | +1.1% | 42.8, 42.82, 43.03 / 42.81, 42.96, 43.78 | within noise |
| relu 30 x 784 forward_batch b512 / numpy | 157.4 (157.1-158.5) | 156.6 (155.9-158.8) | -0.5% | 157.2, 157.3, 158.3 / 156.4, 156.3, 158.4 | within noise |
| relu 30 x 784 forward_batch b512 / rust | 239.4 (235.8-245.4) | 241.1 (239.5-246.8) | +0.7% | 236.1, 239.4, 244.1 / 244.9, 240.2, 240.9 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 363.1 (361.9-365.3) | 366.9 (362.6-369.1) | +1.1% | 363.6, 362.8, 363.3 / 365.4, 367.7, 365.4 | separated, inside spread |
| attention 16 x 32 forward_batch b32 / rust | 328 (322.6-332.1) | 328.7 (322.2-329.9) | +0.2% | 323.9, 329.3, 330.6 / 325.5, 329, 329.2 | within noise |
| attention 16 x 32 forward_batch b512 / numpy | 5590 (5527-5693) | 5594 (5544-5608) | +0.1% | 5551, 5598, 5649 / 5576, 5588, 5597 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 5292 (5206-5321) | 5299 (5181-5460) | +0.1% | 5263, 5281, 5292 / 5226, 5379, 5305 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 247.7 (245.8-255.1) | 249.4 (240.8-259.6) | +0.7% | 247.1, 247.7, 251.1 / 254, 253.9, 244.1 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 190.1 (184.4-204.3) | 168.3 (167-178.3) | -11.5% | 185.9, 198.6, 194.8 / 168.9, 167.9, 173.1 | consistent |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5382 (5312-5523) | 5334 (5306-5522) | -0.9% | 5330, 5368, 5500 / 5330, 5417, 5363 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 3975 (3931-4008) | 2997 (2982-3055) | -24.6% | 3996, 3945, 3972 / 3023, 2993, 2993 | consistent |
