Old `f59388b` against new `f59388b`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --shape 5408 --shape 784 --shape attention --op forward_batch --op downstream_batch --op accumulate_gradient_batch --rust-threads 1 --openblas-threads 1 --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `4dba70e` (extension sha256 `f5c8b6404a1d`) and new crate `ce5a267` (extension sha256 `24bdf26aceef`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 2.03 (HIGH); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / conv tail 32 x 5408 forward_batch b32 / rust -32.7% (344.8 -> 231.9 µs)
- consistent: per call / conv tail 32 x 5408 forward_batch b512 / rust -29.1% (6391 -> 4530 µs)
- consistent: per call / relu 30 x 784 forward_batch b32 / rust -24.4% (42.48 -> 32.11 µs)
- consistent: per call / relu 30 x 784 forward_batch b512 / rust -24.3% (675.1 -> 510.8 µs)
- consistent: per call / dense 30 x 784 forward_batch b512 / rust -23.1% (712.6 -> 547.9 µs)
- consistent: per call / dense 30 x 784 forward_batch b32 / rust -21.6% (46.02 -> 36.06 µs)
- 30 rows within noise (1 separated inside their spread), max |Δ| 2.0%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward_batch b32 / numpy | 290.1 (285.4-293.5) | 287.7 (285.4-290.1) | -0.8% | 288.2, 291.1, 290.1 / 288.3, 287.8, 286.6 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 344.8 (336.2-355.2) | 231.9 (226.8-233.8) | -32.7% | 348.2, 342.2, 344.6 / 233.8, 230.5, 228.8 | consistent |
| conv tail 32 x 5408 forward_batch b512 / numpy | 4204 (4140-4321) | 4172 (4140-4283) | -0.8% | 4186, 4244, 4204 / 4153, 4223, 4201 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 6391 (6301-6605) | 4530 (4509-4584) | -29.1% | 6500, 6346, 6412 / 4563, 4531, 4514 | consistent |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 258.2 (255.4-261.9) | 262.5 (255.7-266.7) | +1.7% | 260, 256.9, 257.9 / 265.2, 259, 259.8 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 240.6 (238.8-241) | 241.4 (238.1-243.4) | +0.3% | 240.8, 239.9, 239.8 / 241.7, 241.3, 240.5 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 4071 (4061-4094) | 4064 (4058-4071) | -0.2% | 4068, 4064, 4086 / 4068, 4067, 4060 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 4372 (4358-4377) | 4395 (4381-4408) | +0.5% | 4372, 4367, 4372 / 4403, 4395, 4387 | separated, inside spread |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 315.5 (304.6-326.9) | 309.7 (308.1-326.5) | -1.9% | 309.8, 317.4, 317.6 / 313, 318.7, 308.2 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 272.5 (271.3-279) | 272.7 (267.8-279.5) | +0.1% | 272.8, 275.9, 271.6 / 276.9, 271.1, 271.2 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 3914 (3887-3958) | 3905 (3882-3968) | -0.2% | 3937, 3890, 3923 / 3929, 3930, 3887 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 5347 (5283-5411) | 5239 (5218-5376) | -2.0% | 5347, 5334, 5351 / 5355, 5236, 5226 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 54.76 (53.82-55.31) | 54.31 (53.38-55.39) | -0.8% | 55.14, 54.13, 54.69 / 54.71, 54.69, 53.56 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 46.02 (45.29-50.71) | 36.06 (34.43-40.68) | -21.6% | 48.22, 45.74, 46.87 / 36.06, 39.55, 34.45 | consistent |
| dense 30 x 784 forward_batch b512 / numpy | 640.5 (636.9-683.4) | 644.4 (631-650.7) | +0.6% | 661.4, 640.8, 639.5 / 646.4, 647.3, 632.8 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 712.6 (701.5-717.6) | 547.9 (531.1-607.9) | -23.1% | 715, 709.5, 710 / 547.9, 606.1, 532.7 | consistent |
| dense 30 x 784 downstream_batch b32 / numpy | 37.74 (37.16-38.17) | 37.46 (36.95-37.56) | -0.8% | 38.08, 37.49, 37.48 / 37.53, 37.27, 37.2 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 32.39 (31.93-33.37) | 32.24 (31.65-33.16) | -0.5% | 32.39, 32.66, 32.39 / 32.27, 32.69, 31.95 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 493.4 (488.5-503.8) | 494.9 (488.6-497.8) | +0.3% | 495.6, 490.8, 496.6 / 493.5, 496.3, 493.2 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 507.4 (500.2-515.4) | 506.9 (500.3-509.5) | -0.1% | 504.1, 512.2, 506.6 / 507.5, 508.4, 501.7 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 51.93 (51.19-52.97) | 52.29 (50.88-52.91) | +0.7% | 52.05, 52.32, 51.67 / 52.33, 52.64, 51.01 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 37.4 (36.69-38.08) | 37.69 (36.72-38.3) | +0.8% | 37.71, 36.74, 37.61 / 37.69, 38.19, 36.93 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 613.1 (604.6-622.9) | 617.8 (603.7-623.3) | +0.8% | 617.9, 609.3, 609.3 / 623, 617.8, 604 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 564.5 (558.7-577.3) | 559.4 (556.8-565.5) | -0.9% | 571.9, 564.5, 558.9 / 559.4, 564.2, 556.8 | within noise |
| relu 30 x 784 forward_batch b32 / numpy | 46.84 (45.97-47.08) | 46.52 (45.58-47.18) | -0.7% | 46.84, 46.5, 46.63 / 46.98, 46.59, 45.85 | within noise |
| relu 30 x 784 forward_batch b32 / rust | 42.48 (42.21-43.4) | 32.11 (31.77-33.19) | -24.4% | 42.79, 42.92, 42.37 / 32.11, 32.9, 31.85 | consistent |
| relu 30 x 784 forward_batch b512 / numpy | 551.4 (547.9-574.6) | 558.4 (547.7-575.4) | +1.3% | 558, 551.2, 561.3 / 569.5, 558.4, 552.6 | within noise |
| relu 30 x 784 forward_batch b512 / rust | 675.1 (664.5-719.4) | 510.8 (495.7-515.6) | -24.3% | 696.6, 674.2, 672 / 512.8, 512.4, 501.5 | consistent |
| attention 16 x 32 forward_batch b32 / numpy | 401.7 (397.8-406.4) | 405.8 (397.8-408.3) | +1.0% | 404.1, 399.7, 402.1 / 408, 405.8, 397.9 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 314.3 (312.8-315.7) | 315.7 (314.3-318.3) | +0.5% | 315.1, 314.2, 313.6 / 315.7, 318.2, 314.9 | within noise |
| attention 16 x 32 forward_batch b512 / numpy | 6132 (6109-6195) | 6180 (6104-6217) | +0.8% | 6149, 6152, 6128 / 6197, 6192, 6109 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 5848 (5806-5867) | 5862 (5812-5904) | +0.2% | 5850, 5830, 5836 / 5885, 5877, 5817 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 279.6 (271.6-284.1) | 283.6 (271.7-289.7) | +1.4% | 277, 277.8, 281.5 / 283.6, 285.9, 280 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 166.6 (163.7-168.1) | 164.5 (162.4-173.6) | -1.3% | 166, 167.9, 164.8 / 165, 168.1, 163.5 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5675 (5582-5822) | 5710 (5569-5844) | +0.6% | 5734, 5710, 5590 / 5814, 5707, 5602 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 3199 (3174-3381) | 3183 (3138-3199) | -0.5% | 3191, 3286, 3199 / 3196, 3184, 3139 | within noise |
