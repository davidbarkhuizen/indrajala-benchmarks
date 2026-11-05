Old `f081ecf` against new `f081ecf`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py scaling --threads 1 2 4 8 12 --repeats 1` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `362e34c` (extension sha256 `7a3f0df0ecd3`) and new crate `362e34c` (extension sha256 `7a3f0df0ecd3`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-1255u.json); max 1-min load 0.34; busy processes: none. Each row pools 1 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: 90 rows, all within noise
- 91 rows within noise, max |Δ| 39.4%
- spread of per-pass medians over 181 rows: median 2.4%, 90th percentile 12.0%, max 52.2%
- pass shifts (median over rows of pass median / pooled median): 1 -0.4%, 2 +0.4%

### per call

| case | median (min-max) µs | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 2048x2048x512, 1 thread, warm / rust | 8.553e+04 (8.161e+04-8.946e+04) | 8.161e+04, 8.946e+04 | 9.2% |
| 2048x2048x512, 1 thread, cold (20 ms idle) / rust | 8.162e+04 (8.006e+04-8.318e+04) | 8.006e+04, 8.318e+04 | 3.8% |
| 2048x2048x512, 2 threads, warm / rust | 5.396e+04 (5.355e+04-5.438e+04) | 5.438e+04, 5.355e+04 | 1.5% |
| 2048x2048x512, 2 threads, cold (20 ms idle) / rust | 4.52e+04 (4.499e+04-4.541e+04) | 4.541e+04, 4.499e+04 | 0.9% |
| 2048x2048x512, 4 threads, warm / rust | 4.419e+04 (4.32e+04-4.518e+04) | 4.518e+04, 4.32e+04 | 4.5% |
| 2048x2048x512, 4 threads, cold (20 ms idle) / rust | 4.258e+04 (3.927e+04-4.588e+04) | 3.927e+04, 4.588e+04 | 15.5% |
| 2048x2048x512, 8 threads, warm / rust | 3.037e+04 (3.022e+04-3.051e+04) | 3.051e+04, 3.022e+04 | 0.9% |
| 2048x2048x512, 8 threads, cold (20 ms idle) / rust | 4.126e+04 (3.666e+04-4.586e+04) | 3.666e+04, 4.586e+04 | 22.3% |
| 2048x2048x512, 12 threads, warm / rust | 2.553e+04 (2.52e+04-2.587e+04) | 2.52e+04, 2.587e+04 | 2.6% |
| 2048x2048x512, 12 threads, cold (20 ms idle) / rust | 4.021e+04 (3.99e+04-4.051e+04) | 3.99e+04, 4.051e+04 | 1.5% |
| 2048x2048x512, 1 thread, warm / numpy (control) | 7.293e+04 (7.171e+04-7.416e+04) | 7.171e+04, 7.416e+04 | 3.4% |
| 2048x2048x512, 1 thread, cold (20 ms idle) / numpy (control) | 7.258e+04 (7.152e+04-7.364e+04) | 7.364e+04, 7.152e+04 | 2.9% |
| 2048x2048x512, 2 threads, warm / numpy (control) | 4.36e+04 (4.328e+04-4.392e+04) | 4.328e+04, 4.392e+04 | 1.5% |
| 2048x2048x512, 2 threads, cold (20 ms idle) / numpy (control) | 3.846e+04 (3.713e+04-3.979e+04) | 3.713e+04, 3.979e+04 | 6.9% |
| 2048x2048x512, 4 threads, warm / numpy (control) | 5.454e+04 (5.4e+04-5.507e+04) | 5.507e+04, 5.4e+04 | 2.0% |
| 2048x2048x512, 4 threads, cold (20 ms idle) / numpy (control) | 5.372e+04 (5.13e+04-5.613e+04) | 5.13e+04, 5.613e+04 | 9.0% |
| 2048x2048x512, 8 threads, warm / numpy (control) | 3.312e+04 (3.298e+04-3.326e+04) | 3.298e+04, 3.326e+04 | 0.8% |
| 2048x2048x512, 8 threads, cold (20 ms idle) / numpy (control) | 3.325e+04 (3.32e+04-3.33e+04) | 3.32e+04, 3.33e+04 | 0.3% |
| 2048x2048x512, 12 threads, warm / numpy (control) | 2.521e+04 (2.496e+04-2.546e+04) | 2.546e+04, 2.496e+04 | 2.0% |
| 2048x2048x512, 12 threads, cold (20 ms idle) / numpy (control) | 2.51e+04 (2.509e+04-2.511e+04) | 2.509e+04, 2.511e+04 | 0.1% |
| 2048x512x2048, 1 thread, warm / rust | 1.086e+05 (1.075e+05-1.098e+05) | 1.098e+05, 1.075e+05 | 2.1% |
| 2048x512x2048, 1 thread, cold (20 ms idle) / rust | 1.037e+05 (1.029e+05-1.045e+05) | 1.029e+05, 1.045e+05 | 1.6% |
| 2048x512x2048, 2 threads, warm / rust | 6.87e+04 (6.707e+04-7.033e+04) | 6.707e+04, 7.033e+04 | 4.7% |
| 2048x512x2048, 2 threads, cold (20 ms idle) / rust | 5.927e+04 (5.836e+04-6.019e+04) | 5.836e+04, 6.019e+04 | 3.1% |
| 2048x512x2048, 4 threads, warm / rust | 5.98e+04 (5.909e+04-6.052e+04) | 5.909e+04, 6.052e+04 | 2.4% |
| 2048x512x2048, 4 threads, cold (20 ms idle) / rust | 5.365e+04 (5.022e+04-5.707e+04) | 5.022e+04, 5.707e+04 | 12.8% |
| 2048x512x2048, 8 threads, warm / rust | 4.812e+04 (4.789e+04-4.834e+04) | 4.789e+04, 4.834e+04 | 0.9% |
| 2048x512x2048, 8 threads, cold (20 ms idle) / rust | 5.059e+04 (5.015e+04-5.103e+04) | 5.015e+04, 5.103e+04 | 1.7% |
| 2048x512x2048, 12 threads, warm / rust | 4.209e+04 (4.2e+04-4.218e+04) | 4.2e+04, 4.218e+04 | 0.4% |
| 2048x512x2048, 12 threads, cold (20 ms idle) / rust | 5.387e+04 (5.364e+04-5.411e+04) | 5.364e+04, 5.411e+04 | 0.9% |
| 2048x512x2048, 1 thread, warm / numpy (control) | 8.112e+04 (7.542e+04-8.681e+04) | 7.542e+04, 8.681e+04 | 14.0% |
| 2048x512x2048, 1 thread, cold (20 ms idle) / numpy (control) | 7.648e+04 (7.34e+04-7.956e+04) | 7.34e+04, 7.956e+04 | 8.1% |
| 2048x512x2048, 2 threads, warm / numpy (control) | 4.253e+04 (4.173e+04-4.333e+04) | 4.173e+04, 4.333e+04 | 3.8% |
| 2048x512x2048, 2 threads, cold (20 ms idle) / numpy (control) | 4.36e+04 (4.159e+04-4.56e+04) | 4.56e+04, 4.159e+04 | 9.2% |
| 2048x512x2048, 4 threads, warm / numpy (control) | 5.773e+04 (5.664e+04-5.882e+04) | 5.664e+04, 5.882e+04 | 3.8% |
| 2048x512x2048, 4 threads, cold (20 ms idle) / numpy (control) | 5.578e+04 (5.243e+04-5.913e+04) | 5.243e+04, 5.913e+04 | 12.0% |
| 2048x512x2048, 8 threads, warm / numpy (control) | 3.724e+04 (3.707e+04-3.741e+04) | 3.707e+04, 3.741e+04 | 0.9% |
| 2048x512x2048, 8 threads, cold (20 ms idle) / numpy (control) | 3.744e+04 (3.732e+04-3.755e+04) | 3.755e+04, 3.732e+04 | 0.6% |
| 2048x512x2048, 12 threads, warm / numpy (control) | 3.173e+04 (3.166e+04-3.18e+04) | 3.18e+04, 3.166e+04 | 0.4% |
| 2048x512x2048, 12 threads, cold (20 ms idle) / numpy (control) | 3.159e+04 (3.156e+04-3.163e+04) | 3.163e+04, 3.156e+04 | 0.2% |
| 512x2048x2048, 1 thread, warm / rust | 9.474e+04 (9.095e+04-9.853e+04) | 9.095e+04, 9.853e+04 | 8.0% |
| 512x2048x2048, 1 thread, cold (20 ms idle) / rust | 9.151e+04 (8.98e+04-9.322e+04) | 9.322e+04, 8.98e+04 | 3.7% |
| 512x2048x2048, 2 threads, warm / rust | 5.943e+04 (5.835e+04-6.051e+04) | 5.835e+04, 6.051e+04 | 3.6% |
| 512x2048x2048, 2 threads, cold (20 ms idle) / rust | 5.388e+04 (4.965e+04-5.812e+04) | 4.965e+04, 5.812e+04 | 15.7% |
| 512x2048x2048, 4 threads, warm / rust | 5.256e+04 (5.114e+04-5.399e+04) | 5.114e+04, 5.399e+04 | 5.4% |
| 512x2048x2048, 4 threads, cold (20 ms idle) / rust | 4.844e+04 (4.632e+04-5.056e+04) | 4.632e+04, 5.056e+04 | 8.8% |
| 512x2048x2048, 8 threads, warm / rust | 4.365e+04 (4.347e+04-4.384e+04) | 4.347e+04, 4.384e+04 | 0.9% |
| 512x2048x2048, 8 threads, cold (20 ms idle) / rust | 4.531e+04 (4.511e+04-4.551e+04) | 4.551e+04, 4.511e+04 | 0.9% |
| 512x2048x2048, 12 threads, warm / rust | 5.21e+04 (5.18e+04-5.24e+04) | 5.24e+04, 5.18e+04 | 1.1% |
| 512x2048x2048, 12 threads, cold (20 ms idle) / rust | 5.94e+04 (5.78e+04-6.101e+04) | 6.101e+04, 5.78e+04 | 5.4% |
| 512x2048x2048, 1 thread, warm / numpy (control) | 8.254e+04 (7.965e+04-8.542e+04) | 7.965e+04, 8.542e+04 | 7.0% |
| 512x2048x2048, 1 thread, cold (20 ms idle) / numpy (control) | 7.268e+04 (7.205e+04-7.33e+04) | 7.205e+04, 7.33e+04 | 1.7% |
| 512x2048x2048, 2 threads, warm / numpy (control) | 4.227e+04 (4.013e+04-4.441e+04) | 4.013e+04, 4.441e+04 | 10.1% |
| 512x2048x2048, 2 threads, cold (20 ms idle) / numpy (control) | 3.931e+04 (3.914e+04-3.948e+04) | 3.914e+04, 3.948e+04 | 0.9% |
| 512x2048x2048, 4 threads, warm / numpy (control) | 5.442e+04 (5.373e+04-5.512e+04) | 5.373e+04, 5.512e+04 | 2.5% |
| 512x2048x2048, 4 threads, cold (20 ms idle) / numpy (control) | 5.064e+04 (5.042e+04-5.087e+04) | 5.042e+04, 5.087e+04 | 0.9% |
| 512x2048x2048, 8 threads, warm / numpy (control) | 3.232e+04 (3.218e+04-3.246e+04) | 3.218e+04, 3.246e+04 | 0.9% |
| 512x2048x2048, 8 threads, cold (20 ms idle) / numpy (control) | 3.223e+04 (3.212e+04-3.235e+04) | 3.212e+04, 3.235e+04 | 0.7% |
| 512x2048x2048, 12 threads, warm / numpy (control) | 2.539e+04 (2.538e+04-2.539e+04) | 2.539e+04, 2.538e+04 | 0.0% |
| 512x2048x2048, 12 threads, cold (20 ms idle) / numpy (control) | 2.554e+04 (2.552e+04-2.556e+04) | 2.556e+04, 2.552e+04 | 0.2% |
| 64x256x1024, 1 thread, warm / rust | 921.7 (887.3-956.1) | 887.3, 956.1 | 7.5% |
| 64x256x1024, 1 thread, cold (20 ms idle) / rust | 2771 (2760-2783) | 2760, 2783 | 0.8% |
| 64x256x1024, 2 threads, warm / rust | 1049 (1046-1052) | 1046, 1052 | 0.6% |
| 64x256x1024, 2 threads, cold (20 ms idle) / rust | 3703 (3665-3742) | 3742, 3665 | 2.1% |
| 64x256x1024, 4 threads, warm / rust | 643.7 (627.3-660.1) | 660.1, 627.3 | 5.1% |
| 64x256x1024, 4 threads, cold (20 ms idle) / rust | 2444 (2353-2535) | 2353, 2535 | 7.4% |
| 64x256x1024, 8 threads, warm / rust | 584.5 (574.8-594.2) | 574.8, 594.2 | 3.3% |
| 64x256x1024, 8 threads, cold (20 ms idle) / rust | 1955 (1889-2021) | 2021, 1889 | 6.8% |
| 64x256x1024, 12 threads, warm / rust | 580.1 (536.9-623.3) | 623.3, 536.9 | 14.9% |
| 64x256x1024, 12 threads, cold (20 ms idle) / rust | 1804 (1782-1826) | 1782, 1826 | 2.4% |
| 64x256x1024, 1 thread, warm / numpy (control) | 674.6 (647.4-701.7) | 647.4, 701.7 | 8.1% |
| 64x256x1024, 1 thread, cold (20 ms idle) / numpy (control) | 2443 (2338-2547) | 2338, 2547 | 8.6% |
| 64x256x1024, 2 threads, warm / numpy (control) | 380.3 (364.5-396) | 396, 364.5 | 8.3% |
| 64x256x1024, 2 threads, cold (20 ms idle) / numpy (control) | 437.6 (437.5-437.7) | 437.7, 437.5 | 0.0% |
| 64x256x1024, 4 threads, warm / numpy (control) | 413.5 (401.5-425.5) | 401.5, 425.5 | 5.8% |
| 64x256x1024, 4 threads, cold (20 ms idle) / numpy (control) | 405.4 (403.5-407.2) | 403.5, 407.2 | 0.9% |
| 64x256x1024, 8 threads, warm / numpy (control) | 384.2 (381.9-386.5) | 386.5, 381.9 | 1.2% |
| 64x256x1024, 8 threads, cold (20 ms idle) / numpy (control) | 390.5 (389.3-391.7) | 391.7, 389.3 | 0.6% |
| 64x256x1024, 12 threads, warm / numpy (control) | 297.9 (297.8-298) | 298, 297.8 | 0.1% |
| 64x256x1024, 12 threads, cold (20 ms idle) / numpy (control) | 289.8 (289-290.6) | 290.6, 289 | 0.5% |
| 32x128x1352, 1 thread, warm / rust | 235.7 (228.5-243) | 243, 228.5 | 6.2% |
| 32x128x1352, 1 thread, cold (20 ms idle) / rust | 901.5 (814.1-988.9) | 814.1, 988.9 | 19.4% |
| 32x128x1352, 2 threads, warm / rust | 277.3 (275.5-279.1) | 279.1, 275.5 | 1.3% |
| 32x128x1352, 2 threads, cold (20 ms idle) / rust | 1683 (1640-1725) | 1725, 1640 | 5.1% |
| 32x128x1352, 4 threads, warm / rust | 190.6 (184.8-196.3) | 184.8, 196.3 | 6.0% |
| 32x128x1352, 4 threads, cold (20 ms idle) / rust | 1118 (1107-1128) | 1107, 1128 | 1.9% |
| 32x128x1352, 8 threads, warm / rust | 182.1 (179.6-184.6) | 179.6, 184.6 | 2.7% |
| 32x128x1352, 8 threads, cold (20 ms idle) / rust | 786.4 (781.6-791.2) | 781.6, 791.2 | 1.2% |
| 32x128x1352, 12 threads, warm / rust | 250.6 (209.4-291.9) | 209.4, 291.9 | 32.9% |
| 32x128x1352, 12 threads, cold (20 ms idle) / rust | 961.9 (944.3-979.6) | 944.3, 979.6 | 3.7% |
| 32x128x1352, 1 thread, warm / numpy (control) | 247.8 (242.9-252.7) | 242.9, 252.7 | 3.9% |
| 32x128x1352, 1 thread, cold (20 ms idle) / numpy (control) | 1025 (981.9-1069) | 981.9, 1069 | 8.4% |
| 32x128x1352, 2 threads, warm / numpy (control) | 132.4 (132.1-132.6) | 132.1, 132.6 | 0.4% |
| 32x128x1352, 2 threads, cold (20 ms idle) / numpy (control) | 193 (188.4-197.7) | 188.4, 197.7 | 4.8% |
| 32x128x1352, 4 threads, warm / numpy (control) | 195.2 (195.2-195.2) | 195.2, 195.2 | 0.0% |
| 32x128x1352, 4 threads, cold (20 ms idle) / numpy (control) | 217.3 (217-217.5) | 217, 217.5 | 0.3% |
| 32x128x1352, 8 threads, warm / numpy (control) | 139.4 (139.2-139.5) | 139.5, 139.2 | 0.2% |
| 32x128x1352, 8 threads, cold (20 ms idle) / numpy (control) | 167.3 (166.9-167.7) | 167.7, 166.9 | 0.5% |
| 32x128x1352, 12 threads, warm / numpy (control) | 112.1 (111.4-112.7) | 112.7, 111.4 | 1.2% |
| 32x128x1352, 12 threads, cold (20 ms idle) / numpy (control) | 106.7 (106.6-106.8) | 106.6, 106.8 | 0.1% |
| 32x30x784, 1 thread, warm / rust | 29.61 (29.03-30.2) | 29.03, 30.2 | 4.0% |
| 32x30x784, 1 thread, cold (20 ms idle) / rust | 153.1 (136-170.1) | 170.1, 136 | 22.3% |
| 32x30x784, 2 threads, warm / rust | 68.53 (64.11-72.94) | 64.11, 72.94 | 12.9% |
| 32x30x784, 2 threads, cold (20 ms idle) / rust | 744.2 (722.6-765.8) | 722.6, 765.8 | 5.8% |
| 32x30x784, 4 threads, warm / rust | 81.05 (73.76-88.33) | 88.33, 73.76 | 18.0% |
| 32x30x784, 4 threads, cold (20 ms idle) / rust | 564.8 (553.2-576.4) | 553.2, 576.4 | 4.1% |
| 32x30x784, 8 threads, warm / rust | 100.3 (100-100.5) | 100.5, 100 | 0.5% |
| 32x30x784, 8 threads, cold (20 ms idle) / rust | 524.6 (517.1-532.1) | 517.1, 532.1 | 2.9% |
| 32x30x784, 12 threads, warm / rust | 122.2 (121.1-123.3) | 121.1, 123.3 | 1.9% |
| 32x30x784, 12 threads, cold (20 ms idle) / rust | 686.9 (652.5-721.3) | 721.3, 652.5 | 10.0% |
| 32x30x784, 1 thread, warm / numpy (control) | 34.05 (33.85-34.25) | 33.85, 34.25 | 1.2% |
| 32x30x784, 1 thread, cold (20 ms idle) / numpy (control) | 240 (234.6-245.5) | 245.5, 234.6 | 4.6% |
| 32x30x784, 2 threads, warm / numpy (control) | 21.14 (21.1-21.18) | 21.1, 21.18 | 0.4% |
| 32x30x784, 2 threads, cold (20 ms idle) / numpy (control) | 44.5 (42.76-46.23) | 42.76, 46.23 | 7.8% |
| 32x30x784, 4 threads, warm / numpy (control) | 22.58 (21.7-23.46) | 23.46, 21.7 | 7.8% |
| 32x30x784, 4 threads, cold (20 ms idle) / numpy (control) | 80.79 (80.73-80.86) | 80.86, 80.73 | 0.2% |
| 32x30x784, 8 threads, warm / numpy (control) | 27.77 (23.95-31.6) | 23.95, 31.6 | 27.5% |
| 32x30x784, 8 threads, cold (20 ms idle) / numpy (control) | 61.25 (45.27-77.22) | 45.27, 77.22 | 52.2% |
| 32x30x784, 12 threads, warm / numpy (control) | 23.14 (22.89-23.38) | 23.38, 22.89 | 2.1% |
| 32x30x784, 12 threads, cold (20 ms idle) / numpy (control) | 42.64 (42.17-43.11) | 43.11, 42.17 | 2.2% |
| dense 30 x 784|forward_batch|512, 1 thread, warm / rust | 616.1 (574.3-657.9) | 574.3, 657.9 | 13.6% |
| dense 30 x 784|forward_batch|512, 1 thread, cold (20 ms idle) / rust | 2048 (1979-2117) | 1979, 2117 | 6.7% |
| dense 30 x 784|forward_batch|512, 2 threads, warm / rust | 631.2 (613.6-648.7) | 613.6, 648.7 | 5.6% |
| dense 30 x 784|forward_batch|512, 2 threads, cold (20 ms idle) / rust | 2728 (2657-2799) | 2799, 2657 | 5.2% |
| dense 30 x 784|forward_batch|512, 4 threads, warm / rust | 439.1 (437.3-440.9) | 440.9, 437.3 | 0.8% |
| dense 30 x 784|forward_batch|512, 4 threads, cold (20 ms idle) / rust | 2046 (2032-2059) | 2032, 2059 | 1.3% |
| dense 30 x 784|forward_batch|512, 8 threads, warm / rust | 380.4 (376.3-384.6) | 376.3, 384.6 | 2.2% |
| dense 30 x 784|forward_batch|512, 8 threads, cold (20 ms idle) / rust | 1628 (1614-1643) | 1643, 1614 | 1.7% |
| dense 30 x 784|forward_batch|512, 12 threads, warm / rust | 416.4 (383.9-448.9) | 383.9, 448.9 | 15.6% |
| dense 30 x 784|forward_batch|512, 12 threads, cold (20 ms idle) / rust | 1537 (1527-1546) | 1546, 1527 | 1.3% |
| dense 30 x 784|forward_batch|512, 1 thread, warm / numpy (control) | 655.5 (652.8-658.3) | 652.8, 658.3 | 0.8% |
| dense 30 x 784|forward_batch|512, 1 thread, cold (20 ms idle) / numpy (control) | 2381 (2303-2459) | 2303, 2459 | 6.6% |
| dense 30 x 784|forward_batch|512, 2 threads, warm / numpy (control) | 380.7 (378.8-382.7) | 382.7, 378.8 | 1.0% |
| dense 30 x 784|forward_batch|512, 2 threads, cold (20 ms idle) / numpy (control) | 455.5 (446.4-464.5) | 446.4, 464.5 | 4.0% |
| dense 30 x 784|forward_batch|512, 4 threads, warm / numpy (control) | 431.6 (430.9-432.3) | 430.9, 432.3 | 0.3% |
| dense 30 x 784|forward_batch|512, 4 threads, cold (20 ms idle) / numpy (control) | 507.7 (439-576.3) | 576.3, 439 | 27.1% |
| dense 30 x 784|forward_batch|512, 8 threads, warm / numpy (control) | 369.4 (368.7-370) | 370, 368.7 | 0.3% |
| dense 30 x 784|forward_batch|512, 8 threads, cold (20 ms idle) / numpy (control) | 392.5 (385.9-399) | 399, 385.9 | 3.3% |
| dense 30 x 784|forward_batch|512, 12 threads, warm / numpy (control) | 360.5 (358.3-362.6) | 358.3, 362.6 | 1.2% |
| dense 30 x 784|forward_batch|512, 12 threads, cold (20 ms idle) / numpy (control) | 360.9 (357.8-363.9) | 363.9, 357.8 | 1.7% |
| conv tail 32 x 5408|downstream_batch|512, 1 thread, warm / rust | 4132 (3994-4271) | 4271, 3994 | 6.7% |
| conv tail 32 x 5408|downstream_batch|512, 1 thread, cold (20 ms idle) / rust | 7436 (7435-7436) | 7436, 7435 | 0.0% |
| conv tail 32 x 5408|downstream_batch|512, 2 threads, warm / rust | 5335 (4757-5914) | 4757, 5914 | 21.7% |
| conv tail 32 x 5408|downstream_batch|512, 2 threads, cold (20 ms idle) / rust | 1.099e+04 (1.072e+04-1.125e+04) | 1.125e+04, 1.072e+04 | 4.8% |
| conv tail 32 x 5408|downstream_batch|512, 4 threads, warm / rust | 2864 (2823-2905) | 2905, 2823 | 2.9% |
| conv tail 32 x 5408|downstream_batch|512, 4 threads, cold (20 ms idle) / rust | 8604 (8560-8648) | 8560, 8648 | 1.0% |
| conv tail 32 x 5408|downstream_batch|512, 8 threads, warm / rust | 2205 (2186-2224) | 2224, 2186 | 1.7% |
| conv tail 32 x 5408|downstream_batch|512, 8 threads, cold (20 ms idle) / rust | 6410 (6359-6461) | 6461, 6359 | 1.6% |
| conv tail 32 x 5408|downstream_batch|512, 12 threads, warm / rust | 2893 (2734-3053) | 2734, 3053 | 11.0% |
| conv tail 32 x 5408|downstream_batch|512, 12 threads, cold (20 ms idle) / rust | 6672 (5837-7506) | 7506, 5837 | 25.0% |
| conv tail 32 x 5408|downstream_batch|512, 1 thread, warm / numpy (control) | 3995 (3777-4213) | 3777, 4213 | 10.9% |
| conv tail 32 x 5408|downstream_batch|512, 1 thread, cold (20 ms idle) / numpy (control) | 6946 (6656-7237) | 7237, 6656 | 8.4% |
| conv tail 32 x 5408|downstream_batch|512, 2 threads, warm / numpy (control) | 2733 (2728-2738) | 2738, 2728 | 0.4% |
| conv tail 32 x 5408|downstream_batch|512, 2 threads, cold (20 ms idle) / numpy (control) | 3074 (3073-3074) | 3073, 3074 | 0.0% |
| conv tail 32 x 5408|downstream_batch|512, 4 threads, warm / numpy (control) | 2908 (2899-2918) | 2899, 2918 | 0.6% |
| conv tail 32 x 5408|downstream_batch|512, 4 threads, cold (20 ms idle) / numpy (control) | 3125 (3009-3242) | 3242, 3009 | 7.5% |
| conv tail 32 x 5408|downstream_batch|512, 8 threads, warm / numpy (control) | 2302 (2300-2304) | 2304, 2300 | 0.2% |
| conv tail 32 x 5408|downstream_batch|512, 8 threads, cold (20 ms idle) / numpy (control) | 2491 (2475-2507) | 2507, 2475 | 1.3% |
| conv tail 32 x 5408|downstream_batch|512, 12 threads, warm / numpy (control) | 1973 (1968-1978) | 1968, 1978 | 0.5% |
| conv tail 32 x 5408|downstream_batch|512, 12 threads, cold (20 ms idle) / numpy (control) | 2158 (2157-2160) | 2157, 2160 | 0.1% |
| conv 26x26x8, 8 ch|downstream_batch|512, 1 thread, warm / rust | 2.3e+04 (2.238e+04-2.361e+04) | 2.238e+04, 2.361e+04 | 5.4% |
| conv 26x26x8, 8 ch|downstream_batch|512, 1 thread, cold (20 ms idle) / rust | 2.095e+04 (2.092e+04-2.098e+04) | 2.098e+04, 2.092e+04 | 0.3% |
| conv 26x26x8, 8 ch|downstream_batch|512, 2 threads, warm / rust | 2.238e+04 (2.227e+04-2.25e+04) | 2.25e+04, 2.227e+04 | 1.0% |
| conv 26x26x8, 8 ch|downstream_batch|512, 2 threads, cold (20 ms idle) / rust | 1.767e+04 (1.685e+04-1.849e+04) | 1.685e+04, 1.849e+04 | 9.3% |
| conv 26x26x8, 8 ch|downstream_batch|512, 4 threads, warm / rust | 1.505e+04 (1.444e+04-1.567e+04) | 1.567e+04, 1.444e+04 | 8.2% |
| conv 26x26x8, 8 ch|downstream_batch|512, 4 threads, cold (20 ms idle) / rust | 1.519e+04 (1.471e+04-1.567e+04) | 1.471e+04, 1.567e+04 | 6.3% |
| conv 26x26x8, 8 ch|downstream_batch|512, 8 threads, warm / rust | 1.092e+04 (1.076e+04-1.107e+04) | 1.076e+04, 1.107e+04 | 2.9% |
| conv 26x26x8, 8 ch|downstream_batch|512, 8 threads, cold (20 ms idle) / rust | 1.827e+04 (1.773e+04-1.882e+04) | 1.773e+04, 1.882e+04 | 5.9% |
| conv 26x26x8, 8 ch|downstream_batch|512, 12 threads, warm / rust | 9811 (9620-1e+04) | 9620, 1e+04 | 3.9% |
| conv 26x26x8, 8 ch|downstream_batch|512, 12 threads, cold (20 ms idle) / rust | 2.231e+04 (2.192e+04-2.269e+04) | 2.192e+04, 2.269e+04 | 3.5% |
| conv 26x26x8, 8 ch|downstream_batch|512, 1 thread, warm / numpy (control) | 1.194e+05 (1.194e+05-1.195e+05) | 1.195e+05, 1.194e+05 | 0.1% |
| conv 26x26x8, 8 ch|downstream_batch|512, 1 thread, cold (20 ms idle) / numpy (control) | 1.171e+05 (1.168e+05-1.173e+05) | 1.173e+05, 1.168e+05 | 0.4% |
| conv 26x26x8, 8 ch|downstream_batch|512, 2 threads, warm / numpy (control) | 1.188e+05 (1.177e+05-1.199e+05) | 1.177e+05, 1.199e+05 | 1.9% |
| conv 26x26x8, 8 ch|downstream_batch|512, 2 threads, cold (20 ms idle) / numpy (control) | 1.179e+05 (1.169e+05-1.188e+05) | 1.169e+05, 1.188e+05 | 1.7% |
| conv 26x26x8, 8 ch|downstream_batch|512, 4 threads, warm / numpy (control) | 1.211e+05 (1.21e+05-1.211e+05) | 1.21e+05, 1.211e+05 | 0.1% |
| conv 26x26x8, 8 ch|downstream_batch|512, 4 threads, cold (20 ms idle) / numpy (control) | 1.178e+05 (1.165e+05-1.191e+05) | 1.191e+05, 1.165e+05 | 2.2% |
| conv 26x26x8, 8 ch|downstream_batch|512, 8 threads, warm / numpy (control) | 1.2e+05 (1.184e+05-1.216e+05) | 1.216e+05, 1.184e+05 | 2.7% |
| conv 26x26x8, 8 ch|downstream_batch|512, 8 threads, cold (20 ms idle) / numpy (control) | 1.179e+05 (1.162e+05-1.196e+05) | 1.162e+05, 1.196e+05 | 2.9% |
| conv 26x26x8, 8 ch|downstream_batch|512, 12 threads, warm / numpy (control) | 1.167e+05 (1.164e+05-1.171e+05) | 1.171e+05, 1.164e+05 | 0.6% |
| conv 26x26x8, 8 ch|downstream_batch|512, 12 threads, cold (20 ms idle) / numpy (control) | 1.144e+05 (1.131e+05-1.158e+05) | 1.131e+05, 1.158e+05 | 2.3% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 20 (20-20) | 20, 20 | 0.0% |
