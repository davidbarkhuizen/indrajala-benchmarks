Old `3332480` against new `3332480`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --shape 5408 --shape 784 --shape attention --op forward_batch --op downstream_batch --op accumulate_gradient_batch --rust-threads 1 --openblas-threads 1 --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `7fffc49` (extension sha256 `21b07c2bef84`) and new crate `a4c4379` (extension sha256 `ccd720475df3`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.96 (HIGH); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / attention 16 x 32 forward_batch b512 / rust -3.0% (6018 -> 5837 µs)
- consistent, small: per call / attention 16 x 32 forward_batch b32 / rust -1.8% (321.1 -> 315.3 µs)
- 34 rows within noise (3 separated inside their spread), max |Δ| 3.5%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward_batch b32 / numpy | 286 (284.1-289.1) | 287.3 (283.9-293.8) | +0.4% | 285.9, 286.1, 286.6 / 290.2, 285.3, 288.5 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 334.7 (324.2-341.7) | 346.5 (336.7-368.3) | +3.5% | 337.1, 332.9, 329.6 / 342.9, 352.5, 353.2 | separated, inside spread |
| conv tail 32 x 5408 forward_batch b512 / numpy | 4179 (4137-4212) | 4201 (4177-4257) | +0.5% | 4184, 4180, 4165 / 4201, 4247, 4182 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 6319 (6197-6333) | 6381 (6229-6638) | +1.0% | 6307, 6265, 6322 / 6257, 6453, 6496 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 258.8 (256.9-260.2) | 257.9 (255-263.1) | -0.4% | 257.9, 259.4, 258.6 / 256.7, 257.5, 260.2 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 237.9 (236.4-243.9) | 239.7 (237.2-243) | +0.8% | 237.9, 243.8, 236.5 / 238.1, 240.6, 241.7 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 4074 (4057-4144) | 4056 (4049-4069) | -0.4% | 4067, 4076, 4100 / 4051, 4062, 4058 | separated, inside spread |
| conv tail 32 x 5408 downstream_batch b512 / rust | 4365 (4356-4376) | 4364 (4359-4383) | -0.0% | 4371, 4361, 4366 / 4364, 4371, 4368 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 307.5 (306.4-311.3) | 308.7 (307.2-311.3) | +0.4% | 307.5, 308.9, 308.9 / 308.7, 307.3, 311.2 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 267 (266.4-267.7) | 267.8 (266.3-280.6) | +0.3% | 267.3, 267.2, 266.6 / 267.4, 266.8, 276 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 3898 (3885-3964) | 3889 (3881-3957) | -0.2% | 3931, 3892, 3897 / 3893, 3887, 3919 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 5280 (5249-5309) | 5290 (5252-5310) | +0.2% | 5277, 5285, 5280 / 5301, 5270, 5285 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 53.96 (53.63-54.3) | 54.33 (53.55-56.64) | +0.7% | 54, 54.02, 53.77 / 54.09, 54.01, 55.67 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 44.84 (44.69-45.68) | 44.92 (44.5-48.7) | +0.2% | 45.04, 45.23, 44.69 / 44.6, 44.99, 46.79 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 647 (637.3-671.7) | 640.7 (629.1-648.4) | -1.0% | 638.9, 657.3, 657.6 / 636.1, 638.8, 645 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 705.6 (703-709.6) | 704.7 (700.7-720.5) | -0.1% | 704, 704.9, 708.1 / 701.4, 706.9, 711.7 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 37.22 (37.18-37.54) | 37.43 (37.12-38.6) | +0.6% | 37.37, 37.2, 37.23 / 37.18, 38.11, 37.7 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 32.13 (31.68-33.36) | 32.29 (31.89-32.58) | +0.5% | 31.94, 32.06, 33.13 / 32.24, 32.41, 32.18 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 488.9 (488.7-496.6) | 497.3 (488-501.3) | +1.7% | 488.9, 493, 488.8 / 492.6, 496.4, 499.3 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 501.8 (500.6-517.3) | 510.1 (464.8-520.8) | +1.7% | 500.7, 501.8, 516.4 / 512, 492.8, 508 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 51 (50.73-52.19) | 51.66 (50.88-52.73) | +1.3% | 51.81, 50.74, 51 / 50.97, 52.02, 52.03 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 36.88 (36.76-37.08) | 37.44 (36.74-38.38) | +1.5% | 36.86, 36.93, 36.9 / 36.94, 37.59, 37.91 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 604.4 (603.8-604.7) | 604.5 (603-626.6) | +0.0% | 604.3, 604.2, 604.7 / 604.2, 614.8, 613.5 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 563.2 (552.2-583.2) | 557.8 (553.4-570.6) | -1.0% | 566, 560.1, 574 / 556.4, 561.3, 564.2 | within noise |
| relu 30 x 784 forward_batch b32 / numpy | 45.98 (45.78-46.12) | 46.59 (45.68-46.92) | +1.3% | 45.89, 45.89, 46.07 / 45.93, 46.91, 46.59 | within noise |
| relu 30 x 784 forward_batch b32 / rust | 42.37 (42.03-42.4) | 42.31 (42-43.27) | -0.1% | 42.31, 42.39, 42.2 / 42.2, 42.81, 42.63 | within noise |
| relu 30 x 784 forward_batch b512 / numpy | 556.3 (550.5-573.2) | 559.1 (551.6-595.4) | +0.5% | 561.8, 559.3, 556.3 / 554.2, 575.6, 561.8 | within noise |
| relu 30 x 784 forward_batch b512 / rust | 663.8 (658.3-710.5) | 670.7 (658.9-679.3) | +1.0% | 687.3, 660.6, 665.6 / 663.8, 669.1, 675.6 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 398.4 (397.6-400.6) | 400.7 (398.1-404.2) | +0.6% | 399.5, 398.6, 397.6 / 399, 400.4, 404 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 321.1 (319.4-325) | 315.3 (313.1-317.1) | -1.8% | 320.6, 322.7, 321.1 / 313.6, 315.7, 316.1 | consistent, small |
| attention 16 x 32 forward_batch b512 / numpy | 6123 (6102-6141) | 6132 (6096-6168) | +0.2% | 6115, 6129, 6119 / 6110, 6129, 6165 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 6018 (5994-6107) | 5837 (5819-5896) | -3.0% | 6005, 6008, 6076 / 5828, 5833, 5890 | consistent |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 275.9 (273.9-280.9) | 280.3 (278.4-287.2) | +1.6% | 280.7, 275.9, 274.9 / 279.2, 284.3, 280.3 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 166.1 (163.7-168.9) | 165.6 (161.9-176.5) | -0.3% | 167.6, 165.4, 165.6 / 163.5, 169.2, 168.7 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5587 (5558-5843) | 5652 (5586-5822) | +1.2% | 5704, 5576, 5587 / 5594, 5655, 5762 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 3132 (3117-3146) | 3153 (3127-3225) | +0.7% | 3137, 3124, 3136 / 3130, 3176, 3177 | within noise |
