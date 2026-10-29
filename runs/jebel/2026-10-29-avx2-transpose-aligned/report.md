Old `700723f` against new `700723f`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --op transpose --op accumulate_gradient_batch --op sum_axis0 --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `be14eac` (extension sha256 `f80c18214fe4`) and new crate `bcee60e` (extension sha256 `0b41a45954b8`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 2.14 (HIGH) (measured just after this run's crate builds); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / dense 10 x 30 transpose b512 / rust +49.3% (4.061 -> 6.062 µs)
- consistent: per call / conv tail 32 x 5408 transpose b32 / rust -26.2% (0.8234 -> 0.608 µs)
- consistent: per call / dense 30 x 784 transpose b32 / rust -21.3% (0.8021 -> 0.6316 µs)
- consistent: per call / attention 16 x 32 accumulate_gradient_batch b32 / rust +13.4% (219.6 -> 249 µs)
- consistent: per call / dense 10 x 30 transpose b32 / rust -12.4% (0.3742 -> 0.3278 µs)
- consistent: per call / attention 16 x 32 accumulate_gradient_batch b512 / rust +4.8% (4059 -> 4253 µs)
- consistent: per call / dense 10 x 30 accumulate_gradient_batch b512 / rust +3.8% (32.65 -> 33.88 µs)
- consistent: per call / dense 10 x 30 accumulate_gradient_batch b32 / rust -2.2% (1.944 -> 1.901 µs)
- consistent, small: per call / conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust +1.2% (3049 -> 3087 µs)
- 51 rows within noise (7 separated inside their spread), max |Δ| 10.5%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 150.7 (135.3-165.9) | 152.5 (138.7-166.1) | +1.2% | 147.4, 153.5, 153.4 / 151.1, 153.8, 152.7 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 282.5 (273.5-290.9) | 282.1 (273.2-289.1) | -0.1% | 279.1, 282.5, 285.6 / 281.1, 282.1, 283.6 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 1851 (1707-1871) | 1833 (1796-1857) | -1.0% | 1770, 1868, 1851 / 1833, 1803, 1854 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 2373 (2273-2625) | 2356 (2223-2395) | -0.7% | 2327, 2494, 2373 / 2324, 2308, 2387 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 40.78 (39.84-41.94) | 40.53 (39.75-41.32) | -0.6% | 41.03, 41.33, 39.91 / 40.7, 40.53, 40.53 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 38.21 (37.53-39.87) | 38.24 (37.52-38.85) | +0.1% | 37.59, 38.83, 39.14 / 37.57, 38.24, 38.76 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 221.3 (219.4-224.8) | 222.3 (221.4-222.6) | +0.4% | 219.9, 221.3, 224.5 / 222.4, 221.8, 222.4 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 316.7 (309.7-326.6) | 327.6 (321.4-336.4) | +3.5% | 313.2, 317.3, 321.6 / 327.6, 329.1, 325.3 | separated, inside spread |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 4.54 (4.44-5.076) | 4.481 (4.421-4.827) | -1.3% | 4.482, 4.514, 4.815 / 4.551, 4.441, 4.63 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 1.944 (1.93-1.955) | 1.901 (1.891-1.914) | -2.2% | 1.949, 1.937, 1.945 / 1.905, 1.908, 1.894 | consistent |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 24.86 (24.6-25.08) | 24.7 (24.4-25.12) | -0.6% | 24.72, 24.75, 25.07 / 24.49, 24.76, 24.9 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 32.65 (32.43-32.68) | 33.88 (33.52-34.34) | +3.8% | 32.66, 32.58, 32.56 / 33.81, 34.27, 33.61 | consistent |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 1307 (1281-1357) | 1312 (1304-1321) | +0.4% | 1319, 1312, 1305 / 1313, 1305, 1320 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 523.4 (521.3-529.2) | 524.6 (522.5-526.9) | +0.2% | 523.3, 523.1, 525.5 / 524.7, 522.6, 526.7 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 2.01e+04 (1.955e+04-2.026e+04) | 1.999e+04 (1.983e+04-2.015e+04) | -0.5% | 1.956e+04, 2.02e+04, 2.011e+04 / 1.997e+04, 1.991e+04, 2.013e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 1.152e+04 (1.149e+04-1.158e+04) | 1.152e+04 (1.15e+04-1.157e+04) | +0.0% | 1.152e+04, 1.152e+04, 1.153e+04 / 1.151e+04, 1.156e+04, 1.152e+04 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 96.79 (94.72-98.71) | 96.23 (94.45-98.83) | -0.6% | 94.87, 96.79, 98.09 / 94.55, 96.23, 97.66 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 27.79 (27.73-27.93) | 27.91 (27.87-28.25) | +0.4% | 27.79, 27.87, 27.74 / 27.91, 28.1, 27.88 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 1450 (1422-1466) | 1447 (1420-1477) | -0.2% | 1422, 1450, 1462 / 1437, 1448, 1456 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 458.2 (452.3-464.2) | 455.7 (453.6-458.9) | -0.5% | 458.2, 460.1, 457.9 / 456.5, 455.5, 456.2 | separated, inside spread |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 601.1 (584.8-612.6) | 601.3 (593.4-609.8) | +0.0% | 591.8, 608, 600.8 / 598.4, 599.3, 606.8 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 169.3 (166.4-172.4) | 166.3 (165.9-167.4) | -1.7% | 167.8, 171, 168 / 166, 166.3, 167.1 | separated, inside spread |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.037e+04 (1.016e+04-1.058e+04) | 1.034e+04 (1.023e+04-1.049e+04) | -0.3% | 1.027e+04, 1.035e+04, 1.054e+04 / 1.029e+04, 1.029e+04, 1.045e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 2532 (2523-2604) | 2595 (2525-2615) | +2.5% | 2561, 2564, 2532 / 2597, 2570, 2595 | separated, inside spread |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 711.6 (697.1-718.5) | 708.9 (704.7-714.3) | -0.4% | 697.9, 711.6, 717.6 / 707.4, 706.4, 714 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 202.2 (199.9-204.5) | 199.9 (199.5-203.8) | -1.1% | 202.5, 204, 200.2 / 199.7, 200.2, 201.7 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 1.229e+04 (1.176e+04-1.257e+04) | 1.23e+04 (1.194e+04-1.232e+04) | +0.0% | 1.192e+04, 1.241e+04, 1.239e+04 / 1.215e+04, 1.213e+04, 1.232e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 3049 (2992-3107) | 3087 (3078-3098) | +1.2% | 3051, 3053, 3042 / 3081, 3089, 3093 | consistent, small |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 3047 (2964-3112) | 3046 (2995-3103) | -0.0% | 2982, 3102, 3054 / 3049, 3035, 3071 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 666.9 (665.3-678) | 669.5 (656.1-692.6) | +0.4% | 666.2, 674.2, 666.4 / 670.3, 674.4, 666.3 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 5.141e+04 (5.012e+04-5.193e+04) | 5.133e+04 (5.101e+04-5.187e+04) | -0.2% | 5.037e+04, 5.159e+04, 5.168e+04 / 5.114e+04, 5.149e+04, 5.138e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 1.187e+04 (1.169e+04-1.207e+04) | 1.203e+04 (1.175e+04-1.211e+04) | +1.4% | 1.206e+04, 1.172e+04, 1.185e+04 / 1.192e+04, 1.202e+04, 1.207e+04 | within noise |
| conv tail 32 x 5408 transpose b32 / numpy | 0.7159 (0.7-0.7222) | 0.7146 (0.6988-0.7191) | -0.2% | 0.7029, 0.7159, 0.7207 / 0.701, 0.7168, 0.7155 | within noise |
| conv tail 32 x 5408 transpose b32 / rust | 0.8234 (0.8071-0.8382) | 0.608 (0.592-0.6195) | -26.2% | 0.8073, 0.825, 0.8325 / 0.607, 0.6057, 0.6104 | consistent |
| conv tail 32 x 5408 transpose b512 / numpy | 12.91 (11.52-13.62) | 12.33 (11.09-13.52) | -4.5% | 13.34, 12.02, 12.72 / 11.88, 11.77, 13.12 | within noise |
| conv tail 32 x 5408 transpose b512 / rust | 12.48 (12.38-12.97) | 13.79 (13.47-23.02) | +10.5% | 12.43, 12.69, 12.56 / 18.29, 13.99, 13.79 | separated, inside spread |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 1.422 (1.351-1.447) | 1.428 (1.38-1.453) | +0.4% | 1.386, 1.434, 1.401 / 1.442, 1.39, 1.434 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.431 (0.4257-0.4364) | 0.4308 (0.4259-0.4475) | -0.0% | 0.4264, 0.4322, 0.4346 / 0.4267, 0.4308, 0.4406 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 11.39 (11.34-11.56) | 11.32 (11.16-11.62) | -0.6% | 11.34, 11.48, 11.43 / 11.24, 11.44, 11.33 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 4.88 (4.731-4.937) | 4.854 (4.815-4.949) | -0.5% | 4.739, 4.91, 4.899 / 4.837, 4.843, 4.927 | within noise |
| dense 30 x 784 transpose b32 / numpy | 0.6894 (0.6819-0.7004) | 0.6868 (0.6809-0.7069) | -0.4% | 0.6822, 0.6894, 0.6981 / 0.684, 0.6848, 0.6976 | within noise |
| dense 30 x 784 transpose b32 / rust | 0.8021 (0.7843-0.8065) | 0.6316 (0.627-0.6431) | -21.3% | 0.785, 0.805, 0.8032 / 0.6279, 0.6355, 0.6355 | consistent |
| dense 30 x 784 transpose b512 / numpy | 7.178 (7.148-7.239) | 7.264 (7.147-7.343) | +1.2% | 7.154, 7.214, 7.181 / 7.181, 7.318, 7.25 | within noise |
| dense 30 x 784 transpose b512 / rust | 13.21 (12.65-13.77) | 12.96 (11.76-14.07) | -1.9% | 12.93, 13.4, 13.42 / 13.79, 12.29, 12.51 | within noise |
| dense 30 x 784 sum_axis0 b32 / numpy | 1.457 (1.41-1.513) | 1.446 (1.418-1.624) | -0.7% | 1.43, 1.464, 1.489 / 1.453, 1.42, 1.544 | within noise |
| dense 30 x 784 sum_axis0 b32 / rust | 0.3831 (0.3729-0.3932) | 0.3893 (0.3864-0.399) | +1.6% | 0.3746, 0.3855, 0.3875 / 0.3934, 0.3892, 0.3892 | separated, inside spread |
| dense 30 x 784 sum_axis0 b512 / numpy | 10.78 (10.75-10.89) | 10.77 (10.72-10.94) | -0.1% | 10.76, 10.83, 10.82 / 10.75, 10.76, 10.91 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 4.157 (4.004-4.217) | 4.147 (4.082-4.291) | -0.3% | 4.008, 4.157, 4.211 / 4.105, 4.192, 4.227 | within noise |
| dense 10 x 30 transpose b32 / numpy | 0.4465 (0.4449-0.4517) | 0.4424 (0.4381-0.4491) | -0.9% | 0.4459, 0.4475, 0.4491 / 0.4402, 0.442, 0.4473 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.3742 (0.369-0.3813) | 0.3278 (0.3246-0.3298) | -12.4% | 0.3692, 0.3774, 0.3773 / 0.3247, 0.3283, 0.3288 | consistent |
| dense 10 x 30 transpose b512 / numpy | 2.971 (2.919-3.045) | 2.932 (2.915-2.985) | -1.3% | 2.955, 2.971, 2.999 / 2.929, 2.94, 2.956 | within noise |
| dense 10 x 30 transpose b512 / rust | 4.061 (4.05-4.201) | 6.062 (5.99-6.207) | +49.3% | 4.052, 4.061, 4.186 / 6.145, 6.036, 6.033 | consistent |
| dense 10 x 30 sum_axis0 b32 / numpy | 1.307 (1.29-1.346) | 1.321 (1.258-1.451) | +1.1% | 1.309, 1.325, 1.302 / 1.271, 1.332, 1.381 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.2812 (0.2726-0.2879) | 0.2851 (0.2805-0.289) | +1.4% | 0.2731, 0.2812, 0.2857 / 0.2847, 0.2844, 0.286 | within noise |
| dense 10 x 30 sum_axis0 b512 / numpy | 9.024 (8.995-9.344) | 9.104 (8.985-9.235) | +0.9% | 9.004, 9.189, 9.048 / 9.11, 9.105, 9.074 | within noise |
| dense 10 x 30 sum_axis0 b512 / rust | 2.543 (2.479-2.57) | 2.552 (2.532-2.581) | +0.4% | 2.484, 2.563, 2.545 / 2.545, 2.551, 2.57 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 247.3 (243-256) | 243.5 (241.3-252.5) | -1.5% | 246.5, 251.7, 248.1 / 242.9, 244.8, 247.5 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 219.6 (209-221.9) | 249 (242.2-259.2) | +13.4% | 215.3, 219.6, 216.3 / 253.6, 246.1, 248.3 | consistent |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5544 (5423-5658) | 5547 (5401-5685) | +0.1% | 5541, 5559, 5515 / 5543, 5479, 5600 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 4059 (4013-4086) | 4253 (4190-4333) | +4.8% | 4056, 4042, 4062 / 4233, 4279, 4253 | consistent |
