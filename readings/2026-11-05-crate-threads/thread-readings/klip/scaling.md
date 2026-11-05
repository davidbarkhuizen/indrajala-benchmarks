Old `f081ecf` against new `f081ecf`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py scaling --repeats 1` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `362e34c` (extension sha256 `7a3f0df0ecd3`) and new crate `362e34c` (extension sha256 `7a3f0df0ecd3`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (ryzen7-3700u-klip.json); max 1-min load 0.81; busy processes: none. Each row pools 1 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: 72 rows, all within noise
- 73 rows within noise, max |Δ| 66.7%
- spread of per-pass medians over 145 rows: median 1.5%, 90th percentile 37.6%, max 67.5%
- pass shifts (median over rows of pass median / pooled median): 1 +0.0%, 2 -0.0%

### per call

| case | median (min-max) µs | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 2048x2048x512, 1 thread, warm / rust | 2.713e+05 (2.706e+05-2.719e+05) | 2.719e+05, 2.706e+05 | 0.5% |
| 2048x2048x512, 1 thread, cold (20 ms idle) / rust | 2.736e+05 (2.731e+05-2.741e+05) | 2.731e+05, 2.741e+05 | 0.4% |
| 2048x2048x512, 2 threads, warm / rust | 1.477e+05 (1.476e+05-1.478e+05) | 1.478e+05, 1.476e+05 | 0.2% |
| 2048x2048x512, 2 threads, cold (20 ms idle) / rust | 1.464e+05 (1.425e+05-1.502e+05) | 1.425e+05, 1.502e+05 | 5.2% |
| 2048x2048x512, 4 threads, warm / rust | 7.667e+04 (7.554e+04-7.78e+04) | 7.78e+04, 7.554e+04 | 2.9% |
| 2048x2048x512, 4 threads, cold (20 ms idle) / rust | 7.923e+04 (7.596e+04-8.25e+04) | 7.596e+04, 8.25e+04 | 8.3% |
| 2048x2048x512, 8 threads, warm / rust | 1.34e+05 (1.338e+05-1.341e+05) | 1.341e+05, 1.338e+05 | 0.3% |
| 2048x2048x512, 8 threads, cold (20 ms idle) / rust | 1.134e+05 (9.206e+04-1.347e+05) | 9.206e+04, 1.347e+05 | 37.6% |
| 2048x2048x512, 1 thread, warm / numpy (control) | 2.691e+05 (2.688e+05-2.693e+05) | 2.693e+05, 2.688e+05 | 0.2% |
| 2048x2048x512, 1 thread, cold (20 ms idle) / numpy (control) | 2.693e+05 (2.689e+05-2.696e+05) | 2.689e+05, 2.696e+05 | 0.2% |
| 2048x2048x512, 2 threads, warm / numpy (control) | 1.297e+05 (1.297e+05-1.297e+05) | 1.297e+05, 1.297e+05 | 0.0% |
| 2048x2048x512, 2 threads, cold (20 ms idle) / numpy (control) | 1.298e+05 (1.296e+05-1.3e+05) | 1.296e+05, 1.3e+05 | 0.4% |
| 2048x2048x512, 4 threads, warm / numpy (control) | 7.058e+04 (6.915e+04-7.201e+04) | 6.915e+04, 7.201e+04 | 4.1% |
| 2048x2048x512, 4 threads, cold (20 ms idle) / numpy (control) | 6.914e+04 (6.903e+04-6.925e+04) | 6.903e+04, 6.925e+04 | 0.3% |
| 2048x2048x512, 8 threads, warm / numpy (control) | 8.944e+04 (8.943e+04-8.945e+04) | 8.943e+04, 8.945e+04 | 0.0% |
| 2048x2048x512, 8 threads, cold (20 ms idle) / numpy (control) | 9.005e+04 (8.992e+04-9.017e+04) | 9.017e+04, 8.992e+04 | 0.3% |
| 2048x512x2048, 1 thread, warm / rust | 3.15e+05 (3.147e+05-3.153e+05) | 3.153e+05, 3.147e+05 | 0.2% |
| 2048x512x2048, 1 thread, cold (20 ms idle) / rust | 3.163e+05 (3.149e+05-3.178e+05) | 3.149e+05, 3.178e+05 | 0.9% |
| 2048x512x2048, 2 threads, warm / rust | 1.832e+05 (1.831e+05-1.833e+05) | 1.833e+05, 1.831e+05 | 0.1% |
| 2048x512x2048, 2 threads, cold (20 ms idle) / rust | 1.837e+05 (1.833e+05-1.84e+05) | 1.84e+05, 1.833e+05 | 0.4% |
| 2048x512x2048, 4 threads, warm / rust | 1.06e+05 (1.06e+05-1.061e+05) | 1.061e+05, 1.06e+05 | 0.1% |
| 2048x512x2048, 4 threads, cold (20 ms idle) / rust | 1.099e+05 (1.091e+05-1.106e+05) | 1.106e+05, 1.091e+05 | 1.3% |
| 2048x512x2048, 8 threads, warm / rust | 1.176e+05 (1.172e+05-1.18e+05) | 1.18e+05, 1.172e+05 | 0.7% |
| 2048x512x2048, 8 threads, cold (20 ms idle) / rust | 1.182e+05 (1.175e+05-1.188e+05) | 1.175e+05, 1.188e+05 | 1.1% |
| 2048x512x2048, 1 thread, warm / numpy (control) | 2.617e+05 (2.611e+05-2.623e+05) | 2.611e+05, 2.623e+05 | 0.5% |
| 2048x512x2048, 1 thread, cold (20 ms idle) / numpy (control) | 2.613e+05 (2.611e+05-2.614e+05) | 2.611e+05, 2.614e+05 | 0.1% |
| 2048x512x2048, 2 threads, warm / numpy (control) | 1.38e+05 (1.377e+05-1.383e+05) | 1.377e+05, 1.383e+05 | 0.4% |
| 2048x512x2048, 2 threads, cold (20 ms idle) / numpy (control) | 1.386e+05 (1.381e+05-1.392e+05) | 1.392e+05, 1.381e+05 | 0.7% |
| 2048x512x2048, 4 threads, warm / numpy (control) | 7.728e+04 (7.713e+04-7.742e+04) | 7.742e+04, 7.713e+04 | 0.4% |
| 2048x512x2048, 4 threads, cold (20 ms idle) / numpy (control) | 7.735e+04 (7.722e+04-7.748e+04) | 7.722e+04, 7.748e+04 | 0.3% |
| 2048x512x2048, 8 threads, warm / numpy (control) | 9.872e+04 (9.866e+04-9.878e+04) | 9.878e+04, 9.866e+04 | 0.1% |
| 2048x512x2048, 8 threads, cold (20 ms idle) / numpy (control) | 9.942e+04 (9.926e+04-9.957e+04) | 9.926e+04, 9.957e+04 | 0.3% |
| 512x2048x2048, 1 thread, warm / rust | 2.782e+05 (2.777e+05-2.787e+05) | 2.787e+05, 2.777e+05 | 0.4% |
| 512x2048x2048, 1 thread, cold (20 ms idle) / rust | 2.779e+05 (2.764e+05-2.794e+05) | 2.764e+05, 2.794e+05 | 1.1% |
| 512x2048x2048, 2 threads, warm / rust | 1.555e+05 (1.537e+05-1.573e+05) | 1.573e+05, 1.537e+05 | 2.3% |
| 512x2048x2048, 2 threads, cold (20 ms idle) / rust | 1.542e+05 (1.514e+05-1.57e+05) | 1.57e+05, 1.514e+05 | 3.6% |
| 512x2048x2048, 4 threads, warm / rust | 9.427e+04 (9.274e+04-9.58e+04) | 9.58e+04, 9.274e+04 | 3.2% |
| 512x2048x2048, 4 threads, cold (20 ms idle) / rust | 9.749e+04 (9.629e+04-9.87e+04) | 9.87e+04, 9.629e+04 | 2.5% |
| 512x2048x2048, 8 threads, warm / rust | 1.419e+05 (1.231e+05-1.606e+05) | 1.606e+05, 1.231e+05 | 26.5% |
| 512x2048x2048, 8 threads, cold (20 ms idle) / rust | 1.52e+05 (1.416e+05-1.624e+05) | 1.624e+05, 1.416e+05 | 13.6% |
| 512x2048x2048, 1 thread, warm / numpy (control) | 2.578e+05 (2.578e+05-2.579e+05) | 2.578e+05, 2.579e+05 | 0.0% |
| 512x2048x2048, 1 thread, cold (20 ms idle) / numpy (control) | 2.584e+05 (2.584e+05-2.584e+05) | 2.584e+05, 2.584e+05 | 0.0% |
| 512x2048x2048, 2 threads, warm / numpy (control) | 1.318e+05 (1.314e+05-1.321e+05) | 1.314e+05, 1.321e+05 | 0.5% |
| 512x2048x2048, 2 threads, cold (20 ms idle) / numpy (control) | 1.328e+05 (1.321e+05-1.335e+05) | 1.321e+05, 1.335e+05 | 1.0% |
| 512x2048x2048, 4 threads, warm / numpy (control) | 6.953e+04 (6.946e+04-6.961e+04) | 6.961e+04, 6.946e+04 | 0.2% |
| 512x2048x2048, 4 threads, cold (20 ms idle) / numpy (control) | 6.999e+04 (6.998e+04-6.999e+04) | 6.998e+04, 6.999e+04 | 0.0% |
| 512x2048x2048, 8 threads, warm / numpy (control) | 8.301e+04 (8.299e+04-8.302e+04) | 8.299e+04, 8.302e+04 | 0.0% |
| 512x2048x2048, 8 threads, cold (20 ms idle) / numpy (control) | 8.286e+04 (8.276e+04-8.295e+04) | 8.295e+04, 8.276e+04 | 0.2% |
| 64x256x1024, 1 thread, warm / rust | 2219 (2216-2222) | 2222, 2216 | 0.3% |
| 64x256x1024, 1 thread, cold (20 ms idle) / rust | 2290 (2287-2293) | 2287, 2293 | 0.3% |
| 64x256x1024, 2 threads, warm / rust | 2540 (2080-3001) | 2080, 3001 | 36.3% |
| 64x256x1024, 2 threads, cold (20 ms idle) / rust | 3734 (3603-3864) | 3603, 3864 | 7.0% |
| 64x256x1024, 4 threads, warm / rust | 1948 (1927-1970) | 1927, 1970 | 2.2% |
| 64x256x1024, 4 threads, cold (20 ms idle) / rust | 1996 (1960-2031) | 1960, 2031 | 3.6% |
| 64x256x1024, 8 threads, warm / rust | 1464 (1098-1830) | 1098, 1830 | 50.0% |
| 64x256x1024, 8 threads, cold (20 ms idle) / rust | 1889 (1872-1907) | 1907, 1872 | 1.9% |
| 64x256x1024, 1 thread, warm / numpy (control) | 2197 (2189-2206) | 2206, 2189 | 0.8% |
| 64x256x1024, 1 thread, cold (20 ms idle) / numpy (control) | 2974 (2285-3662) | 2285, 3662 | 46.3% |
| 64x256x1024, 2 threads, warm / numpy (control) | 1196 (1186-1206) | 1186, 1206 | 1.7% |
| 64x256x1024, 2 threads, cold (20 ms idle) / numpy (control) | 1980 (1844-2115) | 1844, 2115 | 13.7% |
| 64x256x1024, 4 threads, warm / numpy (control) | 633.8 (628.8-638.9) | 638.9, 628.8 | 1.6% |
| 64x256x1024, 4 threads, cold (20 ms idle) / numpy (control) | 968.6 (718-1219) | 1219, 718 | 51.7% |
| 64x256x1024, 8 threads, warm / numpy (control) | 883 (876.9-889.1) | 889.1, 876.9 | 1.4% |
| 64x256x1024, 8 threads, cold (20 ms idle) / numpy (control) | 947.2 (940.6-953.9) | 953.9, 940.6 | 1.4% |
| 32x128x1352, 1 thread, warm / rust | 746.1 (745.4-746.8) | 746.8, 745.4 | 0.2% |
| 32x128x1352, 1 thread, cold (20 ms idle) / rust | 1127 (986.4-1268) | 1268, 986.4 | 25.0% |
| 32x128x1352, 2 threads, warm / rust | 751 (537.1-965) | 965, 537.1 | 57.0% |
| 32x128x1352, 2 threads, cold (20 ms idle) / rust | 743.5 (534.9-952) | 952, 534.9 | 56.1% |
| 32x128x1352, 4 threads, warm / rust | 643 (549.7-736.3) | 549.7, 736.3 | 29.0% |
| 32x128x1352, 4 threads, cold (20 ms idle) / rust | 681.8 (660.4-703.2) | 660.4, 703.2 | 6.3% |
| 32x128x1352, 8 threads, warm / rust | 689.4 (606.4-772.4) | 772.4, 606.4 | 24.1% |
| 32x128x1352, 8 threads, cold (20 ms idle) / rust | 759.7 (743.3-776.1) | 776.1, 743.3 | 4.3% |
| 32x128x1352, 1 thread, warm / numpy (control) | 839.4 (832.9-845.9) | 832.9, 845.9 | 1.6% |
| 32x128x1352, 1 thread, cold (20 ms idle) / numpy (control) | 1131 (856.1-1405) | 1405, 856.1 | 48.5% |
| 32x128x1352, 2 threads, warm / numpy (control) | 501.9 (498.9-504.8) | 498.9, 504.8 | 1.2% |
| 32x128x1352, 2 threads, cold (20 ms idle) / numpy (control) | 778.2 (533.6-1023) | 533.6, 1023 | 62.9% |
| 32x128x1352, 4 threads, warm / numpy (control) | 250 (248.5-251.4) | 251.4, 248.5 | 1.2% |
| 32x128x1352, 4 threads, cold (20 ms idle) / numpy (control) | 336.7 (266-407.4) | 407.4, 266 | 42.0% |
| 32x128x1352, 8 threads, warm / numpy (control) | 313.3 (312.1-314.5) | 314.5, 312.1 | 0.8% |
| 32x128x1352, 8 threads, cold (20 ms idle) / numpy (control) | 326.9 (326.8-327) | 327, 326.8 | 0.0% |
| 32x30x784, 1 thread, warm / rust | 104.5 (103.6-105.3) | 105.3, 103.6 | 1.6% |
| 32x30x784, 1 thread, cold (20 ms idle) / rust | 157 (129.7-184.2) | 129.7, 184.2 | 34.7% |
| 32x30x784, 2 threads, warm / rust | 190.1 (188.1-192.2) | 192.2, 188.1 | 2.2% |
| 32x30x784, 2 threads, cold (20 ms idle) / rust | 203.5 (187.8-219.2) | 219.2, 187.8 | 15.5% |
| 32x30x784, 4 threads, warm / rust | 180.9 (173.7-188.1) | 188.1, 173.7 | 8.0% |
| 32x30x784, 4 threads, cold (20 ms idle) / rust | 250.2 (237.1-263.4) | 237.1, 263.4 | 10.5% |
| 32x30x784, 8 threads, warm / rust | 265 (261.7-268.4) | 268.4, 261.7 | 2.5% |
| 32x30x784, 8 threads, cold (20 ms idle) / rust | 335.9 (332.3-339.4) | 332.3, 339.4 | 2.1% |
| 32x30x784, 1 thread, warm / numpy (control) | 163.2 (161.4-165.1) | 161.4, 165.1 | 2.3% |
| 32x30x784, 1 thread, cold (20 ms idle) / numpy (control) | 219.7 (166.4-273) | 166.4, 273 | 48.5% |
| 32x30x784, 2 threads, warm / numpy (control) | 67.01 (66.91-67.12) | 67.12, 66.91 | 0.3% |
| 32x30x784, 2 threads, cold (20 ms idle) / numpy (control) | 128.4 (115.2-141.6) | 141.6, 115.2 | 20.6% |
| 32x30x784, 4 threads, warm / numpy (control) | 66.92 (66.78-67.06) | 66.78, 67.06 | 0.4% |
| 32x30x784, 4 threads, cold (20 ms idle) / numpy (control) | 93.89 (72.61-115.2) | 115.2, 72.61 | 45.3% |
| 32x30x784, 8 threads, warm / numpy (control) | 67.05 (66.96-67.14) | 67.14, 66.96 | 0.3% |
| 32x30x784, 8 threads, cold (20 ms idle) / numpy (control) | 108.3 (71.7-144.8) | 71.7, 144.8 | 67.5% |
| dense 30 x 784|forward_batch|512, 1 thread, warm / rust | 1842 (1831-1852) | 1831, 1852 | 1.1% |
| dense 30 x 784|forward_batch|512, 1 thread, cold (20 ms idle) / rust | 2551 (1920-3182) | 3182, 1920 | 49.5% |
| dense 30 x 784|forward_batch|512, 2 threads, warm / rust | 1440 (1389-1490) | 1389, 1490 | 7.0% |
| dense 30 x 784|forward_batch|512, 2 threads, cold (20 ms idle) / rust | 1886 (1797-1975) | 1797, 1975 | 9.4% |
| dense 30 x 784|forward_batch|512, 4 threads, warm / rust | 1156 (1147-1164) | 1164, 1147 | 1.5% |
| dense 30 x 784|forward_batch|512, 4 threads, cold (20 ms idle) / rust | 1255 (1234-1276) | 1276, 1234 | 3.4% |
| dense 30 x 784|forward_batch|512, 8 threads, warm / rust | 1326 (1321-1331) | 1331, 1321 | 0.8% |
| dense 30 x 784|forward_batch|512, 8 threads, cold (20 ms idle) / rust | 1420 (1405-1435) | 1435, 1405 | 2.2% |
| dense 30 x 784|forward_batch|512, 1 thread, warm / numpy (control) | 2136 (2027-2246) | 2027, 2246 | 10.2% |
| dense 30 x 784|forward_batch|512, 1 thread, cold (20 ms idle) / numpy (control) | 2557 (2121-2993) | 2121, 2993 | 34.1% |
| dense 30 x 784|forward_batch|512, 2 threads, warm / numpy (control) | 1196 (1174-1217) | 1174, 1217 | 3.6% |
| dense 30 x 784|forward_batch|512, 2 threads, cold (20 ms idle) / numpy (control) | 1796 (1310-2283) | 1310, 2283 | 54.2% |
| dense 30 x 784|forward_batch|512, 4 threads, warm / numpy (control) | 716.4 (714.5-718.2) | 718.2, 714.5 | 0.5% |
| dense 30 x 784|forward_batch|512, 4 threads, cold (20 ms idle) / numpy (control) | 1271 (1179-1363) | 1363, 1179 | 14.5% |
| dense 30 x 784|forward_batch|512, 8 threads, warm / numpy (control) | 946.3 (943.7-948.9) | 943.7, 948.9 | 0.6% |
| dense 30 x 784|forward_batch|512, 8 threads, cold (20 ms idle) / numpy (control) | 975.9 (975-976.9) | 976.9, 975 | 0.2% |
| conv tail 32 x 5408|downstream_batch|512, 1 thread, warm / rust | 1.32e+04 (1.32e+04-1.32e+04) | 1.32e+04, 1.32e+04 | 0.0% |
| conv tail 32 x 5408|downstream_batch|512, 1 thread, cold (20 ms idle) / rust | 1.413e+04 (1.408e+04-1.417e+04) | 1.417e+04, 1.408e+04 | 0.6% |
| conv tail 32 x 5408|downstream_batch|512, 2 threads, warm / rust | 9485 (7834-1.114e+04) | 7834, 1.114e+04 | 34.8% |
| conv tail 32 x 5408|downstream_batch|512, 2 threads, cold (20 ms idle) / rust | 1.128e+04 (1.031e+04-1.225e+04) | 1.031e+04, 1.225e+04 | 17.2% |
| conv tail 32 x 5408|downstream_batch|512, 4 threads, warm / rust | 8023 (7827-8218) | 7827, 8218 | 4.9% |
| conv tail 32 x 5408|downstream_batch|512, 4 threads, cold (20 ms idle) / rust | 7730 (7368-8093) | 7368, 8093 | 9.4% |
| conv tail 32 x 5408|downstream_batch|512, 8 threads, warm / rust | 6470 (5249-7691) | 5249, 7691 | 37.7% |
| conv tail 32 x 5408|downstream_batch|512, 8 threads, cold (20 ms idle) / rust | 8078 (8011-8146) | 8011, 8146 | 1.7% |
| conv tail 32 x 5408|downstream_batch|512, 1 thread, warm / numpy (control) | 1.331e+04 (1.328e+04-1.333e+04) | 1.333e+04, 1.328e+04 | 0.4% |
| conv tail 32 x 5408|downstream_batch|512, 1 thread, cold (20 ms idle) / numpy (control) | 1.418e+04 (1.405e+04-1.431e+04) | 1.405e+04, 1.431e+04 | 1.8% |
| conv tail 32 x 5408|downstream_batch|512, 2 threads, warm / numpy (control) | 8577 (8577-8577) | 8577, 8577 | 0.0% |
| conv tail 32 x 5408|downstream_batch|512, 2 threads, cold (20 ms idle) / numpy (control) | 9064 (8801-9327) | 8801, 9327 | 5.8% |
| conv tail 32 x 5408|downstream_batch|512, 4 threads, warm / numpy (control) | 5940 (5937-5944) | 5937, 5944 | 0.1% |
| conv tail 32 x 5408|downstream_batch|512, 4 threads, cold (20 ms idle) / numpy (control) | 6286 (6149-6423) | 6149, 6423 | 4.3% |
| conv tail 32 x 5408|downstream_batch|512, 8 threads, warm / numpy (control) | 6435 (6421-6449) | 6449, 6421 | 0.4% |
| conv tail 32 x 5408|downstream_batch|512, 8 threads, cold (20 ms idle) / numpy (control) | 6623 (6622-6623) | 6622, 6623 | 0.0% |
| conv 26x26x8, 8 ch|downstream_batch|512, 1 thread, warm / rust | 6.248e+04 (5.991e+04-6.506e+04) | 6.506e+04, 5.991e+04 | 8.2% |
| conv 26x26x8, 8 ch|downstream_batch|512, 1 thread, cold (20 ms idle) / rust | 6.355e+04 (6.127e+04-6.584e+04) | 6.127e+04, 6.584e+04 | 7.2% |
| conv 26x26x8, 8 ch|downstream_batch|512, 2 threads, warm / rust | 3.335e+04 (3.103e+04-3.567e+04) | 3.103e+04, 3.567e+04 | 13.9% |
| conv 26x26x8, 8 ch|downstream_batch|512, 2 threads, cold (20 ms idle) / rust | 3.593e+04 (3.218e+04-3.967e+04) | 3.967e+04, 3.218e+04 | 20.8% |
| conv 26x26x8, 8 ch|downstream_batch|512, 4 threads, warm / rust | 1.932e+04 (1.786e+04-2.077e+04) | 2.077e+04, 1.786e+04 | 15.1% |
| conv 26x26x8, 8 ch|downstream_batch|512, 4 threads, cold (20 ms idle) / rust | 1.698e+04 (1.686e+04-1.71e+04) | 1.71e+04, 1.686e+04 | 1.4% |
| conv 26x26x8, 8 ch|downstream_batch|512, 8 threads, warm / rust | 1.798e+04 (1.759e+04-1.836e+04) | 1.836e+04, 1.759e+04 | 4.2% |
| conv 26x26x8, 8 ch|downstream_batch|512, 8 threads, cold (20 ms idle) / rust | 1.76e+04 (1.721e+04-1.799e+04) | 1.721e+04, 1.799e+04 | 4.5% |
| conv 26x26x8, 8 ch|downstream_batch|512, 1 thread, warm / numpy (control) | 2.103e+05 (2.1e+05-2.106e+05) | 2.1e+05, 2.106e+05 | 0.3% |
| conv 26x26x8, 8 ch|downstream_batch|512, 1 thread, cold (20 ms idle) / numpy (control) | 2.109e+05 (2.104e+05-2.115e+05) | 2.115e+05, 2.104e+05 | 0.6% |
| conv 26x26x8, 8 ch|downstream_batch|512, 2 threads, warm / numpy (control) | 2.115e+05 (2.115e+05-2.115e+05) | 2.115e+05, 2.115e+05 | 0.0% |
| conv 26x26x8, 8 ch|downstream_batch|512, 2 threads, cold (20 ms idle) / numpy (control) | 2.117e+05 (2.114e+05-2.12e+05) | 2.12e+05, 2.114e+05 | 0.3% |
| conv 26x26x8, 8 ch|downstream_batch|512, 4 threads, warm / numpy (control) | 2.115e+05 (2.111e+05-2.118e+05) | 2.118e+05, 2.111e+05 | 0.3% |
| conv 26x26x8, 8 ch|downstream_batch|512, 4 threads, cold (20 ms idle) / numpy (control) | 2.123e+05 (2.118e+05-2.129e+05) | 2.129e+05, 2.118e+05 | 0.5% |
| conv 26x26x8, 8 ch|downstream_batch|512, 8 threads, warm / numpy (control) | 2.108e+05 (2.106e+05-2.109e+05) | 2.106e+05, 2.109e+05 | 0.2% |
| conv 26x26x8, 8 ch|downstream_batch|512, 8 threads, cold (20 ms idle) / numpy (control) | 2.13e+05 (2.115e+05-2.146e+05) | 2.146e+05, 2.115e+05 | 1.5% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 51 (51-51) | 51, 51 | 0.0% |
