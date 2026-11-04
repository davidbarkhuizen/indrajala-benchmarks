Old `515849f` against new `515849f`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --shape 5408 --shape 784 --shape attention --op forward_batch --op downstream_batch --op accumulate_gradient_batch --rust-threads 1 --openblas-threads 1 --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `cba601e` (extension sha256 `bc8a4a1fc83d`) and new crate `480cebc` (extension sha256 `5b3d1d17cea4`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.98; busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- 36 rows within noise (4 separated inside their spread), max |Δ| 2.0%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward_batch b32 / numpy | 288.6 (283.9-294.1) | 287.8 (286.3-293.5) | -0.3% | 286.8, 292.3, 286.7 / 290.7, 288, 286.5 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 229.8 (225.6-236.5) | 226.5 (225.5-229.5) | -1.4% | 227.1, 234.2, 229.2 / 228.1, 225.9, 227.5 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 4217 (4176-4291) | 4193 (4158-4265) | -0.6% | 4234, 4241, 4192 / 4171, 4233, 4199 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 4487 (4482-4524) | 4507 (4497-4593) | +0.4% | 4487, 4505, 4496 / 4516, 4501, 4546 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 258.4 (256.4-264.9) | 257.7 (257.1-264.5) | -0.3% | 259.8, 261.4, 257.7 / 258.6, 260.8, 257.4 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 241.1 (238.3-245.4) | 240.2 (235.9-244.8) | -0.4% | 239, 244.4, 241.1 / 240.3, 237.5, 242.7 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 4113 (4061-4188) | 4080 (4062-4092) | -0.8% | 4062, 4169, 4129 / 4080, 4077, 4074 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 4392 (4325-4501) | 4391 (4379-4503) | -0.0% | 4361, 4483, 4380 / 4391, 4388, 4443 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 308.2 (307-316.1) | 309.1 (305.3-312.5) | +0.3% | 311.9, 310.7, 307.4 / 311.9, 309, 306.2 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 268.8 (265.2-273.2) | 266.3 (264.8-269.3) | -0.9% | 272.3, 268.9, 265.9 / 267.6, 267.3, 265.8 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 3904 (3888-3966) | 3896 (3885-3914) | -0.2% | 3892, 3926, 3934 / 3903, 3902, 3889 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 5244 (5179-5390) | 5261 (5224-5397) | +0.3% | 5309, 5185, 5299 / 5256, 5244, 5334 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 54.2 (53.73-54.6) | 53.81 (53.58-55.24) | -0.7% | 54.16, 54.31, 54.13 / 53.93, 54.55, 53.67 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 34.07 (33.55-34.42) | 34.52 (33.63-35.15) | +1.3% | 34.09, 33.98, 33.99 / 34.09, 34.63, 34.39 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 640.1 (633.9-666.5) | 635.4 (633.3-638.6) | -0.7% | 654.7, 637.6, 637.6 / 635.1, 634.7, 636.6 | separated, inside spread |
| dense 30 x 784 forward_batch b512 / rust | 533.3 (524.5-536) | 533.3 (520.4-546.8) | -0.0% | 524.6, 534.6, 534 / 543.4, 529.4, 527.3 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 37.31 (37.15-37.48) | 37.14 (37.11-37.23) | -0.5% | 37.32, 37.22, 37.38 / 37.14, 37.17, 37.15 | separated, inside spread |
| dense 30 x 784 downstream_batch b32 / rust | 32.54 (31.73-32.73) | 32.48 (31.85-32.88) | -0.2% | 32.2, 32.65, 32.19 / 32.5, 32.1, 32.64 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 500 (489.4-504.2) | 500.6 (494.4-503.4) | +0.1% | 494.1, 497.9, 502.8 / 500.8, 500.6, 498.1 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 510.2 (506.2-514.4) | 505.6 (487.8-509.9) | -0.9% | 509.8, 510.6, 510.2 / 496, 504.7, 508.8 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 50.79 (50.6-52.05) | 51 (50.8-51.07) | +0.4% | 51, 50.65, 51.35 / 50.93, 51, 50.99 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 37.21 (36.71-39.52) | 36.81 (36.65-37.15) | -1.1% | 38.48, 37.33, 36.77 / 36.94, 36.81, 36.76 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 604 (603.7-604.4) | 604.1 (604-605) | +0.0% | 603.9, 604, 604.1 / 604.3, 604.1, 604.5 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 564 (554.9-573.3) | 556 (555.3-564.4) | -1.4% | 569.7, 564.9, 555.6 / 559.8, 556.6, 555.6 | within noise |
| relu 30 x 784 forward_batch b32 / numpy | 46 (45.5-46.7) | 46.09 (45.62-46.63) | +0.2% | 46.1, 45.89, 46 / 45.86, 46.23, 46.36 | within noise |
| relu 30 x 784 forward_batch b32 / rust | 31.51 (31.46-31.74) | 31.43 (30.97-32) | -0.3% | 31.51, 31.6, 31.58 / 31.59, 31.14, 31.69 | within noise |
| relu 30 x 784 forward_batch b512 / numpy | 555.1 (548.9-563.3) | 553 (550.4-566.4) | -0.4% | 558.2, 552.5, 556.5 / 559.4, 556, 551.8 | within noise |
| relu 30 x 784 forward_batch b512 / rust | 494.9 (486.4-502.3) | 495.2 (485.3-544.2) | +0.1% | 491.9, 494.3, 496.6 / 494.8, 514.8, 496.2 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 399.9 (397.4-407.9) | 402.8 (397.7-404.3) | +0.7% | 406, 399.4, 398.3 / 400.8, 401, 403.3 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 261 (260.3-261.7) | 261.8 (261-262.5) | +0.3% | 260.7, 261.3, 261.1 / 261.5, 262.1, 261.7 | separated, inside spread |
| attention 16 x 32 forward_batch b512 / numpy | 6125 (6108-6191) | 6143 (6102-6206) | +0.3% | 6162, 6121, 6118 / 6143, 6154, 6143 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 5063 (5036-5078) | 5091 (5058-5101) | +0.6% | 5048, 5062, 5073 / 5088, 5072, 5097 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 282.2 (275-288.4) | 276.6 (273-285.4) | -2.0% | 286.9, 276.4, 282.2 / 283.5, 274.6, 275.2 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 114.2 (113.9-115.8) | 114.1 (113.8-115.1) | -0.1% | 115, 114.3, 114 / 114.6, 113.9, 114.1 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5662 (5561-5707) | 5580 (5573-5607) | -1.5% | 5702, 5662, 5565 / 5593, 5576, 5585 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 2074 (2061-2137) | 2078 (2052-2096) | +0.2% | 2072, 2068, 2105 / 2064, 2069, 2095 | within noise |
