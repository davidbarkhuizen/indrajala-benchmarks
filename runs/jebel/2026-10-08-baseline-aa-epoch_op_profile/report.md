Old `6f0e9de` against new `6f0e9de`, run with `scripts/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/epoch_op_profile.py --out <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `f31e318a10d7`) on both sides. Machine check: profile: identity matches; max 1-min load 0.80; busy processes: none. Each row pools 9 runs per side.

- controls: none (Rust only; read the profiled total's share)
- consistent: seconds in the run / conv-conv / mini-batch (32) (profiled total) -0.3% (1.302 -> 1.298 s)
- 161 rows within noise (15 separated inside their spread), max |Δ| 23.7%

### seconds in the run

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| conv / single-example (profiled total) | 0.559 (0.539-0.576) | 0.558 (0.542-0.576) | -0.2% | 0.560, 0.559, 0.559 / 0.558, 0.559, 0.543 | separated, inside spread |
| conv / single-example layer_forward | 0.131 (0.121-0.141) | 0.130 (0.121-0.141) | -0.2% | 0.131, 0.131, 0.130 / 0.130, 0.130, 0.122 | within noise |
| conv / single-example conv_forward_batch | 0.130 (0.128-0.131) | 0.130 (0.129-0.130) | +0.0% | 0.129, 0.130, 0.131 / 0.130, 0.130, 0.129 | within noise |
| conv / single-example layer_sgd_step | 0.120 (0.116-0.122) | 0.119 (0.117-0.121) | -0.8% | 0.120, 0.119, 0.119 / 0.118, 0.119, 0.118 | within noise |
| conv / single-example layer_downstream | 0.044 (0.041-0.048) | 0.044 (0.041-0.048) | -0.2% | 0.044, 0.044, 0.044 / 0.044, 0.044, 0.041 | within noise |
| conv / single-example conv_accumulate_gradient_batch | 0.034 (0.034-0.034) | 0.034 (0.034-0.034) | +0.2% | 0.034, 0.034, 0.034 / 0.034, 0.034, 0.034 | within noise |
| conv / single-example Array.row | 0.005 (0.004-0.005) | 0.005 (0.004-0.005) | +0.5% | 0.005, 0.005, 0.004 / 0.005, 0.005, 0.005 | within noise |
| conv / single-example array_relu_mask | 0.005 (0.004-0.005) | 0.005 (0.004-0.005) | -0.6% | 0.005, 0.005, 0.004 / 0.005, 0.005, 0.004 | within noise |
| conv / single-example layer_apply_accumulated_gradient | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | +1.1% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv / single-example layer_hidden_delta | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | +3.2% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv / single-example argmax | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -5.2% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv / single-example layer_output_delta | 0.001 (0.000-0.001) | 0.001 (0.000-0.001) | -0.2% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv / single-example Array.copy | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -0.1% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv / single-example default_rng | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -1.8% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv / mini-batch (32) (profiled total) | 0.362 (0.353-0.373) | 0.354 (0.353-0.373) | -2.4% | 0.354, 0.362, 0.364 / 0.354, 0.373, 0.354 | within noise |
| conv / mini-batch (32) conv_forward_batch | 0.128 (0.128-0.129) | 0.128 (0.128-0.128) | +0.2% | 0.128, 0.128, 0.128 / 0.128, 0.128, 0.128 | within noise |
| conv / mini-batch (32) layer_forward | 0.086 (0.080-0.094) | 0.079 (0.079-0.094) | -7.6% | 0.080, 0.086, 0.086 / 0.079, 0.093, 0.079 | within noise |
| conv / mini-batch (32) conv_accumulate_gradient_batch | 0.036 (0.035-0.036) | 0.035 (0.035-0.036) | -0.8% | 0.035, 0.036, 0.036 / 0.035, 0.036, 0.035 | within noise |
| conv / mini-batch (32) layer_forward_batch | 0.024 (0.023-0.025) | 0.023 (0.023-0.025) | -3.6% | 0.023, 0.024, 0.024 / 0.023, 0.025, 0.023 | within noise |
| conv / mini-batch (32) layer_accumulate_gradient_batch | 0.019 (0.019-0.019) | 0.019 (0.019-0.019) | -1.2% | 0.019, 0.019, 0.019 / 0.019, 0.019, 0.019 | within noise |
| conv / mini-batch (32) layer_downstream_batch | 0.014 (0.014-0.014) | 0.014 (0.014-0.014) | -0.3% | 0.014, 0.014, 0.014 / 0.014, 0.014, 0.014 | within noise |
| conv / mini-batch (32) layer_apply_accumulated_gradient | 0.005 (0.005-0.006) | 0.005 (0.005-0.006) | -1.0% | 0.005, 0.005, 0.005 / 0.005, 0.005, 0.005 | within noise |
| conv / mini-batch (32) array_relu_mask | 0.005 (0.005-0.006) | 0.005 (0.005-0.005) | -2.6% | 0.005, 0.005, 0.005 / 0.005, 0.005, 0.005 | within noise |
| conv / mini-batch (32) Array.row | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | -2.1% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | within noise |
| conv / mini-batch (32) Array.take_rows | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -0.9% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv / mini-batch (32) argmax | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | +7.0% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv / mini-batch (32) Array.copy | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | +0.4% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv / mini-batch (32) layer_hidden_delta_batch | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -1.6% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv / mini-batch (32) layer_output_delta | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -3.2% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv / mini-batch (32) default_rng | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | +2.9% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-pool-conv / single-example (profiled total) | 0.566 (0.558-0.570) | 0.566 (0.555-0.571) | -0.0% | 0.565, 0.570, 0.567 / 0.569, 0.569, 0.558 | within noise |
| conv-pool-conv / single-example conv_forward_batch | 0.260 (0.259-0.261) | 0.260 (0.259-0.260) | -0.1% | 0.260, 0.260, 0.260 / 0.260, 0.260, 0.259 | within noise |
| conv-pool-conv / single-example conv_accumulate_gradient_batch | 0.047 (0.046-0.047) | 0.046 (0.046-0.047) | -0.0% | 0.046, 0.047, 0.046 / 0.047, 0.047, 0.046 | within noise |
| conv-pool-conv / single-example layer_forward | 0.030 (0.028-0.031) | 0.030 (0.028-0.032) | +1.2% | 0.030, 0.031, 0.030 / 0.031, 0.031, 0.029 | within noise |
| conv-pool-conv / single-example conv_downstream_batch | 0.025 (0.025-0.026) | 0.025 (0.025-0.026) | -0.1% | 0.025, 0.026, 0.025 / 0.026, 0.025, 0.025 | within noise |
| conv-pool-conv / single-example max_pool_forward_batch | 0.024 (0.024-0.024) | 0.024 (0.024-0.024) | +0.0% | 0.024, 0.024, 0.024 / 0.024, 0.024, 0.024 | within noise |
| conv-pool-conv / single-example layer_sgd_step | 0.022 (0.021-0.022) | 0.022 (0.021-0.022) | -0.3% | 0.022, 0.022, 0.022 / 0.022, 0.022, 0.021 | within noise |
| conv-pool-conv / single-example max_pool_downstream_batch | 0.011 (0.011-0.011) | 0.011 (0.011-0.011) | -0.1% | 0.011, 0.011, 0.011 / 0.011, 0.011, 0.011 | within noise |
| conv-pool-conv / single-example layer_downstream | 0.008 (0.008-0.009) | 0.008 (0.008-0.009) | +1.6% | 0.008, 0.009, 0.008 / 0.008, 0.008, 0.008 | within noise |
| conv-pool-conv / single-example array_relu_mask | 0.005 (0.005-0.005) | 0.005 (0.005-0.005) | +0.4% | 0.005, 0.005, 0.005 / 0.005, 0.005, 0.005 | within noise |
| conv-pool-conv / single-example Array.row | 0.004 (0.004-0.005) | 0.004 (0.004-0.005) | -1.3% | 0.004, 0.005, 0.004 / 0.004, 0.005, 0.004 | within noise |
| conv-pool-conv / single-example layer_apply_accumulated_gradient | 0.003 (0.002-0.003) | 0.002 (0.002-0.003) | -1.1% | 0.003, 0.003, 0.003 / 0.003, 0.002, 0.002 | within noise |
| conv-pool-conv / single-example layer_hidden_delta | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -4.5% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-pool-conv / single-example argmax | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | +5.8% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-pool-conv / single-example layer_output_delta | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | +1.6% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-pool-conv / single-example Array.copy | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -0.3% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-pool-conv / single-example default_rng | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | +1.1% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-pool-conv / mini-batch (32) (profiled total) | 0.459 (0.456-0.461) | 0.457 (0.454-0.462) | -0.5% | 0.456, 0.459, 0.459 / 0.455, 0.460, 0.455 | within noise |
| conv-pool-conv / mini-batch (32) conv_forward_batch | 0.259 (0.258-0.260) | 0.259 (0.258-0.259) | -0.1% | 0.259, 0.259, 0.259 / 0.259, 0.259, 0.258 | within noise |
| conv-pool-conv / mini-batch (32) conv_accumulate_gradient_batch | 0.051 (0.051-0.051) | 0.051 (0.050-0.051) | -0.3% | 0.051, 0.051, 0.051 / 0.051, 0.051, 0.051 | within noise |
| conv-pool-conv / mini-batch (32) conv_downstream_batch | 0.028 (0.027-0.028) | 0.027 (0.027-0.028) | -1.1% | 0.027, 0.028, 0.028 / 0.027, 0.028, 0.027 | within noise |
| conv-pool-conv / mini-batch (32) max_pool_forward_batch | 0.023 (0.023-0.023) | 0.023 (0.023-0.024) | -0.0% | 0.023, 0.023, 0.023 / 0.023, 0.023, 0.023 | within noise |
| conv-pool-conv / mini-batch (32) layer_forward | 0.019 (0.018-0.021) | 0.019 (0.018-0.020) | -2.7% | 0.018, 0.019, 0.019 / 0.018, 0.020, 0.018 | within noise |
| conv-pool-conv / mini-batch (32) max_pool_downstream_batch | 0.011 (0.010-0.011) | 0.011 (0.010-0.011) | +0.2% | 0.010, 0.011, 0.011 / 0.010, 0.011, 0.010 | within noise |
| conv-pool-conv / mini-batch (32) array_relu_mask | 0.007 (0.007-0.007) | 0.007 (0.007-0.008) | -1.5% | 0.007, 0.007, 0.007 / 0.007, 0.007, 0.007 | within noise |
| conv-pool-conv / mini-batch (32) layer_forward_batch | 0.004 (0.004-0.004) | 0.004 (0.004-0.004) | -0.5% | 0.004, 0.004, 0.004 / 0.004, 0.004, 0.004 | within noise |
| conv-pool-conv / mini-batch (32) layer_accumulate_gradient_batch | 0.004 (0.004-0.004) | 0.004 (0.004-0.004) | -0.2% | 0.004, 0.004, 0.004 / 0.004, 0.004, 0.004 | within noise |
| conv-pool-conv / mini-batch (32) Array.row | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | +0.9% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | within noise |
| conv-pool-conv / mini-batch (32) layer_downstream_batch | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | +0.1% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | within noise |
| conv-pool-conv / mini-batch (32) Array.take_rows | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -1.0% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-pool-conv / mini-batch (32) layer_apply_accumulated_gradient | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -1.1% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-pool-conv / mini-batch (32) argmax | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | +0.0% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-pool-conv / mini-batch (32) layer_hidden_delta_batch | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | +2.3% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-pool-conv / mini-batch (32) Array.copy | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -2.5% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-pool-conv / mini-batch (32) layer_output_delta | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -0.4% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-pool-conv / mini-batch (32) default_rng | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -1.8% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-conv-stride2 / single-example (profiled total) | 0.561 (0.558-0.567) | 0.552 (0.548-0.562) | -1.6% | 0.559, 0.561, 0.564 / 0.551, 0.555, 0.552 | separated, inside spread |
| conv-conv-stride2 / single-example conv_forward_batch | 0.283 (0.282-0.285) | 0.281 (0.281-0.284) | -0.5% | 0.283, 0.282, 0.283 / 0.281, 0.281, 0.282 | separated, inside spread |
| conv-conv-stride2 / single-example conv_accumulate_gradient_batch | 0.049 (0.048-0.049) | 0.048 (0.048-0.049) | -1.5% | 0.048, 0.049, 0.049 / 0.048, 0.048, 0.048 | within noise |
| conv-conv-stride2 / single-example layer_forward | 0.036 (0.034-0.037) | 0.033 (0.032-0.037) | -8.3% | 0.035, 0.036, 0.036 / 0.033, 0.035, 0.033 | separated, inside spread |
| conv-conv-stride2 / single-example conv_downstream_batch | 0.031 (0.031-0.031) | 0.031 (0.031-0.031) | -1.5% | 0.031, 0.031, 0.031 / 0.031, 0.031, 0.031 | separated, inside spread |
| conv-conv-stride2 / single-example layer_sgd_step | 0.026 (0.025-0.026) | 0.025 (0.024-0.026) | -4.6% | 0.026, 0.026, 0.026 / 0.025, 0.025, 0.025 | separated, inside spread |
| conv-conv-stride2 / single-example layer_downstream | 0.010 (0.010-0.010) | 0.009 (0.009-0.010) | -10.7% | 0.010, 0.010, 0.010 / 0.009, 0.010, 0.009 | separated, inside spread |
| conv-conv-stride2 / single-example array_relu_mask | 0.005 (0.005-0.006) | 0.005 (0.005-0.005) | -3.4% | 0.005, 0.005, 0.005 / 0.005, 0.005, 0.005 | separated, inside spread |
| conv-conv-stride2 / single-example Array.row | 0.005 (0.004-0.005) | 0.004 (0.004-0.005) | -1.7% | 0.005, 0.004, 0.005 / 0.004, 0.004, 0.004 | separated, inside spread |
| conv-conv-stride2 / single-example layer_apply_accumulated_gradient | 0.002 (0.002-0.003) | 0.002 (0.002-0.003) | +0.0% | 0.002, 0.002, 0.002 / 0.002, 0.002, 0.002 | within noise |
| conv-conv-stride2 / single-example layer_hidden_delta | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -4.4% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-conv-stride2 / single-example layer_output_delta | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -3.1% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-conv-stride2 / single-example argmax | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | +0.1% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-conv-stride2 / single-example Array.copy | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | +1.4% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-conv-stride2 / single-example default_rng | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | +6.2% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | separated, inside spread |
| conv-conv-stride2 / mini-batch (32) (profiled total) | 0.469 (0.465-0.475) | 0.467 (0.463-0.473) | -0.4% | 0.467, 0.470, 0.467 / 0.464, 0.471, 0.468 | within noise |
| conv-conv-stride2 / mini-batch (32) conv_forward_batch | 0.285 (0.284-0.288) | 0.285 (0.284-0.286) | -0.0% | 0.285, 0.285, 0.284 / 0.284, 0.285, 0.285 | within noise |
| conv-conv-stride2 / mini-batch (32) conv_accumulate_gradient_batch | 0.054 (0.053-0.056) | 0.054 (0.053-0.054) | -0.1% | 0.054, 0.054, 0.053 / 0.053, 0.054, 0.054 | within noise |
| conv-conv-stride2 / mini-batch (32) conv_downstream_batch | 0.039 (0.039-0.040) | 0.039 (0.039-0.040) | -0.5% | 0.039, 0.040, 0.039 / 0.039, 0.040, 0.039 | within noise |
| conv-conv-stride2 / mini-batch (32) layer_forward | 0.022 (0.021-0.024) | 0.022 (0.021-0.024) | -1.5% | 0.022, 0.022, 0.022 / 0.021, 0.024, 0.022 | within noise |
| conv-conv-stride2 / mini-batch (32) array_relu_mask | 0.007 (0.007-0.007) | 0.007 (0.007-0.007) | -0.3% | 0.007, 0.007, 0.007 / 0.007, 0.007, 0.007 | within noise |
| conv-conv-stride2 / mini-batch (32) layer_forward_batch | 0.005 (0.005-0.005) | 0.005 (0.005-0.005) | -0.8% | 0.005, 0.005, 0.005 / 0.005, 0.005, 0.005 | within noise |
| conv-conv-stride2 / mini-batch (32) layer_accumulate_gradient_batch | 0.005 (0.005-0.005) | 0.005 (0.005-0.005) | +0.4% | 0.005, 0.005, 0.005 / 0.005, 0.005, 0.005 | within noise |
| conv-conv-stride2 / mini-batch (32) layer_downstream_batch | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | +0.4% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | within noise |
| conv-conv-stride2 / mini-batch (32) Array.row | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | +1.6% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | within noise |
| conv-conv-stride2 / mini-batch (32) layer_apply_accumulated_gradient | 0.002 (0.002-0.002) | 0.002 (0.002-0.002) | -0.7% | 0.002, 0.002, 0.002 / 0.002, 0.002, 0.002 | within noise |
| conv-conv-stride2 / mini-batch (32) Array.take_rows | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -1.2% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-conv-stride2 / mini-batch (32) argmax | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | +5.9% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-conv-stride2 / mini-batch (32) layer_hidden_delta_batch | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -0.6% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-conv-stride2 / mini-batch (32) Array.copy | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -3.2% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-conv-stride2 / mini-batch (32) layer_output_delta | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -5.2% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-conv-stride2 / mini-batch (32) default_rng | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | +0.6% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-conv / single-example (profiled total) | 1.333 (1.310-1.359) | 1.314 (1.310-1.352) | -1.4% | 1.333, 1.330, 1.354 / 1.312, 1.339, 1.314 | within noise |
| conv-conv / single-example conv_forward_batch | 0.718 (0.713-0.721) | 0.718 (0.716-0.720) | -0.1% | 0.718, 0.715, 0.718 / 0.716, 0.719, 0.717 | within noise |
| conv-conv / single-example layer_forward | 0.127 (0.117-0.136) | 0.118 (0.118-0.136) | -6.8% | 0.127, 0.124, 0.136 / 0.118, 0.127, 0.118 | within noise |
| conv-conv / single-example conv_downstream_batch | 0.116 (0.113-0.119) | 0.114 (0.113-0.117) | -1.5% | 0.115, 0.118, 0.118 / 0.113, 0.116, 0.114 | within noise |
| conv-conv / single-example layer_sgd_step | 0.102 (0.100-0.105) | 0.100 (0.099-0.104) | -2.5% | 0.102, 0.103, 0.104 / 0.100, 0.102, 0.099 | within noise |
| conv-conv / single-example conv_accumulate_gradient_batch | 0.085 (0.084-0.087) | 0.084 (0.084-0.087) | -1.2% | 0.085, 0.085, 0.086 / 0.084, 0.085, 0.084 | within noise |
| conv-conv / single-example layer_downstream | 0.048 (0.045-0.052) | 0.045 (0.045-0.051) | -5.5% | 0.048, 0.047, 0.051 / 0.045, 0.049, 0.045 | within noise |
| conv-conv / single-example array_relu_mask | 0.009 (0.008-0.009) | 0.008 (0.008-0.009) | -4.4% | 0.008, 0.009, 0.009 / 0.008, 0.009, 0.008 | within noise |
| conv-conv / single-example Array.row | 0.005 (0.005-0.005) | 0.005 (0.005-0.005) | -1.6% | 0.005, 0.005, 0.005 / 0.005, 0.005, 0.005 | within noise |
| conv-conv / single-example layer_apply_accumulated_gradient | 0.002 (0.002-0.003) | 0.002 (0.002-0.002) | -0.0% | 0.002, 0.002, 0.002 / 0.002, 0.002, 0.002 | within noise |
| conv-conv / single-example layer_hidden_delta | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -2.7% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-conv / single-example argmax | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | +6.8% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-conv / single-example layer_output_delta | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -3.2% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-conv / single-example Array.copy | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -0.8% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-conv / single-example default_rng | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | +1.5% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-conv / mini-batch (32) (profiled total) | 1.302 (1.298-1.316) | 1.298 (1.294-1.304) | -0.3% | 1.300, 1.302, 1.302 / 1.298, 1.298, 1.296 | consistent |
| conv-conv / mini-batch (32) conv_forward_batch | 0.770 (0.769-0.772) | 0.769 (0.767-0.772) | -0.2% | 0.770, 0.771, 0.770 / 0.769, 0.770, 0.768 | separated, inside spread |
| conv-conv / mini-batch (32) conv_downstream_batch | 0.183 (0.181-0.184) | 0.182 (0.180-0.184) | -0.5% | 0.184, 0.183, 0.181 / 0.181, 0.183, 0.181 | within noise |
| conv-conv / mini-batch (32) conv_accumulate_gradient_batch | 0.099 (0.099-0.100) | 0.099 (0.098-0.100) | -0.2% | 0.099, 0.099, 0.099 / 0.099, 0.099, 0.099 | within noise |
| conv-conv / mini-batch (32) layer_forward | 0.083 (0.077-0.089) | 0.078 (0.077-0.086) | -6.3% | 0.081, 0.080, 0.083 / 0.078, 0.078, 0.077 | separated, inside spread |
| conv-conv / mini-batch (32) layer_accumulate_gradient_batch | 0.028 (0.028-0.029) | 0.029 (0.028-0.029) | +0.6% | 0.028, 0.029, 0.028 / 0.028, 0.029, 0.029 | within noise |
| conv-conv / mini-batch (32) layer_forward_batch | 0.025 (0.025-0.026) | 0.025 (0.025-0.026) | +0.0% | 0.025, 0.025, 0.026 / 0.025, 0.026, 0.025 | within noise |
| conv-conv / mini-batch (32) layer_downstream_batch | 0.021 (0.020-0.021) | 0.021 (0.020-0.021) | +0.0% | 0.021, 0.021, 0.021 / 0.021, 0.021, 0.021 | within noise |
| conv-conv / mini-batch (32) array_relu_mask | 0.016 (0.016-0.017) | 0.016 (0.016-0.017) | -0.5% | 0.017, 0.017, 0.016 / 0.016, 0.017, 0.016 | within noise |
| conv-conv / mini-batch (32) layer_apply_accumulated_gradient | 0.008 (0.007-0.008) | 0.008 (0.007-0.008) | +0.5% | 0.008, 0.008, 0.008 / 0.008, 0.008, 0.008 | within noise |
| conv-conv / mini-batch (32) Array.row | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | +0.8% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | within noise |
| conv-conv / mini-batch (32) Array.take_rows | 0.002 (0.002-0.002) | 0.002 (0.002-0.002) | -0.7% | 0.002, 0.002, 0.002 / 0.002, 0.002, 0.002 | within noise |
| conv-conv / mini-batch (32) Array.copy | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | +0.0% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-conv / mini-batch (32) argmax | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -6.4% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-conv / mini-batch (32) layer_hidden_delta_batch | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -2.8% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-conv / mini-batch (32) layer_output_delta | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -0.0% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-conv / mini-batch (32) default_rng | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | +0.6% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-conv16 / single-example (profiled total) | 1.695 (1.649-1.706) | 1.651 (1.634-1.738) | -2.6% | 1.664, 1.695, 1.695 / 1.645, 1.738, 1.635 | within noise |
| conv-conv16 / single-example conv_forward_batch | 0.691 (0.677-0.692) | 0.677 (0.672-0.692) | -2.0% | 0.691, 0.688, 0.691 / 0.674, 0.691, 0.674 | within noise |
| conv-conv16 / single-example layer_forward | 0.241 (0.224-0.249) | 0.222 (0.220-0.265) | -8.0% | 0.225, 0.242, 0.241 / 0.221, 0.265, 0.220 | within noise |
| conv-conv16 / single-example layer_sgd_step | 0.225 (0.220-0.229) | 0.221 (0.219-0.235) | -1.9% | 0.221, 0.228, 0.225 / 0.221, 0.233, 0.220 | within noise |
| conv-conv16 / single-example conv_downstream_batch | 0.161 (0.159-0.163) | 0.159 (0.158-0.164) | -1.2% | 0.161, 0.161, 0.161 / 0.158, 0.163, 0.159 | within noise |
| conv-conv16 / single-example conv_accumulate_gradient_batch | 0.127 (0.126-0.129) | 0.126 (0.126-0.129) | -0.8% | 0.126, 0.128, 0.127 / 0.126, 0.129, 0.126 | within noise |
| conv-conv16 / single-example layer_downstream | 0.095 (0.090-0.096) | 0.090 (0.088-0.101) | -5.7% | 0.091, 0.095, 0.095 / 0.089, 0.101, 0.089 | within noise |
| conv-conv16 / single-example array_relu_mask | 0.012 (0.012-0.012) | 0.012 (0.012-0.013) | -3.1% | 0.012, 0.012, 0.012 / 0.012, 0.013, 0.012 | within noise |
| conv-conv16 / single-example Array.row | 0.005 (0.005-0.005) | 0.005 (0.005-0.005) | -0.9% | 0.005, 0.005, 0.005 / 0.005, 0.005, 0.005 | within noise |
| conv-conv16 / single-example layer_apply_accumulated_gradient | 0.003 (0.003-0.004) | 0.003 (0.003-0.003) | -1.1% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | within noise |
| conv-conv16 / single-example layer_hidden_delta | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -0.6% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-conv16 / single-example Array.copy | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -11.7% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-conv16 / single-example argmax | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | +1.7% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-conv16 / single-example layer_output_delta | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | +3.2% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-conv16 / single-example default_rng | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | +1.0% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-conv16 / mini-batch (32) (profiled total) | 1.379 (1.361-1.392) | 1.368 (1.358-1.386) | -0.8% | 1.373, 1.387, 1.376 / 1.368, 1.381, 1.358 | within noise |
| conv-conv16 / mini-batch (32) conv_forward_batch | 0.713 (0.697-0.715) | 0.714 (0.699-0.718) | +0.1% | 0.715, 0.714, 0.703 / 0.714, 0.715, 0.701 | within noise |
| conv-conv16 / mini-batch (32) conv_downstream_batch | 0.192 (0.190-0.193) | 0.192 (0.191-0.194) | -0.0% | 0.193, 0.191, 0.192 / 0.192, 0.192, 0.193 | within noise |
| conv-conv16 / mini-batch (32) layer_forward | 0.166 (0.151-0.177) | 0.157 (0.151-0.166) | -5.0% | 0.157, 0.166, 0.166 / 0.162, 0.157, 0.157 | within noise |
| conv-conv16 / mini-batch (32) conv_accumulate_gradient_batch | 0.119 (0.118-0.120) | 0.119 (0.118-0.120) | +0.2% | 0.119, 0.118, 0.119 / 0.119, 0.119, 0.119 | within noise |
| conv-conv16 / mini-batch (32) layer_accumulate_gradient_batch | 0.029 (0.029-0.030) | 0.029 (0.029-0.030) | -0.9% | 0.029, 0.029, 0.029 / 0.029, 0.029, 0.029 | within noise |
| conv-conv16 / mini-batch (32) layer_forward_batch | 0.027 (0.027-0.028) | 0.027 (0.026-0.028) | -0.3% | 0.027, 0.027, 0.027 / 0.027, 0.027, 0.027 | within noise |
| conv-conv16 / mini-batch (32) layer_downstream_batch | 0.025 (0.025-0.026) | 0.025 (0.024-0.027) | +0.4% | 0.025, 0.025, 0.025 / 0.025, 0.025, 0.025 | within noise |
| conv-conv16 / mini-batch (32) array_relu_mask | 0.024 (0.024-0.025) | 0.024 (0.024-0.024) | -0.1% | 0.024, 0.024, 0.024 / 0.024, 0.024, 0.024 | within noise |
| conv-conv16 / mini-batch (32) layer_apply_accumulated_gradient | 0.017 (0.017-0.017) | 0.017 (0.017-0.017) | +0.0% | 0.017, 0.017, 0.017 / 0.017, 0.017, 0.017 | within noise |
| conv-conv16 / mini-batch (32) Array.row | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | -0.5% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | within noise |
| conv-conv16 / mini-batch (32) Array.take_rows | 0.002 (0.002-0.002) | 0.002 (0.002-0.002) | -4.2% | 0.002, 0.002, 0.002 / 0.002, 0.002, 0.002 | separated, inside spread |
| conv-conv16 / mini-batch (32) Array.copy | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -5.0% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-conv16 / mini-batch (32) argmax | 0.001 (0.001-0.001) | 0.001 (0.001-0.001) | -1.0% | 0.001, 0.001, 0.001 / 0.001, 0.001, 0.001 | within noise |
| conv-conv16 / mini-batch (32) layer_hidden_delta_batch | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -0.9% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | within noise |
| conv-conv16 / mini-batch (32) layer_output_delta | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -23.7% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | separated, inside spread |
| conv-conv16 / mini-batch (32) default_rng | 0.000 (0.000-0.000) | 0.000 (0.000-0.000) | -3.8% | 0.000, 0.000, 0.000 / 0.000, 0.000, 0.000 | separated, inside spread |
