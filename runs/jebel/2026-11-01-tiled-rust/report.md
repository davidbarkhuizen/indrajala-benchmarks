Old `5b95176` against new `ccc46d1`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/attention_timing.py --repeats 5 --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `28c4762` (extension sha256 `9e2f1c5564f5`) and new crate `20e87c3` (extension sha256 `8c77a876795f`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.22 (measured just after this run's crate builds); busy processes: none. Each row pools 3 runs per side.

- CONTROL MOVED: 1 of 24 control rows consistent, e.g. backward / T=1024 B=2 causal / numpy -2.8%: changes about that size can't be resolved here (next: epoch_op_profile.py)
- consistent: peak RSS / T=1024 B=2 causal / rust -89.4% (222.3 -> 23.67 MB)
- consistent: peak RSS / T=1024 B=2 packed / rust -89.1% (222.7 -> 24.17 MB)
- consistent: forward / T=1024 B=2 packed / rust -75.4% (0.194 -> 0.048 s)
- consistent: forward / T=1024 B=2 causal / rust -70.2% (0.184 -> 0.055 s)
- consistent: peak RSS / T=256 B=8 causal / rust -59.1% (53.77 -> 21.98 MB)
- consistent: peak RSS / T=256 B=8 packed / rust -58.6% (54.27 -> 22.45 MB)
- consistent: forward / T=256 B=8 causal / rust -52.6% (0.035 -> 0.017 s)
- consistent: backward / T=1024 B=2 packed / rust -52.2% (0.145 -> 0.070 s)
- consistent: forward / T=256 B=8 packed / rust -49.8% (0.032 -> 0.016 s)
- consistent: backward / T=1024 B=2 causal / rust -43.1% (0.146 -> 0.083 s)
- ... 8 more consistent rows (report --md)
- 0 rows within noise

### forward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| T=64 B=32 causal / numpy | 0.012 (0.012-0.012) | 0.012 (0.012-0.012) | +1.1% | 0.012, 0.012, 0.012 / 0.012, 0.012, 0.012 | within noise (control) |
| T=64 B=32 packed / numpy | 0.013 (0.012-0.013) | 0.012 (0.012-0.013) | -0.8% | 0.013, 0.012, 0.013 / 0.012, 0.013, 0.012 | within noise (control) |
| T=256 B=8 causal / numpy | 0.033 (0.033-0.033) | 0.033 (0.032-0.033) | -0.4% | 0.033, 0.033, 0.033 / 0.032, 0.033, 0.033 | within noise (control) |
| T=256 B=8 packed / numpy | 0.032 (0.031-0.032) | 0.031 (0.031-0.032) | -0.5% | 0.032, 0.031, 0.032 / 0.031, 0.031, 0.032 | within noise (control) |
| T=1024 B=2 causal / numpy | 0.105 (0.104-0.105) | 0.105 (0.104-0.105) | -0.3% | 0.105, 0.104, 0.105 / 0.104, 0.105, 0.105 | within noise (control) |
| T=1024 B=2 packed / numpy | 0.103 (0.103-0.104) | 0.103 (0.103-0.103) | -0.3% | 0.103, 0.103, 0.104 / 0.103, 0.103, 0.103 | within noise (control) |
| T=64 B=32 causal / rust | 0.010 (0.010-0.010) | 0.007 (0.007-0.007) | -33.1% | 0.010, 0.010, 0.010 / 0.007, 0.007, 0.007 | consistent |
| T=64 B=32 packed / rust | 0.010 (0.010-0.010) | 0.007 (0.007-0.007) | -32.0% | 0.010, 0.010, 0.010 / 0.007, 0.007, 0.007 | consistent |
| T=256 B=8 causal / rust | 0.035 (0.035-0.036) | 0.017 (0.017-0.017) | -52.6% | 0.035, 0.035, 0.036 / 0.017, 0.017, 0.017 | consistent |
| T=256 B=8 packed / rust | 0.032 (0.032-0.032) | 0.016 (0.016-0.016) | -49.8% | 0.032, 0.032, 0.032 / 0.016, 0.016, 0.016 | consistent |
| T=1024 B=2 causal / rust | 0.184 (0.184-0.185) | 0.055 (0.055-0.055) | -70.2% | 0.185, 0.184, 0.184 / 0.055, 0.055, 0.055 | consistent |
| T=1024 B=2 packed / rust | 0.194 (0.193-0.195) | 0.048 (0.047-0.048) | -75.4% | 0.194, 0.193, 0.195 / 0.047, 0.048, 0.048 | consistent |

### backward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| T=64 B=32 causal / numpy | 0.018 (0.018-0.018) | 0.018 (0.018-0.018) | -0.2% | 0.018, 0.018, 0.018 / 0.018, 0.018, 0.018 | within noise (control) |
| T=64 B=32 packed / numpy | 0.018 (0.018-0.018) | 0.018 (0.018-0.018) | -0.4% | 0.018, 0.018, 0.018 / 0.018, 0.018, 0.018 | within noise (control) |
| T=256 B=8 causal / numpy | 0.039 (0.039-0.039) | 0.039 (0.038-0.039) | -0.8% | 0.039, 0.039, 0.039 / 0.038, 0.039, 0.039 | within noise (control) |
| T=256 B=8 packed / numpy | 0.039 (0.039-0.039) | 0.039 (0.039-0.040) | +0.2% | 0.039, 0.039, 0.039 / 0.040, 0.039, 0.039 | within noise (control) |
| T=1024 B=2 causal / numpy | 0.120 (0.119-0.120) | 0.117 (0.117-0.117) | -2.8% | 0.120, 0.119, 0.120 / 0.117, 0.117, 0.117 | consistent (control) |
| T=1024 B=2 packed / numpy | 0.115 (0.114-0.115) | 0.114 (0.114-0.115) | -0.3% | 0.115, 0.114, 0.115 / 0.115, 0.114, 0.114 | within noise (control) |
| T=64 B=32 causal / rust | 0.010 (0.010-0.010) | 0.012 (0.012-0.012) | +26.0% | 0.010, 0.010, 0.010 / 0.012, 0.012, 0.012 | consistent |
| T=64 B=32 packed / rust | 0.010 (0.010-0.010) | 0.012 (0.012-0.012) | +25.8% | 0.010, 0.010, 0.010 / 0.012, 0.012, 0.012 | consistent |
| T=256 B=8 causal / rust | 0.024 (0.023-0.024) | 0.027 (0.027-0.027) | +12.2% | 0.024, 0.023, 0.024 / 0.027, 0.027, 0.027 | consistent |
| T=256 B=8 packed / rust | 0.024 (0.024-0.024) | 0.025 (0.025-0.025) | +5.3% | 0.024, 0.024, 0.024 / 0.025, 0.025, 0.025 | consistent |
| T=1024 B=2 causal / rust | 0.146 (0.146-0.147) | 0.083 (0.083-0.084) | -43.1% | 0.147, 0.146, 0.146 / 0.083, 0.084, 0.083 | consistent |
| T=1024 B=2 packed / rust | 0.145 (0.145-0.146) | 0.070 (0.069-0.070) | -52.2% | 0.146, 0.145, 0.145 / 0.070, 0.070, 0.069 | consistent |

### peak RSS

| case | old median (min-max) MB | new median (min-max) MB | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| T=64 B=32 causal / numpy | 27.17 (27.16-27.21) | 27.18 (27.16-27.25) | +0.0% | 27.21, 27.16, 27.17 / 27.25, 27.16, 27.18 | within noise (control) |
| T=64 B=32 packed / numpy | 27.16 (27.12-27.17) | 27.16 (26.63-27.18) | -0.0% | 27.12, 27.17, 27.16 / 27.18, 27.16, 26.63 | within noise (control) |
| T=256 B=8 causal / numpy | 27.3 (27.3-27.36) | 27.32 (27.3-27.38) | +0.1% | 27.3, 27.3, 27.36 / 27.3, 27.38, 27.32 | within noise (control) |
| T=256 B=8 packed / numpy | 27.32 (27.29-27.33) | 27.29 (27.23-27.34) | -0.1% | 27.33, 27.32, 27.29 / 27.29, 27.23, 27.34 | within noise (control) |
| T=1024 B=2 causal / numpy | 28.96 (28.8-29.82) | 28.87 (28.87-28.91) | -0.3% | 29.82, 28.96, 28.8 / 28.91, 28.87, 28.87 | within noise (control) |
| T=1024 B=2 packed / numpy | 28.46 (28.4-29.33) | 28.46 (28.4-28.47) | +0.0% | 28.46, 28.4, 29.33 / 28.4, 28.47, 28.46 | within noise (control) |
| T=64 B=32 causal / rust | 29.59 (29.59-29.62) | 21.77 (21.74-21.8) | -26.4% | 29.59, 29.62, 29.59 / 21.8, 21.77, 21.74 | consistent |
| T=64 B=32 packed / rust | 30.1 (30.08-30.11) | 22.3 (22.3-22.32) | -25.9% | 30.1, 30.11, 30.08 / 22.3, 22.3, 22.32 | consistent |
| T=256 B=8 causal / rust | 53.77 (53.73-53.78) | 21.98 (21.97-22) | -59.1% | 53.73, 53.78, 53.77 / 21.98, 22, 21.97 | consistent |
| T=256 B=8 packed / rust | 54.27 (54.27-54.3) | 22.45 (22.44-22.5) | -58.6% | 54.3, 54.27, 54.27 / 22.45, 22.44, 22.5 | consistent |
| T=1024 B=2 causal / rust | 222.3 (222.2-222.3) | 23.67 (23.66-23.67) | -89.4% | 222.2, 222.3, 222.3 / 23.67, 23.67, 23.66 | consistent |
| T=1024 B=2 packed / rust | 222.7 (222.7-222.7) | 24.17 (24.16-24.17) | -89.1% | 222.7, 222.7, 222.7 / 24.17, 24.16, 24.17 | consistent |

### tracemalloc peak

| case | old median (min-max) MB | new median (min-max) MB | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| T=64 B=32 causal / numpy | 21.79 (21.79-21.79) | 21.79 (21.79-21.79) | -0.0% | 21.79, 21.79, 21.79 / 21.79, 21.79, 21.79 | within noise (control) |
| T=64 B=32 packed / numpy | 21.86 (21.86-21.86) | 21.86 (21.86-21.86) | -0.0% | 21.86, 21.86, 21.86 / 21.86, 21.86, 21.86 | within noise (control) |
| T=256 B=8 causal / numpy | 22.2 (22.19-22.2) | 22.2 (22.19-22.2) | +0.0% | 22.2, 22.19, 22.2 / 22.2, 22.19, 22.2 | within noise (control) |
| T=256 B=8 packed / numpy | 22.27 (22.27-22.27) | 22.27 (22.27-22.27) | -0.0% | 22.27, 22.27, 22.27 / 22.27, 22.27, 22.27 | within noise (control) |
| T=1024 B=2 causal / numpy | 22.44 (22.44-22.44) | 22.44 (22.44-22.44) | -0.0% | 22.44, 22.44, 22.44 / 22.44, 22.44, 22.44 | within noise (control) |
| T=1024 B=2 packed / numpy | 22.17 (22.17-22.17) | 22.17 (22.17-22.17) | -0.0% | 22.17, 22.17, 22.17 / 22.17, 22.17, 22.17 | within noise (control) |
