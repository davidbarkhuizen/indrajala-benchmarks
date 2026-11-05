Old `f081ecf` against new `f081ecf`, run with `scripts/measurement/ab.py`: passes in the order ONNO. Each pass ran `python scripts/measurement/thread_cost_probe.py calls` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `7a3f0df0ecd3`) on both sides. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.00; busy processes: none. Each row pools 4 runs per side.

- controls: none (a probe row can carry "control": true)
- consistent: per call / 100k steps, warm, scoped, 1 thread -38.7% (1911 -> 1171 µs)
- consistent: per call / 100k steps, warm, scoped, 8 threads -34.8% (312 -> 203.3 µs)
- consistent: per call / 0k steps, cold (20 ms idle), pool, spin 50 µs, 1 thread +8.3% (0.9543 -> 1.033 µs)
- consistent: per call / 0k steps, cold (20 ms idle), pool, spin 0 µs, 1 thread -5.8% (1.027 -> 0.9667 µs)
- consistent: per call / 0k steps, cold (20 ms idle), scoped, 2 threads -2.4% (337.7 -> 329.5 µs)
- consistent, small: per call / 100k steps, warm, pool, spin 0 µs, 2 threads -0.1% (139.5 -> 139.3 µs)
- consistent, small: per call / 100k steps, warm, pool, spin 50 µs, 4 threads +0.0% (71.2 -> 71.23 µs)
- consistent, small: per call / 1000k steps, warm, pool, spin 0 µs, 8 threads +0.0% (357.6 -> 357.6 µs)
- consistent, small: per call / 100k steps, warm, pool, spin 0 µs, 1 thread +0.0% (272.2 -> 272.2 µs)
- 64 rows within noise (18 separated inside their spread), max |Δ| 245.1%
- spread of per-pass medians over 73 rows: median 1.3%, 90th percentile 26.7%, max 249.0%
- pass shifts (median over rows of pass median / pooled median): 1 +0.0%, 2 -0.0%, 3 +0.0%, 4 +0.0%

### per call

