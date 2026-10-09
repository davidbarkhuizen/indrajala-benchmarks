Old `25a3a03` against new `a6419a6`, run with `scripts/ab.py`: passes in the order ONNOONNO. Each pass ran `python /home/david/code/indrajala-ml/boundary_probe.py` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree. Machine check: profile: not recorded; busy processes: none. Each row pools 4 runs per side.

- controls: none (a probe row can carry "control": true)
- shifted: pass 1 (old, fast -8.3%), pass 2 (new, fast -5.8%), pass 8 (old, slow +5.6%); unbalanced, next: ab.py extend --order NO
- consistent: per call / Array.from_rows(10x30) -41.3% (3485 -> 2047 ns)
- consistent: per call / v.tolist() 30 -28.7% (545.2 -> 388.6 ns)
- consistent: per call / 0.5 * a (reflected) -25.3% (466 -> 348.3 ns)
- consistent: per call / a * 0.5 (scalar operand) -22.4% (392.7 -> 304.8 ns)
- 13 rows within noise (9 separated inside their spread), max |Δ| 33.9%

### per call

| case | old median (min-max) ns | new median (min-max) ns | Δ median | per-pass medians old (1, 4, 5, 8) / new (2, 3, 6, 7) | verdict |
|---|---|---|---|---|---|
| shape (getter, tuple out) | 160.4 (128.9-169.4) | 121.7 (112.4-124.2) | -24.1% | 128.9, 165.2, 155.6, 169.4 / 112.4, 124.2, 121.5, 121.9 | separated, inside spread |
| a[i, j] (index in, float out) | 230.2 (203.7-254.9) | 152.3 (148.7-159.7) | -33.9% | 203.7, 232.6, 227.9, 254.9 / 159.7, 148.7, 155.1, 149.5 | separated, inside spread |
| a[:, :-1] (slices in, Array out) | 390.6 (358.2-494.2) | 335.7 (323.9-343.4) | -14.0% | 358.2, 397.1, 384.1, 494.2 / 323.9, 339.6, 343.4, 331.8 | separated, inside spread |
| a[i, j] = x | 220.4 (206.3-264.3) | 177.7 (172.4-191.8) | -19.4% | 206.3, 217.6, 223.3, 264.3 / 180.1, 175.2, 191.8, 172.4 | separated, inside spread |
| a + b (Array operand) | 353.8 (315.6-418.4) | 292.4 (276-301.9) | -17.3% | 315.6, 353.7, 353.8, 418.4 / 276, 301.9, 293.1, 291.8 | separated, inside spread |
| a + v (broadcast) | 788.2 (705.4-850.5) | 724.7 (665.5-811.8) | -8.1% | 705.4, 805.7, 770.7, 850.5 / 665.5, 811.8, 719.7, 729.7 | within noise |
| a * 0.5 (scalar operand) | 392.7 (383.1-407.6) | 304.8 (293-325.3) | -22.4% | 383.1, 407.6, 387, 398.4 / 293, 325.3, 310.8, 298.8 | consistent |
| 0.5 * a (reflected) | 466 (435.4-485.3) | 348.3 (328.5-362.7) | -25.3% | 435.4, 471.1, 460.9, 485.3 / 328.5, 342.3, 362.7, 354.3 | consistent |
| a += b (in place) | 325.9 (290.4-331.6) | 277.1 (259.7-282.4) | -15.0% | 290.4, 323.1, 331.6, 328.7 / 259.7, 277.8, 276.4, 282.4 | separated, inside spread |
| a.tolist() 10x30 | 5755 (5371-6990) | 4093 (3801-4199) | -28.9% | 5884, 5625, 5371, 6990 / 3801, 4051, 4136, 4199 | separated, inside spread |
| v.tolist() 30 | 545.2 (511.3-597.8) | 388.6 (356.5-422.8) | -28.7% | 511.3, 552.2, 538.2, 597.8 / 356.5, 378.4, 398.8, 422.8 | consistent |
| Array(nested 10x30) | 5500 (5034-5743) | 3922 (3693-4586) | -28.7% | 5034, 5743, 5328, 5671 / 3693, 3929, 3915, 4586 | separated, inside spread |
| Array.from_rows(10x30) | 3485 (3206-4015) | 2047 (1918-2065) | -41.3% | 3206, 3613, 3356, 4015 / 1918, 2065, 2049, 2046 | consistent |
| Array.zeros((10, 30)) | 453.3 (364.2-459.7) | 345.4 (324.3-397) | -23.8% | 364.2, 459.7, 449.1, 457.5 / 324.3, 344.9, 397, 346 | within noise |
| layer_forward 10x30 (&RustArray args) | 1339 (1268-1348) | 1188 (1113-1223) | -11.3% | 1268, 1338, 1339, 1348 / 1113, 1170, 1206, 1223 | separated, inside spread |
| seed(0) (int seed) | 2692 (2454-2763) | 2412 (2319-2734) | -10.4% | 2454, 2652, 2732, 2763 / 2319, 2341, 2734, 2483 | within noise |
| seed([1, 2, 3]) (sequence seed) | 1.003e+04 (9563-1.034e+04) | 9646 (9306-1.013e+04) | -3.8% | 9563, 1.003e+04, 1.003e+04, 1.034e+04 / 9535, 9306, 1.013e+04, 9756 | within noise |
