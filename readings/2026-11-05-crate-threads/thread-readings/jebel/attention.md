Old `f081ecf` against new `f081ecf`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/thread_cost_probe.py epochs --backdrop attention --threads 1 2 4 8 --repeats 1 -- --tokens 256 --features 512 --heads 8 --masks causal --repeats 2` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `7a3f0df0ecd3`) on both sides. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.90 (HIGH); busy processes: none. Each row pools 1 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: none (a probe row can carry "control": true)
- 9 rows within noise, max |Δ| 3.3%
- spread of per-pass medians over 9 rows: median 0.4%, 90th percentile 3.2%, max 3.2%
- pass shifts (median over rows of pass median / pooled median): 1 -0.1%, 2 +0.1%

### forward

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x 1 thread, d=512 T=256 B=8 causal / rust | 0.153 (0.151-0.156) | 0.151, 0.156 | 3.2% |
| 1 x 2 threads, d=512 T=256 B=8 causal / rust | 0.107 (0.106-0.107) | 0.107, 0.106 | 1.1% |
| 1 x 4 threads, d=512 T=256 B=8 causal / rust | 0.086 (0.086-0.086) | 0.086, 0.086 | 0.2% |
| 1 x 8 threads, d=512 T=256 B=8 causal / rust | 0.075 (0.075-0.075) | 0.075, 0.075 | 0.5% |

### backward

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 1 x 1 thread, d=512 T=256 B=8 causal / rust | 0.274 (0.271-0.278) | 0.271, 0.278 | 2.3% |
| 1 x 2 threads, d=512 T=256 B=8 causal / rust | 0.199 (0.198-0.199) | 0.199, 0.198 | 0.4% |
| 1 x 4 threads, d=512 T=256 B=8 causal / rust | 0.157 (0.157-0.158) | 0.157, 0.158 | 0.2% |
| 1 x 8 threads, d=512 T=256 B=8 causal / rust | 0.147 (0.147-0.147) | 0.147, 0.147 | 0.3% |

### peak temperature

| case | median (min-max) C | per-pass medians (1, 2) | spread |
|---|---|---|---|
| the probe | 27.8 (27.8-27.8) | 27.8, 27.8 | 0.0% |
