Old `f081ecf` against new `f081ecf`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py epochs --backdrop prepared --threads 0 1 2 4 8 --repeats 1 -- --configs conv B=32 conv B=512 dense B=32 dense B=512` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `7a3f0df0ecd3`) on both sides. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 2.56 (HIGH); busy processes: none. Each row pools 1 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: none (a probe row can carry "control": true)
- 61 rows within noise, max |Δ| 11.5%
- spread of per-pass medians over 61 rows: median 0.4%, 90th percentile 3.7%, max 10.9%
- pass shifts (median over rows of pass median / pooled median): 1 +0.0%, 2 +0.0%

### epoch

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x default threads, conv B=32 / rust | 0.319 (0.311-0.328) | 0.311, 0.328 | 5.3% |
| 1 x default threads, conv B=512 / rust | 0.356 (0.349-0.364) | 0.349, 0.364 | 4.1% |
| 1 x default threads, dense B=32 / rust | 0.710 (0.709-0.711) | 0.711, 0.709 | 0.4% |
| 1 x default threads, dense B=512 / rust | 0.608 (0.606-0.609) | 0.606, 0.609 | 0.4% |
| 1 x 1 thread, conv B=32 / rust | 0.306 (0.305-0.306) | 0.305, 0.306 | 0.1% |
| 1 x 1 thread, conv B=512 / rust | 0.369 (0.368-0.370) | 0.370, 0.368 | 0.6% |
| 1 x 1 thread, dense B=32 / rust | 0.711 (0.708-0.713) | 0.708, 0.713 | 0.7% |
| 1 x 1 thread, dense B=512 / rust | 0.658 (0.656-0.660) | 0.656, 0.660 | 0.6% |
| 1 x 2 threads, conv B=32 / rust | 0.305 (0.305-0.306) | 0.305, 0.306 | 0.5% |
| 1 x 2 threads, conv B=512 / rust | 0.354 (0.353-0.355) | 0.353, 0.355 | 0.5% |
| 1 x 2 threads, dense B=32 / rust | 0.709 (0.708-0.709) | 0.709, 0.708 | 0.1% |
| 1 x 2 threads, dense B=512 / rust | 0.648 (0.647-0.648) | 0.647, 0.648 | 0.2% |
| 1 x 4 threads, conv B=32 / rust | 0.306 (0.305-0.308) | 0.305, 0.308 | 1.0% |
| 1 x 4 threads, conv B=512 / rust | 0.344 (0.344-0.345) | 0.344, 0.345 | 0.1% |
| 1 x 4 threads, dense B=32 / rust | 0.711 (0.710-0.712) | 0.712, 0.710 | 0.2% |
| 1 x 4 threads, dense B=512 / rust | 0.623 (0.622-0.623) | 0.623, 0.622 | 0.1% |
| 1 x 8 threads, conv B=32 / rust | 0.305 (0.305-0.305) | 0.305, 0.305 | 0.1% |
| 1 x 8 threads, conv B=512 / rust | 0.350 (0.347-0.353) | 0.347, 0.353 | 1.8% |
| 1 x 8 threads, dense B=32 / rust | 0.715 (0.713-0.717) | 0.717, 0.713 | 0.6% |
| 1 x 8 threads, dense B=512 / rust | 0.613 (0.613-0.613) | 0.613, 0.613 | 0.0% |

### prepare

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x default threads, conv B=32 / rust | 0.006 (0.006-0.006) | 0.006, 0.006 | 2.6% |
| 1 x default threads, conv B=512 / rust | 0.007 (0.007-0.007) | 0.007, 0.007 | 3.1% |
| 1 x default threads, dense B=32 / rust | 0.208 (0.207-0.209) | 0.209, 0.207 | 1.2% |
| 1 x default threads, dense B=512 / rust | 0.209 (0.209-0.209) | 0.209, 0.209 | 0.3% |
| 1 x 1 thread, conv B=32 / rust | 0.006 (0.006-0.006) | 0.006, 0.006 | 3.7% |
| 1 x 1 thread, conv B=512 / rust | 0.007 (0.007-0.007) | 0.007, 0.007 | 10.9% |
| 1 x 1 thread, dense B=32 / rust | 0.208 (0.207-0.210) | 0.207, 0.210 | 1.4% |
| 1 x 1 thread, dense B=512 / rust | 0.208 (0.207-0.208) | 0.207, 0.208 | 0.6% |
| 1 x 2 threads, conv B=32 / rust | 0.006 (0.006-0.006) | 0.006, 0.006 | 5.1% |
| 1 x 2 threads, conv B=512 / rust | 0.007 (0.007-0.007) | 0.007, 0.007 | 0.9% |
| 1 x 2 threads, dense B=32 / rust | 0.207 (0.207-0.207) | 0.207, 0.207 | 0.0% |
| 1 x 2 threads, dense B=512 / rust | 0.207 (0.207-0.207) | 0.207, 0.207 | 0.1% |
| 1 x 4 threads, conv B=32 / rust | 0.006 (0.006-0.006) | 0.006, 0.006 | 1.0% |
| 1 x 4 threads, conv B=512 / rust | 0.007 (0.007-0.007) | 0.007, 0.007 | 0.1% |
| 1 x 4 threads, dense B=32 / rust | 0.207 (0.206-0.208) | 0.208, 0.206 | 0.6% |
| 1 x 4 threads, dense B=512 / rust | 0.207 (0.206-0.208) | 0.206, 0.208 | 0.8% |
| 1 x 8 threads, conv B=32 / rust | 0.006 (0.006-0.006) | 0.006, 0.006 | 0.1% |
| 1 x 8 threads, conv B=512 / rust | 0.007 (0.007-0.007) | 0.007, 0.007 | 4.2% |
| 1 x 8 threads, dense B=32 / rust | 0.207 (0.207-0.207) | 0.207, 0.207 | 0.2% |
| 1 x 8 threads, dense B=512 / rust | 0.210 (0.210-0.210) | 0.210, 0.210 | 0.4% |

### epoch, loader

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x default threads, conv B=32 / rust | 0.304 (0.295-0.313) | 0.295, 0.313 | 5.8% |
| 1 x default threads, conv B=512 / rust | 0.328 (0.328-0.329) | 0.329, 0.328 | 0.4% |
| 1 x default threads, dense B=32 / rust | 0.494 (0.491-0.498) | 0.498, 0.491 | 1.3% |
| 1 x default threads, dense B=512 / rust | 0.399 (0.397-0.401) | 0.401, 0.397 | 0.9% |
| 1 x 1 thread, conv B=32 / rust | 0.296 (0.296-0.297) | 0.296, 0.297 | 0.2% |
| 1 x 1 thread, conv B=512 / rust | 0.335 (0.335-0.335) | 0.335, 0.335 | 0.2% |
| 1 x 1 thread, dense B=32 / rust | 0.492 (0.492-0.492) | 0.492, 0.492 | 0.0% |
| 1 x 1 thread, dense B=512 / rust | 0.440 (0.439-0.440) | 0.439, 0.440 | 0.4% |
| 1 x 2 threads, conv B=32 / rust | 0.296 (0.295-0.296) | 0.296, 0.295 | 0.4% |
| 1 x 2 threads, conv B=512 / rust | 0.323 (0.322-0.325) | 0.325, 0.322 | 0.7% |
| 1 x 2 threads, dense B=32 / rust | 0.492 (0.492-0.493) | 0.493, 0.492 | 0.2% |
| 1 x 2 threads, dense B=512 / rust | 0.435 (0.435-0.436) | 0.435, 0.436 | 0.0% |
| 1 x 4 threads, conv B=32 / rust | 0.295 (0.295-0.296) | 0.296, 0.295 | 0.1% |
| 1 x 4 threads, conv B=512 / rust | 0.315 (0.315-0.316) | 0.316, 0.315 | 0.3% |
| 1 x 4 threads, dense B=32 / rust | 0.493 (0.493-0.493) | 0.493, 0.493 | 0.1% |
| 1 x 4 threads, dense B=512 / rust | 0.414 (0.413-0.414) | 0.414, 0.413 | 0.2% |
| 1 x 8 threads, conv B=32 / rust | 0.295 (0.295-0.295) | 0.295, 0.295 | 0.1% |
| 1 x 8 threads, conv B=512 / rust | 0.318 (0.318-0.318) | 0.318, 0.318 | 0.1% |
| 1 x 8 threads, dense B=32 / rust | 0.499 (0.496-0.502) | 0.502, 0.496 | 1.3% |
| 1 x 8 threads, dense B=512 / rust | 0.404 (0.403-0.404) | 0.404, 0.403 | 0.1% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 27.8 (27.8-27.8) | 27.8, 27.8 | 0.0% |
