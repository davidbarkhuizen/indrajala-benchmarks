Old `f081ecf` against new `f081ecf`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py epochs --backdrop sequence --processes 1 2 3 --threads 1 2 4 8 --repeats 1 -- --windows 64 --features 512 --heads 8` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `362e34c` (extension sha256 `7a3f0df0ecd3`) and new crate `362e34c` (extension sha256 `7a3f0df0ecd3`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (ryzen7-3700u-klip.json); max 1-min load 3.28 (HIGH); busy processes: none. Each row pools 1 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: none (a probe row can carry "control": true)
- 13 rows within noise, max |Δ| 14.7%
- spread of per-pass medians over 13 rows: median 0.6%, 90th percentile 5.3%, max 15.8%
- pass shifts (median over rows of pass median / pooled median): 1 +0.0%, 2 +0.0%

### epoch

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x 1 thread, 2-layer rotary d=512 rust W=64 | 13.717 (13.698-13.737) | 13.698, 13.737 | 0.3% |
| 1 x 2 threads, 2-layer rotary d=512 rust W=64 | 8.803 (8.791-8.815) | 8.791, 8.815 | 0.3% |
| 1 x 4 threads, 2-layer rotary d=512 rust W=64 | 6.179 (6.127-6.231) | 6.231, 6.127 | 1.7% |
| 1 x 8 threads, 2-layer rotary d=512 rust W=64 | 6.708 (6.677-6.739) | 6.677, 6.739 | 0.9% |
| 2 x 1 thread, 2-layer rotary d=512 rust W=64 | 14.530 (14.500-14.535) | 14.514, 14.534 | 0.1% |
| 2 x 2 threads, 2-layer rotary d=512 rust W=64 | 9.532 (9.404-9.544) | 9.534, 9.472 | 0.6% |
| 2 x 4 threads, 2-layer rotary d=512 rust W=64 | 10.002 (9.927-10.079) | 10.069, 9.936 | 1.3% |
| 2 x 8 threads, 2-layer rotary d=512 rust W=64 | 10.208 (10.194-10.226) | 10.218, 10.200 | 0.2% |
| 3 x 1 thread, 2-layer rotary d=512 rust W=64 | 17.645 (16.140-19.054) | 19.019, 16.230 | 15.8% |
| 3 x 2 threads, 2-layer rotary d=512 rust W=64 | 18.572 (18.018-19.479) | 19.433, 18.457 | 5.3% |
| 3 x 4 threads, 2-layer rotary d=512 rust W=64 | 19.723 (19.370-19.812) | 19.706, 19.739 | 0.2% |
| 3 x 8 threads, 2-layer rotary d=512 rust W=64 | 21.241 (20.905-21.523) | 20.910, 21.516 | 2.9% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 62 (62-62) | 62, 62 | 0.0% |
