Old `4176d10` against new `4176d10`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py calls --threads 1 2 4` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `17d1c27f71b0`) on both sides. Machine check: profile: identity matches (raspberry-pi-5.json); passes peaked at 43.5-44.6 C; max 1-min load 0.47; busy processes: none. Each row pools 2 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: none (a probe row can carry "control": true)
- 55 rows within noise, max |Δ| 7.6%
- spread of per-pass medians over 55 rows: median 0.4%, 90th percentile 2.2%, max 8.1%
- pass shifts (median over rows of pass median / pooled median): 1 +0.0%, 2 +0.0%

### per call

| case | median (min-max) µs | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 0k steps, warm, scoped, 1 thread | 30.84 (30.29-31.49) | 30.84, 30.89 | 0.2% |
| 100k steps, warm, scoped, 1 thread | 504.8 (503.3-505.9) | 503.7, 505.8 | 0.4% |
| 1000k steps, warm, scoped, 1 thread | 4686 (4676-4694) | 4692, 4679 | 0.3% |
| 0k steps, cold (20 ms idle), scoped, 1 thread | 26.52 (26.04-27.76) | 27.17, 26.25 | 3.5% |
| 100k steps, cold (20 ms idle), scoped, 1 thread | 516 (513.1-516.9) | 515, 516 | 0.2% |
| 1000k steps, cold (20 ms idle), scoped, 1 thread | 4690 (4677-4696) | 4695, 4681 | 0.3% |
| 0k steps, warm, scoped, 2 threads | 51.81 (50.75-53.02) | 51.06, 52.63 | 3.0% |
| 100k steps, warm, scoped, 2 threads | 287.9 (287.2-291.1) | 289.3, 287.7 | 0.6% |
| 1000k steps, warm, scoped, 2 threads | 2397 (2395-2400) | 2398, 2397 | 0.0% |
| 0k steps, cold (20 ms idle), scoped, 2 threads | 40.59 (38.91-40.73) | 39.68, 40.73 | 2.6% |
| 100k steps, cold (20 ms idle), scoped, 2 threads | 282.1 (279-283.3) | 280.5, 282.7 | 0.7% |
| 1000k steps, cold (20 ms idle), scoped, 2 threads | 2390 (2385-2398) | 2392, 2390 | 0.1% |
| 0k steps, warm, scoped, 4 threads | 94.51 (92.62-96.46) | 94.35, 94.69 | 0.4% |
| 100k steps, warm, scoped, 4 threads | 211.7 (207.7-213.2) | 212.2, 209.9 | 1.1% |
| 1000k steps, warm, scoped, 4 threads | 1277 (1269-1278) | 1278, 1273 | 0.4% |
| 0k steps, cold (20 ms idle), scoped, 4 threads | 63.55 (63.12-64.53) | 64.19, 63.18 | 1.6% |
| 100k steps, cold (20 ms idle), scoped, 4 threads | 182.8 (178.6-183.7) | 182.8, 181.2 | 0.9% |
| 1000k steps, cold (20 ms idle), scoped, 4 threads | 1259 (1258-1259) | 1259, 1258 | 0.0% |
| 0k steps, warm, pool, spin 0 µs, 1 thread | 0.08602 (0.08563-0.08749) | 0.08657, 0.08601 | 0.6% |
| 100k steps, warm, pool, spin 0 µs, 1 thread | 477.6 (476.6-484.4) | 481.2, 476.8 | 0.9% |
| 1000k steps, warm, pool, spin 0 µs, 1 thread | 4820 (4818-4832) | 4825, 4820 | 0.1% |
| 0k steps, cold (20 ms idle), pool, spin 0 µs, 1 thread | 0.0888 (0.0852-0.1) | 0.0943, 0.0871 | 8.1% |
| 100k steps, cold (20 ms idle), pool, spin 0 µs, 1 thread | 478.6 (475.4-480.1) | 476.8, 479.6 | 0.6% |
| 1000k steps, cold (20 ms idle), pool, spin 0 µs, 1 thread | 4817 (4812-4826) | 4822, 4814 | 0.2% |
| 0k steps, warm, pool, spin 0 µs, 2 threads | 0.5881 (0.5815-0.6027) | 0.5836, 0.5967 | 2.2% |
| 100k steps, warm, pool, spin 0 µs, 2 threads | 240 (239.4-240.3) | 239.8, 240.1 | 0.1% |
| 1000k steps, warm, pool, spin 0 µs, 2 threads | 2402 (2402-2403) | 2402, 2403 | 0.0% |
| 0k steps, cold (20 ms idle), pool, spin 0 µs, 2 threads | 1.042 (1.033-1.048) | 1.042, 1.041 | 0.2% |
| 100k steps, cold (20 ms idle), pool, spin 0 µs, 2 threads | 240.3 (239.2-244.1) | 240.1, 241.8 | 0.7% |
| 1000k steps, cold (20 ms idle), pool, spin 0 µs, 2 threads | 2406 (2398-2407) | 2402, 2406 | 0.2% |
| 0k steps, warm, pool, spin 0 µs, 4 threads | 1.391 (1.39-1.406) | 1.398, 1.391 | 0.5% |
| 100k steps, warm, pool, spin 0 µs, 4 threads | 125 (124.3-125.4) | 125.4, 124.5 | 0.7% |
| 1000k steps, warm, pool, spin 0 µs, 4 threads | 1199 (1197-1201) | 1201, 1197 | 0.3% |
| 0k steps, cold (20 ms idle), pool, spin 0 µs, 4 threads | 1.871 (1.829-1.893) | 1.852, 1.88 | 1.5% |
| 100k steps, cold (20 ms idle), pool, spin 0 µs, 4 threads | 124.1 (122.4-125.2) | 123.8, 124.1 | 0.2% |
| 1000k steps, cold (20 ms idle), pool, spin 0 µs, 4 threads | 1199 (1199-1200) | 1199, 1199 | 0.0% |
| 0k steps, warm, pool, spin 50 µs, 1 thread | 0.08818 (0.08579-0.0892) | 0.08737, 0.0883 | 1.1% |
| 100k steps, warm, pool, spin 50 µs, 1 thread | 477 (473.2-480.4) | 475.1, 478.7 | 0.8% |
| 1000k steps, warm, pool, spin 50 µs, 1 thread | 4822 (4817-4826) | 4821, 4822 | 0.0% |
| 0k steps, cold (20 ms idle), pool, spin 50 µs, 1 thread | 0.0908 (0.0886-0.0964) | 0.0926, 0.0907 | 2.1% |
| 100k steps, cold (20 ms idle), pool, spin 50 µs, 1 thread | 473.2 (471.5-480.8) | 472.2, 477.1 | 1.0% |
| 1000k steps, cold (20 ms idle), pool, spin 50 µs, 1 thread | 4815 (4815-4825) | 4820, 4815 | 0.1% |
| 0k steps, warm, pool, spin 50 µs, 2 threads | 0.3496 (0.3424-0.3544) | 0.3484, 0.3496 | 0.3% |
| 100k steps, warm, pool, spin 50 µs, 2 threads | 238.7 (238.6-238.9) | 238.7, 238.8 | 0.0% |
| 1000k steps, warm, pool, spin 50 µs, 2 threads | 2404 (2402-2404) | 2403, 2404 | 0.0% |
| 0k steps, cold (20 ms idle), pool, spin 50 µs, 2 threads | 1.041 (1.026-1.052) | 1.039, 1.041 | 0.2% |
| 100k steps, cold (20 ms idle), pool, spin 50 µs, 2 threads | 243.1 (240.7-244.1) | 244, 241.5 | 1.0% |
| 1000k steps, cold (20 ms idle), pool, spin 50 µs, 2 threads | 2403 (2398-2404) | 2403, 2401 | 0.1% |
| 0k steps, warm, pool, spin 50 µs, 4 threads | 0.9228 (0.9099-0.9358) | 0.9228, 0.9228 | 0.0% |
| 100k steps, warm, pool, spin 50 µs, 4 threads | 121.5 (121.5-121.7) | 121.6, 121.5 | 0.0% |
| 1000k steps, warm, pool, spin 50 µs, 4 threads | 1202 (1202-1205) | 1204, 1202 | 0.1% |
| 0k steps, cold (20 ms idle), pool, spin 50 µs, 4 threads | 1.889 (1.874-1.889) | 1.882, 1.889 | 0.4% |
| 100k steps, cold (20 ms idle), pool, spin 50 µs, 4 threads | 124.9 (122.1-126.6) | 123.5, 125.7 | 1.8% |
| 1000k steps, cold (20 ms idle), pool, spin 50 µs, 4 threads | 1199 (1197-1200) | 1200, 1198 | 0.2% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 43.55 (43-44.1) | 44.1, 43 | 2.5% |
