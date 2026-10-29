Old `d6a4d25` against new `e54cd1d`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `40a2761` (extension sha256 `b307f197fdc7`) and new crate `2eb9311` (extension sha256 `694886c704e2`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (raspberry-pi-5.json); max 1-min load 4.09 (HIGH) (measured just after this run's crate builds); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / attention 16 x 32 accumulate_gradient_batch b32 / rust -86.6% (3817 -> 509.8 µs)
- consistent: per call / conv tail 32 x 5408 accumulate_gradient_batch b512 / rust -83.6% (1.2e+05 -> 1.969e+04 µs)
- consistent: per call / conv tail 32 x 5408 bare accumulate b32 / rust -83.4% (7308 -> 1211 µs)
- consistent: per call / dense 30 x 784 bare accumulate b32 / rust -83.1% (745 -> 125.9 µs)
- consistent: per call / dense 30 x 784 bare downstream b32 / rust -83.1% (748.4 -> 126.6 µs)
- consistent: per call / dense 30 x 784 downstream_batch b32 / rust -83.0% (747.3 -> 127 µs)
- consistent: per call / conv tail 32 x 5408 downstream_batch b32 / rust -82.8% (7553 -> 1296 µs)
- consistent: per call / conv tail 32 x 5408 bare accumulate b512 / rust -82.4% (1.109e+05 -> 1.956e+04 µs)
- consistent: per call / conv tail 32 x 5408 bare downstream b32 / rust -82.0% (7431 -> 1338 µs)
- consistent: per call / dense 30 x 784 accumulate_gradient_batch b32 / rust -81.6% (760 -> 140 µs)
- ... 87 more consistent rows (report --md)
- 173 rows within noise (18 separated inside their spread), max |Δ| 388.3%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 78.39 (77.04-80.59) | 78.35 (77.6-80.32) | -0.1% | 77.77, 80.03, 77.74 / 78.16, 78.96, 78.89 | within noise |
| conv tail 32 x 5408 forward / rust | 164.1 (164-164.2) | 164.2 (164-164.7) | +0.1% | 164.1, 164.1, 164.1 / 164.2, 164.1, 164.6 | within noise |
| conv tail 32 x 5408 downstream / numpy | 92.72 (91.21-93.6) | 91.67 (91.41-92.04) | -1.1% | 92.41, 92.29, 92.72 / 91.74, 91.54, 91.77 | consistent |
| conv tail 32 x 5408 downstream / rust | 234.8 (220.6-245.9) | 75.52 (73.93-92.28) | -67.8% | 234.8, 232, 233.2 / 74.16, 83.15, 84.47 | consistent |
| conv tail 32 x 5408 hidden_delta / numpy | 104.8 (103.5-105.9) | 104.7 (103.1-105.2) | -0.1% | 104.9, 105, 104.5 / 103.9, 105.2, 104.2 | within noise |
| conv tail 32 x 5408 hidden_delta / rust | 227.8 (221.4-248.7) | 90.64 (78.72-109.6) | -60.2% | 221.7, 241, 232.4 / 103.5, 81.36, 90.7 | consistent |
| conv tail 32 x 5408 accumulate_gradient / numpy | 654.4 (370-1006) | 629.1 (299.5-968) | -3.9% | 707.9, 624.6, 658.4 / 629.1, 320.3, 953.5 | within noise |
| conv tail 32 x 5408 accumulate_gradient / rust | 98.69 (90.06-101.9) | 97.83 (88.63-99.3) | -0.9% | 95.99, 95.79, 99.38 / 98.52, 93.32, 93.51 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 1673 (1516-2186) | 1609 (1425-1880) | -3.8% | 1528, 1860, 1890 / 1498, 1763, 1627 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 564.7 (414-780.6) | 652.6 (510.2-812.1) | +15.6% | 597.3, 563.4, 564.7 / 621.3, 652.6, 661.1 | separated, inside spread |
| conv tail 32 x 5408 sgd step / numpy | 2959 (2175-3384) | 2751 (2273-2806) | -7.1% | 3241, 2806, 2498 / 2751, 2539, 2568 | within noise |
| conv tail 32 x 5408 sgd step / rust | 118.5 (115.6-278.7) | 119.8 (116.4-122.1) | +1.1% | 116.3, 118.5, 199.4 / 121.4, 117.7, 119.8 | within noise |
| conv tail 32 x 5408 forward_batch b32 / numpy | 513.5 (499.3-555.7) | 531.7 (522.4-537.4) | +3.5% | 527.5, 521.9, 511.2 / 531.7, 522.6, 536.9 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 5254 (5252-5273) | 5253 (5251-5272) | -0.0% | 5254, 5259, 5263 / 5253, 5255, 5262 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1.826e+04 (1.702e+04-1.871e+04) | 1.83e+04 (1.583e+04-1.992e+04) | +0.2% | 1.785e+04, 1.856e+04, 1.765e+04 / 1.722e+04, 1.925e+04, 1.787e+04 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 2.193e+04 (2.179e+04-3.914e+04) | 2.188e+04 (2.183e+04-2.206e+04) | -0.2% | 3.052e+04, 2.184e+04, 2.207e+04 / 2.196e+04, 2.194e+04, 2.186e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 1517 (1048-1540) | 1438 (1300-1663) | -5.3% | 1520, 1508, 1285 / 1410, 1438, 1558 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 7553 (7296-7821) | 1296 (1147-1692) | -82.8% | 7558, 7553, 7566 / 1580, 1223, 1255 | consistent |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3.466e+04 (3.368e+04-4.245e+04) | 3.572e+04 (2.703e+04-4.183e+04) | +3.1% | 3.689e+04, 3.369e+04, 3.899e+04 / 3.403e+04, 3.562e+04, 3.777e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 3.723e+04 (3.388e+04-4.816e+04) | 2.242e+04 (1.684e+04-2.625e+04) | -39.8% | 4.147e+04, 3.546e+04, 3.746e+04 / 2.244e+04, 2.154e+04, 2.148e+04 | consistent |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 3655 (3217-4347) | 3719 (3287-4124) | +1.7% | 3372, 4065, 3725 / 4115, 3543, 3591 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 8315 (7797-8538) | 1961 (1638-2137) | -76.4% | 8197, 8040, 8443 / 1859, 1961, 2026 | consistent |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 7.631e+04 (7.194e+04-8.072e+04) | 7.844e+04 (7.379e+04-9.617e+04) | +2.8% | 7.836e+04, 7.319e+04, 7.634e+04 / 8.865e+04, 7.563e+04, 7.844e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 4.696e+04 (4.365e+04-4.795e+04) | 2.938e+04 (2.665e+04-3.604e+04) | -37.4% | 4.752e+04, 4.709e+04, 4.51e+04 / 2.889e+04, 3.197e+04, 3.134e+04 | consistent |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 1950 (1621-2321) | 2090 (1684-8949) | +7.2% | 2057, 1864, 1918 / 2092, 1841, 5565 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 7870 (7726-8145) | 2364 (2071-3630) | -70.0% | 8003, 7802, 7872 / 2333, 2378, 2850 | consistent |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 2.712e+04 (2.572e+04-2.93e+04) | 2.683e+04 (2.6e+04-2.95e+04) | -1.1% | 2.707e+04, 2.624e+04, 2.839e+04 / 2.745e+04, 2.673e+04, 2.775e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 1.2e+05 (9.116e+04-1.745e+05) | 1.969e+04 (1.949e+04-2.088e+04) | -83.6% | 1.411e+05, 1.414e+05, 1.059e+05 / 2.018e+04, 1.999e+04, 1.959e+04 | consistent |
| dense 30 x 784 forward / numpy | 16.22 (16.03-16.32) | 16.39 (16.22-16.53) | +1.1% | 16.23, 16.2, 16.12 / 16.37, 16.32, 16.43 | separated, inside spread |
| dense 30 x 784 forward / rust | 23.19 (23.15-23.23) | 23.21 (23.21-23.23) | +0.1% | 23.21, 23.18, 23.19 / 23.21, 23.21, 23.22 | within noise |
| dense 30 x 784 downstream / numpy | 12.7 (12.66-12.73) | 12.69 (12.65-12.75) | -0.0% | 12.68, 12.71, 12.7 / 12.72, 12.67, 12.68 | within noise |
| dense 30 x 784 downstream / rust | 23.79 (23.71-24.13) | 6.494 (6.298-6.656) | -72.7% | 23.94, 23.73, 23.9 / 6.32, 6.488, 6.646 | consistent |
| dense 30 x 784 hidden_delta / numpy | 17.11 (16.92-17.42) | 17.07 (17-17.1) | -0.3% | 16.96, 17.12, 17.27 / 17.06, 17.05, 17.07 | within noise |
| dense 30 x 784 hidden_delta / rust | 24.66 (24.56-24.76) | 7.318 (7.184-7.586) | -70.3% | 24.66, 24.68, 24.66 / 7.31, 7.193, 7.532 | consistent |
| dense 30 x 784 accumulate_gradient / numpy | 42.76 (42.71-43.44) | 42.7 (42.62-42.8) | -0.1% | 42.85, 43.08, 42.74 / 42.69, 42.72, 42.71 | separated, inside spread |
| dense 30 x 784 accumulate_gradient / rust | 9.943 (9.705-9.967) | 9.875 (9.845-9.908) | -0.7% | 9.922, 9.83, 9.955 / 9.875, 9.866, 9.888 | within noise |
| dense 30 x 784 apply_accumulated_gradient / numpy | 61.19 (61.06-61.53) | 61.22 (61.14-61.56) | +0.0% | 61.25, 61.12, 61.38 / 61.24, 61.35, 61.17 | within noise |
| dense 30 x 784 apply_accumulated_gradient / rust | 36.62 (36.48-36.79) | 36.41 (36.37-36.68) | -0.6% | 36.64, 36.53, 36.72 / 36.54, 36.42, 36.41 | within noise |
| dense 30 x 784 sgd step / numpy | 108.2 (107.7-116) | 108 (107.8-108.2) | -0.2% | 108, 108.1, 112.1 / 108.1, 107.8, 108 | within noise |
| dense 30 x 784 sgd step / rust | 15.71 (15.65-15.89) | 15.71 (15.65-15.72) | -0.0% | 15.71, 15.74, 15.77 / 15.71, 15.69, 15.68 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 92.81 (91.2-545.4) | 453.2 (90.77-461.9) | +388.3% | 319.1, 91.67, 274.3 / 454.8, 457.9, 91.28 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 724.9 (724.6-725.2) | 724.9 (724.8-725.2) | +0.0% | 725, 724.8, 724.8 / 724.9, 725.1, 724.9 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 2501 (2385-2830) | 2484 (2203-2710) | -0.7% | 2451, 2692, 2480 / 2482, 2485, 2397 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 3233 (3223-6035) | 3231 (3221-3239) | -0.1% | 4637, 3225, 3232 / 3235, 3234, 3224 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 58.18 (56.86-392.7) | 57.66 (56.76-389.1) | -0.9% | 58.11, 225.2, 223.1 / 223.7, 57.02, 57.47 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 747.3 (743.7-752.4) | 127 (125.6-128.1) | -83.0% | 748.1, 751, 743.9 / 127, 126.9, 127 | consistent |
| dense 30 x 784 downstream_batch b512 / numpy | 3358 (2824-4119) | 4101 (3024-4159) | +22.1% | 3802, 3027, 3289 / 3806, 3571, 4123 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 3518 (3512-3526) | 2011 (1561-2430) | -42.8% | 3521, 3515, 3519 / 1995, 2115, 1818 | consistent |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 105.3 (105.1-105.8) | 199.9 (105-295) | +89.8% | 105.6, 105.4, 105.2 / 294.7, 105.2, 200 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / rust | 782.8 (774.1-957.1) | 153.3 (148.8-307.5) | -80.4% | 777.1, 787.3, 868.7 / 151.6, 151.1, 305.7 | consistent |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 9393 (8140-1.24e+04) | 9849 (9326-1.108e+04) | +4.9% | 9842, 1.107e+04, 8590 / 9388, 1.006e+04, 1.059e+04 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / rust | 4884 (4653-4988) | 3481 (2709-3914) | -28.7% | 4938, 4767, 4825 / 3491, 3155, 3548 | consistent |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 263.5 (86.09-447.8) | 449.1 (445.4-456.1) | +70.4% | 263.6, 263.5, 266.9 / 450.5, 445.4, 452.2 | consistent |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 760 (757.2-761) | 140 (139.3-141.4) | -81.6% | 759.1, 759, 760.1 / 140.6, 140.2, 139.7 | consistent |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 1886 (1824-2209) | 2081 (1815-2277) | +10.3% | 1953, 2043, 1860 / 1955, 2195, 1969 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 1.016e+04 (8573-1.072e+04) | 2650 (2315-2770) | -73.9% | 9645, 9623, 1.058e+04 / 2542, 2574, 2655 | consistent |
| dense 10 x 30 forward / numpy | 8.247 (8.144-8.41) | 8.136 (8.091-8.187) | -1.3% | 8.184, 8.342, 8.211 / 8.143, 8.136, 8.136 | separated, inside spread |
| dense 10 x 30 forward / rust | 0.8546 (0.8482-0.8688) | 0.8583 (0.8564-0.8822) | +0.4% | 0.8499, 0.8555, 0.8628 / 0.8566, 0.8704, 0.8585 | within noise |
| dense 10 x 30 downstream / numpy | 1.827 (1.806-1.843) | 1.821 (1.817-1.832) | -0.3% | 1.829, 1.819, 1.824 / 1.817, 1.822, 1.827 | within noise |
| dense 10 x 30 downstream / rust | 0.6166 (0.6137-0.6227) | 0.414 (0.4098-0.4188) | -32.9% | 0.6204, 0.6176, 0.6149 / 0.4108, 0.4183, 0.4134 | consistent |
| dense 10 x 30 hidden_delta / numpy | 4.524 (4.508-4.573) | 4.538 (4.517-4.605) | +0.3% | 4.524, 4.539, 4.541 / 4.543, 4.564, 4.528 | within noise |
| dense 10 x 30 hidden_delta / rust | 1.041 (1.026-1.051) | 0.8241 (0.821-0.84) | -20.9% | 1.04, 1.05, 1.031 / 0.8233, 0.8312, 0.8289 | consistent |
| dense 10 x 30 accumulate_gradient / numpy | 5.284 (5.254-5.462) | 5.274 (5.244-5.393) | -0.2% | 5.295, 5.375, 5.259 / 5.323, 5.248, 5.301 | within noise |
| dense 10 x 30 accumulate_gradient / rust | 0.7856 (0.7682-0.7982) | 0.787 (0.78-0.7939) | +0.2% | 0.7856, 0.7749, 0.7929 / 0.7892, 0.7851, 0.787 | within noise |
| dense 10 x 30 apply_accumulated_gradient / numpy | 8.926 (8.871-9.138) | 8.894 (8.825-9.137) | -0.4% | 8.926, 8.923, 9.012 / 8.93, 8.857, 9.015 | within noise |
| dense 10 x 30 apply_accumulated_gradient / rust | 4.164 (4.151-4.203) | 4.159 (4.137-4.206) | -0.1% | 4.165, 4.177, 4.164 / 4.156, 4.163, 4.173 | within noise |
| dense 10 x 30 sgd step / numpy | 15.08 (15.02-15.3) | 15.02 (14.87-15.07) | -0.4% | 15.05, 15.29, 15.06 / 15.05, 14.94, 15.04 | separated, inside spread |
| dense 10 x 30 sgd step / rust | 0.911 (0.905-0.9152) | 0.9236 (0.9225-0.9355) | +1.4% | 0.9101, 0.9125, 0.9091 / 0.9236, 0.9282, 0.9294 | consistent |
| dense 10 x 30 forward_batch b32 / numpy | 19.45 (19.35-19.61) | 19.5 (19.46-19.6) | +0.2% | 19.48, 19.43, 19.48 / 19.53, 19.51, 19.5 | separated, inside spread |
| dense 10 x 30 forward_batch b32 / rust | 15.24 (15.16-15.34) | 15.26 (15.24-15.32) | +0.1% | 15.17, 15.34, 15.24 / 15.29, 15.26, 15.25 | within noise |
| dense 10 x 30 forward_batch b512 / numpy | 151.7 (150.7-152.6) | 151.6 (150.8-152) | -0.1% | 151.4, 152.2, 151.2 / 151.6, 151.5, 151.4 | within noise |
| dense 10 x 30 forward_batch b512 / rust | 234.4 (234-235.3) | 234.2 (234-234.4) | -0.1% | 234.6, 234.6, 234.2 / 234.3, 234.2, 234.2 | within noise |
| dense 10 x 30 downstream_batch b32 / numpy | 5.931 (5.909-5.995) | 5.909 (5.885-5.97) | -0.4% | 5.924, 5.971, 5.917 / 5.937, 5.915, 5.899 | within noise |
| dense 10 x 30 downstream_batch b32 / rust | 10.75 (10.74-10.75) | 3.847 (3.844-3.853) | -64.2% | 10.75, 10.75, 10.75 / 3.848, 3.847, 3.847 | consistent |
| dense 10 x 30 downstream_batch b512 / numpy | 64.77 (64.57-64.82) | 64.59 (64.47-64.73) | -0.3% | 64.8, 64.7, 64.69 / 64.59, 64.52, 64.72 | within noise |
| dense 10 x 30 downstream_batch b512 / rust | 166.8 (166.7-166.8) | 56.21 (55.75-56.35) | -66.3% | 166.8, 166.7, 166.7 / 56.34, 56.04, 56.04 | consistent |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 10.49 (10.35-10.61) | 10.45 (10.39-10.49) | -0.3% | 10.36, 10.6, 10.49 / 10.44, 10.43, 10.46 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 11.63 (11.61-11.63) | 4.747 (4.716-4.799) | -59.2% | 11.63, 11.62, 11.62 / 4.731, 4.74, 4.775 | consistent |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 93.7 (92.2-96.22) | 94.19 (93.02-95.76) | +0.5% | 94.21, 94.53, 93.7 / 94.66, 93.74, 94.39 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / rust | 176.3 (175.7-188.1) | 65.23 (64.65-65.53) | -63.0% | 176, 176.6, 182.1 / 65.06, 65.47, 64.96 | consistent |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 9.583 (9.545-9.689) | 9.6 (9.524-9.751) | +0.2% | 9.583, 9.588, 9.617 / 9.534, 9.6, 9.695 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 10.44 (10.42-10.45) | 4.578 (4.562-4.584) | -56.1% | 10.44, 10.43, 10.44 / 4.582, 4.578, 4.562 | consistent |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 47.62 (47.37-47.82) | 47.75 (47.56-48.51) | +0.3% | 47.61, 47.54, 47.72 / 47.6, 48.1, 47.87 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 149.9 (149.3-150.2) | 58.97 (58.72-59.02) | -60.6% | 149.9, 150.1, 149.4 / 59.02, 58.94, 58.86 | consistent |
| conv 28x28, 8 ch forward / numpy | 85.29 (84.86-86.89) | 85.75 (85.45-86.66) | +0.5% | 85.63, 85.17, 86.12 / 85.63, 86.34, 85.59 | within noise |
| conv 28x28, 8 ch forward / rust | 75.36 (75.33-75.41) | 51.63 (51.63-51.67) | -31.5% | 75.39, 75.37, 75.34 / 51.65, 51.63, 51.64 | consistent |
| conv 28x28, 8 ch downstream / numpy | 71.03 (70.36-72.74) | 71.49 (70.86-72.64) | +0.6% | 71.9, 71.64, 70.68 / 72.23, 71.02, 71.49 | within noise |
| conv 28x28, 8 ch downstream / rust | 72.09 (72.06-72.11) | 49.65 (49.62-49.67) | -31.1% | 72.09, 72.09, 72.09 / 49.63, 49.64, 49.66 | consistent |
| conv 28x28, 8 ch accumulate_gradient / numpy | 60.9 (60.18-61.81) | 59.08 (57.74-61.28) | -3.0% | 60.8, 61.17, 60.97 / 59.2, 59.56, 58.96 | consistent |
| conv 28x28, 8 ch accumulate_gradient / rust | 51 (50.97-51.03) | 30.23 (30.15-30.29) | -40.7% | 50.99, 50.99, 51.01 / 30.23, 30.22, 30.24 | consistent |
| conv 28x28, 8 ch forward_batch b32 / numpy | 4416 (3939-4686) | 4570 (4445-4796) | +3.5% | 4218, 4312, 4660 / 4539, 4508, 4750 | within noise |
| conv 28x28, 8 ch forward_batch b32 / rust | 2686 (2491-2774) | 1776 (1745-2104) | -33.9% | 2675, 2695, 2632 / 1764, 1861, 1937 | consistent |
| conv 28x28, 8 ch forward_batch b512 / numpy | 7.647e+04 (7.551e+04-9.29e+04) | 7.535e+04 (7.408e+04-7.715e+04) | -1.5% | 7.647e+04, 8.422e+04, 7.626e+04 / 7.562e+04, 7.477e+04, 7.56e+04 | separated, inside spread |
| conv 28x28, 8 ch forward_batch b512 / rust | 4.959e+04 (4.766e+04-5.15e+04) | 3.787e+04 (3.645e+04-3.975e+04) | -23.6% | 4.859e+04, 5.146e+04, 4.948e+04 / 3.732e+04, 3.81e+04, 3.809e+04 | consistent |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 1601 (1483-2056) | 1562 (1503-1599) | -2.4% | 1553, 1817, 1606 / 1534, 1556, 1588 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / rust | 3054 (2678-5046) | 2857 (2338-3258) | -6.5% | 2803, 4217, 2959 / 2712, 2682, 3136 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 5.825e+04 (5.683e+04-6.08e+04) | 5.898e+04 (5.575e+04-5.972e+04) | +1.3% | 6.072e+04, 5.82e+04, 5.733e+04 / 5.752e+04, 5.846e+04, 5.92e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / rust | 4.619e+04 (4.467e+04-4.677e+04) | 5.982e+04 (5.709e+04-6.13e+04) | +29.5% | 4.572e+04, 4.62e+04, 4.619e+04 / 5.906e+04, 5.982e+04, 5.928e+04 | consistent |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 2251 (2248-2370) | 2301 (2246-2322) | +2.2% | 2309, 2299, 2251 / 2287, 2282, 2302 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 1823 (1818-1865) | 1162 (1122-1525) | -36.3% | 1843, 1822, 1837 / 1159, 1162, 1324 | consistent |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 3.815e+04 (3.712e+04-3.834e+04) | 3.764e+04 (3.718e+04-4.171e+04) | -1.3% | 3.771e+04, 3.822e+04, 3.771e+04 / 3.762e+04, 3.946e+04, 3.769e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 4.091e+04 (3.834e+04-4.397e+04) | 3.135e+04 (2.787e+04-3.515e+04) | -23.4% | 4.115e+04, 4.091e+04, 4.148e+04 / 3.198e+04, 3.151e+04, 3.13e+04 | consistent |
| conv 8x8, 8 ch forward / numpy | 34.96 (34.64-35.22) | 34.94 (34.43-36.46) | -0.1% | 35.04, 34.86, 34.93 / 34.94, 35.2, 35.44 | within noise |
| conv 8x8, 8 ch forward / rust | 4.938 (4.927-4.951) | 3.666 (3.65-3.67) | -25.8% | 4.943, 4.938, 4.937 / 3.665, 3.657, 3.668 | consistent |
| conv 8x8, 8 ch downstream / numpy | 39.99 (39.39-41.02) | 40.08 (39.51-40.61) | +0.2% | 39.8, 39.92, 40.44 / 40.03, 39.8, 40.34 | within noise |
| conv 8x8, 8 ch downstream / rust | 4.356 (4.353-4.361) | 3.186 (3.177-3.254) | -26.9% | 4.359, 4.359, 4.355 / 3.185, 3.221, 3.181 | consistent |
| conv 8x8, 8 ch accumulate_gradient / numpy | 12.49 (12.33-12.61) | 12.55 (12.4-12.86) | +0.5% | 12.43, 12.56, 12.41 / 12.6, 12.55, 12.63 | within noise |
| conv 8x8, 8 ch accumulate_gradient / rust | 3.508 (3.501-3.516) | 2.31 (2.305-2.312) | -34.1% | 3.511, 3.505, 3.51 / 2.31, 2.309, 2.308 | consistent |
| conv 8x8, 8 ch forward_batch b32 / numpy | 130.7 (128.9-131.5) | 129.5 (128.8-148.4) | -1.0% | 129, 131.3, 130.8 / 130.1, 139, 129.1 | within noise |
| conv 8x8, 8 ch forward_batch b32 / rust | 128.9 (128.8-129.1) | 88.4 (88.33-88.72) | -31.4% | 128.8, 129.1, 128.9 / 88.56, 88.36, 88.55 | consistent |
| conv 8x8, 8 ch forward_batch b512 / numpy | 4101 (3502-4541) | 3450 (3303-4762) | -15.9% | 3831, 3913, 4293 / 3577, 4124, 3358 | within noise |
| conv 8x8, 8 ch forward_batch b512 / rust | 2332 (2227-2666) | 1818 (1579-1982) | -22.1% | 2255, 2327, 2525 / 1825, 1781, 1804 | consistent |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 115.9 (115-125.3) | 116 (115.1-117.6) | +0.1% | 120.3, 115.4, 116.1 / 115.6, 116.4, 116.8 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / rust | 123.8 (123.8-124.6) | 85.55 (85.45-85.61) | -30.9% | 123.8, 123.8, 124.3 / 85.55, 85.57, 85.52 | consistent |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 1611 (1585-1941) | 1918 (1591-2067) | +19.1% | 1775, 1592, 1764 / 2008, 1828, 1739 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / rust | 2749 (2468-3177) | 1941 (1702-2384) | -29.4% | 2619, 2849, 2753 / 2043, 1941, 1908 | consistent |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 150.7 (148.1-153.7) | 148.7 (148.1-153.7) | -1.3% | 148.2, 152.2, 151.9 / 148.3, 151.2, 148.9 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 87.3 (87.29-87.46) | 51.96 (51.86-52.06) | -40.5% | 87.38, 87.37, 87.29 / 51.94, 52.01, 51.95 | consistent |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 2348 (2293-2420) | 2352 (2296-2374) | +0.2% | 2400, 2302, 2356 / 2354, 2370, 2298 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 1699 (1551-1855) | 992.5 (976.5-1262) | -41.6% | 1849, 1694, 1559 / 1118, 1129, 982.5 | consistent |
| conv 13x13x8, 8 ch forward / numpy | 79.78 (79.54-81.05) | 80.12 (80.02-81.11) | +0.4% | 79.63, 79.85, 80.38 / 80.1, 80.1, 80.6 | within noise |
| conv 13x13x8, 8 ch forward / rust | 82 (81.95-82.14) | 51.37 (51.34-51.61) | -37.4% | 82.08, 81.97, 82.01 / 51.36, 51.49, 51.48 | consistent |
| conv 13x13x8, 8 ch downstream / numpy | 88.94 (88.59-89.6) | 89.82 (89.36-90.22) | +1.0% | 89.32, 88.71, 89 / 89.89, 89.72, 89.78 | separated, inside spread |
| conv 13x13x8, 8 ch downstream / rust | 95.53 (95.39-95.57) | 34.19 (33.96-34.37) | -64.2% | 95.55, 95.46, 95.47 / 34.08, 34.08, 34.31 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 40.6 (39.97-41.1) | 40.4 (40.21-40.99) | -0.5% | 40.81, 40.77, 40.07 / 40.49, 40.64, 40.3 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 63.87 (63.84-64.12) | 14.84 (14.8-14.88) | -76.8% | 63.85, 63.86, 64.02 / 14.81, 14.88, 14.84 | consistent |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 2607 (2486-2950) | 2586 (2440-2643) | -0.8% | 2762, 2572, 2582 / 2497, 2576, 2632 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 3445 (3173-3708) | 2364 (2171-2624) | -31.4% | 3394, 3474, 3478 / 2403, 2339, 2398 | consistent |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 5.197e+04 (4.967e+04-5.267e+04) | 5.306e+04 (5.187e+04-5.526e+04) | +2.1% | 5.107e+04, 5.197e+04, 5.196e+04 / 5.319e+04, 5.366e+04, 5.306e+04 | consistent |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 6.85e+04 (6.745e+04-6.92e+04) | 5.594e+04 (5.228e+04-5.961e+04) | -18.3% | 6.812e+04, 6.832e+04, 6.859e+04 / 5.485e+04, 5.704e+04, 5.572e+04 | consistent |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 4336 (4042-6516) | 4185 (3983-4434) | -3.5% | 5474, 4185, 4236 / 4189, 4212, 4155 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 3332 (3284-3413) | 1379 (1324-1451) | -58.6% | 3386, 3292, 3332 / 1362, 1423, 1351 | consistent |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 1.233e+05 (1.191e+05-1.257e+05) | 1.225e+05 (1.188e+05-1.259e+05) | -0.7% | 1.224e+05, 1.234e+05, 1.226e+05 / 1.232e+05, 1.224e+05, 1.225e+05 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 3.753e+04 (3.534e+04-3.878e+04) | 5.696e+04 (5.266e+04-6.262e+04) | +51.8% | 3.741e+04, 3.76e+04, 3.647e+04 / 5.738e+04, 5.484e+04, 5.976e+04 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 1125 (1123-1138) | 1139 (1126-1146) | +1.2% | 1124, 1133, 1124 / 1138, 1140, 1136 | separated, inside spread |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 2178 (2160-2184) | 608.1 (592-610.8) | -72.1% | 2172, 2173, 2178 / 609.8, 607.7, 599.4 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.835e+04 (1.829e+04-1.874e+04) | 1.838e+04 (1.837e+04-1.87e+04) | +0.2% | 1.83e+04, 1.871e+04, 1.835e+04 / 1.841e+04, 1.853e+04, 1.837e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 2.313e+04 (2.168e+04-2.322e+04) | 1.26e+04 (1.147e+04-1.37e+04) | -45.5% | 2.319e+04, 2.215e+04, 2.315e+04 / 1.287e+04, 1.158e+04, 1.34e+04 | consistent |
| conv 26x26x8/2, 8 ch forward / numpy | 90.36 (89.71-91.02) | 90.11 (89.44-90.58) | -0.3% | 90.57, 89.85, 90.75 / 89.8, 89.85, 90.57 | within noise |
| conv 26x26x8/2, 8 ch forward / rust | 97.43 (97.34-97.72) | 61.07 (61-61.45) | -37.3% | 97.47, 97.58, 97.37 / 61.03, 61.07, 61.35 | consistent |
| conv 26x26x8/2, 8 ch downstream / numpy | 104.1 (103.3-105.8) | 103.7 (102.8-104.7) | -0.4% | 104.9, 103.4, 104.5 / 103.7, 103.7, 103.5 | within noise |
| conv 26x26x8/2, 8 ch downstream / rust | 113.9 (113.8-114) | 40.7 (40.65-41.06) | -64.3% | 113.9, 113.8, 114 / 40.87, 40.67, 40.87 | consistent |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 47.89 (47.6-48.32) | 47.67 (47.43-48.27) | -0.5% | 47.69, 47.85, 48.16 / 47.91, 47.58, 47.69 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 76.44 (76.4-76.53) | 17.45 (17.39-17.49) | -77.2% | 76.4, 76.48, 76.47 / 17.47, 17.42, 17.47 | consistent |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 3498 (3095-3770) | 3537 (3395-3956) | +1.1% | 3459, 3622, 3308 / 3467, 3864, 3504 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 4256 (4062-4472) | 3229 (2913-3268) | -24.1% | 4267, 4400, 4114 / 3110, 3058, 3257 | consistent |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 6.666e+04 (6.568e+04-6.928e+04) | 6.875e+04 (6.631e+04-7.163e+04) | +3.1% | 6.574e+04, 6.666e+04, 6.845e+04 / 6.818e+04, 6.75e+04, 7.084e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 8.827e+04 (8.243e+04-8.908e+04) | 6.966e+04 (6.802e+04-7.159e+04) | -21.1% | 8.725e+04, 8.907e+04, 8.521e+04 / 6.896e+04, 6.926e+04, 7.05e+04 | consistent |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 8391 (7626-1.039e+04) | 8955 (8502-9235) | +6.7% | 8391, 8493, 9007 / 8981, 8720, 8971 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 5473 (4904-5740) | 3217 (2691-4048) | -41.2% | 5627, 4953, 5572 / 2953, 3192, 3640 | consistent |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 1.995e+05 (1.972e+05-2.007e+05) | 1.986e+05 (1.88e+05-2.015e+05) | -0.4% | 1.985e+05, 1.999e+05, 1.996e+05 / 1.994e+05, 1.947e+05, 1.986e+05 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 5.617e+04 (5.362e+04-5.989e+04) | 8.234e+04 (7.821e+04-8.702e+04) | +46.6% | 5.685e+04, 5.69e+04, 5.574e+04 / 7.987e+04, 8.124e+04, 8.555e+04 | consistent |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 1384 (1373-1399) | 1388 (1375-1406) | +0.3% | 1387, 1386, 1379 / 1384, 1403, 1380 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 2624 (2618-3038) | 781.1 (681.1-792.6) | -70.2% | 2831, 2621, 2621 / 731.1, 786.2, 737.6 | consistent |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 2.229e+04 (2.221e+04-2.343e+04) | 2.264e+04 (2.229e+04-2.303e+04) | +1.6% | 2.292e+04, 2.229e+04, 2.222e+04 / 2.233e+04, 2.303e+04, 2.264e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 2.659e+04 (2.623e+04-2.82e+04) | 1.713e+04 (1.6e+04-1.833e+04) | -35.6% | 2.657e+04, 2.722e+04, 2.713e+04 / 1.717e+04, 1.713e+04, 1.73e+04 | consistent |
| conv 26x26x8, 8 ch forward / numpy | 245.4 (244.4-246.2) | 244.1 (243.9-244.7) | -0.5% | 245.5, 245.3, 245.4 / 244, 244.3, 244.3 | consistent |
| conv 26x26x8, 8 ch forward / rust | 384 (383.1-385.1) | 238.9 (237.6-252.3) | -37.8% | 384.3, 384.4, 383.4 / 245.6, 238.4, 238.3 | consistent |
| conv 26x26x8, 8 ch downstream / numpy | 257.1 (254.7-257.5) | 255.1 (253.3-259.1) | -0.8% | 257.4, 256.3, 255.9 / 256, 257, 253.8 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 450.4 (450.3-450.7) | 158.6 (157.3-159.1) | -64.8% | 450.4, 450.6, 450.4 / 158, 158.8, 158 | consistent |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 160.2 (157.3-161.7) | 161.1 (156.8-163.7) | +0.6% | 159.5, 160.7, 160.1 / 160.2, 161.1, 160.6 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 299 (298.7-299.4) | 65.15 (64.74-65.3) | -78.2% | 298.9, 298.9, 299.1 / 65.02, 65.15, 65.16 | consistent |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 1.482e+04 (1.275e+04-1.658e+04) | 1.483e+04 (1.347e+04-1.705e+04) | +0.0% | 1.637e+04, 1.371e+04, 1.417e+04 / 1.411e+04, 1.54e+04, 1.594e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 1.712e+04 (1.645e+04-1.844e+04) | 1.27e+04 (1.224e+04-1.415e+04) | -25.8% | 1.763e+04, 1.654e+04, 1.788e+04 / 1.308e+04, 1.32e+04, 1.269e+04 | consistent |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 2.553e+05 (2.455e+05-3.562e+05) | 2.769e+05 (2.585e+05-3.201e+05) | +8.5% | 2.612e+05, 3.049e+05, 2.458e+05 / 2.997e+05, 2.926e+05, 2.617e+05 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 3.19e+05 (3.173e+05-3.273e+05) | 2.442e+05 (2.425e+05-2.554e+05) | -23.4% | 3.196e+05, 3.229e+05, 3.184e+05 / 2.483e+05, 2.489e+05, 2.438e+05 | consistent |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 2.661e+04 (2.45e+04-2.834e+04) | 2.766e+04 (2.545e+04-2.885e+04) | +4.0% | 2.741e+04, 2.597e+04, 2.642e+04 / 2.708e+04, 2.715e+04, 2.766e+04 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 9732 (8949-1.005e+04) | 1.561e+04 (1.313e+04-1.798e+04) | +60.4% | 9636, 9732, 9445 / 1.56e+04, 1.641e+04, 1.556e+04 | consistent |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 5.397e+05 (5.281e+05-5.554e+05) | 5.436e+05 (5.389e+05-5.726e+05) | +0.7% | 5.475e+05, 5.443e+05, 5.34e+05 / 5.456e+05, 5.431e+05, 5.562e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 1.85e+05 (1.798e+05-1.864e+05) | 3.046e+05 (2.977e+05-3.178e+05) | +64.7% | 1.854e+05, 1.804e+05, 1.858e+05 / 3.046e+05, 3.11e+05, 3.034e+05 | consistent |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 5625 (5581-5651) | 5659 (5636-5686) | +0.6% | 5638, 5602, 5620 / 5661, 5648, 5662 | separated, inside spread |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 6089 (5901-7326) | 3512 (3441-3848) | -42.3% | 6001, 6771, 6034 / 3680, 3584, 3453 | consistent |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 8.947e+04 (8.87e+04-9.146e+04) | 8.899e+04 (8.876e+04-9.057e+04) | -0.5% | 9.012e+04, 8.909e+04, 8.957e+04 / 8.957e+04, 8.968e+04, 8.88e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 1.073e+05 (1.06e+05-1.084e+05) | 6.296e+04 (5.856e+04-6.565e+04) | -41.3% | 1.075e+05, 1.075e+05, 1.067e+05 / 5.99e+04, 6.407e+04, 6.392e+04 | consistent |
| pool 26x26, 8 ch forward / numpy | 105.6 (105.3-106) | 105.7 (104.9-117.6) | +0.0% | 105.5, 105.6, 105.8 / 105.7, 111.6, 105.5 | within noise |
| pool 26x26, 8 ch forward / rust | 5.204 (5.193-5.238) | 5.222 (5.208-5.241) | +0.3% | 5.212, 5.201, 5.221 / 5.221, 5.221, 5.231 | within noise |
| pool 26x26, 8 ch downstream / numpy | 55.21 (54.82-55.99) | 55.38 (54.55-55.95) | +0.3% | 55.55, 55.23, 55.01 / 55.25, 55.38, 55.29 | within noise |
| pool 26x26, 8 ch downstream / rust | 4.294 (4.281-4.319) | 4.302 (4.281-4.33) | +0.2% | 4.307, 4.288, 4.294 / 4.296, 4.321, 4.29 | within noise |
| pool 26x26, 8 ch forward_batch b32 / numpy | 2465 (2402-2505) | 2444 (2398-3208) | -0.8% | 2465, 2483, 2437 / 2402, 2444, 2838 | within noise |
| pool 26x26, 8 ch forward_batch b32 / rust | 228.4 (208.2-240.8) | 229.4 (194.3-264.8) | +0.4% | 218.1, 230.4, 230.5 / 230.8, 250.6, 208.3 | within noise |
| pool 26x26, 8 ch forward_batch b512 / numpy | 4.08e+04 (4.052e+04-4.177e+04) | 4.191e+04 (4.027e+04-4.394e+04) | +2.7% | 4.065e+04, 4.13e+04, 4.103e+04 / 4.112e+04, 4.247e+04, 4.289e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 9504 (8651-1.066e+04) | 9463 (9103-1.04e+04) | -0.4% | 9763, 1.038e+04, 8674 / 9753, 9410, 9725 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 991.1 (971.3-1553) | 987.4 (957.2-1462) | -0.4% | 992.5, 1262, 988.1 / 974, 980.3, 1223 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / rust | 134.7 (134.2-486.4) | 134.4 (134.2-488.8) | -0.2% | 310.4, 134.4, 302.8 / 311.5, 134.3, 308.6 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 6.207e+04 (5.883e+04-6.524e+04) | 6.115e+04 (5.837e+04-6.346e+04) | -1.5% | 6.236e+04, 6.044e+04, 6.366e+04 / 5.924e+04, 6.115e+04, 6.29e+04 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / rust | 2.089e+04 (2.052e+04-2.315e+04) | 2.167e+04 (2.002e+04-2.456e+04) | +3.8% | 2.074e+04, 2.198e+04, 2.142e+04 / 2.215e+04, 2.229e+04, 2.156e+04 | within noise |
| pool 6x6, 8 ch forward / numpy | 39.66 (39.34-40.83) | 39.71 (38.82-39.89) | +0.1% | 39.58, 40.25, 39.53 / 39.24, 39.83, 39.74 | within noise |
| pool 6x6, 8 ch forward / rust | 0.7647 (0.7632-0.7708) | 0.7656 (0.7622-0.7811) | +0.1% | 0.764, 0.7675, 0.7651 / 0.7654, 0.7718, 0.7658 | within noise |
| pool 6x6, 8 ch downstream / numpy | 32.56 (32.27-32.68) | 32.56 (32.44-32.72) | -0.0% | 32.58, 32.41, 32.47 / 32.67, 32.57, 32.48 | within noise |
| pool 6x6, 8 ch downstream / rust | 0.8164 (0.8012-0.8459) | 0.8225 (0.8002-0.8793) | +0.7% | 0.825, 0.8257, 0.807 / 0.8449, 0.8482, 0.8124 | within noise |
| pool 6x6, 8 ch forward_batch b32 / numpy | 167.8 (167.2-168.9) | 168.3 (167.2-169.1) | +0.3% | 168, 168.4, 167.4 / 168.9, 167.5, 168.3 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 10.46 (10.43-10.55) | 10.48 (10.41-10.54) | +0.3% | 10.46, 10.44, 10.49 / 10.49, 10.53, 10.43 | within noise |
| pool 6x6, 8 ch forward_batch b512 / numpy | 2200 (2179-2284) | 2248 (2200-2572) | +2.1% | 2215, 2234, 2200 / 2242, 2386, 2400 | separated, inside spread |
| pool 6x6, 8 ch forward_batch b512 / rust | 164 (163.4-174.7) | 166 (163.5-174.4) | +1.2% | 163.7, 169.4, 167.7 / 163.6, 166.5, 171.4 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 85.26 (84.67-86.55) | 85.14 (84.91-86.22) | -0.1% | 85.61, 85.72, 85.02 / 85.28, 85.14, 85.57 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / rust | 12.22 (12.06-12.38) | 12.14 (12.07-12.32) | -0.7% | 12.09, 12.37, 12.2 / 12.09, 12.22, 12.22 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 945.7 (933.9-954.2) | 937.9 (935.3-950.4) | -0.8% | 942.2, 947.6, 943.6 / 946, 937.8, 936.6 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 196 (195.7-197.9) | 196.7 (196-444.4) | +0.4% | 196.8, 196, 196 / 196.3, 196.5, 322.2 | within noise |
| conv tail 32 x 5408 bare downstream b32 / numpy | 1546 (1094-1615) | 1464 (1245-1519) | -5.3% | 1105, 1549, 1594 / 1447, 1370, 1474 | within noise |
| conv tail 32 x 5408 bare downstream b32 / rust | 7431 (7229-7562) | 1338 (1191-1662) | -82.0% | 7440, 7424, 7384 / 1338, 1426, 1418 | consistent |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3.627e+04 (2.862e+04-4.623e+04) | 4.005e+04 (2.92e+04-4.595e+04) | +10.4% | 4.436e+04, 3.092e+04, 3.482e+04 / 3.734e+04, 4.005e+04, 4.095e+04 | within noise |
| conv tail 32 x 5408 bare downstream b512 / rust | 3.967e+04 (3.657e+04-4.868e+04) | 2.241e+04 (1.664e+04-2.622e+04) | -43.5% | 4.31e+04, 4.175e+04, 3.715e+04 / 1.694e+04, 2.406e+04, 2.36e+04 | consistent |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 1236 (929.9-1541) | 1277 (1042-1631) | +3.3% | 1350, 1382, 1090 / 1270, 1203, 1411 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / rust | 7308 (6960-7514) | 1211 (1175-1366) | -83.4% | 7161, 7393, 7237 / 1187, 1289, 1223 | consistent |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 2.541e+04 (2.419e+04-2.726e+04) | 2.596e+04 (2.48e+04-2.939e+04) | +2.2% | 2.573e+04, 2.504e+04, 2.586e+04 / 2.54e+04, 2.581e+04, 2.856e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / rust | 1.109e+05 (9.501e+04-1.386e+05) | 1.956e+04 (1.893e+04-3.956e+04) | -82.4% | 1.107e+05, 1.248e+05, 1.055e+05 / 1.977e+04, 2.933e+04, 1.914e+04 | consistent |
| conv tail 32 x 5408 transpose b32 / numpy | 1.469 (1.457-1.662) | 1.47 (1.464-1.481) | +0.0% | 1.47, 1.465, 1.564 / 1.468, 1.475, 1.468 | within noise |
| conv tail 32 x 5408 transpose b32 / rust | 1.922 (1.921-1.925) | 1.878 (1.874-1.879) | -2.3% | 1.922, 1.923, 1.922 / 1.878, 1.876, 1.878 | consistent |
| conv tail 32 x 5408 transpose b512 / numpy | 29.94 (29.68-30.09) | 29.99 (29.73-30.1) | +0.2% | 29.89, 29.94, 29.88 / 29.99, 29.87, 29.97 | within noise |
| conv tail 32 x 5408 transpose b512 / rust | 27.07 (27.01-27.16) | 26.55 (26.37-26.87) | -1.9% | 27.11, 27.09, 27.07 / 26.44, 26.69, 26.69 | consistent |
| conv tail 32 x 5408 add b32 / numpy | 322.9 (289-423.4) | 370.5 (319.9-443.4) | +14.7% | 306.9, 372.2, 342.7 / 340.8, 381.7, 401.8 | within noise |
| conv tail 32 x 5408 add b32 / rust | 440.9 (380.5-446.4) | 399.3 (333.8-550.6) | -9.4% | 442.5, 444.1, 380.6 / 494.2, 386.9, 353.6 | within noise |
| conv tail 32 x 5408 add b512 / numpy | 317.6 (308.4-416.4) | 416.5 (296.9-542.7) | +31.1% | 317.6, 413.8, 310.4 / 485.1, 356, 405 | within noise |
| conv tail 32 x 5408 add b512 / rust | 397.3 (312.7-427.6) | 374 (333.8-453.3) | -5.9% | 355.3, 365.4, 422.6 / 353.7, 388.7, 394.8 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 2.816 (2.804-2.858) | 2.821 (2.811-2.878) | +0.2% | 2.831, 2.815, 2.832 / 2.866, 2.818, 2.815 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.779 (0.7761-0.7828) | 0.7812 (0.7797-0.7834) | +0.3% | 0.7817, 0.7778, 0.7784 / 0.7818, 0.7827, 0.7801 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 16.03 (15.83-16.22) | 16.05 (15.78-16.28) | +0.1% | 16.08, 15.86, 16.16 / 16.03, 15.87, 16.26 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 8.676 (8.658-8.693) | 8.672 (8.657-8.68) | -0.1% | 8.676, 8.683, 8.671 / 8.676, 8.666, 8.667 | within noise |
| dense 30 x 784 bare downstream b32 / numpy | 57.77 (56.8-58.5) | 57.08 (56.54-58.09) | -1.2% | 57.83, 57.54, 57.65 / 57.67, 57.4, 56.65 | within noise |
| dense 30 x 784 bare downstream b32 / rust | 748.4 (745.5-752.7) | 126.6 (125.8-127.8) | -83.1% | 751.4, 746.8, 747.6 / 126.8, 126.6, 126.6 | consistent |
| dense 30 x 784 bare downstream b512 / numpy | 4001 (2808-4127) | 3382 (2784-4152) | -15.5% | 3431, 3468, 4021 / 3493, 3265, 3586 | within noise |
| dense 30 x 784 bare downstream b512 / rust | 3504 (3498-3536) | 1786 (1615-2572) | -49.0% | 3507, 3519, 3500 / 1665, 2152, 2157 | consistent |
| dense 30 x 784 bare accumulate b32 / numpy | 66.56 (65.57-389) | 66.8 (66-398.9) | +0.4% | 66.41, 227.8, 66.08 / 229.4, 232.9, 66.5 | within noise |
| dense 30 x 784 bare accumulate b32 / rust | 745 (742.3-746.5) | 125.9 (125.5-127) | -83.1% | 746.4, 743.6, 744.3 / 126.5, 126.3, 125.6 | consistent |
| dense 30 x 784 bare accumulate b512 / numpy | 1914 (1810-2075) | 1993 (1777-2152) | +4.1% | 2072, 1867, 1866 / 2107, 2005, 1833 | within noise |
| dense 30 x 784 bare accumulate b512 / rust | 9243 (8645-1.119e+04) | 2609 (2360-2670) | -71.8% | 9620, 9243, 9985 / 2515, 2555, 2635 | consistent |
| dense 30 x 784 transpose b32 / numpy | 1.4 (1.389-1.411) | 1.413 (1.4-1.43) | +0.9% | 1.4, 1.397, 1.403 / 1.413, 1.413, 1.415 | consistent |
| dense 30 x 784 transpose b32 / rust | 1.867 (1.865-1.872) | 1.822 (1.812-1.827) | -2.4% | 1.868, 1.869, 1.866 / 1.82, 1.822, 1.82 | consistent |
| dense 30 x 784 transpose b512 / numpy | 9.035 (9.001-9.328) | 9.019 (8.973-9.038) | -0.2% | 9.165, 9.035, 9.039 / 9.024, 9.002, 9.01 | separated, inside spread |
| dense 30 x 784 transpose b512 / rust | 25.65 (25.46-25.78) | 24.87 (24.73-25.05) | -3.1% | 25.66, 25.7, 25.57 / 25.02, 24.74, 24.89 | consistent |
| dense 30 x 784 add b32 / numpy | 10.46 (10.25-10.79) | 10.19 (10.03-10.43) | -2.6% | 10.68, 10.34, 10.45 / 10.05, 10.18, 10.43 | within noise |
| dense 30 x 784 add b32 / rust | 9.539 (9.438-11.68) | 9.726 (9.609-11.06) | +2.0% | 9.517, 10.68, 9.487 / 9.83, 10.39, 9.631 | within noise |
| dense 30 x 784 add b512 / numpy | 11.46 (11.25-12.17) | 11.27 (10.53-11.68) | -1.7% | 11.47, 11.45, 11.72 / 11.47, 11.39, 10.82 | within noise |
| dense 30 x 784 add b512 / rust | 9.678 (9.419-9.804) | 9.503 (9.389-9.644) | -1.8% | 9.538, 9.621, 9.751 / 9.456, 9.444, 9.594 | within noise |
| dense 30 x 784 sum_axis0 b32 / numpy | 2.799 (2.79-2.824) | 2.841 (2.798-2.868) | +1.5% | 2.807, 2.8, 2.799 / 2.834, 2.818, 2.86 | separated, inside spread |
| dense 30 x 784 sum_axis0 b32 / rust | 0.701 (0.6971-0.7055) | 0.7052 (0.7023-0.7272) | +0.6% | 0.6991, 0.7032, 0.7012 / 0.7052, 0.7153, 0.7052 | separated, inside spread |
| dense 30 x 784 sum_axis0 b512 / numpy | 15.41 (15.32-15.61) | 15.38 (15.33-16.04) | -0.2% | 15.33, 15.52, 15.5 / 15.4, 15.38, 15.68 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 7.436 (7.43-7.444) | 7.442 (7.428-7.446) | +0.1% | 7.439, 7.43, 7.438 / 7.437, 7.445, 7.435 | within noise |
| dense 10 x 30 bare downstream b32 / numpy | 5.888 (5.855-5.931) | 5.904 (5.883-5.919) | +0.3% | 5.87, 5.913, 5.874 / 5.906, 5.901, 5.9 | within noise |
| dense 10 x 30 bare downstream b32 / rust | 10.7 (10.7-10.71) | 3.803 (3.802-3.819) | -64.5% | 10.71, 10.71, 10.7 / 3.803, 3.811, 3.804 | consistent |
| dense 10 x 30 bare downstream b512 / numpy | 64.79 (64.64-64.98) | 64.5 (64.43-64.87) | -0.4% | 64.98, 64.7, 64.79 / 64.48, 64.58, 64.65 | separated, inside spread |
| dense 10 x 30 bare downstream b512 / rust | 166.7 (166.7-166.8) | 56.22 (55.67-56.25) | -66.3% | 166.7, 166.7, 166.7 / 56.24, 56.22, 55.8 | consistent |
| dense 10 x 30 bare accumulate b32 / numpy | 5.03 (5.006-5.115) | 5.064 (5.019-5.116) | +0.7% | 5.06, 5.024, 5.03 / 5.072, 5.062, 5.067 | separated, inside spread |
| dense 10 x 30 bare accumulate b32 / rust | 9.083 (9.082-9.087) | 3.283 (3.279-3.289) | -63.9% | 9.084, 9.083, 9.085 / 3.282, 3.286, 3.282 | consistent |
| dense 10 x 30 bare accumulate b512 / numpy | 32.58 (32.5-32.64) | 32.62 (32.49-32.83) | +0.1% | 32.62, 32.54, 32.56 / 32.67, 32.68, 32.57 | within noise |
| dense 10 x 30 bare accumulate b512 / rust | 136.2 (135.8-136.4) | 45.59 (45.55-45.68) | -66.5% | 136.2, 136.1, 136.2 / 45.62, 45.6, 45.59 | consistent |
| dense 10 x 30 transpose b32 / numpy | 0.8889 (0.8858-0.9032) | 0.8922 (0.8824-0.901) | +0.4% | 0.8952, 0.8868, 0.8908 / 0.8922, 0.8972, 0.8839 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.8165 (0.8108-0.8189) | 0.798 (0.7892-0.8065) | -2.3% | 0.8133, 0.8179, 0.817 / 0.8034, 0.7909, 0.798 | separated, inside spread |
| dense 10 x 30 transpose b512 / numpy | 3.401 (3.358-3.519) | 3.413 (3.375-3.568) | +0.3% | 3.451, 3.367, 3.439 / 3.488, 3.412, 3.399 | within noise |
| dense 10 x 30 transpose b512 / rust | 8.802 (8.751-8.852) | 8.575 (8.509-8.58) | -2.6% | 8.781, 8.832, 8.776 / 8.547, 8.576, 8.544 | consistent |
| dense 10 x 30 add b32 / numpy | 0.897 (0.8939-0.9144) | 0.8981 (0.895-0.9003) | +0.1% | 0.901, 0.9042, 0.8941 / 0.898, 0.8962, 0.8998 | within noise |
| dense 10 x 30 add b32 / rust | 0.3793 (0.3744-0.4124) | 0.3783 (0.3772-0.38) | -0.3% | 0.3981, 0.378, 0.3774 / 0.3783, 0.3772, 0.3797 | within noise |
| dense 10 x 30 add b512 / numpy | 0.9184 (0.9126-0.9219) | 0.9174 (0.9128-0.9248) | -0.1% | 0.9197, 0.9182, 0.9172 / 0.9166, 0.9188, 0.9179 | within noise |
| dense 10 x 30 add b512 / rust | 0.3988 (0.388-0.4068) | 0.3998 (0.3941-0.4076) | +0.3% | 0.4019, 0.3933, 0.4002 / 0.3969, 0.4038, 0.4008 | within noise |
| dense 10 x 30 sum_axis0 b32 / numpy | 2.467 (2.446-2.492) | 2.491 (2.447-2.525) | +1.0% | 2.467, 2.473, 2.467 / 2.485, 2.468, 2.511 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.5294 (0.5243-0.5366) | 0.5311 (0.5293-0.537) | +0.3% | 0.5289, 0.5305, 0.531 / 0.5318, 0.53, 0.5342 | within noise |
| dense 10 x 30 sum_axis0 b512 / numpy | 12.6 (12.16-12.64) | 12.6 (12.16-12.65) | -0.1% | 12.42, 12.63, 12.38 / 12.4, 12.63, 12.38 | within noise |
| dense 10 x 30 sum_axis0 b512 / rust | 4.65 (4.645-4.655) | 4.65 (4.646-4.659) | +0.0% | 4.654, 4.648, 4.65 / 4.651, 4.65, 4.655 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 747.7 (745.7-756.1) | 747.7 (746-1643) | +0.0% | 748.2, 751.8, 747.7 / 1196, 746.9, 747.4 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 3053 (3038-3056) | 2635 (2630-2639) | -13.7% | 3055, 3041, 3053 / 2634, 2638, 2634 | consistent |
| attention 16 x 32 forward_batch b512 / numpy | 2.634e+04 (2.485e+04-2.793e+04) | 2.528e+04 (2.318e+04-2.746e+04) | -4.1% | 2.533e+04, 2.634e+04, 2.741e+04 / 2.512e+04, 2.518e+04, 2.566e+04 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 2.786e+04 (2.765e+04-2.848e+04) | 2.108e+04 (2.085e+04-2.944e+04) | -24.3% | 2.796e+04, 2.818e+04, 2.773e+04 / 2.515e+04, 2.132e+04, 2.095e+04 | separated, inside spread |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 761.6 (757.1-764.4) | 758.1 (756.3-777.7) | -0.5% | 761.9, 760.8, 761 / 768.5, 756.5, 767.3 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / rust | 3212 (3210-3214) | 795.2 (790.5-796.5) | -75.2% | 3213, 3213, 3211 / 791.5, 796.2, 795.4 | consistent |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 3.078e+04 (2.792e+04-3.367e+04) | 3.022e+04 (2.832e+04-3.184e+04) | -1.8% | 3.296e+04, 3.078e+04, 2.841e+04 / 3.066e+04, 2.981e+04, 3.008e+04 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / rust | 3.49e+04 (3.353e+04-4.436e+04) | 2.062e+04 (1.873e+04-2.218e+04) | -40.9% | 3.511e+04, 3.487e+04, 3.894e+04 / 2.179e+04, 1.914e+04, 2.08e+04 | consistent |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 592.9 (580.4-596.4) | 590.4 (582.1-597) | -0.4% | 588.4, 590.6, 594.3 / 584.8, 590.8, 595.2 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 3817 (3814-3818) | 509.8 (503.9-514.4) | -86.6% | 3816, 3816, 3818 / 505.1, 509, 514.1 | consistent |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 4.466e+04 (3.47e+04-4.583e+04) | 4.39e+04 (3.638e+04-4.506e+04) | -1.7% | 4.007e+04, 4.471e+04, 4.466e+04 / 4.32e+04, 4.072e+04, 4.406e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 9.598e+04 (8.858e+04-1.032e+05) | 3.211e+04 (2.883e+04-3.507e+04) | -66.6% | 9.94e+04, 9.832e+04, 9.11e+04 / 3.405e+04, 2.902e+04, 3.211e+04 | consistent |
