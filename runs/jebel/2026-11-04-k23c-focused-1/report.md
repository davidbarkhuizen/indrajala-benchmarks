Old `bb60c11` against new `bb60c11`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --shape 5408 --shape 784 --shape attention --op forward_batch --op downstream_batch --op accumulate_gradient_batch --rust-threads 1 --openblas-threads 1 --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `10aa3e5` (extension sha256 `24bdf26aceef`) and new crate `3bb2a40` (extension sha256 `bb3d5611c37d`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.30; busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / attention 16 x 32 accumulate_gradient_batch b32 / rust -34.8% (166.4 -> 108.6 µs)
- consistent: per call / attention 16 x 32 accumulate_gradient_batch b512 / rust -33.2% (3191 -> 2131 µs)
- 34 rows within noise (7 separated inside their spread), max |Δ| 2.9%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward_batch b32 / numpy | 289.9 (285.1-291.9) | 291.8 (284.4-292.6) | +0.6% | 288.2, 287.8, 290.9 / 288, 288.4, 292.6 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 231.5 (229.6-237.3) | 226.6 (225.6-235.7) | -2.1% | 229.7, 231.5, 235.2 / 226.4, 233.3, 226 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 4210 (4129-4247) | 4201 (4166-4237) | -0.2% | 4172, 4232, 4184 / 4204, 4225, 4174 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 4541 (4494-4576) | 4529 (4497-4540) | -0.3% | 4512, 4541, 4564 / 4534, 4520, 4517 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 259.3 (255.4-265.4) | 256.1 (255.5-258.9) | -1.2% | 260.2, 256.1, 263.1 / 256.1, 257.4, 256.4 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 241.1 (237.8-246.1) | 237.9 (236.6-239.4) | -1.3% | 239, 241.6, 243.4 / 238, 238.4, 237.2 | separated, inside spread |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 4066 (4056-4075) | 4069 (4058-4096) | +0.1% | 4062, 4066, 4066 / 4067, 4064, 4082 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 4384 (4359-4398) | 4388 (4340-4394) | +0.1% | 4384, 4382, 4378 / 4364, 4389, 4388 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 312.3 (306.6-321.5) | 309 (306.3-311.3) | -1.1% | 312.3, 306.6, 319.5 / 307.3, 311, 308.6 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 272 (265.7-273.5) | 267.3 (265.5-271.6) | -1.7% | 269.6, 269.2, 273 / 266.4, 269, 269.4 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 3915 (3885-3945) | 3893 (3885-3907) | -0.6% | 3891, 3915, 3939 / 3888, 3898, 3898 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 5286 (5210-5316) | 5221 (5113-5296) | -1.2% | 5258, 5262, 5301 / 5247, 5204, 5201 | separated, inside spread |
| dense 30 x 784 forward_batch b32 / numpy | 53.95 (53.48-55.27) | 54.27 (53.75-54.43) | +0.6% | 53.94, 53.76, 54.65 / 54.07, 54.27, 54.25 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 35.22 (34.38-35.55) | 34.68 (34.39-36.07) | -1.5% | 35.04, 34.76, 35.49 / 34.54, 35.23, 35.05 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 636.8 (633-646.1) | 636.5 (631.5-641.1) | -0.1% | 638.1, 633.7, 642.6 / 635.5, 636.5, 636.6 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 550.1 (536.5-555.6) | 544.8 (536.2-607.1) | -1.0% | 541, 549.3, 555.1 / 544.8, 543.9, 571.7 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 37.49 (37.12-37.93) | 37.17 (36.95-37.66) | -0.9% | 37.38, 37.43, 37.7 / 37.04, 37.58, 37.09 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 32.1 (31.62-32.97) | 32.78 (32.1-32.94) | +2.1% | 32.1, 32.3, 32.22 / 32.94, 32.44, 32.75 | separated, inside spread |
| dense 30 x 784 downstream_batch b512 / numpy | 491.2 (488-496.5) | 490.3 (488.2-502.1) | -0.2% | 492.4, 491.2, 491.2 / 492, 497, 488.3 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 511.7 (469.6-521) | 513.8 (506.7-515.9) | +0.4% | 489.1, 514.9, 515.2 / 513.4, 510.5, 513.8 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 51.49 (50.66-52.86) | 51.18 (50.56-51.99) | -0.6% | 51.42, 50.86, 52.7 / 51.18, 51.27, 51.05 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 37.49 (36.9-38.17) | 37.01 (36.78-37.16) | -1.3% | 37.87, 37.16, 37.56 / 36.93, 37.01, 37.03 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 604.3 (603.6-622.7) | 604.7 (604-613.5) | +0.1% | 603.9, 604.1, 618.2 / 604.3, 608.5, 609.2 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 559.9 (555.5-570.1) | 559.4 (554.6-571.2) | -0.1% | 559.8, 561.5, 563.9 / 559.9, 557.1, 562.9 | within noise |
| relu 30 x 784 forward_batch b32 / numpy | 46.6 (45.81-46.78) | 46.09 (45.71-46.6) | -1.1% | 46.64, 46.23, 46.33 / 46.22, 46.15, 46.09 | separated, inside spread |
| relu 30 x 784 forward_batch b32 / rust | 32.64 (32.03-33.16) | 32.41 (32.11-32.51) | -0.7% | 32.85, 32.37, 32.64 / 32.42, 32.34, 32.31 | within noise |
| relu 30 x 784 forward_batch b512 / numpy | 558.5 (552.4-565.3) | 554.1 (549.6-557.7) | -0.8% | 559.2, 558.5, 556.8 / 556.3, 553, 551.6 | separated, inside spread |
| relu 30 x 784 forward_batch b512 / rust | 506.7 (490.9-524) | 508.7 (500.9-513.7) | +0.4% | 500.3, 499.7, 520 / 504.5, 505.2, 511.5 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 405.2 (397.3-407.9) | 398.3 (396.9-404.4) | -1.7% | 407.6, 397.9, 405.2 / 398.3, 400.9, 397.8 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 315.6 (314.8-317.5) | 315.6 (314.1-318.3) | +0.0% | 317.1, 315.4, 315.1 / 315, 315.8, 316.2 | within noise |
| attention 16 x 32 forward_batch b512 / numpy | 6149 (6107-6195) | 6135 (6094-6220) | -0.2% | 6175, 6113, 6160 / 6116, 6124, 6185 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 5846 (5815-5897) | 5828 (5775-5870) | -0.3% | 5866, 5837, 5846 / 5805, 5854, 5811 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 281.6 (270.7-289.1) | 280.9 (275.5-286.3) | -0.3% | 277, 281.3, 283.9 / 281.4, 282.9, 278.7 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 166.4 (163.8-172.5) | 108.6 (108.1-111.4) | -34.8% | 170.6, 166.4, 164 / 108.5, 109, 109.7 | consistent |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5758 (5617-5869) | 5591 (5571-5609) | -2.9% | 5758, 5625, 5858 / 5591, 5601, 5579 | separated, inside spread |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 3191 (3133-3302) | 2131 (2123-2149) | -33.2% | 3191, 3198, 3240 / 2131, 2142, 2126 | consistent |