| case | median (min-max) µs | per-pass medians (1, 2, 3, 4) | spread |
|---|---|---|---|
| 0k steps, warm, scoped, 1 thread | 100.3 (20.95-180.7) | 100, 99.59, 101.6, 100.8 | 2.0% |
| 100k steps, warm, scoped, 1 thread | 1911 (410.3-1925) | 1860, 1171, 1166, 1918 | 39.3% |
| 1000k steps, warm, scoped, 1 thread | 7353 (3759-1.217e+04) | 1.175e+04, 6953, 6402, 4807 | 94.4% |
| 0k steps, cold (20 ms idle), scoped, 1 thread | 277.5 (255.2-284) | 265.8, 265.3, 281.2, 282.6 | 6.2% |
| 100k steps, cold (20 ms idle), scoped, 1 thread | 1918 (1906-1933) | 1913, 1916, 1919, 1930 | 0.9% |
| 1000k steps, cold (20 ms idle), scoped, 1 thread | 1.667e+04 (1.665e+04-1.668e+04) | 1.666e+04, 1.666e+04, 1.667e+04, 1.667e+04 | 0.1% |
| 0k steps, warm, scoped, 2 threads | 144.8 (38.27-245.6) | 144.8, 151.5, 143.7, 136.2 | 10.5% |
| 100k steps, warm, scoped, 2 threads | 776.1 (257.1-1144) | 776.3, 711.1, 712.4, 699.7 | 9.9% |
| 1000k steps, warm, scoped, 2 threads | 4360 (1563-8543) | 5770, 5050, 5184, 3856 | 43.9% |
| 0k steps, cold (20 ms idle), scoped, 2 threads | 332.5 (325.3-342.4) | 335.8, 327.8, 331.7, 337.7 | 3.0% |
| 100k steps, cold (20 ms idle), scoped, 2 threads | 1147 (1138-1159) | 1145, 1147, 1146, 1152 | 0.6% |
| 1000k steps, cold (20 ms idle), scoped, 2 threads | 8525 (7275-8541) | 7605, 8535, 8470, 8526 | 10.9% |
| 0k steps, warm, scoped, 4 threads | 58.66 (50.9-357.5) | 58.53, 202, 204.6, 193.3 | 249.0% |
| 100k steps, warm, scoped, 4 threads | 121.7 (119.6-410.5) | 119.7, 265.7, 182.5, 217.6 | 120.0% |
| 1000k steps, warm, scoped, 4 threads | 861.7 (851.4-968.9) | 859.1, 859.6, 915.5, 864.6 | 6.5% |
| 0k steps, cold (20 ms idle), scoped, 4 threads | 559 (519-575.6) | 560.2, 567.4, 540.7, 549.7 | 4.8% |
| 100k steps, cold (20 ms idle), scoped, 4 threads | 794.3 (783.1-811) | 785.3, 806.9, 792.4, 800.7 | 2.7% |
| 1000k steps, cold (20 ms idle), scoped, 4 threads | 4492 (4481-4500) | 4492, 4491, 4485, 4499 | 0.3% |
| 0k steps, warm, scoped, 8 threads | 402.4 (125.6-571.4) | 405.3, 337.6, 376.4, 413.3 | 18.8% |
| 100k steps, warm, scoped, 8 threads | 224.2 (177.3-400.3) | 289.6, 203.3, 243.6, 314.9 | 49.8% |
| 1000k steps, warm, scoped, 8 threads | 544.5 (440.2-2551) | 1496, 543.7, 1485, 1498 | 175.2% |
| 0k steps, cold (20 ms idle), scoped, 8 threads | 964.3 (881.9-1018) | 949.7, 960.1, 956.6, 985.5 | 3.7% |
| 100k steps, cold (20 ms idle), scoped, 8 threads | 692.2 (687.2-707.1) | 694.3, 697.2, 695.2, 689.6 | 1.1% |
| 1000k steps, cold (20 ms idle), scoped, 8 threads | 2571 (2553-2577) | 2565, 2565, 2571, 2569 | 0.3% |
| 0k steps, warm, pool, spin 0 µs, 1 thread | 0.09004 (0.04862-0.1515) | 0.09355, 0.08964, 0.1001, 0.0889 | 12.4% |
| 100k steps, warm, pool, spin 0 µs, 1 thread | 272.2 (272.2-272.2) | 272.2, 272.2, 272.2, 272.2 | 0.0% |
| 1000k steps, warm, pool, spin 0 µs, 1 thread | 2722 (2718-2722) | 2720, 2720, 2722, 2722 | 0.1% |
| 0k steps, cold (20 ms idle), pool, spin 0 µs, 1 thread | 1.004 (0.961-1.051) | 1.029, 0.9817, 0.966, 1.027 | 6.3% |
| 100k steps, cold (20 ms idle), pool, spin 0 µs, 1 thread | 1651 (1651-1652) | 1651, 1651, 1651, 1651 | 0.0% |
| 1000k steps, cold (20 ms idle), pool, spin 0 µs, 1 thread | 1.64e+04 (1.639e+04-1.64e+04) | 1.64e+04, 1.64e+04, 1.64e+04, 1.64e+04 | 0.0% |
| 0k steps, warm, pool, spin 0 µs, 2 threads | 0.3734 (0.3181-0.4304) | 0.3734, 0.4118, 0.3449, 0.3509 | 17.9% |
| 100k steps, warm, pool, spin 0 µs, 2 threads | 139.3 (139.3-139.6) | 139.5, 139.3, 139.3, 139.4 | 0.2% |
| 1000k steps, warm, pool, spin 0 µs, 2 threads | 1389 (1388-1392) | 1389, 1389, 1389, 1390 | 0.1% |
| 0k steps, cold (20 ms idle), pool, spin 0 µs, 2 threads | 6.776 (6.443-7.059) | 6.472, 6.93, 6.718, 6.803 | 6.8% |
| 100k steps, cold (20 ms idle), pool, spin 0 µs, 2 threads | 900.5 (883-909.6) | 902.9, 892.3, 900.6, 903.7 | 1.3% |
| 1000k steps, cold (20 ms idle), pool, spin 0 µs, 2 threads | 8275 (8272-8278) | 8276, 8276, 8273, 8275 | 0.0% |
| 0k steps, warm, pool, spin 0 µs, 4 threads | 0.6375 (0.6198-0.6526) | 0.6393, 0.6452, 0.6247, 0.635 | 3.2% |
| 100k steps, warm, pool, spin 0 µs, 4 threads | 72.96 (72.92-73.1) | 72.97, 72.98, 72.95, 73.01 | 0.1% |
| 1000k steps, warm, pool, spin 0 µs, 4 threads | 711.2 (711.2-711.3) | 711.2, 711.2, 711.2, 711.2 | 0.0% |
| 0k steps, cold (20 ms idle), pool, spin 0 µs, 4 threads | 8.032 (7.714-8.248) | 8.007, 7.864, 8.016, 8.091 | 2.8% |
| 100k steps, cold (20 ms idle), pool, spin 0 µs, 4 threads | 510 (502.8-516.1) | 508.2, 510, 510.5, 511.3 | 0.6% |
| 1000k steps, cold (20 ms idle), pool, spin 0 µs, 4 threads | 4205 (4203-4209) | 4206, 4205, 4205, 4204 | 0.0% |
| 0k steps, warm, pool, spin 0 µs, 8 threads | 1.626 (1.487-1.739) | 1.674, 1.565, 1.614, 1.619 | 6.7% |
| 100k steps, warm, pool, spin 0 µs, 8 threads | 39.26 (39.16-39.34) | 39.3, 39.22, 39.24, 39.23 | 0.2% |
| 1000k steps, warm, pool, spin 0 µs, 8 threads | 357.6 (357.5-357.8) | 357.6, 357.7, 357.6, 357.6 | 0.0% |
| 0k steps, cold (20 ms idle), pool, spin 0 µs, 8 threads | 11.41 (11.03-11.78) | 11.4, 11.12, 11.5, 11.61 | 4.3% |
| 100k steps, cold (20 ms idle), pool, spin 0 µs, 8 threads | 326.9 (322.4-330.2) | 329.1, 324.6, 325.1, 326.9 | 1.4% |
| 1000k steps, cold (20 ms idle), pool, spin 0 µs, 8 threads | 2191 (2184-2193) | 2190, 2186, 2191, 2193 | 0.3% |
| 0k steps, warm, pool, spin 50 µs, 1 thread | 0.1086 (0.04857-0.2266) | 0.1376, 0.1091, 0.1086, 0.1136 | 26.7% |
| 100k steps, warm, pool, spin 50 µs, 1 thread | 272.2 (272.2-272.2) | 272.2, 272.2, 272.2, 272.2 | 0.0% |
| 1000k steps, warm, pool, spin 50 µs, 1 thread | 2722 (2721-2722) | 2722, 2722, 2722, 2722 | 0.0% |
| 0k steps, cold (20 ms idle), pool, spin 50 µs, 1 thread | 0.9859 (0.9242-1.12) | 0.9335, 1.032, 1.054, 0.978 | 12.2% |
| 100k steps, cold (20 ms idle), pool, spin 50 µs, 1 thread | 1651 (1650-1652) | 1650, 1651, 1652, 1650 | 0.1% |
| 1000k steps, cold (20 ms idle), pool, spin 50 µs, 1 thread | 1.64e+04 (1.639e+04-1.64e+04) | 1.64e+04, 1.639e+04, 1.64e+04, 1.64e+04 | 0.1% |
| 0k steps, warm, pool, spin 50 µs, 2 threads | 0.1632 (0.153-0.1747) | 0.1641, 0.1632, 0.163, 0.1659 | 1.8% |
| 100k steps, warm, pool, spin 50 µs, 2 threads | 139 (138.9-139) | 139, 139, 138.9, 139 | 0.0% |
| 1000k steps, warm, pool, spin 50 µs, 2 threads | 1388 (1388-1388) | 1388, 1388, 1388, 1388 | 0.0% |
| 0k steps, cold (20 ms idle), pool, spin 50 µs, 2 threads | 6.6 (6.379-6.806) | 6.565, 6.405, 6.783, 6.689 | 5.7% |
| 100k steps, cold (20 ms idle), pool, spin 50 µs, 2 threads | 899.7 (881.8-908.7) | 891.4, 893.8, 900.6, 903.9 | 1.4% |
| 1000k steps, cold (20 ms idle), pool, spin 50 µs, 2 threads | 8277 (8272-8283) | 8278, 8276, 8278, 8278 | 0.0% |
| 0k steps, warm, pool, spin 50 µs, 4 threads | 0.4205 (0.3629-0.4807) | 0.3974, 0.3896, 0.4681, 0.4342 | 18.7% |
| 100k steps, warm, pool, spin 50 µs, 4 threads | 71.21 (71.19-71.25) | 71.2, 71.22, 71.23, 71.2 | 0.0% |
| 1000k steps, warm, pool, spin 50 µs, 4 threads | 709.3 (709.3-709.5) | 709.3, 709.3, 709.3, 709.4 | 0.0% |
| 0k steps, cold (20 ms idle), pool, spin 50 µs, 4 threads | 7.891 (7.741-8.485) | 8.1, 7.804, 7.839, 8.398 | 7.5% |
| 100k steps, cold (20 ms idle), pool, spin 50 µs, 4 threads | 505 (503-515.5) | 505.6, 504.6, 505, 509.8 | 1.0% |
| 1000k steps, cold (20 ms idle), pool, spin 50 µs, 4 threads | 4207 (4203-4211) | 4208, 4207, 4206, 4206 | 0.0% |
| 0k steps, warm, pool, spin 50 µs, 8 threads | 0.8163 (0.7003-0.8509) | 0.8163, 0.7484, 0.8421, 0.7764 | 11.5% |
| 100k steps, warm, pool, spin 50 µs, 8 threads | 36.1 (36.07-36.14) | 36.09, 36.09, 36.13, 36.1 | 0.1% |
| 1000k steps, warm, pool, spin 50 µs, 8 threads | 355.2 (355.1-355.7) | 355.2, 355.2, 355.2, 355.4 | 0.1% |
| 0k steps, cold (20 ms idle), pool, spin 50 µs, 8 threads | 11.27 (11.12-11.64) | 11.44, 11.17, 11.29, 11.38 | 2.5% |
| 100k steps, cold (20 ms idle), pool, spin 50 µs, 8 threads | 324 (321.5-327.2) | 322.6, 326.1, 324.3, 322.9 | 1.1% |
| 1000k steps, cold (20 ms idle), pool, spin 50 µs, 8 threads | 2183 (2181-2186) | 2184, 2182, 2183, 2182 | 0.1% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2, 3, 4) | spread |
|---|---|---|---|
| the probe | 27.8 (27.8-27.8) | 27.8, 27.8, 27.8, 27.8 | 0.0% |
