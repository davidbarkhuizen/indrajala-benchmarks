Old `e9ab957` against new `e9ab957`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/focused_benchmark.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `b307f197fdc7`) on both sides. Machine check: profile: identity matches (raspberry-pi-5.json); max 1-min load 0.10; busy processes: none. Each row pools 6 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: per call / dense 30 x 784 apply_accumulated_gradient / rust -0.2% (36.64 -> 36.55 µs)
- consistent: per call / conv 13x13x8, 8 ch forward / rust -0.2% (82.05 -> 81.89 µs)
- 268 rows within noise (29 separated inside their spread), max |Δ| 74.4%

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv tail 32 x 5408 forward / numpy | 77.91 (76.75-81.83) | 77.69 (77.4-79.11) | -0.3% | 76.99, 81.21, 77.91 / 78.41, 77.53, 78.23 | within noise |
| conv tail 32 x 5408 forward / rust | 164 (163.9-164.6) | 164.1 (164-164.5) | +0.1% | 163.9, 164.1, 164.3 / 164.2, 164.2, 164.1 | within noise |
| conv tail 32 x 5408 downstream / numpy | 91.91 (91.57-92.9) | 92.19 (90.89-93.08) | +0.3% | 91.79, 91.94, 92.36 / 91.98, 92.19, 92.06 | within noise |
| conv tail 32 x 5408 downstream / rust | 218.6 (217.9-298.9) | 252.3 (218.3-290.9) | +15.4% | 218.2, 227, 258.7 / 268.4, 235.8, 268.6 | within noise |
| conv tail 32 x 5408 hidden_delta / numpy | 104.2 (103.6-106.2) | 104.2 (103.3-104.4) | -0.0% | 103.9, 104.9, 104.5 / 103.9, 104.2, 104.2 | within noise |
| conv tail 32 x 5408 hidden_delta / rust | 282.5 (245.9-288.6) | 245.2 (229.9-302.9) | -13.2% | 288.4, 282.5, 246.3 / 273.2, 268.1, 238.4 | within noise |
| conv tail 32 x 5408 accumulate_gradient / numpy | 659.5 (380.9-914.4) | 350.6 (330.2-911) | -46.8% | 654.5, 647.7, 673.9 / 345.9, 356.7, 624.2 | separated, inside spread |
| conv tail 32 x 5408 accumulate_gradient / rust | 96.45 (89.18-100.1) | 98.09 (90.35-100.6) | +1.7% | 99.29, 92.05, 94.79 / 93.91, 100.1, 98.09 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / numpy | 1560 (1462-2008) | 1685 (1553-2054) | +8.0% | 1808, 1479, 1560 / 1851, 1614, 1711 | within noise |
| conv tail 32 x 5408 apply_accumulated_gradient / rust | 459.7 (382.2-789.8) | 447.1 (376.1-788.7) | -2.7% | 590.5, 580.5, 459.7 / 549.9, 381.3, 648.3 | within noise |
| conv tail 32 x 5408 sgd step / numpy | 2241 (2196-3214) | 2355 (2099-2984) | +5.1% | 2227, 2376, 2718 / 2105, 2733, 2381 | within noise |
| conv tail 32 x 5408 sgd step / rust | 118.4 (115.8-120.7) | 118.2 (115.5-121.6) | -0.2% | 118.3, 116.7, 119.3 / 116.2, 118.5, 120.2 | within noise |
| conv tail 32 x 5408 forward_batch b32 / numpy | 528.9 (506-554.4) | 522.6 (514.1-547.9) | -1.2% | 528.6, 516.7, 542.3 / 529.4, 522.6, 533.2 | within noise |
| conv tail 32 x 5408 forward_batch b32 / rust | 5258 (5252-5344) | 5252 (5251-5286) | -0.1% | 5258, 5254, 5303 / 5275, 5252, 5251 | within noise |
| conv tail 32 x 5408 forward_batch b512 / numpy | 1.611e+04 (1.546e+04-1.824e+04) | 1.688e+04 (1.612e+04-1.804e+04) | +4.8% | 1.611e+04, 1.572e+04, 1.736e+04 / 1.708e+04, 1.742e+04, 1.662e+04 | within noise |
| conv tail 32 x 5408 forward_batch b512 / rust | 2.2e+04 (2.186e+04-2.206e+04) | 2.188e+04 (2.183e+04-2.206e+04) | -0.5% | 2.2e+04, 2.196e+04, 2.197e+04 / 2.188e+04, 2.195e+04, 2.19e+04 | separated, inside spread |
| conv tail 32 x 5408 downstream_batch b32 / numpy | 1426 (1252-1601) | 1437 (1310-1477) | +0.8% | 1329, 1404, 1553 / 1471, 1371, 1406 | within noise |
| conv tail 32 x 5408 downstream_batch b32 / rust | 7540 (7494-7850) | 7534 (7275-7922) | -0.1% | 7566, 7683, 7500 / 7675, 7598, 7493 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / numpy | 4.139e+04 (2.717e+04-4.512e+04) | 4.101e+04 (3.632e+04-4.53e+04) | -0.9% | 4.067e+04, 3.295e+04, 4.464e+04 / 3.865e+04, 4.132e+04, 4.316e+04 | within noise |
| conv tail 32 x 5408 downstream_batch b512 / rust | 3.718e+04 (3.612e+04-3.777e+04) | 3.76e+04 (3.706e+04-4.992e+04) | +1.1% | 3.636e+04, 3.754e+04, 3.718e+04 / 4.349e+04, 3.72e+04, 3.859e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / numpy | 3234 (3018-3968) | 3755 (3122-3932) | +16.1% | 3362, 3211, 3493 / 3803, 3124, 3849 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b32 / rust | 8615 (7543-8973) | 8416 (7734-1.135e+04) | -2.3% | 7782, 8914, 8615 / 9851, 8233, 8330 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / numpy | 7.307e+04 (6.439e+04-7.668e+04) | 7.274e+04 (7.025e+04-7.674e+04) | -0.5% | 7.307e+04, 7.054e+04, 7.109e+04 / 7.245e+04, 7.162e+04, 7.571e+04 | within noise |
| conv tail 32 x 5408 hidden_delta_batch b512 / rust | 4.64e+04 (4.583e+04-4.798e+04) | 4.699e+04 (4.6e+04-4.794e+04) | +1.3% | 4.672e+04, 4.603e+04, 4.728e+04 / 4.743e+04, 4.627e+04, 4.731e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / numpy | 2031 (1829-2075) | 1958 (1694-2209) | -3.6% | 1935, 1990, 2047 / 2066, 1833, 2006 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b32 / rust | 8212 (7799-8349) | 8063 (7866-8354) | -1.8% | 8330, 8024, 8009 / 8053, 7877, 8345 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / numpy | 2.277e+04 (2.215e+04-2.551e+04) | 2.421e+04 (2.204e+04-2.532e+04) | +6.3% | 2.22e+04, 2.286e+04, 2.431e+04 / 2.421e+04, 2.245e+04, 2.52e+04 | within noise |
| conv tail 32 x 5408 accumulate_gradient_batch b512 / rust | 1.26e+05 (1.09e+05-1.655e+05) | 1.173e+05 (1.115e+05-1.438e+05) | -6.9% | 1.127e+05, 1.44e+05, 1.441e+05 / 1.146e+05, 1.184e+05, 1.303e+05 | within noise |
| dense 30 x 784 forward / numpy | 16.22 (15.99-17.3) | 16.19 (16.07-16.67) | -0.2% | 16.09, 16.73, 16.38 / 16.42, 16.25, 16.18 | within noise |
| dense 30 x 784 forward / rust | 23.2 (23.15-23.21) | 23.2 (23.14-23.22) | -0.0% | 23.18, 23.2, 23.2 / 23.18, 23.21, 23.19 | within noise |
| dense 30 x 784 downstream / numpy | 12.76 (12.71-12.81) | 12.69 (12.65-12.79) | -0.6% | 12.76, 12.77, 12.75 / 12.74, 12.66, 12.71 | separated, inside spread |
| dense 30 x 784 downstream / rust | 23.77 (23.69-23.94) | 23.81 (23.66-24.08) | +0.2% | 23.72, 23.83, 23.82 / 23.81, 23.77, 23.88 | within noise |
| dense 30 x 784 hidden_delta / numpy | 17.03 (16.94-17.15) | 17.03 (16.96-17.08) | -0.0% | 17.09, 17.02, 17.04 / 17.03, 17.04, 17.01 | within noise |
| dense 30 x 784 hidden_delta / rust | 24.7 (24.56-24.8) | 24.62 (24.51-24.73) | -0.3% | 24.71, 24.71, 24.63 / 24.53, 24.66, 24.68 | within noise |
| dense 30 x 784 accumulate_gradient / numpy | 42.84 (42.71-43.16) | 42.93 (42.61-43.72) | +0.2% | 42.73, 42.94, 42.96 / 42.71, 43.22, 43.07 | within noise |
| dense 30 x 784 accumulate_gradient / rust | 9.843 (9.779-9.975) | 9.926 (9.857-10.53) | +0.8% | 9.892, 9.852, 9.807 / 9.899, 10.21, 9.96 | separated, inside spread |
| dense 30 x 784 apply_accumulated_gradient / numpy | 61.12 (61.04-61.51) | 61.29 (61-61.51) | +0.3% | 61.35, 61.09, 61.09 / 61.32, 61.25, 61.16 | within noise |
| dense 30 x 784 apply_accumulated_gradient / rust | 36.64 (36.45-36.84) | 36.55 (36.52-36.62) | -0.2% | 36.62, 36.66, 36.64 / 36.55, 36.55, 36.58 | consistent |
| dense 30 x 784 sgd step / numpy | 107.9 (107.8-108.1) | 108 (107.9-108.6) | +0.1% | 107.9, 108, 108 / 108.3, 108.1, 108 | separated, inside spread |
| dense 30 x 784 sgd step / rust | 15.75 (15.71-15.81) | 15.72 (15.71-15.77) | -0.2% | 15.76, 15.77, 15.74 / 15.72, 15.74, 15.72 | separated, inside spread |
| dense 30 x 784 forward_batch b32 / numpy | 269.3 (90.91-460.5) | 92.06 (91.13-451.5) | -65.8% | 272.5, 275.8, 269.3 / 91.29, 450.5, 92.06 | within noise |
| dense 30 x 784 forward_batch b32 / rust | 725 (724.5-725.5) | 724.6 (724.3-725) | -0.1% | 724.5, 725.3, 725.1 / 724.6, 724.7, 724.5 | within noise |
| dense 30 x 784 forward_batch b512 / numpy | 2268 (2245-2406) | 2253 (2088-2591) | -0.7% | 2268, 2330, 2315 / 2167, 2258, 2426 | within noise |
| dense 30 x 784 forward_batch b512 / rust | 3230 (3224-3237) | 3231 (3225-3242) | +0.0% | 3234, 3231, 3226 / 3237, 3235, 3226 | within noise |
| dense 30 x 784 downstream_batch b32 / numpy | 225.4 (57.35-428.7) | 57.8 (56.91-388.4) | -74.4% | 57.86, 395.4, 243.4 / 223.2, 57.98, 57.28 | within noise |
| dense 30 x 784 downstream_batch b32 / rust | 747.7 (745.2-758) | 749.4 (745.3-759.4) | +0.2% | 748.1, 752.3, 746.8 / 745.8, 749.4, 756.1 | within noise |
| dense 30 x 784 downstream_batch b512 / numpy | 3527 (2801-4142) | 4007 (2503-4139) | +13.6% | 2957, 4027, 3559 / 4098, 4007, 2760 | within noise |
| dense 30 x 784 downstream_batch b512 / rust | 3519 (3488-6990) | 3511 (3503-3526) | -0.2% | 3525, 3490, 5258 / 3506, 3519, 3510 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / numpy | 105.2 (104.2-289.1) | 104.8 (103.8-297.9) | -0.5% | 196.7, 105.2, 105.4 / 201.7, 104.8, 104.1 | within noise |
| dense 30 x 784 hidden_delta_batch b32 / rust | 779.5 (772-950.6) | 780.8 (776.3-944.9) | +0.2% | 947.1, 775.1, 777.6 / 861.8, 783.4, 779.6 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / numpy | 9458 (8996-1.044e+04) | 8856 (8675-1.002e+04) | -6.4% | 9719, 9458, 9788 / 8725, 8981, 9479 | within noise |
| dense 30 x 784 hidden_delta_batch b512 / rust | 4819 (4530-4968) | 4740 (4648-8458) | -1.6% | 4666, 4749, 4915 / 4671, 4738, 6647 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / numpy | 264.8 (86.94-448.2) | 265.7 (86.66-444.9) | +0.4% | 264.7, 267.7, 266.9 / 265.2, 266.3, 266 | within noise |
| dense 30 x 784 accumulate_gradient_batch b32 / rust | 759.8 (755.8-762.1) | 761 (759.6-766) | +0.2% | 761, 757.8, 758.7 / 761, 763, 762.8 | separated, inside spread |
| dense 30 x 784 accumulate_gradient_batch b512 / numpy | 1947 (1767-2016) | 1921 (1753-2.49e+04) | -1.3% | 1962, 1784, 1993 / 1.333e+04, 1855, 1953 | within noise |
| dense 30 x 784 accumulate_gradient_batch b512 / rust | 1.022e+04 (8523-1.072e+04) | 8886 (8349-1.844e+04) | -13.1% | 9828, 1.045e+04, 9395 / 1.367e+04, 8564, 8996 | within noise |
| dense 10 x 30 forward / numpy | 8.121 (8.075-8.163) | 8.201 (8.101-8.321) | +1.0% | 8.119, 8.117, 8.129 / 8.125, 8.296, 8.201 | within noise |
| dense 10 x 30 forward / rust | 0.8562 (0.8495-0.8708) | 0.8579 (0.8479-0.8681) | +0.2% | 0.8504, 0.8702, 0.8556 / 0.8554, 0.8579, 0.8608 | within noise |
| dense 10 x 30 downstream / numpy | 1.824 (1.811-1.847) | 1.822 (1.805-1.838) | -0.1% | 1.816, 1.837, 1.827 / 1.817, 1.817, 1.832 | within noise |
| dense 10 x 30 downstream / rust | 0.6182 (0.6159-0.6392) | 0.6196 (0.6154-0.6231) | +0.2% | 0.6252, 0.6169, 0.6289 / 0.6186, 0.6198, 0.62 | within noise |
| dense 10 x 30 hidden_delta / numpy | 4.513 (4.491-4.536) | 4.536 (4.505-4.583) | +0.5% | 4.53, 4.494, 4.513 / 4.506, 4.567, 4.545 | within noise |
| dense 10 x 30 hidden_delta / rust | 1.038 (1.025-1.046) | 1.032 (1.022-1.038) | -0.6% | 1.043, 1.035, 1.033 / 1.032, 1.035, 1.027 | within noise |
| dense 10 x 30 accumulate_gradient / numpy | 5.295 (5.242-5.424) | 5.271 (5.258-5.297) | -0.4% | 5.35, 5.344, 5.248 / 5.28, 5.275, 5.27 | within noise |
| dense 10 x 30 accumulate_gradient / rust | 0.7802 (0.7702-0.7938) | 0.779 (0.7707-0.7822) | -0.2% | 0.782, 0.7754, 0.7839 / 0.781, 0.7782, 0.7739 | within noise |
| dense 10 x 30 apply_accumulated_gradient / numpy | 8.925 (8.808-9.124) | 8.908 (8.866-9.102) | -0.2% | 9.024, 8.914, 8.866 / 8.998, 8.989, 8.868 | within noise |
| dense 10 x 30 apply_accumulated_gradient / rust | 4.168 (4.133-4.314) | 4.147 (4.132-4.16) | -0.5% | 4.192, 4.224, 4.148 / 4.145, 4.154, 4.141 | within noise |
| dense 10 x 30 sgd step / numpy | 15.04 (14.97-15.54) | 15.04 (14.98-15.45) | -0.0% | 15.29, 15.01, 15.03 / 15.03, 15.17, 15.21 | within noise |
| dense 10 x 30 sgd step / rust | 0.9142 (0.9048-0.9262) | 0.9126 (0.904-0.9192) | -0.2% | 0.9199, 0.9069, 0.9189 / 0.9123, 0.9116, 0.9126 | within noise |
| dense 10 x 30 forward_batch b32 / numpy | 19.42 (19.26-19.57) | 19.41 (19.3-19.71) | -0.1% | 19.51, 19.33, 19.39 / 19.37, 19.56, 19.37 | within noise |
| dense 10 x 30 forward_batch b32 / rust | 15.27 (15.21-15.33) | 15.2 (15.19-15.34) | -0.4% | 15.29, 15.29, 15.23 / 15.3, 15.2, 15.2 | within noise |
| dense 10 x 30 forward_batch b512 / numpy | 151.7 (151.5-152.3) | 151.7 (151.5-152) | -0.0% | 152.2, 151.7, 151.5 / 151.7, 151.5, 152 | within noise |
| dense 10 x 30 forward_batch b512 / rust | 234.1 (233.6-234.7) | 234.4 (233.6-234.7) | +0.1% | 233.7, 234.1, 234.6 / 234, 234.2, 234.6 | within noise |
| dense 10 x 30 downstream_batch b32 / numpy | 5.917 (5.89-6.059) | 5.932 (5.902-5.949) | +0.3% | 5.928, 5.994, 5.897 / 5.937, 5.931, 5.925 | within noise |
| dense 10 x 30 downstream_batch b32 / rust | 10.75 (10.75-10.75) | 10.75 (10.74-10.79) | +0.1% | 10.75, 10.75, 10.75 / 10.75, 10.75, 10.77 | within noise |
| dense 10 x 30 downstream_batch b512 / numpy | 64.76 (64.48-64.92) | 64.75 (64.45-65.32) | -0.0% | 64.9, 64.62, 64.71 / 64.78, 64.96, 64.65 | within noise |
| dense 10 x 30 downstream_batch b512 / rust | 166.7 (166.7-166.8) | 166.7 (166.7-166.9) | +0.0% | 166.7, 166.7, 166.7 / 166.8, 166.8, 166.7 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / numpy | 10.47 (10.41-10.58) | 10.5 (10.46-10.57) | +0.3% | 10.43, 10.53, 10.47 / 10.53, 10.47, 10.53 | within noise |
| dense 10 x 30 hidden_delta_batch b32 / rust | 11.64 (11.63-11.69) | 11.63 (11.61-11.7) | -0.1% | 11.67, 11.64, 11.63 / 11.66, 11.63, 11.63 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / numpy | 93.24 (92.41-95.91) | 93.52 (92.52-94.48) | +0.3% | 94.68, 92.43, 93.42 / 93.59, 94.08, 92.95 | within noise |
| dense 10 x 30 hidden_delta_batch b512 / rust | 177.2 (175.8-179.7) | 178 (175.6-186.9) | +0.4% | 178.3, 176.5, 177.9 / 177.2, 181.2, 178.9 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / numpy | 9.612 (9.5-9.673) | 9.613 (9.497-9.654) | +0.0% | 9.622, 9.557, 9.642 / 9.624, 9.6, 9.576 | within noise |
| dense 10 x 30 accumulate_gradient_batch b32 / rust | 10.44 (10.44-10.49) | 10.44 (10.43-10.45) | -0.0% | 10.46, 10.46, 10.44 / 10.44, 10.44, 10.44 | separated, inside spread |
| dense 10 x 30 accumulate_gradient_batch b512 / numpy | 47.79 (47.41-48.36) | 47.7 (47.56-48.1) | -0.2% | 47.61, 47.73, 48.07 / 47.7, 47.83, 47.8 | within noise |
| dense 10 x 30 accumulate_gradient_batch b512 / rust | 150.1 (149.1-150.2) | 149.8 (149.4-150.1) | -0.2% | 150.1, 149.4, 150.1 / 149.8, 149.7, 149.8 | within noise |
| conv 28x28, 8 ch forward / numpy | 85.47 (85.13-98.74) | 85.34 (84.87-87.13) | -0.2% | 92.25, 85.19, 85.45 / 86.25, 85.51, 84.97 | within noise |
| conv 28x28, 8 ch forward / rust | 75.34 (75.31-75.37) | 75.35 (75.33-75.44) | +0.0% | 75.35, 75.33, 75.34 / 75.35, 75.39, 75.35 | within noise |
| conv 28x28, 8 ch downstream / numpy | 71.39 (70.9-72.09) | 70.98 (70.54-72.27) | -0.6% | 71.59, 71.21, 71.4 / 71.59, 70.8, 71.45 | within noise |
| conv 28x28, 8 ch downstream / rust | 72.09 (72.05-72.1) | 72.09 (72.06-72.12) | -0.0% | 72.08, 72.08, 72.1 / 72.09, 72.09, 72.09 | within noise |
| conv 28x28, 8 ch accumulate_gradient / numpy | 59.33 (57.78-69.95) | 59.73 (57.99-60.67) | +0.7% | 58.18, 59.01, 65.8 / 59.73, 60.61, 58.41 | within noise |
| conv 28x28, 8 ch accumulate_gradient / rust | 50.98 (50.97-51.01) | 50.99 (50.97-51.27) | +0.0% | 50.99, 50.99, 50.98 / 50.98, 51.01, 51.13 | within noise |
| conv 28x28, 8 ch forward_batch b32 / numpy | 4801 (4242-5607) | 5023 (4070-5588) | +4.6% | 4434, 4720, 5291 / 5052, 5188, 4556 | within noise |
| conv 28x28, 8 ch forward_batch b32 / rust | 2576 (2531-2736) | 2850 (2767-3112) | +10.6% | 2634, 2654, 2555 / 2798, 2972, 2907 | separated, inside spread |
| conv 28x28, 8 ch forward_batch b512 / numpy | 7.516e+04 (7.455e+04-7.685e+04) | 7.475e+04 (7.262e+04-7.604e+04) | -0.6% | 7.57e+04, 7.556e+04, 7.504e+04 / 7.377e+04, 7.422e+04, 7.531e+04 | within noise |
| conv 28x28, 8 ch forward_batch b512 / rust | 4.944e+04 (4.914e+04-5.047e+04) | 4.939e+04 (4.825e+04-5.723e+04) | -0.1% | 4.981e+04, 4.967e+04, 4.923e+04 / 5.172e+04, 5.274e+04, 4.939e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / numpy | 1612 (1464-2034) | 1604 (1512-1941) | -0.5% | 1788, 1558, 1702 / 1759, 1726, 1581 | within noise |
| conv 28x28, 8 ch downstream_batch b32 / rust | 3072 (2793-3778) | 3677 (2765-3763) | +19.7% | 3055, 3216, 3299 / 3190, 3761, 3456 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / numpy | 5.548e+04 (5.333e+04-5.961e+04) | 5.712e+04 (5.579e+04-5.858e+04) | +3.0% | 5.473e+04, 5.428e+04, 5.829e+04 / 5.767e+04, 5.747e+04, 5.648e+04 | within noise |
| conv 28x28, 8 ch downstream_batch b512 / rust | 4.524e+04 (4.371e+04-4.692e+04) | 4.536e+04 (4.465e+04-4.762e+04) | +0.3% | 4.524e+04, 4.531e+04, 4.483e+04 / 4.589e+04, 4.468e+04, 4.669e+04 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / numpy | 2269 (2246-2322) | 2251 (2245-2322) | -0.8% | 2285, 2246, 2304 / 2251, 2287, 2281 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b32 / rust | 1827 (1798-2162) | 1830 (1804-2144) | +0.2% | 1801, 2004, 1829 / 1807, 1834, 1996 | within noise |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / numpy | 3.754e+04 (3.718e+04-3.832e+04) | 3.829e+04 (3.755e+04-3.875e+04) | +2.0% | 3.792e+04, 3.764e+04, 3.743e+04 / 3.839e+04, 3.794e+04, 3.837e+04 | separated, inside spread |
| conv 28x28, 8 ch accumulate_gradient_batch b512 / rust | 4.054e+04 (3.906e+04-4.397e+04) | 4.161e+04 (3.862e+04-4.689e+04) | +2.6% | 4.099e+04, 3.998e+04, 4.21e+04 / 4.313e+04, 3.925e+04, 4.405e+04 | within noise |
| conv 8x8, 8 ch forward / numpy | 34.93 (34.31-36.39) | 34.99 (34.75-36.02) | +0.2% | 35.29, 35.35, 34.72 / 35.23, 34.94, 35.38 | within noise |
| conv 8x8, 8 ch forward / rust | 4.935 (4.927-4.946) | 4.939 (4.928-4.956) | +0.1% | 4.931, 4.936, 4.938 / 4.934, 4.933, 4.95 | within noise |
| conv 8x8, 8 ch downstream / numpy | 40.09 (39.67-41.3) | 39.93 (39.43-40.57) | -0.4% | 40.48, 40.19, 40.09 / 39.94, 39.45, 40.28 | within noise |
| conv 8x8, 8 ch downstream / rust | 4.361 (4.359-4.365) | 4.359 (4.358-4.361) | -0.0% | 4.359, 4.363, 4.362 / 4.359, 4.358, 4.361 | within noise |
| conv 8x8, 8 ch accumulate_gradient / numpy | 12.53 (12.45-12.91) | 12.53 (12.47-12.99) | -0.0% | 12.58, 12.68, 12.49 / 12.51, 12.75, 12.54 | within noise |
| conv 8x8, 8 ch accumulate_gradient / rust | 3.508 (3.505-3.527) | 3.506 (3.503-3.509) | -0.1% | 3.507, 3.518, 3.507 / 3.506, 3.505, 3.509 | within noise |
| conv 8x8, 8 ch forward_batch b32 / numpy | 130.5 (128.3-169.6) | 131 (130-132.3) | +0.4% | 130.5, 129.1, 150.6 / 131.3, 130.8, 131.1 | within noise |
| conv 8x8, 8 ch forward_batch b32 / rust | 128.7 (128.5-128.9) | 128.8 (128.7-129) | +0.1% | 128.7, 128.7, 128.7 / 128.7, 128.8, 128.8 | within noise |
| conv 8x8, 8 ch forward_batch b512 / numpy | 4047 (3525-4216) | 3779 (3339-4254) | -6.6% | 3930, 3775, 4133 / 3700, 4053, 3682 | within noise |
| conv 8x8, 8 ch forward_batch b512 / rust | 2402 (2257-2450) | 2631 (2250-2660) | +9.6% | 2339, 2354, 2409 / 2654, 2618, 2432 | separated, inside spread |
| conv 8x8, 8 ch downstream_batch b32 / numpy | 116.6 (115-117.5) | 115.7 (115.4-116.1) | -0.8% | 116.6, 116.3, 116.4 / 115.6, 115.9, 115.5 | separated, inside spread |
| conv 8x8, 8 ch downstream_batch b32 / rust | 123.8 (123.8-123.9) | 123.8 (123.7-123.9) | -0.0% | 123.8, 123.8, 123.8 / 123.8, 123.7, 123.9 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / numpy | 1914 (1593-2022) | 1618 (1594-1656) | -15.5% | 1595, 2021, 1914 / 1611, 1608, 1635 | within noise |
| conv 8x8, 8 ch downstream_batch b512 / rust | 2522 (2228-2781) | 2433 (2208-2775) | -3.5% | 2258, 2679, 2612 / 2547, 2221, 2622 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / numpy | 148.5 (148.2-148.7) | 148.7 (148.3-153.9) | +0.1% | 148.5, 148.7, 148.4 / 151.2, 150.1, 148.5 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b32 / rust | 87.4 (87.29-87.42) | 87.4 (87.31-87.44) | -0.0% | 87.35, 87.37, 87.41 / 87.38, 87.41, 87.36 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / numpy | 2335 (2278-2373) | 2296 (2290-2364) | -1.7% | 2323, 2297, 2371 / 2292, 2308, 2331 | within noise |
| conv 8x8, 8 ch accumulate_gradient_batch b512 / rust | 1686 (1532-1834) | 1553 (1537-1845) | -7.9% | 1827, 1690, 1536 / 1553, 1540, 1840 | within noise |
| conv 13x13x8, 8 ch forward / numpy | 80.39 (79.38-95.87) | 79.99 (79.04-115.8) | -0.5% | 80.12, 79.85, 88.97 / 98.48, 79.92, 79.42 | within noise |
| conv 13x13x8, 8 ch forward / rust | 82.05 (81.95-82.13) | 81.89 (81.81-81.98) | -0.2% | 82.01, 82.03, 82.1 / 81.89, 81.9, 81.88 | consistent |
| conv 13x13x8, 8 ch downstream / numpy | 89.17 (88.92-89.42) | 89.42 (88.86-89.91) | +0.3% | 88.99, 89.13, 89.35 / 89.55, 88.97, 89.71 | within noise |
| conv 13x13x8, 8 ch downstream / rust | 95.52 (95.39-95.59) | 95.41 (95.39-95.55) | -0.1% | 95.49, 95.49, 95.52 / 95.4, 95.54, 95.41 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / numpy | 40.62 (40.43-41.04) | 40.44 (40.2-40.84) | -0.5% | 40.63, 40.81, 40.55 / 40.37, 40.57, 40.44 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient / rust | 63.89 (63.86-64.04) | 63.89 (63.84-63.98) | +0.0% | 63.95, 63.87, 63.91 / 63.95, 63.86, 63.87 | within noise |
| conv 13x13x8, 8 ch forward_batch b32 / numpy | 2643 (2617-3119) | 2505 (2465-2647) | -5.2% | 2643, 2883, 2629 / 2495, 2480, 2612 | separated, inside spread |
| conv 13x13x8, 8 ch forward_batch b32 / rust | 3309 (3141-3507) | 3426 (3204-4267) | +3.5% | 3383, 3411, 3200 / 3770, 3540, 3356 | within noise |
| conv 13x13x8, 8 ch forward_batch b512 / numpy | 5.141e+04 (5.022e+04-5.266e+04) | 5.203e+04 (5.088e+04-5.362e+04) | +1.2% | 5.158e+04, 5.097e+04, 5.179e+04 / 5.222e+04, 5.203e+04, 5.225e+04 | separated, inside spread |
| conv 13x13x8, 8 ch forward_batch b512 / rust | 6.786e+04 (6.612e+04-7.378e+04) | 6.874e+04 (6.596e+04-7.64e+04) | +1.3% | 6.786e+04, 6.995e+04, 6.795e+04 / 7.279e+04, 6.818e+04, 6.794e+04 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / numpy | 4357 (3956-7096) | 4082 (3906-4461) | -6.3% | 4146, 4426, 5550 / 4222, 4232, 4000 | within noise |
| conv 13x13x8, 8 ch downstream_batch b32 / rust | 3343 (3308-3380) | 3351 (3325-3368) | +0.2% | 3342, 3344, 3344 / 3362, 3349, 3335 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / numpy | 1.208e+05 (1.18e+05-1.252e+05) | 1.206e+05 (1.168e+05-1.216e+05) | -0.1% | 1.218e+05, 1.182e+05, 1.232e+05 / 1.208e+05, 1.192e+05, 1.192e+05 | within noise |
| conv 13x13x8, 8 ch downstream_batch b512 / rust | 3.775e+04 (3.643e+04-3.888e+04) | 3.691e+04 (3.595e+04-3.814e+04) | -2.2% | 3.808e+04, 3.732e+04, 3.771e+04 / 3.794e+04, 3.655e+04, 3.66e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / numpy | 1126 (1123-1142) | 1140 (1125-1142) | +1.2% | 1125, 1133, 1134 / 1142, 1136, 1133 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b32 / rust | 2164 (2160-2172) | 2169 (2161-2591) | +0.2% | 2167, 2161, 2166 / 2376, 2172, 2164 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / numpy | 1.838e+04 (1.833e+04-1.936e+04) | 1.85e+04 (1.84e+04-1.927e+04) | +0.7% | 1.835e+04, 1.885e+04, 1.855e+04 / 1.846e+04, 1.863e+04, 1.884e+04 | within noise |
| conv 13x13x8, 8 ch accumulate_gradient_batch b512 / rust | 2.272e+04 (2.15e+04-2.34e+04) | 2.227e+04 (2.163e+04-2.298e+04) | -2.0% | 2.252e+04, 2.291e+04, 2.227e+04 / 2.273e+04, 2.181e+04, 2.239e+04 | within noise |
| conv 26x26x8/2, 8 ch forward / numpy | 90.33 (89.66-91.15) | 90.19 (89.84-90.6) | -0.1% | 90.33, 90.17, 90.45 / 90.14, 90.41, 90.08 | within noise |
| conv 26x26x8/2, 8 ch forward / rust | 97.56 (97.3-97.9) | 97.71 (97.31-97.88) | +0.1% | 97.49, 97.75, 97.43 / 97.68, 97.79, 97.51 | within noise |
| conv 26x26x8/2, 8 ch downstream / numpy | 103.6 (102.6-103.8) | 103.2 (102.9-103.9) | -0.4% | 103.6, 103.8, 102.8 / 103.1, 103.4, 103.4 | within noise |
| conv 26x26x8/2, 8 ch downstream / rust | 113.9 (113.8-114) | 113.9 (113.8-114) | -0.0% | 113.9, 113.9, 113.9 / 113.8, 113.9, 114 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / numpy | 47.67 (47.53-48.03) | 47.68 (47.23-48.52) | +0.0% | 47.78, 47.54, 47.86 / 47.86, 47.36, 48.2 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient / rust | 76.47 (76.39-76.54) | 76.43 (76.38-76.46) | -0.0% | 76.49, 76.5, 76.39 / 76.43, 76.42, 76.44 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / numpy | 3490 (3075-3883) | 3495 (3485-3759) | +0.2% | 3239, 3686, 3508 / 3603, 3495, 3625 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b32 / rust | 4112 (4058-4595) | 4382 (4044-4538) | +6.5% | 4216, 4332, 4112 / 4424, 4452, 4127 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / numpy | 6.773e+04 (6.502e+04-8.013e+04) | 6.661e+04 (6.57e+04-6.824e+04) | -1.6% | 7.258e+04, 6.682e+04, 6.773e+04 / 6.656e+04, 6.577e+04, 6.785e+04 | within noise |
| conv 26x26x8/2, 8 ch forward_batch b512 / rust | 8.427e+04 (8.224e+04-8.896e+04) | 8.53e+04 (8.003e+04-8.907e+04) | +1.2% | 8.284e+04, 8.695e+04, 8.511e+04 / 8.429e+04, 8.575e+04, 8.53e+04 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / numpy | 9437 (7755-1.006e+04) | 8396 (7601-1.032e+04) | -11.0% | 9992, 8264, 9479 / 8895, 7822, 8959 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b32 / rust | 5542 (4788-5706) | 5224 (4904-5686) | -5.7% | 5234, 5616, 5269 / 4965, 5295, 5537 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / numpy | 1.972e+05 (1.939e+05-2.051e+05) | 1.969e+05 (1.9e+05-2.515e+05) | -0.2% | 1.972e+05, 1.972e+05, 1.996e+05 / 1.953e+05, 2.268e+05, 1.931e+05 | within noise |
| conv 26x26x8/2, 8 ch downstream_batch b512 / rust | 5.458e+04 (5.403e+04-5.519e+04) | 5.456e+04 (5.221e+04-5.732e+04) | -0.1% | 5.408e+04, 5.476e+04, 5.494e+04 / 5.337e+04, 5.558e+04, 5.497e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / numpy | 1381 (1375-1423) | 1383 (1374-1393) | +0.1% | 1381, 1400, 1379 / 1384, 1384, 1383 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b32 / rust | 2619 (2613-2626) | 2614 (2603-2624) | -0.2% | 2615, 2621, 2620 / 2608, 2619, 2618 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / numpy | 2.245e+04 (2.222e+04-2.465e+04) | 2.226e+04 (2.212e+04-2.26e+04) | -0.8% | 2.23e+04, 2.242e+04, 2.358e+04 / 2.217e+04, 2.251e+04, 2.226e+04 | within noise |
| conv 26x26x8/2, 8 ch accumulate_gradient_batch b512 / rust | 2.709e+04 (2.621e+04-2.784e+04) | 2.732e+04 (2.63e+04-2.795e+04) | +0.9% | 2.703e+04, 2.703e+04, 2.715e+04 / 2.732e+04, 2.713e+04, 2.715e+04 | within noise |
| conv 26x26x8, 8 ch forward / numpy | 245.1 (243.6-278.1) | 245.6 (244.4-245.8) | +0.2% | 262, 244.7, 244.3 / 245.2, 245.6, 245.1 | within noise |
| conv 26x26x8, 8 ch forward / rust | 383.8 (383.2-396.2) | 383.5 (383.4-385) | -0.1% | 383.8, 383.5, 389.7 / 384.2, 383.5, 383.7 | within noise |
| conv 26x26x8, 8 ch downstream / numpy | 252.9 (252.5-257.9) | 255.8 (252.5-260.5) | +1.1% | 253.5, 255.5, 252.8 / 256.5, 254.4, 256.5 | within noise |
| conv 26x26x8, 8 ch downstream / rust | 450.4 (450.4-450.6) | 450.6 (450.4-450.7) | +0.0% | 450.5, 450.5, 450.4 / 450.6, 450.4, 450.6 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / numpy | 160.1 (158-160.5) | 160.3 (157-163.2) | +0.1% | 159, 160.5, 160 / 160.5, 158.1, 161.7 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient / rust | 298.7 (298.7-298.9) | 299 (298.6-303.5) | +0.1% | 298.8, 298.8, 298.7 / 298.6, 299, 301.6 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / numpy | 1.363e+04 (1.252e+04-1.608e+04) | 1.416e+04 (1.245e+04-1.576e+04) | +3.8% | 1.395e+04, 1.494e+04, 1.328e+04 / 1.285e+04, 1.416e+04, 1.562e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b32 / rust | 1.757e+04 (1.641e+04-1.895e+04) | 1.825e+04 (1.759e+04-1.837e+04) | +3.8% | 1.686e+04, 1.871e+04, 1.734e+04 / 1.794e+04, 1.81e+04, 1.834e+04 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / numpy | 2.587e+05 (2.508e+05-3.028e+05) | 2.617e+05 (2.47e+05-2.742e+05) | +1.2% | 2.805e+05, 2.55e+05, 2.62e+05 / 2.563e+05, 2.566e+05, 2.706e+05 | within noise |
| conv 26x26x8, 8 ch forward_batch b512 / rust | 3.193e+05 (3.174e+05-3.276e+05) | 3.192e+05 (3.16e+05-3.296e+05) | -0.0% | 3.188e+05, 3.184e+05, 3.259e+05 / 3.169e+05, 3.228e+05, 3.21e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b32 / numpy | 2.538e+04 (2.468e+04-2.672e+04) | 2.595e+04 (2.472e+04-2.899e+04) | +2.3% | 2.537e+04, 2.57e+04, 2.585e+04 / 2.656e+04, 2.72e+04, 2.592e+04 | separated, inside spread |
| conv 26x26x8, 8 ch downstream_batch b32 / rust | 9886 (9314-1.558e+04) | 1.013e+04 (9523-1.027e+04) | +2.5% | 1.004e+04, 1.27e+04, 9674 / 9827, 1.018e+04, 1.004e+04 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / numpy | 5.435e+05 (5.264e+05-5.486e+05) | 5.458e+05 (5.257e+05-5.692e+05) | +0.4% | 5.37e+05, 5.435e+05, 5.439e+05 / 5.279e+05, 5.568e+05, 5.532e+05 | within noise |
| conv 26x26x8, 8 ch downstream_batch b512 / rust | 1.806e+05 (1.795e+05-1.842e+05) | 1.807e+05 (1.786e+05-2.082e+05) | +0.1% | 1.815e+05, 1.798e+05, 1.826e+05 / 1.796e+05, 1.934e+05, 1.83e+05 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / numpy | 5651 (5641-5768) | 5641 (5624-5677) | -0.2% | 5647, 5711, 5648 / 5631, 5661, 5641 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b32 / rust | 5974 (5899-6118) | 6109 (6009-6429) | +2.3% | 5964, 5967, 6018 / 6130, 6045, 6283 | separated, inside spread |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / numpy | 8.962e+04 (8.868e+04-9.007e+04) | 8.886e+04 (8.868e+04-9.303e+04) | -0.8% | 8.983e+04, 8.89e+04, 8.977e+04 / 9.09e+04, 8.882e+04, 8.898e+04 | within noise |
| conv 26x26x8, 8 ch accumulate_gradient_batch b512 / rust | 1.073e+05 (1.033e+05-1.084e+05) | 1.072e+05 (9.976e+04-1.08e+05) | -0.2% | 1.052e+05, 1.083e+05, 1.073e+05 / 1.08e+05, 1.047e+05, 1.037e+05 | within noise |
| pool 26x26, 8 ch forward / numpy | 105.9 (104.9-107.1) | 105.7 (104.9-106.4) | -0.2% | 105.2, 106.4, 106.6 / 105.5, 105.9, 105.7 | within noise |
| pool 26x26, 8 ch forward / rust | 5.21 (5.187-5.23) | 5.219 (5.2-5.246) | +0.2% | 5.219, 5.216, 5.2 / 5.211, 5.241, 5.212 | within noise |
| pool 26x26, 8 ch downstream / numpy | 55.18 (54.88-56.47) | 55.12 (54.65-56.41) | -0.1% | 55.18, 55.04, 55.77 / 54.86, 55.65, 55.71 | within noise |
| pool 26x26, 8 ch downstream / rust | 4.288 (4.278-4.301) | 4.297 (4.286-4.309) | +0.2% | 4.29, 4.294, 4.282 / 4.301, 4.299, 4.291 | within noise |
| pool 26x26, 8 ch forward_batch b32 / numpy | 2444 (2384-2866) | 2469 (2398-2625) | +1.0% | 2387, 2671, 2449 / 2511, 2437, 2474 | within noise |
| pool 26x26, 8 ch forward_batch b32 / rust | 234.6 (207.8-240.1) | 222.3 (197.7-229.8) | -5.3% | 221.7, 221.5, 237.7 / 222.3, 213.7, 216.9 | within noise |
| pool 26x26, 8 ch forward_batch b512 / numpy | 4.12e+04 (4.055e+04-4.654e+04) | 4.189e+04 (4.115e+04-4.241e+04) | +1.7% | 4.089e+04, 4.168e+04, 4.384e+04 / 4.206e+04, 4.155e+04, 4.191e+04 | within noise |
| pool 26x26, 8 ch forward_batch b512 / rust | 9289 (8307-9637) | 9459 (8998-1.021e+04) | +1.8% | 8772, 9150, 9489 / 9417, 9881, 9183 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / numpy | 988.5 (949-1503) | 985.5 (950.7-1505) | -0.3% | 1244, 982.4, 973.8 / 1228, 1228, 982.4 | within noise |
| pool 26x26, 8 ch downstream_batch b32 / rust | 304.2 (134.2-488.2) | 299.2 (133.9-484.7) | -1.7% | 134.4, 311.2, 475.9 / 134, 474.1, 309.5 | within noise |
| pool 26x26, 8 ch downstream_batch b512 / numpy | 5.807e+04 (5.555e+04-6.114e+04) | 6.236e+04 (5.802e+04-6.803e+04) | +7.4% | 5.942e+04, 5.911e+04, 5.656e+04 / 6.281e+04, 6.302e+04, 6.205e+04 | separated, inside spread |
| pool 26x26, 8 ch downstream_batch b512 / rust | 2.105e+04 (2.035e+04-2.204e+04) | 2.115e+04 (1.993e+04-2.23e+04) | +0.4% | 2.142e+04, 2.081e+04, 2.105e+04 / 2.219e+04, 2.053e+04, 2.064e+04 | within noise |
| pool 6x6, 8 ch forward / numpy | 39.78 (39.25-41.42) | 39.78 (39.35-41.57) | +0.0% | 40.97, 39.44, 39.62 / 41.18, 39.78, 39.45 | within noise |
| pool 6x6, 8 ch forward / rust | 0.7642 (0.7608-0.7679) | 0.7627 (0.7574-0.7824) | -0.2% | 0.7642, 0.7611, 0.7666 / 0.7619, 0.7721, 0.7613 | within noise |
| pool 6x6, 8 ch downstream / numpy | 32.71 (32.42-33.67) | 32.52 (32.32-32.63) | -0.6% | 32.73, 33.12, 32.6 / 32.47, 32.5, 32.58 | separated, inside spread |
| pool 6x6, 8 ch downstream / rust | 0.8368 (0.8165-0.8645) | 0.8185 (0.8143-0.8283) | -2.2% | 0.8368, 0.8541, 0.8227 / 0.8245, 0.8153, 0.8187 | within noise |
| pool 6x6, 8 ch forward_batch b32 / numpy | 168.8 (167.4-170.5) | 169.2 (167.6-194.1) | +0.2% | 168.3, 168.5, 169.6 / 168.3, 182, 168.6 | within noise |
| pool 6x6, 8 ch forward_batch b32 / rust | 10.5 (10.48-10.52) | 10.46 (10.44-10.51) | -0.4% | 10.51, 10.49, 10.49 / 10.49, 10.48, 10.45 | separated, inside spread |
| pool 6x6, 8 ch forward_batch b512 / numpy | 2236 (2200-2631) | 2211 (2192-2246) | -1.1% | 2253, 2236, 2425 / 2193, 2220, 2227 | separated, inside spread |
| pool 6x6, 8 ch forward_batch b512 / rust | 166.5 (163.2-171.7) | 163.3 (162.9-163.7) | -1.9% | 163.3, 170.2, 166.5 / 163.5, 163.1, 163.1 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / numpy | 85.31 (84.98-85.87) | 85.51 (84.76-86.63) | +0.2% | 85.55, 85.29, 85.18 / 85.23, 85.84, 85.59 | within noise |
| pool 6x6, 8 ch downstream_batch b32 / rust | 12.08 (12.05-12.29) | 12.19 (12.06-12.34) | +0.9% | 12.18, 12.18, 12.06 / 12.32, 12.17, 12.09 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / numpy | 943 (934-957.2) | 938.4 (936.3-942.9) | -0.5% | 938, 943, 954.8 / 941.4, 937.3, 937.8 | within noise |
| pool 6x6, 8 ch downstream_batch b512 / rust | 198 (196-434.2) | 201 (195.9-446.5) | +1.5% | 315.1, 196.1, 316.5 / 315.3, 326.2, 196.2 | within noise |
| conv tail 32 x 5408 bare downstream b32 / numpy | 1418 (1060-1502) | 1207 (993.4-1484) | -14.8% | 1418, 1401, 1273 / 1207, 1215, 1239 | separated, inside spread |
| conv tail 32 x 5408 bare downstream b32 / rust | 7552 (7006-8280) | 7515 (7433-7816) | -0.5% | 7723, 7262, 7827 / 7497, 7468, 7690 | within noise |
| conv tail 32 x 5408 bare downstream b512 / numpy | 3.402e+04 (2.556e+04-4.127e+04) | 4.196e+04 (2.837e+04-4.559e+04) | +23.4% | 3.545e+04, 3.032e+04, 3.496e+04 / 4.037e+04, 3.679e+04, 4.196e+04 | separated, inside spread |
| conv tail 32 x 5408 bare downstream b512 / rust | 3.935e+04 (3.715e+04-7.148e+04) | 3.743e+04 (3.71e+04-4.545e+04) | -4.9% | 3.738e+04, 4.406e+04, 5.634e+04 / 4.071e+04, 4.149e+04, 3.722e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / numpy | 1043 (921-3016) | 1313 (953.1-1466) | +25.8% | 1063, 976.1, 2036 / 1209, 1450, 1156 | within noise |
| conv tail 32 x 5408 bare accumulate b32 / rust | 7351 (6999-7535) | 7422 (6983-7542) | +1.0% | 7152, 7467, 7245 / 7422, 7252, 7441 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / numpy | 2.311e+04 (2.212e+04-2.524e+04) | 2.435e+04 (2.202e+04-2.634e+04) | +5.4% | 2.253e+04, 2.311e+04, 2.466e+04 / 2.418e+04, 2.33e+04, 2.473e+04 | within noise |
| conv tail 32 x 5408 bare accumulate b512 / rust | 1.085e+05 (8.637e+04-1.319e+05) | 1.066e+05 (9.079e+04-1.596e+05) | -1.8% | 1.092e+05, 9.834e+04, 1.122e+05 / 1.362e+05, 1.166e+05, 9.255e+04 | within noise |
| conv tail 32 x 5408 transpose b32 / numpy | 1.455 (1.449-1.471) | 1.469 (1.446-1.496) | +1.0% | 1.458, 1.453, 1.461 / 1.471, 1.475, 1.465 | separated, inside spread |
| conv tail 32 x 5408 transpose b32 / rust | 1.923 (1.919-1.929) | 1.923 (1.921-1.928) | +0.0% | 1.923, 1.922, 1.924 / 1.925, 1.923, 1.922 | within noise |
| conv tail 32 x 5408 transpose b512 / numpy | 29.97 (29.61-30.03) | 30.04 (30-30.11) | +0.3% | 29.82, 29.97, 29.94 / 30.09, 30.02, 30.03 | separated, inside spread |
| conv tail 32 x 5408 transpose b512 / rust | 27.1 (27.02-27.34) | 27.11 (27.01-27.32) | +0.0% | 27.07, 27.21, 27.09 / 27.02, 27.12, 27.21 | within noise |
| conv tail 32 x 5408 add b32 / numpy | 370.2 (312.8-419.1) | 353.6 (334.2-418) | -4.5% | 368.8, 364, 370.2 / 345.1, 385.3, 351 | within noise |
| conv tail 32 x 5408 add b32 / rust | 334.2 (313.5-457.7) | 368.2 (335.7-444.4) | +10.2% | 324, 397.5, 331.8 / 390, 389.8, 357.8 | within noise |
| conv tail 32 x 5408 add b512 / numpy | 334.2 (315.5-418.2) | 374.3 (333.5-421.2) | +12.0% | 325.2, 370, 374.5 / 376.6, 377.3, 374.3 | within noise |
| conv tail 32 x 5408 add b512 / rust | 377.5 (330.1-469.4) | 419.2 (312.1-442.7) | +11.0% | 427.2, 390.8, 350.1 / 374.5, 423.6, 386.1 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / numpy | 2.827 (2.81-2.865) | 2.829 (2.811-2.876) | +0.1% | 2.822, 2.846, 2.823 / 2.842, 2.848, 2.825 | within noise |
| conv tail 32 x 5408 sum_axis0 b32 / rust | 0.7792 (0.7767-0.782) | 0.7771 (0.773-0.8001) | -0.3% | 0.7797, 0.778, 0.7802 / 0.7758, 0.7773, 0.7889 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / numpy | 16.02 (15.9-16.24) | 15.92 (15.7-16.18) | -0.6% | 16.19, 15.96, 15.97 / 16.06, 15.93, 15.71 | within noise |
| conv tail 32 x 5408 sum_axis0 b512 / rust | 8.678 (8.666-8.745) | 8.684 (8.672-8.693) | +0.1% | 8.709, 8.69, 8.67 / 8.678, 8.679, 8.691 | within noise |
| dense 30 x 784 bare downstream b32 / numpy | 57.63 (56.71-57.94) | 57.61 (56.77-57.88) | -0.0% | 57.55, 57.7, 57.32 / 57.5, 57.66, 57.33 | within noise |
| dense 30 x 784 bare downstream b32 / rust | 747.2 (744.1-751.6) | 747.2 (740.8-751) | +0.0% | 745.6, 749.2, 748.6 / 747.2, 750.6, 743.7 | within noise |
| dense 30 x 784 bare downstream b512 / numpy | 3991 (3861-4331) | 3289 (2752-3991) | -17.6% | 4110, 4096, 3945 / 3008, 3971, 3105 | within noise |
| dense 30 x 784 bare downstream b512 / rust | 3516 (3506-6798) | 3505 (3504-3521) | -0.3% | 3508, 5159, 3516 / 3504, 3514, 3510 | within noise |
| dense 30 x 784 bare accumulate b32 / numpy | 66.82 (66.57-400.2) | 66.83 (65.45-412) | +0.0% | 233, 66.74, 233.4 / 406.6, 66.14, 66.66 | within noise |
| dense 30 x 784 bare accumulate b32 / rust | 744.5 (741.6-747.9) | 746.2 (742.1-750.4) | +0.2% | 743.6, 744.7, 744.5 / 749.5, 742.3, 746.2 | within noise |
| dense 30 x 784 bare accumulate b512 / numpy | 1785 (1700-2002) | 1760 (1653-1835) | -1.4% | 1710, 1802, 1923 / 1701, 1767, 1777 | within noise |
| dense 30 x 784 bare accumulate b512 / rust | 8931 (8159-1.036e+04) | 1.099e+04 (8246-1.198e+04) | +23.1% | 9258, 8792, 9051 / 9276, 1.182e+04, 1.103e+04 | separated, inside spread |
| dense 30 x 784 transpose b32 / numpy | 1.406 (1.391-1.42) | 1.406 (1.387-1.627) | +0.0% | 1.413, 1.393, 1.407 / 1.394, 1.512, 1.413 | within noise |
| dense 30 x 784 transpose b32 / rust | 1.869 (1.864-1.871) | 1.871 (1.867-1.873) | +0.1% | 1.87, 1.868, 1.867 / 1.871, 1.869, 1.87 | within noise |
| dense 30 x 784 transpose b512 / numpy | 9.012 (9-9.059) | 8.997 (8.957-9.065) | -0.2% | 9.03, 9.012, 9.012 / 9.034, 8.979, 9.011 | within noise |
| dense 30 x 784 transpose b512 / rust | 25.5 (25.46-25.91) | 25.49 (25.46-25.9) | -0.0% | 25.69, 25.5, 25.68 / 25.68, 25.48, 25.61 | within noise |
| dense 30 x 784 add b32 / numpy | 10.25 (10.1-10.64) | 10.49 (10.18-10.76) | +2.3% | 10.52, 10.24, 10.15 / 10.37, 10.54, 10.51 | within noise |
| dense 30 x 784 add b32 / rust | 10.86 (9.531-11.8) | 9.892 (9.341-11.5) | -8.9% | 10.44, 10.05, 11.74 / 10.19, 9.342, 10.72 | within noise |
| dense 30 x 784 add b512 / numpy | 11.48 (11.28-11.91) | 11.33 (11.16-12.15) | -1.3% | 11.32, 11.66, 11.68 / 11.83, 11.25, 11.28 | within noise |
| dense 30 x 784 add b512 / rust | 9.609 (9.467-9.826) | 9.55 (9.351-9.862) | -0.6% | 9.66, 9.618, 9.602 / 9.446, 9.607, 9.675 | within noise |
| dense 30 x 784 sum_axis0 b32 / numpy | 2.81 (2.795-2.842) | 2.801 (2.795-2.826) | -0.3% | 2.809, 2.818, 2.813 / 2.811, 2.806, 2.801 | within noise |
| dense 30 x 784 sum_axis0 b32 / rust | 0.7039 (0.698-0.7069) | 0.7016 (0.6973-0.7054) | -0.3% | 0.7053, 0.7036, 0.7003 / 0.7014, 0.7029, 0.6994 | within noise |
| dense 30 x 784 sum_axis0 b512 / numpy | 15.41 (15.38-15.61) | 15.42 (15.37-15.7) | +0.1% | 15.49, 15.41, 15.5 / 15.39, 15.56, 15.52 | within noise |
| dense 30 x 784 sum_axis0 b512 / rust | 7.438 (7.422-7.509) | 7.436 (7.428-7.478) | -0.0% | 7.431, 7.438, 7.468 / 7.43, 7.451, 7.454 | within noise |
| dense 10 x 30 bare downstream b32 / numpy | 5.867 (5.843-5.915) | 5.875 (5.853-5.911) | +0.1% | 5.912, 5.867, 5.843 / 5.87, 5.892, 5.867 | within noise |
| dense 10 x 30 bare downstream b32 / rust | 10.7 (10.7-10.71) | 10.71 (10.7-10.71) | +0.0% | 10.71, 10.7, 10.7 / 10.71, 10.7, 10.71 | within noise |
| dense 10 x 30 bare downstream b512 / numpy | 64.58 (64.44-64.74) | 64.67 (64.55-64.86) | +0.1% | 64.64, 64.47, 64.65 / 64.61, 64.71, 64.67 | within noise |
| dense 10 x 30 bare downstream b512 / rust | 166.7 (166.7-166.8) | 166.7 (166.7-173.9) | -0.0% | 166.7, 166.8, 166.7 / 166.7, 166.7, 170.3 | within noise |
| dense 10 x 30 bare accumulate b32 / numpy | 5.059 (5.045-5.079) | 5.079 (4.999-5.113) | +0.4% | 5.069, 5.054, 5.057 / 5.049, 5.052, 5.106 | within noise |
| dense 10 x 30 bare accumulate b32 / rust | 9.082 (9.081-9.085) | 9.083 (9.081-9.086) | +0.0% | 9.083, 9.082, 9.083 / 9.082, 9.085, 9.083 | within noise |
| dense 10 x 30 bare accumulate b512 / numpy | 32.62 (32.55-32.68) | 32.63 (32.48-32.8) | +0.0% | 32.62, 32.65, 32.62 / 32.64, 32.55, 32.64 | within noise |
| dense 10 x 30 bare accumulate b512 / rust | 136.4 (136-136.8) | 136.2 (135.9-136.5) | -0.2% | 136.4, 136.7, 136 / 136.4, 136.1, 136.1 | within noise |
| dense 10 x 30 transpose b32 / numpy | 0.8917 (0.8847-0.8959) | 0.8938 (0.882-1.002) | +0.2% | 0.891, 0.8936, 0.8884 / 0.9481, 0.8889, 0.8901 | within noise |
| dense 10 x 30 transpose b32 / rust | 0.8181 (0.8136-0.8438) | 0.818 (0.8136-0.822) | -0.0% | 0.829, 0.8163, 0.8201 / 0.8198, 0.818, 0.8177 | within noise |
| dense 10 x 30 transpose b512 / numpy | 3.391 (3.369-3.416) | 3.45 (3.351-3.539) | +1.7% | 3.391, 3.373, 3.411 / 3.432, 3.528, 3.375 | within noise |
| dense 10 x 30 transpose b512 / rust | 8.808 (8.751-8.813) | 8.81 (8.805-8.817) | +0.0% | 8.807, 8.81, 8.78 / 8.814, 8.805, 8.812 | within noise |
| dense 10 x 30 add b32 / numpy | 0.9022 (0.8896-0.9335) | 0.8985 (0.8905-0.9185) | -0.4% | 0.9043, 0.902, 0.9176 / 0.8975, 0.9026, 0.9045 | within noise |
| dense 10 x 30 add b32 / rust | 0.3753 (0.3738-0.3823) | 0.3774 (0.3756-0.3792) | +0.6% | 0.3769, 0.3753, 0.378 / 0.3768, 0.3775, 0.3775 | within noise |
| dense 10 x 30 add b512 / numpy | 0.9254 (0.9187-0.9404) | 0.919 (0.905-0.937) | -0.7% | 0.9235, 0.9251, 0.9315 / 0.9272, 0.9182, 0.9161 | within noise |
| dense 10 x 30 add b512 / rust | 0.4017 (0.3984-0.4023) | 0.3967 (0.3948-0.4017) | -1.2% | 0.4019, 0.4001, 0.401 / 0.3957, 0.3985, 0.3994 | separated, inside spread |
| dense 10 x 30 sum_axis0 b32 / numpy | 2.46 (2.448-2.517) | 2.463 (2.451-2.518) | +0.1% | 2.458, 2.484, 2.46 / 2.455, 2.493, 2.469 | within noise |
| dense 10 x 30 sum_axis0 b32 / rust | 0.5311 (0.5215-0.5334) | 0.5311 (0.5247-0.537) | +0.0% | 0.525, 0.5311, 0.5331 / 0.5331, 0.5281, 0.5309 | within noise |
| dense 10 x 30 sum_axis0 b512 / numpy | 12.2 (12.17-12.3) | 12.17 (12.15-12.18) | -0.3% | 12.18, 12.26, 12.19 / 12.17, 12.16, 12.17 | separated, inside spread |
| dense 10 x 30 sum_axis0 b512 / rust | 4.649 (4.64-4.666) | 4.648 (4.643-4.668) | -0.0% | 4.649, 4.653, 4.648 / 4.648, 4.659, 4.644 | within noise |
| attention 16 x 32 forward_batch b32 / numpy | 944.5 (743.2-1629) | 752.8 (745.1-760.7) | -20.3% | 944.5, 1188, 1175 / 751, 747.6, 760 | separated, inside spread |
| attention 16 x 32 forward_batch b32 / rust | 3050 (3047-3053) | 3051 (3045-3062) | +0.0% | 3051, 3051, 3048 / 3052, 3056, 3048 | within noise |
| attention 16 x 32 forward_batch b512 / numpy | 2.437e+04 (2.214e+04-2.666e+04) | 2.521e+04 (2.24e+04-2.568e+04) | +3.4% | 2.263e+04, 2.465e+04, 2.566e+04 / 2.387e+04, 2.402e+04, 2.557e+04 | within noise |
| attention 16 x 32 forward_batch b512 / rust | 2.759e+04 (2.71e+04-3.816e+04) | 2.749e+04 (2.719e+04-2.794e+04) | -0.3% | 3.288e+04, 2.733e+04, 2.769e+04 / 2.765e+04, 2.749e+04, 2.754e+04 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / numpy | 760 (753-1145) | 758.7 (756.3-777.2) | -0.2% | 759.2, 955.4, 755.3 / 758.7, 766.7, 758.9 | within noise |
| attention 16 x 32 hidden_delta_batch b32 / rust | 3216 (3211-3522) | 3212 (3211-3214) | -0.1% | 3211, 3369, 3216 / 3211, 3213, 3213 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / numpy | 2.932e+04 (2.858e+04-3.167e+04) | 2.916e+04 (2.71e+04-2.966e+04) | -0.6% | 2.953e+04, 2.901e+04, 3.015e+04 / 2.965e+04, 2.916e+04, 2.79e+04 | within noise |
| attention 16 x 32 hidden_delta_batch b512 / rust | 3.481e+04 (3.412e+04-3.599e+04) | 3.463e+04 (3.365e+04-3.498e+04) | -0.5% | 3.538e+04, 3.448e+04, 3.488e+04 / 3.459e+04, 3.432e+04, 3.464e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b32 / numpy | 591.2 (580.9-595.8) | 596.3 (586.8-2111) | +0.9% | 586.8, 593.6, 589 / 593.7, 597.9, 1349 | separated, inside spread |
| attention 16 x 32 accumulate_gradient_batch b32 / rust | 3815 (3814-3818) | 3815 (3814-3817) | -0.0% | 3816, 3816, 3815 / 3816, 3814, 3815 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / numpy | 4.418e+04 (3.352e+04-4.539e+04) | 4.343e+04 (3.419e+04-4.463e+04) | -1.7% | 4.512e+04, 3.838e+04, 4.418e+04 / 3.941e+04, 4.343e+04, 3.945e+04 | within noise |
| attention 16 x 32 accumulate_gradient_batch b512 / rust | 9.508e+04 (8.89e+04-9.982e+04) | 9.828e+04 (8.926e+04-1.03e+05) | +3.4% | 9.806e+04, 9.508e+04, 9.07e+04 / 1.014e+05, 9.828e+04, 9.158e+04 | within noise |
