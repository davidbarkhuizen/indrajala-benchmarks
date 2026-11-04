Old `515849f` against new `515849f`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --shape 5408 --shape 784 --shape attention --op forward_batch --op downstream_batch --op accumulate_gradient_batch --rust-threads 1 --openblas-threads 1 --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `cba601e` (extension sha256 `bc8a4a1fc83d`) and new crate `dc571a0` (extension sha256 `1cebe6ff7934`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.59 (HIGH); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- 36 rows within noise (6 separated inside their spread), max |Δ| 2.1%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward_batch b32 / numpy | 289.6 (285.9-291) | 288.2 (284.8-294.2) | -0.5% | 289.5, 290.2, 287.5 / 287.6, 289.5, 289.4 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 228.1 (225.1-232.6) | 230 (225.3-250.8) | +0.8% | 225.2, 228.1, 230.9 / 226.9, 230.3, 241.1 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 4252 (4136-4287) | 4185 (4149-4205) | -1.6% | 4214, 4209, 4260 / 4201, 4187, 4151 | separated, inside spread |
| conv tail 32 x 5408 forward_batch b512 / rust | 4515 (4483-4550) | 4501 (4487-4565) | -0.3% | 4521, 4497, 4523 / 4494, 4499, 4554 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 258.5 (255-260) | 258.5 (255.2-265.3) | +0.0% | 256.6, 259.4, 258.8 / 257.1, 257.8, 262.5 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 242 (238.9-249.7) | 239.2 (236.8-242.6) | -1.2% | 239.8, 243.3, 246.6 / 239.9, 236.8, 241.5 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 4068 (4060-4193) | 4154 (4072-4191) | +2.1% | 4065, 4126, 4127 / 4107, 4143, 4178 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 4383 (4341-4524) | 4391 (4374-4498) | +0.2% | 4361, 4376, 4456 / 4390, 4444, 4396 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 308.4 (304.8-318.6) | 307.9 (306.7-319) | -0.1% | 311.7, 306.3, 311.7 / 311.9, 307.5, 312.8 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 267.7 (267-268.9) | 269.9 (267.6-279.3) | +0.8% | 267.9, 267.9, 267.7 / 268.7, 269.4, 277.4 | separated, inside spread |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 3912 (3886-3962) | 3919 (3896-3992) | +0.2% | 3892, 3923, 3946 / 3898, 3919, 3974 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 5305 (5235-5326) | 5320 (5264-5388) | +0.3% | 5284, 5305, 5280 / 5348, 5317, 5326 | separated, inside spread |
| dense 30 x 784 forward_batch b32 / numpy | 54.55 (53.93-55.74) | 54.42 (53.51-55.06) | -0.2% | 54.41, 54.28, 55.28 / 54.12, 54.48, 54.58 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 34.27 (33.92-35.55) | 34.89 (34.04-35.73) | +1.8% | 35.45, 34.25, 33.98 / 34.44, 35.04, 35.04 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 646.6 (635.8-675.2) | 639.4 (631.4-647.6) | -1.1% | 655.5, 644.1, 646.8 / 636, 637.2, 647 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 536.9 (527.2-545.8) | 537.7 (532.9-550.5) | +0.1% | 533.2, 539.4, 539.8 / 536.6, 534.6, 545.8 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 37.34 (37-37.93) | 37.22 (37-37.77) | -0.3% | 37.6, 37.12, 37.53 / 37.38, 37.11, 37.44 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 32.67 (31.96-32.97) | 32.75 (31.82-33.58) | +0.2% | 32.12, 32.84, 32.78 / 32.65, 32.33, 33.38 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 493.4 (492.1-514.4) | 496.1 (489.9-507.3) | +0.5% | 492.7, 493.3, 505.7 / 496.7, 498.6, 496.1 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 514.4 (507.7-522.5) | 516.9 (512.9-529.7) | +0.5% | 512, 518.1, 513.4 / 516.9, 513.2, 526.5 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 51.13 (50.96-51.84) | 51.11 (50.63-52.41) | -0.0% | 51.54, 50.99, 51.28 / 51.11, 50.93, 51.62 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 37.13 (37-37.78) | 37.78 (37.02-38.1) | +1.7% | 37.52, 37.16, 37 / 37.14, 37.78, 38.04 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 604.3 (603.5-612.7) | 608.9 (603.8-623.6) | +0.8% | 608.5, 603.8, 608.4 / 613.7, 608.7, 613.8 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 567.2 (559-587.1) | 569.7 (563.3-582.4) | +0.4% | 562.2, 564.3, 586.6 / 566, 572.6, 574.1 | within noise |
| relu 30 x 784 forward_batch b32 / numpy | 46.24 (45.79-46.6) | 46.2 (45.59-47.48) | -0.1% | 46.46, 45.9, 46.33 / 46.21, 46.2, 46.53 | within noise |
| relu 30 x 784 forward_batch b32 / rust | 31.69 (31.39-32.19) | 31.93 (31.53-32.88) | +0.8% | 31.64, 31.57, 31.91 / 31.59, 31.9, 32.8 | within noise |
| relu 30 x 784 forward_batch b512 / numpy | 557.3 (547-584.3) | 558.1 (551.5-572.4) | +0.2% | 550.9, 568.3, 562.1 / 560.4, 551.6, 566.1 | within noise |
| relu 30 x 784 forward_batch b512 / rust | 494.4 (486.6-512.3) | 496.2 (489.3-508.1) | +0.4% | 491.4, 492.6, 503.2 / 500.5, 490.1, 503 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 399.2 (398.1-406.8) | 399.5 (398.7-406.9) | +0.1% | 401.2, 398.8, 402.4 / 403, 399.2, 402.8 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 263.2 (261.9-267.3) | 261.8 (259.7-263.1) | -0.6% | 262.1, 265.3, 263.7 / 261.5, 261.4, 261.8 | separated, inside spread |
| attention 16 x 32 forward_batch b512 / numpy | 6124 (6111-6195) | 6156 (6088-6218) | +0.5% | 6118, 6117, 6188 / 6133, 6204, 6131 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 5079 (5070-5098) | 5053 (5047-5098) | -0.5% | 5084, 5079, 5083 / 5059, 5052, 5074 | separated, inside spread |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 281 (277.8-286.5) | 283.7 (279-298.1) | +0.9% | 281.4, 282.1, 280.7 / 283.3, 290.9, 281.6 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 115.7 (114.5-117.6) | 116 (114.2-116.8) | +0.3% | 115.4, 115.9, 116.1 / 114.7, 116, 116.5 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5678 (5574-5808) | 5629 (5600-5826) | -0.9% | 5684, 5586, 5760 / 5657, 5624, 5713 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 2070 (2049-2083) | 2067 (2054-2097) | -0.1% | 2080, 2054, 2070 / 2065, 2067, 2075 | within noise |
