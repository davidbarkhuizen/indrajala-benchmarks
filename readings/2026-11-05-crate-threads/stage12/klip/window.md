Old `239db3a` against new `239db3a`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py epochs --threads 0 --openblas 1 0 --repeats 2 --backdrop window` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `d6ff3e4` (extension sha256 `7194f34f6ce9`) and new crate `d6ff3e4` (extension sha256 `7194f34f6ce9`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity changed (allowed) (ryzen7-3700u-klip.json); max 1-min load 1.59 (HIGH); busy processes: none. Each row pools 2 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: 2 rows, all within noise
- 13 rows within noise, max |Δ| 2.3%
- spread of per-pass medians over 15 rows: median 0.4%, 90th percentile 2.3%, max 2.3%
- pass shifts (median over rows of pass median / pooled median): 1 +0.1%, 2 -0.1%

### per step

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x default threads, OpenBLAS 1, k1 s4 m16 B32 W12 | 0.008 (0.007-0.008) | 0.008, 0.008 | 2.3% |
| 1 x default threads, OpenBLAS 1, k4 s4 m16 B32 W5 | 0.009 (0.009-0.009) | 0.009, 0.009 | 1.8% |
| 1 x default threads, OpenBLAS 1, learn linear k1 s16 m16 B64 W19 | 0.005 (0.005-0.005) | 0.005, 0.005 | 0.3% |
| 1 x default threads, OpenBLAS 1, learn family p7 f32 B64 W16 | 0.042 (0.042-0.043) | 0.042, 0.042 | 0.6% |
| 1 x default threads, OpenBLAS 1, forward linear k1 s16 m16 n1024 | 2.211 (2.205-2.212) | 2.211, 2.209 | 0.1% |
| 1 x default threads, OpenBLAS 1, forward family p7 f32 n1024 | 5.821 (5.805-5.838) | 5.829, 5.813 | 0.3% |
| 1 x default threads, OpenBLAS 1, matmul 256 (control) | 0.001 (0.001-0.001) | 0.001, 0.001 | 0.4% |
| 1 x default threads, OpenBLAS default, k1 s4 m16 B32 W12 | 0.008 (0.007-0.008) | 0.008, 0.008 | 1.1% |
| 1 x default threads, OpenBLAS default, k4 s4 m16 B32 W5 | 0.009 (0.009-0.009) | 0.009, 0.009 | 1.5% |
| 1 x default threads, OpenBLAS default, learn linear k1 s16 m16 B64 W19 | 0.005 (0.005-0.005) | 0.005, 0.005 | 0.1% |
| 1 x default threads, OpenBLAS default, learn family p7 f32 B64 W16 | 0.042 (0.042-0.043) | 0.042, 0.042 | 0.0% |
| 1 x default threads, OpenBLAS default, forward linear k1 s16 m16 n1024 | 2.237 (2.235-2.339) | 2.236, 2.287 | 2.3% |
| 1 x default threads, OpenBLAS default, forward family p7 f32 n1024 | 5.813 (5.805-5.865) | 5.813, 5.835 | 0.4% |
| 1 x default threads, OpenBLAS default, matmul 256 (control) | 0.001 (0.001-0.001) | 0.001, 0.001 | 1.9% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 40 (40-40) | 40, 40 | 0.0% |
