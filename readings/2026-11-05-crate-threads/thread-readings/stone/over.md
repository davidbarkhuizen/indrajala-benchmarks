Old `f081ecf` against new `f081ecf`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py epochs --backdrop sequence --processes 1 2 4 --threads 1 2 4 8 --repeats 1 -- --windows 64 --features 512 --heads 8` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `362e34c` (extension sha256 `7a3f0df0ecd3`) and new crate `362e34c` (extension sha256 `7a3f0df0ecd3`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-1255u.json); max 1-min load 2.83 (HIGH); busy processes: none. Each row pools 1 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: none (a probe row can carry "control": true)
- 13 rows within noise, max |Δ| 1.9%
- spread of per-pass medians over 13 rows: median 0.6%, 90th percentile 1.8%, max 1.8%
- pass shifts (median over rows of pass median / pooled median): 1 +0.0%, 2 +0.1%

### epoch

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x 1 thread, 2-layer rotary d=512 rust W=64 | 5.117 (5.105-5.128) | 5.128, 5.105 | 0.4% |
| 1 x 2 threads, 2-layer rotary d=512 rust W=64 | 3.581 (3.565-3.598) | 3.565, 3.598 | 0.9% |
| 1 x 4 threads, 2-layer rotary d=512 rust W=64 | 3.099 (3.071-3.126) | 3.071, 3.126 | 1.8% |
| 1 x 8 threads, 2-layer rotary d=512 rust W=64 | 2.543 (2.539-2.546) | 2.539, 2.546 | 0.3% |
| 2 x 1 thread, 2-layer rotary d=512 rust W=64 | 5.924 (5.848-6.206) | 5.924, 6.027 | 1.7% |
| 2 x 2 threads, 2-layer rotary d=512 rust W=64 | 5.356 (5.281-5.396) | 5.356, 5.338 | 0.3% |
| 2 x 4 threads, 2-layer rotary d=512 rust W=64 | 4.427 (4.363-4.470) | 4.381, 4.462 | 1.8% |
| 2 x 8 threads, 2-layer rotary d=512 rust W=64 | 3.880 (3.776-3.942) | 3.880, 3.859 | 0.6% |
| 4 x 1 thread, 2-layer rotary d=512 rust W=64 | 9.786 (7.289-12.011) | 9.786, 9.734 | 0.5% |
| 4 x 2 threads, 2-layer rotary d=512 rust W=64 | 8.174 (7.882-8.481) | 8.136, 8.201 | 0.8% |
| 4 x 4 threads, 2-layer rotary d=512 rust W=64 | 7.161 (7.025-7.478) | 7.152, 7.253 | 1.4% |
| 4 x 8 threads, 2-layer rotary d=512 rust W=64 | 7.130 (6.942-7.844) | 7.131, 7.102 | 0.4% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 20 (20-20) | 20, 20 | 0.0% |
