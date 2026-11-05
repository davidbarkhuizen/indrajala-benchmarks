Old `8722277` against new `8722277`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py calls --threads 1 2 4 8 12` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `362e34c` (extension sha256 `7a3f0df0ecd3`) and new crate `362e34c` (extension sha256 `7a3f0df0ecd3`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-1255u.json); max 1-min load 2.92 (HIGH); busy processes: none. Each row pools 2 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: none (a probe row can carry "control": true)
- 91 rows within noise, max |Δ| 17.3%
- spread of per-pass medians over 91 rows: median 1.4%, 90th percentile 8.6%, max 20.3%
- pass shifts (median over rows of pass median / pooled median): 1 +0.0%, 2 +0.0%

### per call

| case | median (min-max) µs | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 0k steps, warm, scoped, 1 thread | 26.93 (22.7-27.44) | 27.31, 24.69 | 9.7% |
| 100k steps, warm, scoped, 1 thread | 528.9 (485.2-556.2) | 528.9, 520.7 | 1.6% |
| 1000k steps, warm, scoped, 1 thread | 4042 (3915-4106) | 3973, 4080 | 2.6% |
| 0k steps, cold (20 ms idle), scoped, 1 thread | 576.5 (543.3-650.9) | 628.9, 544.8 | 14.6% |
| 100k steps, cold (20 ms idle), scoped, 1 thread | 2181 (2144-2310) | 2227, 2181 | 2.1% |
| 1000k steps, cold (20 ms idle), scoped, 1 thread | 8865 (8676-9052) | 8768, 8961 | 2.2% |
| 0k steps, warm, scoped, 2 threads | 33.44 (31.38-38.69) | 33.34, 35.13 | 5.4% |
| 100k steps, warm, scoped, 2 threads | 266 (262.9-267.6) | 266.6, 264.6 | 0.8% |
| 1000k steps, warm, scoped, 2 threads | 2311 (2296-2332) | 2317, 2309 | 0.3% |
| 0k steps, cold (20 ms idle), scoped, 2 threads | 658.7 (625.2-703.4) | 658.7, 664.3 | 0.9% |
| 100k steps, cold (20 ms idle), scoped, 2 threads | 1544 (1524-1559) | 1534, 1552 | 1.2% |
| 1000k steps, cold (20 ms idle), scoped, 2 threads | 6640 (6593-6679) | 6635, 6641 | 0.1% |
| 0k steps, warm, scoped, 4 threads | 59.08 (57.06-59.23) | 59.15, 58.06 | 1.8% |
| 100k steps, warm, scoped, 4 threads | 182.2 (181.2-182.8) | 181.6, 182.6 | 0.6% |
| 1000k steps, warm, scoped, 4 threads | 1249 (1234-1268) | 1245, 1255 | 0.8% |
| 0k steps, cold (20 ms idle), scoped, 4 threads | 727.8 (712.7-744.3) | 727.8, 728.5 | 0.1% |
| 100k steps, cold (20 ms idle), scoped, 4 threads | 1089 (1068-1093) | 1081, 1089 | 0.7% |
| 1000k steps, cold (20 ms idle), scoped, 4 threads | 4687 (4658-4741) | 4700, 4687 | 0.3% |
| 0k steps, warm, scoped, 8 threads | 125.7 (118.5-127.4) | 122.7, 126 | 2.6% |
| 100k steps, warm, scoped, 8 threads | 224.9 (166.3-229.9) | 227.7, 195.3 | 14.4% |
| 1000k steps, warm, scoped, 8 threads | 897.5 (839.5-965.3) | 863.7, 936.2 | 8.1% |
| 0k steps, cold (20 ms idle), scoped, 8 threads | 1202 (1135-1263) | 1225, 1176 | 4.0% |
| 100k steps, cold (20 ms idle), scoped, 8 threads | 1071 (991.1-1127) | 1030, 1100 | 6.6% |
| 1000k steps, cold (20 ms idle), scoped, 8 threads | 2922 (2863-2970) | 2935, 2904 | 1.0% |
| 0k steps, warm, scoped, 12 threads | 175.8 (161.7-181.4) | 168.3, 179.1 | 6.1% |
| 100k steps, warm, scoped, 12 threads | 252.7 (244.3-254.9) | 253.8, 248.5 | 2.1% |
| 1000k steps, warm, scoped, 12 threads | 737.2 (650.1-762.3) | 699.9, 743.5 | 5.9% |
| 0k steps, cold (20 ms idle), scoped, 12 threads | 1563 (1512-1614) | 1563, 1563 | 0.0% |
| 100k steps, cold (20 ms idle), scoped, 12 threads | 1679 (1620-1759) | 1658, 1710 | 3.1% |
| 1000k steps, cold (20 ms idle), scoped, 12 threads | 2573 (2346-2581) | 2579, 2458 | 4.7% |
| 0k steps, warm, pool, spin 0 µs, 1 thread | 0.04898 (0.04395-0.05308) | 0.04849, 0.049 | 1.0% |
| 100k steps, warm, pool, spin 0 µs, 1 thread | 282.9 (256.1-309.1) | 282.6, 282.9 | 0.1% |
| 1000k steps, warm, pool, spin 0 µs, 1 thread | 2827 (2564-3091) | 2827, 2827 | 0.0% |
| 0k steps, cold (20 ms idle), pool, spin 0 µs, 1 thread | 1.661 (1.655-1.739) | 1.698, 1.66 | 2.3% |
| 100k steps, cold (20 ms idle), pool, spin 0 µs, 1 thread | 1123 (1054-1155) | 1091, 1137 | 4.1% |
| 1000k steps, cold (20 ms idle), pool, spin 0 µs, 1 thread | 7406 (7377-7543) | 7406, 7460 | 0.7% |
| 0k steps, warm, pool, spin 0 µs, 2 threads | 0.3698 (0.3517-0.3877) | 0.384, 0.3555 | 7.7% |
| 100k steps, warm, pool, spin 0 µs, 2 threads | 177.8 (177.6-178) | 177.9, 177.7 | 0.1% |
| 1000k steps, warm, pool, spin 0 µs, 2 threads | 1764 (1756-1773) | 1765, 1764 | 0.0% |
| 0k steps, cold (20 ms idle), pool, spin 0 µs, 2 threads | 10.58 (9.905-12.09) | 11.17, 10.41 | 7.2% |
| 100k steps, cold (20 ms idle), pool, spin 0 µs, 2 threads | 763.1 (756.1-775.3) | 761.7, 767.2 | 0.7% |
| 1000k steps, cold (20 ms idle), pool, spin 0 µs, 2 threads | 4956 (4764-5015) | 4857, 4988 | 2.6% |
| 0k steps, warm, pool, spin 0 µs, 4 threads | 0.7514 (0.7195-0.8507) | 0.8022, 0.7343 | 9.0% |
| 100k steps, warm, pool, spin 0 µs, 4 threads | 111.3 (110.5-111.9) | 111.3, 111.2 | 0.1% |
| 1000k steps, warm, pool, spin 0 µs, 4 threads | 1109 (1099-1124) | 1112, 1109 | 0.2% |
| 0k steps, cold (20 ms idle), pool, spin 0 µs, 4 threads | 15.07 (13.93-15.55) | 14.4, 15.4 | 6.6% |
| 100k steps, cold (20 ms idle), pool, spin 0 µs, 4 threads | 516.7 (499.4-553.4) | 510.6, 532.5 | 4.2% |
| 1000k steps, cold (20 ms idle), pool, spin 0 µs, 4 threads | 3128 (3105-3179) | 3150, 3120 | 1.0% |
| 0k steps, warm, pool, spin 0 µs, 8 threads | 2.398 (2.255-2.569) | 2.412, 2.398 | 0.6% |
| 100k steps, warm, pool, spin 0 µs, 8 threads | 78.55 (77.86-78.81) | 78.33, 78.55 | 0.3% |
| 1000k steps, warm, pool, spin 0 µs, 8 threads | 787.4 (756.3-797.4) | 776.2, 788.1 | 1.5% |
| 0k steps, cold (20 ms idle), pool, spin 0 µs, 8 threads | 20.77 (19.39-21.8) | 21.39, 19.98 | 6.8% |
| 100k steps, cold (20 ms idle), pool, spin 0 µs, 8 threads | 383.3 (370.6-393.4) | 383.3, 382 | 0.3% |
| 1000k steps, cold (20 ms idle), pool, spin 0 µs, 8 threads | 1861 (1811-1942) | 1831, 1907 | 4.1% |
| 0k steps, warm, pool, spin 0 µs, 12 threads | 4.616 (4.185-4.652) | 4.631, 4.403 | 4.9% |
| 100k steps, warm, pool, spin 0 µs, 12 threads | 58.72 (58.28-59.23) | 58.84, 58.64 | 0.4% |
| 1000k steps, warm, pool, spin 0 µs, 12 threads | 574.1 (516-582) | 543.1, 580 | 6.4% |
| 0k steps, cold (20 ms idle), pool, spin 0 µs, 12 threads | 28.78 (28.15-29.67) | 28.72, 28.97 | 0.9% |
| 100k steps, cold (20 ms idle), pool, spin 0 µs, 12 threads | 353.7 (352.4-358.2) | 355.9, 353.1 | 0.8% |
| 1000k steps, cold (20 ms idle), pool, spin 0 µs, 12 threads | 1557 (1471-1582) | 1527, 1557 | 1.9% |
| 0k steps, warm, pool, spin 50 µs, 1 thread | 0.05322 (0.05299-0.05364) | 0.05318, 0.05336 | 0.3% |
| 100k steps, warm, pool, spin 50 µs, 1 thread | 309 (256.2-309.1) | 309.1, 282.5 | 8.6% |
| 1000k steps, warm, pool, spin 50 µs, 1 thread | 3090 (3090-3093) | 3090, 3092 | 0.0% |
| 0k steps, cold (20 ms idle), pool, spin 50 µs, 1 thread | 1.698 (1.185-1.798) | 1.698, 1.492 | 12.2% |
| 100k steps, cold (20 ms idle), pool, spin 50 µs, 1 thread | 1156 (1141-1168) | 1149, 1162 | 1.2% |
| 1000k steps, cold (20 ms idle), pool, spin 50 µs, 1 thread | 7646 (7293-7992) | 7872, 7417 | 5.9% |
| 0k steps, warm, pool, spin 50 µs, 2 threads | 0.2119 (0.1824-0.2332) | 0.2119, 0.2078 | 1.9% |
| 100k steps, warm, pool, spin 50 µs, 2 threads | 177.3 (177.2-177.4) | 177.4, 177.2 | 0.1% |
| 1000k steps, warm, pool, spin 50 µs, 2 threads | 1789 (1759-1825) | 1792, 1789 | 0.2% |
| 0k steps, cold (20 ms idle), pool, spin 50 µs, 2 threads | 11.39 (10.36-15.75) | 13.38, 11.07 | 20.3% |
| 100k steps, cold (20 ms idle), pool, spin 50 µs, 2 threads | 751.5 (740.1-758.5) | 753.5, 747.4 | 0.8% |
| 1000k steps, cold (20 ms idle), pool, spin 50 µs, 2 threads | 4813 (4767-4892) | 4799, 4844 | 0.9% |
| 0k steps, warm, pool, spin 50 µs, 4 threads | 0.7048 (0.6182-0.7706) | 0.6678, 0.7314 | 9.0% |
| 100k steps, warm, pool, spin 50 µs, 4 threads | 110.1 (109.6-110.8) | 110.1, 110.2 | 0.1% |
| 1000k steps, warm, pool, spin 50 µs, 4 threads | 1100 (1095-1103) | 1101, 1098 | 0.3% |
| 0k steps, cold (20 ms idle), pool, spin 50 µs, 4 threads | 14.43 (11.73-16.15) | 13.31, 15.06 | 12.1% |
| 100k steps, cold (20 ms idle), pool, spin 50 µs, 4 threads | 510.1 (508.4-544.9) | 526.7, 510.1 | 3.3% |
| 1000k steps, cold (20 ms idle), pool, spin 50 µs, 4 threads | 3173 (3109-3310) | 3210, 3173 | 1.2% |
| 0k steps, warm, pool, spin 50 µs, 8 threads | 1.982 (1.491-2.078) | 2.022, 1.745 | 14.0% |
| 100k steps, warm, pool, spin 50 µs, 8 threads | 75.05 (73.07-75.15) | 75.09, 74.07 | 1.4% |
| 1000k steps, warm, pool, spin 50 µs, 8 threads | 722.7 (706.2-728.4) | 714.1, 725.8 | 1.6% |
| 0k steps, cold (20 ms idle), pool, spin 50 µs, 8 threads | 21.61 (19.73-24.37) | 22.05, 21.61 | 2.0% |
| 100k steps, cold (20 ms idle), pool, spin 50 µs, 8 threads | 393 (374.1-410.4) | 403, 382.2 | 5.3% |
| 1000k steps, cold (20 ms idle), pool, spin 50 µs, 8 threads | 1904 (1865-1974) | 1899, 1925 | 1.3% |
| 0k steps, warm, pool, spin 50 µs, 12 threads | 2.686 (2.611-2.808) | 2.71, 2.686 | 0.9% |
| 100k steps, warm, pool, spin 50 µs, 12 threads | 53.62 (53.49-53.87) | 53.62, 53.68 | 0.1% |
| 1000k steps, warm, pool, spin 50 µs, 12 threads | 514.9 (512.4-528.4) | 520.4, 514.9 | 1.1% |
| 0k steps, cold (20 ms idle), pool, spin 50 µs, 12 threads | 31.68 (31.04-33.83) | 31.22, 32.9 | 5.3% |
| 100k steps, cold (20 ms idle), pool, spin 50 µs, 12 threads | 367.4 (355.6-372.6) | 364.1, 367.4 | 0.9% |
| 1000k steps, cold (20 ms idle), pool, spin 50 µs, 12 threads | 1556 (1539-1583) | 1556, 1561 | 0.3% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 20 (20-20) | 20, 20 | 0.0% |
