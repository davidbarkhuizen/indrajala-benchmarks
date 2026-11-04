Old `0d91d1a` against new `0d91d1a`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --matmul 2048x512x512 --matmul 2048x2048x512 --matmul 512x2048x2048 --matmul 2048x512x2048 --matmul 2048x256x64 --matmul 2048x2048x64 --matmul 64x256x1024 --matmul 32x512x5408 --matmul 30x512x784 --matmul 8x2048x64 --only-matmul --rust-threads 1 --openblas-threads 1 --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `6a8190c` (extension sha256 `84ec4e85d91b`) and new crate `7b9878f` (extension sha256 `21b07c2bef84`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.80 (HIGH); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / matmul 512x2048x2048 bare matmul / rust -68.8% (2.868e+05 -> 8.942e+04 µs)
- consistent: per call / matmul 2048x512x2048 bare matmul / rust -67.7% (3.247e+05 -> 1.048e+05 µs)
- consistent: per call / matmul 2048x2048x512 bare matmul / rust -65.1% (2.53e+05 -> 8.843e+04 µs)
- consistent: per call / matmul 2048x512x512 bare matmul / rust -54.7% (5.346e+04 -> 2.42e+04 µs)
- consistent: per call / matmul 2048x2048x64 bare matmul / rust -50.3% (2.306e+04 -> 1.145e+04 µs)
- consistent: per call / matmul 64x256x1024 bare matmul / rust -46.7% (1415 -> 754.6 µs)
- consistent: per call / matmul 2048x256x64 bare matmul / rust -25.8% (1534 -> 1138 µs)
- 13 rows within noise (3 separated inside their spread), max |Δ| 1.2%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| matmul 2048x512x512 bare matmul / numpy | 1.678e+04 (1.648e+04-1.706e+04) | 1.672e+04 (1.654e+04-1.697e+04) | -0.4% | 1.656e+04, 1.678e+04, 1.703e+04 / 1.686e+04, 1.672e+04, 1.662e+04 | within noise |
| matmul 2048x512x512 bare matmul / rust | 5.346e+04 (5.31e+04-5.618e+04) | 2.42e+04 (2.412e+04-2.445e+04) | -54.7% | 5.327e+04, 5.435e+04, 5.464e+04 / 2.416e+04, 2.416e+04, 2.434e+04 | consistent |
| matmul 2048x2048x512 bare matmul / numpy | 6.644e+04 (6.478e+04-6.799e+04) | 6.662e+04 (6.604e+04-6.783e+04) | +0.3% | 6.491e+04, 6.757e+04, 6.644e+04 / 6.75e+04, 6.618e+04, 6.662e+04 | within noise |
| matmul 2048x2048x512 bare matmul / rust | 2.53e+05 (2.314e+05-2.704e+05) | 8.843e+04 (8.571e+04-9.057e+04) | -65.1% | 2.432e+05, 2.595e+05, 2.552e+05 / 8.903e+04, 8.843e+04, 8.802e+04 | consistent |
| matmul 512x2048x2048 bare matmul / numpy | 6.636e+04 (6.485e+04-6.734e+04) | 6.718e+04 (6.603e+04-6.832e+04) | +1.2% | 6.486e+04, 6.641e+04, 6.683e+04 / 6.751e+04, 6.717e+04, 6.684e+04 | separated, inside spread |
| matmul 512x2048x2048 bare matmul / rust | 2.868e+05 (2.767e+05-3.077e+05) | 8.942e+04 (8.753e+04-9.074e+04) | -68.8% | 2.866e+05, 2.895e+05, 2.922e+05 / 8.967e+04, 8.936e+04, 8.914e+04 | consistent |
| matmul 2048x512x2048 bare matmul / numpy | 6.801e+04 (6.659e+04-6.819e+04) | 6.84e+04 (6.773e+04-6.928e+04) | +0.6% | 6.699e+04, 6.808e+04, 6.81e+04 / 6.85e+04, 6.829e+04, 6.84e+04 | separated, inside spread |
| matmul 2048x512x2048 bare matmul / rust | 3.247e+05 (2.621e+05-3.512e+05) | 1.048e+05 (1.038e+05-1.057e+05) | -67.7% | 3.045e+05, 2.982e+05, 3.371e+05 / 1.048e+05, 1.044e+05, 1.053e+05 | consistent |
| matmul 2048x256x64 bare matmul / numpy | 1175 (1155-1190) | 1180 (1160-1204) | +0.4% | 1162, 1183, 1175 / 1164, 1198, 1180 | within noise |
| matmul 2048x256x64 bare matmul / rust | 1534 (1502-1602) | 1138 (1134-1183) | -25.8% | 1534, 1559, 1522 / 1136, 1159, 1159 | consistent |
| matmul 2048x2048x64 bare matmul / numpy | 1.013e+04 (1.003e+04-1.03e+04) | 1.009e+04 (9967-1.016e+04) | -0.4% | 1.016e+04, 1.013e+04, 1.013e+04 / 1.006e+04, 1.006e+04, 1.011e+04 | separated, inside spread |
| matmul 2048x2048x64 bare matmul / rust | 2.306e+04 (2.27e+04-2.357e+04) | 1.145e+04 (1.06e+04-1.214e+04) | -50.3% | 2.285e+04, 2.31e+04, 2.335e+04 / 1.116e+04, 1.145e+04, 1.164e+04 | consistent |
| matmul 64x256x1024 bare matmul / numpy | 605.5 (599.5-609) | 608.5 (596.9-611.6) | +0.5% | 603.4, 606.3, 605.5 / 600.4, 608.5, 611 | within noise |
| matmul 64x256x1024 bare matmul / rust | 1415 (1382-2340) | 754.6 (751.4-757.2) | -46.7% | 1398, 1415, 1885 / 754.7, 753.8, 754.6 | consistent |
| matmul 32x512x5408 bare matmul / numpy | 3813 (3777-3820) | 3816 (3778-3824) | +0.1% | 3778, 3816, 3817 / 3822, 3796, 3806 | within noise |
| matmul 32x512x5408 bare matmul / rust | 4931 (4899-4943) | 4917 (4864-4941) | -0.3% | 4921, 4938, 4928 / 4925, 4890, 4930 | within noise |
| matmul 30x512x784 bare matmul / numpy | 585.4 (584.8-601.7) | 585.1 (584.4-602.7) | -0.0% | 585.2, 593.4, 589.2 / 584.5, 585.1, 597.9 | within noise |
| matmul 30x512x784 bare matmul / rust | 532 (529.5-539.4) | 534.1 (530.3-539.2) | +0.4% | 530.7, 534.8, 532.6 / 535.1, 532.8, 534.2 | within noise |
| matmul 8x2048x64 bare matmul / numpy | 73.13 (72.32-74.55) | 73.73 (71.89-74.97) | +0.8% | 72.87, 73.43, 73.4 / 74.04, 72.22, 74.34 | within noise |
| matmul 8x2048x64 bare matmul / rust | 55.2 (54.91-56.33) | 55.51 (55.35-57.2) | +0.6% | 55.05, 55.92, 55.14 / 56.89, 55.42, 55.45 | within noise |
