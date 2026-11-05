Old `239db3a` against new `239db3a`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py epochs --threads 0 --openblas 1 0 --repeats 2 --backdrop window` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `d6ff3e4` (extension sha256 `7194f34f6ce9`) and new crate `d6ff3e4` (extension sha256 `7194f34f6ce9`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-1255u.json); max 1-min load 1.28; busy processes: none. Each row pools 2 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: 2 rows, all within noise
- 13 rows within noise, max |Δ| 2.4%
- spread of per-pass medians over 15 rows: median 1.6%, 90th percentile 6.0%, max 6.9%
- pass shifts (median over rows of pass median / pooled median): 1 +0.5%, 2 -0.2%

### per step

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x default threads, OpenBLAS 1, k1 s4 m16 B32 W12 | 0.002 (0.002-0.002) | 0.002, 0.002 | 2.1% |
| 1 x default threads, OpenBLAS 1, k4 s4 m16 B32 W5 | 0.003 (0.003-0.003) | 0.003, 0.003 | 0.2% |
| 1 x default threads, OpenBLAS 1, learn linear k1 s16 m16 B64 W19 | 0.002 (0.002-0.002) | 0.002, 0.002 | 1.9% |
| 1 x default threads, OpenBLAS 1, learn family p7 f32 B64 W16 | 0.014 (0.014-0.014) | 0.014, 0.014 | 1.5% |
| 1 x default threads, OpenBLAS 1, forward linear k1 s16 m16 n1024 | 0.662 (0.658-0.682) | 0.671, 0.661 | 1.6% |
| 1 x default threads, OpenBLAS 1, forward family p7 f32 n1024 | 1.741 (1.728-1.782) | 1.755, 1.741 | 0.8% |
| 1 x default threads, OpenBLAS 1, matmul 256 (control) | 0.000 (0.000-0.000) | 0.000, 0.000 | 6.0% |
| 1 x default threads, OpenBLAS default, k1 s4 m16 B32 W12 | 0.002 (0.002-0.002) | 0.002, 0.002 | 1.8% |
| 1 x default threads, OpenBLAS default, k4 s4 m16 B32 W5 | 0.003 (0.003-0.003) | 0.003, 0.003 | 0.8% |
| 1 x default threads, OpenBLAS default, learn linear k1 s16 m16 B64 W19 | 0.002 (0.002-0.002) | 0.002, 0.002 | 2.1% |
| 1 x default threads, OpenBLAS default, learn family p7 f32 B64 W16 | 0.013 (0.013-0.014) | 0.013, 0.013 | 0.1% |
| 1 x default threads, OpenBLAS default, forward linear k1 s16 m16 n1024 | 0.673 (0.670-0.682) | 0.672, 0.677 | 0.7% |
| 1 x default threads, OpenBLAS default, forward family p7 f32 n1024 | 1.720 (1.698-1.754) | 1.744, 1.702 | 2.4% |
| 1 x default threads, OpenBLAS default, matmul 256 (control) | 0.000 (0.000-0.000) | 0.000, 0.000 | 6.9% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 20 (20-20) | 20, 20 | 0.0% |
