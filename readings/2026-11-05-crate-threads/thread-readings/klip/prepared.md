Old `f081ecf` against new `f081ecf`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py epochs --backdrop prepared --threads 0 1 2 4 8 --repeats 1 -- --configs conv B=32 conv B=512 dense B=32 dense B=512` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `362e34c` (extension sha256 `7a3f0df0ecd3`) and new crate `362e34c` (extension sha256 `7a3f0df0ecd3`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (ryzen7-3700u-klip.json); max 1-min load 2.54 (HIGH); busy processes: none. Each row pools 1 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: none (a probe row can carry "control": true)
- 61 rows within noise, max |Δ| 6.5%
- spread of per-pass medians over 61 rows: median 0.6%, 90th percentile 2.5%, max 6.3%
- pass shifts (median over rows of pass median / pooled median): 1 -0.0%, 2 +0.0%

### epoch

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x default threads, conv B=32 / rust | 0.758 (0.754-0.762) | 0.754, 0.762 | 1.1% |
| 1 x default threads, conv B=512 / rust | 0.861 (0.860-0.862) | 0.860, 0.862 | 0.2% |
| 1 x default threads, dense B=32 / rust | 1.948 (1.948-1.948) | 1.948, 1.948 | 0.0% |
| 1 x default threads, dense B=512 / rust | 1.803 (1.800-1.807) | 1.800, 1.807 | 0.4% |
| 1 x 1 thread, conv B=32 / rust | 0.755 (0.751-0.759) | 0.759, 0.751 | 1.1% |
| 1 x 1 thread, conv B=512 / rust | 0.932 (0.932-0.932) | 0.932, 0.932 | 0.0% |
| 1 x 1 thread, dense B=32 / rust | 1.947 (1.945-1.948) | 1.948, 1.945 | 0.1% |
| 1 x 1 thread, dense B=512 / rust | 1.899 (1.896-1.901) | 1.896, 1.901 | 0.3% |
| 1 x 2 threads, conv B=32 / rust | 0.760 (0.754-0.766) | 0.754, 0.766 | 1.6% |
| 1 x 2 threads, conv B=512 / rust | 0.896 (0.895-0.898) | 0.895, 0.898 | 0.3% |
| 1 x 2 threads, dense B=32 / rust | 1.933 (1.926-1.940) | 1.940, 1.926 | 0.7% |
| 1 x 2 threads, dense B=512 / rust | 1.978 (1.954-2.001) | 2.001, 1.954 | 2.3% |
| 1 x 4 threads, conv B=32 / rust | 0.755 (0.753-0.758) | 0.758, 0.753 | 0.7% |
| 1 x 4 threads, conv B=512 / rust | 0.861 (0.859-0.862) | 0.859, 0.862 | 0.3% |
| 1 x 4 threads, dense B=32 / rust | 1.940 (1.940-1.941) | 1.941, 1.940 | 0.0% |
| 1 x 4 threads, dense B=512 / rust | 1.769 (1.764-1.774) | 1.764, 1.774 | 0.6% |
| 1 x 8 threads, conv B=32 / rust | 0.754 (0.753-0.754) | 0.754, 0.753 | 0.2% |
| 1 x 8 threads, conv B=512 / rust | 0.861 (0.858-0.864) | 0.864, 0.858 | 0.7% |
| 1 x 8 threads, dense B=32 / rust | 1.945 (1.937-1.954) | 1.937, 1.954 | 0.9% |
| 1 x 8 threads, dense B=512 / rust | 1.807 (1.797-1.818) | 1.797, 1.818 | 1.1% |

### prepare

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x default threads, conv B=32 / rust | 0.016 (0.016-0.016) | 0.016, 0.016 | 3.8% |
| 1 x default threads, conv B=512 / rust | 0.018 (0.018-0.018) | 0.018, 0.018 | 1.0% |
| 1 x default threads, dense B=32 / rust | 0.625 (0.625-0.625) | 0.625, 0.625 | 0.0% |
| 1 x default threads, dense B=512 / rust | 0.608 (0.595-0.622) | 0.595, 0.622 | 4.3% |
| 1 x 1 thread, conv B=32 / rust | 0.017 (0.017-0.017) | 0.017, 0.017 | 0.6% |
| 1 x 1 thread, conv B=512 / rust | 0.019 (0.019-0.019) | 0.019, 0.019 | 1.1% |
| 1 x 1 thread, dense B=32 / rust | 0.623 (0.622-0.624) | 0.624, 0.622 | 0.3% |
| 1 x 1 thread, dense B=512 / rust | 0.624 (0.622-0.625) | 0.622, 0.625 | 0.4% |
| 1 x 2 threads, conv B=32 / rust | 0.017 (0.017-0.017) | 0.017, 0.017 | 0.7% |
| 1 x 2 threads, conv B=512 / rust | 0.018 (0.018-0.018) | 0.018, 0.018 | 2.7% |
| 1 x 2 threads, dense B=32 / rust | 0.625 (0.623-0.627) | 0.627, 0.623 | 0.7% |
| 1 x 2 threads, dense B=512 / rust | 0.623 (0.622-0.624) | 0.624, 0.622 | 0.3% |
| 1 x 4 threads, conv B=32 / rust | 0.017 (0.017-0.017) | 0.017, 0.017 | 0.1% |
| 1 x 4 threads, conv B=512 / rust | 0.018 (0.018-0.018) | 0.018, 0.018 | 0.4% |
| 1 x 4 threads, dense B=32 / rust | 0.638 (0.624-0.652) | 0.624, 0.652 | 4.4% |
| 1 x 4 threads, dense B=512 / rust | 0.624 (0.622-0.626) | 0.626, 0.622 | 0.7% |
| 1 x 8 threads, conv B=32 / rust | 0.017 (0.016-0.017) | 0.016, 0.017 | 2.5% |
| 1 x 8 threads, conv B=512 / rust | 0.018 (0.018-0.018) | 0.018, 0.018 | 2.5% |
| 1 x 8 threads, dense B=32 / rust | 0.623 (0.621-0.626) | 0.621, 0.626 | 0.7% |
| 1 x 8 threads, dense B=512 / rust | 0.622 (0.622-0.623) | 0.622, 0.623 | 0.2% |

### epoch, loader

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x default threads, conv B=32 / rust | 0.734 (0.734-0.735) | 0.735, 0.734 | 0.0% |
| 1 x default threads, conv B=512 / rust | 0.754 (0.752-0.755) | 0.755, 0.752 | 0.5% |
| 1 x default threads, dense B=32 / rust | 1.322 (1.322-1.322) | 1.322, 1.322 | 0.0% |
| 1 x default threads, dense B=512 / rust | 1.160 (1.160-1.161) | 1.161, 1.160 | 0.1% |
| 1 x 1 thread, conv B=32 / rust | 0.738 (0.737-0.738) | 0.737, 0.738 | 0.1% |
| 1 x 1 thread, conv B=512 / rust | 0.804 (0.798-0.811) | 0.798, 0.811 | 1.5% |
| 1 x 1 thread, dense B=32 / rust | 1.322 (1.320-1.323) | 1.320, 1.323 | 0.2% |
| 1 x 1 thread, dense B=512 / rust | 1.273 (1.272-1.275) | 1.272, 1.275 | 0.2% |
| 1 x 2 threads, conv B=32 / rust | 0.733 (0.728-0.737) | 0.728, 0.737 | 1.2% |
| 1 x 2 threads, conv B=512 / rust | 0.767 (0.742-0.791) | 0.742, 0.791 | 6.3% |
| 1 x 2 threads, dense B=32 / rust | 1.317 (1.314-1.320) | 1.320, 1.314 | 0.4% |
| 1 x 2 threads, dense B=512 / rust | 1.343 (1.306-1.379) | 1.379, 1.306 | 5.4% |
| 1 x 4 threads, conv B=32 / rust | 0.731 (0.729-0.734) | 0.734, 0.729 | 0.7% |
| 1 x 4 threads, conv B=512 / rust | 0.751 (0.751-0.751) | 0.751, 0.751 | 0.1% |
| 1 x 4 threads, dense B=32 / rust | 1.315 (1.314-1.316) | 1.316, 1.314 | 0.1% |
| 1 x 4 threads, dense B=512 / rust | 1.154 (1.143-1.165) | 1.143, 1.165 | 1.9% |
| 1 x 8 threads, conv B=32 / rust | 0.733 (0.732-0.733) | 0.733, 0.732 | 0.1% |
| 1 x 8 threads, conv B=512 / rust | 0.755 (0.752-0.758) | 0.752, 0.758 | 0.8% |
| 1 x 8 threads, dense B=32 / rust | 1.320 (1.315-1.325) | 1.315, 1.325 | 0.8% |
| 1 x 8 threads, dense B=512 / rust | 1.158 (1.158-1.159) | 1.159, 1.158 | 0.1% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 47 (47-47) | 47, 47 | 0.0% |
