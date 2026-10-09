Old `6f0e9de` against new `6f0e9de`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/op_call_timing.py --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `f31e318a10d7`) on both sides. Machine check: profile: identity matches; max 1-min load 0.86; busy processes: none. Each row pools 6 runs per side.

- controls: none (Rust only; the whole run's seconds are the context)
- 23 rows within noise (4 separated inside their spread), max |Δ| 8.1%
- spread of per-pass medians over 23 rows: median 2.7%, 90th percentile 10.1%, max 11.7%
- pass shifts (median over rows of pass median / pooled median): 1 +0.4%, 2 -0.3%, 3 -0.3%, 4 -0.5%, 5 -0.0%, 6 +0.6%

### whole run

| case | median (min-max) s | per-pass medians (1, 2, 3, 4, 5, 6) | spread |
|---|---|---|---|
| conv / mini-batch (32) / 0:0 | 0.334 (0.328-0.350) | 0.348, 0.329, 0.334, 0.339, 0.334, 0.339 | 5.7% |
| conv-pool-conv / mini-batch (32) / 0:0 | 0.438 (0.433-0.444) | 0.441, 0.437, 0.439, 0.435, 0.437, 0.441 | 1.4% |
| conv-conv-stride2 / mini-batch (32) / 0:0 | 0.449 (0.443-0.453) | 0.450, 0.448, 0.446, 0.447, 0.450, 0.449 | 1.0% |
| conv-conv / mini-batch (32) / 0:0 | 1.287 (1.277-1.294) | 1.289, 1.281, 1.283, 1.285, 1.285, 1.289 | 0.7% |
| conv-conv16 / mini-batch (32) / 0:0 | 1.343 (1.329-1.355) | 1.337, 1.331, 1.348, 1.337, 1.354, 1.353 | 1.7% |

### per call

| case | median (min-max) µs | per-pass medians (1, 2, 3, 4, 5, 6) | spread |
|---|---|---|---|
| conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (32, 5408) (21632, 9) (8, 9) (8,) | 574 (567.4-579.4) | 577, 571.1, 575, 575.7, 572.3, 571.9 | 1.0% |
| conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (16, 5408) (10816, 9) (8, 9) (8,) | 280.3 (275.4-296.9) | 280.8, 286.2, 278.1, 280.6, 280.2, 279.2 | 2.9% |
| conv-pool-conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (32, 5408) (21632, 9) (8, 9) (8,) | 584.5 (578.5-591.2) | 586.5, 582.9, 582.2, 579.4, 582.5, 588.8 | 1.6% |
| conv-pool-conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (32, 968) (3872, 72) (8, 72) (8,) | 236 (231-242.6) | 236.8, 235.6, 236, 232.5, 235.9, 238.7 | 2.7% |
| conv-pool-conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (16, 5408) (10816, 9) (8, 9) (8,) | 282.6 (278.2-320.4) | 283.7, 301.2, 281.8, 278.3, 298.2, 299.5 | 8.1% |
| conv-pool-conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (16, 968) (1936, 72) (8, 72) (8,) | 98.37 (93.67-103.5) | 101.9, 96.97, 97.34, 94.52, 97.39, 102 | 7.6% |
| conv-conv-stride2 / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (32, 5408) (21632, 9) (8, 9) (8,) | 572.7 (567.7-576.8) | 575.7, 572.1, 569.4, 571.1, 574.5, 574.1 | 1.1% |
| conv-conv-stride2 / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (32, 1152) (4608, 72) (8, 72) (8,) | 289.3 (281.3-293.6) | 287.6, 286.1, 285.5, 289.8, 289.1, 289.3 | 1.5% |
| conv-conv-stride2 / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (16, 5408) (10816, 9) (8, 9) (8,) | 278 (273.7-321.8) | 279.4, 276.2, 275.7, 275.2, 300.1, 295.8 | 9.0% |
| conv-conv-stride2 / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (16, 1152) (2304, 72) (8, 72) (8,) | 127.9 (125.7-152.1) | 128.5, 126.3, 139.8, 128, 129.3, 128.7 | 10.6% |
| conv-conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (32, 5408) (21632, 9) (8, 9) (8,) | 696.1 (683.5-701.5) | 696.9, 698.2, 696.9, 687.9, 698.6, 695.8 | 1.5% |
| conv-conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (32, 4608) (18432, 72) (8, 72) (8,) | 945.7 (935.3-954.2) | 951.7, 945.7, 944.6, 936, 938.8, 947.5 | 1.7% |
| conv-conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (16, 5408) (10816, 9) (8, 9) (8,) | 327.4 (316.8-379.6) | 354, 345.9, 321, 349.1, 326.3, 346.7 | 10.1% |
| conv-conv / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (16, 4608) (9216, 72) (8, 72) (8,) | 734.3 (690.7-746.8) | 693.8, 734.2, 743.5, 720.1, 736.1, 729 | 6.8% |
| conv-conv16 / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (32, 5408) (21632, 9) (8, 9) (8,) | 678 (650.2-688.7) | 684.7, 655.1, 668.1, 673, 675.5, 683.6 | 4.4% |
| conv-conv16 / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (32, 9216) (18432, 72) (16, 72) (16,) | 1269 (1257-1277) | 1264, 1271, 1264, 1273, 1270, 1267 | 0.7% |
| conv-conv16 / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (16, 5408) (10816, 9) (8, 9) (8,) | 336.5 (324.2-389.5) | 353.7, 362, 350.8, 355.7, 329.3, 357.4 | 9.7% |
| conv-conv16 / mini-batch (32) / 0:0 / conv_accumulate_gradient_batch (16, 9216) (9216, 72) (16, 72) (16,) | 739.3 (679.5-788.4) | 740.1, 694.1, 739.3, 722.2, 780.6, 746.7 | 11.7% |
