Old `4176d10` against new `4176d10`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py epochs --backdrop prepared --threads 1 2 4 --repeats 1 -- --configs conv B=32 conv B=512 dense B=32 dense B=512` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `17d1c27f71b0`) on both sides. Machine check: profile: identity matches (raspberry-pi-5.json); passes peaked at 48.0-49.0 C; max 1-min load 1.99 (HIGH); busy processes: none. Each row pools 1 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: none (a probe row can carry "control": true)
- 37 rows within noise, max |Δ| 31.0%
- spread of per-pass medians over 37 rows: median 3.6%, 90th percentile 9.9%, max 26.9%
- pass shifts (median over rows of pass median / pooled median): 1 -0.1%, 2 +0.1%

### epoch

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x 1 thread, conv B=32 / rust | 1.188 (1.152-1.223) | 1.152, 1.223 | 6.0% |
| 1 x 1 thread, conv B=512 / rust | 1.183 (1.182-1.184) | 1.184, 1.182 | 0.1% |
| 1 x 1 thread, dense B=32 / rust | 1.738 (1.730-1.747) | 1.730, 1.747 | 0.9% |
| 1 x 1 thread, dense B=512 / rust | 1.992 (1.948-2.035) | 1.948, 2.035 | 4.4% |
| 1 x 2 threads, conv B=32 / rust | 1.167 (1.151-1.182) | 1.151, 1.182 | 2.6% |
| 1 x 2 threads, conv B=512 / rust | 1.134 (1.103-1.164) | 1.164, 1.103 | 5.4% |
| 1 x 2 threads, dense B=32 / rust | 1.773 (1.756-1.790) | 1.790, 1.756 | 1.9% |
| 1 x 2 threads, dense B=512 / rust | 1.825 (1.769-1.881) | 1.881, 1.769 | 6.1% |
| 1 x 4 threads, conv B=32 / rust | 1.176 (1.130-1.222) | 1.222, 1.130 | 7.8% |
| 1 x 4 threads, conv B=512 / rust | 1.071 (1.070-1.072) | 1.072, 1.070 | 0.1% |
| 1 x 4 threads, dense B=32 / rust | 1.864 (1.781-1.947) | 1.781, 1.947 | 8.9% |
| 1 x 4 threads, dense B=512 / rust | 1.974 (1.709-2.239) | 1.709, 2.239 | 26.9% |

### prepare

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x 1 thread, conv B=32 / rust | 0.014 (0.013-0.014) | 0.013, 0.014 | 1.2% |
| 1 x 1 thread, conv B=512 / rust | 0.016 (0.015-0.017) | 0.015, 0.017 | 9.6% |
| 1 x 1 thread, dense B=32 / rust | 0.449 (0.445-0.454) | 0.454, 0.445 | 2.0% |
| 1 x 1 thread, dense B=512 / rust | 0.451 (0.425-0.476) | 0.425, 0.476 | 11.3% |
| 1 x 2 threads, conv B=32 / rust | 0.014 (0.014-0.015) | 0.015, 0.014 | 8.3% |
| 1 x 2 threads, conv B=512 / rust | 0.016 (0.014-0.018) | 0.018, 0.014 | 23.1% |
| 1 x 2 threads, dense B=32 / rust | 0.439 (0.426-0.452) | 0.452, 0.426 | 5.9% |
| 1 x 2 threads, dense B=512 / rust | 0.437 (0.433-0.440) | 0.433, 0.440 | 1.5% |
| 1 x 4 threads, conv B=32 / rust | 0.015 (0.014-0.015) | 0.014, 0.015 | 6.1% |
| 1 x 4 threads, conv B=512 / rust | 0.013 (0.013-0.014) | 0.013, 0.014 | 9.9% |
| 1 x 4 threads, dense B=32 / rust | 0.450 (0.430-0.470) | 0.470, 0.430 | 8.9% |
| 1 x 4 threads, dense B=512 / rust | 0.474 (0.473-0.474) | 0.474, 0.473 | 0.0% |

### epoch, loader

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x 1 thread, conv B=32 / rust | 1.179 (1.167-1.191) | 1.191, 1.167 | 2.0% |
| 1 x 1 thread, conv B=512 / rust | 1.146 (1.143-1.148) | 1.148, 1.143 | 0.4% |
| 1 x 1 thread, dense B=32 / rust | 1.305 (1.304-1.306) | 1.304, 1.306 | 0.2% |
| 1 x 1 thread, dense B=512 / rust | 1.477 (1.449-1.504) | 1.449, 1.504 | 3.7% |
| 1 x 2 threads, conv B=32 / rust | 1.158 (1.129-1.186) | 1.129, 1.186 | 4.8% |
| 1 x 2 threads, conv B=512 / rust | 1.066 (1.065-1.067) | 1.067, 1.065 | 0.2% |
| 1 x 2 threads, dense B=32 / rust | 1.310 (1.309-1.311) | 1.311, 1.309 | 0.1% |
| 1 x 2 threads, dense B=512 / rust | 1.307 (1.284-1.330) | 1.284, 1.330 | 3.6% |
| 1 x 4 threads, conv B=32 / rust | 1.116 (1.113-1.118) | 1.113, 1.118 | 0.5% |
| 1 x 4 threads, conv B=512 / rust | 1.061 (1.057-1.065) | 1.057, 1.065 | 0.7% |
| 1 x 4 threads, dense B=32 / rust | 1.308 (1.307-1.309) | 1.307, 1.309 | 0.2% |
| 1 x 4 threads, dense B=512 / rust | 1.271 (1.241-1.300) | 1.241, 1.300 | 4.6% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 46.58 (46.3-46.85) | 46.85, 46.3 | 1.2% |
