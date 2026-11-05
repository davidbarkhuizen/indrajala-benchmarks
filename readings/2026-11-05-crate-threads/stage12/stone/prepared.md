Old `239db3a` against new `239db3a`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py epochs --threads 0 --openblas 1 0 --repeats 2 --backdrop prepared -- --configs conv B=32 conv B=512 dense B=512` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `d6ff3e4` (extension sha256 `7194f34f6ce9`) and new crate `d6ff3e4` (extension sha256 `7194f34f6ce9`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-1255u.json); max 1-min load 0.41 (measured just after this run's crate builds); busy processes: none. Each row pools 2 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: none (a probe row can carry "control": true)
- 19 rows within noise, max |Δ| 3.6%
- spread of per-pass medians over 19 rows: median 0.5%, 90th percentile 3.2%, max 3.7%
- pass shifts (median over rows of pass median / pooled median): 1 +0.0%, 2 +0.0%

### epoch

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x default threads, OpenBLAS 1, conv B=32 / rust | 0.261 (0.250-0.270) | 0.260, 0.261 | 0.5% |
| 1 x default threads, OpenBLAS 1, conv B=512 / rust | 0.291 (0.287-0.295) | 0.291, 0.292 | 0.4% |
| 1 x default threads, OpenBLAS 1, dense B=512 / rust | 0.548 (0.544-0.550) | 0.548, 0.547 | 0.3% |
| 1 x default threads, OpenBLAS default, conv B=32 / rust | 0.250 (0.249-0.250) | 0.250, 0.249 | 0.5% |
| 1 x default threads, OpenBLAS default, conv B=512 / rust | 0.287 (0.280-0.293) | 0.287, 0.287 | 0.1% |
| 1 x default threads, OpenBLAS default, dense B=512 / rust | 0.556 (0.533-0.561) | 0.547, 0.556 | 1.7% |

### prepare

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x default threads, OpenBLAS 1, conv B=32 / rust | 0.005 (0.005-0.006) | 0.005, 0.005 | 3.7% |
| 1 x default threads, OpenBLAS 1, conv B=512 / rust | 0.006 (0.006-0.006) | 0.006, 0.006 | 1.0% |
| 1 x default threads, OpenBLAS 1, dense B=512 / rust | 0.192 (0.191-0.195) | 0.192, 0.193 | 0.3% |
| 1 x default threads, OpenBLAS default, conv B=32 / rust | 0.005 (0.005-0.005) | 0.005, 0.005 | 1.2% |
| 1 x default threads, OpenBLAS default, conv B=512 / rust | 0.006 (0.006-0.006) | 0.006, 0.006 | 1.6% |
| 1 x default threads, OpenBLAS default, dense B=512 / rust | 0.193 (0.191-0.194) | 0.192, 0.193 | 0.7% |

### epoch, loader

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x default threads, OpenBLAS 1, conv B=32 / rust | 0.254 (0.245-0.262) | 0.254, 0.254 | 0.1% |
| 1 x default threads, OpenBLAS 1, conv B=512 / rust | 0.254 (0.251-0.260) | 0.254, 0.255 | 0.5% |
| 1 x default threads, OpenBLAS 1, dense B=512 / rust | 0.353 (0.336-0.356) | 0.344, 0.355 | 3.2% |
| 1 x default threads, OpenBLAS default, conv B=32 / rust | 0.245 (0.241-0.249) | 0.249, 0.241 | 3.1% |
| 1 x default threads, OpenBLAS default, conv B=512 / rust | 0.255 (0.247-0.261) | 0.255, 0.254 | 0.3% |
| 1 x default threads, OpenBLAS default, dense B=512 / rust | 0.353 (0.348-0.356) | 0.352, 0.353 | 0.2% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 20 (20-20) | 20, 20 | 0.0% |
