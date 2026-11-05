Old `f081ecf` against new `f081ecf`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py scaling --repeats 1` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `7a3f0df0ecd3`) on both sides. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.32; busy processes: none. Each row pools 1 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: 72 rows, all within noise
- 73 rows within noise, max |Δ| 29.8%
- spread of per-pass medians over 145 rows: median 1.2%, 90th percentile 6.7%, max 35.0%
- pass shifts (median over rows of pass median / pooled median): 1 -0.1%, 2 +0.1%

### per call

| case | median (min-max) µs | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 2048x2048x512, 1 thread, warm / rust | 9.2e+04 (9.143e+04-9.256e+04) | 9.143e+04, 9.256e+04 | 1.2% |
| 2048x2048x512, 1 thread, cold (20 ms idle) / rust | 8.56e+04 (8.515e+04-8.605e+04) | 8.515e+04, 8.605e+04 | 1.1% |
| 2048x2048x512, 2 threads, warm / rust | 4.771e+04 (4.733e+04-4.81e+04) | 4.733e+04, 4.81e+04 | 1.6% |
| 2048x2048x512, 2 threads, cold (20 ms idle) / rust | 4.821e+04 (4.774e+04-4.867e+04) | 4.867e+04, 4.774e+04 | 1.9% |
| 2048x2048x512, 4 threads, warm / rust | 2.827e+04 (2.82e+04-2.834e+04) | 2.82e+04, 2.834e+04 | 0.5% |
| 2048x2048x512, 4 threads, cold (20 ms idle) / rust | 2.72e+04 (2.717e+04-2.722e+04) | 2.722e+04, 2.717e+04 | 0.2% |
| 2048x2048x512, 8 threads, warm / rust | 2.127e+04 (2.079e+04-2.176e+04) | 2.176e+04, 2.079e+04 | 4.6% |
| 2048x2048x512, 8 threads, cold (20 ms idle) / rust | 2.174e+04 (2.122e+04-2.227e+04) | 2.122e+04, 2.227e+04 | 4.8% |
| 2048x2048x512, 1 thread, warm / numpy (control) | 6.923e+04 (6.874e+04-6.973e+04) | 6.973e+04, 6.874e+04 | 1.4% |
| 2048x2048x512, 1 thread, cold (20 ms idle) / numpy (control) | 6.756e+04 (6.753e+04-6.758e+04) | 6.758e+04, 6.753e+04 | 0.1% |
| 2048x2048x512, 2 threads, warm / numpy (control) | 3.548e+04 (3.545e+04-3.551e+04) | 3.551e+04, 3.545e+04 | 0.1% |
| 2048x2048x512, 2 threads, cold (20 ms idle) / numpy (control) | 3.442e+04 (3.427e+04-3.458e+04) | 3.427e+04, 3.458e+04 | 0.9% |
| 2048x2048x512, 4 threads, warm / numpy (control) | 1.91e+04 (1.895e+04-1.926e+04) | 1.895e+04, 1.926e+04 | 1.6% |
| 2048x2048x512, 4 threads, cold (20 ms idle) / numpy (control) | 1.992e+04 (1.986e+04-1.999e+04) | 1.986e+04, 1.999e+04 | 0.7% |
| 2048x2048x512, 8 threads, warm / numpy (control) | 2.216e+04 (2.188e+04-2.245e+04) | 2.188e+04, 2.245e+04 | 2.6% |
| 2048x2048x512, 8 threads, cold (20 ms idle) / numpy (control) | 2.143e+04 (2.086e+04-2.199e+04) | 2.086e+04, 2.199e+04 | 5.3% |
| 2048x512x2048, 1 thread, warm / rust | 1.06e+05 (1.06e+05-1.06e+05) | 1.06e+05, 1.06e+05 | 0.0% |
| 2048x512x2048, 1 thread, cold (20 ms idle) / rust | 1.054e+05 (1.036e+05-1.073e+05) | 1.036e+05, 1.073e+05 | 3.5% |
| 2048x512x2048, 2 threads, warm / rust | 5.886e+04 (5.88e+04-5.892e+04) | 5.88e+04, 5.892e+04 | 0.2% |
| 2048x512x2048, 2 threads, cold (20 ms idle) / rust | 5.818e+04 (5.772e+04-5.864e+04) | 5.772e+04, 5.864e+04 | 1.6% |
| 2048x512x2048, 4 threads, warm / rust | 4.021e+04 (3.998e+04-4.045e+04) | 4.045e+04, 3.998e+04 | 1.2% |
| 2048x512x2048, 4 threads, cold (20 ms idle) / rust | 3.759e+04 (3.745e+04-3.773e+04) | 3.745e+04, 3.773e+04 | 0.8% |
| 2048x512x2048, 8 threads, warm / rust | 3.439e+04 (3.404e+04-3.473e+04) | 3.404e+04, 3.473e+04 | 2.0% |
| 2048x512x2048, 8 threads, cold (20 ms idle) / rust | 3.355e+04 (3.335e+04-3.374e+04) | 3.335e+04, 3.374e+04 | 1.2% |
| 2048x512x2048, 1 thread, warm / numpy (control) | 7.035e+04 (7.022e+04-7.048e+04) | 7.022e+04, 7.048e+04 | 0.4% |
| 2048x512x2048, 1 thread, cold (20 ms idle) / numpy (control) | 6.918e+04 (6.883e+04-6.953e+04) | 6.953e+04, 6.883e+04 | 1.0% |
| 2048x512x2048, 2 threads, warm / numpy (control) | 3.635e+04 (3.627e+04-3.642e+04) | 3.642e+04, 3.627e+04 | 0.4% |
| 2048x512x2048, 2 threads, cold (20 ms idle) / numpy (control) | 3.563e+04 (3.557e+04-3.569e+04) | 3.569e+04, 3.557e+04 | 0.3% |
| 2048x512x2048, 4 threads, warm / numpy (control) | 2.087e+04 (2.081e+04-2.094e+04) | 2.081e+04, 2.094e+04 | 0.6% |
| 2048x512x2048, 4 threads, cold (20 ms idle) / numpy (control) | 2.166e+04 (2.165e+04-2.167e+04) | 2.165e+04, 2.167e+04 | 0.1% |
| 2048x512x2048, 8 threads, warm / numpy (control) | 2.485e+04 (2.403e+04-2.568e+04) | 2.568e+04, 2.403e+04 | 6.7% |
| 2048x512x2048, 8 threads, cold (20 ms idle) / numpy (control) | 2.5e+04 (2.491e+04-2.509e+04) | 2.509e+04, 2.491e+04 | 0.7% |
| 512x2048x2048, 1 thread, warm / rust | 9.045e+04 (8.905e+04-9.184e+04) | 8.905e+04, 9.184e+04 | 3.1% |
| 512x2048x2048, 1 thread, cold (20 ms idle) / rust | 9.21e+04 (9.151e+04-9.269e+04) | 9.269e+04, 9.151e+04 | 1.3% |
| 512x2048x2048, 2 threads, warm / rust | 5.076e+04 (5.012e+04-5.14e+04) | 5.012e+04, 5.14e+04 | 2.5% |
| 512x2048x2048, 2 threads, cold (20 ms idle) / rust | 5.026e+04 (5.005e+04-5.046e+04) | 5.046e+04, 5.005e+04 | 0.8% |
| 512x2048x2048, 4 threads, warm / rust | 3.652e+04 (3.607e+04-3.696e+04) | 3.607e+04, 3.696e+04 | 2.4% |
| 512x2048x2048, 4 threads, cold (20 ms idle) / rust | 3.437e+04 (3.435e+04-3.439e+04) | 3.435e+04, 3.439e+04 | 0.1% |
| 512x2048x2048, 8 threads, warm / rust | 4.711e+04 (4.675e+04-4.747e+04) | 4.675e+04, 4.747e+04 | 1.5% |
| 512x2048x2048, 8 threads, cold (20 ms idle) / rust | 4.565e+04 (4.524e+04-4.605e+04) | 4.524e+04, 4.605e+04 | 1.8% |
| 512x2048x2048, 1 thread, warm / numpy (control) | 6.957e+04 (6.889e+04-7.025e+04) | 6.889e+04, 7.025e+04 | 2.0% |
| 512x2048x2048, 1 thread, cold (20 ms idle) / numpy (control) | 6.776e+04 (6.742e+04-6.811e+04) | 6.811e+04, 6.742e+04 | 1.0% |
| 512x2048x2048, 2 threads, warm / numpy (control) | 3.533e+04 (3.519e+04-3.546e+04) | 3.519e+04, 3.546e+04 | 0.8% |
| 512x2048x2048, 2 threads, cold (20 ms idle) / numpy (control) | 3.473e+04 (3.458e+04-3.489e+04) | 3.458e+04, 3.489e+04 | 0.9% |
| 512x2048x2048, 4 threads, warm / numpy (control) | 1.978e+04 (1.975e+04-1.981e+04) | 1.975e+04, 1.981e+04 | 0.3% |
| 512x2048x2048, 4 threads, cold (20 ms idle) / numpy (control) | 2.059e+04 (2.055e+04-2.062e+04) | 2.055e+04, 2.062e+04 | 0.3% |
| 512x2048x2048, 8 threads, warm / numpy (control) | 1.534e+04 (1.525e+04-1.543e+04) | 1.525e+04, 1.543e+04 | 1.2% |
| 512x2048x2048, 8 threads, cold (20 ms idle) / numpy (control) | 1.347e+04 (1.332e+04-1.363e+04) | 1.332e+04, 1.363e+04 | 2.3% |
| 64x256x1024, 1 thread, warm / rust | 857.5 (855.7-859.3) | 855.7, 859.3 | 0.4% |
| 64x256x1024, 1 thread, cold (20 ms idle) / rust | 4453 (4384-4522) | 4384, 4522 | 3.1% |
| 64x256x1024, 2 threads, warm / rust | 915.2 (908-922.5) | 922.5, 908 | 1.6% |
| 64x256x1024, 2 threads, cold (20 ms idle) / rust | 4705 (4573-4838) | 4573, 4838 | 5.6% |
| 64x256x1024, 4 threads, warm / rust | 728.4 (671.6-785.2) | 785.2, 671.6 | 15.6% |
| 64x256x1024, 4 threads, cold (20 ms idle) / rust | 3260 (3057-3462) | 3462, 3057 | 12.4% |
| 64x256x1024, 8 threads, warm / rust | 452.3 (430.1-474.6) | 430.1, 474.6 | 9.8% |
| 64x256x1024, 8 threads, cold (20 ms idle) / rust | 1990 (1831-2148) | 2148, 1831 | 15.9% |
| 64x256x1024, 1 thread, warm / numpy (control) | 602.1 (599.5-604.6) | 599.5, 604.6 | 0.9% |
| 64x256x1024, 1 thread, cold (20 ms idle) / numpy (control) | 3681 (3652-3710) | 3652, 3710 | 1.6% |
| 64x256x1024, 2 threads, warm / numpy (control) | 334.6 (333.8-335.4) | 333.8, 335.4 | 0.5% |
| 64x256x1024, 2 threads, cold (20 ms idle) / numpy (control) | 346.3 (344.4-348.2) | 348.2, 344.4 | 1.1% |
| 64x256x1024, 4 threads, warm / numpy (control) | 183.4 (182.9-183.9) | 183.9, 182.9 | 0.5% |
| 64x256x1024, 4 threads, cold (20 ms idle) / numpy (control) | 195.3 (194.5-196.2) | 196.2, 194.5 | 0.9% |
| 64x256x1024, 8 threads, warm / numpy (control) | 167.5 (166.4-168.6) | 166.4, 168.6 | 1.3% |
| 64x256x1024, 8 threads, cold (20 ms idle) / numpy (control) | 167.9 (167.7-168.2) | 167.7, 168.2 | 0.3% |
| 32x128x1352, 1 thread, warm / rust | 248.2 (245-251.5) | 245, 251.5 | 2.6% |
| 32x128x1352, 1 thread, cold (20 ms idle) / rust | 1242 (1226-1259) | 1226, 1259 | 2.7% |
| 32x128x1352, 2 threads, warm / rust | 199.8 (199.4-200.1) | 200.1, 199.4 | 0.4% |
| 32x128x1352, 2 threads, cold (20 ms idle) / rust | 989.7 (986.5-992.9) | 986.5, 992.9 | 0.6% |
| 32x128x1352, 4 threads, warm / rust | 129.6 (128.6-130.5) | 128.6, 130.5 | 1.5% |
| 32x128x1352, 4 threads, cold (20 ms idle) / rust | 795.2 (764.9-825.5) | 825.5, 764.9 | 7.6% |
| 32x128x1352, 8 threads, warm / rust | 134.7 (134.7-134.7) | 134.7, 134.7 | 0.0% |
| 32x128x1352, 8 threads, cold (20 ms idle) / rust | 680.2 (623.3-737.1) | 737.1, 623.3 | 16.7% |
| 32x128x1352, 1 thread, warm / numpy (control) | 239.5 (239.5-239.5) | 239.5, 239.5 | 0.0% |
| 32x128x1352, 1 thread, cold (20 ms idle) / numpy (control) | 1473 (1460-1487) | 1460, 1487 | 1.8% |
| 32x128x1352, 2 threads, warm / numpy (control) | 138.9 (138.8-138.9) | 138.9, 138.8 | 0.1% |
| 32x128x1352, 2 threads, cold (20 ms idle) / numpy (control) | 147.9 (147.4-148.4) | 148.4, 147.4 | 0.7% |
| 32x128x1352, 4 threads, warm / numpy (control) | 105.4 (105.3-105.5) | 105.3, 105.5 | 0.2% |
| 32x128x1352, 4 threads, cold (20 ms idle) / numpy (control) | 112.1 (112-112.2) | 112, 112.2 | 0.1% |
| 32x128x1352, 8 threads, warm / numpy (control) | 71.41 (71.36-71.47) | 71.36, 71.47 | 0.2% |
| 32x128x1352, 8 threads, cold (20 ms idle) / numpy (control) | 79.83 (78.21-81.45) | 81.45, 78.21 | 4.1% |
| 32x30x784, 1 thread, warm / rust | 32.2 (31.76-32.64) | 31.76, 32.64 | 2.7% |
| 32x30x784, 1 thread, cold (20 ms idle) / rust | 167.9 (162.2-173.6) | 162.2, 173.6 | 6.8% |
| 32x30x784, 2 threads, warm / rust | 48.83 (48.5-49.16) | 49.16, 48.5 | 1.3% |
| 32x30x784, 2 threads, cold (20 ms idle) / rust | 330.2 (326.3-334) | 334, 326.3 | 2.3% |
| 32x30x784, 4 threads, warm / rust | 57.95 (57.71-58.18) | 57.71, 58.18 | 0.8% |
| 32x30x784, 4 threads, cold (20 ms idle) / rust | 386.3 (373.3-399.3) | 399.3, 373.3 | 6.7% |
| 32x30x784, 8 threads, warm / rust | 87.76 (85.51-90.01) | 90.01, 85.51 | 5.1% |
| 32x30x784, 8 threads, cold (20 ms idle) / rust | 490 (480.2-499.8) | 480.2, 499.8 | 4.0% |
| 32x30x784, 1 thread, warm / numpy (control) | 41.05 (40.87-41.23) | 41.23, 40.87 | 0.9% |
| 32x30x784, 1 thread, cold (20 ms idle) / numpy (control) | 295.4 (291.1-299.8) | 299.8, 291.1 | 3.0% |
| 32x30x784, 2 threads, warm / numpy (control) | 23.2 (22.82-23.57) | 22.82, 23.57 | 3.2% |
| 32x30x784, 2 threads, cold (20 ms idle) / numpy (control) | 40.91 (40.74-41.08) | 41.08, 40.74 | 0.8% |
| 32x30x784, 4 threads, warm / numpy (control) | 22.87 (22.85-22.88) | 22.85, 22.88 | 0.1% |
| 32x30x784, 4 threads, cold (20 ms idle) / numpy (control) | 39.94 (39.62-40.27) | 39.62, 40.27 | 1.6% |
| 32x30x784, 8 threads, warm / numpy (control) | 22.79 (22.76-22.82) | 22.82, 22.76 | 0.3% |
| 32x30x784, 8 threads, cold (20 ms idle) / numpy (control) | 41.12 (40.67-41.57) | 40.67, 41.57 | 2.2% |
| dense 30 x 784|forward_batch|512, 1 thread, warm / rust | 603.6 (593.8-613.3) | 593.8, 613.3 | 3.2% |
| dense 30 x 784|forward_batch|512, 1 thread, cold (20 ms idle) / rust | 3472 (3391-3554) | 3554, 3391 | 4.7% |
| dense 30 x 784|forward_batch|512, 2 threads, warm / rust | 436.6 (412.7-460.5) | 412.7, 460.5 | 10.9% |
| dense 30 x 784|forward_batch|512, 2 threads, cold (20 ms idle) / rust | 2227 (2182-2273) | 2182, 2273 | 4.1% |
| dense 30 x 784|forward_batch|512, 4 threads, warm / rust | 308.7 (306.8-310.7) | 306.8, 310.7 | 1.3% |
| dense 30 x 784|forward_batch|512, 4 threads, cold (20 ms idle) / rust | 1365 (1332-1398) | 1332, 1398 | 4.9% |
| dense 30 x 784|forward_batch|512, 8 threads, warm / rust | 254.8 (248.5-261) | 261, 248.5 | 4.9% |
| dense 30 x 784|forward_batch|512, 8 threads, cold (20 ms idle) / rust | 1090 (1083-1097) | 1083, 1097 | 1.3% |
| dense 30 x 784|forward_batch|512, 1 thread, warm / numpy (control) | 639.2 (635.7-642.7) | 642.7, 635.7 | 1.1% |
| dense 30 x 784|forward_batch|512, 1 thread, cold (20 ms idle) / numpy (control) | 3912 (3903-3921) | 3903, 3921 | 0.4% |
| dense 30 x 784|forward_batch|512, 2 threads, warm / numpy (control) | 403.3 (401.2-405.3) | 401.2, 405.3 | 1.0% |
| dense 30 x 784|forward_batch|512, 2 threads, cold (20 ms idle) / numpy (control) | 435.4 (434.8-435.9) | 435.9, 434.8 | 0.3% |
| dense 30 x 784|forward_batch|512, 4 threads, warm / numpy (control) | 266.2 (263.9-268.6) | 268.6, 263.9 | 1.8% |
| dense 30 x 784|forward_batch|512, 4 threads, cold (20 ms idle) / numpy (control) | 298.8 (296.6-301.1) | 301.1, 296.6 | 1.5% |
| dense 30 x 784|forward_batch|512, 8 threads, warm / numpy (control) | 228.6 (228.2-229) | 228.2, 229 | 0.4% |
| dense 30 x 784|forward_batch|512, 8 threads, cold (20 ms idle) / numpy (control) | 254.8 (254.8-254.9) | 254.8, 254.9 | 0.0% |
| conv tail 32 x 5408|downstream_batch|512, 1 thread, warm / rust | 4323 (4313-4334) | 4313, 4334 | 0.5% |
| conv tail 32 x 5408|downstream_batch|512, 1 thread, cold (20 ms idle) / rust | 1.851e+04 (1.767e+04-1.935e+04) | 1.767e+04, 1.935e+04 | 9.1% |
| conv tail 32 x 5408|downstream_batch|512, 2 threads, warm / rust | 2822 (2815-2829) | 2815, 2829 | 0.5% |
| conv tail 32 x 5408|downstream_batch|512, 2 threads, cold (20 ms idle) / rust | 1.178e+04 (9901-1.366e+04) | 1.366e+04, 9901 | 31.9% |
| conv tail 32 x 5408|downstream_batch|512, 4 threads, warm / rust | 2440 (2436-2444) | 2444, 2436 | 0.3% |
| conv tail 32 x 5408|downstream_batch|512, 4 threads, cold (20 ms idle) / rust | 6122 (5050-7193) | 7193, 5050 | 35.0% |
| conv tail 32 x 5408|downstream_batch|512, 8 threads, warm / rust | 2459 (2446-2472) | 2472, 2446 | 1.0% |
| conv tail 32 x 5408|downstream_batch|512, 8 threads, cold (20 ms idle) / rust | 6045 (6044-6045) | 6044, 6045 | 0.0% |
| conv tail 32 x 5408|downstream_batch|512, 1 thread, warm / numpy (control) | 4114 (4110-4118) | 4118, 4110 | 0.2% |
| conv tail 32 x 5408|downstream_batch|512, 1 thread, cold (20 ms idle) / numpy (control) | 1.859e+04 (1.82e+04-1.899e+04) | 1.82e+04, 1.899e+04 | 4.3% |
| conv tail 32 x 5408|downstream_batch|512, 2 threads, warm / numpy (control) | 2848 (2831-2865) | 2831, 2865 | 1.2% |
| conv tail 32 x 5408|downstream_batch|512, 2 threads, cold (20 ms idle) / numpy (control) | 2897 (2894-2899) | 2899, 2894 | 0.2% |
| conv tail 32 x 5408|downstream_batch|512, 4 threads, warm / numpy (control) | 2714 (2698-2730) | 2730, 2698 | 1.2% |
| conv tail 32 x 5408|downstream_batch|512, 4 threads, cold (20 ms idle) / numpy (control) | 2757 (2749-2765) | 2749, 2765 | 0.6% |
| conv tail 32 x 5408|downstream_batch|512, 8 threads, warm / numpy (control) | 3192 (3190-3194) | 3190, 3194 | 0.1% |
| conv tail 32 x 5408|downstream_batch|512, 8 threads, cold (20 ms idle) / numpy (control) | 3238 (3230-3245) | 3245, 3230 | 0.4% |
| conv 26x26x8, 8 ch|downstream_batch|512, 1 thread, warm / rust | 2.733e+04 (2.715e+04-2.752e+04) | 2.715e+04, 2.752e+04 | 1.4% |
| conv 26x26x8, 8 ch|downstream_batch|512, 1 thread, cold (20 ms idle) / rust | 2.669e+04 (2.644e+04-2.695e+04) | 2.695e+04, 2.644e+04 | 1.9% |
| conv 26x26x8, 8 ch|downstream_batch|512, 2 threads, warm / rust | 1.5e+04 (1.496e+04-1.505e+04) | 1.505e+04, 1.496e+04 | 0.6% |
| conv 26x26x8, 8 ch|downstream_batch|512, 2 threads, cold (20 ms idle) / rust | 1.672e+04 (1.668e+04-1.676e+04) | 1.668e+04, 1.676e+04 | 0.5% |
| conv 26x26x8, 8 ch|downstream_batch|512, 4 threads, warm / rust | 8199 (8184-8214) | 8214, 8184 | 0.4% |
| conv 26x26x8, 8 ch|downstream_batch|512, 4 threads, cold (20 ms idle) / rust | 1.033e+04 (9331-1.134e+04) | 9331, 1.134e+04 | 19.4% |
| conv 26x26x8, 8 ch|downstream_batch|512, 8 threads, warm / rust | 5628 (5206-6050) | 6050, 5206 | 15.0% |
| conv 26x26x8, 8 ch|downstream_batch|512, 8 threads, cold (20 ms idle) / rust | 1.677e+04 (1.455e+04-1.899e+04) | 1.899e+04, 1.455e+04 | 26.5% |
| conv 26x26x8, 8 ch|downstream_batch|512, 1 thread, warm / numpy (control) | 1.138e+05 (1.137e+05-1.138e+05) | 1.137e+05, 1.138e+05 | 0.1% |
| conv 26x26x8, 8 ch|downstream_batch|512, 1 thread, cold (20 ms idle) / numpy (control) | 1.134e+05 (1.133e+05-1.135e+05) | 1.133e+05, 1.135e+05 | 0.2% |
| conv 26x26x8, 8 ch|downstream_batch|512, 2 threads, warm / numpy (control) | 1.157e+05 (1.153e+05-1.161e+05) | 1.161e+05, 1.153e+05 | 0.7% |
| conv 26x26x8, 8 ch|downstream_batch|512, 2 threads, cold (20 ms idle) / numpy (control) | 1.153e+05 (1.153e+05-1.154e+05) | 1.154e+05, 1.153e+05 | 0.1% |
| conv 26x26x8, 8 ch|downstream_batch|512, 4 threads, warm / numpy (control) | 1.146e+05 (1.141e+05-1.152e+05) | 1.152e+05, 1.141e+05 | 0.9% |
| conv 26x26x8, 8 ch|downstream_batch|512, 4 threads, cold (20 ms idle) / numpy (control) | 1.15e+05 (1.14e+05-1.16e+05) | 1.16e+05, 1.14e+05 | 1.7% |
| conv 26x26x8, 8 ch|downstream_batch|512, 8 threads, warm / numpy (control) | 1.168e+05 (1.164e+05-1.172e+05) | 1.172e+05, 1.164e+05 | 0.7% |
| conv 26x26x8, 8 ch|downstream_batch|512, 8 threads, cold (20 ms idle) / numpy (control) | 1.161e+05 (1.154e+05-1.169e+05) | 1.154e+05, 1.169e+05 | 1.3% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 27.8 (27.8-27.8) | 27.8, 27.8 | 0.0% |
