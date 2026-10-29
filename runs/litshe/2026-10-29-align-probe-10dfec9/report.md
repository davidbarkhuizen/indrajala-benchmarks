Old `19bea85` against new `19bea85`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `a722c7c` (extension sha256 `2d514ad229dc`) and new crate `be14eac` (extension sha256 `44f6a8e617ba`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (raspberry-pi-5.json); passes peaked at 52.4-59.0 C; max 1-min load 0.45 (measured just after this run's crate builds); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / conv 13x13x8, 8 ch downstream_batch b512 / rust -86.8% (4.883e+04 -> 6445 µs)
- consistent: per call / conv 28x28, 8 ch downstream_batch b512 / rust -79.5% (5.146e+04 -> 1.053e+04 µs)
- consistent: per call / conv 26x26x8, 8 ch downstream_batch b512 / rust -75.1% (2.717e+05 -> 6.766e+04 µs)
- consistent: per call / conv 26x26x8, 8 ch downstream_batch b32 / rust -74.5% (1.337e+04 -> 3408 µs)
- consistent: per call / conv 26x26x8/2, 8 ch downstream_batch b32 / rust -66.0% (3672 -> 1250 µs)
- consistent: per call / conv 26x26x8/2, 8 ch downstream_batch b512 / rust -65.4% (6.906e+04 -> 2.387e+04 µs)
- consistent: per call / conv tail 32 x 5408 transpose b32 / rust -58.0% (1.878 -> 0.7894 µs)
- consistent: per call / dense 30 x 784 transpose b512 / rust -57.1% (24.92 -> 10.68 µs)
- consistent: per call / conv tail 32 x 5408 transpose b512 / rust -56.8% (26.79 -> 11.57 µs)
- consistent: per call / dense 10 x 30 transpose b512 / rust -55.6% (8.588 -> 3.815 µs)
- ... 33 more consistent rows (report --md)
- 227 rows within noise (33 separated inside their spread), max |Δ| 122.1%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 78.29 (77.51-81.11) | 78.04 (77.25-80.11) | -0.3% | 79.31, 78.29, 79.35 / 77.51, 79.87, 78.04 | within noise |
| conv tail 32 x 5408 forward / rust | 77.06 (73.25-77.28) | 75.52 (58.64-77.29) | -2.0% | 77.22, 75.45, 75.23 / 66.02, 76.19, 76.37 | within noise |
| conv tail 32 x 5408 downstream / numpy | 92.12 (91.18-93.43) | 92.43 (91.32-92.84) | +0.3% | 92.29, 92.74, 91.47 / 92, 92.08, 92.7 | within noise |
| conv tail 32 x 5408 downstream / rust | 77.62 (75.36-105.9) | 74.23 (74.04-104.5) | -4.4% | 92.37, 75.88, 89.89 / 89.38, 74.2, 83.05 | within noise |
| conv tail 32 x 5408 hidden_delta / numpy | 104.2 (103.5-105.3) | 104.5 (103.4-105.3) | +0.3% | 104.6, 104.7, 103.6 / 104.5, 104.3, 104.8 | within noise |
| conv tail 32 x 5408 hidden_delta / rust | 82.3 (79.76-84.61) | 80.16 (78.72-93.01) | -2.6% | 82.8, 82.18, 82.16 / 80.41, 79.27, 86.75 | within noise |
| conv tail 32 x 5408 accumulate_gradient / numpy | 384.4 (329.5-898.3) | 344 (266-368.6) | -10.5% | 656.2, 605.5, 351.9 / 290, 359.9, 346.3 | within noise |
| conv tail 32 x 5408 accumulate_gradient / rust | 91.52 (87.85-105.3) | 95.15 (89.53-97.54) | +4.0% | 90.44, 96.28, 96.59 / 95.2, 93.5, 94.05 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 1442 (1393-2073) | 1501 (1322-2096) | +4.1% | 1442, 1744, 1448 / 1822, 1475, 1421 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 572.2 (377.6-779.1) | 576.7 (425.1-637.2) | +0.8% | 600.5, 511.2, 574 / 568.6, 529.7, 576.7 | within noise |
| conv tail 32 x 5408 sgd step / numpy | 2152 (2108-2659) | 2635 (2110-3018) | +22.4% | 2177, 2126, 2418 / 2751, 2174, 2779 | within noise |
| conv tail 32 x 5408 sgd step / rust | 118 (115.4-278.4) | 120.7 (119.1-268.5) | +2.3% | 194, 197, 115.7 / 120.7, 120.5, 193.8 | within noise |
| conv tail 32 x 5408 forward_batch b32 / numpy | 508.3 (496.1-521.3) | 522.6 (499.4-544.9) | +2.8% | 505.9, 508.7, 512.8 / 522.6, 508.2, 535.7 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 1125 (1098-1128) | 1113 (1087-1129) | -1.1% | 1116, 1125, 1112 / 1113, 1118, 1104 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1.559e+04 (1.537e+04-1.699e+04) | 1.534e+04 (1.434e+04-1.62e+04) | -1.6% | 1.618e+04, 1.582e+04, 1.556e+04 / 1.544e+04, 1.574e+04, 1.438e+04 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1.14e+04 (1.054e+04-1.29e+04) | 1.167e+04 (1.042e+04-1.283e+04) | +2.3% | 1.157e+04, 1.182e+04, 1.131e+04 / 1.149e+04, 1.229e+04, 1.162e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 1403 (1345-1448) | 1318 (961.2-1508) | -6.1% | 1428, 1386, 1384 / 1004, 1318, 1464 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 1205 (1102-1690) | 1287 (1148-1637) | +6.9% | 1205, 1428, 1276 / 1296, 1393, 1256 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3.399e+04 (2.425e+04-4.525e+04) | 2.687e+04 (2.356e+04-4.005e+04) | -20.9% | 4.12e+04, 2.679e+04, 3.399e+04 / 3.116e+04, 3.292e+04, 2.576e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 1.935e+04 (1.336e+04-2.071e+04) | 1.916e+04 (1.354e+04-2.659e+04) | -1.0% | 1.634e+04, 1.879e+04, 2.031e+04 / 2.379e+04, 1.862e+04, 1.66e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 3233 (3127-3395) | 3206 (2932-3879) | -0.8% | 3279, 3152, 3303 / 3531, 3192, 3206 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 1732 (1610-2129) | 1931 (1597-2182) | +11.5% | 1897, 1869, 1623 / 1782, 2074, 1878 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 6.547e+04 (6.056e+04-6.898e+04) | 6.406e+04 (6.314e+04-6.777e+04) | -2.2% | 6.776e+04, 6.257e+04, 6.399e+04 / 6.645e+04, 6.371e+04, 6.369e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 2.261e+04 (2.094e+04-3.25e+04) | 2.444e+04 (2.207e+04-3.167e+04) | +8.1% | 2.754e+04, 2.196e+04, 2.527e+04 / 2.43e+04, 2.701e+04, 2.539e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 1885 (1837-2216) | 1796 (1643-2019) | -4.7% | 2079, 1883, 1855 / 1769, 1831, 1836 | separated, inside spread |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 2114 (2007-2232) | 2162 (2027-2359) | +2.3% | 2090, 2204, 2047 / 2095, 2293, 2157 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 2.3e+04 (2.151e+04-2.663e+04) | 2.217e+04 (2.145e+04-2.469e+04) | -3.6% | 2.636e+04, 2.233e+04, 2.239e+04 / 2.213e+04, 2.307e+04, 2.232e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 1.988e+04 (1.938e+04-2.03e+04) | 1.949e+04 (1.913e+04-2.084e+04) | -1.9% | 2.022e+04, 1.992e+04, 1.945e+04 / 1.956e+04, 2.027e+04, 1.916e+04 | within noise |
| dense 30 x 784 forward / numpy | 16.35 (16.12-16.41) | 16.32 (16.19-16.4) | -0.2% | 16.41, 16.23, 16.27 / 16.35, 16.26, 16.34 | within noise |
| dense 30 x 784 forward / rust | 6.486 (6.44-6.576) | 6.467 (6.368-6.517) | -0.3% | 6.475, 6.52, 6.508 / 6.495, 6.442, 6.436 | within noise |
| dense 30 x 784 downstream / numpy | 12.73 (12.66-12.81) | 12.69 (12.67-12.72) | -0.3% | 12.71, 12.69, 12.8 / 12.68, 12.71, 12.7 | within noise |
| dense 30 x 784 downstream / rust | 6.573 (6.308-6.696) | 6.586 (6.306-6.706) | +0.2% | 6.502, 6.565, 6.573 / 6.478, 6.586, 6.597 | within noise |
| dense 30 x 784 hidden_delta / numpy | 17.07 (16.97-17.14) | 17.04 (17.01-17.1) | -0.2% | 17.1, 17.08, 17.02 / 17.09, 17.01, 17.04 | within noise |
| dense 30 x 784 hidden_delta / rust | 7.479 (7.422-7.579) | 7.428 (7.186-7.53) | -0.7% | 7.47, 7.5, 7.512 / 7.366, 7.428, 7.341 | separated, inside spread |
| dense 30 x 784 accumulate_gradient / numpy | 42.87 (42.72-43.05) | 42.69 (42.67-42.82) | -0.4% | 42.97, 42.89, 42.79 / 42.7, 42.69, 42.74 | separated, inside spread |
| dense 30 x 784 accumulate_gradient / rust | 9.748 (9.698-9.928) | 9.888 (9.827-9.981) | +1.4% | 9.721, 9.788, 9.835 / 9.9, 9.888, 9.911 | separated, inside spread |
| dense 30 x 784 apply_accumulated_gradient / numpy | 61.14 (61.03-61.37) | 61.21 (61.12-61.33) | +0.1% | 61.06, 61.2, 61.2 / 61.3, 61.21, 61.13 | within noise |
| dense 30 x 784 apply_accumulated_gradient / rust | 36.37 (36.27-36.5) | 36.34 (36.21-36.45) | -0.1% | 36.4, 36.32, 36.39 / 36.36, 36.25, 36.43 | within noise |
| dense 30 x 784 sgd step / numpy | 108.1 (108-109.1) | 107.9 (107.7-108.4) | -0.1% | 108.1, 108.6, 108.1 / 107.8, 107.8, 108.2 | within noise |
| dense 30 x 784 sgd step / rust | 15.79 (15.68-15.82) | 15.69 (15.63-15.72) | -0.6% | 15.76, 15.74, 15.8 / 15.71, 15.66, 15.69 | separated, inside spread |
| dense 30 x 784 forward_batch b32 / numpy | 455.3 (91.81-460.8) | 454.4 (91.32-464.6) | -0.2% | 458.1, 274.1, 273.5 / 273.2, 277.9, 454.5 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 115.5 (114.7-118.7) | 119.3 (114.8-119.6) | +3.2% | 115.2, 116.4, 117.1 / 117.2, 117.2, 119.3 | separated, inside spread |
| dense 30 x 784 forward_batch b512 / numpy | 2152 (2016-2231) | 2320 (2087-2466) | +7.8% | 2166, 2154, 2087 / 2243, 2289, 2370 | separated, inside spread |
| dense 30 x 784 forward_batch b512 / rust | 981.5 (943.1-1057) | 998.6 (885.4-1091) | +1.7% | 981.5, 1010, 997.5 / 988.1, 970.8, 1015 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 219.4 (57.68-400.6) | 219.2 (57.41-388.6) | -0.1% | 229.3, 222.7, 219.2 / 388, 219.2, 57.52 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 126.4 (125.7-126.7) | 126.2 (125.8-126.5) | -0.2% | 126.3, 126.7, 126 / 126.2, 126.2, 126.1 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 3135 (2868-3796) | 3327 (2415-4092) | +6.1% | 3047, 3420, 3240 / 3327, 3247, 3254 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 2121 (1721-2510) | 1873 (1778-2182) | -11.7% | 2180, 2110, 2057 / 1997, 1869, 1856 | separated, inside spread |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 105.5 (105.1-300.9) | 105.5 (104.6-106.7) | -0.1% | 105.3, 105.5, 203.2 / 106, 105, 105.9 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / rust | 154.3 (149.9-156.4) | 155.2 (148.3-317.1) | +0.5% | 152.4, 155.1, 153.7 / 314.1, 153.1, 151.3 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 9321 (8428-1.033e+04) | 9266 (7462-9726) | -0.6% | 9848, 8745, 9512 / 8213, 9695, 9266 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / rust | 2967 (2680-3859) | 3098 (2673-3968) | +4.4% | 2838, 3380, 3280 / 3276, 3321, 3098 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 440.1 (85.95-448.3) | 265.4 (85.94-448.4) | -39.7% | 267.8, 440.6, 264.9 / 267.9, 443.6, 86.01 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 140.3 (138.8-141.5) | 138.9 (138.2-140.5) | -1.0% | 139.4, 140, 141.3 / 139.3, 138.9, 139.3 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 1859 (1689-2026) | 1815 (1715-2004) | -2.4% | 1839, 1963, 1783 / 1815, 1860, 1833 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 2506 (2205-2654) | 2422 (2111-2642) | -3.4% | 2385, 2506, 2480 / 2599, 2130, 2448 | within noise |
| dense 10 x 30 forward / numpy | 8.118 (8.019-8.182) | 8.131 (8.056-8.171) | +0.2% | 8.133, 8.07, 8.13 / 8.114, 8.12, 8.131 | within noise |
| dense 10 x 30 forward / rust | 0.6275 (0.6192-0.6392) | 0.6229 (0.6207-0.635) | -0.7% | 0.6233, 0.6243, 0.6377 / 0.6278, 0.6212, 0.6291 | within noise |
| dense 10 x 30 downstream / numpy | 1.833 (1.803-1.842) | 1.831 (1.809-1.864) | -0.1% | 1.842, 1.82, 1.815 / 1.822, 1.836, 1.835 | within noise |
| dense 10 x 30 downstream / rust | 0.3954 (0.3847-0.425) | 0.3911 (0.3849-0.4094) | -1.1% | 0.4061, 0.3965, 0.3926 / 0.4022, 0.3907, 0.386 | within noise |
| dense 10 x 30 hidden_delta / numpy | 4.545 (4.51-4.588) | 4.585 (4.496-4.634) | +0.9% | 4.566, 4.558, 4.521 / 4.499, 4.63, 4.585 | within noise |
| dense 10 x 30 hidden_delta / rust | 0.7787 (0.7409-0.8228) | 0.8034 (0.7841-0.8188) | +3.2% | 0.7774, 0.7876, 0.7741 / 0.8049, 0.8034, 0.7987 | separated, inside spread |
| dense 10 x 30 accumulate_gradient / numpy | 5.262 (5.246-5.288) | 5.287 (5.278-5.338) | +0.5% | 5.25, 5.273, 5.267 / 5.283, 5.285, 5.314 | separated, inside spread |
| dense 10 x 30 accumulate_gradient / rust | 0.7789 (0.756-0.7885) | 0.7736 (0.763-0.7903) | -0.7% | 0.7789, 0.7752, 0.7723 / 0.7722, 0.7684, 0.7837 | within noise |
| dense 10 x 30 apply_accumulated_gradient / numpy | 8.919 (8.825-9.1) | 8.965 (8.818-9.117) | +0.5% | 8.963, 8.887, 8.991 / 8.983, 8.881, 9.046 | within noise |
| dense 10 x 30 apply_accumulated_gradient / rust | 4.095 (4.069-4.102) | 4.03 (4.016-4.07) | -1.6% | 4.092, 4.1, 4.083 / 4.046, 4.046, 4.022 | consistent |
| dense 10 x 30 sgd step / numpy | 15.03 (15-15.18) | 15.02 (14.97-15.3) | -0.1% | 15.11, 15.01, 15.06 / 15.16, 15.14, 15 | within noise |
| dense 10 x 30 sgd step / rust | 0.9266 (0.9194-0.9347) | 0.9157 (0.9132-1.022) | -1.2% | 0.9227, 0.9347, 0.9241 / 0.9142, 0.969, 0.9162 | within noise |
| dense 10 x 30 forward_batch b32 / numpy | 19.49 (19.35-19.73) | 19.46 (19.39-19.51) | -0.1% | 19.49, 19.42, 19.6 / 19.49, 19.43, 19.45 | within noise |
| dense 10 x 30 forward_batch b32 / rust | 7.297 (7.287-7.312) | 7.29 (7.282-7.304) | -0.1% | 7.288, 7.303, 7.305 / 7.286, 7.297, 7.293 | within noise |
| dense 10 x 30 forward_batch b512 / numpy | 151.6 (151.4-152.8) | 151.6 (151.1-151.9) | -0.0% | 152.1, 151.6, 151.6 / 151.2, 151.6, 151.8 | within noise |
| dense 10 x 30 forward_batch b512 / rust | 107.6 (107.4-107.7) | 107.5 (107.5-107.7) | -0.0% | 107.6, 107.5, 107.6 / 107.5, 107.5, 107.7 | within noise |
| dense 10 x 30 downstream_batch b32 / numpy | 5.945 (5.902-6.01) | 5.918 (5.901-5.948) | -0.5% | 5.984, 5.917, 5.961 / 5.942, 5.91, 5.911 | within noise |
| dense 10 x 30 downstream_batch b32 / rust | 3.229 (3.223-3.25) | 3.232 (3.222-3.238) | +0.1% | 3.226, 3.238, 3.237 / 3.231, 3.226, 3.237 | within noise |
| dense 10 x 30 downstream_batch b512 / numpy | 64.73 (64.53-64.83) | 64.72 (64.57-64.89) | -0.0% | 64.79, 64.56, 64.75 / 64.67, 64.72, 64.78 | within noise |
| dense 10 x 30 downstream_batch b512 / rust | 46.32 (46.07-46.35) | 46.2 (46.06-46.36) | -0.2% | 46.13, 46.32, 46.34 / 46.21, 46.21, 46.2 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 10.44 (10.36-10.48) | 10.45 (10.37-10.53) | +0.1% | 10.46, 10.37, 10.44 / 10.45, 10.45, 10.44 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 4.099 (4.077-4.119) | 4.098 (4.079-4.12) | -0.0% | 4.1, 4.089, 4.106 / 4.105, 4.088, 4.105 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 93.02 (91.94-94.92) | 93.52 (91.93-95.4) | +0.5% | 92.79, 93.02, 93.48 / 94.06, 93.67, 92.82 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / rust | 54.94 (54.6-55.5) | 54.93 (54.69-55.57) | -0.0% | 54.61, 54.95, 55.24 / 55.16, 54.97, 54.91 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 9.626 (9.506-9.676) | 9.586 (9.536-9.804) | -0.4% | 9.565, 9.62, 9.639 / 9.685, 9.574, 9.576 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 4.237 (4.223-4.243) | 4.287 (4.273-4.387) | +1.2% | 4.241, 4.231, 4.231 / 4.33, 4.283, 4.292 | separated, inside spread |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 47.79 (47.62-48.05) | 47.92 (47.62-48.2) | +0.3% | 47.69, 47.87, 47.85 / 47.92, 47.91, 47.87 | separated, inside spread |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 59.01 (58.83-59.16) | 54.41 (54.3-54.59) | -7.8% | 59.09, 59.01, 58.91 / 54.42, 54.32, 54.5 | consistent |
| conv 28x28, 8 ch forward / numpy | 85.6 (84.82-86.07) | 85.31 (84.88-108.5) | -0.3% | 85.37, 85.72, 85.6 / 96.94, 85.28, 85.08 | within noise |
| conv 28x28, 8 ch forward / rust | 46.78 (46.72-46.82) | 46.73 (46.7-46.78) | -0.1% | 46.77, 46.78, 46.77 / 46.73, 46.7, 46.76 | separated, inside spread |
| conv 28x28, 8 ch downstream / numpy | 71.88 (71.1-72.76) | 70.69 (70.46-71.02) | -1.7% | 71.93, 71.88, 71.78 / 70.76, 70.65, 70.75 | consistent |
| conv 28x28, 8 ch downstream / rust | 42.02 (41.81-42.19) | 45.05 (44.88-45.19) | +7.2% | 42, 42.01, 42.03 / 45.14, 44.95, 45.05 | consistent |
| conv 28x28, 8 ch accumulate_gradient / numpy | 57.94 (57.72-60.29) | 60.24 (57.87-60.48) | +4.0% | 57.75, 57.94, 59.26 / 59.11, 59.29, 60.31 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 30.28 (30.26-30.3) | 31.56 (31.51-31.61) | +4.2% | 30.29, 30.27, 30.28 / 31.56, 31.58, 31.53 | consistent |
| conv 28x28, 8 ch forward_batch b32 / numpy | 4227 (3819-5240) | 4640 (4179-5586) | +9.8% | 4530, 4401, 4227 / 4622, 4333, 5189 | within noise |
| conv 28x28, 8 ch forward_batch b32 / rust | 1664 (1567-1914) | 1610 (1541-1811) | -3.3% | 1630, 1812, 1634 / 1553, 1610, 1800 | within noise |
| conv 28x28, 8 ch forward_batch b512 / numpy | 7.038e+04 (6.9e+04-7.253e+04) | 7.13e+04 (7.054e+04-7.393e+04) | +1.3% | 6.919e+04, 7.038e+04, 7.221e+04 / 7.093e+04, 7.234e+04, 7.184e+04 | within noise |
| conv 28x28, 8 ch forward_batch b512 / rust | 3.272e+04 (3.211e+04-3.35e+04) | 3.271e+04 (3.194e+04-3.47e+04) | -0.0% | 3.296e+04, 3.272e+04, 3.243e+04 / 3.255e+04, 3.233e+04, 3.462e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 1607 (1468-1762) | 1711 (1472-1915) | +6.5% | 1565, 1615, 1610 / 1904, 1711, 1533 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / rust | 2870 (2048-3235) | 1384 (1375-1385) | -51.8% | 2874, 2088, 3085 / 1384, 1383, 1380 | separated, inside spread |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 5.354e+04 (5.133e+04-5.897e+04) | 5.392e+04 (5.156e+04-5.68e+04) | +0.7% | 5.225e+04, 5.626e+04, 5.424e+04 / 5.27e+04, 5.325e+04, 5.58e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / rust | 5.146e+04 (4.986e+04-5.316e+04) | 1.053e+04 (9420-1.11e+04) | -79.5% | 5.01e+04, 5.277e+04, 5.146e+04 / 1.025e+04, 1.052e+04, 1.079e+04 | consistent |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 2246 (2244-2319) | 2285 (2240-2442) | +1.7% | 2246, 2281, 2281 / 2285, 2345, 2282 | separated, inside spread |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 1141 (1104-1470) | 1340 (1177-1521) | +17.4% | 1154, 1287, 1138 / 1350, 1360, 1323 | separated, inside spread |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 3.736e+04 (3.704e+04-3.82e+04) | 3.773e+04 (3.717e+04-3.829e+04) | +1.0% | 3.762e+04, 3.715e+04, 3.756e+04 / 3.772e+04, 3.72e+04, 3.827e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 2.807e+04 (2.783e+04-3.021e+04) | 2.818e+04 (2.764e+04-3.333e+04) | +0.4% | 2.795e+04, 2.906e+04, 2.893e+04 / 3.022e+04, 2.797e+04, 3.069e+04 | within noise |
| conv 8x8, 8 ch forward / numpy | 34.83 (34.57-36.5) | 34.9 (34.43-35.27) | +0.2% | 34.7, 34.91, 35.65 / 34.94, 34.97, 34.66 | within noise |
| conv 8x8, 8 ch forward / rust | 3.401 (3.373-3.424) | 3.335 (3.328-3.351) | -1.9% | 3.401, 3.398, 3.4 / 3.335, 3.336, 3.339 | consistent |
| conv 8x8, 8 ch downstream / numpy | 39.95 (39.57-40.92) | 39.94 (39.7-40.6) | -0.0% | 40.25, 39.9, 40.24 / 40.17, 40.13, 39.84 | within noise |
| conv 8x8, 8 ch downstream / rust | 2.806 (2.761-2.814) | 2.927 (2.919-2.935) | +4.3% | 2.8, 2.809, 2.784 / 2.927, 2.928, 2.925 | consistent |
| conv 8x8, 8 ch accumulate_gradient / numpy | 12.52 (12.36-12.84) | 12.45 (12.37-12.96) | -0.6% | 12.44, 12.48, 12.72 / 12.79, 12.44, 12.39 | within noise |
| conv 8x8, 8 ch accumulate_gradient / rust | 2.312 (2.311-2.318) | 2.427 (2.421-2.44) | +5.0% | 2.315, 2.311, 2.315 / 2.433, 2.427, 2.427 | consistent |
| conv 8x8, 8 ch forward_batch b32 / numpy | 129.5 (128.3-157.7) | 129 (128-130.8) | -0.4% | 129.6, 129.4, 143 / 128.7, 130.4, 128.5 | within noise |
| conv 8x8, 8 ch forward_batch b32 / rust | 80.14 (80.02-80.38) | 80.05 (79.95-80.46) | -0.1% | 80.16, 80.08, 80.2 / 80.02, 80.35, 79.98 | within noise |
| conv 8x8, 8 ch forward_batch b512 / numpy | 3879 (3245-4516) | 3780 (3554-4453) | -2.6% | 4217, 3722, 3616 / 4108, 3740, 3889 | within noise |
| conv 8x8, 8 ch forward_batch b512 / rust | 1540 (1422-1914) | 1548 (1464-1935) | +0.5% | 1540, 1776, 1442 / 1524, 1548, 1699 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 116.1 (115.3-126.6) | 115.9 (114.9-116.6) | -0.2% | 115.7, 121.3, 116 / 115.3, 116.6, 115.6 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / rust | 74.17 (73.92-74.41) | 76.42 (76.26-76.57) | +3.0% | 74.23, 74.17, 74.12 / 76.42, 76.55, 76.28 | consistent |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 1806 (1600-2079) | 1634 (1604-2003) | -9.5% | 1828, 1843, 1804 / 1820, 1748, 1630 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / rust | 1873 (1643-2056) | 1219 (1216-1221) | -34.9% | 1749, 1917, 1960 / 1216, 1219, 1220 | consistent |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 148.4 (148-148.7) | 148.6 (148.5-150.9) | +0.1% | 148.4, 148.3, 148.4 / 148.5, 149.7, 149.7 | separated, inside spread |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 51.97 (51.92-52.03) | 54.3 (54.15-54.31) | +4.5% | 52.03, 51.94, 51.96 / 54.22, 54.31, 54.27 | consistent |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 2343 (2290-2397) | 2328 (2283-2407) | -0.6% | 2379, 2291, 2343 / 2291, 2383, 2331 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 1246 (981.6-1274) | 1145 (991.8-1306) | -8.1% | 1122, 1123, 1257 / 1149, 1006, 1293 | within noise |
| conv 13x13x8, 8 ch forward / numpy | 79.83 (79.53-81.15) | 79.75 (79.27-115.1) | -0.1% | 79.87, 79.61, 80.5 / 79.5, 79.84, 97.32 | within noise |
| conv 13x13x8, 8 ch forward / rust | 48.25 (48.17-48.45) | 47.62 (47.57-47.79) | -1.3% | 48.19, 48.36, 48.33 / 47.58, 47.66, 47.73 | consistent |
| conv 13x13x8, 8 ch downstream / numpy | 89.85 (89.28-90.08) | 89.33 (88.97-91.51) | -0.6% | 89.78, 89.68, 89.91 / 90.34, 89.25, 89.88 | within noise |
| conv 13x13x8, 8 ch downstream / rust | 32.15 (31.94-32.37) | 33.61 (33.24-33.64) | +4.5% | 32.18, 32.12, 32.17 / 33.62, 33.55, 33.43 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 40.49 (40.04-41.01) | 40.28 (40.21-40.44) | -0.5% | 40.62, 40.57, 40.29 / 40.33, 40.28, 40.32 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 14.85 (14.82-14.87) | 16.33 (16.29-16.37) | +9.9% | 14.85, 14.85, 14.85 / 16.34, 16.34, 16.31 | consistent |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 2477 (2323-2876) | 2465 (2318-2624) | -0.5% | 2458, 2365, 2721 / 2601, 2381, 2465 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 2053 (1978-2225) | 2279 (2058-2561) | +11.0% | 2053, 2200, 2005 / 2242, 2357, 2255 | separated, inside spread |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 5.076e+04 (4.802e+04-5.184e+04) | 4.965e+04 (4.828e+04-5.144e+04) | -2.2% | 5.006e+04, 5.076e+04, 4.987e+04 / 4.929e+04, 4.988e+04, 4.986e+04 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 5.076e+04 (4.813e+04-5.219e+04) | 5.365e+04 (5.022e+04-5.499e+04) | +5.7% | 5.088e+04, 4.922e+04, 5.164e+04 / 5.261e+04, 5.351e+04, 5.365e+04 | separated, inside spread |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 4337 (3981-4787) | 4041 (3998-4288) | -6.8% | 4569, 4303, 4152 / 4068, 4016, 4144 | separated, inside spread |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 1287 (1252-1326) | 1011 (1010-1016) | -21.5% | 1315, 1262, 1289 / 1010, 1013, 1014 | consistent |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 1.104e+05 (1.074e+05-1.194e+05) | 1.155e+05 (1.081e+05-1.187e+05) | +4.6% | 1.085e+05, 1.135e+05, 1.137e+05 / 1.129e+05, 1.134e+05, 1.18e+05 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 4.883e+04 (4.773e+04-5.136e+04) | 6445 (6106-6524) | -86.8% | 4.791e+04, 4.974e+04, 4.97e+04 / 6445, 6462, 6315 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 1135 (1117-1144) | 1133 (1126-1143) | -0.2% | 1134, 1140, 1129 / 1132, 1133, 1134 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 604.4 (589.3-611.2) | 641.5 (635.9-651.5) | +6.1% | 607.6, 602.6, 597.2 / 640.7, 645.7, 641.5 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.837e+04 (1.83e+04-1.865e+04) | 1.834e+04 (1.828e+04-1.849e+04) | -0.2% | 1.844e+04, 1.831e+04, 1.851e+04 / 1.834e+04, 1.832e+04, 1.841e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 1.236e+04 (1.112e+04-1.254e+04) | 1.316e+04 (1.223e+04-1.371e+04) | +6.5% | 1.239e+04, 1.237e+04, 1.178e+04 / 1.348e+04, 1.29e+04, 1.294e+04 | separated, inside spread |
| conv 26x26x8/2, 8 ch forward / numpy | 90.06 (89.58-91.01) | 89.76 (89.23-114.6) | -0.3% | 89.91, 89.87, 90.69 / 102.2, 89.97, 89.48 | within noise |
| conv 26x26x8/2, 8 ch forward / rust | 57.26 (57.04-57.44) | 56.48 (56.44-56.83) | -1.4% | 57.43, 57.05, 57.26 / 56.6, 56.64, 56.48 | consistent |
| conv 26x26x8/2, 8 ch downstream / numpy | 103.6 (102.5-103.9) | 103.1 (102.6-103.8) | -0.5% | 103.5, 103.7, 103.1 / 103.4, 102.7, 103.3 | within noise |
| conv 26x26x8/2, 8 ch downstream / rust | 38.67 (38.16-38.97) | 40.36 (39.7-40.46) | +4.4% | 38.71, 38.39, 38.81 / 40.13, 40.08, 40.37 | consistent |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 47.64 (47.12-48.6) | 47.85 (47.52-48.05) | +0.4% | 47.72, 47.86, 47.56 / 47.63, 47.91, 47.98 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 17.44 (17.4-17.49) | 19.28 (19.2-19.31) | +10.5% | 17.44, 17.48, 17.41 / 19.29, 19.26, 19.27 | consistent |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 3467 (3066-3705) | 3386 (3062-3481) | -2.3% | 3554, 3591, 3104 / 3269, 3386, 3363 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 2768 (2711-3045) | 2680 (2494-2908) | -3.2% | 2934, 2726, 2768 / 2636, 2701, 2680 | separated, inside spread |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 6.309e+04 (6.086e+04-6.677e+04) | 6.381e+04 (6.259e+04-6.607e+04) | +1.1% | 6.259e+04, 6.345e+04, 6.381e+04 / 6.41e+04, 6.433e+04, 6.381e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 5.908e+04 (5.799e+04-6.173e+04) | 6.334e+04 (6.132e+04-6.732e+04) | +7.2% | 6.014e+04, 5.908e+04, 5.914e+04 / 6.238e+04, 6.264e+04, 6.544e+04 | separated, inside spread |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 8910 (7691-9026) | 8407 (7604-8943) | -5.6% | 8987, 8789, 8318 / 8407, 8251, 8274 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 3672 (3103-4077) | 1250 (1231-1257) | -66.0% | 3543, 3428, 3881 / 1250, 1231, 1253 | consistent |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 1.861e+05 (1.822e+05-1.913e+05) | 1.865e+05 (1.845e+05-1.937e+05) | +0.2% | 1.888e+05, 1.869e+05, 1.84e+05 / 1.867e+05, 1.894e+05, 1.862e+05 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 6.906e+04 (6.818e+04-7.046e+04) | 2.387e+04 (2.205e+04-2.802e+04) | -65.4% | 6.932e+04, 6.938e+04, 6.867e+04 / 2.662e+04, 2.432e+04, 2.228e+04 | consistent |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 1377 (1371-1406) | 1381 (1370-1392) | +0.3% | 1376, 1395, 1374 / 1382, 1375, 1387 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 771.4 (664.2-783.9) | 823.4 (756.1-838.6) | +6.7% | 783.2, 730.7, 712.4 / 797.4, 823.4, 806.4 | separated, inside spread |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 2.225e+04 (2.211e+04-2.252e+04) | 2.221e+04 (2.217e+04-2.244e+04) | -0.2% | 2.236e+04, 2.237e+04, 2.218e+04 / 2.231e+04, 2.22e+04, 2.221e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 1.447e+04 (1.305e+04-1.638e+04) | 1.481e+04 (1.347e+04-1.552e+04) | +2.4% | 1.447e+04, 1.547e+04, 1.371e+04 / 1.468e+04, 1.534e+04, 1.396e+04 | within noise |
| conv 26x26x8, 8 ch forward / numpy | 245.8 (245-247.2) | 246.1 (243.9-247.2) | +0.1% | 245.1, 246.8, 246.1 / 246.4, 245.2, 245.7 | within noise |
| conv 26x26x8, 8 ch forward / rust | 222.1 (221.4-223.3) | 221.6 (221.4-222.6) | -0.3% | 221.9, 222.8, 222 / 221.4, 222.1, 222 | within noise |
| conv 26x26x8, 8 ch downstream / numpy | 256.2 (252.6-258.6) | 254.6 (253.1-257.6) | -0.6% | 255.3, 256.2, 255.9 / 254.6, 255.3, 254.5 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 145.1 (144.9-146) | 154.5 (154-156.2) | +6.5% | 145, 145.5, 145 / 154.3, 155, 155.4 | consistent |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 161.2 (156.4-161.6) | 159.8 (157.3-161) | -0.9% | 161.5, 161.1, 158.7 / 159.8, 159.8, 158.9 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 65.05 (64.9-65.11) | 72.31 (72.13-72.38) | +11.2% | 65, 65.08, 65.04 / 72.28, 72.23, 72.34 | consistent |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 1.333e+04 (1.177e+04-1.384e+04) | 1.404e+04 (1.236e+04-1.596e+04) | +5.3% | 1.278e+04, 1.347e+04, 1.333e+04 / 1.404e+04, 1.417e+04, 1.388e+04 | separated, inside spread |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 1.144e+04 (1.115e+04-1.262e+04) | 1.157e+04 (1.097e+04-1.377e+04) | +1.2% | 1.192e+04, 1.208e+04, 1.117e+04 / 1.286e+04, 1.115e+04, 1.175e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 2.53e+05 (2.364e+05-2.584e+05) | 2.581e+05 (2.428e+05-2.732e+05) | +2.0% | 2.53e+05, 2.453e+05, 2.5e+05 / 2.488e+05, 2.664e+05, 2.588e+05 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 2.307e+05 (2.257e+05-2.4e+05) | 2.281e+05 (2.269e+05-2.361e+05) | -1.1% | 2.329e+05, 2.303e+05, 2.313e+05 / 2.278e+05, 2.285e+05, 2.317e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 2.779e+04 (2.37e+04-2.907e+04) | 2.592e+04 (2.377e+04-2.827e+04) | -6.7% | 2.893e+04, 2.415e+04, 2.779e+04 / 2.784e+04, 2.394e+04, 2.634e+04 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 1.337e+04 (1.258e+04-1.51e+04) | 3408 (3201-4584) | -74.5% | 1.307e+04, 1.469e+04, 1.302e+04 / 3944, 3350, 3628 | consistent |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 5.185e+05 (5.063e+05-5.222e+05) | 5.244e+05 (4.944e+05-5.349e+05) | +1.1% | 5.142e+05, 5.148e+05, 5.189e+05 / 5.09e+05, 5.301e+05, 5.235e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 2.717e+05 (2.601e+05-2.777e+05) | 6.766e+04 (6.404e+04-8.329e+04) | -75.1% | 2.729e+05, 2.714e+05, 2.689e+05 / 7.122e+04, 6.766e+04, 7.433e+04 | consistent |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 5645 (5618-5659) | 5630 (5599-5700) | -0.3% | 5641, 5638, 5654 / 5658, 5619, 5639 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 3311 (3187-3719) | 3584 (3430-3958) | +8.3% | 3497, 3311, 3411 / 3697, 3699, 3525 | separated, inside spread |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 8.973e+04 (8.87e+04-9.05e+04) | 8.973e+04 (8.898e+04-8.998e+04) | +0.0% | 8.922e+04, 8.924e+04, 9.021e+04 / 8.991e+04, 8.959e+04, 8.93e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 5.838e+04 (5.751e+04-6.139e+04) | 6.256e+04 (5.874e+04-6.87e+04) | +7.2% | 6.009e+04, 5.774e+04, 5.878e+04 / 6.271e+04, 6.233e+04, 6.372e+04 | separated, inside spread |
| pool 26x26, 8 ch forward / numpy | 105.8 (105.3-106.9) | 105.9 (105.5-106.9) | +0.2% | 106.4, 105.7, 105.6 / 105.8, 106.1, 106.4 | within noise |
| pool 26x26, 8 ch forward / rust | 5.315 (5.303-5.323) | 5.216 (5.199-5.248) | -1.9% | 5.314, 5.31, 5.315 / 5.202, 5.216, 5.242 | consistent |
| pool 26x26, 8 ch downstream / numpy | 55.25 (54.73-56.26) | 55.33 (55-56.35) | +0.1% | 55.19, 55.47, 55.5 / 55.4, 55.86, 55.14 | within noise |
| pool 26x26, 8 ch downstream / rust | 4.296 (4.271-4.321) | 4.151 (4.126-4.179) | -3.4% | 4.305, 4.297, 4.283 / 4.165, 4.139, 4.155 | consistent |
| pool 26x26, 8 ch forward_batch b32 / numpy | 2420 (2380-2483) | 2403 (2389-3238) | -0.7% | 2446, 2410, 2418 / 2821, 2400, 2395 | within noise |
| pool 26x26, 8 ch forward_batch b32 / rust | 230.3 (204.3-263.9) | 228.5 (216.8-238.3) | -0.8% | 218.8, 221.7, 248.5 / 223.4, 234.7, 227.5 | within noise |
| pool 26x26, 8 ch forward_batch b512 / numpy | 3.981e+04 (3.906e+04-4.024e+04) | 3.978e+04 (3.941e+04-4.03e+04) | -0.1% | 4.009e+04, 3.947e+04, 3.95e+04 / 3.976e+04, 3.99e+04, 3.974e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 8349 (8065-9538) | 8597 (8205-8878) | +3.0% | 8915, 8116, 8476 / 8738, 8429, 8472 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 985.2 (966.7-998.7) | 1463 (973.6-1536) | +48.5% | 987.3, 983.9, 982 / 1463, 1255, 1228 | consistent |
| pool 26x26, 8 ch downstream_batch b32 / rust | 134.3 (133.9-469.6) | 298.4 (129.8-476.8) | +122.1% | 134.2, 301.5, 301.9 / 303.3, 298.3, 302.5 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 5.768e+04 (5.248e+04-6.181e+04) | 5.53e+04 (5.096e+04-5.802e+04) | -4.1% | 5.632e+04, 5.557e+04, 6.151e+04 / 5.521e+04, 5.632e+04, 5.449e+04 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / rust | 1.981e+04 (1.912e+04-2.097e+04) | 1.975e+04 (1.91e+04-2.041e+04) | -0.3% | 2.062e+04, 1.978e+04, 1.931e+04 / 1.919e+04, 2.012e+04, 2.002e+04 | within noise |
| pool 6x6, 8 ch forward / numpy | 39.73 (39.47-41.25) | 39.73 (39.2-40.61) | -0.0% | 40.45, 39.65, 39.83 / 39.84, 39.94, 39.43 | within noise |
| pool 6x6, 8 ch forward / rust | 0.7926 (0.7894-0.795) | 0.7642 (0.7582-0.7666) | -3.6% | 0.7939, 0.7911, 0.7914 / 0.7642, 0.7658, 0.76 | consistent |
| pool 6x6, 8 ch downstream / numpy | 32.56 (32.34-33.19) | 32.63 (32.56-33.54) | +0.2% | 32.56, 32.9, 32.39 / 32.72, 32.63, 33.05 | within noise |
| pool 6x6, 8 ch downstream / rust | 0.82 (0.8031-0.841) | 0.6671 (0.6593-0.6775) | -18.6% | 0.8222, 0.8143, 0.8275 / 0.6673, 0.6725, 0.663 | consistent |
| pool 6x6, 8 ch forward_batch b32 / numpy | 167.9 (167.4-171.1) | 168.3 (167.8-168.6) | +0.2% | 169.6, 168.5, 167.5 / 168.1, 168.5, 168.1 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 10.61 (10.6-10.64) | 10.57 (10.55-10.59) | -0.3% | 10.62, 10.61, 10.61 / 10.55, 10.57, 10.59 | separated, inside spread |
| pool 6x6, 8 ch forward_batch b512 / numpy | 2207 (2181-2538) | 2198 (2174-2965) | -0.4% | 2377, 2188, 2362 / 2177, 2240, 2581 | within noise |
| pool 6x6, 8 ch forward_batch b512 / rust | 165.4 (165-165.6) | 165.7 (165.2-173.6) | +0.2% | 165.1, 165.5, 165.4 / 167, 165.7, 169.4 | separated, inside spread |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 86 (85.17-86.37) | 85.76 (84.97-86.65) | -0.3% | 86.15, 85.58, 86.02 / 86.46, 85.04, 85.9 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / rust | 12.11 (12.08-12.3) | 7.843 (7.837-7.875) | -35.2% | 12.11, 12.11, 12.19 / 7.863, 7.842, 7.84 | consistent |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 951.3 (936.1-954.1) | 938.7 (932-951.1) | -1.3% | 945.2, 945.1, 952.4 / 945.2, 943.8, 935 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 198.6 (196.1-457.7) | 129 (128.8-385) | -35.0% | 318.6, 198.2, 327.2 / 129, 257, 128.9 | within noise |
| conv tail 32 x 5408 bare downstream b32 / numpy | 1342 (803.4-1422) | 1325 (1193-1523) | -1.3% | 1186, 1342, 1108 / 1240, 1308, 1493 | within noise |
| conv tail 32 x 5408 bare downstream b32 / rust | 1174 (1141-1617) | 1403 (1156-1681) | +19.5% | 1156, 1174, 1408 / 1503, 1519, 1301 | within noise |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3.349e+04 (2.62e+04-3.796e+04) | 3.314e+04 (2.473e+04-4.036e+04) | -1.0% | 3.6e+04, 2.978e+04, 3.073e+04 / 3.612e+04, 2.496e+04, 3.543e+04 | within noise |
| conv tail 32 x 5408 bare downstream b512 / rust | 2.139e+04 (1.94e+04-2.566e+04) | 2e+04 (1.819e+04-2.24e+04) | -6.5% | 2.154e+04, 2.022e+04, 2.392e+04 / 1.837e+04, 2.145e+04, 2.011e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 1205 (990.4-1577) | 1178 (873.9-1592) | -2.3% | 1448, 1021, 1218 / 998.7, 1490, 1094 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / rust | 1162 (1081-1372) | 1182 (1097-1364) | +1.7% | 1160, 1274, 1121 / 1264, 1136, 1269 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 2.115e+04 (1.914e+04-2.221e+04) | 2.167e+04 (2.064e+04-2.331e+04) | +2.4% | 2.141e+04, 2.161e+04, 2.005e+04 / 2.237e+04, 2.154e+04, 2.135e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / rust | 1.884e+04 (1.817e+04-1.984e+04) | 1.864e+04 (1.85e+04-1.923e+04) | -1.1% | 1.85e+04, 1.871e+04, 1.963e+04 / 1.892e+04, 1.88e+04, 1.853e+04 | within noise |
| conv tail 32 x 5408 transpose b32 / numpy | 1.47 (1.458-1.746) | 1.462 (1.45-1.481) | -0.5% | 1.468, 1.47, 1.602 / 1.458, 1.477, 1.458 | within noise |
| conv tail 32 x 5408 transpose b32 / rust | 1.878 (1.87-1.898) | 0.7894 (0.7856-0.7924) | -58.0% | 1.888, 1.875, 1.876 / 0.7904, 0.7865, 0.7908 | consistent |
| conv tail 32 x 5408 transpose b512 / numpy | 30.03 (29.69-30.09) | 29.9 (29.73-30.1) | -0.4% | 29.89, 30.03, 29.92 / 29.91, 29.8, 30.03 | within noise |
| conv tail 32 x 5408 transpose b512 / rust | 26.79 (26.61-27.23) | 11.57 (10.61-11.79) | -56.8% | 26.69, 27.01, 26.91 / 11.43, 11.07, 11.77 | consistent |
| conv tail 32 x 5408 add b32 / numpy | 318.8 (305-423.1) | 342.6 (308.6-403.9) | +7.5% | 329.5, 364, 316.4 / 370.2, 356.2, 333.6 | within noise |
| conv tail 32 x 5408 add b32 / rust | 326.6 (305.3-437.4) | 344.6 (300.8-411.6) | +5.5% | 327.7, 326.6, 371.4 / 382.5, 310.5, 360.4 | within noise |
| conv tail 32 x 5408 add b512 / numpy | 361.1 (296.9-426.5) | 378.4 (320.9-429.5) | +4.8% | 417.3, 354.4, 320.9 / 388, 415.8, 332.5 | within noise |
| conv tail 32 x 5408 add b512 / rust | 310.7 (286.5-333.5) | 378.6 (305.8-452) | +21.9% | 316.7, 298.6, 322.1 / 395.3, 320.3, 429.6 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 2.812 (2.804-2.892) | 2.835 (2.792-2.88) | +0.8% | 2.84, 2.849, 2.809 / 2.834, 2.835, 2.836 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.7771 (0.775-0.7799) | 0.7799 (0.7696-0.7938) | +0.4% | 0.7789, 0.7759, 0.7774 / 0.7882, 0.7799, 0.7739 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 15.85 (15.75-16.14) | 15.85 (15.81-16.18) | +0.0% | 15.79, 15.98, 16 / 16.07, 15.83, 15.84 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 8.696 (8.671-8.736) | 8.68 (8.676-8.714) | -0.2% | 8.696, 8.727, 8.675 / 8.695, 8.68, 8.685 | within noise |
| dense 30 x 784 bare downstream b32 / numpy | 57.63 (56.91-409.8) | 57.85 (56.79-398.9) | +0.4% | 57.37, 57.2, 234 / 58.01, 57.56, 227.9 | within noise |
| dense 30 x 784 bare downstream b32 / rust | 126.7 (125.7-127.9) | 126.8 (125.6-127.9) | +0.1% | 126.7, 127, 126.2 / 126.9, 127.7, 125.6 | within noise |
| dense 30 x 784 bare downstream b512 / numpy | 2909 (2305-3346) | 2890 (2441-3226) | -0.7% | 3195, 2561, 2676 / 2890, 2735, 2888 | within noise |
| dense 30 x 784 bare downstream b512 / rust | 1959 (1700-2517) | 2119 (1561-2509) | +8.2% | 2272, 1830, 2108 / 1832, 2322, 2123 | within noise |
| dense 30 x 784 bare accumulate b32 / numpy | 67.02 (65.59-67.31) | 66.48 (65.74-399.9) | -0.8% | 66.42, 67.12, 67.01 / 233.5, 66, 66.48 | within noise |
| dense 30 x 784 bare accumulate b32 / rust | 125.9 (124.8-126.9) | 125.8 (124.8-127) | -0.1% | 126.3, 126.3, 125.3 / 125.7, 125.9, 126.1 | within noise |
| dense 30 x 784 bare accumulate b512 / numpy | 1727 (1711-1883) | 1764 (1702-1799) | +2.1% | 1808, 1741, 1714 / 1798, 1717, 1764 | within noise |
| dense 30 x 784 bare accumulate b512 / rust | 2458 (2041-2613) | 2357 (2030-2497) | -4.1% | 2058, 2513, 2536 / 2155, 2465, 2365 | within noise |
| dense 30 x 784 transpose b32 / numpy | 1.404 (1.39-1.43) | 1.409 (1.393-1.63) | +0.4% | 1.41, 1.396, 1.411 / 1.521, 1.4, 1.41 | within noise |
| dense 30 x 784 transpose b32 / rust | 1.819 (1.813-1.833) | 0.8123 (0.8068-0.827) | -55.3% | 1.819, 1.823, 1.818 / 0.811, 0.8243, 0.809 | consistent |
| dense 30 x 784 transpose b512 / numpy | 9.008 (8.977-9.059) | 9.015 (8.989-9.059) | +0.1% | 9.028, 9.006, 8.998 / 9, 9.008, 9.039 | within noise |
| dense 30 x 784 transpose b512 / rust | 24.92 (24.86-25) | 10.68 (10.1-10.93) | -57.1% | 24.94, 24.93, 24.92 / 10.81, 10.38, 10.69 | consistent |
| dense 30 x 784 add b32 / numpy | 10.17 (9.963-10.44) | 10.43 (10.14-10.78) | +2.6% | 10.31, 10.05, 10.13 / 10.3, 10.53, 10.43 | within noise |
| dense 30 x 784 add b32 / rust | 10.36 (9.421-11.66) | 9.619 (9.424-11.52) | -7.1% | 11.28, 9.61, 10.33 / 10.66, 9.589, 9.513 | within noise |
| dense 30 x 784 add b512 / numpy | 11.38 (11.02-11.73) | 11.55 (11.36-11.81) | +1.5% | 11.09, 11.42, 11.61 / 11.64, 11.57, 11.5 | within noise |
| dense 30 x 784 add b512 / rust | 9.685 (9.379-9.903) | 9.549 (9.329-9.881) | -1.4% | 9.729, 9.685, 9.618 / 9.595, 9.538, 9.605 | separated, inside spread |
| dense 30 x 784 sum_axis0 b32 / numpy | 2.796 (2.791-2.809) | 2.803 (2.796-2.813) | +0.3% | 2.8, 2.794, 2.797 / 2.806, 2.798, 2.807 | within noise |
| dense 30 x 784 sum_axis0 b32 / rust | 0.7017 (0.6996-0.7051) | 0.7031 (0.6932-0.7068) | +0.2% | 0.6998, 0.7027, 0.7033 / 0.7038, 0.6984, 0.7046 | within noise |
| dense 30 x 784 sum_axis0 b512 / numpy | 15.4 (15.32-15.64) | 15.38 (15.33-15.64) | -0.1% | 15.4, 15.46, 15.51 / 15.35, 15.52, 15.38 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 7.441 (7.426-7.462) | 7.433 (7.43-7.446) | -0.1% | 7.451, 7.434, 7.438 / 7.434, 7.438, 7.433 | within noise |
| dense 10 x 30 bare downstream b32 / numpy | 5.882 (5.865-5.931) | 5.86 (5.852-5.87) | -0.4% | 5.881, 5.898, 5.882 / 5.861, 5.86, 5.862 | consistent, small |
| dense 10 x 30 bare downstream b32 / rust | 3.185 (3.176-3.189) | 3.179 (3.175-3.185) | -0.2% | 3.181, 3.186, 3.183 / 3.179, 3.181, 3.178 | within noise |
| dense 10 x 30 bare downstream b512 / numpy | 64.62 (64.4-64.69) | 64.66 (64.39-64.89) | +0.1% | 64.59, 64.52, 64.69 / 64.56, 64.56, 64.81 | within noise |
| dense 10 x 30 bare downstream b512 / rust | 46.08 (45.65-46.37) | 45.96 (45.66-46.24) | -0.3% | 45.97, 46.28, 45.96 / 45.95, 45.95, 46 | within noise |
| dense 10 x 30 bare accumulate b32 / numpy | 5.042 (5.016-5.119) | 5.047 (5.025-5.064) | +0.1% | 5.032, 5.042, 5.067 / 5.054, 5.044, 5.038 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 2.877 (2.876-2.882) | 2.878 (2.866-2.881) | +0.0% | 2.876, 2.882, 2.877 / 2.871, 2.879, 2.88 | within noise |
| dense 10 x 30 bare accumulate b512 / numpy | 32.65 (32.5-32.76) | 32.53 (32.35-32.59) | -0.4% | 32.63, 32.63, 32.69 / 32.51, 32.56, 32.44 | separated, inside spread |
| dense 10 x 30 bare accumulate b512 / rust | 45.13 (45.08-45.18) | 45.14 (45.1-45.19) | +0.0% | 45.14, 45.13, 45.11 / 45.14, 45.16, 45.14 | within noise |
| dense 10 x 30 transpose b32 / numpy | 0.8895 (0.8865-0.8953) | 0.8937 (0.8847-0.9075) | +0.5% | 0.8893, 0.892, 0.8907 / 0.9006, 0.893, 0.8896 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.7988 (0.7933-0.8031) | 0.5008 (0.4964-0.5099) | -37.3% | 0.7967, 0.7982, 0.8002 / 0.5032, 0.5046, 0.498 | consistent |
| dense 10 x 30 transpose b512 / numpy | 3.396 (3.36-3.474) | 3.381 (3.352-3.496) | -0.4% | 3.438, 3.378, 3.385 / 3.43, 3.42, 3.374 | within noise |
| dense 10 x 30 transpose b512 / rust | 8.588 (8.502-8.595) | 3.815 (3.755-3.944) | -55.6% | 8.544, 8.55, 8.59 / 3.849, 3.877, 3.79 | consistent |
| dense 10 x 30 add b32 / numpy | 0.8956 (0.8897-0.9082) | 0.906 (0.8948-0.9172) | +1.2% | 0.8999, 0.8942, 0.8972 / 0.9165, 0.9041, 0.8968 | within noise |
| dense 10 x 30 add b32 / rust | 0.3861 (0.3819-0.3897) | 0.3837 (0.378-0.3897) | -0.6% | 0.3821, 0.3861, 0.3891 / 0.3849, 0.3808, 0.3859 | within noise |
| dense 10 x 30 add b512 / numpy | 0.9179 (0.9123-0.9229) | 0.9173 (0.9077-0.924) | -0.1% | 0.9179, 0.9127, 0.9214 / 0.917, 0.9179, 0.9159 | within noise |
| dense 10 x 30 add b512 / rust | 0.4069 (0.4033-0.4128) | 0.4088 (0.3985-0.4259) | +0.5% | 0.4068, 0.4045, 0.4105 / 0.4055, 0.4104, 0.4122 | within noise |
| dense 10 x 30 sum_axis0 b32 / numpy | 2.463 (2.441-2.466) | 2.453 (2.443-2.477) | -0.4% | 2.465, 2.456, 2.452 / 2.445, 2.458, 2.464 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.5471 (0.5437-0.5509) | 0.545 (0.5439-0.5489) | -0.4% | 0.5437, 0.5508, 0.5471 / 0.5468, 0.5456, 0.5439 | within noise |
| dense 10 x 30 sum_axis0 b512 / numpy | 12.22 (12.17-12.63) | 12.19 (12.18-12.6) | -0.2% | 12.19, 12.43, 12.2 / 12.2, 12.18, 12.4 | within noise |
| dense 10 x 30 sum_axis0 b512 / rust | 4.96 (4.956-4.976) | 4.959 (4.956-4.964) | -0.0% | 4.968, 4.96, 4.96 / 4.959, 4.961, 4.96 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 747.7 (744.7-761.4) | 747.9 (745.3-1148) | +0.0% | 750.8, 747.7, 753.6 / 751.4, 747.9, 946.8 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 829.5 (828.3-836.8) | 810.9 (810.2-813.3) | -2.2% | 829.4, 833.1, 829.1 / 812.1, 811, 810.5 | consistent |
| attention 16 x 32 forward_batch b512 / numpy | 2.278e+04 (2.094e+04-2.518e+04) | 2.282e+04 (2.178e+04-2.392e+04) | +0.2% | 2.194e+04, 2.39e+04, 2.234e+04 / 2.35e+04, 2.264e+04, 2.232e+04 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 1.725e+04 (1.636e+04-1.797e+04) | 1.662e+04 (1.608e+04-1.745e+04) | -3.6% | 1.716e+04, 1.727e+04, 1.693e+04 / 1.659e+04, 1.676e+04, 1.664e+04 | separated, inside spread |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 759.1 (756.5-1234) | 760.5 (753.9-767.1) | +0.2% | 761.4, 757.2, 996.2 / 760.5, 766, 755 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / rust | 795.7 (793.6-797.2) | 761.3 (759.8-763.7) | -4.3% | 794.7, 796.9, 794.8 / 761.5, 760.7, 761.9 | consistent |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 2.749e+04 (2.606e+04-2.936e+04) | 2.674e+04 (2.589e+04-2.77e+04) | -2.7% | 2.908e+04, 2.695e+04, 2.703e+04 / 2.765e+04, 2.602e+04, 2.674e+04 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / rust | 1.978e+04 (1.87e+04-2.079e+04) | 1.805e+04 (1.741e+04-2.043e+04) | -8.8% | 2.049e+04, 1.974e+04, 1.903e+04 / 1.928e+04, 1.764e+04, 1.813e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 595.9 (588.9-2094) | 595.9 (591.4-599.9) | -0.0% | 594, 593.1, 1344 / 591.4, 595.9, 599.8 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 513.2 (511-515.5) | 460 (458.2-463.6) | -10.4% | 511.5, 515.2, 512.9 / 459.2, 463.2, 459.7 | consistent |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 3.749e+04 (3.38e+04-4.207e+04) | 4.198e+04 (3.376e+04-4.404e+04) | +12.0% | 3.803e+04, 3.401e+04, 4.058e+04 / 3.442e+04, 4.226e+04, 4.309e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 3.033e+04 (2.293e+04-3.705e+04) | 3.288e+04 (2.788e+04-3.637e+04) | +8.4% | 2.597e+04, 3.199e+04, 3.426e+04 / 3.353e+04, 3.044e+04, 3.342e+04 | within noise |
