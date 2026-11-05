Old `239db3a` against new `239db3a`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py epochs --threads 0 --openblas 1 0 --repeats 2 --backdrop prepared -- --configs conv B=32 conv B=512 dense B=512` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `d6ff3e4` (extension sha256 `7194f34f6ce9`) and new crate `d6ff3e4` (extension sha256 `7194f34f6ce9`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity changed (allowed) (ryzen7-3700u-klip.json); max 1-min load 0.73; busy processes: none. Each row pools 2 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: none (a probe row can carry "control": true)
- 19 rows within noise, max |Δ| 6.4%
- spread of per-pass medians over 19 rows: median 0.4%, 90th percentile 3.5%, max 6.4%
- pass shifts (median over rows of pass median / pooled median): 1 -0.0%, 2 +0.1%

### epoch

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x default threads, OpenBLAS 1, conv B=32 / rust | 0.761 (0.752-0.856) | 0.758, 0.807 | 6.4% |
| 1 x default threads, OpenBLAS 1, conv B=512 / rust | 0.808 (0.797-0.810) | 0.810, 0.802 | 1.0% |
| 1 x default threads, OpenBLAS 1, dense B=512 / rust | 1.686 (1.685-1.689) | 1.686, 1.687 | 0.1% |
| 1 x default threads, OpenBLAS default, conv B=32 / rust | 0.770 (0.764-0.773) | 0.771, 0.768 | 0.4% |
| 1 x default threads, OpenBLAS default, conv B=512 / rust | 0.810 (0.798-0.812) | 0.810, 0.805 | 0.6% |
| 1 x default threads, OpenBLAS default, dense B=512 / rust | 1.689 (1.686-1.691) | 1.687, 1.691 | 0.2% |

### prepare

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x default threads, OpenBLAS 1, conv B=32 / rust | 0.017 (0.017-0.017) | 0.017, 0.017 | 0.4% |
| 1 x default threads, OpenBLAS 1, conv B=512 / rust | 0.019 (0.019-0.019) | 0.019, 0.019 | 1.7% |
| 1 x default threads, OpenBLAS 1, dense B=512 / rust | 0.620 (0.619-0.621) | 0.619, 0.620 | 0.1% |
| 1 x default threads, OpenBLAS default, conv B=32 / rust | 0.017 (0.017-0.017) | 0.017, 0.017 | 0.2% |
| 1 x default threads, OpenBLAS default, conv B=512 / rust | 0.019 (0.019-0.019) | 0.019, 0.019 | 0.1% |
| 1 x default threads, OpenBLAS default, dense B=512 / rust | 0.620 (0.619-0.623) | 0.620, 0.621 | 0.1% |

### epoch, loader

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x default threads, OpenBLAS 1, conv B=32 / rust | 0.735 (0.730-0.783) | 0.734, 0.758 | 3.3% |
| 1 x default threads, OpenBLAS 1, conv B=512 / rust | 0.700 (0.698-0.706) | 0.700, 0.702 | 0.3% |
| 1 x default threads, OpenBLAS 1, dense B=512 / rust | 1.058 (1.057-1.073) | 1.057, 1.065 | 0.8% |
| 1 x default threads, OpenBLAS default, conv B=32 / rust | 0.745 (0.736-0.746) | 0.741, 0.745 | 0.6% |
| 1 x default threads, OpenBLAS default, conv B=512 / rust | 0.733 (0.701-0.743) | 0.740, 0.715 | 3.5% |
| 1 x default threads, OpenBLAS default, dense B=512 / rust | 1.059 (1.058-1.065) | 1.059, 1.062 | 0.4% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 38.5 (38-39) | 38, 39 | 2.6% |
