Old `0b17d22` against new `0b17d22`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --shape 5408 --shape 784 --shape attention --op forward_batch --op downstream_batch --op accumulate_gradient_batch --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `edce2de` (extension sha256 `f72612f402e8`) and new crate `51a2baf` (extension sha256 `7194f34f6ce9`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.75 (HIGH); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / relu 30 x 784 forward_batch b512 / rust -38.2% (206.1 -> 127.3 µs)
- consistent: per call / dense 30 x 784 forward_batch b512 / rust -30.0% (258.4 -> 180.9 µs)
- consistent: per call / dense 30 x 784 downstream_batch b512 / rust -26.4% (242.3 -> 178.2 µs)
- consistent: per call / dense 30 x 784 accumulate_gradient_batch b512 / rust -23.1% (252.2 -> 193.9 µs)
- consistent: per call / attention 16 x 32 accumulate_gradient_batch b512 / rust -12.8% (1633 -> 1424 µs)
- consistent: per call / conv tail 32 x 5408 downstream_batch b512 / rust -12.6% (2421 -> 2116 µs)
- consistent: per call / conv tail 32 x 5408 forward_batch b512 / rust -9.6% (1128 -> 1020 µs)
- consistent: per call / attention 16 x 32 forward_batch b512 / rust -6.3% (4261 -> 3991 µs)
- 28 rows within noise (4 separated inside their spread), max |Δ| 4.5%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward_batch b32 / numpy | 149.8 (144.9-157) | 151.1 (143.4-157.2) | +0.8% | 149.5, 151.5, 150.8 / 149.9, 151.1, 151.2 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 256.2 (246.1-264.3) | 254.5 (249.3-262.8) | -0.7% | 249.5, 260.3, 259.4 / 252.7, 257.9, 255.2 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1163 (1055-1175) | 1166 (1155-1171) | +0.3% | 1108, 1159, 1171 / 1167, 1161, 1167 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1128 (1095-1136) | 1020 (1017-1029) | -9.6% | 1110, 1129, 1133 / 1024, 1019, 1021 | consistent |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 78.48 (77.77-78.98) | 78.3 (77.55-78.97) | -0.2% | 77.87, 78.91, 78.48 / 77.78, 78.49, 78.76 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 241.6 (237-247.7) | 243.9 (238.9-250.4) | +0.9% | 238.9, 243.6, 245 / 243.9, 242.9, 246.8 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3190 (3171-3202) | 3193 (3177-3200) | +0.1% | 3178, 3186, 3199 / 3196, 3196, 3177 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 2421 (2406-2436) | 2116 (2111-2145) | -12.6% | 2435, 2417, 2412 / 2123, 2112, 2131 | consistent |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 162.7 (159-163.8) | 162.9 (160-164) | +0.1% | 161.2, 162.1, 163 / 162.9, 163.9, 160.1 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 289.9 (287.9-305.5) | 295 (289.9-301.5) | +1.8% | 289.2, 293.2, 296.7 / 295, 295.4, 295.7 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 1856 (1814-1864) | 1853 (1819-1884) | -0.2% | 1836, 1858, 1854 / 1846, 1846, 1869 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 1988 (1953-2204) | 1899 (1877-1909) | -4.5% | 1974, 1998, 2087 / 1893, 1898, 1900 | separated, inside spread |
| dense 30 x 784 forward_batch b32 / numpy | 38.56 (38.33-38.88) | 38.13 (37.7-38.78) | -1.1% | 38.6, 38.53, 38.56 / 38.1, 38.24, 38.42 | separated, inside spread |
| dense 30 x 784 forward_batch b32 / rust | 35.51 (34.67-36.11) | 36.14 (35.14-37.92) | +1.8% | 35.19, 35.91, 35.22 / 35.94, 36.59, 36.53 | separated, inside spread |
| dense 30 x 784 forward_batch b512 / numpy | 267.4 (264.4-269.3) | 267.2 (264.9-268.4) | -0.1% | 265, 267.4, 268.7 / 265.8, 267.5, 267.9 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 258.4 (254.1-262.2) | 180.9 (167.9-246.8) | -30.0% | 255.8, 258, 261.9 / 174.4, 180.6, 213.8 | consistent |
| dense 30 x 784 downstream_batch b32 / numpy | 23.15 (22.78-23.71) | 23.19 (23.02-23.52) | +0.2% | 22.85, 23.17, 23.51 / 23.27, 23.26, 23.08 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 30.29 (29.05-34.84) | 30.24 (29.53-30.71) | -0.2% | 29.53, 30.55, 32.46 / 29.67, 30.24, 30.53 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 133.2 (132.3-134.7) | 132.6 (132.1-134.1) | -0.4% | 134.5, 132.6, 133.2 / 133.1, 132.6, 132.8 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 242.3 (239.4-245.9) | 178.2 (177.9-179.2) | -26.4% | 240.9, 244, 243.3 / 178.2, 178.3, 178.7 | consistent |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 40.44 (39.94-41.02) | 40.16 (39.96-40.58) | -0.7% | 39.98, 40.43, 40.93 / 40.19, 40.06, 40.37 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 40.97 (39.81-41.86) | 40.89 (39.49-41.91) | -0.2% | 39.91, 41.27, 41.47 / 40.07, 40.86, 41.52 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 222 (220-224.8) | 222.6 (221-224) | +0.3% | 221, 223.1, 223.1 / 221.8, 221.9, 223.8 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 252.2 (248.7-256.3) | 193.9 (192.6-194.7) | -23.1% | 249.3, 254.4, 253.2 / 193.4, 193.6, 193.9 | consistent |
| relu 30 x 784 forward_batch b32 / numpy | 30.12 (29.24-30.22) | 29.59 (29.39-29.9) | -1.7% | 29.31, 30.17, 30.16 / 29.65, 29.68, 29.5 | within noise |
| relu 30 x 784 forward_batch b32 / rust | 33.07 (32.03-34.61) | 33.52 (32.85-34.53) | +1.4% | 32.34, 33.64, 33.55 / 33.29, 33.29, 34.35 | within noise |
| relu 30 x 784 forward_batch b512 / numpy | 157.8 (156.3-159.2) | 157.6 (157.5-159.2) | -0.1% | 156.9, 158.8, 157.8 / 158.5, 157.6, 158.2 | within noise |
| relu 30 x 784 forward_batch b512 / rust | 206.1 (203.2-212) | 127.3 (126.1-195.3) | -38.2% | 204.1, 207.3, 209.5 / 126.5, 127.3, 161.9 | consistent |
| attention 16 x 32 forward_batch b32 / numpy | 361.2 (360.6-371.9) | 361.8 (359.8-364.7) | +0.2% | 366.7, 360.7, 365.3 / 360.1, 362.9, 362.8 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 260.2 (253.4-272.5) | 261.7 (260.2-266.7) | +0.6% | 254, 262.4, 266 / 260.4, 263.1, 263.7 | within noise |
| attention 16 x 32 forward_batch b512 / numpy | 5537 (5447-5573) | 5526 (5487-5604) | -0.2% | 5461, 5544, 5559 / 5495, 5579, 5520 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 4261 (4166-4302) | 3991 (3952-4042) | -6.3% | 4214, 4243, 4287 / 3990, 4035, 3969 | consistent |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 254.8 (245.2-260.9) | 247.1 (242-252.2) | -3.1% | 258.5, 249.9, 251.7 / 244.8, 249.8, 244.9 | separated, inside spread |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 111.1 (105.6-112.6) | 110.1 (108-111) | -0.9% | 107.2, 111.8, 111.3 / 108.1, 110.8, 110.1 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 5350 (5252-5544) | 5339 (5296-5362) | -0.2% | 5310, 5388, 5437 / 5320, 5331, 5343 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 1633 (1607-1650) | 1424 (1397-1439) | -12.8% | 1608, 1633, 1645 / 1410, 1432, 1424 | consistent |
