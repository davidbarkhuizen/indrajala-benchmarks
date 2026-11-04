Old `1854b89` against new `1854b89`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --shape 5408 --shape 784 --shape attention --op forward_batch --op downstream_batch --op accumulate_gradient_batch --rust-threads 1 --openblas-threads 1 --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `690bce8` (extension sha256 `7ba3057a73f7`) and new crate `5a19b18` (extension sha256 `84ec4e85d91b`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.51 (HIGH); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / conv tail 32 x 5408 accumulate_gradient_batch b512 / rust -65.9% (1.549e+04 -> 5279 µs)
- consistent: per call / attention 16 x 32 accumulate_gradient_batch b512 / rust -63.7% (8655 -> 3142 µs)
- consistent: per call / dense 30 x 784 accumulate_gradient_batch b512 / rust -39.1% (910.7 -> 554.6 µs)
- consistent: per call / attention 16 x 32 accumulate_gradient_batch b32 / rust -15.9% (199.6 -> 167.8 µs)
- 32 rows within noise (3 separated inside their spread), max |Δ| 7.3%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward_batch b32 / numpy | 288.4 (285.6-289.9) | 286.6 (284.2-293.6) | -0.6% | 287.8, 287.9, 288.7 / 285.2, 286.2, 291.1 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 364.5 (336.5-452.3) | 337.8 (336.4-383) | -7.3% | 413, 364.5, 338.2 / 338.6, 337.8, 359.7 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 4168 (4143-4188) | 4174 (4147-4215) | +0.1% | 4180, 4171, 4153 / 4183, 4174, 4180 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 6547 (6297-6741) | 6378 (6240-6739) | -2.6% | 6714, 6547, 6308 / 6378, 6250, 6598 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 260.2 (257.7-265.1) | 257.4 (256.4-262) | -1.1% | 260.1, 261.4, 260.5 / 256.6, 257.5, 259.9 | separated, inside spread |
| conv tail 32 x 5408 downstream_batch b32 / rust | 239.4 (238.3-242.5) | 237.8 (236.3-241.6) | -0.7% | 241.3, 239.5, 238.6 / 237.8, 236.5, 240.8 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 4077 (4059-4080) | 4069 (4057-4091) | -0.2% | 4077, 4060, 4078 / 4073, 4066, 4074 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 4377 (4357-4395) | 4366 (4357-4395) | -0.3% | 4390, 4377, 4357 / 4365, 4376, 4371 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 312.4 (306.2-324.6) | 312.1 (307.4-327.7) | -0.1% | 323.9, 310.1, 308.9 / 310, 313.8, 319.7 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 270.6 (266.2-281) | 268.2 (265.8-277.4) | -0.9% | 270.6, 279, 266.3 / 266.9, 267.4, 274.3 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 3915 (3897-3963) | 3904 (3894-3948) | -0.3% | 3942, 3919, 3898 / 3905, 3895, 3927 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 1.549e+04 (1.52e+04-1.554e+04) | 5279 (5261-5414) | -65.9% | 1.539e+04, 1.551e+04, 1.535e+04 / 5267, 5277, 5377 | consistent |
| dense 30 x 784 forward_batch b32 / numpy | 54.86 (53.78-56.24) | 54.47 (53.87-55.26) | -0.7% | 55.68, 55.16, 53.87 / 54.25, 54.5, 54.79 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 45.44 (44.38-45.77) | 45.18 (44.9-45.77) | -0.6% | 45, 45.71, 45.06 / 45.05, 45.14, 45.62 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 634.5 (631.8-650.5) | 642.7 (639.4-663.7) | +1.3% | 641.6, 640.5, 633.1 / 653.1, 642.4, 643.5 | separated, inside spread |
| dense 30 x 784 forward_batch b512 / rust | 713.7 (702.3-717.8) | 708.1 (704.4-751.6) | -0.8% | 713.7, 717.3, 703.5 / 728, 707.8, 712.1 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 37.65 (36.99-38.15) | 37.32 (36.93-38.01) | -0.9% | 38.05, 37.61, 37.21 / 37.17, 37.29, 37.67 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 32.25 (31.75-32.53) | 31.98 (31.57-32.67) | -0.8% | 32.26, 32.28, 32 / 32.16, 31.58, 32.42 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 492 (488-497.4) | 490 (488.4-492.2) | -0.4% | 494.9, 494.3, 488.6 / 490, 488.6, 492 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 504.9 (500-508) | 503.6 (500-512) | -0.3% | 504.9, 507.9, 500.4 / 502.2, 502.8, 509.3 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 51.73 (50.87-52.66) | 51.26 (50.77-51.99) | -0.9% | 52.36, 51.73, 50.89 / 50.89, 51.16, 51.89 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 37.41 (36.81-38.5) | 36.81 (36.61-38.18) | -1.6% | 37.92, 37.88, 36.84 / 36.81, 36.7, 38.16 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 622.1 (604.5-623.1) | 609.2 (604.2-622.9) | -2.1% | 617.4, 622.7, 613.8 / 613.5, 604.8, 613.5 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 910.7 (877.8-978.9) | 554.6 (552.2-569.8) | -39.1% | 968.6, 906, 886.5 / 553.7, 553.6, 567.1 | consistent |
| relu 30 x 784 forward_batch b32 / numpy | 46.43 (45.93-46.72) | 46.22 (45.59-46.89) | -0.5% | 46.56, 46.33, 46.16 / 45.7, 46.22, 46.61 | within noise |
| relu 30 x 784 forward_batch b32 / rust | 42.5 (42.06-42.81) | 42.51 (42.11-43.07) | +0.0% | 42.77, 42.53, 42.07 / 42.36, 42.26, 42.95 | within noise |
| relu 30 x 784 forward_batch b512 / numpy | 557.7 (546.1-564.6) | 554 (549.4-560.3) | -0.7% | 559.8, 560.9, 549.8 / 555.2, 555.8, 552.3 | within noise |
| relu 30 x 784 forward_batch b512 / rust | 666.4 (658.1-675.4) | 667.9 (666.8-673.8) | +0.2% | 671.2, 668.5, 660.2 / 669.4, 667, 670.7 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 404.8 (398.4-406.3) | 399.1 (397.2-407.8) | -1.4% | 405.5, 403.9, 401.6 / 397.6, 399.1, 405.2 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 323.3 (320.9-324.7) | 320.8 (319.5-325.2) | -0.8% | 323.3, 324.2, 321.9 / 320, 320.8, 323.7 | within noise |
| attention 16 x 32 forward_batch b512 / numpy | 6147 (6100-6232) | 6163 (6093-6209) | +0.3% | 6223, 6142, 6124 / 6151, 6137, 6169 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 6099 (6016-6156) | 6024 (5988-6120) | -1.2% | 6151, 6099, 6031 / 6069, 6013, 6024 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 278.3 (274.4-287.1) | 280.4 (275.2-286.3) | +0.8% | 279.3, 277.3, 281.7 / 278.8, 279.3, 283.2 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 199.6 (188.3-212.6) | 167.8 (163.9-171.7) | -15.9% | 194.5, 212, 194.8 / 166.1, 166.3, 170.5 | consistent |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5813 (5591-5893) | 5567 (5561-5718) | -4.2% | 5813, 5859, 5656 / 5562, 5567, 5715 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 8655 (8315-9139) | 3142 (3116-3245) | -63.7% | 8655, 8741, 8727 / 3126, 3142, 3213 | consistent |
