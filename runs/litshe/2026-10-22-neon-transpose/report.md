Old `3d6a264` against new `3d6a264`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `45d6a37` (extension sha256 `00e539bde5d3`) and new crate `df441b3` (extension sha256 `d4d6c26f5f50`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (raspberry-pi-5.json); passes peaked at 48.0-57.3 C; max 1-min load 3.17 (HIGH) (measured just after this run's crate builds); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / conv tail 32 x 5408 transpose b512 / rust -58.4% (26.58 -> 11.05 µs)
- consistent: per call / dense 30 x 784 transpose b512 / rust -57.0% (24.78 -> 10.67 µs)
- consistent: per call / conv tail 32 x 5408 transpose b32 / rust -56.6% (1.879 -> 0.8155 µs)
- consistent: per call / dense 10 x 30 transpose b512 / rust -55.4% (8.568 -> 3.821 µs)
- consistent: per call / dense 30 x 784 transpose b32 / rust -54.1% (1.818 -> 0.834 µs)
- consistent: per call / dense 10 x 30 bare downstream b512 / rust +41.8% (46.03 -> 65.29 µs)
- consistent: per call / dense 10 x 30 downstream_batch b512 / rust +41.0% (46.32 -> 65.3 µs)
- consistent: per call / dense 10 x 30 transpose b32 / rust -37.1% (0.8001 -> 0.503 µs)
- consistent: per call / dense 10 x 30 hidden_delta_batch b512 / rust +34.8% (54.76 -> 73.8 µs)
- consistent: per call / dense 10 x 30 downstream_batch b32 / rust +21.2% (3.225 -> 3.908 µs)
- ... 17 more consistent rows (report --md)
- 243 rows within noise (37 separated inside their spread), max |Δ| 95.7%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 77.77 (77.2-79.26) | 80.08 (77.05-81.42) | +3.0% | 77.35, 78.47, 78.13 / 80.24, 77.3, 80.8 | within noise |
| conv tail 32 x 5408 forward / rust | 75.79 (54.38-77) | 54.22 (53.28-73.73) | -28.5% | 67.52, 76.02, 65.4 / 72.82, 54.1, 53.69 | within noise |
| conv tail 32 x 5408 downstream / numpy | 91.81 (91.53-92.87) | 91.72 (91.42-93.3) | -0.1% | 91.73, 91.63, 92.6 / 91.61, 91.66, 92.52 | within noise |
| conv tail 32 x 5408 downstream / rust | 74.84 (74.03-106.3) | 78.82 (74.77-106.5) | +5.3% | 74.8, 89.57, 90.16 / 76.79, 92.66, 78.25 | within noise |
| conv tail 32 x 5408 hidden_delta / numpy | 104.9 (103.8-106.9) | 104.3 (103.7-104.9) | -0.6% | 104.9, 105.3, 105.1 / 104.5, 104.3, 104.2 | separated, inside spread |
| conv tail 32 x 5408 hidden_delta / rust | 82.79 (79.7-96.81) | 80.68 (78.84-94.74) | -2.5% | 81.1, 90.16, 81.99 / 80.36, 87.26, 86.52 | within noise |
| conv tail 32 x 5408 accumulate_gradient / numpy | 417.6 (308.6-982.8) | 817.4 (406.3-995.1) | +95.7% | 689.9, 444.7, 360.6 / 704.8, 852, 648.8 | within noise |
| conv tail 32 x 5408 accumulate_gradient / rust | 93.8 (88.5-99.9) | 89.7 (88.04-98.57) | -4.4% | 94.81, 89.13, 98.87 / 89.33, 91.33, 93.31 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 1758 (1522-2017) | 1506 (1279-2037) | -14.3% | 1880, 1564, 1789 / 1562, 1737, 1477 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 649.2 (396-814.3) | 561.3 (378.7-668.6) | -13.5% | 574.7, 658.1, 605.1 / 655.3, 499.3, 453.2 | within noise |
| conv tail 32 x 5408 sgd step / numpy | 2113 (1937-2836) | 2448 (2160-3338) | +15.9% | 2176, 2041, 2446 / 2387, 2749, 2794 | within noise |
| conv tail 32 x 5408 sgd step / rust | 117.8 (116.3-271) | 116 (115-119.9) | -1.5% | 119, 116.7, 193.7 / 118.1, 116, 115.1 | within noise |
| conv tail 32 x 5408 forward_batch b32 / numpy | 529.2 (499.9-551.7) | 521.7 (504.7-532.1) | -1.4% | 525.3, 545.6, 509.4 / 518.4, 523.8, 519.9 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 1111 (1099-1125) | 1112 (1094-1119) | +0.1% | 1111, 1105, 1118 / 1102, 1116, 1113 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1.509e+04 (1.432e+04-1.984e+04) | 1.597e+04 (1.511e+04-1.902e+04) | +5.8% | 1.726e+04, 1.512e+04, 1.484e+04 / 1.542e+04, 1.769e+04, 1.597e+04 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1.099e+04 (9944-1.334e+04) | 1.033e+04 (1.001e+04-1.114e+04) | -6.0% | 1.164e+04, 1.074e+04, 1.178e+04 / 1.002e+04, 1.046e+04, 1.071e+04 | separated, inside spread |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 1516 (977.3-1680) | 1502 (1216-1565) | -0.9% | 1375, 1328, 1527 / 1431, 1390, 1533 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 1318 (1140-1664) | 1210 (1162-1695) | -8.2% | 1656, 1289, 1188 / 1452, 1429, 1170 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3.185e+04 (2.59e+04-3.55e+04) | 3.429e+04 (2.537e+04-3.904e+04) | +7.7% | 2.986e+04, 3.53e+04, 2.921e+04 / 3.306e+04, 2.955e+04, 3.491e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 1.832e+04 (1.325e+04-2.168e+04) | 1.908e+04 (1.78e+04-2.377e+04) | +4.2% | 1.746e+04, 1.641e+04, 1.896e+04 / 1.872e+04, 1.992e+04, 2.078e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 3495 (2947-3932) | 3386 (3192-4038) | -3.1% | 3439, 3649, 3368 / 3657, 3386, 3615 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 1634 (1609-1806) | 1946 (1632-2165) | +19.1% | 1642, 1622, 1711 / 1803, 2096, 1813 | separated, inside spread |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 6.461e+04 (5.914e+04-8.104e+04) | 6.184e+04 (5.793e+04-6.5e+04) | -4.3% | 7.292e+04, 6.474e+04, 5.958e+04 / 6.146e+04, 6.166e+04, 6.221e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 2.739e+04 (2.331e+04-4.189e+04) | 2.49e+04 (2.162e+04-3.162e+04) | -9.1% | 3.374e+04, 2.739e+04, 2.659e+04 / 2.49e+04, 2.662e+04, 2.5e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 1904 (1604-9056) | 1794 (1600-1892) | -5.8% | 5443, 2080, 1759 / 1695, 1746, 1870 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 2328 (2104-2405) | 2181 (2043-2353) | -6.3% | 2394, 2316, 2196 / 2263, 2146, 2117 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 2.217e+04 (2.004e+04-2.87e+04) | 2.322e+04 (2.067e+04-2.567e+04) | +4.7% | 2.446e+04, 2.217e+04, 2.223e+04 / 2.457e+04, 2.341e+04, 2.101e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 1.937e+04 (1.85e+04-2.027e+04) | 1.945e+04 (1.914e+04-1.975e+04) | +0.4% | 1.985e+04, 1.943e+04, 1.852e+04 / 1.936e+04, 1.954e+04, 1.945e+04 | within noise |
| dense 30 x 784 forward / numpy | 16.13 (16.05-16.14) | 16.11 (15.97-16.3) | -0.1% | 16.1, 16.13, 16.09 / 16.11, 16.15, 16.13 | within noise |
| dense 30 x 784 forward / rust | 6.466 (6.416-6.528) | 6.373 (6.315-6.47) | -1.4% | 6.519, 6.453, 6.444 / 6.392, 6.355, 6.399 | separated, inside spread |
| dense 30 x 784 downstream / numpy | 12.68 (12.66-12.7) | 12.69 (12.66-12.77) | +0.1% | 12.68, 12.69, 12.68 / 12.72, 12.69, 12.7 | separated, inside spread |
| dense 30 x 784 downstream / rust | 6.65 (6.512-6.677) | 6.642 (6.312-6.696) | -0.1% | 6.526, 6.65, 6.675 / 6.651, 6.493, 6.644 | within noise |
| dense 30 x 784 hidden_delta / numpy | 17.02 (16.92-17.33) | 17.04 (16.91-17.17) | +0.1% | 17.15, 17, 17.02 / 17.04, 17.07, 17.01 | within noise |
| dense 30 x 784 hidden_delta / rust | 7.428 (7.194-7.535) | 7.51 (7.212-7.569) | +1.1% | 7.432, 7.352, 7.368 / 7.557, 7.457, 7.344 | within noise |
| dense 30 x 784 accumulate_gradient / numpy | 42.89 (42.61-43.11) | 42.73 (42.6-42.8) | -0.4% | 42.77, 43.06, 42.78 / 42.7, 42.67, 42.78 | within noise |
| dense 30 x 784 accumulate_gradient / rust | 9.632 (9.592-9.901) | 9.808 (9.684-9.865) | +1.8% | 9.69, 9.771, 9.608 / 9.803, 9.838, 9.744 | within noise |
| dense 30 x 784 apply_accumulated_gradient / numpy | 61.09 (60.94-61.53) | 61.14 (61.11-61.24) | +0.1% | 60.96, 61.3, 61.11 / 61.14, 61.21, 61.11 | within noise |
| dense 30 x 784 apply_accumulated_gradient / rust | 36.49 (36.33-36.68) | 36.25 (36.22-36.31) | -0.7% | 36.55, 36.62, 36.38 / 36.29, 36.26, 36.24 | separated, inside spread |
| dense 30 x 784 sgd step / numpy | 108.1 (107.8-108.4) | 108.1 (107.8-109.2) | +0.0% | 108.2, 108, 108.1 / 108, 108.2, 108.5 | within noise |
| dense 30 x 784 sgd step / rust | 15.81 (15.79-15.85) | 15.64 (15.61-15.8) | -1.1% | 15.82, 15.82, 15.81 / 15.72, 15.67, 15.62 | separated, inside spread |
| dense 30 x 784 forward_batch b32 / numpy | 273.6 (90.95-463.2) | 273.3 (90.96-455.4) | -0.1% | 92.23, 272.6, 459.6 / 272.5, 91.92, 454.8 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 117.1 (114.8-119.4) | 119.1 (115.3-119.5) | +1.7% | 116.9, 117.1, 117.2 / 117.5, 119.1, 117.2 | separated, inside spread |
| dense 30 x 784 forward_batch b512 / numpy | 2430 (2292-2783) | 2574 (2195-2781) | +5.9% | 2345, 2750, 2430 / 2471, 2501, 2655 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 1067 (995.2-1159) | 1022 (950.3-1112) | -4.2% | 1051, 1129, 1015 / 1022, 1094, 958.4 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 57.85 (56.46-400.6) | 58.06 (57.4-58.37) | +0.4% | 228.6, 57.04, 229.3 / 57.96, 57.89, 58.2 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 126.9 (126.6-127.2) | 126.7 (125.7-127.8) | -0.2% | 126.7, 127, 127 / 127, 127, 126.1 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 3249 (2582-4216) | 3622 (2726-4087) | +11.5% | 4131, 3249, 2686 / 3608, 3130, 3760 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 1873 (1809-1950) | 2312 (1603-2596) | +23.4% | 1895, 1845, 1907 / 2395, 2271, 2000 | separated, inside spread |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 105.7 (104.1-296.2) | 106 (104.6-294.1) | +0.2% | 105, 294.1, 105 / 108, 105.3, 200 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / rust | 153.8 (145.6-157.9) | 153.9 (148.8-158.2) | +0.1% | 157.2, 149.8, 151.4 / 154.3, 150.9, 155.6 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 8315 (7727-1.1e+04) | 8560 (7456-1.177e+04) | +2.9% | 9578, 8101, 8511 / 9239, 8521, 9613 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / rust | 3211 (2762-3915) | 3261 (2954-4233) | +1.6% | 3338, 3417, 3211 / 3642, 3620, 2979 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 87.22 (85.85-452.1) | 87.36 (85.9-449.2) | +0.2% | 269, 87.22, 264.1 / 87.52, 268.3, 86.58 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 139.5 (139.2-140) | 138.9 (138.4-140.5) | -0.4% | 139.6, 139.3, 139.7 / 139.5, 139.7, 138.5 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 2138 (1847-2260) | 1904 (1768-2120) | -10.9% | 2037, 2143, 2097 / 1989, 1847, 1977 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 2406 (2226-2740) | 2459 (2224-2515) | +2.2% | 2483, 2342, 2457 / 2496, 2296, 2472 | within noise |
| dense 10 x 30 forward / numpy | 8.162 (8.081-8.286) | 8.139 (8.073-8.168) | -0.3% | 8.104, 8.2, 8.184 / 8.119, 8.167, 8.11 | within noise |
| dense 10 x 30 forward / rust | 0.6305 (0.6297-0.6501) | 0.6326 (0.6225-0.6512) | +0.3% | 0.6299, 0.6399, 0.6383 / 0.632, 0.6238, 0.6495 | within noise |
| dense 10 x 30 downstream / numpy | 1.824 (1.798-1.854) | 1.83 (1.813-1.847) | +0.3% | 1.846, 1.824, 1.808 / 1.838, 1.835, 1.82 | within noise |
| dense 10 x 30 downstream / rust | 0.3913 (0.3844-0.4047) | 0.3895 (0.3814-0.3979) | -0.5% | 0.3958, 0.3913, 0.3898 / 0.3886, 0.3911, 0.3896 | within noise |
| dense 10 x 30 hidden_delta / numpy | 4.546 (4.502-4.564) | 4.525 (4.501-4.607) | -0.5% | 4.561, 4.545, 4.523 / 4.515, 4.557, 4.525 | within noise |
| dense 10 x 30 hidden_delta / rust | 0.8452 (0.7461-0.86) | 0.7493 (0.7417-0.766) | -11.3% | 0.8548, 0.7951, 0.8432 / 0.7484, 0.766, 0.7434 | separated, inside spread |
| dense 10 x 30 accumulate_gradient / numpy | 5.274 (5.248-5.344) | 5.277 (5.246-5.309) | +0.1% | 5.314, 5.266, 5.261 / 5.278, 5.263, 5.291 | within noise |
| dense 10 x 30 accumulate_gradient / rust | 0.7886 (0.7775-0.8003) | 0.77 (0.7572-0.7803) | -2.4% | 0.7966, 0.7866, 0.7831 / 0.7719, 0.7765, 0.7579 | separated, inside spread |
| dense 10 x 30 apply_accumulated_gradient / numpy | 9.015 (8.907-9.135) | 8.909 (8.814-8.928) | -1.2% | 9.021, 9.05, 8.997 / 8.866, 8.918, 8.887 | consistent |
| dense 10 x 30 apply_accumulated_gradient / rust | 4.08 (4.062-4.091) | 4.063 (4.023-4.083) | -0.4% | 4.08, 4.078, 4.074 / 4.035, 4.081, 4.065 | within noise |
| dense 10 x 30 sgd step / numpy | 15.02 (14.9-15.31) | 15.04 (14.84-15.34) | +0.2% | 15.01, 14.96, 15.17 / 15.04, 14.95, 15.18 | within noise |
| dense 10 x 30 sgd step / rust | 0.9344 (0.9234-0.9953) | 0.9372 (0.9288-0.9448) | +0.3% | 0.9651, 0.924, 0.935 / 0.934, 0.9347, 0.9423 | within noise |
| dense 10 x 30 forward_batch b32 / numpy | 19.41 (19.33-19.47) | 19.42 (19.34-19.67) | +0.1% | 19.37, 19.4, 19.46 / 19.44, 19.52, 19.38 | within noise |
| dense 10 x 30 forward_batch b32 / rust | 7.173 (7.159-7.187) | 7.3 (7.288-7.351) | +1.8% | 7.174, 7.173, 7.168 / 7.294, 7.329, 7.298 | consistent |
| dense 10 x 30 forward_batch b512 / numpy | 151.4 (151-151.8) | 151.5 (150.9-151.7) | +0.1% | 151.6, 151.5, 151.1 / 151.2, 151.5, 151.4 | within noise |
| dense 10 x 30 forward_batch b512 / rust | 106.4 (106-106.6) | 107.9 (107.7-108.1) | +1.4% | 106.2, 106.5, 106.3 / 107.9, 107.8, 108 | consistent |
| dense 10 x 30 downstream_batch b32 / numpy | 5.937 (5.881-5.994) | 5.922 (5.907-5.947) | -0.3% | 5.95, 5.955, 5.917 / 5.907, 5.942, 5.922 | within noise |
| dense 10 x 30 downstream_batch b32 / rust | 3.225 (3.223-3.234) | 3.908 (3.896-4.027) | +21.2% | 3.227, 3.225, 3.229 / 3.908, 3.963, 3.907 | consistent |
| dense 10 x 30 downstream_batch b512 / numpy | 64.69 (64.63-65.73) | 64.7 (64.6-64.87) | +0.0% | 64.63, 65.19, 64.75 / 64.68, 64.78, 64.73 | within noise |
| dense 10 x 30 downstream_batch b512 / rust | 46.32 (45.86-46.36) | 65.3 (64.48-69.77) | +41.0% | 46.1, 46.24, 46.32 / 69.74, 64.93, 65.17 | consistent |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 10.44 (10.41-10.49) | 10.45 (10.41-10.46) | +0.1% | 10.44, 10.46, 10.43 / 10.43, 10.43, 10.46 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 4.108 (4.088-4.115) | 4.898 (4.773-4.929) | +19.2% | 4.11, 4.095, 4.111 / 4.834, 4.851, 4.905 | consistent |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 93.28 (92.12-95.18) | 92.71 (92.1-95.03) | -0.6% | 93.77, 93.44, 92.86 / 93.94, 92.18, 92.71 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / rust | 54.76 (54.64-55.01) | 73.8 (73.62-78.73) | +34.8% | 54.8, 54.92, 54.66 / 76.31, 73.84, 73.67 | consistent |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 9.609 (9.498-9.704) | 9.618 (9.595-9.897) | +0.1% | 9.553, 9.629, 9.614 / 9.607, 9.761, 9.613 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 4.269 (4.261-4.273) | 3.926 (3.916-3.942) | -8.0% | 4.271, 4.268, 4.264 / 3.923, 3.933, 3.929 | consistent |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 47.71 (47.52-47.92) | 47.85 (47.56-48.38) | +0.3% | 47.68, 47.89, 47.61 / 47.68, 48.14, 47.93 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 58.73 (58.69-58.77) | 53.98 (53.91-54.06) | -8.1% | 58.76, 58.7, 58.72 / 54, 53.98, 53.98 | consistent |
| conv 28x28, 8 ch forward / numpy | 85.42 (84.78-87.23) | 85.77 (85.15-93.55) | +0.4% | 86.35, 85.34, 85.76 / 89.68, 85.44, 85.71 | within noise |
| conv 28x28, 8 ch forward / rust | 47.13 (47.07-47.16) | 47.07 (47.04-47.13) | -0.1% | 47.13, 47.14, 47.11 / 47.07, 47.08, 47.09 | separated, inside spread |
| conv 28x28, 8 ch downstream / numpy | 71.9 (70.88-72.72) | 70.93 (70.66-71.38) | -1.4% | 71.9, 71.8, 71.8 / 71.35, 70.83, 70.81 | separated, inside spread |
| conv 28x28, 8 ch downstream / rust | 45.06 (45-45.31) | 46.48 (46.19-46.6) | +3.1% | 45.06, 45.25, 45.01 / 46.5, 46.38, 46.39 | consistent |
| conv 28x28, 8 ch accumulate_gradient / numpy | 60.24 (57.89-60.6) | 59.56 (57.73-60.37) | -1.1% | 60.43, 59.24, 59.13 / 59.18, 59.05, 59.6 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 31.56 (31.54-31.57) | 31.54 (31.51-31.61) | -0.1% | 31.56, 31.56, 31.56 / 31.53, 31.55, 31.57 | within noise |
| conv 28x28, 8 ch forward_batch b32 / numpy | 4108 (3720-6015) | 4340 (3706-5358) | +5.7% | 5037, 4084, 4326 / 4399, 5009, 3858 | within noise |
| conv 28x28, 8 ch forward_batch b32 / rust | 1819 (1599-1939) | 1577 (1542-1784) | -13.3% | 1720, 1738, 1886 / 1549, 1602, 1673 | separated, inside spread |
| conv 28x28, 8 ch forward_batch b512 / numpy | 6.888e+04 (6.718e+04-7.712e+04) | 6.916e+04 (6.697e+04-7.112e+04) | +0.4% | 7.332e+04, 6.826e+04, 6.926e+04 / 7.028e+04, 6.754e+04, 6.916e+04 | within noise |
| conv 28x28, 8 ch forward_batch b512 / rust | 3.462e+04 (3.175e+04-3.679e+04) | 3.303e+04 (3.162e+04-3.401e+04) | -4.6% | 3.326e+04, 3.506e+04, 3.474e+04 / 3.303e+04, 3.242e+04, 3.326e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 1732 (1486-2369) | 1538 (1465-2002) | -11.2% | 1732, 1786, 1927 / 1519, 1739, 1538 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / rust | 1386 (1383-1387) | 1424 (1420-1428) | +2.8% | 1385, 1386, 1385 / 1427, 1425, 1421 | consistent |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 5.223e+04 (5.05e+04-6.066e+04) | 5.281e+04 (5.106e+04-5.574e+04) | +1.1% | 5.558e+04, 5.181e+04, 5.467e+04 / 5.546e+04, 5.174e+04, 5.281e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / rust | 1.094e+04 (9467-1.241e+04) | 9866 (9602-1.16e+04) | -9.8% | 1.215e+04, 1.082e+04, 1.016e+04 / 1.04e+04, 9770, 1.065e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 2286 (2248-2353) | 2252 (2249-2256) | -1.5% | 2285, 2250, 2339 / 2252, 2250, 2254 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 1210 (1169-1522) | 1201 (1190-1546) | -0.7% | 1388, 1202, 1190 / 1196, 1204, 1373 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 3.716e+04 (3.715e+04-3.75e+04) | 3.72e+04 (3.716e+04-3.732e+04) | +0.1% | 3.718e+04, 3.732e+04, 3.716e+04 / 3.718e+04, 3.726e+04, 3.725e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 3.06e+04 (2.756e+04-3.362e+04) | 2.792e+04 (2.678e+04-3.106e+04) | -8.7% | 3.227e+04, 2.891e+04, 3.122e+04 / 2.818e+04, 2.775e+04, 2.933e+04 | within noise |
| conv 8x8, 8 ch forward / numpy | 34.87 (34.5-35.09) | 34.85 (34.7-37.03) | -0.1% | 34.82, 34.94, 34.78 / 35.94, 35.01, 34.77 | within noise |
| conv 8x8, 8 ch forward / rust | 3.431 (3.42-3.45) | 3.363 (3.354-3.378) | -2.0% | 3.427, 3.431, 3.44 / 3.368, 3.36, 3.365 | consistent |
| conv 8x8, 8 ch downstream / numpy | 39.67 (39.31-39.9) | 39.99 (39.55-41.37) | +0.8% | 39.71, 39.6, 39.67 / 40.6, 40.64, 39.71 | within noise |
| conv 8x8, 8 ch downstream / rust | 2.924 (2.915-2.949) | 2.929 (2.925-2.934) | +0.2% | 2.943, 2.921, 2.922 / 2.926, 2.933, 2.929 | within noise |
| conv 8x8, 8 ch accumulate_gradient / numpy | 12.56 (12.5-12.75) | 12.52 (12.35-12.6) | -0.4% | 12.56, 12.62, 12.58 / 12.53, 12.43, 12.56 | within noise |
| conv 8x8, 8 ch accumulate_gradient / rust | 2.422 (2.412-2.438) | 2.424 (2.413-2.437) | +0.0% | 2.429, 2.413, 2.426 / 2.43, 2.423, 2.425 | within noise |
| conv 8x8, 8 ch forward_batch b32 / numpy | 129.1 (128.3-130.7) | 130 (128.5-131.2) | +0.7% | 129.9, 129.9, 128.6 / 129.4, 129.4, 130.7 | within noise |
| conv 8x8, 8 ch forward_batch b32 / rust | 80.97 (80.81-81.14) | 80.77 (80.52-80.98) | -0.2% | 80.96, 80.98, 80.98 / 80.72, 80.6, 80.92 | separated, inside spread |
| conv 8x8, 8 ch forward_batch b512 / numpy | 3962 (3711-4228) | 3566 (3206-3978) | -10.0% | 3962, 3935, 3969 / 3518, 3963, 3345 | within noise |
| conv 8x8, 8 ch forward_batch b512 / rust | 1765 (1480-1963) | 1637 (1480-1776) | -7.2% | 1721, 1827, 1729 / 1718, 1599, 1567 | separated, inside spread |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 116.1 (114.9-117.4) | 116.1 (115.4-117.9) | +0.0% | 115.4, 116.9, 116.4 / 116.9, 115.6, 116.6 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / rust | 76.49 (76.31-76.51) | 76.34 (76.28-76.51) | -0.2% | 76.37, 76.51, 76.49 / 76.49, 76.31, 76.31 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 1906 (1628-2162) | 1809 (1592-2040) | -5.1% | 1968, 1765, 2033 / 1819, 1809, 1816 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / rust | 1218 (1214-1218) | 1216 (1215-1219) | -0.1% | 1218, 1216, 1216 / 1219, 1216, 1215 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 149.1 (148.1-150.6) | 148.7 (148.1-155.7) | -0.2% | 148.6, 148.6, 150.6 / 151.8, 148.6, 152.1 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 54.19 (54.16-54.34) | 54.18 (54.15-54.34) | -0.0% | 54.19, 54.18, 54.25 / 54.17, 54.24, 54.23 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 2295 (2291-2413) | 2289 (2277-2302) | -0.2% | 2291, 2354, 2297 / 2291, 2289, 2289 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 1134 (997.7-1291) | 1138 (998.2-1302) | +0.4% | 1286, 999.6, 1133 / 1278, 1150, 1005 | within noise |
| conv 13x13x8, 8 ch forward / numpy | 79.85 (79.09-101.2) | 79.74 (79.01-79.97) | -0.1% | 79.43, 90.54, 80.16 / 79.82, 79.46, 79.41 | within noise |
| conv 13x13x8, 8 ch forward / rust | 48.77 (48.64-49.12) | 48.09 (48.07-48.13) | -1.4% | 48.9, 48.79, 48.75 / 48.12, 48.09, 48.08 | consistent |
| conv 13x13x8, 8 ch downstream / numpy | 89.18 (88.71-89.82) | 88.99 (88.67-90.13) | -0.2% | 89.07, 88.88, 89.71 / 89.42, 89.4, 88.99 | within noise |
| conv 13x13x8, 8 ch downstream / rust | 33.62 (33.5-33.68) | 33.47 (33.26-33.63) | -0.5% | 33.57, 33.67, 33.59 / 33.54, 33.53, 33.37 | separated, inside spread |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 40.44 (40.2-40.85) | 40.31 (40.18-40.54) | -0.3% | 40.74, 40.42, 40.31 / 40.43, 40.25, 40.27 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 16.34 (16.32-16.35) | 16.36 (16.31-16.41) | +0.1% | 16.34, 16.35, 16.34 / 16.33, 16.38, 16.35 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 2488 (2398-2631) | 2508 (2431-2836) | +0.8% | 2515, 2485, 2540 / 2484, 2678, 2475 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 2175 (2003-2423) | 2225 (2071-2405) | +2.3% | 2295, 2229, 2076 / 2139, 2323, 2201 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 5.024e+04 (4.895e+04-5.323e+04) | 4.907e+04 (4.763e+04-5.049e+04) | -2.3% | 5.235e+04, 5.007e+04, 4.916e+04 / 4.907e+04, 4.94e+04, 4.906e+04 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 5.052e+04 (4.707e+04-5.667e+04) | 4.973e+04 (4.84e+04-5.293e+04) | -1.6% | 5.332e+04, 5.131e+04, 4.836e+04 / 5.077e+04, 5.137e+04, 4.903e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 4324 (3887-4425) | 4187 (3994-4427) | -3.2% | 4377, 4131, 4312 / 4031, 4165, 4406 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 1020 (1013-1024) | 1016 (1010-1022) | -0.3% | 1020, 1017, 1022 / 1019, 1017, 1013 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 1.146e+05 (1.095e+05-1.264e+05) | 1.144e+05 (1.086e+05-1.163e+05) | -0.2% | 1.235e+05, 1.146e+05, 1.098e+05 / 1.132e+05, 1.146e+05, 1.123e+05 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 6972 (6117-8145) | 6811 (6402-7367) | -2.3% | 7431, 6767, 6972 / 6811, 7355, 6463 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 1136 (1121-1139) | 1131 (1125-1137) | -0.5% | 1130, 1136, 1134 / 1132, 1135, 1128 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 644 (634.6-646.7) | 645.7 (643.2-665.4) | +0.3% | 646.3, 644, 638.5 / 657.3, 644.4, 644.9 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.862e+04 (1.834e+04-1.876e+04) | 1.836e+04 (1.832e+04-1.863e+04) | -1.4% | 1.871e+04, 1.849e+04, 1.85e+04 / 1.834e+04, 1.837e+04, 1.849e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 1.279e+04 (1.165e+04-1.453e+04) | 1.186e+04 (1.163e+04-1.223e+04) | -7.3% | 1.309e+04, 1.279e+04, 1.288e+04 / 1.163e+04, 1.203e+04, 1.2e+04 | consistent |
| conv 26x26x8/2, 8 ch forward / numpy | 90.17 (89.72-90.44) | 90.24 (89.6-91.43) | +0.1% | 90.06, 90.31, 89.99 / 90.31, 90.24, 90.52 | within noise |
| conv 26x26x8/2, 8 ch forward / rust | 57.93 (57.47-57.97) | 56.98 (56.95-57.08) | -1.6% | 57.96, 57.51, 57.94 / 56.98, 57.02, 56.98 | consistent |
| conv 26x26x8/2, 8 ch downstream / numpy | 102.7 (102.4-104) | 103.3 (103-103.9) | +0.6% | 103.3, 102.7, 102.8 / 103.1, 103.5, 103.6 | within noise |
| conv 26x26x8/2, 8 ch downstream / rust | 40.28 (39.8-40.47) | 40.17 (39.7-40.27) | -0.3% | 40.35, 40.13, 40.27 / 39.92, 40.21, 40.2 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 47.43 (46.69-47.58) | 47.82 (47.26-48.13) | +0.8% | 47.49, 47.28, 47.1 / 47.82, 47.68, 47.69 | separated, inside spread |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 19.26 (19.23-19.28) | 19.31 (19.23-19.36) | +0.3% | 19.27, 19.24, 19.27 / 19.33, 19.34, 19.27 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 3415 (3253-3816) | 3309 (3085-3380) | -3.1% | 3534, 3363, 3537 / 3366, 3176, 3234 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 2690 (2581-3114) | 2691 (2569-2860) | +0.0% | 2847, 2690, 2782 / 2691, 2715, 2707 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 6.328e+04 (6.104e+04-6.7e+04) | 6.322e+04 (6.156e+04-6.961e+04) | -0.1% | 6.519e+04, 6.295e+04, 6.241e+04 / 6.318e+04, 6.322e+04, 6.568e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 6.118e+04 (5.842e+04-6.676e+04) | 5.782e+04 (5.642e+04-6.288e+04) | -5.5% | 6.259e+04, 6.068e+04, 6.183e+04 / 5.811e+04, 5.965e+04, 5.782e+04 | separated, inside spread |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 8776 (7641-1.027e+04) | 8449 (7586-8935) | -3.7% | 8476, 8958, 8903 / 7991, 8254, 8919 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 1241 (1233-1254) | 1247 (1229-1253) | +0.4% | 1244, 1241, 1241 / 1247, 1252, 1229 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 1.834e+05 (1.775e+05-2.086e+05) | 1.828e+05 (1.804e+05-1.84e+05) | -0.4% | 1.939e+05, 1.869e+05, 1.799e+05 / 1.822e+05, 1.828e+05, 1.822e+05 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 2.306e+04 (2.139e+04-2.971e+04) | 2.31e+04 (2.098e+04-2.703e+04) | +0.2% | 2.59e+04, 2.306e+04, 2.232e+04 / 2.31e+04, 2.4e+04, 2.4e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 1381 (1370-1407) | 1384 (1368-1429) | +0.2% | 1379, 1381, 1392 / 1398, 1384, 1390 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 802.8 (774.8-837.3) | 806.8 (772.5-841.4) | +0.5% | 776.9, 802, 833.1 / 807.5, 773.2, 839.8 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 2.244e+04 (2.214e+04-2.279e+04) | 2.227e+04 (2.219e+04-2.253e+04) | -0.7% | 2.247e+04, 2.225e+04, 2.266e+04 / 2.24e+04, 2.223e+04, 2.232e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 1.603e+04 (1.529e+04-1.879e+04) | 1.604e+04 (1.513e+04-1.682e+04) | +0.1% | 1.765e+04, 1.534e+04, 1.626e+04 / 1.635e+04, 1.641e+04, 1.537e+04 | within noise |
| conv 26x26x8, 8 ch forward / numpy | 244.7 (244.5-245.9) | 245.3 (244.3-403.2) | +0.3% | 244.7, 245.3, 244.6 / 246, 244.5, 323.9 | within noise |
| conv 26x26x8, 8 ch forward / rust | 224.4 (224.2-225.6) | 224 (223.5-224.9) | -0.2% | 225.5, 224.2, 224.4 / 224.2, 224.3, 223.8 | within noise |
| conv 26x26x8, 8 ch downstream / numpy | 255.5 (252.5-258.3) | 255.4 (254.2-256.3) | -0.0% | 257.3, 255.6, 253.6 / 255.7, 255.2, 254.9 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 155.4 (154.8-156.5) | 154.9 (154.3-155.6) | -0.3% | 155.5, 155.9, 155.2 / 154.6, 155.3, 155 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 159.7 (158.7-161.6) | 160 (158.9-162) | +0.2% | 158.8, 159.9, 160.9 / 160, 160.5, 160.2 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 72.22 (71.95-72.38) | 72.32 (71.82-72.4) | +0.1% | 72.22, 72.16, 72.17 / 72.15, 72.35, 72.08 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 1.401e+04 (1.21e+04-1.503e+04) | 1.48e+04 (1.377e+04-1.659e+04) | +5.6% | 1.431e+04, 1.327e+04, 1.377e+04 / 1.437e+04, 1.577e+04, 1.43e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 1.205e+04 (1.16e+04-1.299e+04) | 1.157e+04 (1.11e+04-1.282e+04) | -4.0% | 1.224e+04, 1.17e+04, 1.25e+04 / 1.157e+04, 1.226e+04, 1.118e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 2.478e+05 (2.291e+05-2.622e+05) | 2.435e+05 (2.414e+05-2.56e+05) | -1.7% | 2.496e+05, 2.457e+05, 2.451e+05 / 2.424e+05, 2.493e+05, 2.493e+05 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 2.303e+05 (2.213e+05-2.319e+05) | 2.232e+05 (2.217e+05-2.327e+05) | -3.1% | 2.31e+05, 2.26e+05, 2.259e+05 / 2.233e+05, 2.281e+05, 2.228e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 2.666e+04 (2.449e+04-2.803e+04) | 2.48e+04 (2.353e+04-2.59e+04) | -6.9% | 2.803e+04, 2.606e+04, 2.545e+04 / 2.519e+04, 2.472e+04, 2.431e+04 | separated, inside spread |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 3336 (3026-4722) | 3462 (2930-3909) | +3.8% | 3318, 3237, 4015 / 3462, 3173, 3881 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 5.094e+05 (4.889e+05-5.244e+05) | 4.937e+05 (4.889e+05-5.145e+05) | -3.1% | 5.145e+05, 5.052e+05, 5.015e+05 / 5.037e+05, 4.957e+05, 4.926e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 5.918e+04 (4.937e+04-6.416e+04) | 5.51e+04 (5.085e+04-6.198e+04) | -6.9% | 5.918e+04, 5.847e+04, 5.676e+04 / 5.51e+04, 5.642e+04, 5.453e+04 | separated, inside spread |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 5635 (5608-5757) | 5652 (5613-5729) | +0.3% | 5682, 5646, 5617 / 5674, 5685, 5628 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 3689 (3253-3998) | 3389 (2989-3686) | -8.1% | 3423, 3794, 3653 / 3389, 3116, 3668 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 8.87e+04 (8.84e+04-8.963e+04) | 8.876e+04 (8.814e+04-9.053e+04) | +0.1% | 8.957e+04, 8.87e+04, 8.844e+04 / 8.933e+04, 8.907e+04, 8.876e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 5.794e+04 (5.19e+04-6.328e+04) | 5.91e+04 (5.684e+04-6.549e+04) | +2.0% | 5.941e+04, 5.569e+04, 5.759e+04 / 6.17e+04, 5.782e+04, 6.236e+04 | within noise |
| pool 26x26, 8 ch forward / numpy | 105.7 (105.2-105.9) | 105.8 (105.3-106.8) | +0.1% | 105.9, 105.4, 105.7 / 105.7, 105.8, 106.1 | within noise |
| pool 26x26, 8 ch forward / rust | 5.225 (5.221-5.231) | 5.217 (5.2-5.235) | -0.1% | 5.225, 5.222, 5.229 / 5.21, 5.225, 5.225 | within noise |
| pool 26x26, 8 ch downstream / numpy | 55.27 (54.87-55.83) | 55.49 (54.8-56.15) | +0.4% | 55.21, 55.12, 55.59 / 55.14, 55.43, 55.83 | within noise |
| pool 26x26, 8 ch downstream / rust | 4.144 (4.127-4.153) | 4.142 (4.115-4.154) | -0.1% | 4.146, 4.147, 4.137 / 4.126, 4.134, 4.151 | within noise |
| pool 26x26, 8 ch forward_batch b32 / numpy | 2397 (2387-2462) | 2423 (2391-3167) | +1.1% | 2405, 2428, 2392 / 2392, 2423, 2809 | within noise |
| pool 26x26, 8 ch forward_batch b32 / rust | 214.1 (202.9-243.2) | 224.9 (194-242.7) | +5.0% | 211.3, 224.7, 220.3 / 218.4, 228.7, 213.7 | within noise |
| pool 26x26, 8 ch forward_batch b512 / numpy | 3.981e+04 (3.922e+04-4.14e+04) | 4.023e+04 (3.887e+04-4.144e+04) | +1.1% | 3.953e+04, 3.988e+04, 4.051e+04 / 4.018e+04, 4.11e+04, 3.94e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 8302 (7459-8834) | 8584 (8150-9273) | +3.4% | 8343, 8579, 7734 / 8151, 8982, 8700 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 973.2 (964.8-1504) | 968.3 (951-1540) | -0.5% | 965.4, 1235, 1234 / 951.2, 1257, 969.5 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / rust | 130.1 (129.9-469) | 130.4 (129.6-470.2) | +0.2% | 299.5, 130.2, 130 / 130.7, 129.9, 299.9 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 5.613e+04 (5.237e+04-5.89e+04) | 5.618e+04 (5.271e+04-5.835e+04) | +0.1% | 5.804e+04, 5.644e+04, 5.259e+04 / 5.534e+04, 5.705e+04, 5.573e+04 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / rust | 2.133e+04 (1.902e+04-2.248e+04) | 2.115e+04 (1.955e+04-2.626e+04) | -0.9% | 2.166e+04, 2.177e+04, 1.943e+04 / 2.012e+04, 2.235e+04, 2.298e+04 | within noise |
| pool 6x6, 8 ch forward / numpy | 39.7 (39.49-40.03) | 40.18 (39.46-41.52) | +1.2% | 39.74, 39.7, 39.76 / 40.7, 40.33, 40 | separated, inside spread |
| pool 6x6, 8 ch forward / rust | 0.766 (0.7624-0.7796) | 0.7708 (0.7506-0.7762) | +0.6% | 0.7638, 0.767, 0.7732 / 0.7708, 0.7762, 0.7582 | within noise |
| pool 6x6, 8 ch downstream / numpy | 32.48 (32.26-32.66) | 32.69 (32.5-33.57) | +0.6% | 32.44, 32.41, 32.53 / 32.79, 32.53, 33.14 | separated, inside spread |
| pool 6x6, 8 ch downstream / rust | 0.6537 (0.6513-0.6866) | 0.6626 (0.6546-0.6645) | +1.4% | 0.6524, 0.6696, 0.6574 / 0.6635, 0.6631, 0.6577 | within noise |
| pool 6x6, 8 ch forward_batch b32 / numpy | 168.3 (167.3-169) | 168.6 (167.7-169.6) | +0.2% | 168.2, 168.4, 168.2 / 168.2, 169, 168.2 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 10.58 (10.56-10.6) | 10.57 (10.55-10.61) | -0.1% | 10.59, 10.57, 10.59 / 10.59, 10.55, 10.57 | within noise |
| pool 6x6, 8 ch forward_batch b512 / numpy | 2198 (2184-2961) | 2194 (2185-2479) | -0.2% | 2198, 2245, 2576 / 2333, 2252, 2187 | within noise |
| pool 6x6, 8 ch forward_batch b512 / rust | 168.2 (165.4-175) | 166.8 (165.3-170.3) | -0.8% | 165.7, 168.1, 172.6 / 166.8, 167.8, 167.1 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 85.29 (84.95-85.56) | 85.86 (85.43-86.37) | +0.7% | 85.47, 85.29, 84.99 / 86.08, 85.68, 86 | separated, inside spread |
| pool 6x6, 8 ch downstream_batch b32 / rust | 7.855 (7.841-7.864) | 7.845 (7.831-7.866) | -0.1% | 7.852, 7.857, 7.853 / 7.851, 7.831, 7.854 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 947.3 (934.2-969.9) | 940.6 (935.1-951.6) | -0.7% | 956.6, 947.3, 942.7 / 941.5, 936.9, 946 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 129 (128.9-454.9) | 128.9 (128.8-129.3) | -0.1% | 292, 129, 129 / 129.1, 128.8, 128.9 | within noise |
| conv tail 32 x 5408 bare downstream b32 / numpy | 1324 (917-1603) | 1242 (1089-1486) | -6.1% | 1372, 1260, 1243 / 1418, 1161, 1218 | within noise |
| conv tail 32 x 5408 bare downstream b32 / rust | 1352 (1154-1664) | 1537 (1240-1678) | +13.7% | 1158, 1371, 1513 / 1440, 1647, 1409 | within noise |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3.297e+04 (3.131e+04-4.051e+04) | 3.117e+04 (2.283e+04-3.998e+04) | -5.5% | 3.674e+04, 3.22e+04, 3.297e+04 / 2.83e+04, 3.55e+04, 2.953e+04 | within noise |
| conv tail 32 x 5408 bare downstream b512 / rust | 1.403e+04 (1.281e+04-2.037e+04) | 1.767e+04 (1.304e+04-1.943e+04) | +26.0% | 1.659e+04, 1.488e+04, 1.315e+04 / 1.456e+04, 1.767e+04, 1.925e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 1283 (858.8-1505) | 1464 (1233-1669) | +14.1% | 1170, 1283, 1341 / 1481, 1451, 1432 | separated, inside spread |
| conv tail 32 x 5408 bare accumulate b32 / rust | 1089 (1085-1378) | 1190 (1186-1234) | +9.2% | 1086, 1163, 1235 / 1212, 1198, 1187 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 2.214e+04 (2.08e+04-2.579e+04) | 2.102e+04 (1.965e+04-2.333e+04) | -5.1% | 2.123e+04, 2.535e+04, 2.179e+04 / 2.208e+04, 2.043e+04, 2.156e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / rust | 1.873e+04 (1.807e+04-1.953e+04) | 1.826e+04 (1.809e+04-1.933e+04) | -2.5% | 1.9e+04, 1.853e+04, 1.887e+04 / 1.821e+04, 1.818e+04, 1.907e+04 | within noise |
| conv tail 32 x 5408 transpose b32 / numpy | 1.461 (1.456-1.483) | 1.469 (1.456-1.475) | +0.5% | 1.458, 1.461, 1.473 / 1.464, 1.464, 1.475 | within noise |
| conv tail 32 x 5408 transpose b32 / rust | 1.879 (1.873-1.885) | 0.8155 (0.8132-0.8176) | -56.6% | 1.875, 1.883, 1.879 / 0.8144, 0.8168, 0.8151 | consistent |
| conv tail 32 x 5408 transpose b512 / numpy | 30 (29.85-30.08) | 30 (29.96-30) | -0.0% | 30.06, 29.93, 29.98 / 30, 29.96, 30 | within noise |
| conv tail 32 x 5408 transpose b512 / rust | 26.58 (26.35-26.85) | 11.05 (10.2-12.06) | -58.4% | 26.58, 26.71, 26.46 / 11, 11.05, 11.23 | consistent |
| conv tail 32 x 5408 add b32 / numpy | 322.4 (293.8-405.1) | 312.1 (261.9-407.9) | -3.2% | 354.5, 353.6, 305.6 / 312.1, 349.1, 294 | within noise |
| conv tail 32 x 5408 add b32 / rust | 349.9 (265.7-376.7) | 343.5 (264.8-395.6) | -1.8% | 305.4, 361, 334.6 / 331.7, 299.2, 378.1 | within noise |
| conv tail 32 x 5408 add b512 / numpy | 321.6 (305.4-416.6) | 346.1 (313.2-439.6) | +7.6% | 329.2, 309.8, 366.2 / 338.8, 393.8, 367.8 | within noise |
| conv tail 32 x 5408 add b512 / rust | 324.5 (293.6-457.5) | 394.3 (319.4-431.4) | +21.5% | 308.4, 313.6, 409.8 / 360.3, 360.6, 430.7 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 2.832 (2.812-2.845) | 2.834 (2.81-2.882) | +0.1% | 2.826, 2.844, 2.817 / 2.819, 2.844, 2.851 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.7756 (0.7695-0.7797) | 0.7817 (0.7726-0.7844) | +0.8% | 0.7736, 0.7777, 0.7741 / 0.7781, 0.7824, 0.7804 | separated, inside spread |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 15.96 (15.71-16.16) | 16.1 (15.85-16.2) | +0.8% | 16.01, 15.83, 16.05 / 16.13, 16, 15.99 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 8.675 (8.66-8.713) | 8.67 (8.657-8.699) | -0.0% | 8.687, 8.675, 8.675 / 8.666, 8.678, 8.671 | within noise |
| dense 30 x 784 bare downstream b32 / numpy | 58.07 (57.65-400.2) | 58.17 (56.49-390.6) | +0.2% | 57.89, 228.9, 58.07 / 58.31, 224.3, 57.35 | within noise |
| dense 30 x 784 bare downstream b32 / rust | 126.1 (125.5-127.1) | 126.7 (125.7-127) | +0.5% | 126.1, 126.3, 126.2 / 126.3, 126.7, 126.3 | separated, inside spread |
| dense 30 x 784 bare downstream b512 / numpy | 3188 (2579-4022) | 3409 (2893-4233) | +6.9% | 3046, 3584, 2970 / 3563, 3504, 3409 | within noise |
| dense 30 x 784 bare downstream b512 / rust | 1787 (1612-2531) | 1991 (1624-2357) | +11.4% | 1733, 2163, 1757 / 1955, 1731, 2252 | within noise |
| dense 30 x 784 bare accumulate b32 / numpy | 66.7 (65.12-399.2) | 66.15 (65.29-403.3) | -0.8% | 67.17, 66.31, 232.1 / 233.2, 65.38, 234.6 | within noise |
| dense 30 x 784 bare accumulate b32 / rust | 125.4 (124.8-126.6) | 125.6 (124.8-126.1) | +0.1% | 125.7, 125.4, 125.4 / 125.3, 125.7, 125.5 | within noise |
| dense 30 x 784 bare accumulate b512 / numpy | 1844 (1715-2044) | 1976 (1842-2065) | +7.2% | 1777, 1909, 1945 / 2009, 1858, 2005 | within noise |
| dense 30 x 784 bare accumulate b512 / rust | 2421 (2266-2738) | 2572 (2518-2720) | +6.2% | 2454, 2519, 2404 / 2561, 2645, 2546 | separated, inside spread |
| dense 30 x 784 transpose b32 / numpy | 1.4 (1.395-1.414) | 1.401 (1.388-1.414) | +0.1% | 1.409, 1.398, 1.397 / 1.403, 1.398, 1.401 | within noise |
| dense 30 x 784 transpose b32 / rust | 1.818 (1.81-1.819) | 0.834 (0.8333-0.8469) | -54.1% | 1.814, 1.817, 1.818 / 0.8337, 0.8405, 0.8358 | consistent |
| dense 30 x 784 transpose b512 / numpy | 9.013 (8.976-9.048) | 9.032 (8.959-9.061) | +0.2% | 8.998, 9.034, 8.994 / 9.05, 8.992, 9.026 | within noise |
| dense 30 x 784 transpose b512 / rust | 24.78 (24.75-25.15) | 10.67 (10.09-10.95) | -57.0% | 25, 24.77, 24.76 / 10.39, 10.8, 10.79 | consistent |
| dense 30 x 784 add b32 / numpy | 10.17 (10.07-10.57) | 10.42 (10.06-10.8) | +2.4% | 10.08, 10.37, 10.31 / 10.5, 10.43, 10.29 | within noise |
| dense 30 x 784 add b32 / rust | 9.782 (9.618-11.06) | 10.27 (9.616-12) | +5.0% | 10.08, 9.664, 10.46 / 11.33, 9.817, 10.22 | within noise |
| dense 30 x 784 add b512 / numpy | 11.4 (10.98-11.85) | 11.35 (10.8-11.91) | -0.4% | 11.69, 11.29, 11.24 / 11.62, 11.01, 11.43 | within noise |
| dense 30 x 784 add b512 / rust | 9.535 (9.271-10.04) | 9.553 (9.392-9.679) | +0.2% | 9.394, 9.781, 9.609 / 9.618, 9.472, 9.534 | within noise |
| dense 30 x 784 sum_axis0 b32 / numpy | 2.815 (2.794-2.878) | 2.813 (2.788-2.862) | -0.1% | 2.81, 2.826, 2.836 / 2.79, 2.841, 2.827 | within noise |
| dense 30 x 784 sum_axis0 b32 / rust | 0.7021 (0.6974-0.7083) | 0.7046 (0.6978-0.7059) | +0.4% | 0.6987, 0.7039, 0.705 / 0.705, 0.7052, 0.6992 | within noise |
| dense 30 x 784 sum_axis0 b512 / numpy | 15.37 (15.31-15.7) | 15.39 (15.33-15.44) | +0.1% | 15.35, 15.34, 15.57 / 15.37, 15.39, 15.4 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 7.445 (7.436-7.514) | 7.431 (7.422-7.445) | -0.2% | 7.445, 7.445, 7.475 / 7.439, 7.425, 7.43 | separated, inside spread |
| dense 10 x 30 bare downstream b32 / numpy | 5.849 (5.843-5.905) | 5.874 (5.842-5.909) | +0.4% | 5.847, 5.874, 5.851 / 5.858, 5.907, 5.859 | within noise |
| dense 10 x 30 bare downstream b32 / rust | 3.186 (3.183-3.188) | 3.858 (3.838-3.986) | +21.1% | 3.187, 3.184, 3.186 / 3.857, 3.922, 3.85 | consistent |
| dense 10 x 30 bare downstream b512 / numpy | 64.62 (64.44-64.73) | 64.66 (64.47-64.8) | +0.1% | 64.64, 64.52, 64.66 / 64.64, 64.57, 64.73 | within noise |
| dense 10 x 30 bare downstream b512 / rust | 46.03 (45.75-46.39) | 65.29 (64.65-68.48) | +41.8% | 46.16, 45.87, 46.15 / 65.29, 65.23, 66.56 | consistent |
| dense 10 x 30 bare accumulate b32 / numpy | 5.065 (5.031-5.089) | 5.059 (5.02-5.128) | -0.1% | 5.069, 5.065, 5.058 / 5.04, 5.073, 5.093 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 2.88 (2.875-2.883) | 2.882 (2.877-2.891) | +0.1% | 2.878, 2.882, 2.878 / 2.881, 2.885, 2.882 | within noise |
| dense 10 x 30 bare accumulate b512 / numpy | 32.53 (32.39-32.78) | 32.56 (32.47-32.71) | +0.1% | 32.59, 32.53, 32.52 / 32.51, 32.65, 32.6 | within noise |
| dense 10 x 30 bare accumulate b512 / rust | 45.11 (45.02-45.18) | 45.15 (45.12-45.21) | +0.1% | 45.1, 45.09, 45.13 / 45.15, 45.15, 45.17 | separated, inside spread |
| dense 10 x 30 transpose b32 / numpy | 0.8876 (0.8836-0.8923) | 0.8919 (0.8796-0.9693) | +0.5% | 0.8839, 0.8904, 0.8876 / 0.8882, 0.9296, 0.8919 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.8001 (0.7943-0.8022) | 0.503 (0.499-0.505) | -37.1% | 0.7975, 0.801, 0.7997 / 0.5025, 0.503, 0.5016 | consistent |
| dense 10 x 30 transpose b512 / numpy | 3.397 (3.36-3.408) | 3.44 (3.373-3.527) | +1.2% | 3.384, 3.395, 3.402 / 3.46, 3.449, 3.414 | separated, inside spread |
| dense 10 x 30 transpose b512 / rust | 8.568 (8.508-8.585) | 3.821 (3.787-3.84) | -55.4% | 8.565, 8.585, 8.539 / 3.831, 3.802, 3.815 | consistent |
| dense 10 x 30 add b32 / numpy | 0.8947 (0.886-0.9201) | 0.8951 (0.891-0.9068) | +0.0% | 0.9097, 0.8943, 0.888 / 0.8987, 0.8997, 0.8928 | within noise |
| dense 10 x 30 add b32 / rust | 0.3775 (0.3763-0.3813) | 0.3923 (0.3812-0.3946) | +3.9% | 0.3796, 0.3781, 0.3771 / 0.3928, 0.3931, 0.3866 | consistent |
| dense 10 x 30 add b512 / numpy | 0.9177 (0.9112-0.9304) | 0.92 (0.9106-0.9305) | +0.3% | 0.9154, 0.9186, 0.9214 / 0.92, 0.9227, 0.9205 | within noise |
| dense 10 x 30 add b512 / rust | 0.3992 (0.3982-0.4146) | 0.4153 (0.4097-0.4183) | +4.0% | 0.3988, 0.3987, 0.4071 / 0.4104, 0.4171, 0.4156 | separated, inside spread |
| dense 10 x 30 sum_axis0 b32 / numpy | 2.457 (2.444-2.474) | 2.46 (2.428-2.487) | +0.1% | 2.446, 2.464, 2.465 / 2.474, 2.467, 2.444 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.5299 (0.5275-0.5383) | 0.5331 (0.5287-0.5344) | +0.6% | 0.5329, 0.5308, 0.5288 / 0.5331, 0.5298, 0.5341 | within noise |
| dense 10 x 30 sum_axis0 b512 / numpy | 12.22 (12.16-12.57) | 12.21 (12.15-12.25) | -0.1% | 12.21, 12.2, 12.39 / 12.23, 12.18, 12.19 | within noise |
| dense 10 x 30 sum_axis0 b512 / rust | 4.644 (4.639-4.647) | 4.646 (4.638-4.652) | +0.0% | 4.643, 4.642, 4.644 / 4.648, 4.647, 4.641 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 745.8 (743.6-757.5) | 749.3 (747.7-759.4) | +0.5% | 744, 756.6, 745.8 / 754.5, 753.5, 748.2 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 807.4 (802.4-810.9) | 812 (810.3-813) | +0.6% | 807.3, 809.9, 804.8 / 811.4, 812.8, 811 | separated, inside spread |
| attention 16 x 32 forward_batch b512 / numpy | 2.308e+04 (2.134e+04-2.822e+04) | 2.265e+04 (2.128e+04-2.439e+04) | -1.9% | 2.308e+04, 2.327e+04, 2.478e+04 / 2.284e+04, 2.236e+04, 2.265e+04 | separated, inside spread |
| attention 16 x 32 forward_batch b512 / rust | 1.657e+04 (1.612e+04-1.706e+04) | 1.618e+04 (1.579e+04-1.706e+04) | -2.3% | 1.689e+04, 1.672e+04, 1.621e+04 / 1.596e+04, 1.654e+04, 1.662e+04 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 759.3 (751.9-786.5) | 755.3 (753.6-757.1) | -0.5% | 756, 762.2, 769.2 / 755.4, 754.1, 756.4 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / rust | 795.4 (791.9-798.2) | 760.2 (759-764.1) | -4.4% | 798, 793.9, 794.2 / 760.3, 761.6, 760.1 | consistent |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 2.713e+04 (2.626e+04-3.189e+04) | 2.703e+04 (2.519e+04-2.792e+04) | -0.3% | 2.713e+04, 2.938e+04, 2.702e+04 / 2.547e+04, 2.722e+04, 2.761e+04 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / rust | 1.924e+04 (1.853e+04-2.067e+04) | 1.84e+04 (1.807e+04-1.892e+04) | -4.3% | 1.96e+04, 1.94e+04, 1.924e+04 / 1.841e+04, 1.849e+04, 1.84e+04 | consistent |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 590.9 (586.4-598.3) | 585.2 (583.9-599.5) | -1.0% | 588.8, 589.3, 595.1 / 587.9, 584.6, 591.7 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 512.8 (509.3-516.5) | 459.9 (458.2-462.8) | -10.3% | 512.9, 512.5, 513.5 / 459.9, 462.6, 458.3 | consistent |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 3.699e+04 (3.26e+04-4.255e+04) | 4.211e+04 (3.67e+04-4.391e+04) | +13.8% | 3.617e+04, 3.933e+04, 3.745e+04 / 4.211e+04, 4.377e+04, 3.893e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 2.792e+04 (2.132e+04-3.148e+04) | 3.547e+04 (2.537e+04-3.772e+04) | +27.0% | 2.605e+04, 2.951e+04, 2.743e+04 / 3.609e+04, 3e+04, 3.634e+04 | separated, inside spread |
