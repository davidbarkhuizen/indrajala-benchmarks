Old `0b17d22` against new `0b17d22`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --shape 5408 --shape 784 --shape attention --op forward_batch --op downstream_batch --op accumulate_gradient_batch --rust-threads 1 --openblas-threads 1 --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `edce2de` (extension sha256 `f72612f402e8`) and new crate `51a2baf` (extension sha256 `7194f34f6ce9`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.21; busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- 36 rows within noise (2 separated inside their spread), max |Δ| 2.4%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward_batch b32 / numpy | 286.2 (283.6-296.1) | 288.9 (285.3-292.4) | +0.9% | 290.6, 284.3, 288.6 / 287.8, 288.8, 290 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 231.2 (225-238.2) | 231.6 (226.6-239.8) | +0.2% | 231.2, 230.2, 233.3 / 235.3, 229.5, 231.2 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 4248 (4175-4288) | 4214 (4164-4240) | -0.8% | 4283, 4199, 4226 / 4221, 4202, 4214 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 4522 (4488-4557) | 4521 (4503-4538) | -0.0% | 4504, 4514, 4546 / 4527, 4521, 4510 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 263.1 (256.7-271) | 260.6 (258-262.8) | -0.9% | 264, 259.7, 263.9 / 260.4, 258.9, 262.3 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 244.1 (240-249.8) | 243.3 (241.4-248.7) | -0.3% | 247.1, 240.2, 246.2 / 245, 244.3, 243.2 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 4078 (4054-4140) | 4066 (4053-4163) | -0.3% | 4059, 4072, 4123 / 4097, 4063, 4115 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 4398 (4373-4498) | 4398 (4373-4521) | +0.0% | 4381, 4494, 4398 / 4406, 4381, 4458 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 316.3 (309.8-321.8) | 313.6 (310.7-321.3) | -0.9% | 317.2, 312.3, 319.8 / 316, 312.3, 314.1 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 290.3 (286.8-293.2) | 289.6 (283.4-297.3) | -0.2% | 289, 289.4, 292.5 / 286.5, 286.7, 295.7 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 3901 (3882-3928) | 3908 (3878-3939) | +0.2% | 3905, 3887, 3913 / 3908, 3886, 3934 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 5265 (5176-5362) | 5210 (5162-5408) | -1.0% | 5328, 5180, 5265 / 5229, 5210, 5295 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 54.6 (53.67-55.94) | 54.69 (53.97-55) | +0.2% | 54.6, 53.85, 55.73 / 54.49, 54.79, 54.45 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 33.99 (33.03-34.96) | 34.4 (33.28-36.28) | +1.2% | 34.56, 33.17, 34.07 / 34.63, 33.41, 35.59 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 648.7 (639.4-662.9) | 633.3 (629.3-640.2) | -2.4% | 640.6, 658.8, 648.9 / 630.1, 635.1, 636.5 | separated, inside spread |
| dense 30 x 784 forward_batch b512 / rust | 539 (523.8-554) | 547.3 (523.4-574.6) | +1.5% | 535.7, 531.1, 547.6 / 548.3, 529.5, 562.9 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 37.42 (37.26-38) | 37.68 (37.25-38.06) | +0.7% | 37.6, 37.42, 37.63 / 37.49, 37.49, 37.92 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 32.91 (32.76-33.21) | 33.03 (31.82-33.44) | +0.4% | 32.92, 32.89, 32.98 / 33.1, 32.25, 33.37 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 491.5 (488.3-508.5) | 492.3 (489.3-507.1) | +0.2% | 497.2, 488.5, 498.7 / 496.6, 490.8, 498.2 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 513.3 (505.2-518.2) | 512.8 (495.8-522.1) | -0.1% | 511.7, 513.3, 511.5 / 507.5, 512.5, 514.5 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 51.83 (50.86-53.24) | 51.12 (50.74-52.77) | -1.4% | 51.48, 51.47, 52.77 / 51.76, 51.12, 51.34 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 40.06 (39.04-40.67) | 39.93 (39.11-40.53) | -0.3% | 40.38, 39.27, 40.22 / 40.24, 39.48, 39.97 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 613.5 (605.2-623.7) | 605 (603.9-623.7) | -1.4% | 609.7, 614.3, 618.4 / 614.2, 604.8, 608.5 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 575.7 (560.3-580.4) | 574.9 (568.1-594.3) | -0.1% | 576.1, 566.7, 577.9 / 572.5, 572.3, 585.5 | within noise |
| relu 30 x 784 forward_batch b32 / numpy | 46.58 (45.91-47.5) | 46.27 (45.71-47.58) | -0.7% | 46.58, 45.92, 47.24 / 46.84, 46.08, 46.11 | within noise |
| relu 30 x 784 forward_batch b32 / rust | 31.71 (31.07-32.45) | 31.38 (30.44-32.23) | -1.0% | 31.98, 31.12, 32.01 / 30.9, 31.18, 32.19 | within noise |
| relu 30 x 784 forward_batch b512 / numpy | 558.7 (552.4-589.2) | 553.5 (550.1-562.6) | -0.9% | 555.5, 570.8, 564.8 / 551.4, 557.9, 556.3 | within noise |
| relu 30 x 784 forward_batch b512 / rust | 493.1 (486.7-522.1) | 504.2 (486.7-514.8) | +2.2% | 489.2, 506.5, 502.8 / 500.5, 508.2, 504.2 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 402.2 (398.2-409.5) | 400.1 (397.7-404.6) | -0.5% | 399.4, 402.4, 407.2 / 400.4, 401.2, 399.8 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 262.6 (261.7-263.9) | 263.6 (260.7-267.2) | +0.4% | 262.6, 261.8, 263.6 / 264, 262.9, 264.4 | within noise |
| attention 16 x 32 forward_batch b512 / numpy | 6152 (6125-6181) | 6131 (6116-6144) | -0.3% | 6162, 6133, 6165 / 6131, 6128, 6132 | separated, inside spread |
| attention 16 x 32 forward_batch b512 / rust | 5085 (5069-5132) | 5099 (5078-5122) | +0.3% | 5085, 5072, 5119 / 5095, 5093, 5108 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 282.5 (275.8-286.9) | 282 (275.8-287.4) | -0.2% | 282.5, 276.4, 286.8 / 281.6, 284.5, 278.8 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 108.5 (106-109.2) | 109.5 (107.4-117.3) | +1.0% | 108.5, 106.7, 109.2 / 113.8, 107.5, 109.6 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5613 (5562-5704) | 5608 (5581-5835) | -0.1% | 5653, 5592, 5646 / 5757, 5602, 5592 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 2135 (2105-2157) | 2141 (2074-2175) | +0.3% | 2130, 2115, 2152 / 2160, 2108, 2129 | within noise |
