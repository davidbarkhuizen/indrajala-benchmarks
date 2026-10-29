Old `6dcd34c` against new `6dcd34c`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `10dfec9` (extension sha256 `7d70efbe6dbd`) and new crate `4f230a4` (extension sha256 `403e794b8b56`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.15 (measured just after this run's crate builds); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / dense 30 x 784 bare downstream b32 / rust +34.6% (29.44 -> 39.62 µs)
- consistent: per call / dense 10 x 30 forward_batch b512 / rust -33.5% (58.27 -> 38.74 µs)
- consistent: per call / pool 6x6, 8 ch downstream_batch b32 / rust -32.5% (11.37 -> 7.671 µs)
- consistent: per call / pool 6x6, 8 ch downstream_batch b512 / rust -32.5% (178.9 -> 120.7 µs)
- consistent: per call / dense 10 x 30 forward_batch b32 / rust -31.3% (3.992 -> 2.744 µs)
- consistent: per call / dense 30 x 784 downstream_batch b32 / rust +28.8% (31.92 -> 41.1 µs)
- consistent: per call / conv tail 32 x 5408 bare accumulate b32 / rust +24.8% (240 -> 299.4 µs)
- consistent: per call / conv tail 32 x 5408 downstream_batch b32 / rust +23.4% (246.7 -> 304.4 µs)
- consistent: per call / dense 30 x 784 bare accumulate b32 / rust +22.9% (32.81 -> 40.31 µs)
- consistent: per call / dense 30 x 784 hidden_delta_batch b32 / rust +21.5% (42.21 -> 51.3 µs)
- ... 43 more consistent rows (report --md)
- 217 rows within noise (43 separated inside their spread), max |Δ| 11.3%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 27.95 (27.09-29.76) | 28.98 (27.35-29.91) | +3.7% | 28.53, 27.95, 28.37 / 28.97, 28.63, 29.19 | separated, inside spread |
| conv tail 32 x 5408 forward / rust | 19.96 (19.17-22.64) | 19.16 (18.98-20.62) | -4.0% | 19.92, 21.63, 19.24 / 19.89, 19.37, 19.01 | within noise |
| conv tail 32 x 5408 downstream / numpy | 24.04 (23.32-25.86) | 25.05 (23.4-25.87) | +4.2% | 24.63, 24.59, 24.04 / 25.11, 24.54, 25.13 | within noise |
| conv tail 32 x 5408 downstream / rust | 22.3 (22.04-23.67) | 21.51 (20.65-23.51) | -3.6% | 23.63, 22.14, 22.22 / 20.7, 22.75, 22.21 | within noise |
| conv tail 32 x 5408 hidden_delta / numpy | 31.95 (31.39-34.41) | 33.86 (31.37-33.96) | +6.0% | 33.45, 32.75, 31.4 / 33.91, 32.61, 33.25 | within noise |
| conv tail 32 x 5408 hidden_delta / rust | 24.27 (23.05-26.15) | 24.3 (23.2-25.73) | +0.1% | 25.37, 23.61, 23.73 / 23.78, 24.31, 24.47 | within noise |
| conv tail 32 x 5408 accumulate_gradient / numpy | 92.44 (88.39-94.7) | 90.32 (85.39-91.17) | -2.3% | 94.32, 92.44, 88.63 / 90.42, 88.45, 88.18 | within noise |
| conv tail 32 x 5408 accumulate_gradient / rust | 55.04 (53.68-55.87) | 54.77 (52.86-62.79) | -0.5% | 55.38, 54.18, 55.49 / 53.83, 54.44, 58.76 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 177.6 (177.1-184.3) | 180.6 (176.9-184.3) | +1.7% | 180.9, 181, 177.1 / 180.6, 182.5, 180.5 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 111.5 (106.7-112.5) | 110.5 (106.7-114.4) | -0.9% | 112.2, 110.7, 108.9 / 109.4, 110.6, 110.5 | within noise |
| conv tail 32 x 5408 sgd step / numpy | 263.7 (262.8-275.8) | 270.4 (263.8-277.3) | +2.5% | 269.5, 269.1, 263.6 / 267.2, 273.8, 270.4 | within noise |
| conv tail 32 x 5408 sgd step / rust | 59.55 (58.44-60.59) | 59.59 (57.72-60.88) | +0.1% | 60.35, 59.78, 58.6 / 59.03, 58.47, 60.42 | within noise |
| conv tail 32 x 5408 forward_batch b32 / numpy | 150.5 (145.4-157.4) | 147.1 (145.9-155.4) | -2.2% | 146.4, 152.2, 155.4 / 147.1, 148.1, 150.6 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 357.9 (351.6-378.4) | 353.3 (334.7-384.9) | -1.3% | 368.2, 358.8, 354.5 / 339.6, 371, 354.3 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1162 (1058-1168) | 1164 (1155-1169) | +0.2% | 1110, 1164, 1165 / 1163, 1161, 1165 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1859 (1713-1900) | 1813 (1795-1836) | -2.5% | 1782, 1893, 1859 / 1809, 1815, 1820 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 79.34 (78.6-80.43) | 79.34 (79.22-80.06) | -0.0% | 78.71, 79.88, 79.47 / 79.24, 79.34, 79.96 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 246.7 (245.4-259.6) | 304.4 (295.9-306.4) | +23.4% | 245.5, 252.7, 250.6 / 296.9, 304.5, 306.1 | consistent |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3103 (3065-3118) | 3088 (3070-3093) | -0.5% | 3094, 3083, 3113 / 3088, 3080, 3088 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2406 (2390-2437) | 2426 (2415-2449) | +0.8% | 2408, 2414, 2398 / 2423, 2440, 2420 | separated, inside spread |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 611.2 (610.5-632.3) | 627.2 (608.2-633.3) | +2.6% | 621.6, 619.9, 611.2 / 610.2, 629.5, 629.3 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 324.9 (309.2-334.2) | 374 (364-381.6) | +15.1% | 313.3, 329.2, 328.6 / 364.8, 378.3, 376 | consistent |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 1.221e+04 (1.217e+04-1.244e+04) | 1.227e+04 (1.197e+04-1.238e+04) | +0.5% | 1.221e+04, 1.231e+04, 1.221e+04 / 1.213e+04, 1.229e+04, 1.228e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 5948 (5895-6032) | 5801 (5775-5830) | -2.5% | 5980, 5931, 5940 / 5775, 5826, 5801 | consistent |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 164.9 (159.8-168.2) | 165.1 (164.5-166.1) | +0.1% | 161.5, 166.3, 165.6 / 164.9, 164.7, 165.9 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 281.5 (268.8-285.7) | 280.3 (271.4-282.4) | -0.4% | 274.1, 277.6, 285.4 / 276.9, 280.3, 280 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 1846 (1808-1866) | 1846 (1806-1876) | +0.0% | 1812, 1854, 1849 / 1874, 1822, 1831 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 2345 (2222-2382) | 2321 (2239-2354) | -1.0% | 2291, 2348, 2351 / 2292, 2336, 2284 | within noise |
| dense 30 x 784 forward / numpy | 8.368 (7.972-8.627) | 8.051 (7.897-8.908) | -3.8% | 8.4, 8.321, 8.242 / 8.402, 8.051, 8.103 | within noise |
| dense 30 x 784 forward / rust | 2.771 (2.668-2.825) | 2.68 (2.587-2.795) | -3.3% | 2.746, 2.714, 2.8 / 2.641, 2.654, 2.731 | within noise |
| dense 30 x 784 downstream / numpy | 4.007 (3.888-4.122) | 3.897 (3.877-4.099) | -2.7% | 4.021, 3.955, 4.008 / 3.955, 4.006, 3.879 | within noise |
| dense 30 x 784 downstream / rust | 2.238 (2.117-2.349) | 2.078 (1.995-2.214) | -7.1% | 2.17, 2.224, 2.3 / 2.047, 2.066, 2.154 | separated, inside spread |
| dense 30 x 784 hidden_delta / numpy | 6.882 (6.744-7.135) | 6.88 (6.604-7.151) | -0.0% | 7.035, 6.796, 6.842 / 6.685, 7.102, 6.863 | within noise |
| dense 30 x 784 hidden_delta / rust | 2.759 (2.648-2.93) | 2.832 (2.699-3.121) | +2.6% | 2.796, 2.759, 2.781 / 2.757, 3.004, 2.777 | within noise |
| dense 30 x 784 accumulate_gradient / numpy | 28.46 (27.96-29.32) | 27.74 (27.21-28.44) | -2.5% | 28.33, 28.43, 28.88 / 27.48, 28.09, 27.78 | separated, inside spread |
| dense 30 x 784 accumulate_gradient / rust | 7.016 (6.732-7.197) | 7.029 (6.855-7.248) | +0.2% | 6.959, 7.023, 7.016 / 7.061, 7.144, 6.911 | within noise |
| dense 30 x 784 apply_accumulated_gradient / numpy | 31.86 (31.67-32.62) | 31.34 (30.85-32.53) | -1.6% | 32.14, 31.71, 32.17 / 31.31, 31.71, 31.62 | within noise |
| dense 30 x 784 apply_accumulated_gradient / rust | 17.07 (16.51-17.32) | 17.07 (16.7-17.46) | +0.0% | 16.88, 16.81, 17.17 / 17.24, 16.88, 17.12 | within noise |
| dense 30 x 784 sgd step / numpy | 61.11 (59.5-62.23) | 60.92 (59.08-61.55) | -0.3% | 60.63, 60.86, 61.12 / 60.22, 60.92, 60.32 | within noise |
| dense 30 x 784 sgd step / rust | 7.426 (7.272-7.672) | 7.612 (7.332-7.81) | +2.5% | 7.434, 7.337, 7.588 / 7.509, 7.674, 7.641 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 38.33 (37.93-38.79) | 38.45 (37.65-38.94) | +0.3% | 38.33, 38.04, 38.75 / 38.37, 38.74, 38.08 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 50.45 (49.7-51.04) | 46.48 (46.07-46.95) | -7.9% | 49.73, 50.55, 50.78 / 46.48, 46.09, 46.81 | consistent |
| dense 30 x 784 forward_batch b512 / numpy | 267.8 (225.8-270.6) | 267.4 (264.9-270.4) | -0.2% | 245.1, 267.8, 270.6 / 265.3, 268, 269 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 362.8 (356.3-370.8) | 301.8 (297.4-307.3) | -16.8% | 359, 365.4, 366.7 / 305, 300, 300.8 | consistent |
| dense 30 x 784 downstream_batch b32 / numpy | 23.99 (23.67-24.19) | 23.85 (23.52-24.26) | -0.6% | 24.05, 23.8, 23.94 / 23.87, 23.85, 23.89 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 31.92 (31.18-33.01) | 41.1 (40.05-41.53) | +28.8% | 31.53, 31.89, 32.94 / 40.31, 41.22, 41.38 | consistent |
| dense 30 x 784 downstream_batch b512 / numpy | 130.7 (129.7-132.2) | 130.7 (130.4-131.4) | +0.1% | 129.9, 131.1, 131.5 / 130.5, 130.7, 131.1 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 244.5 (238.6-245.5) | 267.1 (261.5-273.6) | +9.3% | 239.5, 244.7, 245.3 / 268.7, 267.1, 267.6 | consistent |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 63.41 (61.79-64.75) | 62.98 (61.87-64.95) | -0.7% | 64.12, 62.73, 63.27 / 63.75, 62.89, 62.63 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / rust | 42.21 (41.34-43.42) | 51.3 (50.85-52.78) | +21.5% | 41.87, 41.94, 43.05 / 51.15, 52.4, 51.11 | consistent |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 1696 (1570-1713) | 1708 (1679-1761) | +0.7% | 1635, 1709, 1686 / 1689, 1744, 1708 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / rust | 499.5 (492.3-522.1) | 521.9 (513.4-525.5) | +4.5% | 499.5, 500.3, 507.2 / 519.4, 517.1, 524.4 | consistent |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 41.12 (40.07-41.42) | 40.24 (39.45-40.97) | -2.1% | 41.38, 41.14, 40.14 / 39.85, 40.81, 39.95 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 38 (37.04-39.46) | 40.49 (37.96-41.43) | +6.5% | 37.87, 37.62, 38.92 / 39.07, 40.38, 40.97 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 222.9 (216.5-223.7) | 222.9 (220.2-225.2) | +0.0% | 218, 223.6, 222.9 / 221.7, 221.5, 224.7 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 316.5 (313-321.9) | 313.5 (312.7-317.2) | -0.9% | 314.8, 319.9, 316 / 315, 312.7, 315.2 | within noise |
| dense 10 x 30 forward / numpy | 4.576 (4.418-4.769) | 4.536 (4.462-4.864) | -0.9% | 4.657, 4.518, 4.525 / 4.467, 4.579, 4.708 | within noise |
| dense 10 x 30 forward / rust | 0.3464 (0.3364-0.3677) | 0.3134 (0.3083-0.3156) | -9.5% | 0.3373, 0.3464, 0.3582 / 0.3128, 0.3109, 0.315 | consistent |
| dense 10 x 30 downstream / numpy | 0.8467 (0.8001-0.918) | 0.8369 (0.823-0.8476) | -1.2% | 0.8591, 0.8345, 0.8587 / 0.8353, 0.8276, 0.8448 | within noise |
| dense 10 x 30 downstream / rust | 0.2016 (0.196-0.2111) | 0.2244 (0.209-0.2277) | +11.3% | 0.1998, 0.199, 0.2066 / 0.225, 0.2136, 0.2261 | separated, inside spread |
| dense 10 x 30 hidden_delta / numpy | 2.24 (2.186-2.285) | 2.24 (2.174-2.279) | +0.0% | 2.211, 2.256, 2.254 / 2.198, 2.247, 2.262 | within noise |
| dense 10 x 30 hidden_delta / rust | 0.4359 (0.4193-0.4508) | 0.4305 (0.4261-0.4455) | -1.2% | 0.4271, 0.4434, 0.437 / 0.4272, 0.4298, 0.445 | within noise |
| dense 10 x 30 accumulate_gradient / numpy | 2.881 (2.813-2.91) | 2.897 (2.858-2.93) | +0.5% | 2.861, 2.857, 2.881 / 2.894, 2.864, 2.927 | within noise |
| dense 10 x 30 accumulate_gradient / rust | 0.4302 (0.41-0.4459) | 0.407 (0.3966-0.4131) | -5.4% | 0.4162, 0.4428, 0.4268 / 0.411, 0.398, 0.4074 | separated, inside spread |
| dense 10 x 30 apply_accumulated_gradient / numpy | 4.713 (4.486-5.144) | 4.661 (4.491-4.737) | -1.1% | 4.945, 4.535, 4.766 / 4.548, 4.65, 4.723 | within noise |
| dense 10 x 30 apply_accumulated_gradient / rust | 2.215 (2.165-2.268) | 2.211 (2.168-2.224) | -0.2% | 2.18, 2.216, 2.252 / 2.189, 2.214, 2.215 | within noise |
| dense 10 x 30 sgd step / numpy | 8.409 (8.151-8.925) | 8.373 (8.313-8.609) | -0.4% | 8.409, 8.538, 8.371 / 8.432, 8.317, 8.512 | within noise |
| dense 10 x 30 sgd step / rust | 0.4687 (0.4512-0.4999) | 0.4842 (0.4688-0.4914) | +3.3% | 0.4526, 0.4687, 0.4935 / 0.4769, 0.4807, 0.4894 | within noise |
| dense 10 x 30 forward_batch b32 / numpy | 9.928 (9.761-10.56) | 9.798 (9.482-9.889) | -1.3% | 10.24, 9.868, 9.845 / 9.611, 9.865, 9.765 | within noise |
| dense 10 x 30 forward_batch b32 / rust | 3.992 (3.978-4.077) | 2.744 (2.697-2.763) | -31.3% | 3.98, 3.992, 4.065 / 2.719, 2.733, 2.761 | consistent |
| dense 10 x 30 forward_batch b512 / numpy | 55.07 (54.63-56.13) | 54.61 (53.41-55.27) | -0.8% | 54.66, 55.53, 55.28 / 53.44, 54.61, 55.17 | within noise |
| dense 10 x 30 forward_batch b512 / rust | 58.27 (57.9-59.64) | 38.74 (38-39.13) | -33.5% | 57.98, 58.22, 59.31 / 38.38, 38.79, 38.75 | consistent |
| dense 10 x 30 downstream_batch b32 / numpy | 1.819 (1.762-1.87) | 1.785 (1.752-1.874) | -1.8% | 1.777, 1.843, 1.84 / 1.77, 1.771, 1.846 | within noise |
| dense 10 x 30 downstream_batch b32 / rust | 1.14 (1.117-1.185) | 1.341 (1.318-1.365) | +17.7% | 1.121, 1.141, 1.163 / 1.337, 1.341, 1.344 | consistent |
| dense 10 x 30 downstream_batch b512 / numpy | 12.41 (12.27-12.46) | 12.43 (12.23-12.59) | +0.1% | 12.33, 12.41, 12.45 / 12.38, 12.4, 12.48 | within noise |
| dense 10 x 30 downstream_batch b512 / rust | 15.16 (14.93-15.48) | 17.37 (17.15-17.94) | +14.6% | 14.93, 15.17, 15.34 / 17.22, 17.37, 17.91 | consistent |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 4.847 (4.79-4.961) | 4.935 (4.835-5.122) | +1.8% | 4.916, 4.825, 4.827 / 4.906, 4.935, 4.979 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 1.705 (1.659-1.747) | 1.915 (1.87-1.975) | +12.3% | 1.664, 1.726, 1.716 / 1.908, 1.902, 1.939 | consistent |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 35.73 (34.73-37.02) | 35.6 (34.61-36.88) | -0.4% | 36.52, 35.97, 34.98 / 36.08, 35.74, 35.19 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / rust | 22.45 (22.08-23.21) | 24.56 (24.22-24.96) | +9.4% | 22.18, 22.61, 22.93 / 24.34, 24.5, 24.94 | consistent |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 4.665 (4.398-4.916) | 4.544 (4.463-4.695) | -2.6% | 4.752, 4.497, 4.677 / 4.613, 4.547, 4.51 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 1.981 (1.952-2.015) | 1.968 (1.936-1.996) | -0.6% | 1.957, 2, 1.984 / 1.961, 1.953, 1.995 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 24.74 (24.48-25.33) | 25.09 (24.7-25.6) | +1.4% | 25.01, 24.57, 24.97 / 24.85, 25.53, 24.99 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 32.81 (32.27-33.17) | 33.28 (32.84-33.45) | +1.4% | 32.56, 32.75, 32.81 / 33.05, 33.37, 33.22 | separated, inside spread |
| conv 28x28, 8 ch forward / numpy | 55.66 (54.24-56.31) | 54.87 (54.32-55.95) | -1.4% | 56.03, 55.18, 55.14 / 54.43, 55.56, 54.87 | within noise |
| conv 28x28, 8 ch forward / rust | 18.88 (18.26-19.28) | 20.07 (19.86-20.64) | +6.3% | 18.26, 19.1, 19.04 / 20.02, 20.08, 20.28 | consistent |
| conv 28x28, 8 ch downstream / numpy | 38.74 (37.65-39.77) | 38.55 (37.58-40.57) | -0.5% | 39.65, 37.99, 38.74 / 38.22, 39.66, 38.58 | within noise |
| conv 28x28, 8 ch downstream / rust | 17.36 (16.85-17.96) | 17.92 (17.38-18.28) | +3.2% | 16.96, 17.67, 17.64 / 17.54, 17.92, 18.23 | within noise |
| conv 28x28, 8 ch accumulate_gradient / numpy | 35.78 (35.28-36.76) | 35.53 (35.21-36.1) | -0.7% | 35.47, 35.63, 36.33 / 35.32, 36, 35.48 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 16.1 (16.03-16.26) | 15.92 (15.85-15.96) | -1.1% | 16.04, 16.21, 16.1 / 15.89, 15.94, 15.9 | separated, inside spread |
| conv 28x28, 8 ch forward_batch b32 / numpy | 981.6 (970.4-985.5) | 977.4 (959.8-991.4) | -0.4% | 982.7, 977, 981.6 / 972.4, 989, 970.5 | within noise |
| conv 28x28, 8 ch forward_batch b32 / rust | 558 (550.6-576.7) | 600.6 (591.3-616) | +7.6% | 554.1, 557.5, 568.3 / 593, 600.9, 608.8 | consistent |
| conv 28x28, 8 ch forward_batch b512 / numpy | 1.829e+04 (1.808e+04-1.845e+04) | 1.834e+04 (1.791e+04-1.847e+04) | +0.3% | 1.834e+04, 1.817e+04, 1.835e+04 / 1.812e+04, 1.841e+04, 1.838e+04 | within noise |
| conv 28x28, 8 ch forward_batch b512 / rust | 9263 (9000-9476) | 9727 (9579-1.005e+04) | +5.0% | 9023, 9404, 9271 / 9583, 9727, 9968 | separated, inside spread |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 587.4 (576.5-614.9) | 595.8 (576.7-618.2) | +1.4% | 605.3, 578.7, 586.4 / 597.4, 613, 580.6 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / rust | 505.6 (489.7-511.2) | 519.8 (509.9-529.8) | +2.8% | 494.4, 506.6, 509.5 / 519.2, 514.9, 526.6 | separated, inside spread |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 1.617e+04 (1.6e+04-1.636e+04) | 1.609e+04 (1.6e+04-1.627e+04) | -0.5% | 1.632e+04, 1.617e+04, 1.606e+04 / 1.604e+04, 1.621e+04, 1.608e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / rust | 1432 (1421-1435) | 1462 (1446-1496) | +2.0% | 1426, 1435, 1431 / 1462, 1480, 1452 | separated, inside spread |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 1300 (1284-1388) | 1220 (1204-1226) | -6.1% | 1289, 1307, 1346 / 1205, 1220, 1224 | consistent |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 531.6 (529.6-536) | 530.7 (527.6-533.3) | -0.2% | 533, 531.4, 532.9 / 530.1, 531.2, 530 | separated, inside spread |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 2.004e+04 (1.959e+04-2.037e+04) | 2.013e+04 (1.99e+04-2.057e+04) | +0.4% | 1.961e+04, 2.004e+04, 2.023e+04 / 1.997e+04, 2.013e+04, 2.036e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 1.163e+04 (1.16e+04-1.168e+04) | 1.156e+04 (1.151e+04-1.158e+04) | -0.6% | 1.166e+04, 1.163e+04, 1.162e+04 / 1.156e+04, 1.157e+04, 1.153e+04 | consistent, small |
| conv 8x8, 8 ch forward / numpy | 28.39 (27.97-29.61) | 29.34 (27.68-29.46) | +3.3% | 29.32, 28.33, 28.08 / 28.81, 29.4, 28.57 | within noise |
| conv 8x8, 8 ch forward / rust | 1.502 (1.445-1.554) | 1.567 (1.557-1.585) | +4.3% | 1.465, 1.53, 1.51 / 1.564, 1.564, 1.582 | separated, inside spread |
| conv 8x8, 8 ch downstream / numpy | 21.89 (21.81-22.49) | 22.14 (21.73-23.34) | +1.1% | 21.92, 22.19, 21.86 / 22.02, 21.92, 22.79 | within noise |
| conv 8x8, 8 ch downstream / rust | 1.209 (1.161-1.241) | 1.241 (1.23-1.281) | +2.6% | 1.186, 1.222, 1.21 / 1.235, 1.25, 1.257 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient / numpy | 7.349 (7.165-7.539) | 7.403 (7.198-7.705) | +0.7% | 7.457, 7.428, 7.168 / 7.438, 7.451, 7.36 | within noise |
| conv 8x8, 8 ch accumulate_gradient / rust | 1.166 (1.157-1.191) | 1.171 (1.163-1.185) | +0.4% | 1.161, 1.165, 1.179 / 1.174, 1.176, 1.168 | within noise |
| conv 8x8, 8 ch forward_batch b32 / numpy | 75.64 (73.97-76.55) | 75.5 (74.91-78.96) | -0.2% | 76.28, 75.26, 74.59 / 77.1, 75.81, 75.5 | within noise |
| conv 8x8, 8 ch forward_batch b32 / rust | 31.61 (30.77-33.05) | 33.11 (32.91-33.68) | +4.7% | 31.91, 31.1, 31.94 / 32.98, 33.27, 33.39 | consistent |
| conv 8x8, 8 ch forward_batch b512 / numpy | 880.1 (873.9-890.8) | 884.4 (863.2-896.2) | +0.5% | 884.4, 880.8, 879.5 / 872.7, 890.7, 887.8 | within noise |
| conv 8x8, 8 ch forward_batch b512 / rust | 495.1 (471.4-507.5) | 519.5 (515.2-563.3) | +4.9% | 483.2, 494.1, 495.9 / 516.7, 521, 540.1 | separated, inside spread |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 65.13 (62.92-67.28) | 65.11 (62.89-65.96) | -0.0% | 65.84, 64.24, 65.27 / 63.81, 65.41, 65.49 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / rust | 28.25 (27.08-29.52) | 28.91 (28.78-30.92) | +2.3% | 27.14, 29.1, 28.25 / 28.99, 29.89, 28.79 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 693.1 (683.4-714.7) | 710.1 (682.4-725.2) | +2.5% | 699, 690.9, 693.1 / 699.8, 710.1, 710.9 | separated, inside spread |
| conv 8x8, 8 ch downstream_batch b512 / rust | 445.2 (427.3-451.5) | 461.4 (457.7-466.5) | +3.6% | 427.6, 449.7, 446.5 / 459.4, 460.6, 465.7 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 96.73 (95.16-97.39) | 93.45 (90.86-93.81) | -3.4% | 95.29, 96.95, 97.13 / 92.15, 93, 93.64 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 28.44 (28.25-28.54) | 27.4 (27.29-27.48) | -3.6% | 28.54, 28.36, 28.39 / 27.33, 27.36, 27.46 | consistent |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 1451 (1373-1468) | 1392 (1376-1409) | -4.1% | 1401, 1458, 1460 / 1379, 1398, 1399 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 465.8 (460.1-477.7) | 460.2 (454.7-466.5) | -1.2% | 467.8, 464.4, 468.9 / 457.5, 463.3, 457.6 | separated, inside spread |
| conv 13x13x8, 8 ch forward / numpy | 51.12 (49.91-52.04) | 50.71 (50.25-52.05) | -0.8% | 51.61, 50.48, 50.98 / 51.45, 50.71, 50.4 | within noise |
| conv 13x13x8, 8 ch forward / rust | 20.33 (20.28-20.73) | 20.04 (19.95-20.3) | -1.4% | 20.33, 20.43, 20.51 / 19.97, 20.14, 20.2 | separated, inside spread |
| conv 13x13x8, 8 ch downstream / numpy | 51.68 (50.97-53.5) | 52.17 (50.45-53.37) | +0.9% | 52.43, 51.48, 51.65 / 51.57, 52.34, 52.51 | within noise |
| conv 13x13x8, 8 ch downstream / rust | 12.03 (11.79-12.43) | 13.15 (12.93-13.6) | +9.3% | 11.81, 12.33, 12.03 / 12.98, 13.24, 13.34 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 23.21 (22.98-23.3) | 23.55 (22.9-24.12) | +1.4% | 23.18, 23.22, 23.13 / 23.21, 23.8, 23.69 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 5.355 (5.296-5.495) | 5.018 (4.932-5.163) | -6.3% | 5.333, 5.33, 5.457 / 4.95, 5.024, 5.114 | consistent |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 1016 (1002-1021) | 1014 (1004-1032) | -0.2% | 1018, 1011, 1014 / 1004, 1023, 1022 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 607.7 (603.9-613.5) | 602.3 (600.2-628.2) | -0.9% | 608.2, 607, 609.5 / 600.6, 603.7, 614.9 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 1.42e+04 (1.415e+04-1.424e+04) | 1.413e+04 (1.406e+04-1.424e+04) | -0.5% | 1.417e+04, 1.419e+04, 1.424e+04 / 1.417e+04, 1.413e+04, 1.413e+04 | separated, inside spread |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 1.813e+04 (1.803e+04-1.842e+04) | 1.813e+04 (1.783e+04-1.828e+04) | +0.0% | 1.816e+04, 1.812e+04, 1.826e+04 / 1.805e+04, 1.813e+04, 1.814e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 899 (858.8-932.2) | 915.1 (857.4-942.1) | +1.8% | 927.6, 879.1, 893.5 / 896.7, 916.9, 901.5 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 351.7 (337.5-360.4) | 386.5 (382.9-392.4) | +9.9% | 341.9, 355.8, 353.7 / 385.6, 387.4, 389.6 | consistent |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 2.575e+04 (2.563e+04-2.607e+04) | 2.598e+04 (2.566e+04-2.644e+04) | +0.9% | 2.596e+04, 2.57e+04, 2.57e+04 / 2.566e+04, 2.624e+04, 2.611e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 1046 (1034-1132) | 1137 (1123-1144) | +8.7% | 1037, 1056, 1088 / 1130, 1137, 1136 | separated, inside spread |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 597.7 (586.9-615.3) | 602.7 (597.3-613.4) | +0.8% | 588.6, 613.9, 597.7 / 601.8, 600.2, 612.1 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 169.4 (166-172.7) | 168.9 (166.3-172.9) | -0.3% | 171.1, 166.4, 169.4 / 168.6, 172.9, 167.1 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.04e+04 (1.017e+04-1.054e+04) | 1.038e+04 (1.022e+04-1.045e+04) | -0.2% | 1.02e+04, 1.044e+04, 1.047e+04 / 1.028e+04, 1.039e+04, 1.043e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 2603 (2549-2606) | 2572 (2536-2617) | -1.2% | 2603, 2602, 2578 / 2542, 2607, 2576 | within noise |
| conv 26x26x8/2, 8 ch forward / numpy | 54.1 (53.75-55.65) | 54.72 (53.1-55.44) | +1.2% | 55.52, 53.87, 54.01 / 53.76, 55.24, 54.25 | within noise |
| conv 26x26x8/2, 8 ch forward / rust | 24.22 (24.02-24.46) | 24.03 (23.6-24.33) | -0.8% | 24.06, 24.42, 24.21 / 23.83, 24.04, 24.17 | within noise |
| conv 26x26x8/2, 8 ch downstream / numpy | 61.16 (59.98-62.57) | 61.12 (58.89-62.74) | -0.1% | 62.18, 61.16, 60.05 / 61.28, 61.61, 60.05 | within noise |
| conv 26x26x8/2, 8 ch downstream / rust | 15.05 (14.69-15.39) | 16.39 (16.13-16.9) | +8.9% | 14.74, 15.18, 15.22 / 16.28, 16.37, 16.69 | consistent |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 26.33 (25.98-26.76) | 26.52 (26.23-26.67) | +0.7% | 26.15, 26.37, 26.39 / 26.37, 26.52, 26.53 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 5.897 (5.837-5.925) | 5.837 (5.709-5.953) | -1.0% | 5.915, 5.874, 5.863 / 5.897, 5.771, 5.861 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 1244 (1232-1264) | 1232 (1215-1238) | -1.0% | 1245, 1255, 1238 / 1226, 1232, 1235 | separated, inside spread |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 732.6 (721-741.1) | 732.5 (719.7-738.4) | -0.0% | 729.4, 729.5, 735.9 / 727.5, 737.6, 725.5 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 1.725e+04 (1.722e+04-1.752e+04) | 1.727e+04 (1.708e+04-1.738e+04) | +0.1% | 1.724e+04, 1.724e+04, 1.744e+04 / 1.719e+04, 1.722e+04, 1.732e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 2.245e+04 (2.223e+04-2.261e+04) | 2.258e+04 (2.252e+04-2.295e+04) | +0.6% | 2.247e+04, 2.242e+04, 2.244e+04 / 2.257e+04, 2.276e+04, 2.265e+04 | separated, inside spread |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 1173 (1159-1222) | 1177 (1168-1260) | +0.4% | 1180, 1166, 1198 / 1201, 1214, 1171 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 438.9 (420.9-442.8) | 470.9 (469.9-483.1) | +7.3% | 421.6, 439.1, 440.9 / 472.9, 470.6, 476.7 | consistent |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 4.218e+04 (4.139e+04-4.281e+04) | 4.255e+04 (4.239e+04-4.275e+04) | +0.9% | 4.242e+04, 4.252e+04, 4.158e+04 / 4.252e+04, 4.26e+04, 4.254e+04 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 2315 (2309-2322) | 2351 (2341-2373) | +1.6% | 2310, 2321, 2316 / 2360, 2349, 2352 | consistent, small |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 708.5 (697.1-724.5) | 710 (704.4-721.5) | +0.2% | 698.4, 708.5, 724.4 / 708.1, 707.6, 720.3 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 203.7 (200.1-208.3) | 204.6 (201.2-209) | +0.4% | 205.8, 202.5, 202.3 / 204.3, 206.3, 205.1 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 1.218e+04 (1.182e+04-1.238e+04) | 1.231e+04 (1.199e+04-1.242e+04) | +1.1% | 1.188e+04, 1.224e+04, 1.229e+04 / 1.212e+04, 1.229e+04, 1.237e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 3035 (2999-3106) | 2998 (2987-3059) | -1.2% | 3009, 3079, 3048 / 2991, 3046, 2995 | within noise |
| conv 26x26x8, 8 ch forward / numpy | 126.2 (124.9-127.2) | 126.8 (124.4-128.6) | +0.5% | 125.6, 126.7, 125.9 / 124.6, 127.1, 127.6 | within noise |
| conv 26x26x8, 8 ch forward / rust | 93.75 (92.99-94.87) | 91.68 (90.91-93.36) | -2.2% | 93.45, 93.93, 94.12 / 91.32, 91.75, 92.49 | separated, inside spread |
| conv 26x26x8, 8 ch downstream / numpy | 154.5 (145.8-155.6) | 151.8 (142.1-158.2) | -1.7% | 154.5, 155.5, 147.5 / 142.3, 155.7, 153.4 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 58.45 (56.37-59.87) | 63.79 (61.67-64.26) | +9.1% | 58.11, 57.88, 59.3 / 62.13, 63.79, 64.21 | consistent |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 89.57 (88.51-91.25) | 89.46 (88.62-91.87) | -0.1% | 89.02, 91.01, 89.53 / 89.19, 89.06, 91.47 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 25.09 (24.94-25.29) | 25.29 (24.88-25.38) | +0.8% | 25.2, 25, 25.12 / 25.11, 25.07, 25.36 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 4259 (4170-4303) | 4304 (4237-4369) | +1.0% | 4228, 4291, 4231 / 4304, 4296, 4326 | separated, inside spread |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 2983 (2950-3032) | 2975 (2944-2996) | -0.3% | 2976, 2993, 2993 / 2961, 2974, 2984 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 6.754e+04 (6.692e+04-6.784e+04) | 6.737e+04 (6.717e+04-6.857e+04) | -0.2% | 6.705e+04, 6.773e+04, 6.754e+04 / 6.732e+04, 6.746e+04, 6.79e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 8.565e+04 (8.516e+04-8.59e+04) | 8.456e+04 (8.435e+04-8.637e+04) | -1.3% | 8.564e+04, 8.55e+04, 8.565e+04 / 8.496e+04, 8.54e+04, 8.452e+04 | separated, inside spread |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 4762 (4698-4843) | 4823 (4617-4985) | +1.3% | 4762, 4770, 4761 / 4735, 4954, 4728 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 388.9 (379.7-403.3) | 417.3 (408.4-452.7) | +7.3% | 381.9, 402.2, 388.9 / 410.3, 436.8, 432.2 | separated, inside spread |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 1.135e+05 (1.125e+05-1.152e+05) | 1.131e+05 (1.125e+05-1.155e+05) | -0.4% | 1.15e+05, 1.133e+05, 1.13e+05 / 1.126e+05, 1.13e+05, 1.146e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 5013 (4963-5179) | 5308 (5277-5369) | +5.9% | 4986, 5082, 5050 / 5292, 5295, 5347 | consistent |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 3049 (2965-3100) | 3023 (2982-3091) | -0.9% | 2965, 3078, 3064 / 3000, 3051, 3052 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 667.9 (657.8-685.1) | 664.8 (656.8-669) | -0.5% | 669.8, 671.5, 667.9 / 665.7, 667.9, 657.3 | separated, inside spread |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 5.126e+04 (5.05e+04-5.201e+04) | 5.137e+04 (5.052e+04-5.213e+04) | +0.2% | 5.075e+04, 5.121e+04, 5.183e+04 / 5.062e+04, 5.137e+04, 5.186e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 1.205e+04 (1.174e+04-1.21e+04) | 1.205e+04 (1.174e+04-1.213e+04) | -0.0% | 1.178e+04, 1.207e+04, 1.206e+04 / 1.204e+04, 1.208e+04, 1.19e+04 | within noise |
| pool 26x26, 8 ch forward / numpy | 70.82 (69.88-71.92) | 70.61 (69.56-71.68) | -0.3% | 71.83, 70.37, 70.77 / 70.17, 70.01, 71.38 | within noise |
| pool 26x26, 8 ch forward / rust | 3.718 (3.682-3.761) | 3.784 (3.761-3.859) | +1.8% | 3.696, 3.729, 3.74 / 3.782, 3.77, 3.85 | separated, inside spread |
| pool 26x26, 8 ch downstream / numpy | 35.55 (34.77-36.26) | 34.74 (33.98-36.91) | -2.3% | 36.05, 34.94, 35.55 / 35.44, 34.78, 34.55 | within noise |
| pool 26x26, 8 ch downstream / rust | 5.158 (5.106-5.204) | 4.109 (4.05-4.172) | -20.3% | 5.132, 5.145, 5.188 / 4.072, 4.111, 4.143 | consistent |
| pool 26x26, 8 ch forward_batch b32 / numpy | 1223 (1219-1245) | 1222 (1219-1239) | -0.1% | 1224, 1219, 1234 / 1221, 1220, 1235 | within noise |
| pool 26x26, 8 ch forward_batch b32 / rust | 112 (110.6-114.2) | 112.1 (112-112.6) | +0.1% | 111.3, 111.7, 113.3 / 112.6, 112.1, 112 | within noise |
| pool 26x26, 8 ch forward_batch b512 / numpy | 2.026e+04 (2.004e+04-2.03e+04) | 2.022e+04 (1.997e+04-2.036e+04) | -0.2% | 2.006e+04, 2.027e+04, 2.028e+04 / 2.004e+04, 2.022e+04, 2.035e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 2412 (2395-2429) | 2423 (2417-2455) | +0.4% | 2422, 2419, 2402 / 2436, 2429, 2423 | separated, inside spread |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 485.2 (476.4-500.9) | 490.3 (475.5-504.5) | +1.1% | 495.7, 478.6, 484.5 / 491.8, 492.6, 487.7 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / rust | 158.9 (157.9-160.4) | 132.1 (130.2-132.3) | -16.9% | 159, 159.5, 158.4 / 131.3, 132.2, 131.9 | consistent |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 1.37e+04 (1.36e+04-1.381e+04) | 1.374e+04 (1.348e+04-1.407e+04) | +0.3% | 1.372e+04, 1.369e+04, 1.37e+04 / 1.37e+04, 1.39e+04, 1.369e+04 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / rust | 3001 (2992-3041) | 2619 (2605-2635) | -12.7% | 2999, 3019, 3001 / 2620, 2631, 2607 | consistent |
| pool 6x6, 8 ch forward / numpy | 33.94 (32.97-35.67) | 34.2 (33.61-34.88) | +0.8% | 34.76, 33.6, 33.51 / 33.99, 34.16, 34.55 | within noise |
| pool 6x6, 8 ch forward / rust | 0.4889 (0.4814-0.4996) | 0.4963 (0.4942-0.5028) | +1.5% | 0.4816, 0.4889, 0.4986 / 0.4951, 0.4971, 0.4997 | within noise |
| pool 6x6, 8 ch downstream / numpy | 19.46 (19.19-19.86) | 19.39 (18.9-19.97) | -0.4% | 19.49, 19.38, 19.53 / 19.45, 19.09, 19.69 | within noise |
| pool 6x6, 8 ch downstream / rust | 0.5706 (0.5615-0.5809) | 0.4693 (0.4543-0.4752) | -17.8% | 0.5651, 0.5673, 0.5785 / 0.4647, 0.4693, 0.4676 | consistent |
| pool 6x6, 8 ch forward_batch b32 / numpy | 108.8 (107.8-110) | 108.8 (108.1-110.3) | -0.0% | 109.3, 108.4, 108.9 / 109.4, 108.5, 109.1 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 8.301 (8.209-8.362) | 8.348 (8.287-8.449) | +0.6% | 8.225, 8.36, 8.292 / 8.329, 8.386, 8.366 | within noise |
| pool 6x6, 8 ch forward_batch b512 / numpy | 1212 (1210-1224) | 1209 (1203-1231) | -0.3% | 1210, 1217, 1214 / 1207, 1217, 1220 | within noise |
| pool 6x6, 8 ch forward_batch b512 / rust | 129.2 (127.7-130.9) | 130.4 (129.6-133.7) | +0.9% | 128.2, 130.1, 129.5 / 130.2, 130, 132 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 60.1 (59.24-61.63) | 60.63 (59.17-61.89) | +0.9% | 60.6, 59.65, 60.68 / 61.11, 60.25, 60.07 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / rust | 11.37 (11.22-11.59) | 7.671 (7.602-7.73) | -32.5% | 11.23, 11.49, 11.37 / 7.65, 7.64, 7.712 | consistent |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 600.2 (595.6-611.4) | 598.5 (590.9-611.3) | -0.3% | 608, 597.2, 599.5 / 602.3, 597.6, 598.5 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 178.9 (177-184) | 120.7 (119.2-123.9) | -32.5% | 177.9, 179.4, 181.8 / 120.4, 119.8, 122.5 | consistent |
| conv tail 32 x 5408 bare downstream b32 / numpy | 72.03 (65.62-79.64) | 69.06 (67.02-77.97) | -4.1% | 66.15, 74.38, 75.4 / 67.79, 72.72, 73.44 | within noise |
| conv tail 32 x 5408 bare downstream b32 / rust | 250.7 (240.8-253.3) | 300.5 (298.1-305.8) | +19.8% | 243.1, 251.5, 252.2 / 299, 301.8, 303.4 | consistent |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3219 (3188-3230) | 3208 (3095-3222) | -0.3% | 3208, 3210, 3227 / 3211, 3205, 3159 | within noise |
| conv tail 32 x 5408 bare downstream b512 / rust | 2414 (2406-2443) | 2277 (2255-2309) | -5.7% | 2437, 2413, 2407 / 2285, 2266, 2293 | consistent |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 78.95 (78.6-79.32) | 79.14 (78.63-80.02) | +0.2% | 79, 78.84, 79.07 / 79.06, 78.79, 79.74 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / rust | 240 (234-249.2) | 299.4 (292.9-302.8) | +24.8% | 236.6, 238.3, 246.7 / 297.9, 299.7, 299.4 | consistent |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 1633 (1618-1661) | 1651 (1613-1672) | +1.1% | 1641, 1635, 1626 / 1663, 1620, 1659 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / rust | 2219 (2133-2257) | 2241 (2230-2283) | +1.0% | 2175, 2249, 2202 / 2241, 2279, 2232 | within noise |
| conv tail 32 x 5408 transpose b32 / numpy | 0.7099 (0.7007-0.7294) | 0.7164 (0.706-0.7235) | +0.9% | 0.7012, 0.7167, 0.72 / 0.7089, 0.7182, 0.7216 | within noise |
| conv tail 32 x 5408 transpose b32 / rust | 0.8342 (0.8079-0.8507) | 0.8588 (0.8387-0.8711) | +3.0% | 0.8082, 0.8342, 0.8483 / 0.8403, 0.864, 0.862 | within noise |
| conv tail 32 x 5408 transpose b512 / numpy | 11.56 (10.7-12.61) | 11.56 (10.96-12.71) | -0.0% | 11.56, 10.9, 12.25 / 12.24, 11.53, 11.27 | within noise |
| conv tail 32 x 5408 transpose b512 / rust | 12.6 (12.26-12.69) | 14.59 (13.92-15.12) | +15.7% | 12.43, 12.64, 12.6 / 14.93, 14.57, 14.25 | consistent |
| conv tail 32 x 5408 add b32 / numpy | 95.49 (94.84-100.8) | 97.87 (95.43-101.2) | +2.5% | 98.01, 96.57, 95.11 / 98.31, 97.87, 97.86 | within noise |
| conv tail 32 x 5408 add b32 / rust | 65.99 (63.02-69.36) | 66.19 (66.06-69.32) | +0.3% | 67.67, 64.54, 64.58 / 69.31, 66.06, 66.19 | within noise |
| conv tail 32 x 5408 add b512 / numpy | 95.54 (94-99.98) | 98.42 (94.66-100.1) | +3.0% | 98.34, 95.54, 94.09 / 97.34, 99.99, 96.89 | within noise |
| conv tail 32 x 5408 add b512 / rust | 65.91 (62.95-69.47) | 62.52 (62.39-62.79) | -5.2% | 67.69, 64.44, 64.6 / 62.48, 62.68, 62.45 | separated, inside spread |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 1.443 (1.375-1.494) | 1.463 (1.4-1.53) | +1.4% | 1.435, 1.458, 1.423 / 1.465, 1.471, 1.439 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.4393 (0.4236-0.4429) | 0.4286 (0.4232-0.4361) | -2.4% | 0.4248, 0.4412, 0.4393 / 0.4245, 0.4286, 0.4329 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 11.47 (11.24-11.67) | 10.44 (10.19-10.66) | -9.0% | 11.3, 11.61, 11.53 / 10.33, 10.41, 10.53 | consistent |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 4.875 (4.751-4.92) | 4.779 (4.735-4.833) | -2.0% | 4.784, 4.909, 4.875 / 4.746, 4.79, 4.802 | within noise |
| dense 30 x 784 bare downstream b32 / numpy | 23.71 (23.02-24.07) | 23.09 (22.64-23.52) | -2.6% | 23.9, 23.42, 23.36 / 22.95, 23.16, 23.2 | separated, inside spread |
| dense 30 x 784 bare downstream b32 / rust | 29.44 (29.28-30.15) | 39.62 (38.95-40.5) | +34.6% | 29.43, 29.56, 29.74 / 39.14, 39.64, 40.2 | consistent |
| dense 30 x 784 bare downstream b512 / numpy | 137.9 (112.3-141.4) | 138.9 (136-142) | +0.7% | 125.7, 139.3, 137.9 / 137.9, 137.9, 140.6 | within noise |
| dense 30 x 784 bare downstream b512 / rust | 246.1 (240.6-249.5) | 266.8 (262.5-271) | +8.4% | 242.3, 248.6, 246.3 / 263.2, 269, 267.8 | consistent |
| dense 30 x 784 bare accumulate b32 / numpy | 28.57 (27.95-28.94) | 28.96 (28.75-29.33) | +1.4% | 28.57, 28.68, 28.33 / 28.79, 29.22, 29.06 | separated, inside spread |
| dense 30 x 784 bare accumulate b32 / rust | 32.81 (31.73-33.8) | 40.31 (39.43-40.86) | +22.9% | 31.97, 33.5, 32.81 / 39.93, 39.96, 40.75 | consistent |
| dense 30 x 784 bare accumulate b512 / numpy | 194.2 (191.9-195.7) | 194.4 (192.5-196.3) | +0.1% | 194.9, 193.7, 193.1 / 194.4, 194.2, 195.2 | within noise |
| dense 30 x 784 bare accumulate b512 / rust | 283.6 (275.6-291.9) | 289.7 (281.5-296.9) | +2.1% | 278.2, 289.1, 284.9 / 283.9, 289.7, 295 | within noise |
| dense 30 x 784 transpose b32 / numpy | 0.7003 (0.6791-0.7357) | 0.695 (0.6789-0.704) | -0.8% | 0.6806, 0.7064, 0.7155 / 0.6863, 0.6976, 0.6928 | within noise |
| dense 30 x 784 transpose b32 / rust | 0.8092 (0.7877-0.8135) | 0.8352 (0.8146-0.8419) | +3.2% | 0.7886, 0.8114, 0.8104 / 0.8154, 0.8413, 0.8352 | separated, inside spread |
| dense 30 x 784 transpose b512 / numpy | 7.248 (7.167-7.426) | 7.205 (7.119-7.363) | -0.6% | 7.248, 7.41, 7.179 / 7.186, 7.26, 7.205 | within noise |
| dense 30 x 784 transpose b512 / rust | 12.76 (12.51-13.71) | 13.8 (13.26-14.22) | +8.1% | 12.65, 13.21, 12.82 / 13.3, 13.8, 14.08 | separated, inside spread |
| dense 30 x 784 add b32 / numpy | 10.94 (10.55-11.61) | 9.072 (9.018-9.97) | -17.1% | 11.31, 10.94, 10.59 / 9.525, 9.36, 9.056 | consistent |
| dense 30 x 784 add b32 / rust | 9.168 (8.895-9.568) | 9.076 (8.694-9.712) | -1.0% | 9.232, 9.267, 9.168 / 9.203, 9.042, 9.076 | within noise |
| dense 30 x 784 add b512 / numpy | 12.65 (12.23-12.97) | 12.27 (12.15-12.96) | -3.0% | 12.78, 12.77, 12.43 / 12.5, 12.6, 12.27 | within noise |
| dense 30 x 784 add b512 / rust | 9.014 (8.613-9.339) | 9.064 (8.483-9.414) | +0.5% | 9.17, 9.048, 8.651 / 8.967, 8.799, 9.064 | within noise |
| dense 30 x 784 sum_axis0 b32 / numpy | 1.479 (1.46-1.505) | 1.468 (1.427-1.499) | -0.7% | 1.481, 1.479, 1.483 / 1.458, 1.463, 1.473 | separated, inside spread |
| dense 30 x 784 sum_axis0 b32 / rust | 0.3912 (0.3817-0.4046) | 0.4031 (0.3944-0.427) | +3.0% | 0.3857, 0.3939, 0.3959 / 0.3977, 0.4031, 0.4184 | separated, inside spread |
| dense 30 x 784 sum_axis0 b512 / numpy | 10.95 (10.68-11.68) | 10.88 (10.67-11.39) | -0.6% | 10.91, 10.96, 11.18 / 10.7, 10.91, 11.17 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 4.156 (4.026-4.254) | 4.438 (4.308-4.489) | +6.8% | 4.053, 4.254, 4.156 / 4.399, 4.403, 4.46 | separated, inside spread |
| dense 10 x 30 bare downstream b32 / numpy | 1.802 (1.779-1.857) | 1.797 (1.76-1.825) | -0.3% | 1.787, 1.81, 1.829 / 1.792, 1.797, 1.803 | within noise |
| dense 10 x 30 bare downstream b32 / rust | 1.165 (1.13-1.202) | 1.247 (1.224-1.277) | +7.0% | 1.142, 1.188, 1.176 / 1.23, 1.247, 1.274 | separated, inside spread |
| dense 10 x 30 bare downstream b512 / numpy | 11.92 (11.82-12.37) | 11.98 (11.7-12.13) | +0.6% | 11.87, 12.14, 11.98 / 11.86, 11.99, 12.04 | within noise |
| dense 10 x 30 bare downstream b512 / rust | 15.85 (15.46-15.97) | 17.68 (17.52-18.32) | +11.5% | 15.46, 15.88, 15.92 / 17.54, 17.68, 18.25 | consistent |
| dense 10 x 30 bare accumulate b32 / numpy | 1.822 (1.793-1.88) | 1.803 (1.76-1.9) | -1.1% | 1.819, 1.822, 1.836 / 1.794, 1.778, 1.876 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 1.207 (1.203-1.211) | 1.283 (1.273-1.299) | +6.3% | 1.206, 1.21, 1.205 / 1.275, 1.294, 1.283 | consistent |
| dense 10 x 30 bare accumulate b512 / numpy | 13.44 (13.24-13.57) | 13.37 (13.18-13.72) | -0.5% | 13.49, 13.41, 13.41 / 13.19, 13.37, 13.64 | within noise |
| dense 10 x 30 bare accumulate b512 / rust | 25.52 (25.18-26.14) | 25.61 (25.39-26.27) | +0.4% | 25.78, 25.53, 25.49 / 25.57, 25.61, 25.83 | within noise |
| dense 10 x 30 transpose b32 / numpy | 0.4471 (0.4341-0.4573) | 0.4487 (0.4351-0.4812) | +0.4% | 0.4446, 0.4471, 0.4505 / 0.4413, 0.4443, 0.4657 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.3815 (0.3692-0.3958) | 0.3869 (0.3834-0.3902) | +1.4% | 0.371, 0.384, 0.3885 / 0.3846, 0.3884, 0.3879 | within noise |
| dense 10 x 30 transpose b512 / numpy | 2.955 (2.932-3.042) | 2.989 (2.957-3.017) | +1.2% | 2.965, 2.955, 2.987 / 2.988, 2.967, 3.008 | within noise |
| dense 10 x 30 transpose b512 / rust | 4.136 (4.079-4.211) | 3.983 (3.925-4.016) | -3.7% | 4.08, 4.178, 4.158 / 3.954, 3.963, 3.999 | separated, inside spread |
| dense 10 x 30 add b32 / numpy | 0.4092 (0.397-0.412) | 0.409 (0.4033-0.4154) | -0.0% | 0.3991, 0.411, 0.4098 / 0.4048, 0.4115, 0.4111 | within noise |
| dense 10 x 30 add b32 / rust | 0.194 (0.1895-0.2047) | 0.1917 (0.1886-0.2077) | -1.2% | 0.1903, 0.1947, 0.1991 / 0.1982, 0.1899, 0.1926 | within noise |
| dense 10 x 30 add b512 / numpy | 0.421 (0.4066-0.4256) | 0.4236 (0.4125-0.4247) | +0.6% | 0.4079, 0.4212, 0.4232 / 0.4178, 0.4244, 0.4231 | within noise |
| dense 10 x 30 add b512 / rust | 0.2031 (0.1978-0.2079) | 0.2104 (0.1997-0.2315) | +3.6% | 0.1995, 0.2053, 0.2038 / 0.2098, 0.2005, 0.2263 | within noise |
| dense 10 x 30 sum_axis0 b32 / numpy | 1.289 (1.259-1.329) | 1.299 (1.259-1.36) | +0.8% | 1.272, 1.289, 1.315 / 1.272, 1.33, 1.306 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.2861 (0.2747-0.2921) | 0.3086 (0.3058-0.3204) | +7.9% | 0.278, 0.2861, 0.2917 / 0.3075, 0.3132, 0.309 | consistent |
| dense 10 x 30 sum_axis0 b512 / numpy | 9.063 (9.013-9.211) | 9.118 (8.984-9.913) | +0.6% | 9.022, 9.063, 9.182 / 8.999, 9.141, 9.505 | within noise |
| dense 10 x 30 sum_axis0 b512 / rust | 2.565 (2.485-2.61) | 2.983 (2.954-3.057) | +16.3% | 2.487, 2.582, 2.58 / 2.96, 2.999, 3.029 | consistent |
| attention 16 x 32 forward_batch b32 / numpy | 293.7 (287-298.4) | 289.1 (286.1-293.8) | -1.6% | 296.1, 294.1, 289.2 / 290.8, 288.3, 289.8 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 364 (357-368.1) | 386.1 (377.8-392.4) | +6.1% | 358, 367.1, 365 / 381.1, 386.1, 390.2 | consistent |
| attention 16 x 32 forward_batch b512 / numpy | 5120 (4872-5195) | 5140 (5009-5183) | +0.4% | 4899, 5132, 5163 / 5085, 5165, 5128 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 5648 (5579-5713) | 6024 (5823-6046) | +6.7% | 5610, 5646, 5688 / 5934, 6029, 5994 | consistent |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 266.4 (262.5-270.7) | 262.8 (262.3-268.8) | -1.4% | 264.4, 266.3, 268.8 / 263.3, 265.5, 262.4 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / rust | 251 (246.3-253.6) | 285.3 (281.8-288.8) | +13.7% | 248.1, 252.4, 251 / 281.9, 285.3, 288.7 | consistent |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 4567 (4520-4579) | 4571 (4531-4613) | +0.1% | 4548, 4579, 4543 / 4549, 4596, 4571 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / rust | 4674 (4614-4710) | 4951 (4858-4995) | +5.9% | 4663, 4691, 4644 / 4968, 4938, 4913 | consistent |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 248 (243.4-252.9) | 246.8 (241.7-259.1) | -0.5% | 245.8, 248.5, 250.3 / 250.7, 245.3, 246.8 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 214.2 (205-224.8) | 216.1 (208.3-238.2) | +0.9% | 211.9, 209.9, 221.7 / 211.8, 218.4, 223.3 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5566 (5471-6002) | 5575 (5461-5696) | +0.1% | 5566, 5837, 5474 / 5578, 5568, 5575 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 4054 (4013-4075) | 4010 (4003-4024) | -1.1% | 4015, 4059, 4069 / 4005, 4018, 4015 | within noise |
