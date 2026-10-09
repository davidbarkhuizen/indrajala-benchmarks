Old `25a3a03` against new `a6419a6`, run with `scripts/ab.py`: passes in the order ONNOONNO. Each pass ran `python scripts/epoch_op_profile.py --architectures conv --repeats 3 --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree. Machine check: profile: not recorded; busy processes: none. Each row pools 12 runs per side.

- controls: none (Rust only; read the profiled total's share)
- shifted: pass 6 (new, fast -6.9%), pass 8 (old, slow +12.1%); unbalanced, next: ab.py extend --order ONNO
- 28 rows within noise (1 separated inside their spread), max |Δ| 16.2%

### seconds in the run

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 5, 8) / new (2, 3, 6, 7) | verdict |
|---|---|---|---|---|---|
| conv / single-example (profiled total) | 0.794 (0.687-1.033) | 0.837 (0.743-0.979) | +5.3% | 0.809, 0.769, 0.763, 0.894 / 0.851, 0.796, 0.755, 0.845 | within noise |
| conv / single-example layer_sgd_step | 0.177 (0.150-0.266) | 0.190 (0.152-0.234) | +7.5% | 0.188, 0.170, 0.159, 0.207 / 0.219, 0.182, 0.170, 0.198 | within noise |
| conv / single-example layer_forward | 0.168 (0.141-0.235) | 0.177 (0.160-0.205) | +5.6% | 0.167, 0.165, 0.161, 0.190 / 0.186, 0.168, 0.161, 0.178 | within noise |
| conv / single-example conv_forward_batch | 0.173 (0.156-0.201) | 0.188 (0.168-0.215) | +8.9% | 0.167, 0.169, 0.173, 0.200 / 0.193, 0.178, 0.172, 0.188 | within noise |
| conv / single-example layer_downstream | 0.056 (0.050-0.073) | 0.061 (0.055-0.071) | +8.4% | 0.054, 0.057, 0.055, 0.065 / 0.062, 0.058, 0.055, 0.063 | within noise |
| conv / single-example conv_accumulate_gradient_batch | 0.057 (0.051-0.063) | 0.060 (0.055-0.068) | +4.6% | 0.051, 0.056, 0.057, 0.063 / 0.057, 0.059, 0.056, 0.062 | within noise |
| conv / single-example Array.row | 0.007 (0.007-0.009) | 0.007 (0.006-0.009) | -2.8% | 0.008, 0.007, 0.007, 0.008 / 0.007, 0.007, 0.006, 0.007 | within noise |
| conv / single-example array_relu_mask | 0.006 (0.006-0.030) | 0.006 (0.005-0.008) | +0.6% | 0.007, 0.006, 0.006, 0.007 / 0.007, 0.006, 0.006, 0.007 | within noise |
| conv / single-example layer_hidden_delta | 0.002 (0.001-0.003) | 0.002 (0.001-0.002) | -10.8% | 0.002, 0.002, 0.002, 0.002 / 0.002, 0.002, 0.002, 0.002 | within noise |
| conv / single-example layer_apply_accumulated_gradient | 0.002 (0.001-0.003) | 0.002 (0.001-0.002) | -10.8% | 0.002, 0.002, 0.002, 0.002 / 0.002, 0.001, 0.001, 0.002 | within noise |
| conv / single-example layer_output_delta | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -7.6% | 0.001, 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001, 0.001 | within noise |
| conv / single-example argmax | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -15.2% | 0.001, 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001, 0.001 | within noise |
| conv / single-example Array.copy | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | +4.8% | 0.001, 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001, 0.001 | within noise |
| conv / mini-batch (32) (profiled total) | 0.604 (0.556-0.781) | 0.658 (0.603-0.734) | +9.1% | 0.571, 0.605, 0.603, 0.680 / 0.664, 0.643, 0.612, 0.692 | within noise |
| conv / mini-batch (32) conv_forward_batch | 0.171 (0.152-0.225) | 0.184 (0.170-0.226) | +7.7% | 0.155, 0.171, 0.170, 0.186 / 0.181, 0.184, 0.175, 0.192 | within noise |
| conv / mini-batch (32) layer_forward | 0.096 (0.082-0.119) | 0.100 (0.094-0.129) | +3.9% | 0.083, 0.096, 0.096, 0.102 / 0.095, 0.100, 0.099, 0.106 | within noise |
| conv / mini-batch (32) conv_accumulate_gradient_batch | 0.069 (0.067-0.089) | 0.075 (0.067-0.082) | +7.6% | 0.068, 0.070, 0.069, 0.077 / 0.071, 0.075, 0.071, 0.079 | within noise |
| conv / mini-batch (32) layer_accumulate_gradient_batch | 0.057 (0.055-0.077) | 0.064 (0.057-0.126) | +11.8% | 0.057, 0.057, 0.057, 0.065 / 0.067, 0.063, 0.057, 0.069 | within noise |
| conv / mini-batch (32) layer_forward_batch | 0.048 (0.046-0.060) | 0.051 (0.048-0.057) | +5.8% | 0.047, 0.048, 0.048, 0.052 / 0.050, 0.051, 0.049, 0.054 | within noise |
| conv / mini-batch (32) layer_downstream_batch | 0.042 (0.039-0.054) | 0.046 (0.042-0.052) | +8.0% | 0.041, 0.042, 0.042, 0.049 / 0.045, 0.046, 0.043, 0.050 | within noise |
| conv / mini-batch (32) array_relu_mask | 0.020 (0.018-0.023) | 0.021 (0.020-0.023) | +3.2% | 0.020, 0.020, 0.019, 0.022 / 0.021, 0.021, 0.020, 0.023 | within noise |
| conv / mini-batch (32) layer_apply_accumulated_gradient | 0.014 (0.012-0.020) | 0.015 (0.013-0.020) | +8.7% | 0.014, 0.013, 0.013, 0.017 / 0.014, 0.015, 0.013, 0.019 | within noise |
| conv / mini-batch (32) Array.row | 0.004 (0.004-0.005) | 0.004 (0.004-0.005) | -0.9% | 0.004, 0.004, 0.004, 0.005 / 0.004, 0.004, 0.004, 0.005 | within noise |
| conv / mini-batch (32) Array.take_rows | 0.004 (0.003-0.005) | 0.004 (0.003-0.004) | +0.7% | 0.004, 0.003, 0.003, 0.004 / 0.004, 0.004, 0.003, 0.004 | within noise |
| conv / mini-batch (32) argmax | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -11.5% | 0.001, 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001, 0.001 | within noise |
| conv / mini-batch (32) Array.copy | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -1.1% | 0.001, 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001, 0.001 | within noise |
| conv / mini-batch (32) layer_hidden_delta_batch | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | +6.2% | 0.000, 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000, 0.000 | within noise |
| conv / mini-batch (32) layer_output_delta | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -16.2% | 0.000, 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000, 0.000 | separated, inside spread |
