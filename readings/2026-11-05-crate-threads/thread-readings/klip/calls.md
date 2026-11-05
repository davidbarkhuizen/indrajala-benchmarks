Old `8722277` against new `8722277`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py calls` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `362e34c` (extension sha256 `7a3f0df0ecd3`) and new crate `362e34c` (extension sha256 `7a3f0df0ecd3`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (ryzen7-3700u-klip.json); max 1-min load 5.60 (HIGH); busy processes: none. Each row pools 2 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: none (a probe row can carry "control": true)
- 73 rows within noise, max |Δ| 21.1%
- spread of per-pass medians over 73 rows: median 0.9%, 90th percentile 8.7%, max 19.7%
- pass shifts (median over rows of pass median / pooled median): 1 +0.0%, 2 +0.0%

### per call

| case | median (min-max) µs | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 0k steps, warm, scoped, 1 thread | 55.97 (54.47-75.35) | 55.62, 65.27 | 17.2% |
| 100k steps, warm, scoped, 1 thread | 1022 (819-1085) | 1050, 923.3 | 12.4% |
| 1000k steps, warm, scoped, 1 thread | 1.012e+04 (8076-1.107e+04) | 9573, 1.012e+04 | 5.4% |
| 0k steps, cold (20 ms idle), scoped, 1 thread | 283.3 (279.1-288.3) | 286.8, 280.2 | 2.3% |
| 100k steps, cold (20 ms idle), scoped, 1 thread | 1426 (1419-1441) | 1430, 1426 | 0.3% |
| 1000k steps, cold (20 ms idle), scoped, 1 thread | 1.047e+04 (9357-1.125e+04) | 9932, 1.085e+04 | 8.7% |
| 0k steps, warm, scoped, 2 threads | 95.13 (92.14-98.79) | 93.9, 96.69 | 2.9% |
| 100k steps, warm, scoped, 2 threads | 702 (613.8-752.9) | 683.4, 702 | 2.7% |
| 1000k steps, warm, scoped, 2 threads | 5927 (5639-6284) | 5927, 5962 | 0.6% |
| 0k steps, cold (20 ms idle), scoped, 2 threads | 330.7 (320.1-348.7) | 330.7, 334.4 | 1.1% |
| 100k steps, cold (20 ms idle), scoped, 2 threads | 916 (902.9-924.8) | 921.6, 908.3 | 1.4% |
| 1000k steps, cold (20 ms idle), scoped, 2 threads | 6386 (5845-6890) | 5913, 6841 | 14.5% |
| 0k steps, warm, scoped, 4 threads | 147.1 (144.6-150.6) | 147.6, 147.1 | 0.4% |
| 100k steps, warm, scoped, 4 threads | 557.5 (432.3-609.1) | 519.3, 559 | 7.1% |
| 1000k steps, warm, scoped, 4 threads | 3304 (2985-3606) | 3560, 3038 | 15.8% |
| 0k steps, cold (20 ms idle), scoped, 4 threads | 411.8 (377.6-432.3) | 421.8, 394.9 | 6.5% |
| 100k steps, cold (20 ms idle), scoped, 4 threads | 653.6 (648-680.7) | 667.3, 650.7 | 2.5% |
| 1000k steps, cold (20 ms idle), scoped, 4 threads | 3144 (2963-3573) | 3314, 3099 | 6.8% |
| 0k steps, warm, scoped, 8 threads | 241.9 (239.5-244) | 240.1, 243.5 | 1.4% |
| 100k steps, warm, scoped, 8 threads | 345.8 (341.4-361.2) | 345.8, 351.3 | 1.6% |
| 1000k steps, warm, scoped, 8 threads | 1491 (1078-1901) | 1491, 1489 | 0.1% |
| 0k steps, cold (20 ms idle), scoped, 8 threads | 586.1 (559.7-588.4) | 572, 588.1 | 2.8% |
| 100k steps, cold (20 ms idle), scoped, 8 threads | 665.3 (628.1-701.5) | 665.3, 664.8 | 0.1% |
| 1000k steps, cold (20 ms idle), scoped, 8 threads | 1827 (1808-1946) | 1814, 1890 | 4.2% |
| 0k steps, warm, pool, spin 0 µs, 1 thread | 0.1338 (0.1332-0.1341) | 0.1339, 0.1335 | 0.3% |
| 100k steps, warm, pool, spin 0 µs, 1 thread | 659.6 (659.4-660.5) | 660, 659.5 | 0.1% |
| 1000k steps, warm, pool, spin 0 µs, 1 thread | 6593 (6588-6595) | 6593, 6591 | 0.0% |
| 0k steps, cold (20 ms idle), pool, spin 0 µs, 1 thread | 1.615 (1.407-2.114) | 1.76, 1.615 | 9.0% |
| 100k steps, cold (20 ms idle), pool, spin 0 µs, 1 thread | 1133 (1132-1135) | 1133, 1134 | 0.1% |
| 1000k steps, cold (20 ms idle), pool, spin 0 µs, 1 thread | 1.058e+04 (6605-1.088e+04) | 8742, 1.058e+04 | 17.4% |
| 0k steps, warm, pool, spin 0 µs, 2 threads | 0.8222 (0.6705-0.9735) | 0.8222, 0.822 | 0.0% |
| 100k steps, warm, pool, spin 0 µs, 2 threads | 333.5 (332.6-333.6) | 333, 333.6 | 0.2% |
| 1000k steps, warm, pool, spin 0 µs, 2 threads | 3315 (3311-3321) | 3316, 3314 | 0.1% |
| 0k steps, cold (20 ms idle), pool, spin 0 µs, 2 threads | 12.38 (11.8-12.84) | 12.32, 12.38 | 0.5% |
| 100k steps, cold (20 ms idle), pool, spin 0 µs, 2 threads | 661.7 (660.8-670.2) | 665.5, 661.7 | 0.6% |
| 1000k steps, cold (20 ms idle), pool, spin 0 µs, 2 threads | 5498 (5451-5713) | 5464, 5615 | 2.7% |
| 0k steps, warm, pool, spin 0 µs, 4 threads | 1.217 (1.206-1.224) | 1.218, 1.214 | 0.3% |
| 100k steps, warm, pool, spin 0 µs, 4 threads | 172.4 (172.4-173) | 172.4, 172.7 | 0.1% |
| 1000k steps, warm, pool, spin 0 µs, 4 threads | 1663 (1659-1664) | 1661, 1663 | 0.1% |
| 0k steps, cold (20 ms idle), pool, spin 0 µs, 4 threads | 16.38 (15.4-17.93) | 16.38, 16.67 | 1.8% |
| 100k steps, cold (20 ms idle), pool, spin 0 µs, 4 threads | 394.2 (389.2-404.8) | 397, 394.2 | 0.7% |
| 1000k steps, cold (20 ms idle), pool, spin 0 µs, 4 threads | 2773 (2767-2841) | 2773, 2804 | 1.1% |
| 0k steps, warm, pool, spin 0 µs, 8 threads | 3.027 (2.931-3.264) | 2.978, 3.147 | 5.6% |
| 100k steps, warm, pool, spin 0 µs, 8 threads | 92.66 (92.49-93.65) | 93.15, 92.58 | 0.6% |
| 1000k steps, warm, pool, spin 0 µs, 8 threads | 834.7 (833.8-837) | 836, 834.1 | 0.2% |
| 0k steps, cold (20 ms idle), pool, spin 0 µs, 8 threads | 30.23 (28.79-31.31) | 31.06, 29.23 | 6.1% |
| 100k steps, cold (20 ms idle), pool, spin 0 µs, 8 threads | 259.6 (255.9-267.7) | 261.8, 259.6 | 0.8% |
| 1000k steps, cold (20 ms idle), pool, spin 0 µs, 8 threads | 1612 (1512-1714) | 1611, 1614 | 0.2% |
| 0k steps, warm, pool, spin 50 µs, 1 thread | 0.1336 (0.1335-0.1337) | 0.1336, 0.1336 | 0.0% |
| 100k steps, warm, pool, spin 50 µs, 1 thread | 659.5 (658.8-660) | 659.6, 659.4 | 0.0% |
| 1000k steps, warm, pool, spin 50 µs, 1 thread | 6595 (6592-6599) | 6595, 6595 | 0.0% |
| 0k steps, cold (20 ms idle), pool, spin 50 µs, 1 thread | 1.57 (1.473-1.791) | 1.539, 1.663 | 7.9% |
| 100k steps, cold (20 ms idle), pool, spin 50 µs, 1 thread | 1133 (1080-1136) | 1133, 1108 | 2.2% |
| 1000k steps, cold (20 ms idle), pool, spin 50 µs, 1 thread | 1.088e+04 (6597-1.089e+04) | 1.088e+04, 8743 | 19.7% |
| 0k steps, warm, pool, spin 50 µs, 2 threads | 0.4606 (0.4326-0.5281) | 0.4859, 0.455 | 6.7% |
| 100k steps, warm, pool, spin 50 µs, 2 threads | 331.3 (331.2-331.6) | 331.3, 331.4 | 0.0% |
| 1000k steps, warm, pool, spin 50 µs, 2 threads | 3308 (3306-3309) | 3307, 3308 | 0.0% |
| 0k steps, cold (20 ms idle), pool, spin 50 µs, 2 threads | 12.22 (11.94-12.86) | 12.01, 12.61 | 5.0% |
| 100k steps, cold (20 ms idle), pool, spin 50 µs, 2 threads | 662.2 (661.8-665.5) | 663.9, 662 | 0.3% |
| 1000k steps, cold (20 ms idle), pool, spin 50 µs, 2 threads | 5516 (5475-5600) | 5478, 5576 | 1.8% |
| 0k steps, warm, pool, spin 50 µs, 4 threads | 0.9335 (0.9067-0.9509) | 0.9461, 0.9162 | 3.2% |
| 100k steps, warm, pool, spin 50 µs, 4 threads | 166.4 (166.3-166.6) | 166.4, 166.5 | 0.1% |
| 1000k steps, warm, pool, spin 50 µs, 4 threads | 1656 (1653-1659) | 1656, 1656 | 0.0% |
| 0k steps, cold (20 ms idle), pool, spin 50 µs, 4 threads | 16.15 (15.63-17.71) | 16.67, 16.15 | 3.2% |
| 100k steps, cold (20 ms idle), pool, spin 50 µs, 4 threads | 400.4 (386-407.5) | 396.7, 400.4 | 0.9% |
| 1000k steps, cold (20 ms idle), pool, spin 50 µs, 4 threads | 2808 (2768-2874) | 2825, 2804 | 0.8% |
| 0k steps, warm, pool, spin 50 µs, 8 threads | 1.433 (1.394-1.498) | 1.433, 1.446 | 0.9% |
| 100k steps, warm, pool, spin 50 µs, 8 threads | 83.76 (83.71-83.99) | 83.86, 83.75 | 0.1% |
| 1000k steps, warm, pool, spin 50 µs, 8 threads | 826.7 (825.8-828) | 827.1, 826.5 | 0.1% |
| 0k steps, cold (20 ms idle), pool, spin 50 µs, 8 threads | 28.16 (27.32-29.34) | 28.33, 28.16 | 0.6% |
| 100k steps, cold (20 ms idle), pool, spin 50 µs, 8 threads | 258.7 (254.7-272.5) | 258.7, 263.6 | 1.9% |
| 1000k steps, cold (20 ms idle), pool, spin 50 µs, 8 threads | 1514 (1511-1530) | 1521, 1514 | 0.5% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 40 (40-40) | 40, 40 | 0.0% |
