Old `f081ecf` against new `f081ecf`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py epochs --backdrop prepared --threads 0 1 2 4 8 --repeats 1 -- --configs conv B=32 conv B=512 dense B=32 dense B=512` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `362e34c` (extension sha256 `7a3f0df0ecd3`) and new crate `362e34c` (extension sha256 `7a3f0df0ecd3`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-1255u.json); max 1-min load 6.28 (HIGH); busy processes: none. Each row pools 1 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: none (a probe row can carry "control": true)
- 61 rows within noise, max |Δ| 7.9%
- spread of per-pass medians over 61 rows: median 1.3%, 90th percentile 4.1%, max 7.6%
- pass shifts (median over rows of pass median / pooled median): 1 -0.3%, 2 +0.3%

### epoch

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x default threads, conv B=32 / rust | 0.262 (0.260-0.264) | 0.264, 0.260 | 1.3% |
| 1 x default threads, conv B=512 / rust | 0.304 (0.302-0.306) | 0.302, 0.306 | 1.3% |
| 1 x default threads, dense B=32 / rust | 0.621 (0.615-0.628) | 0.615, 0.628 | 2.1% |
| 1 x default threads, dense B=512 / rust | 0.574 (0.574-0.575) | 0.574, 0.575 | 0.1% |
| 1 x 1 thread, conv B=32 / rust | 0.275 (0.275-0.276) | 0.276, 0.275 | 0.2% |
| 1 x 1 thread, conv B=512 / rust | 0.333 (0.331-0.334) | 0.334, 0.331 | 1.1% |
| 1 x 1 thread, dense B=32 / rust | 0.616 (0.608-0.625) | 0.608, 0.625 | 2.8% |
| 1 x 1 thread, dense B=512 / rust | 0.603 (0.580-0.626) | 0.580, 0.626 | 7.6% |
| 1 x 2 threads, conv B=32 / rust | 0.273 (0.270-0.277) | 0.270, 0.277 | 2.3% |
| 1 x 2 threads, conv B=512 / rust | 0.330 (0.326-0.333) | 0.326, 0.333 | 2.3% |
| 1 x 2 threads, dense B=32 / rust | 0.624 (0.623-0.626) | 0.623, 0.626 | 0.5% |
| 1 x 2 threads, dense B=512 / rust | 0.659 (0.654-0.664) | 0.654, 0.664 | 1.5% |
| 1 x 4 threads, conv B=32 / rust | 0.266 (0.259-0.273) | 0.259, 0.273 | 5.3% |
| 1 x 4 threads, conv B=512 / rust | 0.308 (0.306-0.310) | 0.306, 0.310 | 1.2% |
| 1 x 4 threads, dense B=32 / rust | 0.623 (0.621-0.624) | 0.621, 0.624 | 0.5% |
| 1 x 4 threads, dense B=512 / rust | 0.596 (0.591-0.601) | 0.591, 0.601 | 1.7% |
| 1 x 8 threads, conv B=32 / rust | 0.267 (0.262-0.271) | 0.262, 0.271 | 3.4% |
| 1 x 8 threads, conv B=512 / rust | 0.308 (0.307-0.309) | 0.307, 0.309 | 0.8% |
| 1 x 8 threads, dense B=32 / rust | 0.650 (0.626-0.674) | 0.674, 0.626 | 7.4% |
| 1 x 8 threads, dense B=512 / rust | 0.574 (0.572-0.575) | 0.575, 0.572 | 0.4% |

### prepare

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x default threads, conv B=32 / rust | 0.006 (0.006-0.006) | 0.006, 0.006 | 0.1% |
| 1 x default threads, conv B=512 / rust | 0.006 (0.006-0.006) | 0.006, 0.006 | 1.1% |
| 1 x default threads, dense B=32 / rust | 0.199 (0.198-0.200) | 0.198, 0.200 | 0.9% |
| 1 x default threads, dense B=512 / rust | 0.201 (0.199-0.203) | 0.199, 0.203 | 2.0% |
| 1 x 1 thread, conv B=32 / rust | 0.005 (0.005-0.006) | 0.005, 0.006 | 4.1% |
| 1 x 1 thread, conv B=512 / rust | 0.006 (0.006-0.006) | 0.006, 0.006 | 6.8% |
| 1 x 1 thread, dense B=32 / rust | 0.203 (0.200-0.206) | 0.206, 0.200 | 2.8% |
| 1 x 1 thread, dense B=512 / rust | 0.198 (0.196-0.199) | 0.199, 0.196 | 1.3% |
| 1 x 2 threads, conv B=32 / rust | 0.006 (0.006-0.006) | 0.006, 0.006 | 0.6% |
| 1 x 2 threads, conv B=512 / rust | 0.006 (0.006-0.006) | 0.006, 0.006 | 0.6% |
| 1 x 2 threads, dense B=32 / rust | 0.199 (0.199-0.200) | 0.199, 0.200 | 0.3% |
| 1 x 2 threads, dense B=512 / rust | 0.205 (0.202-0.207) | 0.202, 0.207 | 2.1% |
| 1 x 4 threads, conv B=32 / rust | 0.006 (0.005-0.006) | 0.006, 0.005 | 3.1% |
| 1 x 4 threads, conv B=512 / rust | 0.006 (0.006-0.006) | 0.006, 0.006 | 2.5% |
| 1 x 4 threads, dense B=32 / rust | 0.202 (0.200-0.204) | 0.200, 0.204 | 2.1% |
| 1 x 4 threads, dense B=512 / rust | 0.199 (0.196-0.202) | 0.196, 0.202 | 2.9% |
| 1 x 8 threads, conv B=32 / rust | 0.006 (0.006-0.006) | 0.006, 0.006 | 1.6% |
| 1 x 8 threads, conv B=512 / rust | 0.006 (0.006-0.006) | 0.006, 0.006 | 0.7% |
| 1 x 8 threads, dense B=32 / rust | 0.201 (0.201-0.201) | 0.201, 0.201 | 0.3% |
| 1 x 8 threads, dense B=512 / rust | 0.203 (0.202-0.203) | 0.203, 0.202 | 0.4% |

### epoch, loader

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x default threads, conv B=32 / rust | 0.257 (0.257-0.258) | 0.258, 0.257 | 0.2% |
| 1 x default threads, conv B=512 / rust | 0.273 (0.270-0.276) | 0.270, 0.276 | 2.1% |
| 1 x default threads, dense B=32 / rust | 0.418 (0.414-0.421) | 0.414, 0.421 | 1.5% |
| 1 x default threads, dense B=512 / rust | 0.382 (0.378-0.386) | 0.386, 0.378 | 2.2% |
| 1 x 1 thread, conv B=32 / rust | 0.268 (0.268-0.268) | 0.268, 0.268 | 0.0% |
| 1 x 1 thread, conv B=512 / rust | 0.299 (0.296-0.301) | 0.301, 0.296 | 1.8% |
| 1 x 1 thread, dense B=32 / rust | 0.412 (0.405-0.419) | 0.405, 0.419 | 3.6% |
| 1 x 1 thread, dense B=512 / rust | 0.378 (0.377-0.379) | 0.377, 0.379 | 0.5% |
| 1 x 2 threads, conv B=32 / rust | 0.265 (0.262-0.269) | 0.262, 0.269 | 2.7% |
| 1 x 2 threads, conv B=512 / rust | 0.296 (0.295-0.296) | 0.295, 0.296 | 0.4% |
| 1 x 2 threads, dense B=32 / rust | 0.420 (0.419-0.421) | 0.419, 0.421 | 0.6% |
| 1 x 2 threads, dense B=512 / rust | 0.442 (0.440-0.444) | 0.440, 0.444 | 1.0% |
| 1 x 4 threads, conv B=32 / rust | 0.259 (0.253-0.265) | 0.253, 0.265 | 4.8% |
| 1 x 4 threads, conv B=512 / rust | 0.277 (0.276-0.278) | 0.276, 0.278 | 0.7% |
| 1 x 4 threads, dense B=32 / rust | 0.416 (0.413-0.418) | 0.418, 0.413 | 1.4% |
| 1 x 4 threads, dense B=512 / rust | 0.402 (0.400-0.404) | 0.404, 0.400 | 1.0% |
| 1 x 8 threads, conv B=32 / rust | 0.266 (0.266-0.266) | 0.266, 0.266 | 0.2% |
| 1 x 8 threads, conv B=512 / rust | 0.274 (0.273-0.274) | 0.274, 0.273 | 0.2% |
| 1 x 8 threads, dense B=32 / rust | 0.441 (0.424-0.457) | 0.457, 0.424 | 7.5% |
| 1 x 8 threads, dense B=512 / rust | 0.367 (0.364-0.369) | 0.364, 0.369 | 1.2% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 20 (20-20) | 20, 20 | 0.0% |
