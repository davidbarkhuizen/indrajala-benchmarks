Old `b900778` against new `504a1f6`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `0a6910b` (extension sha256 `efb050f9ebfe`) and new crate `1f798b6` (extension sha256 `dd53acd61b7c`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (raspberry-pi-5.json); passes peaked at 57.9-60.0 C; max 1-min load 1.29 (measured just after this run's crate builds); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / conv 13x13x8, 8 ch downstream_batch b512 / rust -86.6% (5.421e+04 -> 7258 µs)
- consistent: per call / conv 28x28, 8 ch downstream_batch b512 / rust -81.4% (5.626e+04 -> 1.045e+04 µs)
- consistent: per call / conv 26x26x8, 8 ch downstream_batch b512 / rust -78.2% (2.563e+05 -> 5.587e+04 µs)
- consistent: per call / conv 26x26x8, 8 ch downstream_batch b32 / rust -72.5% (1.326e+04 -> 3641 µs)
- consistent: per call / conv 26x26x8/2, 8 ch downstream_batch b512 / rust -64.6% (7.156e+04 -> 2.534e+04 µs)
- consistent: per call / conv 28x28, 8 ch downstream_batch b32 / rust -48.8% (2909 -> 1489 µs)
- consistent: per call / pool 6x6, 8 ch downstream_batch b32 / rust -36.0% (12.3 -> 7.865 µs)
- consistent: per call / conv 13x13x8, 8 ch downstream_batch b32 / rust -23.8% (1335 -> 1018 µs)
- consistent: per call / pool 6x6, 8 ch downstream / rust -21.0% (0.8324 -> 0.6577 µs)
- consistent: per call / dense 10 x 30 downstream_batch b512 / rust +17.1% (46.57 -> 54.54 µs)
- ... 35 more consistent rows (report --md)
- 225 rows within noise (32 separated inside their spread), max |Δ| 406.5%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 79.41 (77.79-82.21) | 78.22 (77.82-79.47) | -1.5% | 81.38, 80.09, 77.87 / 78.88, 77.82, 78.47 | within noise |
| conv tail 32 x 5408 forward / rust | 58.31 (54.73-75.97) | 66.07 (55.98-76.76) | +13.3% | 67.7, 64.03, 56.1 / 66.37, 66.2, 65.68 | within noise |
| conv tail 32 x 5408 downstream / numpy | 91.94 (91.34-92.3) | 91.7 (91.51-92) | -0.3% | 91.63, 91.82, 92.06 / 91.7, 91.7, 91.78 | within noise |
| conv tail 32 x 5408 downstream / rust | 89.51 (75.11-92.17) | 83.74 (74.39-104.5) | -6.4% | 91.19, 83.86, 82.34 / 89.97, 83.19, 83.7 | within noise |
| conv tail 32 x 5408 hidden_delta / numpy | 104.4 (103.5-104.8) | 104.1 (103.4-105.6) | -0.3% | 104.6, 104.1, 104.3 / 104.1, 104.3, 104.5 | within noise |
| conv tail 32 x 5408 hidden_delta / rust | 94.65 (79.93-96.81) | 80.47 (78.98-98.54) | -15.0% | 94.66, 87.53, 95.48 / 80.47, 86.93, 88.76 | within noise |
| conv tail 32 x 5408 accumulate_gradient / numpy | 410 (280.1-962.6) | 403 (311.1-844.1) | -1.7% | 410, 310, 938.2 / 359.7, 620.9, 399.8 | within noise |
| conv tail 32 x 5408 accumulate_gradient / rust | 97.47 (90.44-100.9) | 95.23 (89.03-100.4) | -2.3% | 95.28, 94.38, 98.94 / 93.9, 94.63, 96.05 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 1583 (1366-2000) | 1647 (1471-1874) | +4.0% | 1892, 1466, 1569 / 1647, 1481, 1829 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 470.3 (377.6-814.4) | 451.4 (376.1-626.4) | -4.0% | 664.3, 529.5, 396.3 / 571.2, 446.6, 383.1 | within noise |
| conv tail 32 x 5408 sgd step / numpy | 2578 (2178-3349) | 2566 (2121-3387) | -0.5% | 2598, 2319, 3022 / 2208, 3194, 2555 | within noise |
| conv tail 32 x 5408 sgd step / rust | 120.5 (115.6-287.3) | 122 (119.4-279.2) | +1.3% | 121.4, 204.2, 116 / 196, 199.6, 121 | within noise |
| conv tail 32 x 5408 forward_batch b32 / numpy | 519 (503.6-562.6) | 527.9 (523.4-535.2) | +1.7% | 538.2, 515, 515.7 / 535.2, 525.8, 526.6 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 1120 (1092-1138) | 1118 (1094-1128) | -0.2% | 1120, 1120, 1115 / 1126, 1101, 1119 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1.812e+04 (1.652e+04-1.893e+04) | 1.783e+04 (1.597e+04-2.113e+04) | -1.5% | 1.839e+04, 1.772e+04, 1.782e+04 / 1.849e+04, 1.92e+04, 1.665e+04 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1.118e+04 (1.031e+04-1.382e+04) | 1.126e+04 (1.065e+04-1.3e+04) | +0.7% | 1.207e+04, 1.056e+04, 1.269e+04 / 1.103e+04, 1.231e+04, 1.097e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 1476 (1124-1675) | 1250 (1075-1684) | -15.3% | 1494, 1514, 1312 / 1153, 1522, 1176 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 1487 (1177-1623) | 1215 (1134-1449) | -18.3% | 1419, 1561, 1326 / 1215, 1276, 1292 | separated, inside spread |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3.179e+04 (3.068e+04-4.217e+04) | 3.128e+04 (3.002e+04-3.843e+04) | -1.6% | 3.179e+04, 3.068e+04, 4.073e+04 / 3.058e+04, 3.429e+04, 3.493e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2.221e+04 (1.659e+04-2.682e+04) | 2.124e+04 (1.139e+04-2.486e+04) | -4.3% | 2.412e+04, 2.017e+04, 2.221e+04 / 1.751e+04, 1.812e+04, 2.235e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 3210 (2796-3641) | 3479 (3038-4094) | +8.4% | 3368, 3060, 3332 / 3755, 3274, 3479 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 1873 (1602-2116) | 1810 (1577-2139) | -3.4% | 1806, 1939, 1857 / 2011, 1859, 1645 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 6.822e+04 (6.381e+04-8.148e+04) | 6.645e+04 (6.438e+04-8.162e+04) | -2.6% | 6.832e+04, 6.747e+04, 7.282e+04 / 6.633e+04, 6.787e+04, 7.305e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 3.182e+04 (2.826e+04-3.48e+04) | 3.011e+04 (2.608e+04-3.427e+04) | -5.4% | 2.92e+04, 3.191e+04, 3.388e+04 / 2.911e+04, 3.011e+04, 3.121e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 2098 (1496-2256) | 1866 (1556-2376) | -11.1% | 2012, 1876, 2098 / 2222, 1660, 1773 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 2184 (2118-2375) | 2194 (2095-2357) | +0.5% | 2138, 2239, 2256 / 2227, 2134, 2286 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 2.582e+04 (2.262e+04-2.794e+04) | 2.74e+04 (2.133e+04-2.834e+04) | +6.1% | 2.64e+04, 2.515e+04, 2.528e+04 / 2.74e+04, 2.573e+04, 2.484e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 2.004e+04 (1.917e+04-2.038e+04) | 1.94e+04 (1.887e+04-2.054e+04) | -3.2% | 2.004e+04, 1.93e+04, 2.025e+04 / 1.919e+04, 2.043e+04, 1.918e+04 | within noise |
| dense 30 x 784 forward / numpy | 16.28 (16.15-16.4) | 16.33 (16.17-16.66) | +0.3% | 16.27, 16.26, 16.3 / 16.31, 16.5, 16.29 | within noise |
| dense 30 x 784 forward / rust | 6.523 (6.415-6.558) | 6.512 (6.451-6.521) | -0.2% | 6.525, 6.499, 6.469 / 6.483, 6.494, 6.518 | within noise |
| dense 30 x 784 downstream / numpy | 12.7 (12.65-12.75) | 12.71 (12.65-12.74) | +0.1% | 12.66, 12.74, 12.7 / 12.68, 12.72, 12.69 | within noise |
| dense 30 x 784 downstream / rust | 6.584 (6.277-6.687) | 6.602 (6.329-6.683) | +0.3% | 6.668, 6.597, 6.297 / 6.641, 6.63, 6.459 | within noise |
| dense 30 x 784 hidden_delta / numpy | 17.09 (17.01-17.13) | 17.1 (17.06-17.22) | +0.1% | 17.11, 17.07, 17.06 / 17.17, 17.1, 17.06 | within noise |
| dense 30 x 784 hidden_delta / rust | 7.514 (7.445-7.578) | 7.327 (7.153-7.57) | -2.5% | 7.482, 7.512, 7.548 / 7.348, 7.52, 7.18 | within noise |
| dense 30 x 784 accumulate_gradient / numpy | 42.74 (42.6-43.16) | 42.7 (42.61-42.89) | -0.1% | 42.67, 42.95, 42.8 / 42.75, 42.74, 42.7 | within noise |
| dense 30 x 784 accumulate_gradient / rust | 9.808 (9.59-9.823) | 9.867 (9.832-9.89) | +0.6% | 9.695, 9.82, 9.793 / 9.866, 9.882, 9.844 | separated, inside spread |
| dense 30 x 784 apply_accumulated_gradient / numpy | 61.16 (61.09-61.24) | 61.23 (61.03-61.51) | +0.1% | 61.13, 61.17, 61.18 / 61.5, 61.23, 61.08 | within noise |
| dense 30 x 784 apply_accumulated_gradient / rust | 36.38 (36.26-36.49) | 36.65 (36.52-36.94) | +0.7% | 36.32, 36.35, 36.43 / 36.56, 36.62, 36.85 | separated, inside spread |
| dense 30 x 784 sgd step / numpy | 108 (107.5-108.6) | 108 (107.8-108.4) | -0.0% | 108, 108, 108.1 / 108.1, 108.1, 108 | within noise |
| dense 30 x 784 sgd step / rust | 15.78 (15.62-15.82) | 15.73 (15.69-15.76) | -0.3% | 15.71, 15.8, 15.7 / 15.71, 15.72, 15.73 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 92.18 (91.29-454.5) | 455.7 (91.28-463.2) | +394.3% | 91.93, 91.7, 273.4 / 456.3, 273.9, 459 | separated, inside spread |
| dense 30 x 784 forward_batch b32 / rust | 116.6 (115.3-118.9) | 115.8 (115.2-119) | -0.6% | 115.4, 116.9, 118.2 / 117.1, 115.5, 117.4 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 2729 (2361-2809) | 2587 (2291-2945) | -5.2% | 2574, 2729, 2697 / 2767, 2527, 2507 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 1081 (1003-1090) | 1056 (1002-1083) | -2.3% | 1087, 1041, 1065 / 1047, 1036, 1056 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 228.8 (56.68-400.3) | 58.48 (56.8-394.4) | -74.4% | 57.22, 229, 399.7 / 225.6, 58.41, 220.5 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 125.8 (125.6-126.9) | 126.1 (125.7-128.1) | +0.3% | 125.7, 126.3, 125.8 / 125.9, 127.2, 126.8 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 3609 (2418-4240) | 3656 (2938-4247) | +1.3% | 2792, 4167, 3609 / 3291, 3592, 4034 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 2079 (1666-2487) | 2121 (1727-2525) | +2.0% | 2337, 1871, 1930 / 2513, 2114, 1735 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 105.4 (104.4-299.4) | 105.4 (104.3-156.2) | -0.0% | 203.6, 105.4, 104.5 / 105.4, 132.1, 104.6 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / rust | 181 (146.8-306.4) | 176.7 (152.7-311.2) | -2.4% | 180, 304.5, 149.8 / 232.5, 176.1, 230 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 9151 (8166-1.06e+04) | 9289 (8228-1.199e+04) | +1.5% | 8735, 9370, 9568 / 9904, 1.037e+04, 8581 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / rust | 3248 (2886-3777) | 3180 (2597-3931) | -2.1% | 3432, 2931, 3478 / 3180, 3150, 3394 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 87.69 (85.83-442.7) | 444.1 (87.23-459.4) | +406.5% | 86.47, 265.3, 87.95 / 266, 273.3, 446 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 139.4 (139.1-139.6) | 140.3 (139.4-141) | +0.6% | 139.3, 139.4, 139.3 / 140.1, 139.6, 141 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 2192 (1958-2231) | 1965 (1876-2088) | -10.4% | 2063, 2224, 2188 / 1985, 2039, 1889 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 2481 (2287-2724) | 2627 (2322-5855) | +5.9% | 2539, 2442, 2481 / 4338, 2503, 2475 | within noise |
| dense 10 x 30 forward / numpy | 8.129 (8.109-8.173) | 8.122 (8.093-8.509) | -0.1% | 8.119, 8.157, 8.121 / 8.301, 8.124, 8.122 | within noise |
| dense 10 x 30 forward / rust | 0.6245 (0.6222-0.665) | 0.6304 (0.626-0.6391) | +0.9% | 0.6223, 0.6563, 0.6245 / 0.6303, 0.6315, 0.6326 | within noise |
| dense 10 x 30 downstream / numpy | 1.822 (1.8-1.839) | 1.825 (1.799-1.845) | +0.2% | 1.807, 1.834, 1.819 / 1.819, 1.827, 1.825 | within noise |
| dense 10 x 30 downstream / rust | 0.3841 (0.3778-0.3856) | 0.4025 (0.3913-0.4085) | +4.8% | 0.3816, 0.3832, 0.3853 / 0.4025, 0.3981, 0.4038 | consistent |
| dense 10 x 30 hidden_delta / numpy | 4.549 (4.505-4.659) | 4.513 (4.493-4.538) | -0.8% | 4.529, 4.564, 4.582 / 4.516, 4.508, 4.52 | separated, inside spread |
| dense 10 x 30 hidden_delta / rust | 0.8035 (0.7955-0.8489) | 0.8162 (0.8092-0.8405) | +1.6% | 0.8345, 0.8022, 0.7989 / 0.8299, 0.8151, 0.8124 | within noise |
| dense 10 x 30 accumulate_gradient / numpy | 5.28 (5.249-5.434) | 5.287 (5.246-5.454) | +0.1% | 5.254, 5.417, 5.28 / 5.28, 5.367, 5.35 | within noise |
| dense 10 x 30 accumulate_gradient / rust | 0.7869 (0.7754-0.7959) | 0.7895 (0.7735-0.7973) | +0.3% | 0.7826, 0.7857, 0.7909 / 0.7895, 0.7854, 0.7895 | within noise |
| dense 10 x 30 apply_accumulated_gradient / numpy | 8.885 (8.873-9.103) | 8.948 (8.903-9.151) | +0.7% | 8.875, 8.998, 8.957 / 8.984, 8.926, 9.03 | within noise |
| dense 10 x 30 apply_accumulated_gradient / rust | 4.064 (4.046-4.081) | 4.183 (4.148-4.206) | +2.9% | 4.053, 4.065, 4.074 / 4.169, 4.196, 4.166 | consistent |
| dense 10 x 30 sgd step / numpy | 15.02 (14.93-15.36) | 15.04 (14.9-15.07) | +0.1% | 15.16, 14.97, 15.06 / 14.98, 15.01, 15.04 | within noise |
| dense 10 x 30 sgd step / rust | 0.9212 (0.9158-0.9337) | 0.9284 (0.92-0.9411) | +0.8% | 0.92, 0.9273, 0.9194 / 0.9362, 0.9247, 0.9251 | within noise |
| dense 10 x 30 forward_batch b32 / numpy | 19.44 (19.32-19.63) | 19.47 (19.28-19.55) | +0.2% | 19.4, 19.52, 19.44 / 19.47, 19.39, 19.49 | within noise |
| dense 10 x 30 forward_batch b32 / rust | 7.296 (7.292-7.3) | 7.312 (7.3-7.472) | +0.2% | 7.296, 7.296, 7.297 / 7.386, 7.312, 7.312 | separated, inside spread |
| dense 10 x 30 forward_batch b512 / numpy | 151.6 (151.1-151.9) | 151.7 (151.3-152.2) | +0.0% | 151.5, 151.7, 151.6 / 151.5, 151.9, 151.6 | within noise |
| dense 10 x 30 forward_batch b512 / rust | 107.7 (107.6-107.9) | 107.9 (107.8-108.1) | +0.3% | 107.6, 107.7, 107.7 / 107.9, 108, 107.9 | consistent, small |
| dense 10 x 30 downstream_batch b32 / numpy | 5.947 (5.921-5.976) | 5.927 (5.887-5.969) | -0.3% | 5.939, 5.971, 5.933 / 5.936, 5.944, 5.901 | within noise |
| dense 10 x 30 downstream_batch b32 / rust | 3.25 (3.242-3.266) | 3.745 (3.74-3.754) | +15.2% | 3.259, 3.245, 3.247 / 3.742, 3.75, 3.748 | consistent |
| dense 10 x 30 downstream_batch b512 / numpy | 64.72 (64.56-64.97) | 64.61 (64.36-64.85) | -0.2% | 64.84, 64.73, 64.64 / 64.75, 64.44, 64.65 | within noise |
| dense 10 x 30 downstream_batch b512 / rust | 46.57 (46.1-46.8) | 54.54 (54.25-54.82) | +17.1% | 46.62, 46.29, 46.71 / 54.54, 54.53, 54.54 | consistent |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 10.48 (10.42-10.52) | 10.49 (10.42-10.63) | +0.1% | 10.49, 10.48, 10.47 / 10.42, 10.57, 10.49 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 4.128 (4.123-4.15) | 4.629 (4.605-4.641) | +12.1% | 4.139, 4.128, 4.132 / 4.618, 4.626, 4.64 | consistent |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 93.32 (92.42-94.04) | 93.38 (92.38-113.2) | +0.1% | 92.77, 93.78, 93.24 / 94.11, 93.19, 102.8 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / rust | 55.45 (55.14-56.04) | 63.28 (63.07-64.22) | +14.1% | 55.58, 55.3, 55.73 / 63.15, 64.04, 63.27 | consistent |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 9.616 (9.521-9.682) | 9.601 (9.589-9.763) | -0.2% | 9.587, 9.598, 9.644 / 9.683, 9.594, 9.633 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 4.227 (4.189-4.243) | 4.58 (4.56-4.621) | +8.3% | 4.234, 4.207, 4.232 / 4.574, 4.58, 4.59 | consistent |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 47.84 (47.58-48.44) | 47.92 (47.41-48.12) | +0.2% | 47.71, 47.81, 48.14 / 47.72, 48.01, 47.87 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 58.5 (58.48-58.65) | 58.92 (58.67-58.98) | +0.7% | 58.48, 58.56, 58.59 / 58.93, 58.94, 58.8 | consistent, small |
| conv 28x28, 8 ch forward / numpy | 85.02 (84.74-86.02) | 85.7 (84.69-97.6) | +0.8% | 85.62, 85.08, 84.83 / 91.68, 85.16, 85.69 | within noise |
| conv 28x28, 8 ch forward / rust | 46.29 (46.27-46.36) | 52.23 (52.2-52.27) | +12.8% | 46.27, 46.29, 46.32 / 52.23, 52.24, 52.24 | consistent |
| conv 28x28, 8 ch downstream / numpy | 71.18 (70.58-72.09) | 71.18 (70.8-71.85) | +0.0% | 71.19, 70.72, 71.64 / 71.08, 71.2, 71.37 | within noise |
| conv 28x28, 8 ch downstream / rust | 43.17 (43.04-43.44) | 48.32 (48.28-48.37) | +11.9% | 43.11, 43.3, 43.21 / 48.32, 48.35, 48.29 | consistent |
| conv 28x28, 8 ch accumulate_gradient / numpy | 59.04 (57.69-60.23) | 60.33 (57.81-61.91) | +2.2% | 60.22, 59, 57.77 / 59.14, 61.09, 59.14 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 32.22 (32.19-32.23) | 32.38 (32.37-32.41) | +0.5% | 32.23, 32.22, 32.2 / 32.37, 32.37, 32.39 | consistent, small |
| conv 28x28, 8 ch forward_batch b32 / numpy | 4480 (3736-4927) | 4489 (4051-5602) | +0.2% | 4702, 4691, 3903 / 4827, 4513, 4374 | within noise |
| conv 28x28, 8 ch forward_batch b32 / rust | 1768 (1571-2027) | 1909 (1740-2360) | +7.9% | 2009, 1768, 1586 / 1967, 2072, 1887 | within noise |
| conv 28x28, 8 ch forward_batch b512 / numpy | 6.987e+04 (6.819e+04-9.183e+04) | 7.096e+04 (6.977e+04-7.275e+04) | +1.6% | 8.075e+04, 6.844e+04, 7.132e+04 / 7.174e+04, 7.131e+04, 6.998e+04 | within noise |
| conv 28x28, 8 ch forward_batch b512 / rust | 3.478e+04 (3.313e+04-3.656e+04) | 3.673e+04 (3.421e+04-4.134e+04) | +5.6% | 3.489e+04, 3.532e+04, 3.43e+04 / 3.547e+04, 3.967e+04, 3.653e+04 | separated, inside spread |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 1587 (1498-1881) | 1580 (1465-2067) | -0.5% | 1881, 1587, 1506 / 1848, 1723, 1499 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / rust | 2909 (2395-3430) | 1489 (1488-1491) | -48.8% | 2912, 2622, 3109 / 1490, 1489, 1489 | consistent |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 5.33e+04 (5.089e+04-5.783e+04) | 5.879e+04 (5.222e+04-6.129e+04) | +10.3% | 5.476e+04, 5.486e+04, 5.262e+04 / 5.989e+04, 5.566e+04, 5.622e+04 | separated, inside spread |
| conv 28x28, 8 ch downstream_batch b512 / rust | 5.626e+04 (5.205e+04-5.937e+04) | 1.045e+04 (9556-1.207e+04) | -81.4% | 5.297e+04, 5.826e+04, 5.699e+04 / 1.063e+04, 1.002e+04, 1.096e+04 | consistent |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 2259 (2247-2322) | 2253 (2241-2552) | -0.3% | 2259, 2285, 2284 / 2246, 2404, 2281 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 1251 (1201-1604) | 1207 (1194-1247) | -3.5% | 1225, 1428, 1238 / 1204, 1221, 1216 | separated, inside spread |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 3.766e+04 (3.722e+04-3.816e+04) | 3.721e+04 (3.717e+04-3.821e+04) | -1.2% | 3.766e+04, 3.725e+04, 3.816e+04 / 3.772e+04, 3.718e+04, 3.721e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 2.964e+04 (2.816e+04-3.782e+04) | 3.213e+04 (2.937e+04-3.431e+04) | +8.4% | 3.426e+04, 2.826e+04, 2.964e+04 / 3.302e+04, 3.095e+04, 3.177e+04 | within noise |
| conv 8x8, 8 ch forward / numpy | 34.73 (34.15-34.94) | 34.88 (34.75-35.9) | +0.4% | 34.37, 34.58, 34.91 / 34.84, 35.04, 35.33 | within noise |
| conv 8x8, 8 ch forward / rust | 3.385 (3.371-3.489) | 3.709 (3.68-3.84) | +9.6% | 3.383, 3.432, 3.385 / 3.699, 3.716, 3.76 | consistent |
| conv 8x8, 8 ch downstream / numpy | 39.86 (39.49-41.14) | 39.6 (39.52-39.88) | -0.6% | 40.29, 39.75, 40.38 / 39.52, 39.75, 39.71 | within noise |
| conv 8x8, 8 ch downstream / rust | 2.82 (2.813-2.826) | 3.171 (3.166-3.235) | +12.5% | 2.82, 2.823, 2.816 / 3.168, 3.17, 3.205 | consistent |
| conv 8x8, 8 ch accumulate_gradient / numpy | 12.53 (12.48-12.96) | 12.47 (12.37-13.06) | -0.5% | 12.5, 12.63, 12.76 / 12.43, 12.82, 12.4 | within noise |
| conv 8x8, 8 ch accumulate_gradient / rust | 2.459 (2.457-2.469) | 2.483 (2.477-2.492) | +0.9% | 2.459, 2.467, 2.458 / 2.485, 2.483, 2.481 | consistent, small |
| conv 8x8, 8 ch forward_batch b32 / numpy | 128.8 (127.8-131) | 129.8 (128.2-131.8) | +0.7% | 129.5, 128.8, 129.4 / 130.1, 129.2, 130.6 | within noise |
| conv 8x8, 8 ch forward_batch b32 / rust | 79.75 (79.27-79.79) | 89.54 (89.38-89.7) | +12.3% | 79.75, 79.67, 79.53 / 89.51, 89.51, 89.58 | consistent |
| conv 8x8, 8 ch forward_batch b512 / numpy | 4146 (3370-4871) | 3626 (3370-6028) | -12.6% | 4146, 4812, 3654 / 4772, 3488, 3865 | within noise |
| conv 8x8, 8 ch forward_batch b512 / rust | 1704 (1450-1872) | 1827 (1596-2071) | +7.2% | 1704, 1567, 1799 / 1798, 1834, 1858 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 116.1 (115.2-117.4) | 116.2 (115.8-117.6) | +0.1% | 116.1, 116.4, 116 / 116.5, 116.9, 116 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / rust | 74.81 (74.29-75.09) | 84 (83.66-84.45) | +12.3% | 74.85, 74.63, 74.87 / 84.18, 83.93, 83.94 | consistent |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 1619 (1602-2022) | 1644 (1583-2024) | +1.6% | 1754, 1610, 1821 / 1605, 1815, 1787 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / rust | 2008 (1613-2962) | 1339 (1334-1349) | -33.3% | 2021, 2507, 1737 / 1335, 1342, 1344 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 151.3 (148.6-153.6) | 148.4 (148.1-153.6) | -1.9% | 151, 151, 151.4 / 148.3, 150.8, 148.8 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 55.39 (55.34-55.49) | 55.73 (55.66-55.8) | +0.6% | 55.39, 55.39, 55.41 / 55.74, 55.69, 55.76 | consistent, small |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 2326 (2299-2417) | 2295 (2286-2399) | -1.3% | 2305, 2356, 2378 / 2292, 2305, 2347 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 1014 (1010-1319) | 1035 (1017-1342) | +2.1% | 1165, 1162, 1013 / 1026, 1325, 1033 | within noise |
| conv 13x13x8, 8 ch forward / numpy | 79.84 (79.08-80.65) | 79.41 (79.07-80.15) | -0.5% | 80.29, 80.04, 79.24 / 79.19, 79.55, 79.69 | within noise |
| conv 13x13x8, 8 ch forward / rust | 47.74 (47.64-48.4) | 52.05 (52-52.26) | +9.0% | 47.66, 48.04, 47.8 / 52, 52.05, 52.24 | consistent |
| conv 13x13x8, 8 ch downstream / numpy | 89.15 (88.55-90.28) | 89.77 (88.89-93.04) | +0.7% | 89.61, 88.72, 89.81 / 91.33, 89.41, 89.78 | within noise |
| conv 13x13x8, 8 ch downstream / rust | 33.05 (32.89-33.25) | 33.39 (33.16-33.45) | +1.0% | 33.05, 33.05, 33.07 / 33.41, 33.32, 33.29 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 40.48 (40.3-41.18) | 40.27 (40.15-40.65) | -0.5% | 40.42, 41.06, 40.41 / 40.54, 40.21, 40.21 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 15.3 (15.29-15.37) | 16.4 (16.37-16.45) | +7.2% | 15.34, 15.3, 15.29 / 16.39, 16.38, 16.43 | consistent |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 2577 (2286-2789) | 2472 (2316-2673) | -4.1% | 2538, 2558, 2596 / 2472, 2420, 2535 | separated, inside spread |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 2242 (1972-2518) | 2372 (2169-2498) | +5.8% | 2207, 2443, 2105 / 2269, 2328, 2439 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 4.975e+04 (4.78e+04-5.203e+04) | 5.049e+04 (4.927e+04-5.264e+04) | +1.5% | 5.203e+04, 4.895e+04, 4.882e+04 / 5.052e+04, 5.008e+04, 5.136e+04 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 4.922e+04 (4.897e+04-5.047e+04) | 5.313e+04 (5.033e+04-5.646e+04) | +7.9% | 4.952e+04, 4.922e+04, 4.978e+04 / 5.158e+04, 5.502e+04, 5.265e+04 | separated, inside spread |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 4028 (3890-4495) | 4062 (3882-4412) | +0.8% | 4271, 4095, 4001 / 3940, 4138, 4269 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 1335 (1291-1360) | 1018 (1010-1018) | -23.8% | 1313, 1326, 1346 / 1016, 1018, 1014 | consistent |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 1.141e+05 (1.08e+05-1.237e+05) | 1.167e+05 (1.098e+05-1.175e+05) | +2.3% | 1.211e+05, 1.141e+05, 1.094e+05 / 1.149e+05, 1.137e+05, 1.167e+05 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 5.421e+04 (5.02e+04-5.908e+04) | 7258 (6598-7836) | -86.6% | 5.839e+04, 5.211e+04, 5.371e+04 / 6915, 7120, 7560 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 1138 (1123-1144) | 1139 (1123-1145) | +0.1% | 1135, 1138, 1134 / 1142, 1129, 1142 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 619.1 (609.6-621.3) | 642.2 (639.8-649.7) | +3.7% | 615.1, 617.4, 619.2 / 645, 644.1, 640.4 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.846e+04 (1.836e+04-1.87e+04) | 1.841e+04 (1.826e+04-1.848e+04) | -0.3% | 1.841e+04, 1.866e+04, 1.844e+04 / 1.842e+04, 1.837e+04, 1.837e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 1.311e+04 (1.118e+04-1.378e+04) | 1.314e+04 (1.165e+04-1.402e+04) | +0.2% | 1.354e+04, 1.222e+04, 1.225e+04 / 1.187e+04, 1.39e+04, 1.314e+04 | within noise |
| conv 26x26x8/2, 8 ch forward / numpy | 90.18 (89.73-90.26) | 90.23 (89.19-90.59) | +0.0% | 90, 90.22, 90.07 / 89.51, 90.23, 90.44 | within noise |
| conv 26x26x8/2, 8 ch forward / rust | 56.55 (56.5-56.9) | 61.88 (61.69-62.1) | +9.4% | 56.85, 56.51, 56.55 / 61.88, 61.9, 61.88 | consistent |
| conv 26x26x8/2, 8 ch downstream / numpy | 103.6 (102.9-104.8) | 103.4 (102.6-104.7) | -0.2% | 103.7, 103.8, 103.4 / 103.9, 103.7, 102.9 | within noise |
| conv 26x26x8/2, 8 ch downstream / rust | 39.64 (39.33-40.08) | 39.62 (39.53-40.19) | -0.1% | 39.7, 39.71, 39.64 / 39.91, 39.58, 39.59 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 47.73 (46.83-47.95) | 47.64 (47.28-48.39) | -0.2% | 47.86, 47.08, 47.81 / 48.09, 47.38, 47.69 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 18.03 (18-18.09) | 19.37 (19.34-19.53) | +7.4% | 18.06, 18.01, 18.05 / 19.35, 19.37, 19.46 | consistent |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 3413 (3251-3805) | 3473 (3286-3806) | +1.8% | 3285, 3435, 3660 / 3300, 3676, 3499 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 2783 (2607-2806) | 3128 (2742-3374) | +12.4% | 2788, 2695, 2750 / 2888, 3061, 3306 | separated, inside spread |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 6.338e+04 (6.253e+04-6.537e+04) | 6.446e+04 (6.24e+04-6.627e+04) | +1.7% | 6.482e+04, 6.256e+04, 6.338e+04 / 6.446e+04, 6.286e+04, 6.556e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 6.076e+04 (5.745e+04-6.308e+04) | 6.323e+04 (5.931e+04-6.605e+04) | +4.1% | 6.122e+04, 6.075e+04, 5.987e+04 / 6.567e+04, 6.024e+04, 6.254e+04 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 8614 (8128-1.33e+04) | 8818 (7617-9076) | +2.4% | 8674, 8462, 1.099e+04 / 8290, 8628, 9019 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 3173 (2586-5124) | 1246 (1230-1250) | -60.7% | 2596, 3166, 4457 / 1245, 1239, 1246 | separated, inside spread |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 1.802e+05 (1.711e+05-1.94e+05) | 1.835e+05 (1.77e+05-1.897e+05) | +1.9% | 1.866e+05, 1.841e+05, 1.747e+05 / 1.84e+05, 1.798e+05, 1.871e+05 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 7.156e+04 (6.745e+04-7.458e+04) | 2.534e+04 (2.022e+04-2.861e+04) | -64.6% | 7.246e+04, 7.011e+04, 7.194e+04 / 2.441e+04, 2.579e+04, 2.374e+04 | consistent |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 1391 (1373-1412) | 1407 (1383-1417) | +1.1% | 1382, 1396, 1400 / 1414, 1395, 1404 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 696.1 (668.3-799.2) | 831.8 (776.1-841.6) | +19.5% | 749.5, 682.7, 690.8 / 776.2, 838.5, 831.8 | separated, inside spread |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 2.235e+04 (2.213e+04-2.259e+04) | 2.246e+04 (2.219e+04-2.28e+04) | +0.5% | 2.249e+04, 2.233e+04, 2.222e+04 / 2.274e+04, 2.232e+04, 2.232e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 1.485e+04 (1.346e+04-2.302e+04) | 1.626e+04 (1.526e+04-1.813e+04) | +9.5% | 1.867e+04, 1.485e+04, 1.503e+04 / 1.635e+04, 1.537e+04, 1.716e+04 | within noise |
| conv 26x26x8, 8 ch forward / numpy | 245.4 (244.2-404.8) | 244.9 (244-246.3) | -0.2% | 245.1, 244.8, 326.1 / 245.3, 245.2, 244.7 | within noise |
| conv 26x26x8, 8 ch forward / rust | 219.6 (219.3-221.2) | 240.8 (240.5-245) | +9.6% | 219.8, 220.4, 219.5 / 240.7, 242.8, 241.4 | consistent |
| conv 26x26x8, 8 ch downstream / numpy | 254.5 (253-257.8) | 254.9 (253.2-270.5) | +0.1% | 254.5, 257.7, 253.2 / 254, 262.7, 254.7 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 153.7 (152.3-154.3) | 153 (152.9-153.9) | -0.4% | 154, 153, 153.3 / 153.4, 152.9, 153.5 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 159.7 (158.9-160.7) | 161.1 (157.3-162.7) | +0.9% | 159.5, 160.1, 159.7 / 161.8, 161.2, 159.1 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 67.16 (67.05-67.45) | 72.35 (72.14-72.44) | +7.7% | 67.25, 67.22, 67.16 / 72.42, 72.35, 72.22 | consistent |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 1.315e+04 (1.262e+04-1.431e+04) | 1.406e+04 (1.353e+04-1.542e+04) | +6.9% | 1.275e+04, 1.315e+04, 1.421e+04 / 1.469e+04, 1.447e+04, 1.374e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 1.197e+04 (1.176e+04-1.313e+04) | 1.297e+04 (1.24e+04-1.383e+04) | +8.3% | 1.263e+04, 1.215e+04, 1.183e+04 / 1.312e+04, 1.317e+04, 1.288e+04 | separated, inside spread |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 2.431e+05 (2.32e+05-2.63e+05) | 2.49e+05 (2.419e+05-2.923e+05) | +2.4% | 2.478e+05, 2.431e+05, 2.418e+05 / 2.671e+05, 2.49e+05, 2.505e+05 | separated, inside spread |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 2.24e+05 (2.229e+05-2.294e+05) | 2.346e+05 (2.326e+05-2.444e+05) | +4.8% | 2.25e+05, 2.24e+05, 2.261e+05 / 2.333e+05, 2.348e+05, 2.398e+05 | consistent |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 2.479e+04 (2.371e+04-2.655e+04) | 2.598e+04 (2.437e+04-2.785e+04) | +4.8% | 2.403e+04, 2.616e+04, 2.479e+04 / 2.686e+04, 2.503e+04, 2.67e+04 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 1.326e+04 (1.241e+04-1.629e+04) | 3641 (3241-4904) | -72.5% | 1.513e+04, 1.326e+04, 1.249e+04 / 4109, 3272, 4085 | consistent |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 5.016e+05 (4.901e+05-5.262e+05) | 5.092e+05 (5.031e+05-5.242e+05) | +1.5% | 5.147e+05, 5e+05, 4.992e+05 / 5.155e+05, 5.072e+05, 5.116e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 2.563e+05 (2.494e+05-2.608e+05) | 5.587e+04 (4.965e+04-6.538e+04) | -78.2% | 2.589e+05, 2.547e+05, 2.551e+05 / 5.198e+04, 5.512e+04, 6.372e+04 | consistent |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 5625 (5610-5670) | 5650 (5620-5693) | +0.4% | 5640, 5624, 5634 / 5623, 5683, 5650 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 3365 (3174-3612) | 3380 (3245-4194) | +0.4% | 3315, 3292, 3527 / 3297, 3602, 3802 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 8.891e+04 (8.833e+04-8.955e+04) | 8.924e+04 (8.871e+04-9.046e+04) | +0.4% | 8.891e+04, 8.857e+04, 8.929e+04 / 8.975e+04, 8.883e+04, 8.959e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 5.684e+04 (4.858e+04-7.422e+04) | 5.838e+04 (5.7e+04-6.319e+04) | +2.7% | 6.668e+04, 5.404e+04, 5.156e+04 / 6.178e+04, 5.811e+04, 5.762e+04 | within noise |
| pool 26x26, 8 ch forward / numpy | 106 (105.4-106.4) | 105.9 (105-107.2) | -0.1% | 106, 105.7, 106.2 / 106.5, 105.2, 105.9 | within noise |
| pool 26x26, 8 ch forward / rust | 5.215 (5.205-5.22) | 5.22 (5.205-5.231) | +0.1% | 5.22, 5.212, 5.212 / 5.225, 5.225, 5.206 | within noise |
| pool 26x26, 8 ch downstream / numpy | 55.05 (54.99-55.55) | 55.4 (54.63-56.08) | +0.6% | 55.02, 55.31, 55.18 / 55.57, 54.73, 55.86 | within noise |
| pool 26x26, 8 ch downstream / rust | 4.3 (4.277-4.35) | 4.13 (4.121-4.137) | -4.0% | 4.31, 4.318, 4.287 / 4.13, 4.129, 4.129 | consistent |
| pool 26x26, 8 ch forward_batch b32 / numpy | 2460 (2383-3135) | 2420 (2403-3115) | -1.6% | 2480, 2776, 2413 / 2545, 2759, 2419 | within noise |
| pool 26x26, 8 ch forward_batch b32 / rust | 216.6 (202.6-245.2) | 207.8 (192.1-245) | -4.1% | 217, 216.6, 223.9 / 224.6, 200.8, 218.5 | within noise |
| pool 26x26, 8 ch forward_batch b512 / numpy | 4.104e+04 (3.994e+04-4.136e+04) | 4.102e+04 (3.883e+04-4.687e+04) | -0.1% | 4.065e+04, 4.107e+04, 4.058e+04 / 4.322e+04, 4.404e+04, 3.981e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 8728 (7981-1.084e+04) | 8664 (8068-9340) | -0.7% | 8390, 9053, 9409 / 9023, 8928, 8154 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 984.8 (952.2-1537) | 971.2 (940.5-1483) | -1.4% | 988.4, 969.3, 1260 / 1241, 962.5, 958.3 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / rust | 305.1 (134.4-492.9) | 478.2 (129.8-609.9) | +56.7% | 134.7, 310, 484 / 130.1, 548.6, 478.2 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 5.555e+04 (5.406e+04-6.018e+04) | 5.831e+04 (5.213e+04-6.342e+04) | +5.0% | 5.712e+04, 5.555e+04, 5.622e+04 / 5.501e+04, 6.107e+04, 5.812e+04 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / rust | 2.014e+04 (1.922e+04-2.157e+04) | 2.141e+04 (2.021e+04-2.272e+04) | +6.3% | 2.072e+04, 1.952e+04, 2.063e+04 / 2.149e+04, 2.044e+04, 2.217e+04 | within noise |
| pool 6x6, 8 ch forward / numpy | 39.69 (39.21-40) | 39.8 (39.44-41.4) | +0.3% | 39.61, 39.92, 39.41 / 40.46, 39.6, 39.95 | within noise |
| pool 6x6, 8 ch forward / rust | 0.766 (0.7608-0.7701) | 0.7661 (0.7635-0.7742) | +0.0% | 0.7672, 0.7679, 0.762 / 0.7645, 0.7669, 0.7704 | within noise |
| pool 6x6, 8 ch downstream / numpy | 32.62 (32.28-33.59) | 32.5 (32.26-32.61) | -0.4% | 32.47, 33.17, 32.49 / 32.44, 32.53, 32.5 | within noise |
| pool 6x6, 8 ch downstream / rust | 0.8324 (0.8039-0.8414) | 0.6577 (0.6512-0.6595) | -21.0% | 0.8121, 0.8329, 0.8404 / 0.6585, 0.6544, 0.6554 | consistent |
| pool 6x6, 8 ch forward_batch b32 / numpy | 168.6 (167.3-183.7) | 173.1 (168.6-292) | +2.7% | 169.2, 176.4, 168 / 173.1, 230.4, 175.8 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 10.54 (10.52-10.55) | 10.6 (10.56-10.63) | +0.6% | 10.55, 10.53, 10.53 / 10.6, 10.58, 10.62 | separated, inside spread |
| pool 6x6, 8 ch forward_batch b512 / numpy | 2218 (2188-2292) | 2223 (2174-2473) | +0.2% | 2239, 2241, 2199 / 2340, 2220, 2206 | within noise |
| pool 6x6, 8 ch forward_batch b512 / rust | 164.7 (164.5-168.8) | 169.3 (166.2-272.2) | +2.8% | 164.6, 166.8, 164.8 / 219.2, 168.9, 169.3 | separated, inside spread |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 85.13 (84.9-88.27) | 85.44 (85-86.41) | +0.4% | 85.29, 86.63, 85.04 / 85.81, 85.64, 85.44 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / rust | 12.3 (12.09-12.34) | 7.865 (7.835-7.893) | -36.0% | 12.31, 12.21, 12.22 / 7.877, 7.845, 7.865 | consistent |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 936.3 (929.9-942.2) | 940.2 (934-954.3) | +0.4% | 934.9, 939.8, 934.6 / 947.6, 936.8, 939.3 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 198.4 (196.5-423.9) | 129.2 (128.9-129.6) | -34.9% | 312.2, 196.8, 198.2 / 129.1, 129.3, 129.2 | separated, inside spread |
| conv tail 32 x 5408 bare downstream b32 / numpy | 1553 (1250-1666) | 1335 (1007-1687) | -14.0% | 1553, 1458, 1525 / 1347, 1348, 1335 | consistent |
| conv tail 32 x 5408 bare downstream b32 / rust | 1476 (1185-1626) | 1178 (1128-1666) | -20.2% | 1415, 1476, 1405 / 1199, 1147, 1397 | separated, inside spread |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3.34e+04 (2.348e+04-4.15e+04) | 3.271e+04 (2.757e+04-3.585e+04) | -2.0% | 2.782e+04, 3.821e+04, 3.114e+04 / 3.171e+04, 3.479e+04, 3.01e+04 | within noise |
| conv tail 32 x 5408 bare downstream b512 / rust | 2.553e+04 (1.93e+04-2.643e+04) | 2.25e+04 (1.368e+04-2.801e+04) | -11.9% | 2.31e+04, 2.247e+04, 2.563e+04 / 2.25e+04, 1.646e+04, 2.613e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 1154 (1078-1254) | 1398 (924.9-1538) | +21.2% | 1133, 1173, 1173 / 1473, 1094, 1458 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / rust | 1160 (1090-1236) | 1166 (1116-1229) | +0.6% | 1160, 1164, 1150 / 1205, 1155, 1150 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 2.743e+04 (2.552e+04-2.998e+04) | 2.629e+04 (2.365e+04-2.762e+04) | -4.2% | 2.757e+04, 2.671e+04, 2.827e+04 / 2.507e+04, 2.58e+04, 2.738e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / rust | 1.883e+04 (1.776e+04-1.964e+04) | 1.958e+04 (1.839e+04-3.62e+04) | +4.0% | 1.797e+04, 1.939e+04, 1.902e+04 / 2.741e+04, 1.853e+04, 2.492e+04 | within noise |
| conv tail 32 x 5408 transpose b32 / numpy | 1.464 (1.447-1.538) | 1.472 (1.463-1.486) | +0.6% | 1.506, 1.457, 1.455 / 1.464, 1.479, 1.479 | within noise |
| conv tail 32 x 5408 transpose b32 / rust | 1.879 (1.877-1.88) | 1.874 (1.867-1.881) | -0.2% | 1.879, 1.877, 1.88 / 1.871, 1.874, 1.878 | within noise |
| conv tail 32 x 5408 transpose b512 / numpy | 30.04 (29.57-30.08) | 30 (29.72-30.04) | -0.1% | 29.81, 30.03, 30.05 / 30, 30.04, 29.85 | within noise |
| conv tail 32 x 5408 transpose b512 / rust | 26.61 (26.52-26.96) | 26.63 (26.38-26.94) | +0.0% | 26.66, 26.61, 26.78 / 26.78, 26.53, 26.56 | within noise |
| conv tail 32 x 5408 add b32 / numpy | 353.3 (296-406.3) | 315.1 (291.6-417.4) | -10.8% | 389.3, 353.3, 299 / 307.6, 312.6, 366.8 | within noise |
| conv tail 32 x 5408 add b32 / rust | 310 (257.6-425.8) | 356 (272.8-408.1) | +14.9% | 347, 281.5, 359.4 / 317.6, 340.5, 363.3 | within noise |
| conv tail 32 x 5408 add b512 / numpy | 323.9 (304.4-426) | 406.5 (321.1-417.1) | +25.5% | 370.2, 319, 335 / 414.5, 364.2, 369.7 | within noise |
| conv tail 32 x 5408 add b512 / rust | 330.2 (253.2-433.1) | 407 (333.5-428.3) | +23.3% | 293.4, 380, 315.1 / 419, 411.9, 333.7 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 2.829 (2.816-2.874) | 2.825 (2.807-2.906) | -0.1% | 2.825, 2.825, 2.849 / 2.837, 2.818, 2.856 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.7739 (0.7702-0.7759) | 0.7781 (0.777-0.7943) | +0.5% | 0.7739, 0.7731, 0.7739 / 0.7777, 0.786, 0.7786 | separated, inside spread |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 15.93 (15.81-16.31) | 16.09 (15.72-16.26) | +1.0% | 16.04, 16.06, 15.86 / 15.95, 16.24, 15.95 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 8.614 (8.592-8.668) | 8.685 (8.676-8.688) | +0.8% | 8.634, 8.614, 8.619 / 8.678, 8.686, 8.686 | consistent, small |
| dense 30 x 784 bare downstream b32 / numpy | 58.01 (56.73-58.69) | 58.11 (57.18-58.4) | +0.2% | 57.81, 57.38, 58.08 / 58.19, 58, 57.79 | within noise |
| dense 30 x 784 bare downstream b32 / rust | 126.8 (125.5-127.8) | 127.7 (125.8-127.9) | +0.7% | 126.6, 126.5, 127.3 / 126.8, 127.7, 127.3 | within noise |
| dense 30 x 784 bare downstream b512 / numpy | 3816 (2869-4141) | 4095 (2385-4197) | +7.3% | 3470, 3602, 3816 / 3239, 4150, 3909 | within noise |
| dense 30 x 784 bare downstream b512 / rust | 2105 (1599-2491) | 2405 (1585-2648) | +14.3% | 1967, 2322, 2045 / 1922, 2558, 2201 | within noise |
| dense 30 x 784 bare accumulate b32 / numpy | 66.33 (65.52-67.02) | 67.76 (66.45-399.9) | +2.2% | 66.71, 65.89, 66.12 / 233.3, 222.9, 67.38 | separated, inside spread |
| dense 30 x 784 bare accumulate b32 / rust | 126 (125.2-126.4) | 125.2 (124.8-155.7) | -0.6% | 125.8, 125.8, 126.2 / 125.7, 125.2, 140.3 | within noise |
| dense 30 x 784 bare accumulate b512 / numpy | 1985 (1827-2086) | 1889 (1627-2091) | -4.8% | 2018, 1884, 2027 / 1793, 1797, 2051 | within noise |
| dense 30 x 784 bare accumulate b512 / rust | 2675 (2335-2765) | 2535 (2232-2757) | -5.2% | 2695, 2744, 2478 / 2495, 2583, 2535 | within noise |
| dense 30 x 784 transpose b32 / numpy | 1.403 (1.392-1.63) | 1.405 (1.399-1.421) | +0.1% | 1.399, 1.41, 1.514 / 1.417, 1.401, 1.405 | within noise |
| dense 30 x 784 transpose b32 / rust | 1.821 (1.816-1.828) | 1.816 (1.809-1.82) | -0.3% | 1.823, 1.82, 1.823 / 1.815, 1.816, 1.815 | consistent, small |
| dense 30 x 784 transpose b512 / numpy | 8.992 (8.97-9.023) | 8.993 (8.946-9.013) | +0.0% | 9, 8.981, 9.004 / 8.957, 9.008, 8.993 | within noise |
| dense 30 x 784 transpose b512 / rust | 24.76 (24.73-24.96) | 24.99 (24.73-25.15) | +0.9% | 24.79, 24.84, 24.74 / 24.92, 24.82, 25.13 | within noise |
| dense 30 x 784 add b32 / numpy | 10.47 (10.26-11.4) | 10.38 (10.11-10.84) | -0.8% | 10.47, 10.83, 10.37 / 10.51, 10.35, 10.38 | within noise |
| dense 30 x 784 add b32 / rust | 9.847 (9.669-11.71) | 9.589 (9.339-11.07) | -2.6% | 10.39, 9.709, 10.78 / 9.785, 10.28, 9.348 | within noise |
| dense 30 x 784 add b512 / numpy | 11.58 (11.15-11.99) | 11.56 (11.17-11.73) | -0.2% | 11.47, 11.36, 11.79 / 11.45, 11.47, 11.61 | within noise |
| dense 30 x 784 add b512 / rust | 9.621 (9.42-9.671) | 9.66 (9.433-9.822) | +0.4% | 9.524, 9.593, 9.625 / 9.748, 9.549, 9.627 | within noise |
| dense 30 x 784 sum_axis0 b32 / numpy | 2.809 (2.791-2.853) | 2.827 (2.808-2.88) | +0.6% | 2.802, 2.826, 2.822 / 2.827, 2.822, 2.847 | within noise |
| dense 30 x 784 sum_axis0 b32 / rust | 0.7014 (0.6978-0.7079) | 0.7029 (0.7019-0.7058) | +0.2% | 0.7014, 0.7017, 0.7029 / 0.7039, 0.7024, 0.7045 | within noise |
| dense 30 x 784 sum_axis0 b512 / numpy | 15.42 (15.31-15.65) | 15.65 (15.3-16.06) | +1.4% | 15.42, 15.45, 15.52 / 15.47, 15.68, 15.84 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 7.45 (7.439-7.461) | 7.439 (7.428-7.448) | -0.2% | 7.45, 7.45, 7.45 / 7.434, 7.441, 7.439 | consistent, small |
| dense 10 x 30 bare downstream b32 / numpy | 5.895 (5.846-5.961) | 5.895 (5.857-7.692) | -0.0% | 5.92, 5.886, 5.884 / 5.877, 6.811, 5.877 | within noise |
| dense 10 x 30 bare downstream b32 / rust | 3.209 (3.206-3.218) | 3.703 (3.698-3.708) | +15.4% | 3.211, 3.213, 3.209 / 3.701, 3.701, 3.707 | consistent |
| dense 10 x 30 bare downstream b512 / numpy | 64.7 (64.62-65.54) | 64.68 (64.41-65.02) | -0.0% | 65.13, 64.65, 64.74 / 64.86, 64.53, 64.73 | within noise |
| dense 10 x 30 bare downstream b512 / rust | 46.58 (45.98-46.72) | 54.45 (54.19-54.74) | +16.9% | 46.29, 46.7, 46.3 / 54.45, 54.43, 54.6 | consistent |
| dense 10 x 30 bare accumulate b32 / numpy | 5.081 (5.039-5.11) | 5.049 (5.015-5.144) | -0.6% | 5.042, 5.091, 5.096 / 5.029, 5.099, 5.043 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 2.875 (2.871-2.879) | 3.254 (3.252-3.256) | +13.2% | 2.874, 2.876, 2.874 / 3.252, 3.254, 3.255 | consistent |
| dense 10 x 30 bare accumulate b512 / numpy | 32.65 (32.52-32.69) | 32.68 (32.48-32.78) | +0.1% | 32.59, 32.63, 32.68 / 32.67, 32.59, 32.7 | within noise |
| dense 10 x 30 bare accumulate b512 / rust | 45.07 (45.05-45.11) | 45.37 (45.34-45.41) | +0.7% | 45.1, 45.07, 45.05 / 45.37, 45.38, 45.37 | consistent, small |
| dense 10 x 30 transpose b32 / numpy | 0.8892 (0.885-0.8985) | 0.8932 (0.8911-0.9) | +0.4% | 0.8921, 0.8888, 0.8905 / 0.8918, 0.8999, 0.8927 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.7988 (0.7912-0.8044) | 0.7964 (0.7879-0.8024) | -0.3% | 0.7996, 0.7998, 0.7956 / 0.8005, 0.7931, 0.7926 | within noise |
| dense 10 x 30 transpose b512 / numpy | 3.401 (3.362-3.5) | 3.395 (3.366-3.409) | -0.2% | 3.4, 3.403, 3.431 / 3.385, 3.4, 3.382 | separated, inside spread |
| dense 10 x 30 transpose b512 / rust | 8.583 (8.569-8.603) | 8.579 (8.57-8.637) | -0.0% | 8.589, 8.592, 8.576 / 8.578, 8.611, 8.573 | within noise |
| dense 10 x 30 add b32 / numpy | 0.8996 (0.8887-0.9021) | 0.8998 (0.8876-0.9122) | +0.0% | 0.8976, 0.8953, 0.8996 / 0.9066, 0.8931, 0.8981 | within noise |
| dense 10 x 30 add b32 / rust | 0.3778 (0.3765-0.3983) | 0.3737 (0.3713-0.3779) | -1.1% | 0.3779, 0.3881, 0.3771 / 0.3724, 0.376, 0.3737 | separated, inside spread |
| dense 10 x 30 add b512 / numpy | 0.9173 (0.9134-0.9283) | 0.9141 (0.9069-0.9173) | -0.4% | 0.9165, 0.9205, 0.9214 / 0.9095, 0.9164, 0.9141 | separated, inside spread |
| dense 10 x 30 add b512 / rust | 0.4009 (0.3995-0.4033) | 0.3961 (0.3932-0.3992) | -1.2% | 0.402, 0.4005, 0.4009 / 0.3942, 0.3984, 0.3961 | separated, inside spread |
| dense 10 x 30 sum_axis0 b32 / numpy | 2.467 (2.441-2.504) | 2.456 (2.437-2.502) | -0.5% | 2.465, 2.45, 2.491 / 2.465, 2.476, 2.449 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.531 (0.5267-0.5345) | 0.532 (0.5285-0.5334) | +0.2% | 0.5328, 0.5288, 0.5302 / 0.5328, 0.5302, 0.532 | within noise |
| dense 10 x 30 sum_axis0 b512 / numpy | 12.61 (12.2-12.66) | 12.4 (12.15-12.68) | -1.7% | 12.61, 12.45, 12.4 / 12.4, 12.41, 12.41 | within noise |
| dense 10 x 30 sum_axis0 b512 / rust | 4.645 (4.64-4.653) | 4.648 (4.643-4.665) | +0.1% | 4.648, 4.645, 4.645 / 4.647, 4.645, 4.658 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 749.2 (745.4-759.7) | 749.1 (744.1-759) | -0.0% | 750, 752.5, 749.2 / 746.7, 752.4, 753.7 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 818.8 (817.1-820.8) | 822.4 (820.9-825) | +0.4% | 818.8, 820.2, 817.6 / 822.6, 823.9, 821.4 | separated, inside spread |
| attention 16 x 32 forward_batch b512 / numpy | 2.502e+04 (2.387e+04-2.694e+04) | 2.409e+04 (2.219e+04-2.831e+04) | -3.7% | 2.503e+04, 2.442e+04, 2.601e+04 / 2.409e+04, 2.436e+04, 2.525e+04 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 1.772e+04 (1.702e+04-1.939e+04) | 1.672e+04 (1.588e+04-2.145e+04) | -5.7% | 1.862e+04, 1.802e+04, 1.731e+04 / 1.866e+04, 1.672e+04, 1.713e+04 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 760.2 (754-1737) | 776.8 (761.6-781.4) | +2.2% | 755.5, 1250, 760.3 / 772.3, 771.2, 776.8 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / rust | 793.7 (789.7-798.1) | 795.2 (792.2-799.1) | +0.2% | 795.9, 791.3, 793.9 / 792.8, 797.2, 795.5 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 2.96e+04 (2.847e+04-3.242e+04) | 2.973e+04 (2.65e+04-3.214e+04) | +0.4% | 2.924e+04, 3.044e+04, 2.98e+04 / 3.15e+04, 2.708e+04, 2.973e+04 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / rust | 2.012e+04 (1.847e+04-2.209e+04) | 1.897e+04 (1.838e+04-2.196e+04) | -5.7% | 2.045e+04, 2.012e+04, 1.978e+04 / 1.932e+04, 1.871e+04, 2.043e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 590 (584.1-595.8) | 592 (580.9-2097) | +0.3% | 590.6, 589.7, 590 / 587.9, 589.5, 1346 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 509.3 (503.8-510.3) | 507.9 (504-515.9) | -0.3% | 507.7, 506.3, 510 / 507.1, 508.6, 509.9 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 4.327e+04 (3.343e+04-6.655e+04) | 4.062e+04 (3.247e+04-4.529e+04) | -6.1% | 3.932e+04, 5.57e+04, 4.052e+04 / 3.888e+04, 4.431e+04, 3.573e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 2.389e+04 (2.039e+04-3.771e+04) | 2.895e+04 (2.569e+04-3.464e+04) | +21.2% | 3.344e+04, 2.288e+04, 2.24e+04 / 2.895e+04, 2.934e+04, 3.016e+04 | within noise |
