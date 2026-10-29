Old `6dcd34c` against new `6dcd34c`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `10dfec9` (extension sha256 `dd311e7a023b`) and new crate `13fe89a` (extension sha256 `ecff7892e7cb`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (raspberry-pi-5.json); passes peaked at 57.3-59.0 C; max 1-min load 1.36 (measured just after this run's crate builds); busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / conv tail 32 x 5408 sgd step / rust +65.2% (120.5 -> 199.1 µs)
- consistent: per call / pool 6x6, 8 ch downstream_batch b32 / rust +21.1% (7.843 -> 9.496 µs)
- consistent: per call / dense 10 x 30 downstream_batch b512 / rust -15.2% (54.69 -> 46.39 µs)
- consistent: per call / dense 10 x 30 bare downstream b512 / rust -14.9% (54.44 -> 46.33 µs)
- consistent: per call / dense 10 x 30 downstream_batch b32 / rust -13.9% (3.767 -> 3.244 µs)
- consistent: per call / dense 10 x 30 bare downstream b32 / rust -13.9% (3.71 -> 3.196 µs)
- consistent: per call / dense 10 x 30 hidden_delta_batch b512 / rust -13.2% (63.26 -> 54.92 µs)
- consistent: per call / conv 8x8, 8 ch forward_batch b512 / rust -12.0% (1916 -> 1687 µs)
- consistent: per call / dense 10 x 30 hidden_delta_batch b32 / rust -11.1% (4.646 -> 4.131 µs)
- consistent: per call / dense 10 x 30 bare accumulate b32 / rust -10.8% (3.25 -> 2.899 µs)
- ... 32 more consistent rows (report --md)
- 228 rows within noise (26 separated inside their spread), max |Δ| 71.0%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 78.28 (76.94-79.76) | 78.52 (77.84-79.92) | +0.3% | 78.76, 78.28, 78.35 / 78.43, 78.41, 79.01 | within noise |
| conv tail 32 x 5408 forward / rust | 65.39 (54.49-76.96) | 76.77 (54.36-77.19) | +17.4% | 67.42, 65.72, 64.72 / 76.97, 55.5, 76.82 | within noise |
| conv tail 32 x 5408 downstream / numpy | 92.17 (91.48-92.46) | 91.55 (90.98-92.51) | -0.7% | 92.17, 91.89, 91.97 / 91.43, 91.26, 92.07 | within noise |
| conv tail 32 x 5408 downstream / rust | 81.35 (74.1-88.91) | 105.2 (76.21-106.2) | +29.4% | 88.54, 81.51, 74.3 / 106.1, 82.11, 105.2 | within noise |
| conv tail 32 x 5408 hidden_delta / numpy | 104.2 (103.2-105.9) | 104.1 (103.5-104.9) | -0.1% | 103.8, 103.7, 105.1 / 103.9, 104, 104.6 | within noise |
| conv tail 32 x 5408 hidden_delta / rust | 110.2 (92.96-111.4) | 88.42 (78.4-110.3) | -19.7% | 110.6, 102, 103.7 / 95.18, 93.9, 87.74 | separated, inside spread |
| conv tail 32 x 5408 accumulate_gradient / numpy | 601 (366.6-865.2) | 852.7 (321.5-934.9) | +41.9% | 377.4, 839.4, 619.4 / 844.8, 628.2, 886.8 | within noise |
| conv tail 32 x 5408 accumulate_gradient / rust | 98.99 (89.58-288.8) | 90.92 (88.6-99.46) | -8.2% | 93.92, 99.82, 189.9 / 90.56, 95.17, 93.66 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 1740 (1536-2084) | 1473 (1282-1616) | -15.3% | 1936, 1784, 1613 / 1537, 1462, 1386 | separated, inside spread |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 443.7 (377.2-631.9) | 555.8 (379.9-769.2) | +25.3% | 507.7, 446.1, 442.8 / 590.5, 489.5, 574.3 | within noise |
| conv tail 32 x 5408 sgd step / numpy | 2331 (2207-2872) | 2348 (2071-3104) | +0.7% | 2291, 2444, 2539 / 2237, 2502, 2588 | within noise |
| conv tail 32 x 5408 sgd step / rust | 120.5 (116.3-123.8) | 199.1 (116.5-284.6) | +65.2% | 122.4, 120.5, 117.3 / 197.2, 201, 199.5 | consistent |
| conv tail 32 x 5408 forward_batch b32 / numpy | 519.1 (510.3-535.7) | 518.3 (505.8-539.1) | -0.1% | 512.3, 530.9, 517.9 / 524.4, 512, 524.5 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 1121 (1108-1140) | 1120 (1102-1128) | -0.1% | 1124, 1113, 1129 / 1127, 1117, 1111 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1.562e+04 (1.456e+04-1.646e+04) | 1.553e+04 (1.51e+04-1.6e+04) | -0.5% | 1.568e+04, 1.612e+04, 1.501e+04 / 1.55e+04, 1.562e+04, 1.548e+04 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 1.208e+04 (1.059e+04-1.282e+04) | 1.207e+04 (1.142e+04-1.356e+04) | -0.1% | 1.179e+04, 1.17e+04, 1.244e+04 / 1.164e+04, 1.247e+04, 1.277e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 1384 (1204-1537) | 1355 (1104-1435) | -2.1% | 1302, 1304, 1470 / 1254, 1383, 1314 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 1293 (1175-1458) | 1447 (1161-1622) | +11.9% | 1293, 1337, 1268 / 1303, 1535, 1436 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 3.541e+04 (2.428e+04-4.59e+04) | 3.454e+04 (2.526e+04-3.995e+04) | -2.4% | 4.242e+04, 3.054e+04, 3.01e+04 / 3.454e+04, 3.052e+04, 3.396e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 1.929e+04 (1.719e+04-2.482e+04) | 1.948e+04 (1.46e+04-2.249e+04) | +1.0% | 2.186e+04, 1.929e+04, 1.861e+04 / 1.948e+04, 1.744e+04, 1.864e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 3051 (2728-4034) | 3454 (3064-3651) | +13.2% | 3381, 3364, 3051 / 3159, 3558, 3534 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 1932 (1605-2032) | 1938 (1549-2105) | +0.3% | 2004, 1742, 1932 / 1983, 2011, 1726 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 7.291e+04 (6.748e+04-8.207e+04) | 6.846e+04 (6.544e+04-7.227e+04) | -6.1% | 6.952e+04, 7.282e+04, 8.196e+04 / 7.084e+04, 6.885e+04, 6.681e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 2.991e+04 (2.779e+04-3.406e+04) | 3.01e+04 (2.694e+04-3.407e+04) | +0.6% | 3.108e+04, 3.093e+04, 2.964e+04 / 3.05e+04, 3.01e+04, 3.118e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 1764 (1559-1934) | 1896 (1451-1997) | +7.5% | 1640, 1720, 1934 / 1544, 1896, 1982 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 2241 (2133-2380) | 2170 (2123-2232) | -3.2% | 2273, 2241, 2194 / 2132, 2226, 2170 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 2.265e+04 (2.195e+04-2.363e+04) | 2.284e+04 (2.225e+04-2.38e+04) | +0.8% | 2.279e+04, 2.298e+04, 2.241e+04 / 2.377e+04, 2.264e+04, 2.249e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 2.004e+04 (1.902e+04-2.048e+04) | 2.013e+04 (1.94e+04-2.136e+04) | +0.5% | 2.02e+04, 1.984e+04, 1.965e+04 / 1.967e+04, 2.068e+04, 2.056e+04 | within noise |
| dense 30 x 784 forward / numpy | 16.29 (16.16-16.53) | 16.19 (16.12-16.32) | -0.6% | 16.34, 16.28, 16.3 / 16.23, 16.26, 16.14 | separated, inside spread |
| dense 30 x 784 forward / rust | 6.474 (6.417-6.546) | 6.475 (6.436-6.55) | +0.0% | 6.465, 6.48, 6.481 / 6.479, 6.493, 6.47 | within noise |
| dense 30 x 784 downstream / numpy | 12.67 (12.65-12.72) | 12.68 (12.67-12.74) | +0.1% | 12.66, 12.69, 12.69 / 12.68, 12.7, 12.71 | within noise |
| dense 30 x 784 downstream / rust | 6.649 (6.292-6.673) | 6.5 (6.297-6.637) | -2.2% | 6.467, 6.647, 6.665 / 6.419, 6.386, 6.586 | within noise |
| dense 30 x 784 hidden_delta / numpy | 17.06 (16.98-17.25) | 17.01 (16.99-17.16) | -0.3% | 17.06, 17.1, 17.11 / 17.04, 17.01, 17.08 | within noise |
| dense 30 x 784 hidden_delta / rust | 7.367 (7.178-7.572) | 7.309 (7.186-7.587) | -0.8% | 7.281, 7.554, 7.274 / 7.309, 7.395, 7.351 | within noise |
| dense 30 x 784 accumulate_gradient / numpy | 42.66 (42.56-42.72) | 42.73 (42.65-42.79) | +0.2% | 42.7, 42.6, 42.66 / 42.78, 42.69, 42.7 | within noise |
| dense 30 x 784 accumulate_gradient / rust | 9.881 (9.851-10.01) | 9.937 (9.869-9.994) | +0.6% | 9.877, 9.917, 9.935 / 9.985, 9.876, 9.937 | within noise |
| dense 30 x 784 apply_accumulated_gradient / numpy | 61.19 (61.07-61.24) | 61.16 (61.11-61.21) | -0.1% | 61.2, 61.14, 61.2 / 61.16, 61.15, 61.16 | within noise |
| dense 30 x 784 apply_accumulated_gradient / rust | 36.77 (36.53-36.95) | 36.33 (36.29-36.47) | -1.2% | 36.79, 36.6, 36.87 / 36.32, 36.32, 36.39 | separated, inside spread |
| dense 30 x 784 sgd step / numpy | 108 (107.7-108.5) | 108 (107.9-108.8) | -0.0% | 107.9, 108.3, 107.9 / 108.4, 108, 107.9 | within noise |
| dense 30 x 784 sgd step / rust | 15.71 (15.64-15.73) | 15.7 (15.66-15.72) | -0.1% | 15.72, 15.72, 15.68 / 15.7, 15.71, 15.69 | within noise |
| dense 30 x 784 forward_batch b32 / numpy | 449.3 (90.79-453.8) | 271.8 (90.89-457.1) | -39.5% | 272.3, 449.3, 272.1 / 273, 271.5, 274 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 117.2 (115-119.4) | 118.9 (115.5-119.7) | +1.4% | 115.2, 117.1, 119.3 / 117.8, 119.4, 117 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 2246 (2146-2405) | 2190 (2092-2620) | -2.5% | 2293, 2209, 2275 / 2108, 2190, 2494 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 972.9 (897.1-1015) | 1023 (936.7-1079) | +5.1% | 946.5, 1004, 943.1 / 1055, 975.6, 996.9 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 391.3 (57.92-400) | 397.7 (57.54-401.1) | +1.6% | 226, 398.2, 223.3 / 227.6, 398.9, 229.6 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 126.2 (125.7-126.8) | 125.3 (124.7-127.4) | -0.8% | 125.8, 126.7, 126.3 / 126.2, 124.9, 126.1 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 3368 (2980-3674) | 3713 (3235-4127) | +10.2% | 3234, 3479, 3327 / 3565, 3728, 3769 | separated, inside spread |
| dense 30 x 784 downstream_batch b512 / rust | 1803 (1656-2303) | 2144 (1667-2432) | +18.9% | 1787, 2040, 1975 / 2429, 1800, 2139 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 104.8 (103.8-296.6) | 105.4 (104.4-300.8) | +0.6% | 200.6, 104.6, 104.8 / 105.1, 203, 105.7 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / rust | 153.8 (144.8-156.4) | 153 (145.2-320.8) | -0.5% | 155.3, 149.9, 149.7 / 234.3, 228.7, 153 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 9274 (7809-1.034e+04) | 9570 (7840-1.1e+04) | +3.2% | 8501, 1.024e+04, 8610 / 8947, 1.001e+04, 9570 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / rust | 3158 (2751-4004) | 3004 (2891-4096) | -4.9% | 3158, 3338, 3490 / 2990, 3229, 3494 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 441.7 (86.74-447.3) | 440.7 (85.8-443.8) | -0.2% | 442.7, 438.8, 265.1 / 263.9, 442, 263.5 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 138.5 (137.7-140.1) | 138.3 (137.9-140.2) | -0.1% | 139.2, 138.8, 138.1 / 138.3, 139.6, 138 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 1873 (1668-1928) | 1891 (1751-1967) | +1.0% | 1831, 1873, 1798 / 1895, 1944, 1803 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 2258 (2156-2673) | 2187 (2091-2615) | -3.1% | 2398, 2220, 2438 / 2127, 2277, 2380 | within noise |
| dense 10 x 30 forward / numpy | 8.137 (8.083-8.258) | 8.156 (8.08-8.336) | +0.2% | 8.133, 8.165, 8.17 / 8.208, 8.135, 8.171 | within noise |
| dense 10 x 30 forward / rust | 0.6312 (0.6237-0.6371) | 0.633 (0.6298-0.661) | +0.3% | 0.6321, 0.6347, 0.6269 / 0.6461, 0.6352, 0.6298 | within noise |
| dense 10 x 30 downstream / numpy | 1.829 (1.8-1.851) | 1.837 (1.816-1.895) | +0.5% | 1.847, 1.818, 1.817 / 1.827, 1.832, 1.871 | within noise |
| dense 10 x 30 downstream / rust | 0.4114 (0.4012-0.4136) | 0.3884 (0.3832-0.397) | -5.6% | 0.403, 0.4122, 0.4121 / 0.3934, 0.3869, 0.3865 | consistent |
| dense 10 x 30 hidden_delta / numpy | 4.54 (4.489-4.599) | 4.536 (4.522-4.603) | -0.1% | 4.567, 4.535, 4.528 / 4.526, 4.539, 4.569 | within noise |
| dense 10 x 30 hidden_delta / rust | 0.856 (0.8401-0.887) | 0.8101 (0.8012-0.8709) | -5.4% | 0.8618, 0.8635, 0.856 / 0.8054, 0.8433, 0.8079 | separated, inside spread |
| dense 10 x 30 accumulate_gradient / numpy | 5.265 (5.227-5.445) | 5.287 (5.258-5.511) | +0.4% | 5.265, 5.347, 5.253 / 5.385, 5.286, 5.323 | within noise |
| dense 10 x 30 accumulate_gradient / rust | 0.7882 (0.7823-0.7988) | 0.7761 (0.7661-0.7941) | -1.5% | 0.7922, 0.7914, 0.784 / 0.7848, 0.7714, 0.7738 | within noise |
| dense 10 x 30 apply_accumulated_gradient / numpy | 8.898 (8.826-8.965) | 8.931 (8.83-9.02) | +0.4% | 8.94, 8.887, 8.854 / 8.875, 8.951, 8.959 | within noise |
| dense 10 x 30 apply_accumulated_gradient / rust | 4.104 (4.095-4.116) | 4.158 (4.143-4.172) | +1.3% | 4.115, 4.099, 4.101 / 4.153, 4.15, 4.17 | consistent |
| dense 10 x 30 sgd step / numpy | 14.97 (14.85-15.04) | 15.03 (14.91-15.42) | +0.4% | 14.93, 15.03, 14.92 / 15.1, 15.19, 15.03 | within noise |
| dense 10 x 30 sgd step / rust | 0.9293 (0.9271-0.9378) | 0.9343 (0.9274-0.95) | +0.5% | 0.9335, 0.9301, 0.9272 / 0.9303, 0.9374, 0.9387 | within noise |
| dense 10 x 30 forward_batch b32 / numpy | 19.43 (19.32-19.68) | 19.44 (19.38-19.61) | +0.0% | 19.54, 19.51, 19.35 / 19.44, 19.49, 19.44 | within noise |
| dense 10 x 30 forward_batch b32 / rust | 7.276 (7.252-7.357) | 7.296 (7.274-7.328) | +0.3% | 7.264, 7.295, 7.308 / 7.293, 7.284, 7.324 | within noise |
| dense 10 x 30 forward_batch b512 / numpy | 151.9 (151.4-153.1) | 151.6 (151.4-152.9) | -0.2% | 151.7, 151.8, 152.7 / 151.6, 152.1, 151.8 | within noise |
| dense 10 x 30 forward_batch b512 / rust | 107.1 (106.9-108) | 107.8 (107.6-108.1) | +0.6% | 107.1, 107.4, 107.5 / 107.7, 107.7, 108 | separated, inside spread |
| dense 10 x 30 downstream_batch b32 / numpy | 5.943 (5.893-5.954) | 5.927 (5.897-5.989) | -0.3% | 5.933, 5.949, 5.924 / 5.942, 5.906, 5.953 | within noise |
| dense 10 x 30 downstream_batch b32 / rust | 3.767 (3.746-3.791) | 3.244 (3.24-3.248) | -13.9% | 3.769, 3.764, 3.767 / 3.245, 3.246, 3.242 | consistent |
| dense 10 x 30 downstream_batch b512 / numpy | 64.74 (64.63-64.98) | 64.77 (64.62-64.88) | +0.0% | 64.73, 64.69, 64.86 / 64.78, 64.67, 64.81 | within noise |
| dense 10 x 30 downstream_batch b512 / rust | 54.69 (54.53-54.84) | 46.39 (46.32-46.76) | -15.2% | 54.81, 54.58, 54.66 / 46.37, 46.35, 46.76 | consistent |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 10.48 (10.37-10.55) | 10.48 (10.41-10.52) | -0.0% | 10.52, 10.48, 10.42 / 10.5, 10.45, 10.44 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 4.646 (4.631-4.653) | 4.131 (4.103-4.144) | -11.1% | 4.638, 4.653, 4.64 / 4.121, 4.122, 4.14 | consistent |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 93.67 (92.5-94.44) | 93.11 (91.89-94.42) | -0.6% | 94.18, 93.27, 93.27 / 92.86, 93.41, 93.19 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / rust | 63.26 (63.09-64.08) | 54.92 (54.87-55.52) | -13.2% | 63.55, 63.58, 63.26 / 54.9, 55.41, 54.9 | consistent |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 9.556 (9.473-9.616) | 9.633 (9.578-9.867) | +0.8% | 9.553, 9.515, 9.593 / 9.755, 9.633, 9.602 | separated, inside spread |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 4.276 (4.258-4.281) | 3.93 (3.917-3.936) | -8.1% | 4.274, 4.269, 4.279 / 3.917, 3.93, 3.936 | consistent |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 47.79 (47.48-47.9) | 47.68 (47.37-47.91) | -0.2% | 47.75, 47.79, 47.67 / 47.72, 47.49, 47.81 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 54.06 (54.01-54.13) | 53.87 (53.84-54.04) | -0.4% | 54.06, 54.07, 54.08 / 53.94, 53.88, 53.85 | consistent, small |
| conv 28x28, 8 ch forward / numpy | 85.43 (84.95-104.5) | 84.91 (84.68-85.97) | -0.6% | 85.23, 94.87, 85.6 / 85.32, 85, 84.91 | within noise |
| conv 28x28, 8 ch forward / rust | 50.72 (50.7-50.78) | 47.21 (47.15-47.51) | -6.9% | 50.71, 50.76, 50.72 / 47.22, 47.19, 47.33 | consistent |
| conv 28x28, 8 ch downstream / numpy | 71.61 (71.06-72.47) | 71.15 (70.31-72.15) | -0.7% | 71.76, 71.52, 71.71 / 71.08, 71.6, 70.77 | within noise |
| conv 28x28, 8 ch downstream / rust | 47.64 (47.62-47.67) | 43.22 (43.14-43.32) | -9.3% | 47.65, 47.63, 47.65 / 43.28, 43.22, 43.19 | consistent |
| conv 28x28, 8 ch accumulate_gradient / numpy | 60.3 (57.94-60.55) | 60.34 (57.8-60.58) | +0.1% | 59.25, 60.43, 59.24 / 60.4, 58.53, 60.48 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 30.37 (30.34-30.39) | 30.2 (30.09-30.25) | -0.6% | 30.38, 30.38, 30.34 / 30.24, 30.17, 30.15 | consistent, small |
| conv 28x28, 8 ch forward_batch b32 / numpy | 4437 (4184-4724) | 4374 (4147-5639) | -1.4% | 4473, 4454, 4313 / 4896, 4590, 4187 | within noise |
| conv 28x28, 8 ch forward_batch b32 / rust | 1862 (1765-2040) | 1612 (1581-1949) | -13.4% | 1902, 1862, 1871 / 1729, 1603, 1777 | separated, inside spread |
| conv 28x28, 8 ch forward_batch b512 / numpy | 7.316e+04 (7.218e+04-7.579e+04) | 7.2e+04 (7.022e+04-7.383e+04) | -1.6% | 7.298e+04, 7.455e+04, 7.395e+04 / 7.132e+04, 7.163e+04, 7.317e+04 | within noise |
| conv 28x28, 8 ch forward_batch b512 / rust | 3.682e+04 (3.587e+04-4.148e+04) | 3.42e+04 (3.321e+04-3.565e+04) | -7.1% | 3.948e+04, 3.812e+04, 3.593e+04 / 3.411e+04, 3.469e+04, 3.399e+04 | separated, inside spread |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 1572 (1462-2018) | 1584 (1487-1920) | +0.8% | 1745, 1753, 1510 / 1605, 1516, 1755 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / rust | 1468 (1467-1471) | 1325 (1320-1329) | -9.8% | 1468, 1469, 1470 / 1328, 1322, 1324 | consistent |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 5.746e+04 (5.348e+04-6.373e+04) | 5.918e+04 (5.786e+04-6.354e+04) | +3.0% | 5.516e+04, 5.904e+04, 5.831e+04 / 6.281e+04, 5.821e+04, 5.897e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / rust | 1.055e+04 (9896-1.305e+04) | 1.025e+04 (1.02e+04-1.057e+04) | -2.8% | 1.097e+04, 1.155e+04, 1.024e+04 / 1.042e+04, 1.021e+04, 1.026e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 2259 (2244-2320) | 2314 (2252-2322) | +2.4% | 2246, 2293, 2285 / 2288, 2314, 2287 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 1156 (1144-1167) | 1147 (1122-1168) | -0.8% | 1161, 1151, 1151 / 1145, 1145, 1147 | separated, inside spread |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 3.72e+04 (3.712e+04-3.783e+04) | 3.813e+04 (3.721e+04-3.828e+04) | +2.5% | 3.718e+04, 3.719e+04, 3.751e+04 / 3.776e+04, 3.771e+04, 3.813e+04 | separated, inside spread |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 3.046e+04 (2.931e+04-3.467e+04) | 3.21e+04 (2.984e+04-3.454e+04) | +5.4% | 2.98e+04, 3.105e+04, 3.266e+04 / 3.152e+04, 3.072e+04, 3.357e+04 | within noise |
| conv 8x8, 8 ch forward / numpy | 34.9 (34.65-36.22) | 34.88 (34.72-35.05) | -0.0% | 35.56, 34.78, 34.97 / 35.03, 34.84, 34.77 | within noise |
| conv 8x8, 8 ch forward / rust | 3.552 (3.548-3.573) | 3.374 (3.369-3.376) | -5.0% | 3.548, 3.552, 3.569 / 3.372, 3.375, 3.375 | consistent |
| conv 8x8, 8 ch downstream / numpy | 39.97 (39.62-40.79) | 39.91 (39.61-40.63) | -0.1% | 40.76, 39.91, 39.75 / 39.87, 39.76, 40.46 | within noise |
| conv 8x8, 8 ch downstream / rust | 3.138 (3.128-3.143) | 2.914 (2.911-2.93) | -7.1% | 3.142, 3.134, 3.135 / 2.913, 2.914, 2.92 | consistent |
| conv 8x8, 8 ch accumulate_gradient / numpy | 12.59 (12.4-12.87) | 12.52 (12.46-12.58) | -0.5% | 12.73, 12.6, 12.43 / 12.51, 12.52, 12.52 | within noise |
| conv 8x8, 8 ch accumulate_gradient / rust | 2.33 (2.322-2.342) | 2.266 (2.256-2.283) | -2.8% | 2.339, 2.328, 2.325 / 2.266, 2.27, 2.271 | consistent |
| conv 8x8, 8 ch forward_batch b32 / numpy | 129.7 (128.4-131) | 128.7 (127.6-129.1) | -0.8% | 128.8, 130, 130.3 / 129, 128.4, 128.4 | within noise |
| conv 8x8, 8 ch forward_batch b32 / rust | 87.21 (86.94-87.46) | 80.75 (80.42-80.91) | -7.4% | 87.19, 87.21, 87.2 / 80.6, 80.77, 80.73 | consistent |
| conv 8x8, 8 ch forward_batch b512 / numpy | 3940 (3484-4715) | 4085 (3258-4977) | +3.7% | 4048, 3507, 4347 / 4117, 3809, 4491 | within noise |
| conv 8x8, 8 ch forward_batch b512 / rust | 1916 (1805-2041) | 1687 (1456-1754) | -12.0% | 1864, 1870, 2008 / 1597, 1687, 1607 | consistent |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 116.2 (115.5-118.1) | 116 (115.4-117.9) | -0.2% | 116, 117.4, 115.9 / 116.8, 115.8, 116.6 | within noise |
| conv 8x8, 8 ch downstream_batch b32 / rust | 82.72 (82.57-82.9) | 76.73 (75.88-76.88) | -7.2% | 82.62, 82.74, 82.79 / 76.29, 76.56, 76.76 | consistent |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 1955 (1600-2016) | 1617 (1595-2012) | -17.3% | 1775, 2013, 1793 / 1816, 1610, 1726 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / rust | 1319 (1316-1320) | 1210 (1209-1223) | -8.2% | 1320, 1318, 1317 / 1217, 1210, 1215 | consistent |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 148.7 (148.3-151.9) | 148.6 (148.2-153.9) | -0.0% | 148.5, 150.2, 148.6 / 148.6, 151.1, 148.7 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 52.15 (51.95-52.17) | 51.87 (51.74-51.9) | -0.5% | 52.15, 52.16, 52.04 / 51.82, 51.84, 51.89 | consistent, small |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 2370 (2284-2585) | 2363 (2300-2401) | -0.3% | 2369, 2484, 2326 / 2383, 2345, 2330 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 1122 (986.9-1281) | 990 (979-1307) | -11.8% | 1133, 1265, 988.5 / 1293, 986.7, 983.2 | within noise |
| conv 13x13x8, 8 ch forward / numpy | 79.83 (79.75-81.15) | 80.08 (79.23-80.95) | +0.3% | 80.5, 79.85, 79.77 / 80.21, 79.51, 80.49 | within noise |
| conv 13x13x8, 8 ch forward / rust | 50.37 (50.29-53.71) | 48.23 (48.06-48.42) | -4.2% | 50.33, 52.02, 50.51 / 48.23, 48.4, 48.08 | consistent |
| conv 13x13x8, 8 ch downstream / numpy | 89.75 (88.64-93.14) | 89.51 (88.79-91.48) | -0.3% | 89.57, 89.24, 91.42 / 90.58, 88.81, 89.51 | within noise |
| conv 13x13x8, 8 ch downstream / rust | 33.33 (33.2-33.63) | 32.68 (32.62-32.97) | -1.9% | 33.48, 33.43, 33.22 / 32.64, 32.92, 32.68 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 40.32 (40.23-41.03) | 40.39 (40-40.99) | +0.2% | 40.65, 40.3, 40.46 / 40.38, 40.67, 40.3 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 15.87 (15.85-15.92) | 14.78 (14.76-14.82) | -6.9% | 15.87, 15.91, 15.86 / 14.77, 14.79, 14.78 | consistent |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 2415 (2284-2531) | 2439 (2383-2612) | +1.0% | 2436, 2425, 2369 / 2590, 2394, 2436 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 2519 (2168-2693) | 2185 (2065-2584) | -13.3% | 2592, 2406, 2380 / 2335, 2382, 2128 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 5.199e+04 (4.919e+04-5.467e+04) | 5.146e+04 (5.096e+04-5.243e+04) | -1.0% | 5.181e+04, 5.149e+04, 5.293e+04 / 5.146e+04, 5.11e+04, 5.243e+04 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 5.505e+04 (5.195e+04-6.048e+04) | 4.984e+04 (4.872e+04-5.45e+04) | -9.5% | 5.236e+04, 5.844e+04, 5.538e+04 / 5.156e+04, 4.883e+04, 5.206e+04 | separated, inside spread |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 4133 (3956-4376) | 4236 (3956-4437) | +2.5% | 4096, 4200, 4166 / 4236, 4163, 4196 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 1018 (1009-1022) | 998.7 (991.8-1003) | -1.8% | 1014, 1020, 1017 / 997.2, 998.7, 996.5 | consistent |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 1.189e+05 (1.138e+05-1.27e+05) | 1.22e+05 (1.172e+05-1.254e+05) | +2.7% | 1.199e+05, 1.147e+05, 1.232e+05 / 1.235e+05, 1.21e+05, 1.201e+05 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 6671 (6317-6818) | 6967 (6444-8108) | +4.4% | 6493, 6549, 6816 / 7871, 6501, 6937 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 1131 (1121-1149) | 1128 (1122-1136) | -0.2% | 1128, 1127, 1143 / 1132, 1129, 1125 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 629.1 (624-632.2) | 606 (600.6-609.5) | -3.7% | 624.2, 631, 629.5 / 604.7, 607.7, 603.6 | consistent |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.835e+04 (1.833e+04-1.873e+04) | 1.834e+04 (1.83e+04-1.837e+04) | -0.1% | 1.834e+04, 1.851e+04, 1.854e+04 / 1.832e+04, 1.836e+04, 1.832e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 1.218e+04 (1.18e+04-1.317e+04) | 1.21e+04 (1.128e+04-1.311e+04) | -0.6% | 1.204e+04, 1.225e+04, 1.248e+04 / 1.291e+04, 1.137e+04, 1.214e+04 | within noise |
| conv 26x26x8/2, 8 ch forward / numpy | 90.08 (89.68-91.09) | 90.44 (89.88-90.57) | +0.4% | 90.57, 90.19, 89.71 / 90.54, 90.32, 90.19 | within noise |
| conv 26x26x8/2, 8 ch forward / rust | 60.2 (60.16-60.9) | 57.27 (57.02-57.63) | -4.9% | 60.54, 60.45, 60.19 / 57.54, 57.05, 57.34 | consistent |
| conv 26x26x8/2, 8 ch downstream / numpy | 103.4 (102.7-104.2) | 103.8 (103.2-104.6) | +0.4% | 103.4, 103, 103.9 / 104, 104.1, 103.3 | within noise |
| conv 26x26x8/2, 8 ch downstream / rust | 40.15 (39.91-40.18) | 39.37 (38.7-39.47) | -1.9% | 40.12, 40.04, 40.16 / 39.45, 38.71, 39.39 | separated, inside spread |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 47.93 (47.53-48.34) | 47.72 (47.44-48) | -0.4% | 47.79, 47.93, 47.93 / 47.71, 47.96, 47.53 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 18.7 (18.68-18.79) | 17.36 (17.29-17.4) | -7.2% | 18.71, 18.75, 18.69 / 17.32, 17.37, 17.36 | consistent |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 3355 (3074-3626) | 3395 (3046-3499) | +1.2% | 3330, 3180, 3549 / 3306, 3254, 3452 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 2800 (2661-3131) | 2768 (2562-3242) | -1.1% | 3062, 2738, 2747 / 2675, 2950, 2995 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 6.557e+04 (6.498e+04-6.669e+04) | 6.518e+04 (6.327e+04-6.824e+04) | -0.6% | 6.572e+04, 6.54e+04, 6.601e+04 / 6.42e+04, 6.466e+04, 6.673e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 6.716e+04 (6.16e+04-6.962e+04) | 6.171e+04 (6.017e+04-6.561e+04) | -8.1% | 6.566e+04, 6.716e+04, 6.463e+04 / 6.171e+04, 6.144e+04, 6.299e+04 | separated, inside spread |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 8989 (7655-9899) | 8800 (7776-8971) | -2.1% | 8774, 9461, 8348 / 8374, 8238, 8906 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 1244 (1240-1248) | 1203 (1202-1218) | -3.3% | 1248, 1244, 1240 / 1202, 1218, 1203 | consistent |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 1.951e+05 (1.901e+05-2.071e+05) | 1.932e+05 (1.831e+05-2.04e+05) | -1.0% | 1.965e+05, 1.935e+05, 1.999e+05 / 1.925e+05, 1.935e+05, 1.932e+05 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 2.767e+04 (2.411e+04-3.092e+04) | 2.742e+04 (2.412e+04-3.171e+04) | -0.9% | 2.69e+04, 2.966e+04, 2.672e+04 / 2.637e+04, 3e+04, 2.556e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 1387 (1377-1412) | 1378 (1374-1386) | -0.6% | 1383, 1402, 1382 / 1378, 1380, 1378 | separated, inside spread |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 784.7 (739.4-822.4) | 777 (681.1-788.8) | -1.0% | 776.1, 790.2, 784.7 / 782.2, 729.2, 779.4 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 2.237e+04 (2.219e+04-2.272e+04) | 2.23e+04 (2.216e+04-2.252e+04) | -0.3% | 2.238e+04, 2.225e+04, 2.257e+04 / 2.235e+04, 2.234e+04, 2.23e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 1.592e+04 (1.436e+04-1.788e+04) | 1.519e+04 (1.458e+04-1.67e+04) | -4.6% | 1.541e+04, 1.628e+04, 1.604e+04 / 1.519e+04, 1.56e+04, 1.564e+04 | within noise |
| conv 26x26x8, 8 ch forward / numpy | 245.8 (243.8-247.2) | 245.2 (244.7-245.4) | -0.3% | 245.8, 247, 244.4 / 245, 245, 245.3 | within noise |
| conv 26x26x8, 8 ch forward / rust | 235.1 (235-236.6) | 223.8 (223.6-225.7) | -4.8% | 235.1, 235.8, 235.8 / 224.7, 223.6, 223.8 | consistent |
| conv 26x26x8, 8 ch downstream / numpy | 254.5 (253.4-258.1) | 255 (253.8-258.3) | +0.2% | 254.2, 253.9, 256.5 / 255.7, 255, 256.1 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 153 (151.8-153.4) | 147.8 (147.1-149.4) | -3.4% | 153.3, 152.8, 152.4 / 148.4, 148.2, 147.7 | consistent |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 160.2 (157.5-162.2) | 161 (158.6-162.5) | +0.5% | 158.2, 161.4, 160.4 / 158.9, 162, 161.3 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 70.25 (70.22-70.35) | 64.73 (64.66-65.06) | -7.9% | 70.3, 70.29, 70.23 / 64.7, 64.79, 64.89 | consistent |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 1.479e+04 (1.358e+04-1.592e+04) | 1.316e+04 (1.253e+04-1.487e+04) | -11.1% | 1.471e+04, 1.45e+04, 1.528e+04 / 1.283e+04, 1.402e+04, 1.313e+04 | separated, inside spread |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 1.256e+04 (1.173e+04-1.354e+04) | 1.181e+04 (1.125e+04-1.231e+04) | -6.0% | 1.264e+04, 1.256e+04, 1.276e+04 / 1.213e+04, 1.156e+04, 1.17e+04 | separated, inside spread |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 2.541e+05 (2.449e+05-2.725e+05) | 2.524e+05 (2.479e+05-2.674e+05) | -0.7% | 2.62e+05, 2.504e+05, 2.616e+05 / 2.517e+05, 2.518e+05, 2.595e+05 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 2.415e+05 (2.392e+05-2.428e+05) | 2.361e+05 (2.307e+05-2.422e+05) | -2.3% | 2.398e+05, 2.422e+05, 2.418e+05 / 2.361e+05, 2.362e+05, 2.365e+05 | consistent |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 2.578e+04 (2.462e+04-2.714e+04) | 2.536e+04 (2.498e+04-2.855e+04) | -1.6% | 2.516e+04, 2.535e+04, 2.69e+04 / 2.661e+04, 2.688e+04, 2.523e+04 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 3896 (3225-4726) | 4673 (3304-5008) | +20.0% | 3526, 4145, 4345 / 4007, 4274, 4823 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 5.337e+05 (5.203e+05-5.464e+05) | 5.281e+05 (5.23e+05-5.317e+05) | -1.1% | 5.274e+05, 5.388e+05, 5.354e+05 / 5.273e+05, 5.281e+05, 5.263e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 6.411e+04 (5.846e+04-8.423e+04) | 8.263e+04 (6.625e+04-8.531e+04) | +28.9% | 6.206e+04, 6.109e+04, 7.711e+04 / 8.192e+04, 8.452e+04, 7.39e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 5636 (5616-5758) | 5614 (5599-5675) | -0.4% | 5687, 5643, 5636 / 5645, 5628, 5604 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 3467 (3334-3881) | 3658 (3158-3787) | +5.5% | 3661, 3607, 3387 / 3736, 3395, 3623 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 8.908e+04 (8.858e+04-9.026e+04) | 8.884e+04 (8.841e+04-8.915e+04) | -0.3% | 8.928e+04, 8.875e+04, 8.964e+04 / 8.893e+04, 8.871e+04, 8.884e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 6.456e+04 (6.041e+04-6.956e+04) | 6.207e+04 (5.167e+04-6.457e+04) | -3.9% | 6.653e+04, 6.479e+04, 6.251e+04 / 6.413e+04, 6.037e+04, 5.787e+04 | within noise |
| pool 26x26, 8 ch forward / numpy | 105.7 (105.4-106.1) | 105.7 (105.2-106.1) | -0.0% | 105.7, 105.5, 105.9 / 105.7, 105.7, 105.7 | within noise |
| pool 26x26, 8 ch forward / rust | 5.218 (5.207-5.26) | 5.216 (5.209-5.228) | -0.0% | 5.243, 5.211, 5.216 / 5.213, 5.221, 5.219 | within noise |
| pool 26x26, 8 ch downstream / numpy | 55.36 (54.68-56.51) | 55.36 (54.54-56.34) | -0.0% | 55.36, 56.36, 54.98 / 55.27, 55.36, 55.44 | within noise |
| pool 26x26, 8 ch downstream / rust | 4.139 (4.135-4.15) | 4.193 (4.172-4.229) | +1.3% | 4.139, 4.139, 4.143 / 4.193, 4.178, 4.22 | separated, inside spread |
| pool 26x26, 8 ch forward_batch b32 / numpy | 2424 (2383-2558) | 2427 (2395-2466) | +0.1% | 2515, 2397, 2424 / 2451, 2406, 2435 | within noise |
| pool 26x26, 8 ch forward_batch b32 / rust | 223.7 (202-239.4) | 222.5 (196.8-248.5) | -0.5% | 233.3, 223.7, 204.1 / 217.7, 239.6, 207.5 | within noise |
| pool 26x26, 8 ch forward_batch b512 / numpy | 4.024e+04 (3.978e+04-4.085e+04) | 4.073e+04 (3.983e+04-4.194e+04) | +1.2% | 4.084e+04, 4.005e+04, 4.009e+04 / 4.018e+04, 4.145e+04, 4.052e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 9132 (8463-1.01e+04) | 8719 (8398-1.024e+04) | -4.5% | 9691, 9132, 8717 / 8479, 9558, 8870 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 970.6 (948.7-987.2) | 981.3 (951-1486) | +1.1% | 966.8, 957.8, 982.6 / 1219, 981.3, 1222 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / rust | 301.5 (129.7-519.1) | 132 (131-482.8) | -56.2% | 301.5, 496.7, 129.9 / 306.9, 131.8, 299.4 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 5.86e+04 (5.681e+04-6.354e+04) | 5.632e+04 (5.301e+04-6.746e+04) | -3.9% | 6.204e+04, 5.778e+04, 5.781e+04 / 5.308e+04, 5.632e+04, 6.366e+04 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / rust | 2.151e+04 (1.986e+04-2.396e+04) | 2.114e+04 (2.019e+04-2.303e+04) | -1.7% | 2.228e+04, 2.161e+04, 2.077e+04 / 2.061e+04, 2.166e+04, 2.18e+04 | within noise |
| pool 6x6, 8 ch forward / numpy | 39.87 (39.59-40.59) | 39.74 (39.51-40.59) | -0.3% | 39.65, 39.83, 40.36 / 39.61, 39.7, 40.25 | within noise |
| pool 6x6, 8 ch forward / rust | 0.7632 (0.762-0.7719) | 0.7596 (0.7586-0.7655) | -0.5% | 0.7674, 0.7624, 0.7663 / 0.7618, 0.7592, 0.7625 | within noise |
| pool 6x6, 8 ch downstream / numpy | 32.58 (32.26-33.81) | 32.46 (32.29-32.59) | -0.4% | 32.41, 33.11, 33.03 / 32.4, 32.39, 32.58 | within noise |
| pool 6x6, 8 ch downstream / rust | 0.6641 (0.6578-0.6669) | 0.6704 (0.6629-0.6768) | +0.9% | 0.6641, 0.6666, 0.6591 / 0.6671, 0.6731, 0.6708 | separated, inside spread |
| pool 6x6, 8 ch forward_batch b32 / numpy | 168.7 (167.6-297.4) | 168.3 (167.7-169.1) | -0.2% | 179, 167.8, 233.5 / 168.5, 168.7, 167.9 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 10.57 (10.52-10.6) | 10.45 (10.44-10.49) | -1.1% | 10.58, 10.55, 10.57 / 10.46, 10.46, 10.45 | consistent |
| pool 6x6, 8 ch forward_batch b512 / numpy | 2240 (2175-2547) | 2195 (2186-2546) | -2.0% | 2219, 2418, 2201 / 2393, 2192, 2193 | within noise |
| pool 6x6, 8 ch forward_batch b512 / rust | 165.7 (165.4-166) | 165.4 (163.7-173.1) | -0.1% | 165.7, 165.5, 165.9 / 165.3, 165.7, 168.6 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 85.36 (85.13-87.42) | 85.08 (84.55-85.47) | -0.3% | 86.28, 85.63, 85.28 / 84.98, 85.31, 84.87 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / rust | 7.843 (7.838-7.873) | 9.496 (9.481-9.507) | +21.1% | 7.856, 7.843, 7.847 / 9.503, 9.487, 9.492 | consistent |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 939.8 (937.8-951.5) | 938.8 (931.9-954.4) | -0.1% | 938.4, 940.1, 946.1 / 945.2, 939.3, 935.6 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 129.4 (129-349.9) | 155.9 (155.5-156.3) | +20.5% | 231.2, 129.3, 239.6 / 155.9, 156.1, 155.9 | within noise |
| conv tail 32 x 5408 bare downstream b32 / numpy | 1436 (833.8-1518) | 1312 (942.9-1633) | -8.7% | 1176, 1436, 1411 / 1304, 1471, 1147 | within noise |
| conv tail 32 x 5408 bare downstream b32 / rust | 1207 (1152-1488) | 1217 (1197-1353) | +0.9% | 1320, 1207, 1279 / 1202, 1333, 1213 | within noise |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3.047e+04 (2.592e+04-3.617e+04) | 3.236e+04 (2.581e+04-3.746e+04) | +6.2% | 3.105e+04, 3.032e+04, 3.047e+04 / 2.912e+04, 3.448e+04, 3.34e+04 | within noise |
| conv tail 32 x 5408 bare downstream b512 / rust | 2.202e+04 (2.124e+04-2.333e+04) | 2.112e+04 (1.397e+04-2.334e+04) | -4.1% | 2.241e+04, 2.154e+04, 2.235e+04 / 2.208e+04, 2.026e+04, 1.77e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 1366 (1267-1504) | 1398 (1144-1655) | +2.4% | 1441, 1366, 1275 / 1412, 1399, 1366 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / rust | 1178 (1096-1354) | 1173 (1130-1342) | -0.5% | 1118, 1197, 1261 / 1189, 1170, 1236 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 2.223e+04 (2.091e+04-2.276e+04) | 2.161e+04 (2.116e+04-2.258e+04) | -2.8% | 2.154e+04, 2.215e+04, 2.243e+04 / 2.15e+04, 2.135e+04, 2.226e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / rust | 1.894e+04 (1.829e+04-1.938e+04) | 1.965e+04 (1.906e+04-2.101e+04) | +3.7% | 1.866e+04, 1.883e+04, 1.917e+04 / 2.075e+04, 1.916e+04, 1.956e+04 | within noise |
| conv tail 32 x 5408 transpose b32 / numpy | 1.46 (1.453-1.475) | 1.466 (1.458-1.496) | +0.5% | 1.458, 1.468, 1.459 / 1.477, 1.464, 1.471 | within noise |
| conv tail 32 x 5408 transpose b32 / rust | 0.7983 (0.7926-0.8093) | 0.8101 (0.802-0.8132) | +1.5% | 0.7983, 0.801, 0.7975 / 0.8072, 0.8057, 0.8126 | separated, inside spread |
| conv tail 32 x 5408 transpose b512 / numpy | 30.01 (29.86-30.06) | 30.01 (29.87-30.19) | +0.0% | 30.04, 30.01, 29.93 / 29.93, 30.02, 30.1 | within noise |
| conv tail 32 x 5408 transpose b512 / rust | 11.37 (10.3-11.62) | 11.55 (10.3-11.77) | +1.6% | 10.9, 11.61, 10.77 / 11.73, 10.92, 10.97 | within noise |
| conv tail 32 x 5408 add b32 / numpy | 326.1 (295.9-383.6) | 312.6 (293.7-418.4) | -4.2% | 353.9, 302.7, 331 / 302.1, 334.9, 366.5 | within noise |
| conv tail 32 x 5408 add b32 / rust | 334.9 (294.1-418.8) | 345.1 (297.1-398.9) | +3.0% | 376.1, 336.7, 313.9 / 374.3, 352.6, 307.3 | within noise |
| conv tail 32 x 5408 add b512 / numpy | 340 (317.7-409.9) | 387 (307.5-416.8) | +13.8% | 338, 327.5, 387.5 / 321.4, 391.6, 409.4 | within noise |
| conv tail 32 x 5408 add b512 / rust | 321.5 (308.1-453.7) | 352.1 (305.1-428.8) | +9.5% | 314.5, 316.7, 393.9 / 396.1, 333.5, 367 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 2.842 (2.811-2.917) | 2.842 (2.814-2.853) | -0.0% | 2.856, 2.888, 2.816 / 2.847, 2.828, 2.838 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.7767 (0.775-0.7815) | 0.7788 (0.7756-0.7991) | +0.3% | 0.7793, 0.7766, 0.7756 / 0.7874, 0.78, 0.7786 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 15.85 (15.72-15.91) | 16.08 (15.9-16.36) | +1.4% | 15.88, 15.88, 15.78 / 16.03, 16.12, 16.13 | consistent |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 8.703 (8.658-8.725) | 8.691 (8.656-8.726) | -0.1% | 8.717, 8.706, 8.667 / 8.716, 8.684, 8.669 | within noise |
| dense 30 x 784 bare downstream b32 / numpy | 58.02 (56.85-58.35) | 57.9 (56.83-58.35) | -0.2% | 58.25, 57.22, 58.07 / 57.9, 57.5, 57.71 | within noise |
| dense 30 x 784 bare downstream b32 / rust | 126.3 (125.7-128.1) | 126.1 (125.5-126.7) | -0.1% | 126.9, 125.8, 127.4 / 125.9, 125.8, 126.5 | within noise |
| dense 30 x 784 bare downstream b512 / numpy | 3535 (2573-3819) | 3233 (2572-4077) | -8.5% | 3598, 2806, 3694 / 3710, 2811, 3571 | within noise |
| dense 30 x 784 bare downstream b512 / rust | 2207 (1590-2581) | 2156 (1564-2490) | -2.3% | 2129, 2279, 2049 / 2108, 2247, 2027 | within noise |
| dense 30 x 784 bare accumulate b32 / numpy | 229.2 (66.35-401.8) | 66.55 (65.21-400.7) | -71.0% | 229.1, 233.3, 234.1 / 400.6, 66.5, 65.84 | within noise |
| dense 30 x 784 bare accumulate b32 / rust | 124.9 (124.8-126.9) | 126.4 (125.4-126.7) | +1.2% | 125.1, 124.9, 125.9 / 126.2, 126.7, 126.1 | separated, inside spread |
| dense 30 x 784 bare accumulate b512 / numpy | 1751 (1671-1827) | 1754 (1619-1864) | +0.2% | 1788, 1733, 1735 / 1719, 1741, 1759 | within noise |
| dense 30 x 784 bare accumulate b512 / rust | 2318 (2069-2538) | 2150 (2025-2507) | -7.3% | 2299, 2523, 2098 / 2150, 2352, 2046 | within noise |
| dense 30 x 784 transpose b32 / numpy | 1.404 (1.39-1.419) | 1.404 (1.392-1.413) | +0.0% | 1.401, 1.395, 1.413 / 1.404, 1.403, 1.402 | within noise |
| dense 30 x 784 transpose b32 / rust | 0.8211 (0.8172-0.828) | 0.8235 (0.8165-0.8422) | +0.3% | 0.8249, 0.8209, 0.819 / 0.8235, 0.8294, 0.8229 | within noise |
| dense 30 x 784 transpose b512 / numpy | 9.021 (8.981-9.034) | 9.005 (8.99-9.026) | -0.2% | 9.011, 9.027, 9.004 / 9.005, 9.004, 9.012 | within noise |
| dense 30 x 784 transpose b512 / rust | 10.67 (10.24-10.93) | 10.68 (10.15-10.95) | +0.1% | 10.78, 10.45, 10.7 / 10.55, 10.81, 10.43 | within noise |
| dense 30 x 784 add b32 / numpy | 10.27 (10.01-10.58) | 10.17 (9.916-10.41) | -0.9% | 10.1, 10.55, 10.26 / 10.03, 10.34, 10.16 | within noise |
| dense 30 x 784 add b32 / rust | 9.78 (9.396-11.51) | 9.705 (9.576-11.3) | -0.8% | 10.45, 10.25, 9.78 / 10.43, 10.44, 9.63 | within noise |
| dense 30 x 784 add b512 / numpy | 11.42 (11.27-11.71) | 11.63 (11.18-11.72) | +1.9% | 11.49, 11.52, 11.4 / 11.66, 11.65, 11.39 | within noise |
| dense 30 x 784 add b512 / rust | 9.621 (9.469-9.863) | 9.696 (9.601-9.933) | +0.8% | 9.567, 9.561, 9.738 / 9.831, 9.615, 9.779 | within noise |
| dense 30 x 784 sum_axis0 b32 / numpy | 2.828 (2.798-2.893) | 2.81 (2.782-2.825) | -0.6% | 2.817, 2.857, 2.839 / 2.819, 2.8, 2.801 | within noise |
| dense 30 x 784 sum_axis0 b32 / rust | 0.7009 (0.6996-0.7044) | 0.7037 (0.7016-0.7073) | +0.4% | 0.7001, 0.7008, 0.7042 / 0.7038, 0.7047, 0.7026 | within noise |
| dense 30 x 784 sum_axis0 b512 / numpy | 15.41 (15.33-15.47) | 15.39 (15.36-15.63) | -0.1% | 15.36, 15.45, 15.4 / 15.4, 15.5, 15.38 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 7.435 (7.424-7.457) | 7.451 (7.433-7.49) | +0.2% | 7.428, 7.435, 7.448 / 7.437, 7.474, 7.455 | within noise |
| dense 10 x 30 bare downstream b32 / numpy | 5.868 (5.847-5.913) | 5.858 (5.825-5.92) | -0.2% | 5.865, 5.866, 5.886 / 5.845, 5.853, 5.891 | within noise |
| dense 10 x 30 bare downstream b32 / rust | 3.71 (3.705-3.724) | 3.196 (3.192-3.204) | -13.9% | 3.711, 3.717, 3.706 / 3.194, 3.198, 3.2 | consistent |
| dense 10 x 30 bare downstream b512 / numpy | 64.73 (64.54-64.9) | 64.73 (64.54-64.81) | +0.0% | 64.63, 64.73, 64.78 / 64.78, 64.72, 64.68 | within noise |
| dense 10 x 30 bare downstream b512 / rust | 54.44 (54.21-54.75) | 46.33 (46.05-46.72) | -14.9% | 54.44, 54.56, 54.33 / 46.37, 46.53, 46.19 | consistent |
| dense 10 x 30 bare accumulate b32 / numpy | 5.051 (5.022-5.107) | 5.041 (5.024-5.056) | -0.2% | 5.046, 5.048, 5.075 / 5.052, 5.031, 5.039 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 3.25 (3.248-3.256) | 2.899 (2.898-2.911) | -10.8% | 3.256, 3.249, 3.249 / 2.905, 2.899, 2.899 | consistent |
| dense 10 x 30 bare accumulate b512 / numpy | 32.55 (32.44-32.6) | 32.56 (32.5-32.79) | +0.0% | 32.55, 32.59, 32.47 / 32.57, 32.67, 32.53 | within noise |
| dense 10 x 30 bare accumulate b512 / rust | 45.34 (45.3-45.38) | 45.21 (45.18-45.25) | -0.3% | 45.35, 45.36, 45.31 / 45.22, 45.21, 45.19 | consistent, small |
| dense 10 x 30 transpose b32 / numpy | 0.8884 (0.8832-0.8923) | 0.8879 (0.8832-0.8993) | -0.1% | 0.8918, 0.8841, 0.8884 / 0.8883, 0.8877, 0.893 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.5041 (0.4976-0.5192) | 0.5078 (0.501-0.5198) | +0.7% | 0.5095, 0.5099, 0.5005 / 0.5069, 0.5091, 0.5104 | within noise |
| dense 10 x 30 transpose b512 / numpy | 3.391 (3.379-3.583) | 3.369 (3.356-3.382) | -0.7% | 3.391, 3.417, 3.483 / 3.365, 3.369, 3.374 | separated, inside spread |
| dense 10 x 30 transpose b512 / rust | 3.764 (3.748-3.933) | 3.824 (3.795-3.901) | +1.6% | 3.918, 3.762, 3.754 / 3.873, 3.799, 3.824 | within noise |
| dense 10 x 30 add b32 / numpy | 0.895 (0.8895-0.9185) | 0.8974 (0.8896-0.9175) | +0.3% | 0.904, 0.8936, 0.8966 / 0.9025, 0.8974, 0.9043 | within noise |
| dense 10 x 30 add b32 / rust | 0.386 (0.3831-0.3931) | 0.3823 (0.3797-0.4245) | -1.0% | 0.3867, 0.3895, 0.3839 / 0.3823, 0.3801, 0.4102 | within noise |
| dense 10 x 30 add b512 / numpy | 0.9149 (0.9055-0.9335) | 0.9202 (0.9138-0.9446) | +0.6% | 0.923, 0.9136, 0.9117 / 0.9292, 0.9226, 0.9185 | within noise |
| dense 10 x 30 add b512 / rust | 0.4059 (0.4035-0.4118) | 0.4058 (0.4029-0.4155) | -0.0% | 0.4082, 0.405, 0.4081 / 0.4041, 0.4079, 0.4092 | within noise |
| dense 10 x 30 sum_axis0 b32 / numpy | 2.457 (2.451-2.472) | 2.455 (2.445-2.462) | -0.1% | 2.463, 2.453, 2.466 / 2.457, 2.455, 2.453 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.5271 (0.5219-0.5304) | 0.5315 (0.5283-0.5363) | +0.8% | 0.5288, 0.5266, 0.526 / 0.5341, 0.5325, 0.5298 | separated, inside spread |
| dense 10 x 30 sum_axis0 b512 / numpy | 12.22 (12.14-12.32) | 12.21 (12.17-12.61) | -0.1% | 12.19, 12.24, 12.23 / 12.21, 12.39, 12.21 | within noise |
| dense 10 x 30 sum_axis0 b512 / rust | 4.645 (4.641-4.651) | 4.658 (4.648-4.691) | +0.3% | 4.645, 4.644, 4.647 / 4.669, 4.649, 4.679 | separated, inside spread |
| attention 16 x 32 forward_batch b32 / numpy | 749.5 (743.1-1665) | 752.3 (743.5-1625) | +0.4% | 1204, 748.2, 940.9 / 750, 748.1, 1192 | within noise |
| attention 16 x 32 forward_batch b32 / rust | 803 (799.3-805.4) | 782.1 (781.1-783.2) | -2.6% | 803, 801.8, 802.3 / 782.5, 782.1, 782.2 | consistent |
| attention 16 x 32 forward_batch b512 / numpy | 2.266e+04 (2.229e+04-2.408e+04) | 2.259e+04 (2.186e+04-2.301e+04) | -0.3% | 2.236e+04, 2.365e+04, 2.266e+04 / 2.219e+04, 2.278e+04, 2.272e+04 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 1.679e+04 (1.624e+04-1.722e+04) | 1.601e+04 (1.571e+04-1.774e+04) | -4.6% | 1.673e+04, 1.705e+04, 1.657e+04 / 1.574e+04, 1.634e+04, 1.684e+04 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 764.6 (758.3-1230) | 761.2 (752.4-763.8) | -0.4% | 996.5, 763.7, 764.6 / 759.4, 756.7, 762.2 | separated, inside spread |
| attention 16 x 32 hidden_delta_batch b32 / rust | 757.5 (756.5-759.3) | 753.1 (752.2-757.1) | -0.6% | 759, 756.9, 757.2 / 753.1, 754.7, 753.5 | consistent, small |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 2.756e+04 (2.582e+04-2.913e+04) | 2.694e+04 (2.613e+04-2.812e+04) | -2.2% | 2.777e+04, 2.747e+04, 2.723e+04 / 2.67e+04, 2.675e+04, 2.739e+04 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / rust | 1.888e+04 (1.815e+04-2.054e+04) | 1.815e+04 (1.715e+04-2.001e+04) | -3.9% | 1.957e+04, 1.978e+04, 1.826e+04 / 1.778e+04, 1.816e+04, 1.885e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 591.8 (580.6-597.7) | 593.4 (580.7-2125) | +0.3% | 587, 592.1, 589.1 / 2117, 591.8, 587.7 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 461.2 (447.8-464.4) | 457.4 (448.4-465.3) | -0.8% | 456.1, 456.1, 461.2 / 465.1, 456.9, 449.6 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 4.105e+04 (3.326e+04-4.536e+04) | 4.321e+04 (3.399e+04-4.505e+04) | +5.3% | 3.931e+04, 4.105e+04, 4.08e+04 / 3.456e+04, 4.436e+04, 4.351e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 3.286e+04 (2.616e+04-3.757e+04) | 3.522e+04 (3.041e+04-3.697e+04) | +7.2% | 3.175e+04, 3.38e+04, 3.23e+04 / 3.28e+04, 3.34e+04, 3.639e+04 | within noise |
