Old `f59388b` against new `f59388b`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --shape 5408 --shape 784 --shape attention --op forward_batch --op downstream_batch --op accumulate_gradient_batch --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `4dba70e` (extension sha256 `f5c8b6404a1d`) and new crate `ce5a267` (extension sha256 `24bdf26aceef`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.73 (HIGH); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / conv tail 32 x 5408 forward_batch b512 / rust -33.1% (1695 -> 1134 µs)
- consistent: per call / conv tail 32 x 5408 forward_batch b32 / rust -32.8% (347.9 -> 233.9 µs)
- consistent: per call / relu 30 x 784 forward_batch b32 / rust -23.5% (43.2 -> 33.03 µs)
- consistent: per call / dense 30 x 784 forward_batch b32 / rust -23.0% (45.93 -> 35.37 µs)
- consistent: per call / relu 30 x 784 forward_batch b512 / rust -11.0% (239.4 -> 213 µs)
- consistent: per call / dense 30 x 784 forward_batch b512 / rust -11.0% (291.5 -> 259.5 µs)
- consistent: per call / conv tail 32 x 5408 downstream_batch b512 / rust +6.6% (2246 -> 2395 µs)
- 29 rows within noise, max |Δ| 3.1%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward_batch b32 / numpy | 150 (148.9-160.2) | 154.7 (145.6-159.6) | +3.1% | 150, 153.8, 154.6 / 152.7, 152.1, 156 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 347.9 (329.7-378.2) | 233.9 (230.3-238) | -32.8% | 363.3, 352.4, 341.3 / 231.7, 233.5, 236.9 | consistent |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1165 (1061-1177) | 1167 (1146-1168) | +0.2% | 1111, 1165, 1173 / 1155, 1168, 1167 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1695 (1600-1787) | 1134 (1128-1157) | -33.1% | 1725, 1616, 1734 / 1131, 1146, 1133 | consistent |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 77.71 (77.34-78.75) | 77.91 (77.42-78.36) | +0.3% | 77.77, 77.71, 78.2 / 77.69, 77.94, 78.06 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 239.5 (231.9-247.9) | 241.4 (234.8-245.3) | +0.8% | 234.8, 242.6, 242.7 / 236.8, 241.4, 245.1 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3178 (3150-3211) | 3184 (3173-3201) | +0.2% | 3164, 3182, 3193 / 3182, 3187, 3186 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2246 (2233-2279) | 2395 (2390-2409) | +6.6% | 2245, 2237, 2264 / 2395, 2399, 2401 | consistent |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 162.6 (160.2-166.4) | 163.6 (162.1-169.6) | +0.6% | 161, 166, 162 / 162.5, 163.9, 166.6 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 275.2 (271.4-286.5) | 272.6 (266.8-283.3) | -0.9% | 273.6, 274.4, 284.2 / 270.9, 271.4, 278.3 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 1848 (1766-1861) | 1838 (1762-1861) | -0.5% | 1810, 1831, 1852 / 1849, 1789, 1846 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 1970 (1947-2038) | 1988 (1956-2226) | +0.9% | 1968, 1960, 2007 / 2091, 1982, 2099 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 38.13 (37.81-38.98) | 38.27 (37.72-38.92) | +0.4% | 38.13, 38.4, 38.32 / 38.02, 38.29, 38.57 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 45.93 (45.43-47.19) | 35.37 (34.62-36.32) | -23.0% | 45.72, 45.76, 46.62 / 34.66, 35.62, 35.77 | consistent |
| dense 30 x 784 forward_batch b512 / numpy | 266.8 (263.9-268.1) | 266.7 (265.3-269.3) | -0.0% | 266, 265.9, 267.8 / 265.6, 266.7, 268.5 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 291.5 (285.7-303.1) | 259.5 (257.4-279.2) | -11.0% | 288.3, 297.5, 291.2 / 260.2, 258.3, 268.7 | consistent |
| dense 30 x 784 downstream_batch b32 / numpy | 23.72 (23.49-24.41) | 24.1 (23.27-24.32) | +1.6% | 23.75, 24.04, 23.63 / 24.08, 24.19, 23.7 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 32.73 (32.05-34.2) | 33.31 (32.08-33.61) | +1.8% | 32.38, 32.98, 33.35 / 32.84, 33.41, 32.82 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 131.4 (129.9-139.3) | 130.8 (130.2-132.1) | -0.5% | 135.3, 130.8, 131.4 / 131, 130.3, 131.4 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 243.5 (238.9-248.3) | 242.3 (240.5-245.2) | -0.5% | 240.6, 244.9, 245.4 / 241.9, 241.4, 245 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 40.57 (39.21-41.28) | 40.06 (39.25-40.91) | -1.3% | 40.02, 40.37, 40.65 / 39.6, 40.11, 40.49 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 40.24 (39.77-41.01) | 40.89 (39.88-41.32) | +1.6% | 40, 40.27, 40.61 / 40.33, 41.16, 40.7 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 223.3 (221.5-225.1) | 222.9 (222-223.6) | -0.2% | 222, 223.3, 224.6 / 222.8, 222.7, 223.1 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 253.9 (251.4-256.3) | 255.5 (250.5-259.3) | +0.6% | 251.8, 255.2, 254.8 / 252.5, 254.5, 258.8 | within noise |
| relu 30 x 784 forward_batch b32 / numpy | 29.93 (29.48-30.5) | 30.23 (29.47-30.88) | +1.0% | 29.8, 30.19, 29.86 / 30.08, 29.93, 30.47 | within noise |
| relu 30 x 784 forward_batch b32 / rust | 43.2 (42.54-43.88) | 33.03 (31.99-33.34) | -23.5% | 42.68, 43.39, 43.56 / 32.41, 33.24, 32.88 | consistent |
| relu 30 x 784 forward_batch b512 / numpy | 158.3 (155.9-159.1) | 156.9 (155.9-158.1) | -0.9% | 156.8, 157.9, 159 / 157.4, 157.1, 156.5 | within noise |
| relu 30 x 784 forward_batch b512 / rust | 239.4 (235.9-243.2) | 213 (207.8-215.4) | -11.0% | 239.5, 239.6, 239.3 / 214.4, 208.1, 213.5 | consistent |
| attention 16 x 32 forward_batch b32 / numpy | 367.7 (361.2-372.9) | 368.5 (361.8-371.4) | +0.2% | 365.4, 366.9, 369.4 / 370.6, 365.1, 366.1 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 323.2 (314.8-330.4) | 323.6 (320.6-328.5) | +0.1% | 315.6, 323.2, 328.4 / 323.9, 322.2, 326.5 | within noise |
| attention 16 x 32 forward_batch b512 / numpy | 5617 (5551-5689) | 5585 (5547-5674) | -0.6% | 5557, 5629, 5666 / 5560, 5585, 5636 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 5080 (5010-5209) | 5065 (5024-5253) | -0.3% | 5075, 5033, 5156 / 5034, 5201, 5063 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 253.5 (242.9-256.6) | 250.4 (245.6-257) | -1.2% | 248.7, 253.4, 254.6 / 250.4, 252.6, 250.3 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 168.9 (165.6-178.1) | 168.6 (166.4-170.7) | -0.1% | 165.8, 168.9, 174.8 / 168.5, 168.6, 169.4 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5388 (5328-5487) | 5365 (5295-5557) | -0.4% | 5476, 5328, 5388 / 5327, 5358, 5464 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 3011 (2998-3042) | 3011 (2983-3068) | +0.0% | 3030, 3000, 3021 / 3011, 2995, 3045 | within noise |
