Old `4176d10` against new `4176d10`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py epochs --backdrop sequence --processes 1 2 4 --threads 1 2 4 --repeats 1 -- --windows 64 --features 512 --heads 8` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `17d1c27f71b0`) on both sides. Machine check: profile: identity matches (raspberry-pi-5.json); passes peaked at 64.5-65.0 C; max 1-min load 2.43 (HIGH); busy processes: none. Each row pools 1 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: none (a probe row can carry "control": true)
- 10 rows within noise, max |Δ| 8.9%
- spread of per-pass medians over 10 rows: median 1.5%, 90th percentile 9.3%, max 9.3%
- pass shifts (median over rows of pass median / pooled median): 1 -0.4%, 2 +0.3%

### epoch

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x 1 thread, 2-layer rotary d=512 rust W=64 | 17.158 (17.058-17.257) | 17.058, 17.257 | 1.2% |
| 1 x 2 threads, 2-layer rotary d=512 rust W=64 | 11.318 (11.291-11.345) | 11.345, 11.291 | 0.5% |
| 1 x 4 threads, 2-layer rotary d=512 rust W=64 | 11.835 (11.287-12.383) | 12.383, 11.287 | 9.3% |
| 2 x 1 thread, 2-layer rotary d=512 rust W=64 | 24.996 (23.857-25.255) | 25.108, 24.444 | 2.7% |
| 2 x 2 threads, 2-layer rotary d=512 rust W=64 | 23.075 (21.992-23.609) | 22.323, 23.553 | 5.3% |
| 2 x 4 threads, 2-layer rotary d=512 rust W=64 | 27.213 (26.955-27.353) | 27.094, 27.273 | 0.7% |
| 4 x 1 thread, 2-layer rotary d=512 rust W=64 | 61.694 (60.544-62.523) | 61.239, 62.229 | 1.6% |
| 4 x 2 threads, 2-layer rotary d=512 rust W=64 | 59.504 (57.038-61.306) | 60.629, 57.821 | 4.7% |
| 4 x 4 threads, 2-layer rotary d=512 rust W=64 | 60.906 (58.730-61.704) | 60.360, 61.270 | 1.5% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 60.33 (60.05-60.6) | 60.05, 60.6 | 0.9% |
