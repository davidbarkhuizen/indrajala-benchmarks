Old `e54cd1d` against new `b900778`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `2eb9311` (extension sha256 `694886c704e2`) and new crate `0a6910b` (extension sha256 `efb050f9ebfe`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (raspberry-pi-5.json); max 1-min load 0.47 (measured just after this run's crate builds); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / dense 30 x 784 forward_batch b32 / rust -83.6% (724.9 -> 118.6 µs)
- consistent: per call / conv tail 32 x 5408 forward_batch b32 / rust -78.8% (5252 -> 1115 µs)
- consistent: per call / dense 30 x 784 forward / rust -72.0% (23.2 -> 6.491 µs)
- consistent: per call / attention 16 x 32 forward_batch b32 / rust -68.9% (2637 -> 818.8 µs)
- consistent: per call / dense 30 x 784 forward_batch b512 / rust -68.8% (3232 -> 1007 µs)
- consistent: per call / conv tail 32 x 5408 forward / rust -55.0% (164.1 -> 73.9 µs)
- consistent: per call / dense 10 x 30 forward_batch b512 / rust -54.0% (233.9 -> 107.6 µs)
- consistent: per call / dense 10 x 30 forward_batch b32 / rust -52.3% (15.28 -> 7.297 µs)
- consistent: per call / conv tail 32 x 5408 forward_batch b512 / rust -45.1% (2.181e+04 -> 1.198e+04 µs)
- consistent: per call / dense 10 x 30 forward / rust -27.4% (0.8632 -> 0.6267 µs)
- ... 33 more consistent rows (report --md)
- 227 rows within noise (30 separated inside their spread), max |Δ| 406.8%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 77.49 (76.93-80.31) | 78.57 (77.5-79.47) | +1.4% | 79.01, 77.1, 78.71 / 78.63, 78.48, 78.19 | within noise |
| conv tail 32 x 5408 forward / rust | 164.1 (163.9-164.9) | 73.9 (56.04-77.22) | -55.0% | 164, 164.1, 164.8 / 74.58, 65.71, 74.82 | consistent |
| conv tail 32 x 5408 downstream / numpy | 91.68 (91.52-93.28) | 92.65 (91.42-93.36) | +1.1% | 91.54, 91.68, 92.58 / 92.54, 92.39, 92.69 | within noise |
| conv tail 32 x 5408 downstream / rust | 83.95 (74.26-89.49) | 81.53 (74.67-92.21) | -2.9% | 76.52, 89.38, 81.78 / 81.5, 83.47, 83.46 | within noise |
| conv tail 32 x 5408 hidden_delta / numpy | 104.8 (103.2-106.1) | 105 (104-106.4) | +0.2% | 105.2, 105.3, 103.8 / 105.9, 105, 104.3 | within noise |
| conv tail 32 x 5408 hidden_delta / rust | 94.05 (79.67-95.98) | 90.51 (78.66-111.1) | -3.8% | 88.47, 87.83, 94.05 / 104.3, 81.01, 94.92 | within noise |
| conv tail 32 x 5408 accumulate_gradient / numpy | 537.4 (377.4-926) | 410.9 (334.7-860.3) | -23.5% | 642, 503.7, 685.5 / 381.1, 386.6, 640.8 | within noise |
| conv tail 32 x 5408 accumulate_gradient / rust | 93.55 (89.38-160.4) | 98.33 (89.36-100.1) | +5.1% | 91.2, 128.1, 93.91 / 98.33, 95.46, 94.72 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 1884 (1521-2200) | 1806 (1490-2221) | -4.1% | 1697, 2053, 1716 / 1687, 1806, 1903 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 628.3 (505.8-816.1) | 649.7 (500.2-806.3) | +3.4% | 647.1, 566.8, 721.5 / 506.5, 734.4, 720 | within noise |
| conv tail 32 x 5408 sgd step / numpy | 2760 (2229-2911) | 2504 (2165-2807) | -9.3% | 2839, 2569, 2499 / 2486, 2668, 2291 | within noise |
| conv tail 32 x 5408 sgd step / rust | 119.7 (115.6-276.4) | 118.2 (115.5-121.3) | -1.2% | 117.4, 271.4, 118.1 / 120.7, 117.8, 116.3 | within noise |
| conv tail 32 x 5408 forward_batch b32 / numpy | 522.7 (512.8-552.3) | 529.1 (519.4-554.8) | +1.2% | 513, 538, 526.1 / 522.4, 534.4, 542.4 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 5252 (5250-5266) | 1115 (1097-1124) | -78.8% | 5252, 5252, 5259 / 1119, 1113, 1111 | consistent |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1.9e+04 (1.76e+04-1.998e+04) | 1.861e+04 (1.483e+04-2.021e+04) | -2.1% | 1.913e+04, 1.948e+04, 1.761e+04 / 1.752e+04, 1.906e+04, 1.727e+04 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 2.181e+04 (2.173e+04-2.196e+04) | 1.198e+04 (1.043e+04-1.318e+04) | -45.1% | 2.185e+04, 2.18e+04, 2.181e+04 / 1.057e+04, 1.204e+04, 1.266e+04 | consistent |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 1554 (1055-1610) | 1533 (1074-1697) | -1.4% | 1349, 1304, 1583 / 1349, 1533, 1586 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 1397 (1139-1684) | 1215 (1141-1658) | -13.1% | 1431, 1426, 1281 / 1215, 1622, 1176 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3.068e+04 (2.455e+04-4.587e+04) | 4.227e+04 (2.968e+04-5.015e+04) | +37.8% | 3.79e+04, 3.181e+04, 2.887e+04 / 4.21e+04, 3.449e+04, 4.558e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 1.989e+04 (1.445e+04-2.496e+04) | 2.045e+04 (1.522e+04-2.276e+04) | +2.8% | 1.971e+04, 1.989e+04, 1.98e+04 / 1.972e+04, 1.876e+04, 2.063e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 3545 (3076-3906) | 3415 (2775-4257) | -3.7% | 3681, 3584, 3347 / 3516, 3796, 3121 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 1940 (1607-1998) | 2025 (1661-2162) | +4.4% | 1774, 1818, 1949 / 1840, 2025, 2126 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 6.455e+04 (5.9e+04-7.553e+04) | 6.698e+04 (6.373e+04-7.269e+04) | +3.8% | 7.412e+04, 6.223e+04, 6.361e+04 / 6.723e+04, 6.986e+04, 6.531e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 3.065e+04 (2.6e+04-3.286e+04) | 2.815e+04 (2.52e+04-4.2e+04) | -8.2% | 3.254e+04, 2.808e+04, 3.034e+04 / 3.647e+04, 2.65e+04, 2.758e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 1946 (1666-2179) | 2112 (1929-2238) | +8.5% | 2006, 1943, 1863 / 2003, 2196, 2041 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 2289 (1994-2422) | 2291 (2232-2431) | +0.1% | 2324, 2221, 2197 / 2289, 2340, 2288 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 2.73e+04 (2.3e+04-2.932e+04) | 2.558e+04 (2.225e+04-2.93e+04) | -6.3% | 2.539e+04, 2.616e+04, 2.858e+04 / 2.578e+04, 2.558e+04, 2.477e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 2.022e+04 (1.96e+04-2.12e+04) | 2.023e+04 (1.921e+04-2.087e+04) | +0.0% | 1.996e+04, 2.066e+04, 2.036e+04 / 1.96e+04, 2.053e+04, 2.046e+04 | within noise |
| dense 30 x 784 forward / numpy | 16.17 (16.1-16.48) | 16.35 (16.27-16.43) | +1.1% | 16.14, 16.3, 16.23 / 16.32, 16.3, 16.42 | within noise |
| dense 30 x 784 forward / rust | 23.2 (23.1-23.21) | 6.491 (6.463-6.652) | -72.0% | 23.2, 23.21, 23.15 / 6.557, 6.49, 6.566 | consistent |
| dense 30 x 784 downstream / numpy | 12.69 (12.66-12.73) | 12.69 (12.67-12.75) | +0.0% | 12.71, 12.68, 12.67 / 12.69, 12.73, 12.67 | within noise |
| dense 30 x 784 downstream / rust | 6.678 (6.315-6.692) | 6.595 (6.342-6.683) | -1.2% | 6.622, 6.688, 6.494 / 6.569, 6.62, 6.489 | within noise |
| dense 30 x 784 hidden_delta / numpy | 16.99 (16.89-17.16) | 16.99 (16.91-17.2) | +0.1% | 17.07, 16.98, 16.95 / 17.01, 17.1, 16.94 | within noise |
| dense 30 x 784 hidden_delta / rust | 7.526 (7.19-7.57) | 7.346 (7.184-7.577) | -2.4% | 7.494, 7.38, 7.536 / 7.36, 7.389, 7.336 | within noise |
| dense 30 x 784 accumulate_gradient / numpy | 42.92 (42.57-43.02) | 42.72 (42.62-42.89) | -0.5% | 42.8, 42.79, 42.94 / 42.84, 42.7, 42.65 | within noise |
| dense 30 x 784 accumulate_gradient / rust | 9.763 (9.686-10.08) | 9.881 (9.826-9.935) | +1.2% | 9.786, 9.914, 9.726 / 9.876, 9.881, 9.89 | within noise |
| dense 30 x 784 apply_accumulated_gradient / numpy | 61.19 (61.11-61.46) | 61.16 (61.04-61.64) | -0.0% | 61.31, 61.17, 61.18 / 61.37, 61.08, 61.34 | within noise |
| dense 30 x 784 apply_accumulated_gradient / rust | 36.42 (36.3-36.5) | 36.4 (36.26-36.48) | -0.1% | 36.4, 36.42, 36.4 / 36.32, 36.35, 36.48 | within noise |
| dense 30 x 784 sgd step / numpy | 108.1 (108.1-108.6) | 107.9 (107.8-108) | -0.2% | 108.4, 108.1, 108.1 / 108, 107.9, 107.9 | separated, inside spread |
| dense 30 x 784 sgd step / rust | 15.78 (15.6-15.82) | 15.72 (15.69-15.85) | -0.4% | 15.66, 15.8, 15.8 / 15.8, 15.7, 15.71 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 456.8 (92.27-461.4) | 92.21 (91.11-454.3) | -79.8% | 276.8, 458.6, 454.4 / 272.7, 92.41, 91.61 | separated, inside spread |
| dense 30 x 784 forward_batch b32 / rust | 724.9 (724.8-725.4) | 118.6 (115.6-119.7) | -83.6% | 725.1, 724.9, 724.8 / 119.1, 118.5, 117.1 | consistent |
| dense 30 x 784 forward_batch b512 / numpy | 2622 (2344-4156) | 2690 (2203-2820) | +2.6% | 3474, 2548, 2445 / 2661, 2690, 2511 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 3232 (3230-4353) | 1007 (970.8-1031) | -68.8% | 3793, 3233, 3231 / 1020, 1005, 989.1 | consistent |
| dense 30 x 784 downstream_batch b32 / numpy | 392.1 (58.15-400.1) | 221.6 (56.7-401.8) | -43.5% | 228.2, 222.3, 399.3 / 220.7, 230.2, 228.7 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 126.2 (125.7-127.8) | 127 (125.4-128.1) | +0.6% | 126.2, 126.9, 126.6 / 126.7, 127, 127 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 3702 (2516-4236) | 3235 (2737-4270) | -12.6% | 3060, 4018, 3371 / 3596, 3120, 3401 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 1906 (1644-2212) | 2235 (1867-2534) | +17.2% | 1906, 1700, 2085 / 1921, 2497, 2219 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 105.4 (104.2-298.6) | 105.8 (104.9-294.7) | +0.4% | 104.7, 201.7, 106.1 / 105, 199.9, 199.4 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / rust | 155.3 (153-166.5) | 161.6 (149.3-312.1) | +4.0% | 153.9, 157, 159.8 / 158, 306, 153.9 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 9158 (8690-1.127e+04) | 8840 (7754-1.023e+04) | -3.5% | 9742, 9158, 1.001e+04 / 9177, 9803, 7993 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / rust | 3282 (2760-4240) | 3651 (2566-4062) | +11.3% | 3828, 3300, 2886 / 3716, 3933, 2738 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 86.97 (86.08-443.3) | 440.7 (87.41-457.7) | +406.8% | 86.6, 86.8, 265.9 / 448.8, 442.6, 262.1 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 139.3 (139-141.5) | 140.4 (139-141) | +0.8% | 140.5, 139.2, 139.1 / 140, 140.4, 140.1 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 2168 (1865-6134) | 2015 (1914-2218) | -7.0% | 2051, 2087, 4127 / 2109, 2103, 1915 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 2423 (2252-2765) | 2543 (2358-2759) | +5.0% | 2423, 2501, 2576 / 2455, 2451, 2743 | within noise |
| dense 10 x 30 forward / numpy | 8.125 (8.06-8.174) | 8.119 (8.088-8.169) | -0.1% | 8.089, 8.113, 8.153 / 8.101, 8.159, 8.109 | within noise |
| dense 10 x 30 forward / rust | 0.8632 (0.8563-0.8756) | 0.6267 (0.6226-0.6309) | -27.4% | 0.8631, 0.8622, 0.867 / 0.6295, 0.6266, 0.6243 | consistent |
| dense 10 x 30 downstream / numpy | 1.822 (1.801-1.847) | 1.822 (1.798-1.848) | -0.0% | 1.83, 1.822, 1.822 / 1.829, 1.834, 1.812 | within noise |
| dense 10 x 30 downstream / rust | 0.4138 (0.4083-0.4569) | 0.3823 (0.3788-0.3841) | -7.6% | 0.4138, 0.4138, 0.4348 / 0.3798, 0.3839, 0.3815 | consistent |
| dense 10 x 30 hidden_delta / numpy | 4.566 (4.505-4.625) | 4.573 (4.505-4.657) | +0.2% | 4.566, 4.565, 4.57 / 4.594, 4.573, 4.555 | within noise |
| dense 10 x 30 hidden_delta / rust | 0.8185 (0.8101-0.8311) | 0.8081 (0.7982-0.8177) | -1.3% | 0.8258, 0.8141, 0.8181 / 0.8125, 0.8054, 0.8073 | separated, inside spread |
| dense 10 x 30 accumulate_gradient / numpy | 5.26 (5.239-5.297) | 5.262 (5.229-5.29) | +0.0% | 5.281, 5.246, 5.268 / 5.272, 5.27, 5.246 | within noise |
| dense 10 x 30 accumulate_gradient / rust | 0.7891 (0.7822-0.7984) | 0.7902 (0.7744-0.8061) | +0.1% | 0.7917, 0.7837, 0.7956 / 0.7861, 0.7979, 0.7826 | within noise |
| dense 10 x 30 apply_accumulated_gradient / numpy | 8.87 (8.764-8.949) | 8.901 (8.798-8.924) | +0.4% | 8.885, 8.842, 8.866 / 8.905, 8.917, 8.845 | within noise |
| dense 10 x 30 apply_accumulated_gradient / rust | 4.139 (4.115-4.176) | 4.088 (4.057-4.1) | -1.2% | 4.127, 4.133, 4.157 / 4.099, 4.072, 4.078 | separated, inside spread |
| dense 10 x 30 sgd step / numpy | 15.01 (15-15.11) | 15.01 (14.96-15.33) | -0.0% | 15.06, 15.02, 15.01 / 15.17, 14.99, 15.01 | within noise |
| dense 10 x 30 sgd step / rust | 0.9226 (0.9182-0.9274) | 0.922 (0.914-0.9279) | -0.1% | 0.9212, 0.9218, 0.9254 / 0.9143, 0.9246, 0.9235 | within noise |
| dense 10 x 30 forward_batch b32 / numpy | 19.47 (19.33-19.82) | 19.47 (19.44-19.58) | +0.0% | 19.7, 19.47, 19.38 / 19.46, 19.49, 19.53 | within noise |
| dense 10 x 30 forward_batch b32 / rust | 15.28 (15.2-15.33) | 7.297 (7.291-7.303) | -52.3% | 15.23, 15.31, 15.29 / 7.299, 7.295, 7.297 | consistent |
| dense 10 x 30 forward_batch b512 / numpy | 151.5 (151.1-151.9) | 151.9 (151.3-152.8) | +0.3% | 151.6, 151.7, 151.2 / 151.6, 152.3, 152 | within noise |
| dense 10 x 30 forward_batch b512 / rust | 233.9 (233.6-234.3) | 107.6 (107.4-108) | -54.0% | 233.9, 233.8, 234.2 / 107.6, 107.8, 107.6 | consistent |
| dense 10 x 30 downstream_batch b32 / numpy | 5.919 (5.902-5.986) | 5.948 (5.905-5.996) | +0.5% | 5.95, 5.925, 5.913 / 5.934, 5.953, 5.951 | within noise |
| dense 10 x 30 downstream_batch b32 / rust | 3.85 (3.846-3.859) | 3.245 (3.233-3.259) | -15.7% | 3.852, 3.846, 3.854 / 3.239, 3.252, 3.249 | consistent |
| dense 10 x 30 downstream_batch b512 / numpy | 64.69 (64.59-64.85) | 64.56 (64.38-64.73) | -0.2% | 64.72, 64.69, 64.73 / 64.53, 64.69, 64.44 | within noise |
| dense 10 x 30 downstream_batch b512 / rust | 55.91 (55.74-56.15) | 46.66 (46.05-46.68) | -16.6% | 56.03, 55.83, 56 / 46.66, 46.43, 46.36 | consistent |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 10.48 (10.38-10.61) | 10.45 (10.4-10.51) | -0.3% | 10.48, 10.49, 10.46 / 10.42, 10.48, 10.45 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 4.732 (4.719-4.736) | 4.131 (4.112-4.147) | -12.7% | 4.732, 4.734, 4.722 / 4.131, 4.131, 4.125 | consistent |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 93.42 (91.69-95.38) | 93.12 (92.6-94.74) | -0.3% | 92.51, 94.38, 94.4 / 93.12, 94.31, 92.61 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / rust | 64.98 (64.56-66.4) | 55.05 (54.66-55.38) | -15.3% | 65.59, 64.82, 65.09 / 55.05, 54.68, 55.22 | consistent |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 9.632 (9.557-9.696) | 9.556 (9.504-9.668) | -0.8% | 9.62, 9.664, 9.626 / 9.536, 9.606, 9.559 | separated, inside spread |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 4.566 (4.539-4.583) | 4.227 (4.22-4.249) | -7.4% | 4.574, 4.565, 4.553 / 4.229, 4.238, 4.223 | consistent |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 48.09 (47.6-48.29) | 47.81 (47.39-50) | -0.6% | 47.94, 47.97, 48.15 / 47.99, 47.55, 48.86 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 58.88 (58.73-58.97) | 58.71 (58.39-59.01) | -0.3% | 58.8, 58.95, 58.85 / 58.53, 58.71, 58.87 | within noise |
| conv 28x28, 8 ch forward / numpy | 87.83 (84.86-110.6) | 85.23 (84.81-86.26) | -3.0% | 97.94, 87.56, 97.82 / 85.08, 85.26, 85.78 | separated, inside spread |
| conv 28x28, 8 ch forward / rust | 51.61 (51.59-51.68) | 46.3 (46.28-46.33) | -10.3% | 51.6, 51.61, 51.66 / 46.31, 46.31, 46.29 | consistent |
| conv 28x28, 8 ch downstream / numpy | 71.09 (70.4-72.04) | 71.25 (70.71-72.02) | +0.2% | 71.62, 70.69, 71.23 / 70.75, 71.64, 71.43 | within noise |
| conv 28x28, 8 ch downstream / rust | 49.64 (49.62-49.67) | 43.13 (43.11-43.27) | -13.1% | 49.63, 49.66, 49.64 / 43.27, 43.12, 43.12 | consistent |
| conv 28x28, 8 ch accumulate_gradient / numpy | 59.07 (57.78-60.84) | 58.38 (57.87-61.19) | -1.2% | 57.91, 60.21, 59.31 / 58.38, 59.54, 59.08 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 30.25 (30.22-30.27) | 32.23 (32.21-32.24) | +6.6% | 30.26, 30.23, 30.25 / 32.22, 32.22, 32.23 | consistent |
| conv 28x28, 8 ch forward_batch b32 / numpy | 4737 (4432-5742) | 4241 (4086-5227) | -10.5% | 5115, 4648, 4857 / 4367, 4656, 4193 | within noise |
| conv 28x28, 8 ch forward_batch b32 / rust | 1821 (1740-2194) | 1659 (1581-1692) | -8.9% | 1790, 2020, 1810 / 1690, 1659, 1592 | separated, inside spread |
| conv 28x28, 8 ch forward_batch b512 / numpy | 7.217e+04 (6.919e+04-7.542e+04) | 7.135e+04 (6.916e+04-7.408e+04) | -1.1% | 7.463e+04, 7.027e+04, 7.145e+04 / 6.998e+04, 7.299e+04, 7.139e+04 | within noise |
| conv 28x28, 8 ch forward_batch b512 / rust | 3.754e+04 (3.68e+04-3.901e+04) | 3.414e+04 (3.319e+04-3.584e+04) | -9.0% | 3.79e+04, 3.848e+04, 3.696e+04 / 3.515e+04, 3.33e+04, 3.417e+04 | separated, inside spread |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 1722 (1451-1965) | 1502 (1441-1613) | -12.8% | 1468, 1729, 1936 / 1524, 1565, 1474 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / rust | 2531 (2178-2996) | 2243 (2069-2367) | -11.4% | 2647, 2267, 2851 / 2189, 2176, 2339 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 5.695e+04 (5.405e+04-6.209e+04) | 5.472e+04 (5.081e+04-7.335e+04) | -3.9% | 6.022e+04, 5.57e+04, 5.558e+04 / 6.396e+04, 5.355e+04, 5.428e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / rust | 5.681e+04 (5.24e+04-6.278e+04) | 5.505e+04 (5.152e+04-5.76e+04) | -3.1% | 5.95e+04, 5.672e+04, 5.738e+04 / 5.626e+04, 5.619e+04, 5.251e+04 | separated, inside spread |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 2281 (2249-2327) | 2252 (2248-2322) | -1.3% | 2319, 2250, 2286 / 2266, 2249, 2287 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 1126 (1118-1178) | 1383 (1175-1560) | +22.8% | 1125, 1150, 1132 / 1547, 1208, 1368 | separated, inside spread |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 3.752e+04 (3.717e+04-3.825e+04) | 3.718e+04 (3.714e+04-3.733e+04) | -0.9% | 3.788e+04, 3.739e+04, 3.763e+04 / 3.717e+04, 3.721e+04, 3.724e+04 | separated, inside spread |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 3.308e+04 (2.831e+04-3.503e+04) | 3.016e+04 (2.854e+04-3.629e+04) | -8.8% | 3.169e+04, 3.362e+04, 3.08e+04 / 3.157e+04, 3.246e+04, 3.016e+04 | within noise |
| conv 8x8, 8 ch forward / numpy | 34.95 (34.53-36.03) | 35 (34.44-35.18) | +0.1% | 34.73, 35.32, 35.28 / 34.77, 35.14, 34.81 | within noise |
| conv 8x8, 8 ch forward / rust | 3.669 (3.647-3.722) | 3.381 (3.362-3.399) | -7.9% | 3.674, 3.695, 3.653 / 3.381, 3.384, 3.377 | consistent |
| conv 8x8, 8 ch downstream / numpy | 39.77 (39.63-40.94) | 39.93 (39.31-40.92) | +0.4% | 39.7, 40.19, 40.28 / 40.13, 40.11, 39.77 | within noise |
| conv 8x8, 8 ch downstream / rust | 3.187 (3.178-3.197) | 2.819 (2.815-2.858) | -11.6% | 3.181, 3.188, 3.192 / 2.835, 2.816, 2.839 | consistent |
| conv 8x8, 8 ch accumulate_gradient / numpy | 12.61 (12.32-12.77) | 12.46 (12.42-12.54) | -1.2% | 12.54, 12.58, 12.65 / 12.44, 12.46, 12.5 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient / rust | 2.31 (2.299-2.339) | 2.459 (2.457-2.478) | +6.4% | 2.326, 2.302, 2.313 / 2.467, 2.468, 2.459 | consistent |
| conv 8x8, 8 ch forward_batch b32 / numpy | 129.4 (128.2-130.5) | 128.7 (128.2-156.1) | -0.5% | 129.8, 129.7, 128.4 / 128.3, 142.5, 128.7 | within noise |
| conv 8x8, 8 ch forward_batch b32 / rust | 88.3 (88.2-88.47) | 79.63 (79.33-79.86) | -9.8% | 88.29, 88.25, 88.45 / 79.63, 79.69, 79.55 | consistent |
| conv 8x8, 8 ch forward_batch b512 / numpy | 4099 (3358-4741) | 4092 (3233-5078) | -0.2% | 4430, 4244, 3460 / 3751, 4152, 4496 | within noise |
| conv 8x8, 8 ch forward_batch b512 / rust | 1795 (1605-2044) | 1724 (1406-1830) | -4.0% | 1869, 1824, 1758 / 1618, 1673, 1757 | separated, inside spread |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 115.6 (114.8-117.9) | 115.7 (115-116.7) | +0.1% | 116.7, 115.9, 115.1 / 116, 116.1, 115.1 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / rust | 85.5 (85.46-85.6) | 75.09 (74.33-75.2) | -12.2% | 85.49, 85.53, 85.5 / 74.76, 74.76, 75.1 | consistent |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 1923 (1582-2085) | 1917 (1600-2429) | -0.3% | 2006, 1765, 1809 / 1767, 2014, 1956 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / rust | 2161 (2003-2291) | 1867 (1526-2151) | -13.6% | 2164, 2147, 2148 / 2046, 1745, 1733 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 154.8 (148.8-156.1) | 148.9 (148.3-155.3) | -3.8% | 152.4, 155.8, 152 / 154.5, 148.6, 148.6 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 51.95 (51.83-52.05) | 55.53 (55.51-56.05) | +6.9% | 51.95, 51.99, 51.94 / 55.55, 55.78, 55.53 | consistent |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 2366 (2278-2377) | 2301 (2284-2366) | -2.8% | 2326, 2339, 2370 / 2325, 2293, 2334 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 1130 (976.5-1294) | 1174 (1021-1309) | +3.9% | 1278, 1141, 986.4 / 1175, 1307, 1028 | within noise |
| conv 13x13x8, 8 ch forward / numpy | 79.54 (79.24-114) | 80.57 (79.3-115.6) | +1.3% | 96.62, 79.7, 79.52 / 97.46, 79.91, 80.88 | within noise |
| conv 13x13x8, 8 ch forward / rust | 51.31 (51.27-51.57) | 47.72 (47.63-47.79) | -7.0% | 51.32, 51.28, 51.44 / 47.72, 47.66, 47.77 | consistent |
| conv 13x13x8, 8 ch downstream / numpy | 89.74 (89.25-94.03) | 90.31 (89.59-93.41) | +0.6% | 90.13, 91.79, 89.56 / 90.67, 91.56, 90.27 | within noise |
| conv 13x13x8, 8 ch downstream / rust | 33.99 (33.96-34.2) | 33.25 (32.85-33.4) | -2.2% | 34.1, 33.98, 33.97 / 33.38, 33.12, 33.12 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 40.41 (40.17-40.96) | 40.31 (40.12-40.8) | -0.2% | 40.36, 40.24, 40.81 / 40.17, 40.52, 40.45 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 14.85 (14.81-15.16) | 15.3 (15.29-15.32) | +3.1% | 15.02, 14.84, 14.83 / 15.3, 15.31, 15.29 | consistent |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 2637 (2504-2710) | 2633 (2325-2827) | -0.1% | 2680, 2642, 2523 / 2478, 2594, 2715 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 2460 (2192-2706) | 2306 (1966-2530) | -6.2% | 2515, 2450, 2449 / 2098, 2306, 2455 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 5.118e+04 (5.002e+04-5.611e+04) | 5.028e+04 (4.854e+04-5.245e+04) | -1.7% | 5.351e+04, 5.046e+04, 5.158e+04 / 5.019e+04, 5.059e+04, 5.05e+04 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 5.457e+04 (5.205e+04-5.738e+04) | 5.029e+04 (4.872e+04-5.266e+04) | -7.8% | 5.538e+04, 5.431e+04, 5.471e+04 / 4.95e+04, 5.095e+04, 5.134e+04 | consistent |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 4039 (3855-4407) | 4285 (4038-4477) | +6.1% | 3934, 4210, 4195 / 4182, 4338, 4301 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 1380 (1334-1420) | 1350 (1315-1405) | -2.1% | 1406, 1364, 1353 / 1360, 1341, 1350 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 1.181e+05 (1.097e+05-1.595e+05) | 1.168e+05 (1.098e+05-1.247e+05) | -1.1% | 1.199e+05, 1.157e+05, 1.346e+05 / 1.15e+05, 1.168e+05, 1.172e+05 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 5.673e+04 (5.31e+04-5.807e+04) | 5.499e+04 (5.149e+04-5.685e+04) | -3.1% | 5.734e+04, 5.662e+04, 5.484e+04 / 5.499e+04, 5.406e+04, 5.459e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 1139 (1127-1149) | 1128 (1122-1149) | -0.9% | 1138, 1139, 1139 / 1139, 1132, 1123 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 602.8 (591.4-608) | 621.8 (620.3-627.6) | +3.1% | 603.9, 593.9, 606 / 621.1, 621.1, 625.1 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.847e+04 (1.833e+04-1.869e+04) | 1.841e+04 (1.833e+04-1.874e+04) | -0.4% | 1.846e+04, 1.85e+04, 1.854e+04 / 1.86e+04, 1.834e+04, 1.841e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 1.317e+04 (1.144e+04-1.367e+04) | 1.321e+04 (1.111e+04-1.348e+04) | +0.3% | 1.316e+04, 1.227e+04, 1.344e+04 / 1.225e+04, 1.329e+04, 1.308e+04 | within noise |
| conv 26x26x8/2, 8 ch forward / numpy | 90.09 (89.5-90.74) | 90.04 (89.49-90.8) | -0.1% | 90.68, 89.59, 90.09 / 89.89, 89.79, 90.57 | within noise |
| conv 26x26x8/2, 8 ch forward / rust | 61.27 (60.98-61.46) | 56.66 (56.49-57.04) | -7.5% | 61.17, 61.32, 61.32 / 56.83, 56.72, 56.51 | consistent |
| conv 26x26x8/2, 8 ch downstream / numpy | 103.4 (103.2-104.2) | 103.8 (102.9-105.2) | +0.4% | 103.9, 103.2, 103.4 / 103, 104.6, 103.9 | within noise |
| conv 26x26x8/2, 8 ch downstream / rust | 41.13 (40.66-41.19) | 39.77 (39.41-39.81) | -3.3% | 41.15, 41.14, 40.89 / 39.8, 39.6, 39.59 | consistent |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 47.83 (47.48-48.49) | 47.49 (47.37-47.97) | -0.7% | 47.84, 48.21, 47.61 / 47.88, 47.39, 47.47 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 17.42 (17.4-17.48) | 18.01 (17.97-18.07) | +3.4% | 17.41, 17.42, 17.47 / 18, 18, 18.06 | consistent |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 3327 (3182-3815) | 3472 (3384-3797) | +4.4% | 3270, 3261, 3693 / 3601, 3430, 3580 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 2916 (2809-3274) | 2659 (2473-3107) | -8.8% | 3100, 3066, 2836 / 2831, 2662, 2611 | separated, inside spread |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 6.382e+04 (6.214e+04-6.783e+04) | 6.406e+04 (6.221e+04-6.729e+04) | +0.4% | 6.629e+04, 6.261e+04, 6.382e+04 / 6.569e+04, 6.492e+04, 6.293e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 6.552e+04 (5.995e+04-6.939e+04) | 6.143e+04 (5.821e+04-6.415e+04) | -6.2% | 6.925e+04, 6.191e+04, 6.387e+04 / 6.143e+04, 6.1e+04, 6.173e+04 | separated, inside spread |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 8312 (7533-9256) | 8534 (7284-1.307e+04) | +2.7% | 9106, 8312, 7649 / 7397, 9033, 1.103e+04 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 3466 (3142-4126) | 3631 (2649-4145) | +4.8% | 3634, 3466, 3667 / 3397, 4082, 2985 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 1.918e+05 (1.845e+05-2.065e+05) | 1.825e+05 (1.807e+05-2.071e+05) | -4.8% | 1.994e+05, 1.924e+05, 1.879e+05 / 1.845e+05, 1.948e+05, 1.816e+05 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 8.066e+04 (6.656e+04-8.436e+04) | 7.755e+04 (7.444e+04-8.046e+04) | -3.9% | 8.15e+04, 7.823e+04, 7.546e+04 / 7.928e+04, 7.83e+04, 7.517e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 1390 (1372-1840) | 1387 (1375-1411) | -0.2% | 1606, 1390, 1382 / 1393, 1385, 1393 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 771.2 (710.3-785.9) | 695.1 (671.9-799.5) | -9.9% | 736.2, 771.8, 781.7 / 695.1, 680.2, 794.6 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 2.231e+04 (2.221e+04-2.243e+04) | 2.243e+04 (2.219e+04-2.313e+04) | +0.6% | 2.235e+04, 2.233e+04, 2.227e+04 / 2.243e+04, 2.286e+04, 2.223e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 1.662e+04 (1.372e+04-1.77e+04) | 1.525e+04 (1.382e+04-1.704e+04) | -8.2% | 1.757e+04, 1.591e+04, 1.511e+04 / 1.626e+04, 1.579e+04, 1.43e+04 | within noise |
| conv 26x26x8, 8 ch forward / numpy | 245.3 (244.6-245.5) | 244.7 (243.8-365) | -0.2% | 245.3, 244.6, 245.5 / 304.5, 244.7, 245.5 | within noise |
| conv 26x26x8, 8 ch forward / rust | 237.8 (237.3-250) | 220.6 (219.6-221.3) | -7.3% | 244.4, 237.4, 237.7 / 219.9, 220.3, 221.2 | consistent |
| conv 26x26x8, 8 ch downstream / numpy | 254.9 (253-260.8) | 255.3 (253.8-257.6) | +0.1% | 258.2, 253.7, 254.7 / 255.7, 254.4, 256.2 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 158 (157.5-159.4) | 153.6 (153.6-153.8) | -2.8% | 157.6, 158.4, 158.6 / 153.7, 153.7, 153.6 | consistent |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 159.9 (158.8-160.6) | 160.4 (156.5-161.4) | +0.3% | 160.5, 159, 159.9 / 157.7, 160.6, 161.1 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 65.33 (64.79-66.67) | 67.32 (67.08-67.73) | +3.1% | 65.98, 64.94, 65.9 / 67.27, 67.41, 67.4 | consistent |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 1.397e+04 (1.303e+04-1.526e+04) | 1.454e+04 (1.357e+04-1.691e+04) | +4.1% | 1.377e+04, 1.516e+04, 1.331e+04 / 1.448e+04, 1.672e+04, 1.364e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 1.264e+04 (1.21e+04-1.377e+04) | 1.204e+04 (1.113e+04-1.298e+04) | -4.8% | 1.26e+04, 1.293e+04, 1.297e+04 / 1.242e+04, 1.247e+04, 1.154e+04 | separated, inside spread |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 2.36e+05 (2.334e+05-2.544e+05) | 2.473e+05 (2.435e+05-2.644e+05) | +4.8% | 2.443e+05, 2.382e+05, 2.356e+05 / 2.568e+05, 2.45e+05, 2.506e+05 | separated, inside spread |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 2.37e+05 (2.322e+05-2.489e+05) | 2.299e+05 (2.236e+05-2.358e+05) | -3.0% | 2.467e+05, 2.34e+05, 2.37e+05 / 2.341e+05, 2.255e+05, 2.295e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 2.752e+04 (2.547e+04-2.89e+04) | 2.676e+04 (2.467e+04-2.836e+04) | -2.8% | 2.851e+04, 2.717e+04, 2.67e+04 / 2.692e+04, 2.651e+04, 2.659e+04 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 1.521e+04 (1.263e+04-1.799e+04) | 1.312e+04 (1.243e+04-1.342e+04) | -13.7% | 1.521e+04, 1.335e+04, 1.733e+04 / 1.311e+04, 1.276e+04, 1.328e+04 | separated, inside spread |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 5.04e+05 (4.85e+05-5.371e+05) | 5.039e+05 (4.943e+05-5.213e+05) | -0.0% | 5.178e+05, 4.964e+05, 5.04e+05 / 5.092e+05, 5.078e+05, 5.01e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 2.706e+05 (2.452e+05-2.98e+05) | 2.576e+05 (2.55e+05-2.682e+05) | -4.8% | 2.716e+05, 2.722e+05, 2.618e+05 / 2.63e+05, 2.592e+05, 2.562e+05 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 5627 (5597-5656) | 5638 (5598-5670) | +0.2% | 5610, 5642, 5634 / 5655, 5650, 5614 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 3611 (3231-4075) | 3460 (3227-3790) | -4.2% | 3966, 3611, 3287 / 3680, 3460, 3265 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 8.885e+04 (8.837e+04-9.052e+04) | 8.909e+04 (8.829e+04-9.173e+04) | +0.3% | 8.954e+04, 8.944e+04, 8.86e+04 / 9.049e+04, 8.861e+04, 8.895e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 5.829e+04 (5.571e+04-5.95e+04) | 5.636e+04 (5.341e+04-7.339e+04) | -3.3% | 5.686e+04, 5.876e+04, 5.886e+04 / 6.667e+04, 5.636e+04, 5.409e+04 | within noise |
| pool 26x26, 8 ch forward / numpy | 105.6 (105.2-107.1) | 105.6 (105.2-117.6) | -0.0% | 105.5, 105.8, 106.2 / 111.5, 105.3, 105.8 | within noise |
| pool 26x26, 8 ch forward / rust | 5.221 (5.196-5.229) | 5.211 (5.198-5.24) | -0.2% | 5.208, 5.217, 5.223 / 5.205, 5.204, 5.228 | within noise |
| pool 26x26, 8 ch downstream / numpy | 55.3 (54.87-56) | 55.22 (55.06-55.52) | -0.2% | 55.55, 55.46, 55.01 / 55.16, 55.3, 55.29 | within noise |
| pool 26x26, 8 ch downstream / rust | 4.29 (4.281-4.321) | 4.298 (4.276-4.334) | +0.2% | 4.293, 4.307, 4.284 / 4.315, 4.292, 4.305 | within noise |
| pool 26x26, 8 ch forward_batch b32 / numpy | 2472 (2386-2804) | 2484 (2428-3204) | +0.5% | 2472, 2619, 2430 / 2816, 2484, 2484 | within noise |
| pool 26x26, 8 ch forward_batch b32 / rust | 216.1 (196-228.3) | 223.4 (201.4-273.5) | +3.4% | 226.7, 216.1, 200.8 / 212.6, 252.3, 222.1 | within noise |
| pool 26x26, 8 ch forward_batch b512 / numpy | 4.094e+04 (3.896e+04-4.145e+04) | 4.021e+04 (3.901e+04-4.217e+04) | -1.8% | 4.103e+04, 4.043e+04, 4.002e+04 / 3.968e+04, 4.183e+04, 4.004e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 8958 (8135-9968) | 9865 (8810-1.076e+04) | +10.1% | 9786, 8754, 8515 / 9648, 1.024e+04, 9792 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 987 (963.4-1546) | 972.6 (960.8-1525) | -1.5% | 964.5, 1265, 1266 / 1248, 1243, 968 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / rust | 135 (134.1-476.2) | 304 (134.2-485.1) | +125.1% | 305.6, 134.1, 135.2 / 303.7, 306.9, 309.7 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 5.994e+04 (5.436e+04-6.34e+04) | 6.083e+04 (5.479e+04-6.799e+04) | +1.5% | 6.026e+04, 5.722e+04, 5.95e+04 / 6.013e+04, 6.083e+04, 6.139e+04 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / rust | 2.077e+04 (1.948e+04-2.198e+04) | 2.017e+04 (1.998e+04-2.371e+04) | -2.9% | 2.133e+04, 2.052e+04, 2.046e+04 / 2.188e+04, 2.013e+04, 2.105e+04 | within noise |
| pool 6x6, 8 ch forward / numpy | 39.71 (39.5-41.16) | 39.76 (39.26-40.11) | +0.1% | 40.1, 39.64, 40.39 / 39.99, 39.4, 39.76 | within noise |
| pool 6x6, 8 ch forward / rust | 0.7715 (0.7663-0.8) | 0.766 (0.7572-0.7794) | -0.7% | 0.7721, 0.7715, 0.7832 / 0.7688, 0.7609, 0.7703 | separated, inside spread |
| pool 6x6, 8 ch downstream / numpy | 33.07 (32.34-33.58) | 32.75 (32.49-33.57) | -1.0% | 33.07, 32.93, 33.05 / 33.17, 32.71, 32.73 | within noise |
| pool 6x6, 8 ch downstream / rust | 0.8379 (0.8259-0.852) | 0.8142 (0.7994-0.837) | -2.8% | 0.8382, 0.8454, 0.8284 / 0.8283, 0.818, 0.8041 | separated, inside spread |
| pool 6x6, 8 ch forward_batch b32 / numpy | 168.7 (167.6-169.2) | 168.8 (167.9-225.3) | +0.1% | 169.1, 168.1, 168.8 / 182.5, 196.6, 168.3 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 10.51 (10.42-10.54) | 10.55 (10.51-10.57) | +0.4% | 10.51, 10.44, 10.53 / 10.54, 10.54, 10.56 | separated, inside spread |
| pool 6x6, 8 ch forward_batch b512 / numpy | 2259 (2173-2567) | 2380 (2190-2538) | +5.3% | 2203, 2392, 2425 / 2350, 2380, 2373 | within noise |
| pool 6x6, 8 ch forward_batch b512 / rust | 163.5 (162.8-172.8) | 164.5 (164-170.3) | +0.6% | 163.1, 168.2, 166.4 / 164.5, 167.1, 165.1 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 85.82 (85.25-86.42) | 85.31 (85.09-86.67) | -0.6% | 86.07, 85.82, 85.82 / 85.77, 85.9, 85.31 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / rust | 12.13 (12.06-12.32) | 12.21 (12.09-12.37) | +0.6% | 12.18, 12.21, 12.1 / 12.24, 12.21, 12.2 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 943.6 (936-956.4) | 947.6 (934.6-954.6) | +0.4% | 938.2, 943.6, 950.9 / 943.3, 951.4, 942.5 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 200.1 (196.7-423) | 198.8 (196.5-432.1) | -0.6% | 198.5, 198.5, 311.5 / 198.6, 198.6, 314.5 | within noise |
| conv tail 32 x 5408 bare downstream b32 / numpy | 1381 (1060-1601) | 1334 (831.8-1650) | -3.4% | 1345, 1196, 1459 / 1283, 1038, 1538 | within noise |
| conv tail 32 x 5408 bare downstream b32 / rust | 1339 (1165-1611) | 1350 (1169-1658) | +0.8% | 1339, 1183, 1550 / 1417, 1414, 1350 | within noise |
| conv tail 32 x 5408 bare downstream b512 / numpy | 4.093e+04 (2.901e+04-4.772e+04) | 3.526e+04 (2.951e+04-4.399e+04) | -13.9% | 4.092e+04, 3.547e+04, 4.228e+04 / 3.606e+04, 3.675e+04, 3.526e+04 | within noise |
| conv tail 32 x 5408 bare downstream b512 / rust | 2.198e+04 (1.988e+04-2.42e+04) | 2.28e+04 (1.844e+04-2.809e+04) | +3.8% | 2.123e+04, 2.328e+04, 2.118e+04 / 2.143e+04, 2.496e+04, 2.28e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 1607 (971.9-7981) | 1514 (1217-1626) | -5.8% | 1408, 4753, 1726 / 1358, 1408, 1577 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / rust | 1152 (1091-2144) | 1197 (1148-1373) | +3.9% | 1149, 1748, 1113 / 1269, 1293, 1149 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 2.489e+04 (2.096e+04-2.813e+04) | 2.439e+04 (2.202e+04-2.555e+04) | -2.0% | 2.402e+04, 2.556e+04, 2.455e+04 / 2.311e+04, 2.379e+04, 2.506e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / rust | 1.831e+04 (1.808e+04-1.966e+04) | 1.855e+04 (1.788e+04-1.927e+04) | +1.3% | 1.913e+04, 1.818e+04, 1.826e+04 / 1.857e+04, 1.86e+04, 1.854e+04 | within noise |
| conv tail 32 x 5408 transpose b32 / numpy | 1.468 (1.458-1.489) | 1.469 (1.459-1.482) | +0.1% | 1.469, 1.463, 1.478 / 1.473, 1.473, 1.463 | within noise |
| conv tail 32 x 5408 transpose b32 / rust | 1.877 (1.869-1.883) | 1.877 (1.87-1.881) | -0.0% | 1.877, 1.879, 1.876 / 1.874, 1.879, 1.874 | within noise |
| conv tail 32 x 5408 transpose b512 / numpy | 30.03 (29.95-30.15) | 29.98 (29.84-30.09) | -0.2% | 30.07, 30.03, 30.02 / 30.07, 29.9, 29.94 | within noise |
| conv tail 32 x 5408 transpose b512 / rust | 26.59 (26.38-27.03) | 26.58 (26.4-26.64) | -0.0% | 26.5, 26.72, 26.79 / 26.61, 26.54, 26.52 | within noise |
| conv tail 32 x 5408 add b32 / numpy | 336.2 (301.4-388.4) | 380.8 (344.2-419.7) | +13.3% | 336.1, 330.7, 356.5 / 398, 375.7, 364.7 | separated, inside spread |
| conv tail 32 x 5408 add b32 / rust | 326.9 (260-375.3) | 367.3 (319.2-383.6) | +12.4% | 319.4, 290.1, 354.4 / 339.7, 358.8, 375.1 | within noise |
| conv tail 32 x 5408 add b512 / numpy | 323.5 (264.1-426.3) | 377.9 (313.3-487.3) | +16.8% | 327, 358.6, 296 / 456.3, 369.5, 328.8 | within noise |
| conv tail 32 x 5408 add b512 / rust | 342.3 (311.3-422.2) | 334.5 (307-353.1) | -2.3% | 320.5, 369.4, 386.3 / 342.6, 337.1, 320.3 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 2.824 (2.816-2.854) | 2.831 (2.816-2.904) | +0.2% | 2.819, 2.84, 2.835 / 2.861, 2.83, 2.851 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.7809 (0.7756-0.7834) | 0.7758 (0.7685-0.7797) | -0.7% | 0.782, 0.7777, 0.7822 / 0.7723, 0.7773, 0.7767 | separated, inside spread |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 15.87 (15.78-16.15) | 15.92 (15.72-16.15) | +0.3% | 15.86, 15.83, 16.01 / 16.12, 15.84, 15.81 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 8.676 (8.657-8.695) | 8.605 (8.577-8.628) | -0.8% | 8.668, 8.694, 8.665 / 8.605, 8.606, 8.603 | consistent, small |
| dense 30 x 784 bare downstream b32 / numpy | 57.76 (56.85-388.5) | 56.95 (56.69-57.51) | -1.4% | 57.74, 223.3, 57.17 / 57.21, 57.1, 56.81 | within noise |
| dense 30 x 784 bare downstream b32 / rust | 126.5 (125.7-127.5) | 126.6 (125.7-126.9) | +0.1% | 127, 126.2, 126.2 / 126.3, 126.6, 126.8 | within noise |
| dense 30 x 784 bare downstream b512 / numpy | 3846 (2853-4165) | 3380 (2932-3939) | -12.1% | 3600, 4145, 3210 / 3081, 3299, 3874 | within noise |
| dense 30 x 784 bare downstream b512 / rust | 1889 (1548-2497) | 2511 (1853-2552) | +33.0% | 2236, 1675, 2134 / 2530, 2515, 2184 | within noise |
| dense 30 x 784 bare accumulate b32 / numpy | 234.2 (65.6-411.3) | 230.4 (66.22-401.2) | -1.6% | 238.5, 401.8, 66.64 / 230.2, 233.7, 233.7 | within noise |
| dense 30 x 784 bare accumulate b32 / rust | 125.7 (124.7-126.7) | 125.8 (125.2-126) | +0.1% | 125.1, 125.9, 125.7 / 125.9, 125.5, 125.8 | within noise |
| dense 30 x 784 bare accumulate b512 / numpy | 1903 (1705-2144) | 2010 (1665-2188) | +5.6% | 1874, 1903, 1924 / 2035, 1847, 2026 | within noise |
| dense 30 x 784 bare accumulate b512 / rust | 2520 (2270-2720) | 2445 (2170-2602) | -3.0% | 2391, 2635, 2404 / 2547, 2461, 2249 | within noise |
| dense 30 x 784 transpose b32 / numpy | 1.41 (1.389-1.702) | 1.411 (1.392-1.427) | +0.1% | 1.548, 1.4, 1.411 / 1.412, 1.403, 1.417 | within noise |
| dense 30 x 784 transpose b32 / rust | 1.82 (1.779-1.833) | 1.82 (1.809-1.826) | +0.0% | 1.806, 1.821, 1.819 / 1.816, 1.825, 1.815 | within noise |
| dense 30 x 784 transpose b512 / numpy | 8.993 (8.973-9.015) | 9.005 (8.982-9.266) | +0.1% | 8.988, 8.982, 9.008 / 9.011, 9.124, 9.002 | within noise |
| dense 30 x 784 transpose b512 / rust | 24.76 (24.73-25.09) | 24.74 (24.73-25.27) | -0.1% | 24.75, 24.91, 24.77 / 24.74, 24.74, 25.23 | within noise |
| dense 30 x 784 add b32 / numpy | 10.34 (9.954-10.79) | 10.28 (9.98-10.38) | -0.6% | 10.6, 10.21, 10.21 / 10.12, 10.24, 10.34 | within noise |
| dense 30 x 784 add b32 / rust | 9.667 (9.522-9.9) | 9.794 (9.665-11.69) | +1.3% | 9.822, 9.55, 9.73 / 9.807, 10.74, 9.706 | within noise |
| dense 30 x 784 add b512 / numpy | 11.67 (11.17-11.76) | 11.46 (11.3-12) | -1.8% | 11.44, 11.7, 11.67 / 11.31, 11.61, 11.77 | within noise |
| dense 30 x 784 add b512 / rust | 9.625 (9.561-9.85) | 9.435 (9.34-9.762) | -2.0% | 9.612, 9.71, 9.65 / 9.445, 9.412, 9.552 | separated, inside spread |
| dense 30 x 784 sum_axis0 b32 / numpy | 2.8 (2.784-2.832) | 2.808 (2.776-2.836) | +0.3% | 2.799, 2.792, 2.816 / 2.793, 2.809, 2.812 | within noise |
| dense 30 x 784 sum_axis0 b32 / rust | 0.7063 (0.7038-0.7155) | 0.7006 (0.6957-0.7023) | -0.8% | 0.7097, 0.7057, 0.7063 / 0.7001, 0.701, 0.6988 | consistent, small |
| dense 30 x 784 sum_axis0 b512 / numpy | 15.6 (15.39-15.64) | 15.38 (15.32-15.99) | -1.4% | 15.6, 15.63, 15.4 / 15.49, 15.35, 15.69 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 7.435 (7.425-7.442) | 7.465 (7.451-7.467) | +0.4% | 7.435, 7.433, 7.433 / 7.461, 7.459, 7.465 | consistent, small |
| dense 10 x 30 bare downstream b32 / numpy | 5.891 (5.84-7.734) | 5.875 (5.85-5.928) | -0.3% | 5.868, 6.816, 5.876 / 5.909, 5.866, 5.862 | within noise |
| dense 10 x 30 bare downstream b32 / rust | 3.801 (3.799-3.805) | 3.205 (3.201-3.21) | -15.7% | 3.804, 3.801, 3.8 / 3.205, 3.203, 3.207 | consistent |
| dense 10 x 30 bare downstream b512 / numpy | 64.68 (64.6-64.74) | 64.55 (64.41-64.72) | -0.2% | 64.63, 64.68, 64.74 / 64.58, 64.56, 64.54 | separated, inside spread |
| dense 10 x 30 bare downstream b512 / rust | 56.24 (55.8-56.35) | 46.12 (46-46.59) | -18.0% | 56.09, 56.24, 56.07 / 46.38, 46.24, 46 | consistent |
| dense 10 x 30 bare accumulate b32 / numpy | 5.037 (5.013-5.075) | 5.066 (5.026-5.094) | +0.6% | 5.017, 5.046, 5.062 / 5.086, 5.032, 5.066 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 3.284 (3.277-3.288) | 2.879 (2.876-2.882) | -12.3% | 3.285, 3.282, 3.283 / 2.878, 2.879, 2.879 | consistent |
| dense 10 x 30 bare accumulate b512 / numpy | 32.59 (32.46-32.9) | 32.76 (32.53-32.96) | +0.5% | 32.52, 32.59, 32.77 / 32.78, 32.77, 32.65 | within noise |
| dense 10 x 30 bare accumulate b512 / rust | 45.6 (45.54-45.65) | 45.04 (45.01-45.13) | -1.2% | 45.57, 45.63, 45.59 / 45.02, 45.08, 45.07 | consistent |
| dense 10 x 30 transpose b32 / numpy | 0.8892 (0.8805-0.9921) | 0.8895 (0.8868-0.8943) | +0.0% | 0.8827, 0.9377, 0.8947 / 0.8924, 0.8879, 0.8893 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.7993 (0.795-0.8072) | 0.7979 (0.794-0.8005) | -0.2% | 0.8024, 0.7959, 0.8019 / 0.8002, 0.7979, 0.7953 | within noise |
| dense 10 x 30 transpose b512 / numpy | 3.388 (3.363-3.583) | 3.396 (3.366-3.454) | +0.2% | 3.385, 3.369, 3.497 / 3.397, 3.382, 3.424 | within noise |
| dense 10 x 30 transpose b512 / rust | 8.578 (8.548-8.592) | 8.58 (8.571-8.587) | +0.0% | 8.585, 8.576, 8.568 / 8.58, 8.579, 8.581 | within noise |
| dense 10 x 30 add b32 / numpy | 0.8965 (0.8895-0.9054) | 0.8947 (0.8908-0.8979) | -0.2% | 0.8974, 0.8979, 0.8965 / 0.8937, 0.8947, 0.8954 | separated, inside spread |
| dense 10 x 30 add b32 / rust | 0.3785 (0.3737-0.3835) | 0.3786 (0.3752-0.4072) | +0.0% | 0.3832, 0.3784, 0.3751 / 0.3768, 0.393, 0.3774 | within noise |
| dense 10 x 30 add b512 / numpy | 0.9228 (0.9184-0.9471) | 0.9262 (0.9175-0.933) | +0.4% | 0.9328, 0.9228, 0.9244 / 0.9205, 0.9319, 0.9242 | within noise |
| dense 10 x 30 add b512 / rust | 0.4022 (0.3951-0.4076) | 0.401 (0.3982-0.4042) | -0.3% | 0.4028, 0.4022, 0.4014 / 0.4036, 0.3989, 0.401 | within noise |
| dense 10 x 30 sum_axis0 b32 / numpy | 2.467 (2.444-2.496) | 2.469 (2.435-2.479) | +0.1% | 2.465, 2.482, 2.462 / 2.469, 2.477, 2.442 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.5333 (0.5285-0.5362) | 0.5272 (0.5264-0.5331) | -1.1% | 0.5321, 0.5333, 0.5329 / 0.5288, 0.5268, 0.5302 | separated, inside spread |
| dense 10 x 30 sum_axis0 b512 / numpy | 12.2 (12.16-12.63) | 12.42 (12.17-12.63) | +1.8% | 12.2, 12.4, 12.19 / 12.38, 12.4, 12.44 | within noise |
| dense 10 x 30 sum_axis0 b512 / rust | 4.65 (4.641-4.652) | 4.65 (4.643-4.657) | -0.0% | 4.65, 4.65, 4.646 / 4.65, 4.65, 4.65 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 748.9 (745.2-968.4) | 747.9 (744.4-750.9) | -0.1% | 859.6, 745.9, 752 / 749.5, 746.1, 746.7 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 2637 (2628-2646) | 818.8 (813.8-822.7) | -68.9% | 2634, 2640, 2637 / 818.8, 821.3, 815.4 | consistent |
| attention 16 x 32 forward_batch b512 / numpy | 2.61e+04 (2.443e+04-2.842e+04) | 2.547e+04 (2.395e+04-2.628e+04) | -2.4% | 2.716e+04, 2.61e+04, 2.555e+04 / 2.536e+04, 2.506e+04, 2.588e+04 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 2.051e+04 (2.029e+04-2.16e+04) | 1.773e+04 (1.658e+04-1.88e+04) | -13.6% | 2.095e+04, 2.077e+04, 2.034e+04 / 1.871e+04, 1.773e+04, 1.692e+04 | separated, inside spread |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 762.1 (757.8-1717) | 762.8 (754.7-1755) | +0.1% | 762.4, 758.1, 1240 / 759.8, 1266, 758.2 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / rust | 790.7 (789.3-796.9) | 793.9 (791.3-796.9) | +0.4% | 790.8, 794, 789.6 / 795.4, 792.5, 794.6 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 2.952e+04 (2.526e+04-3.195e+04) | 3.149e+04 (2.731e+04-3.491e+04) | +6.7% | 2.952e+04, 2.785e+04, 2.89e+04 / 3.177e+04, 3.152e+04, 3.01e+04 | separated, inside spread |
| attention 16 x 32 hidden_delta_batch b512 / rust | 1.984e+04 (1.915e+04-2.235e+04) | 1.982e+04 (1.84e+04-2.237e+04) | -0.1% | 2.075e+04, 1.96e+04, 2.005e+04 / 2.038e+04, 2.007e+04, 1.917e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 586.8 (584-594.6) | 595.1 (580.3-2247) | +1.4% | 590.3, 588.3, 584.9 / 593, 1423, 588.2 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 510.2 (507.4-513.3) | 511.3 (504-556.5) | +0.2% | 509.9, 511.5, 509.1 / 507.1, 534.7, 509.6 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 4.193e+04 (3.426e+04-4.56e+04) | 4.492e+04 (3.506e+04-4.653e+04) | +7.1% | 4.142e+04, 3.735e+04, 4.451e+04 / 4.042e+04, 4.492e+04, 4.517e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 2.988e+04 (1.957e+04-3.789e+04) | 2.802e+04 (1.99e+04-3.781e+04) | -6.2% | 2.675e+04, 3.149e+04, 2.873e+04 / 2.833e+04, 3.314e+04, 2.346e+04 | within noise |
