Old `6f0e9de` against new `6f0e9de`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/epoch_op_profile.py --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `f31e318a10d7`) on both sides. Machine check: profile: identity matches; max 1-min load 0.80; busy processes: none. Each row pools 9 runs per side.

- controls: none (Rust only; read the profiled total's share)
- consistent: seconds in the run / conv-conv / mini-batch (32) (profiled total) -0.3% (1.302 -> 1.298 s)
- 161 rows within noise (15 separated inside their spread), max |Δ| 23.7%
- spread of per-pass medians over 162 rows: median 4.3%, 90th percentile 13.0%, max 66.1%
- pass shifts (median over rows of pass median / pooled median): 1 -0.0%, 2 -0.4%, 3 +0.4%, 4 +0.2%, 5 -0.7%, 6 +0.3%

### seconds in the run

| case | median (min-max) s | per-pass medians (1, 2, 3, 4, 5, 6) | spread |
|---|---|---|---|
| conv / single-example (profiled total) | 0.559 (0.539-0.576) | 0.560, 0.558, 0.559, 0.559, 0.543, 0.559 | 3.0% |
| conv / single-example layer_forward | 0.130 (0.121-0.141) | 0.131, 0.130, 0.130, 0.131, 0.122, 0.130 | 6.3% |
| conv / single-example conv_forward_batch | 0.130 (0.128-0.131) | 0.129, 0.130, 0.130, 0.130, 0.129, 0.131 | 1.1% |
| conv / single-example layer_sgd_step | 0.119 (0.116-0.122) | 0.120, 0.118, 0.119, 0.119, 0.118, 0.119 | 1.7% |
| conv / single-example layer_downstream | 0.044 (0.041-0.048) | 0.044, 0.044, 0.044, 0.044, 0.041, 0.044 | 6.3% |
| conv / single-example conv_accumulate_gradient_batch | 0.034 (0.034-0.034) | 0.034, 0.034, 0.034, 0.034, 0.034, 0.034 | 1.3% |
| conv / single-example Array.row | 0.005 (0.004-0.005) | 0.005, 0.005, 0.005, 0.005, 0.005, 0.004 | 2.2% |
| conv / single-example array_relu_mask | 0.005 (0.004-0.005) | 0.005, 0.005, 0.005, 0.005, 0.004, 0.004 | 5.4% |
| conv / single-example layer_apply_accumulated_gradient | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 6.6% |
| conv / single-example layer_hidden_delta | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 5.6% |
| conv / single-example argmax | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 17.3% |
| conv / single-example layer_output_delta | 0.001 (0.000-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 7.9% |
| conv / single-example Array.copy | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 3.8% |
| conv / single-example default_rng | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 6.7% |
| conv / mini-batch (32) (profiled total) | 0.355 (0.353-0.373) | 0.354, 0.354, 0.373, 0.362, 0.354, 0.364 | 5.3% |
| conv / mini-batch (32) conv_forward_batch | 0.128 (0.128-0.129) | 0.128, 0.128, 0.128, 0.128, 0.128, 0.128 | 0.5% |
| conv / mini-batch (32) layer_forward | 0.080 (0.079-0.094) | 0.080, 0.079, 0.093, 0.086, 0.079, 0.086 | 16.9% |
| conv / mini-batch (32) conv_accumulate_gradient_batch | 0.035 (0.035-0.036) | 0.035, 0.035, 0.036, 0.036, 0.035, 0.036 | 1.2% |
| conv / mini-batch (32) layer_forward_batch | 0.023 (0.023-0.025) | 0.023, 0.023, 0.025, 0.024, 0.023, 0.024 | 9.7% |
| conv / mini-batch (32) layer_accumulate_gradient_batch | 0.019 (0.019-0.019) | 0.019, 0.019, 0.019, 0.019, 0.019, 0.019 | 2.3% |
| conv / mini-batch (32) layer_downstream_batch | 0.014 (0.014-0.014) | 0.014, 0.014, 0.014, 0.014, 0.014, 0.014 | 2.6% |
| conv / mini-batch (32) layer_apply_accumulated_gradient | 0.005 (0.005-0.006) | 0.005, 0.005, 0.005, 0.005, 0.005, 0.005 | 3.4% |
| conv / mini-batch (32) array_relu_mask | 0.005 (0.005-0.006) | 0.005, 0.005, 0.005, 0.005, 0.005, 0.005 | 5.4% |
| conv / mini-batch (32) Array.row | 0.003 (0.003-0.003) | 0.003, 0.003, 0.003, 0.003, 0.003, 0.003 | 3.5% |
| conv / mini-batch (32) Array.take_rows | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 5.2% |
| conv / mini-batch (32) argmax | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 13.0% |
| conv / mini-batch (32) Array.copy | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 5.5% |
| conv / mini-batch (32) layer_hidden_delta_batch | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 10.1% |
| conv / mini-batch (32) layer_output_delta | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 13.0% |
| conv / mini-batch (32) default_rng | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 7.5% |
| conv-pool-conv / single-example (profiled total) | 0.566 (0.555-0.571) | 0.565, 0.569, 0.569, 0.570, 0.558, 0.567 | 2.1% |
| conv-pool-conv / single-example conv_forward_batch | 0.260 (0.259-0.261) | 0.260, 0.260, 0.260, 0.260, 0.259, 0.260 | 0.6% |
| conv-pool-conv / single-example conv_accumulate_gradient_batch | 0.046 (0.046-0.047) | 0.046, 0.047, 0.047, 0.047, 0.046, 0.046 | 1.7% |
| conv-pool-conv / single-example layer_forward | 0.030 (0.028-0.032) | 0.030, 0.031, 0.031, 0.031, 0.029, 0.030 | 9.9% |
| conv-pool-conv / single-example conv_downstream_batch | 0.025 (0.025-0.026) | 0.025, 0.026, 0.025, 0.026, 0.025, 0.025 | 1.1% |
| conv-pool-conv / single-example max_pool_forward_batch | 0.024 (0.024-0.024) | 0.024, 0.024, 0.024, 0.024, 0.024, 0.024 | 1.3% |
| conv-pool-conv / single-example layer_sgd_step | 0.022 (0.021-0.022) | 0.022, 0.022, 0.022, 0.022, 0.021, 0.022 | 7.0% |
| conv-pool-conv / single-example max_pool_downstream_batch | 0.011 (0.011-0.011) | 0.011, 0.011, 0.011, 0.011, 0.011, 0.011 | 1.0% |
| conv-pool-conv / single-example layer_downstream | 0.008 (0.008-0.009) | 0.008, 0.008, 0.008, 0.009, 0.008, 0.008 | 11.2% |
| conv-pool-conv / single-example array_relu_mask | 0.005 (0.005-0.005) | 0.005, 0.005, 0.005, 0.005, 0.005, 0.005 | 3.7% |
| conv-pool-conv / single-example Array.row | 0.004 (0.004-0.005) | 0.004, 0.004, 0.005, 0.005, 0.004, 0.004 | 3.9% |
| conv-pool-conv / single-example layer_apply_accumulated_gradient | 0.003 (0.002-0.003) | 0.003, 0.003, 0.002, 0.003, 0.002, 0.003 | 3.6% |
| conv-pool-conv / single-example layer_hidden_delta | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 5.9% |
| conv-pool-conv / single-example argmax | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 12.0% |
| conv-pool-conv / single-example layer_output_delta | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 5.1% |
| conv-pool-conv / single-example Array.copy | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 4.6% |
| conv-pool-conv / single-example default_rng | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 6.1% |
| conv-pool-conv / mini-batch (32) (profiled total) | 0.458 (0.454-0.462) | 0.456, 0.455, 0.460, 0.459, 0.455, 0.459 | 1.0% |
| conv-pool-conv / mini-batch (32) conv_forward_batch | 0.259 (0.258-0.260) | 0.259, 0.259, 0.259, 0.259, 0.258, 0.259 | 0.4% |
| conv-pool-conv / mini-batch (32) conv_accumulate_gradient_batch | 0.051 (0.050-0.051) | 0.051, 0.051, 0.051, 0.051, 0.051, 0.051 | 0.7% |
| conv-pool-conv / mini-batch (32) conv_downstream_batch | 0.028 (0.027-0.028) | 0.027, 0.027, 0.028, 0.028, 0.027, 0.028 | 2.4% |
| conv-pool-conv / mini-batch (32) max_pool_forward_batch | 0.023 (0.023-0.024) | 0.023, 0.023, 0.023, 0.023, 0.023, 0.023 | 1.1% |
| conv-pool-conv / mini-batch (32) layer_forward | 0.019 (0.018-0.021) | 0.018, 0.018, 0.020, 0.019, 0.018, 0.019 | 7.6% |
| conv-pool-conv / mini-batch (32) max_pool_downstream_batch | 0.011 (0.010-0.011) | 0.010, 0.010, 0.011, 0.011, 0.010, 0.011 | 1.0% |
| conv-pool-conv / mini-batch (32) array_relu_mask | 0.007 (0.007-0.008) | 0.007, 0.007, 0.007, 0.007, 0.007, 0.007 | 3.9% |
| conv-pool-conv / mini-batch (32) layer_forward_batch | 0.004 (0.004-0.004) | 0.004, 0.004, 0.004, 0.004, 0.004, 0.004 | 1.5% |
| conv-pool-conv / mini-batch (32) layer_accumulate_gradient_batch | 0.004 (0.004-0.004) | 0.004, 0.004, 0.004, 0.004, 0.004, 0.004 | 1.4% |
| conv-pool-conv / mini-batch (32) Array.row | 0.003 (0.003-0.003) | 0.003, 0.003, 0.003, 0.003, 0.003, 0.003 | 3.5% |
| conv-pool-conv / mini-batch (32) layer_downstream_batch | 0.003 (0.003-0.003) | 0.003, 0.003, 0.003, 0.003, 0.003, 0.003 | 2.3% |
| conv-pool-conv / mini-batch (32) Array.take_rows | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 1.9% |
| conv-pool-conv / mini-batch (32) layer_apply_accumulated_gradient | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 2.3% |
| conv-pool-conv / mini-batch (32) argmax | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 15.1% |
| conv-pool-conv / mini-batch (32) layer_hidden_delta_batch | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 6.5% |
| conv-pool-conv / mini-batch (32) Array.copy | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 5.7% |
| conv-pool-conv / mini-batch (32) layer_output_delta | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 14.2% |
| conv-pool-conv / mini-batch (32) default_rng | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 9.8% |
| conv-conv-stride2 / single-example (profiled total) | 0.559 (0.548-0.567) | 0.559, 0.551, 0.555, 0.561, 0.552, 0.564 | 2.3% |
| conv-conv-stride2 / single-example conv_forward_batch | 0.282 (0.281-0.285) | 0.283, 0.281, 0.281, 0.282, 0.282, 0.283 | 0.8% |
| conv-conv-stride2 / single-example conv_accumulate_gradient_batch | 0.048 (0.048-0.049) | 0.048, 0.048, 0.048, 0.049, 0.048, 0.049 | 1.7% |
| conv-conv-stride2 / single-example layer_forward | 0.035 (0.032-0.037) | 0.035, 0.033, 0.035, 0.036, 0.033, 0.036 | 10.7% |
| conv-conv-stride2 / single-example conv_downstream_batch | 0.031 (0.031-0.031) | 0.031, 0.031, 0.031, 0.031, 0.031, 0.031 | 2.0% |
| conv-conv-stride2 / single-example layer_sgd_step | 0.025 (0.024-0.026) | 0.026, 0.025, 0.025, 0.026, 0.025, 0.026 | 6.0% |
| conv-conv-stride2 / single-example layer_downstream | 0.010 (0.009-0.010) | 0.010, 0.009, 0.010, 0.010, 0.009, 0.010 | 13.4% |
| conv-conv-stride2 / single-example array_relu_mask | 0.005 (0.005-0.006) | 0.005, 0.005, 0.005, 0.005, 0.005, 0.005 | 4.0% |
| conv-conv-stride2 / single-example Array.row | 0.004 (0.004-0.005) | 0.005, 0.004, 0.004, 0.004, 0.004, 0.005 | 3.9% |
| conv-conv-stride2 / single-example layer_apply_accumulated_gradient | 0.002 (0.002-0.003) | 0.002, 0.002, 0.002, 0.002, 0.002, 0.002 | 3.9% |
| conv-conv-stride2 / single-example layer_hidden_delta | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 7.4% |
| conv-conv-stride2 / single-example layer_output_delta | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 5.3% |
| conv-conv-stride2 / single-example argmax | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 5.9% |
| conv-conv-stride2 / single-example Array.copy | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 15.3% |
| conv-conv-stride2 / single-example default_rng | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 10.5% |
| conv-conv-stride2 / mini-batch (32) (profiled total) | 0.468 (0.463-0.475) | 0.467, 0.464, 0.471, 0.470, 0.468, 0.467 | 1.3% |
| conv-conv-stride2 / mini-batch (32) conv_forward_batch | 0.285 (0.284-0.288) | 0.285, 0.284, 0.285, 0.285, 0.285, 0.284 | 0.4% |
| conv-conv-stride2 / mini-batch (32) conv_accumulate_gradient_batch | 0.054 (0.053-0.056) | 0.054, 0.053, 0.054, 0.054, 0.054, 0.053 | 1.2% |
| conv-conv-stride2 / mini-batch (32) conv_downstream_batch | 0.039 (0.039-0.040) | 0.039, 0.039, 0.040, 0.040, 0.039, 0.039 | 1.8% |
| conv-conv-stride2 / mini-batch (32) layer_forward | 0.022 (0.021-0.024) | 0.022, 0.021, 0.024, 0.022, 0.022, 0.022 | 10.3% |
| conv-conv-stride2 / mini-batch (32) array_relu_mask | 0.007 (0.007-0.007) | 0.007, 0.007, 0.007, 0.007, 0.007, 0.007 | 3.1% |
| conv-conv-stride2 / mini-batch (32) layer_forward_batch | 0.005 (0.005-0.005) | 0.005, 0.005, 0.005, 0.005, 0.005, 0.005 | 2.4% |
| conv-conv-stride2 / mini-batch (32) layer_accumulate_gradient_batch | 0.005 (0.005-0.005) | 0.005, 0.005, 0.005, 0.005, 0.005, 0.005 | 2.1% |
| conv-conv-stride2 / mini-batch (32) layer_downstream_batch | 0.003 (0.003-0.003) | 0.003, 0.003, 0.003, 0.003, 0.003, 0.003 | 1.6% |
| conv-conv-stride2 / mini-batch (32) Array.row | 0.003 (0.003-0.003) | 0.003, 0.003, 0.003, 0.003, 0.003, 0.003 | 3.9% |
| conv-conv-stride2 / mini-batch (32) layer_apply_accumulated_gradient | 0.002 (0.002-0.002) | 0.002, 0.002, 0.002, 0.002, 0.002, 0.002 | 2.1% |
| conv-conv-stride2 / mini-batch (32) Array.take_rows | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 4.9% |
| conv-conv-stride2 / mini-batch (32) argmax | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 10.2% |
| conv-conv-stride2 / mini-batch (32) layer_hidden_delta_batch | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 4.8% |
| conv-conv-stride2 / mini-batch (32) Array.copy | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 11.6% |
| conv-conv-stride2 / mini-batch (32) layer_output_delta | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 16.8% |
| conv-conv-stride2 / mini-batch (32) default_rng | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 5.6% |
| conv-conv / single-example (profiled total) | 1.331 (1.310-1.359) | 1.333, 1.312, 1.339, 1.330, 1.314, 1.354 | 3.2% |
| conv-conv / single-example conv_forward_batch | 0.718 (0.713-0.721) | 0.718, 0.716, 0.719, 0.715, 0.717, 0.718 | 0.6% |
| conv-conv / single-example layer_forward | 0.125 (0.117-0.136) | 0.127, 0.118, 0.127, 0.124, 0.118, 0.136 | 14.2% |
| conv-conv / single-example conv_downstream_batch | 0.115 (0.113-0.119) | 0.115, 0.113, 0.116, 0.118, 0.114, 0.118 | 4.3% |
| conv-conv / single-example layer_sgd_step | 0.101 (0.099-0.105) | 0.102, 0.100, 0.102, 0.103, 0.099, 0.104 | 4.6% |
| conv-conv / single-example conv_accumulate_gradient_batch | 0.085 (0.084-0.087) | 0.085, 0.084, 0.085, 0.085, 0.084, 0.086 | 2.8% |
| conv-conv / single-example layer_downstream | 0.047 (0.045-0.052) | 0.048, 0.045, 0.049, 0.047, 0.045, 0.051 | 12.3% |
| conv-conv / single-example array_relu_mask | 0.008 (0.008-0.009) | 0.008, 0.008, 0.009, 0.009, 0.008, 0.009 | 7.7% |
| conv-conv / single-example Array.row | 0.005 (0.005-0.005) | 0.005, 0.005, 0.005, 0.005, 0.005, 0.005 | 4.1% |
| conv-conv / single-example layer_apply_accumulated_gradient | 0.002 (0.002-0.003) | 0.002, 0.002, 0.002, 0.002, 0.002, 0.002 | 4.0% |
| conv-conv / single-example layer_hidden_delta | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 8.2% |
| conv-conv / single-example argmax | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 13.5% |
| conv-conv / single-example layer_output_delta | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 12.0% |
| conv-conv / single-example Array.copy | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 7.1% |
| conv-conv / single-example default_rng | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 7.8% |
| conv-conv / mini-batch (32) (profiled total) | 1.302 (1.294-1.316) | 1.300, 1.298, 1.298, 1.302, 1.296, 1.302 | 0.5% |
| conv-conv / mini-batch (32) conv_forward_batch | 0.770 (0.767-0.772) | 0.770, 0.769, 0.770, 0.771, 0.768, 0.770 | 0.3% |
| conv-conv / mini-batch (32) conv_downstream_batch | 0.182 (0.180-0.184) | 0.184, 0.181, 0.183, 0.183, 0.181, 0.181 | 1.7% |
| conv-conv / mini-batch (32) conv_accumulate_gradient_batch | 0.099 (0.098-0.100) | 0.099, 0.099, 0.099, 0.099, 0.099, 0.099 | 0.5% |
| conv-conv / mini-batch (32) layer_forward | 0.080 (0.077-0.089) | 0.081, 0.078, 0.078, 0.080, 0.077, 0.083 | 6.8% |
| conv-conv / mini-batch (32) layer_accumulate_gradient_batch | 0.029 (0.028-0.029) | 0.028, 0.028, 0.029, 0.029, 0.029, 0.028 | 1.1% |
| conv-conv / mini-batch (32) layer_forward_batch | 0.025 (0.025-0.026) | 0.025, 0.025, 0.026, 0.025, 0.025, 0.026 | 0.9% |
| conv-conv / mini-batch (32) layer_downstream_batch | 0.021 (0.020-0.021) | 0.021, 0.021, 0.021, 0.021, 0.021, 0.021 | 3.6% |
| conv-conv / mini-batch (32) array_relu_mask | 0.016 (0.016-0.017) | 0.017, 0.016, 0.017, 0.017, 0.016, 0.016 | 2.9% |
| conv-conv / mini-batch (32) layer_apply_accumulated_gradient | 0.008 (0.007-0.008) | 0.008, 0.008, 0.008, 0.008, 0.008, 0.008 | 3.9% |
| conv-conv / mini-batch (32) Array.row | 0.003 (0.003-0.003) | 0.003, 0.003, 0.003, 0.003, 0.003, 0.003 | 3.3% |
| conv-conv / mini-batch (32) Array.take_rows | 0.002 (0.002-0.002) | 0.002, 0.002, 0.002, 0.002, 0.002, 0.002 | 5.3% |
| conv-conv / mini-batch (32) Array.copy | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 1.9% |
| conv-conv / mini-batch (32) argmax | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 9.3% |
| conv-conv / mini-batch (32) layer_hidden_delta_batch | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 8.7% |
| conv-conv / mini-batch (32) layer_output_delta | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 24.6% |
| conv-conv / mini-batch (32) default_rng | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 18.3% |
| conv-conv16 / single-example (profiled total) | 1.680 (1.634-1.738) | 1.664, 1.645, 1.738, 1.695, 1.635, 1.695 | 6.2% |
| conv-conv16 / single-example conv_forward_batch | 0.688 (0.672-0.692) | 0.691, 0.674, 0.691, 0.688, 0.674, 0.691 | 2.5% |
| conv-conv16 / single-example layer_forward | 0.241 (0.220-0.265) | 0.225, 0.221, 0.265, 0.242, 0.220, 0.241 | 18.5% |
| conv-conv16 / single-example layer_sgd_step | 0.225 (0.219-0.235) | 0.221, 0.221, 0.233, 0.228, 0.220, 0.225 | 5.8% |
| conv-conv16 / single-example conv_downstream_batch | 0.161 (0.158-0.164) | 0.161, 0.158, 0.163, 0.161, 0.159, 0.161 | 2.6% |
| conv-conv16 / single-example conv_accumulate_gradient_batch | 0.127 (0.126-0.129) | 0.126, 0.126, 0.129, 0.128, 0.126, 0.127 | 2.2% |
| conv-conv16 / single-example layer_downstream | 0.095 (0.088-0.101) | 0.091, 0.089, 0.101, 0.095, 0.089, 0.095 | 12.9% |
| conv-conv16 / single-example array_relu_mask | 0.012 (0.012-0.013) | 0.012, 0.012, 0.013, 0.012, 0.012, 0.012 | 9.5% |
| conv-conv16 / single-example Array.row | 0.005 (0.005-0.005) | 0.005, 0.005, 0.005, 0.005, 0.005, 0.005 | 2.4% |
| conv-conv16 / single-example layer_apply_accumulated_gradient | 0.003 (0.003-0.004) | 0.003, 0.003, 0.003, 0.003, 0.003, 0.003 | 4.3% |
| conv-conv16 / single-example layer_hidden_delta | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 5.6% |
| conv-conv16 / single-example Array.copy | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 16.5% |
| conv-conv16 / single-example argmax | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 13.6% |
| conv-conv16 / single-example layer_output_delta | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 6.0% |
| conv-conv16 / single-example default_rng | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 7.5% |
| conv-conv16 / mini-batch (32) (profiled total) | 1.378 (1.358-1.392) | 1.373, 1.368, 1.381, 1.387, 1.358, 1.376 | 2.1% |
| conv-conv16 / mini-batch (32) conv_forward_batch | 0.713 (0.697-0.718) | 0.715, 0.714, 0.715, 0.714, 0.701, 0.703 | 1.9% |
| conv-conv16 / mini-batch (32) conv_downstream_batch | 0.192 (0.190-0.194) | 0.193, 0.192, 0.192, 0.191, 0.193, 0.192 | 1.2% |
| conv-conv16 / mini-batch (32) layer_forward | 0.160 (0.151-0.177) | 0.157, 0.162, 0.157, 0.166, 0.157, 0.166 | 5.9% |
| conv-conv16 / mini-batch (32) conv_accumulate_gradient_batch | 0.119 (0.118-0.120) | 0.119, 0.119, 0.119, 0.118, 0.119, 0.119 | 1.3% |
| conv-conv16 / mini-batch (32) layer_accumulate_gradient_batch | 0.029 (0.029-0.030) | 0.029, 0.029, 0.029, 0.029, 0.029, 0.029 | 1.7% |
| conv-conv16 / mini-batch (32) layer_forward_batch | 0.027 (0.026-0.028) | 0.027, 0.027, 0.027, 0.027, 0.027, 0.027 | 2.6% |
| conv-conv16 / mini-batch (32) layer_downstream_batch | 0.025 (0.024-0.027) | 0.025, 0.025, 0.025, 0.025, 0.025, 0.025 | 3.7% |
| conv-conv16 / mini-batch (32) array_relu_mask | 0.024 (0.024-0.025) | 0.024, 0.024, 0.024, 0.024, 0.024, 0.024 | 1.2% |
| conv-conv16 / mini-batch (32) layer_apply_accumulated_gradient | 0.017 (0.017-0.017) | 0.017, 0.017, 0.017, 0.017, 0.017, 0.017 | 1.3% |
| conv-conv16 / mini-batch (32) Array.row | 0.003 (0.003-0.003) | 0.003, 0.003, 0.003, 0.003, 0.003, 0.003 | 8.9% |
| conv-conv16 / mini-batch (32) Array.take_rows | 0.002 (0.002-0.002) | 0.002, 0.002, 0.002, 0.002, 0.002, 0.002 | 6.6% |
| conv-conv16 / mini-batch (32) Array.copy | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 11.5% |
| conv-conv16 / mini-batch (32) argmax | 0.001 (0.001-0.001) | 0.001, 0.001, 0.001, 0.001, 0.001, 0.001 | 8.9% |
| conv-conv16 / mini-batch (32) layer_hidden_delta_batch | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 5.9% |
| conv-conv16 / mini-batch (32) layer_output_delta | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 66.1% |
| conv-conv16 / mini-batch (32) default_rng | 0.000 (0.000-0.000) | 0.000, 0.000, 0.000, 0.000, 0.000, 0.000 | 6.8% |
