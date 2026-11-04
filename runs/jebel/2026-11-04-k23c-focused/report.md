Old `bb60c11` against new `bb60c11`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --shape 5408 --shape 784 --shape attention --op forward_batch --op downstream_batch --op accumulate_gradient_batch --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `10aa3e5` (extension sha256 `24bdf26aceef`) and new crate `3bb2a40` (extension sha256 `bb3d5611c37d`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.92 (HIGH); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / attention 16 x 32 accumulate_gradient_batch b512 / rust -46.6% (3018 -> 1611 µs)
- consistent: per call / attention 16 x 32 accumulate_gradient_batch b32 / rust -34.3% (170.6 -> 112.1 µs)
- 34 rows within noise (2 separated inside their spread), max |Δ| 3.0%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward_batch b32 / numpy | 148.9 (146.7-159.8) | 153 (147.4-160.2) | +2.7% | 148.9, 153.2, 152.6 / 153.2, 153.8, 153 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 241.8 (227.8-257.8) | 234.5 (228.8-243.6) | -3.0% | 229.6, 249, 243.9 / 231, 233, 240.8 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1170 (1063-1174) | 1156 (1066-1176) | -1.3% | 1111, 1172, 1173 / 1117, 1133, 1160 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1135 (1128-1149) | 1123 (1116-1137) | -1.1% | 1128, 1142, 1136 / 1119, 1127, 1123 | separated, inside spread |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 78.4 (77.27-78.78) | 77.88 (76.92-78.32) | -0.7% | 78.02, 77.95, 78.48 / 77.08, 77.88, 78.29 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 243 (239.3-250.5) | 245.6 (237-250.4) | +1.1% | 239.9, 242.7, 248.9 / 241.1, 245.2, 249.6 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3191 (3163-3207) | 3191 (3167-3205) | -0.0% | 3185, 3179, 3198 / 3198, 3178, 3193 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2399 (2384-2437) | 2393 (2381-2448) | -0.3% | 2422, 2386, 2399 / 2388, 2414, 2395 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 161.9 (158.5-164.9) | 162.7 (159.2-167.5) | +0.5% | 158.7, 163.2, 163 / 160.7, 164.4, 164.3 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 274.2 (265.8-288.3) | 280.2 (273.8-283.4) | +2.2% | 270.7, 279.3, 279.7 / 278.6, 280.3, 278.2 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 1824 (1793-1876) | 1814 (1792-1858) | -0.6% | 1831, 1807, 1852 / 1833, 1835, 1795 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 1956 (1887-2071) | 1964 (1946-2148) | +0.4% | 1918, 2004, 1966 / 2047, 1960, 1964 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 38.34 (37.7-38.9) | 38.18 (37.67-39.03) | -0.4% | 38.3, 37.91, 38.8 / 37.97, 38.05, 38.74 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 35.87 (34.18-36.12) | 35.58 (34.67-35.99) | -0.8% | 34.55, 35.87, 36.04 / 34.73, 35.79, 35.62 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 266.3 (264.8-268.2) | 266.9 (265.3-268.7) | +0.2% | 265.1, 266.3, 267.7 / 266, 268.1, 266.9 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 261.8 (257.9-291.9) | 263.3 (256.9-267.6) | +0.6% | 259.7, 279.6, 261.4 / 257.3, 264.1, 265.2 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 23.95 (23.69-24.17) | 24.24 (23.77-24.33) | +1.2% | 23.83, 24.05, 24.02 / 23.98, 24.31, 24.08 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 32.72 (32.44-33.86) | 33.64 (30.27-34.07) | +2.8% | 32.5, 32.68, 33.71 / 33.97, 31.94, 33.06 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 130.9 (130.4-134.4) | 131 (130.3-137.2) | +0.1% | 132.8, 130.5, 130.9 / 133.9, 131.2, 130.6 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 239.8 (239.1-244.2) | 243.9 (238.8-246.7) | +1.7% | 240.2, 239.2, 241.9 / 241.1, 245.9, 243.8 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 39.98 (39.29-41.01) | 40.54 (39.26-41.78) | +1.4% | 39.81, 39.85, 40.47 / 40.52, 40.79, 40.29 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 40.92 (39.57-41.86) | 41.46 (40.53-42.5) | +1.3% | 40.06, 40.92, 41.46 / 40.56, 41.62, 41.97 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 223.3 (220.9-224.1) | 224 (219.1-225) | +0.3% | 222.2, 224.1, 223.2 / 220.5, 224.8, 224 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 255.5 (251.8-257.4) | 256.5 (251.3-261.5) | +0.4% | 253.1, 255.5, 257 / 257.1, 252.7, 260 | within noise |
| relu 30 x 784 forward_batch b32 / numpy | 29.86 (29.62-30.23) | 29.73 (29.63-30.37) | -0.4% | 29.93, 29.94, 29.86 / 29.65, 29.98, 30.08 | within noise |
| relu 30 x 784 forward_batch b32 / rust | 32.81 (32.18-33.49) | 32.94 (32.15-33.25) | +0.4% | 32.35, 32.69, 33.45 / 32.32, 33.04, 33.08 | within noise |
| relu 30 x 784 forward_batch b512 / numpy | 155.5 (155.4-158.6) | 157.3 (156.5-160) | +1.2% | 156, 155.4, 157 / 158.3, 158.1, 157.3 | separated, inside spread |
| relu 30 x 784 forward_batch b512 / rust | 212.1 (207.6-214.2) | 212.4 (209.4-216) | +0.1% | 211.6, 212.7, 210.9 / 213.6, 212, 211.5 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 362.4 (360.8-371.4) | 366.9 (360.9-372.2) | +1.3% | 364.3, 361.9, 366.3 / 366.6, 366.1, 367.2 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 325.6 (315.9-337.1) | 325.1 (320.3-330.8) | -0.2% | 317.9, 325.6, 335.4 / 321.9, 327.6, 327.8 | within noise |
| attention 16 x 32 forward_batch b512 / numpy | 5631 (5551-5681) | 5606 (5504-5665) | -0.4% | 5555, 5638, 5669 / 5623, 5585, 5606 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 5046 (5009-5111) | 5046 (5011-5119) | -0.0% | 5042, 5046, 5071 / 5018, 5110, 5046 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 247 (243.5-260.1) | 248.9 (246.4-254.4) | +0.7% | 252.9, 245.5, 251.2 / 251.4, 246.8, 250.4 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 170.6 (165.1-172.2) | 112.1 (110.6-115.9) | -34.3% | 169.3, 168.6, 171.3 / 110.9, 113.7, 113.3 | consistent |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5411 (5265-5534) | 5431 (5345-5524) | +0.4% | 5365, 5339, 5534 / 5430, 5432, 5435 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 3018 (2986-3080) | 1611 (1598-1621) | -46.6% | 3020, 3010, 3033 / 1612, 1605, 1611 | consistent |
