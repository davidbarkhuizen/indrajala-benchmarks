Old `25a3a03` against new `a6419a6`, run with `scripts/ab.py`: passes in the order ONNOONNO. Each pass ran `python scripts/focused_benchmark.py --backend rust --shape dense 10 x 30 --shape dense 30 x 784 --batch-sizes 1 --passes 1 --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree. Machine check: profile: not recorded; busy processes: none. Each row pools 4 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- shifted: pass 1 (old, fast -13.5%), pass 2 (new, fast -11.6%); balanced
- 30 rows within noise, max |Δ| 20.0%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 5, 8) / new (2, 3, 6, 7) | verdict |
|---|---|---|---|---|---|
| dense 30 x 784 forward / rust | 4.343 (3.781-4.501) | 4.138 (3.567-4.257) | -4.7% | 3.781, 4.501, 4.317, 4.37 / 3.567, 4.038, 4.257, 4.239 | within noise |
| dense 30 x 784 downstream / rust | 4.017 (3.36-4.083) | 3.707 (3.261-3.94) | -7.7% | 3.36, 3.984, 4.051, 4.083 / 3.261, 3.644, 3.77, 3.94 | within noise |
| dense 30 x 784 hidden_delta / rust | 4.426 (3.816-4.796) | 4.284 (4.109-4.43) | -3.2% | 3.816, 4.416, 4.435, 4.796 / 4.109, 4.199, 4.43, 4.37 | within noise |
| dense 30 x 784 accumulate_gradient / rust | 8.935 (8.429-10.99) | 8.091 (6.799-8.65) | -9.5% | 8.775, 8.429, 10.99, 9.096 / 6.799, 8.067, 8.65, 8.114 | within noise |
| dense 30 x 784 apply_accumulated_gradient / rust | 22.24 (20.89-24.71) | 22.33 (18.38-23.86) | +0.4% | 20.89, 21.85, 24.71, 22.64 / 18.38, 20.84, 23.83, 23.86 | within noise |
| dense 30 x 784 sgd step / rust | 10.05 (8.282-10.18) | 9.681 (8.112-10.21) | -3.6% | 8.282, 10.18, 10.16, 9.929 / 8.112, 9.429, 10.21, 9.933 | within noise |
| dense 30 x 784 forward_batch b1 / rust | 4.35 (3.772-5.06) | 4.234 (3.75-4.434) | -2.7% | 3.772, 4.293, 5.06, 4.406 / 3.75, 4.107, 4.36, 4.434 | within noise |
| dense 30 x 784 downstream_batch b1 / rust | 4.003 (3.262-4.238) | 3.826 (3.244-4.389) | -4.4% | 3.262, 3.872, 4.238, 4.133 / 3.244, 3.656, 4.389, 3.995 | within noise |
| dense 30 x 784 hidden_delta_batch b1 / rust | 4.69 (4.17-4.85) | 4.236 (3.896-4.467) | -9.7% | 4.17, 4.546, 4.85, 4.834 / 3.896, 4.107, 4.366, 4.467 | within noise |
| dense 30 x 784 accumulate_gradient_batch b1 / rust | 14.19 (11.91-18.46) | 13.58 (11.98-14) | -4.3% | 11.91, 13.69, 18.46, 14.69 / 11.98, 13.35, 13.8, 14 | within noise |
| dense 10 x 30 forward / rust | 0.8251 (0.7878-0.8789) | 0.8048 (0.7177-0.8156) | -2.5% | 0.7964, 0.7878, 0.8789, 0.8539 / 0.7177, 0.8053, 0.8156, 0.8043 | within noise |
| dense 10 x 30 downstream / rust | 0.5561 (0.489-0.5675) | 0.4519 (0.399-0.54) | -18.7% | 0.489, 0.5675, 0.5458, 0.5663 / 0.399, 0.4715, 0.54, 0.4324 | within noise |
| dense 10 x 30 hidden_delta / rust | 0.7666 (0.6269-0.7792) | 0.7072 (0.5979-0.7418) | -7.7% | 0.6269, 0.7792, 0.7565, 0.7766 / 0.5979, 0.6735, 0.741, 0.7418 | within noise |
| dense 10 x 30 accumulate_gradient / rust | 1.068 (0.9854-1.249) | 0.9303 (0.8547-1.042) | -12.9% | 0.9854, 1.249, 1.04, 1.095 / 0.8547, 0.9521, 0.9085, 1.042 | within noise |
| dense 10 x 30 apply_accumulated_gradient / rust | 2.256 (1.948-2.673) | 1.925 (1.817-2.342) | -14.6% | 1.948, 2.313, 2.199, 2.673 / 1.942, 1.817, 1.909, 2.342 | within noise |
| dense 10 x 30 sgd step / rust | 1.135 (0.9457-1.167) | 0.9289 (0.8747-1.047) | -18.1% | 0.9457, 1.104, 1.166, 1.167 / 0.8936, 0.8747, 0.9642, 1.047 | within noise |
| dense 10 x 30 forward_batch b1 / rust | 0.91 (0.7842-0.942) | 0.8132 (0.7094-0.8792) | -10.6% | 0.7842, 0.8933, 0.9268, 0.942 / 0.7094, 0.8074, 0.8189, 0.8792 | within noise |
| dense 10 x 30 downstream_batch b1 / rust | 0.5383 (0.444-0.5815) | 0.4793 (0.4548-0.5062) | -11.0% | 0.444, 0.5815, 0.5223, 0.5543 / 0.4637, 0.4949, 0.5062, 0.4548 | within noise |
| dense 10 x 30 hidden_delta_batch b1 / rust | 0.7829 (0.6685-0.7861) | 0.6734 (0.6168-0.6834) | -14.0% | 0.6685, 0.7833, 0.7861, 0.7825 / 0.6168, 0.6738, 0.673, 0.6834 | within noise |
| dense 10 x 30 accumulate_gradient_batch b1 / rust | 1.29 (1.212-1.305) | 1.304 (1.125-1.369) | +1.1% | 1.212, 1.278, 1.305, 1.303 / 1.125, 1.369, 1.299, 1.309 | within noise |
| dense 30 x 784 bare downstream b1 / rust | 3.635 (3.194-3.749) | 3.569 (3.186-3.768) | -1.8% | 3.194, 3.65, 3.62, 3.749 / 3.186, 3.555, 3.584, 3.768 | within noise |
| dense 30 x 784 bare accumulate b1 / rust | 9.666 (8.339-9.825) | 9.553 (8.639-9.958) | -1.2% | 8.339, 9.536, 9.825, 9.796 / 8.639, 9.543, 9.563, 9.958 | within noise |
| dense 30 x 784 transpose b1 / rust | 0.3481 (0.2778-0.3657) | 0.3095 (0.2838-0.3517) | -11.1% | 0.2778, 0.3511, 0.3657, 0.3452 / 0.2838, 0.2906, 0.3283, 0.3517 | within noise |
| dense 30 x 784 add b1 / rust | 7.891 (6.145-9.495) | 7.622 (6.046-8.264) | -3.4% | 6.145, 7.786, 7.996, 9.495 / 6.046, 7.613, 7.631, 8.264 | within noise |
| dense 30 x 784 sum_axis0 b1 / rust | 0.3472 (0.3065-0.3758) | 0.296 (0.2412-0.3266) | -14.8% | 0.3065, 0.3446, 0.3758, 0.3498 / 0.2412, 0.2796, 0.3266, 0.3125 | within noise |
| dense 10 x 30 bare downstream b1 / rust | 0.4034 (0.3299-0.4147) | 0.3226 (0.306-0.3614) | -20.0% | 0.3299, 0.4101, 0.4147, 0.3968 / 0.3176, 0.3277, 0.306, 0.3614 | within noise |
| dense 10 x 30 bare accumulate b1 / rust | 0.645 (0.5605-0.6477) | 0.5673 (0.5269-0.5882) | -12.0% | 0.5605, 0.6451, 0.6449, 0.6477 / 0.5269, 0.582, 0.5882, 0.5526 | within noise |
| dense 10 x 30 transpose b1 / rust | 0.2696 (0.2636-0.2805) | 0.2551 (0.2103-0.274) | -5.4% | 0.2659, 0.2636, 0.2733, 0.2805 / 0.2103, 0.2469, 0.2632, 0.274 | within noise |
| dense 10 x 30 add b1 / rust | 0.4082 (0.3677-0.4343) | 0.3388 (0.3315-0.3686) | -17.0% | 0.3677, 0.421, 0.4343, 0.3954 / 0.3357, 0.3315, 0.3686, 0.342 | within noise |
| dense 10 x 30 sum_axis0 b1 / rust | 0.3204 (0.3014-0.35) | 0.31 (0.2493-0.3531) | -3.2% | 0.3014, 0.35, 0.3251, 0.3156 / 0.2493, 0.3123, 0.3077, 0.3531 | within noise |
