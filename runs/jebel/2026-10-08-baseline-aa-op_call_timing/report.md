Old `6f0e9de` against new `6f0e9de`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/op_call_timing.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `f31e318a10d7`) on both sides. Machine check: profile: identity matches; max 1-min load 0.86; busy processes: none. Each row pools 6 runs per side.

- controls: none (Rust only; the whole run's seconds are the context)
- 23 rows within noise (4 separated inside their spread), max |Δ| 8.1%

### whole run

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv / mini-batch (32) / 0:0 | 0.348 (0.329-0.350) | 0.330 (0.328-0.339) | -5.4% | 0.348, 0.339, 0.339 / 0.329, 0.334, 0.334 | separated, inside spread |
| conv-pool-conv / mini-batch (32) / 0:0 | 0.439 (0.435-0.442) | 0.437 (0.433-0.444) | -0.7% | 0.441, 0.435, 0.441 / 0.437, 0.439, 0.437 | within noise |
| conv-conv-stride2 / mini-batch (32) / 0:0 | 0.449 (0.445-0.453) | 0.449 (0.443-0.450) | -0.0% | 0.450, 0.447, 0.449 / 0.448, 0.446, 0.450 | within noise |
| conv-conv / mini-batch (32) / 0:0 | 1.289 (1.277-1.294) | 1.282 (1.279-1.290) | -0.6% | 1.289, 1.285, 1.289 / 1.281, 1.283, 1.285 | separated, inside spread |
| conv-conv16 / mini-batch (32) / 0:0 | 1.340 (1.332-1.353) | 1.348 (1.329-1.355) | +0.6% | 1.337, 1.337, 1.353 / 1.331, 1.348, 1.354 | within noise |

### per call

| case | old median (min-max) µs | new median (min-max) µs | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (32, 5408) (21632, 9) (8, 9) (8,) | 575.5 (567.4-579.4) | 572.1 (570.3-577.6) | -0.6% | 577, 575.7, 571.9 / 571.1, 575, 572.3 | within noise |
| conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (16, 5408) (10816, 9) (8, 9) (8,) | 280.8 (277.8-282.6) | 280.1 (275.4-296.9) | -0.2% | 280.8, 280.6, 279.2 / 286.2, 278.1, 280.2 | within noise |
| conv-pool-conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (32, 5408) (21632, 9) (8, 9) (8,) | 585.7 (579-591.2) | 582.6 (578.5-585.9) | -0.5% | 586.5, 579.4, 588.8 / 582.9, 582.2, 582.5 | within noise |
| conv-pool-conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (32, 968) (3872, 72) (8, 72) (8,) | 235.8 (231-242.6) | 236 (232.4-238.7) | +0.0% | 236.8, 232.5, 238.7 / 235.6, 236, 235.9 | within noise |
| conv-pool-conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (16, 5408) (10816, 9) (8, 9) (8,) | 282.4 (278.2-315.9) | 283.1 (279.2-320.4) | +0.3% | 283.7, 278.3, 299.5 / 301.2, 281.8, 298.2 | within noise |
| conv-pool-conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (16, 968) (1936, 72) (8, 72) (8,) | 100.5 (93.67-103.5) | 97.34 (94.69-99.26) | -3.1% | 101.9, 94.52, 102 / 96.97, 97.34, 97.39 | within noise |
| conv-conv-stride2 / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (32, 5408) (21632, 9) (8, 9) (8,) | 573.6 (569.5-576.8) | 571.9 (567.7-576.3) | -0.3% | 575.7, 571.1, 574.1 / 572.1, 569.4, 574.5 | within noise |
| conv-conv-stride2 / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (32, 1152) (4608, 72) (8, 72) (8,) | 289.4 (285.1-293.6) | 288.7 (281.3-290.2) | -0.2% | 287.6, 289.8, 289.3 / 286.1, 285.5, 289.1 | within noise |
| conv-conv-stride2 / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (16, 5408) (10816, 9) (8, 9) (8,) | 279.4 (273.7-310.9) | 276.7 (274.9-321.8) | -1.0% | 279.4, 275.2, 295.8 / 276.2, 275.7, 300.1 | within noise |
| conv-conv-stride2 / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (16, 1152) (2304, 72) (8, 72) (8,) | 128 (126.9-130.5) | 127.9 (125.7-152.1) | -0.1% | 128.5, 128, 128.7 / 126.3, 139.8, 129.3 | within noise |
| conv-conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (32, 5408) (21632, 9) (8, 9) (8,) | 694.9 (683.5-699.1) | 698.2 (693-701.5) | +0.5% | 696.9, 687.9, 695.8 / 698.2, 696.9, 698.6 | within noise |
| conv-conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (32, 4608) (18432, 72) (8, 72) (8,) | 947.5 (935.3-954.2) | 942.3 (936.3-953) | -0.5% | 951.7, 936, 947.5 / 945.7, 944.6, 938.8 | within noise |
| conv-conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (16, 5408) (10816, 9) (8, 9) (8,) | 350 (320.5-379.6) | 321.6 (316.8-371.1) | -8.1% | 354, 349.1, 346.7 / 345.9, 321, 326.3 | separated, inside spread |
| conv-conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (16, 4608) (9216, 72) (8, 72) (8,) | 709.3 (690.7-743.4) | 739 (730.3-746.8) | +4.2% | 693.8, 720.1, 729 / 734.2, 743.5, 736.1 | separated, inside spread |
| conv-conv16 / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (32, 5408) (21632, 9) (8, 9) (8,) | 682.6 (664.7-688.7) | 666.8 (650.2-679.1) | -2.3% | 684.7, 673, 683.6 / 655.1, 668.1, 675.5 | within noise |
| conv-conv16 / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (32, 9216) (18432, 72) (16, 72) (16,) | 1271 (1257-1277) | 1269 (1259-1275) | -0.2% | 1264, 1273, 1267 / 1271, 1264, 1270 | within noise |
| conv-conv16 / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (16, 5408) (10816, 9) (8, 9) (8,) | 353.7 (325.3-389.5) | 336.5 (324.2-384) | -4.9% | 353.7, 355.7, 357.4 / 362, 350.8, 329.3 | within noise |
| conv-conv16 / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (16, 9216) (9216, 72) (16, 72) (16,) | 736.1 (679.5-786.1) | 739.3 (684.7-788.4) | +0.4% | 740.1, 722.2, 746.7 / 694.1, 739.3, 780.6 | within noise |
