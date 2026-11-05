Old `f081ecf` against new `f081ecf`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py epochs --backdrop sequence --processes 1 2 4 8 --threads 1 2 4 8 --repeats 1 -- --windows 64 --features 512 --heads 8` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `7a3f0df0ecd3`) on both sides. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.38; busy processes: none. Each row pools 1 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: none (a probe row can carry "control": true)
- 17 rows within noise, max |Δ| 4.2%
- spread of per-pass medians over 17 rows: median 1.0%, 90th percentile 2.2%, max 4.4%
- pass shifts (median over rows of pass median / pooled median): 1 -0.0%, 2 +0.0%

### epoch

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x 1 thread, 2-layer rotary d=512 rust W=64 | 4.804 (4.781-4.828) | 4.828, 4.781 | 1.0% |
| 1 x 2 threads, 2-layer rotary d=512 rust W=64 | 3.116 (3.112-3.120) | 3.112, 3.120 | 0.3% |
| 1 x 4 threads, 2-layer rotary d=512 rust W=64 | 2.250 (2.248-2.253) | 2.248, 2.253 | 0.3% |
| 1 x 8 threads, 2-layer rotary d=512 rust W=64 | 2.014 (2.011-2.017) | 2.017, 2.011 | 0.3% |
| 2 x 1 thread, 2-layer rotary d=512 rust W=64 | 5.689 (5.659-5.830) | 5.687, 5.747 | 1.0% |
| 2 x 2 threads, 2-layer rotary d=512 rust W=64 | 3.992 (3.936-4.032) | 4.032, 3.944 | 2.2% |
| 2 x 4 threads, 2-layer rotary d=512 rust W=64 | 3.117 (3.081-3.155) | 3.145, 3.091 | 1.7% |
| 2 x 8 threads, 2-layer rotary d=512 rust W=64 | 3.381 (3.356-3.404) | 3.358, 3.403 | 1.3% |
| 4 x 1 thread, 2-layer rotary d=512 rust W=64 | 8.467 (8.104-8.517) | 8.435, 8.476 | 0.5% |
| 4 x 2 threads, 2-layer rotary d=512 rust W=64 | 6.548 (6.295-6.599) | 6.532, 6.548 | 0.2% |
| 4 x 4 threads, 2-layer rotary d=512 rust W=64 | 6.415 (5.979-6.697) | 6.657, 6.375 | 4.4% |
| 4 x 8 threads, 2-layer rotary d=512 rust W=64 | 7.289 (7.227-7.390) | 7.237, 7.342 | 1.5% |
| 8 x 1 thread, 2-layer rotary d=512 rust W=64 | 16.166 (15.438-16.388) | 16.149, 16.186 | 0.2% |
| 8 x 2 threads, 2-layer rotary d=512 rust W=64 | 15.744 (14.787-16.139) | 15.850, 15.601 | 1.6% |
| 8 x 4 threads, 2-layer rotary d=512 rust W=64 | 15.367 (14.588-15.696) | 15.237, 15.442 | 1.3% |
| 8 x 8 threads, 2-layer rotary d=512 rust W=64 | 15.292 (14.588-15.841) | 15.369, 15.167 | 1.3% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 27.8 (27.8-27.8) | 27.8, 27.8 | 0.0% |
