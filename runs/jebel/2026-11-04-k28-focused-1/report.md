Old `5cf590a` against new `5cf590a`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --shape 5408 --shape 784 --shape attention --op forward_batch --op downstream_batch --op accumulate_gradient_batch --rust-threads 1 --openblas-threads 1 --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `238a017` (extension sha256 `bb3d5611c37d`) and new crate `18ce111` (extension sha256 `bc8a4a1fc83d`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.07; busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / attention 16 x 32 forward_batch b32 / rust -16.6% (316.6 -> 264.2 µs)
- consistent: per call / attention 16 x 32 forward_batch b512 / rust -12.9% (5857 -> 5099 µs)
- consistent: per call / attention 16 x 32 accumulate_gradient_batch b32 / rust +6.8% (108.5 -> 115.9 µs)
- consistent, small: per call / attention 16 x 32 accumulate_gradient_batch b512 / rust -1.5% (2134 -> 2102 µs)
- 32 rows within noise (8 separated inside their spread), max |Δ| 2.5%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward_batch b32 / numpy | 288.2 (286.3-294) | 287.9 (285.4-292.3) | -0.1% | 286.6, 292, 288.2 / 287.9, 287.1, 289 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 232.3 (228.9-238.1) | 235.2 (231.8-253.8) | +1.3% | 230.7, 232.7, 235.8 / 233.9, 233.9, 245.6 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 4172 (4128-4285) | 4233 (4134-4295) | +1.5% | 4167, 4172, 4216 / 4262, 4230, 4176 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 4550 (4537-4598) | 4519 (4499-4544) | -0.7% | 4550, 4571, 4556 / 4510, 4532, 4516 | separated, inside spread |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 258.2 (257.2-261) | 261.6 (259.6-269.2) | +1.3% | 257.4, 259.4, 259.2 / 261.1, 265.3, 262.1 | separated, inside spread |
| conv tail 32 x 5408 downstream_batch b32 / rust | 240.4 (238.2-246) | 242.4 (240.4-246.3) | +0.9% | 240.4, 242.1, 241.2 / 243.9, 242.4, 241.6 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 4067 (4055-4185) | 4074 (4065-4085) | +0.2% | 4060, 4083, 4126 / 4074, 4081, 4067 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 4398 (4324-4431) | 4412 (4387-4502) | +0.3% | 4364, 4373, 4425 / 4391, 4412, 4461 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 308.7 (306.1-314.8) | 315.5 (307.8-318.1) | +2.2% | 306.8, 312.7, 309.2 / 315.5, 317.4, 309.2 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 270.2 (267.2-275.2) | 272.2 (267.5-276.1) | +0.8% | 273.2, 271, 267.3 / 270, 272.5, 273.7 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 3914 (3889-3939) | 3928 (3898-3958) | +0.4% | 3889, 3914, 3939 / 3915, 3941, 3935 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 5306 (5262-5420) | 5373 (5269-5471) | +1.3% | 5343, 5375, 5264 / 5391, 5361, 5370 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 54.32 (53.83-55.01) | 54.69 (53.82-55.97) | +0.7% | 54.63, 53.98, 54.68 / 54.94, 54.69, 54.9 | separated, inside spread |
| dense 30 x 784 forward_batch b32 / rust | 35.01 (34.49-35.53) | 34.53 (33.95-35.06) | -1.4% | 35.01, 35.01, 34.95 / 34.3, 34.83, 34.22 | separated, inside spread |
| dense 30 x 784 forward_batch b512 / numpy | 637.9 (632.1-643.9) | 645.8 (638.1-686.5) | +1.2% | 635.2, 638.5, 640.7 / 647.4, 642.7, 662.3 | separated, inside spread |
| dense 30 x 784 forward_batch b512 / rust | 538.9 (535.3-551.2) | 534 (528.8-546.6) | -0.9% | 537.7, 550.8, 536.7 / 533.5, 531.5, 540.4 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 37.6 (36.99-37.96) | 37.82 (37.45-37.97) | +0.6% | 37.47, 37.49, 37.67 / 37.85, 37.71, 37.77 | separated, inside spread |
| dense 30 x 784 downstream_batch b32 / rust | 32.29 (31.94-32.75) | 32.29 (32.22-33.12) | +0.0% | 32.52, 32.11, 32.24 / 32.29, 32.53, 32.67 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 493.9 (490-507.1) | 494.6 (488.5-505.9) | +0.1% | 493.6, 491.7, 506.5 / 493.7, 500.5, 496.6 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 506.6 (499-518.5) | 516 (510.6-520.2) | +1.9% | 499.8, 513, 506.6 / 516, 519.7, 510.9 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 51.58 (50.78-52.58) | 52.14 (50.81-52.69) | +1.1% | 51.69, 51.79, 51.27 / 52.51, 51.3, 51.82 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 36.97 (36.77-38.09) | 37.89 (37.38-38.55) | +2.5% | 37.57, 36.88, 36.92 / 37.67, 38.18, 37.9 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 613.4 (603.9-623.6) | 617.6 (605-622.8) | +0.7% | 618.5, 608.7, 608.8 / 617.6, 617.9, 613.9 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 561.1 (554.4-584.3) | 567.7 (565.2-573.4) | +1.2% | 561.1, 563.6, 569.4 / 565.5, 570, 571 | within noise |
| relu 30 x 784 forward_batch b32 / numpy | 46.68 (46.08-47.17) | 46.91 (46.48-47.23) | +0.5% | 46.19, 46.86, 46.91 / 46.83, 47.09, 46.82 | within noise |
| relu 30 x 784 forward_batch b32 / rust | 32.17 (31.73-33.1) | 32.14 (31.19-32.54) | -0.1% | 32.65, 32.6, 31.86 / 32.08, 32.3, 31.86 | within noise |
| relu 30 x 784 forward_batch b512 / numpy | 555.4 (549.7-616.6) | 557 (552.5-564.5) | +0.3% | 555.4, 556.4, 583.2 / 564.5, 554.3, 556.8 | within noise |
| relu 30 x 784 forward_batch b512 / rust | 499.3 (490.1-555.4) | 496.8 (488.1-517) | -0.5% | 507.4, 492.9, 527 / 493.5, 496.8, 505.9 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 404.6 (396-406.1) | 405.5 (402.4-408.5) | +0.2% | 399.6, 406, 404.5 / 402.8, 405.5, 407.5 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 316.6 (313.8-319.5) | 264.2 (263.7-267.4) | -16.6% | 317, 315.3, 317.2 / 264, 264.1, 265.8 | consistent |
| attention 16 x 32 forward_batch b512 / numpy | 6160 (6112-6283) | 6172 (6127-6203) | +0.2% | 6152, 6137, 6222 / 6155, 6190, 6150 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 5857 (5803-5906) | 5099 (5089-5144) | -12.9% | 5886, 5852, 5825 / 5096, 5099, 5119 | consistent |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 282.2 (276.1-283.9) | 287 (280.7-290.8) | +1.7% | 280, 279.6, 282.6 / 288.3, 283.3, 287.8 | separated, inside spread |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 108.5 (107.9-110.7) | 115.9 (115.5-120.1) | +6.8% | 109.8, 108.8, 108.1 / 115.7, 115.7, 118.7 | consistent |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5691 (5593-5815) | 5747 (5586-5863) | +1.0% | 5645, 5715, 5695 / 5648, 5782, 5818 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 2134 (2115-2155) | 2102 (2085-2114) | -1.5% | 2135, 2133, 2144 / 2099, 2095, 2109 | consistent, small |
