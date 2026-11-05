Old `4176d10` against new `4176d10`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py scaling --threads 1 2 4 --repeats 1` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `17d1c27f71b0`) on both sides. Machine check: profile: identity matches (raspberry-pi-5.json); passes peaked at 52.9-53.5 C; max 1-min load 0.33; busy processes: none. Each row pools 1 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: 54 rows, all within noise
- 55 rows within noise, max |Δ| 64.8%
- spread of per-pass medians over 109 rows: median 3.3%, 90th percentile 20.6%, max 48.9%
- pass shifts (median over rows of pass median / pooled median): 1 +0.2%, 2 -0.2%

### per call

| case | median (min-max) µs | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 2048x2048x512, 1 thread, warm / rust | 3.547e+05 (3.487e+05-3.607e+05) | 3.607e+05, 3.487e+05 | 3.4% |
| 2048x2048x512, 1 thread, cold (20 ms idle) / rust | 3.416e+05 (3.373e+05-3.46e+05) | 3.46e+05, 3.373e+05 | 2.5% |
| 2048x2048x512, 2 threads, warm / rust | 2.239e+05 (2.179e+05-2.298e+05) | 2.298e+05, 2.179e+05 | 5.4% |
| 2048x2048x512, 2 threads, cold (20 ms idle) / rust | 2.171e+05 (2.063e+05-2.279e+05) | 2.279e+05, 2.063e+05 | 10.0% |
| 2048x2048x512, 4 threads, warm / rust | 3.452e+05 (3.431e+05-3.473e+05) | 3.431e+05, 3.473e+05 | 1.2% |
| 2048x2048x512, 4 threads, cold (20 ms idle) / rust | 4.129e+05 (3.963e+05-4.294e+05) | 3.963e+05, 4.294e+05 | 8.0% |
| 2048x2048x512, 1 thread, warm / numpy (control) | 2.843e+05 (2.827e+05-2.858e+05) | 2.858e+05, 2.827e+05 | 1.1% |
| 2048x2048x512, 1 thread, cold (20 ms idle) / numpy (control) | 2.856e+05 (2.835e+05-2.878e+05) | 2.878e+05, 2.835e+05 | 1.5% |
| 2048x2048x512, 2 threads, warm / numpy (control) | 1.846e+05 (1.837e+05-1.854e+05) | 1.837e+05, 1.854e+05 | 0.9% |
| 2048x2048x512, 2 threads, cold (20 ms idle) / numpy (control) | 1.809e+05 (1.791e+05-1.827e+05) | 1.791e+05, 1.827e+05 | 2.0% |
| 2048x2048x512, 4 threads, warm / numpy (control) | 2.67e+05 (2.495e+05-2.845e+05) | 2.495e+05, 2.845e+05 | 13.1% |
| 2048x2048x512, 4 threads, cold (20 ms idle) / numpy (control) | 2.902e+05 (2.706e+05-3.098e+05) | 2.706e+05, 3.098e+05 | 13.5% |
| 2048x512x2048, 1 thread, warm / rust | 3.801e+05 (3.769e+05-3.833e+05) | 3.769e+05, 3.833e+05 | 1.7% |
| 2048x512x2048, 1 thread, cold (20 ms idle) / rust | 3.824e+05 (3.809e+05-3.839e+05) | 3.839e+05, 3.809e+05 | 0.8% |
| 2048x512x2048, 2 threads, warm / rust | 2.459e+05 (2.435e+05-2.484e+05) | 2.435e+05, 2.484e+05 | 2.0% |
| 2048x512x2048, 2 threads, cold (20 ms idle) / rust | 2.517e+05 (2.466e+05-2.568e+05) | 2.568e+05, 2.466e+05 | 4.0% |
| 2048x512x2048, 4 threads, warm / rust | 3.123e+05 (3.034e+05-3.211e+05) | 3.211e+05, 3.034e+05 | 5.7% |
| 2048x512x2048, 4 threads, cold (20 ms idle) / rust | 2.972e+05 (2.746e+05-3.199e+05) | 2.746e+05, 3.199e+05 | 15.2% |
| 2048x512x2048, 1 thread, warm / numpy (control) | 2.906e+05 (2.905e+05-2.906e+05) | 2.906e+05, 2.905e+05 | 0.0% |
| 2048x512x2048, 1 thread, cold (20 ms idle) / numpy (control) | 2.927e+05 (2.905e+05-2.95e+05) | 2.95e+05, 2.905e+05 | 1.5% |
| 2048x512x2048, 2 threads, warm / numpy (control) | 2.423e+05 (2.364e+05-2.482e+05) | 2.364e+05, 2.482e+05 | 4.9% |
| 2048x512x2048, 2 threads, cold (20 ms idle) / numpy (control) | 2.394e+05 (2.323e+05-2.465e+05) | 2.465e+05, 2.323e+05 | 5.9% |
| 2048x512x2048, 4 threads, warm / numpy (control) | 3.317e+05 (3.154e+05-3.481e+05) | 3.154e+05, 3.481e+05 | 9.9% |
| 2048x512x2048, 4 threads, cold (20 ms idle) / numpy (control) | 3.208e+05 (2.98e+05-3.435e+05) | 2.98e+05, 3.435e+05 | 14.2% |
| 512x2048x2048, 1 thread, warm / rust | 4.295e+05 (4.239e+05-4.351e+05) | 4.351e+05, 4.239e+05 | 2.6% |
| 512x2048x2048, 1 thread, cold (20 ms idle) / rust | 4.257e+05 (4.099e+05-4.414e+05) | 4.099e+05, 4.414e+05 | 7.4% |
| 512x2048x2048, 2 threads, warm / rust | 3.252e+05 (3.042e+05-3.461e+05) | 3.042e+05, 3.461e+05 | 12.9% |
| 512x2048x2048, 2 threads, cold (20 ms idle) / rust | 3.353e+05 (3.344e+05-3.363e+05) | 3.363e+05, 3.344e+05 | 0.5% |
| 512x2048x2048, 4 threads, warm / rust | 4.789e+05 (4.718e+05-4.859e+05) | 4.859e+05, 4.718e+05 | 3.0% |
| 512x2048x2048, 4 threads, cold (20 ms idle) / rust | 5.311e+05 (5.198e+05-5.425e+05) | 5.425e+05, 5.198e+05 | 4.3% |
| 512x2048x2048, 1 thread, warm / numpy (control) | 2.907e+05 (2.86e+05-2.954e+05) | 2.86e+05, 2.954e+05 | 3.2% |
| 512x2048x2048, 1 thread, cold (20 ms idle) / numpy (control) | 2.89e+05 (2.849e+05-2.931e+05) | 2.931e+05, 2.849e+05 | 2.9% |
| 512x2048x2048, 2 threads, warm / numpy (control) | 2.119e+05 (1.96e+05-2.278e+05) | 2.278e+05, 1.96e+05 | 15.0% |
| 512x2048x2048, 2 threads, cold (20 ms idle) / numpy (control) | 2.209e+05 (2.068e+05-2.349e+05) | 2.068e+05, 2.349e+05 | 12.8% |
| 512x2048x2048, 4 threads, warm / numpy (control) | 2.348e+05 (1.979e+05-2.718e+05) | 1.979e+05, 2.718e+05 | 31.4% |
| 512x2048x2048, 4 threads, cold (20 ms idle) / numpy (control) | 2.279e+05 (1.933e+05-2.626e+05) | 2.626e+05, 1.933e+05 | 30.4% |
| 64x256x1024, 1 thread, warm / rust | 2394 (2331-2457) | 2457, 2331 | 5.3% |
| 64x256x1024, 1 thread, cold (20 ms idle) / rust | 2490 (2490-2491) | 2491, 2490 | 0.0% |
| 64x256x1024, 2 threads, warm / rust | 3153 (3133-3173) | 3133, 3173 | 1.3% |
| 64x256x1024, 2 threads, cold (20 ms idle) / rust | 3030 (2898-3162) | 2898, 3162 | 8.7% |
| 64x256x1024, 4 threads, warm / rust | 1660 (1262-2059) | 2059, 1262 | 48.0% |
| 64x256x1024, 4 threads, cold (20 ms idle) / rust | 2245 (2098-2391) | 2391, 2098 | 13.0% |
| 64x256x1024, 1 thread, warm / numpy (control) | 2300 (2278-2323) | 2323, 2278 | 2.0% |
| 64x256x1024, 1 thread, cold (20 ms idle) / numpy (control) | 2411 (2286-2537) | 2286, 2537 | 10.4% |
| 64x256x1024, 2 threads, warm / numpy (control) | 1326 (1249-1404) | 1249, 1404 | 11.7% |
| 64x256x1024, 2 threads, cold (20 ms idle) / numpy (control) | 1394 (1322-1466) | 1322, 1466 | 10.4% |
| 64x256x1024, 4 threads, warm / numpy (control) | 1573 (1525-1620) | 1620, 1525 | 6.1% |
| 64x256x1024, 4 threads, cold (20 ms idle) / numpy (control) | 1766 (1625-1908) | 1908, 1625 | 16.0% |
| 32x128x1352, 1 thread, warm / rust | 787.9 (774.3-801.5) | 801.5, 774.3 | 3.5% |
| 32x128x1352, 1 thread, cold (20 ms idle) / rust | 901.1 (845.3-956.9) | 956.9, 845.3 | 12.4% |
| 32x128x1352, 2 threads, warm / rust | 500.9 (447-554.8) | 447, 554.8 | 21.5% |
| 32x128x1352, 2 threads, cold (20 ms idle) / rust | 583.2 (576.9-589.5) | 589.5, 576.9 | 2.2% |
| 32x128x1352, 4 threads, warm / rust | 300.8 (296.8-304.8) | 304.8, 296.8 | 2.7% |
| 32x128x1352, 4 threads, cold (20 ms idle) / rust | 419.1 (416.8-421.4) | 421.4, 416.8 | 1.1% |
| 32x128x1352, 1 thread, warm / numpy (control) | 780.7 (778.7-782.6) | 782.6, 778.7 | 0.5% |
| 32x128x1352, 1 thread, cold (20 ms idle) / numpy (control) | 793 (787.2-798.8) | 798.8, 787.2 | 1.5% |
| 32x128x1352, 2 threads, warm / numpy (control) | 440.5 (438.5-442.4) | 438.5, 442.4 | 0.9% |
| 32x128x1352, 2 threads, cold (20 ms idle) / numpy (control) | 472.2 (468.2-476.1) | 468.2, 476.1 | 1.7% |
| 32x128x1352, 4 threads, warm / numpy (control) | 930.1 (920.2-940) | 920.2, 940 | 2.1% |
| 32x128x1352, 4 threads, cold (20 ms idle) / numpy (control) | 1013 (976.1-1050) | 976.1, 1050 | 7.3% |
| 32x30x784, 1 thread, warm / rust | 124.7 (124.7-124.7) | 124.7, 124.7 | 0.0% |
| 32x30x784, 1 thread, cold (20 ms idle) / rust | 128.1 (127.8-128.5) | 128.5, 127.8 | 0.6% |
| 32x30x784, 2 threads, warm / rust | 66.81 (66.29-67.33) | 66.29, 67.33 | 1.6% |
| 32x30x784, 2 threads, cold (20 ms idle) / rust | 73.09 (72.82-73.36) | 73.36, 72.82 | 0.7% |
| 32x30x784, 4 threads, warm / rust | 37.58 (37.23-37.94) | 37.23, 37.94 | 1.9% |
| 32x30x784, 4 threads, cold (20 ms idle) / rust | 44.48 (44.2-44.76) | 44.76, 44.2 | 1.3% |
| 32x30x784, 1 thread, warm / numpy (control) | 108.2 (108.1-108.2) | 108.1, 108.2 | 0.1% |
| 32x30x784, 1 thread, cold (20 ms idle) / numpy (control) | 121.2 (120.4-122) | 122, 120.4 | 1.3% |
| 32x30x784, 2 threads, warm / numpy (control) | 57.41 (56.87-57.94) | 56.87, 57.94 | 1.9% |
| 32x30x784, 2 threads, cold (20 ms idle) / numpy (control) | 65.45 (63.88-67.01) | 67.01, 63.88 | 4.8% |
| 32x30x784, 4 threads, warm / numpy (control) | 57.61 (56.93-58.29) | 56.93, 58.29 | 2.4% |
| 32x30x784, 4 threads, cold (20 ms idle) / numpy (control) | 419.9 (419.7-420.2) | 419.7, 420.2 | 0.1% |
| dense 30 x 784|forward_batch|512, 1 thread, warm / rust | 2016 (2008-2024) | 2008, 2024 | 0.8% |
| dense 30 x 784|forward_batch|512, 1 thread, cold (20 ms idle) / rust | 2061 (2049-2073) | 2049, 2073 | 1.2% |
| dense 30 x 784|forward_batch|512, 2 threads, warm / rust | 1195 (1190-1201) | 1201, 1190 | 0.9% |
| dense 30 x 784|forward_batch|512, 2 threads, cold (20 ms idle) / rust | 1255 (1226-1284) | 1284, 1226 | 4.6% |
| dense 30 x 784|forward_batch|512, 4 threads, warm / rust | 812.3 (798.8-825.8) | 798.8, 825.8 | 3.3% |
| dense 30 x 784|forward_batch|512, 4 threads, cold (20 ms idle) / rust | 850.5 (812.5-888.5) | 888.5, 812.5 | 8.9% |
| dense 30 x 784|forward_batch|512, 1 thread, warm / numpy (control) | 2498 (2491-2506) | 2491, 2506 | 0.6% |
| dense 30 x 784|forward_batch|512, 1 thread, cold (20 ms idle) / numpy (control) | 2497 (2495-2499) | 2499, 2495 | 0.2% |
| dense 30 x 784|forward_batch|512, 2 threads, warm / numpy (control) | 1463 (1453-1472) | 1453, 1472 | 1.3% |
| dense 30 x 784|forward_batch|512, 2 threads, cold (20 ms idle) / numpy (control) | 1530 (1527-1533) | 1533, 1527 | 0.4% |
| dense 30 x 784|forward_batch|512, 4 threads, warm / numpy (control) | 2764 (2740-2787) | 2787, 2740 | 1.7% |
| dense 30 x 784|forward_batch|512, 4 threads, cold (20 ms idle) / numpy (control) | 2656 (2432-2879) | 2879, 2432 | 16.8% |
| conv tail 32 x 5408|downstream_batch|512, 1 thread, warm / rust | 2.182e+04 (2.009e+04-2.355e+04) | 2.009e+04, 2.355e+04 | 15.9% |
| conv tail 32 x 5408|downstream_batch|512, 1 thread, cold (20 ms idle) / rust | 2.431e+04 (2.403e+04-2.46e+04) | 2.46e+04, 2.403e+04 | 2.3% |
| conv tail 32 x 5408|downstream_batch|512, 2 threads, warm / rust | 1.688e+04 (1.275e+04-2.101e+04) | 1.275e+04, 2.101e+04 | 48.9% |
| conv tail 32 x 5408|downstream_batch|512, 2 threads, cold (20 ms idle) / rust | 2.222e+04 (2.02e+04-2.423e+04) | 2.423e+04, 2.02e+04 | 18.2% |
| conv tail 32 x 5408|downstream_batch|512, 4 threads, warm / rust | 2.385e+04 (2.139e+04-2.63e+04) | 2.63e+04, 2.139e+04 | 20.6% |
| conv tail 32 x 5408|downstream_batch|512, 4 threads, cold (20 ms idle) / rust | 2.18e+04 (1.93e+04-2.43e+04) | 2.43e+04, 1.93e+04 | 23.0% |
| conv tail 32 x 5408|downstream_batch|512, 1 thread, warm / numpy (control) | 2.189e+04 (2.171e+04-2.207e+04) | 2.171e+04, 2.207e+04 | 1.6% |
| conv tail 32 x 5408|downstream_batch|512, 1 thread, cold (20 ms idle) / numpy (control) | 2.191e+04 (2.088e+04-2.295e+04) | 2.295e+04, 2.088e+04 | 9.4% |
| conv tail 32 x 5408|downstream_batch|512, 2 threads, warm / numpy (control) | 2.784e+04 (2.28e+04-3.287e+04) | 2.28e+04, 3.287e+04 | 36.2% |
| conv tail 32 x 5408|downstream_batch|512, 2 threads, cold (20 ms idle) / numpy (control) | 3.547e+04 (3.224e+04-3.87e+04) | 3.224e+04, 3.87e+04 | 18.2% |
| conv tail 32 x 5408|downstream_batch|512, 4 threads, warm / numpy (control) | 3.871e+04 (3.26e+04-4.483e+04) | 4.483e+04, 3.26e+04 | 31.6% |
| conv tail 32 x 5408|downstream_batch|512, 4 threads, cold (20 ms idle) / numpy (control) | 4.818e+04 (4.658e+04-4.979e+04) | 4.979e+04, 4.658e+04 | 6.7% |
| conv 26x26x8, 8 ch|downstream_batch|512, 1 thread, warm / rust | 8.172e+04 (8.159e+04-8.185e+04) | 8.159e+04, 8.185e+04 | 0.3% |
| conv 26x26x8, 8 ch|downstream_batch|512, 1 thread, cold (20 ms idle) / rust | 8.398e+04 (8.384e+04-8.411e+04) | 8.384e+04, 8.411e+04 | 0.3% |
| conv 26x26x8, 8 ch|downstream_batch|512, 2 threads, warm / rust | 4.587e+04 (4.432e+04-4.742e+04) | 4.742e+04, 4.432e+04 | 6.8% |
| conv 26x26x8, 8 ch|downstream_batch|512, 2 threads, cold (20 ms idle) / rust | 4.442e+04 (4.347e+04-4.537e+04) | 4.537e+04, 4.347e+04 | 4.3% |
| conv 26x26x8, 8 ch|downstream_batch|512, 4 threads, warm / rust | 6.766e+04 (5.629e+04-7.903e+04) | 7.903e+04, 5.629e+04 | 33.6% |
| conv 26x26x8, 8 ch|downstream_batch|512, 4 threads, cold (20 ms idle) / rust | 7.307e+04 (6.589e+04-8.026e+04) | 8.026e+04, 6.589e+04 | 19.7% |
| conv 26x26x8, 8 ch|downstream_batch|512, 1 thread, warm / numpy (control) | 5.167e+05 (5.068e+05-5.265e+05) | 5.265e+05, 5.068e+05 | 3.8% |
| conv 26x26x8, 8 ch|downstream_batch|512, 1 thread, cold (20 ms idle) / numpy (control) | 5.319e+05 (5.213e+05-5.424e+05) | 5.213e+05, 5.424e+05 | 4.0% |
| conv 26x26x8, 8 ch|downstream_batch|512, 2 threads, warm / numpy (control) | 5.322e+05 (5.305e+05-5.339e+05) | 5.305e+05, 5.339e+05 | 0.6% |
| conv 26x26x8, 8 ch|downstream_batch|512, 2 threads, cold (20 ms idle) / numpy (control) | 5.411e+05 (4.745e+05-6.078e+05) | 4.745e+05, 6.078e+05 | 24.6% |
| conv 26x26x8, 8 ch|downstream_batch|512, 4 threads, warm / numpy (control) | 5.339e+05 (5.286e+05-5.392e+05) | 5.286e+05, 5.392e+05 | 2.0% |
| conv 26x26x8, 8 ch|downstream_batch|512, 4 threads, cold (20 ms idle) / numpy (control) | 5.165e+05 (5.079e+05-5.252e+05) | 5.079e+05, 5.252e+05 | 3.3% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 50.98 (50.7-51.25) | 51.25, 50.7 | 1.1% |
