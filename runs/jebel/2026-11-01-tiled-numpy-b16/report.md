Old `b1e92b9` against new `7a121c1`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/attention_timing.py --repeats 5 --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `9e2f1c5564f5`) on both sides. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.08; busy processes: none. Each row pools 3 runs per side.

- CONTROL MOVED: 2 of 18 control rows consistent, e.g. forward / T=256 B=8 causal / rust +18.0%: changes about that size can't be resolved here (next: epoch_op_profile.py)
- consistent: tracemalloc peak / T=1024 B=2 packed / numpy -94.4% (397.3 -> 22.17 MB)
- consistent: tracemalloc peak / T=1024 B=2 causal / numpy -94.4% (397.2 -> 22.44 MB)
- consistent: peak RSS / T=1024 B=2 packed / numpy -93.0% (404.1 -> 28.47 MB)
- consistent: peak RSS / T=1024 B=2 causal / numpy -92.8% (403.9 -> 29.07 MB)
- consistent: tracemalloc peak / T=256 B=8 causal / numpy -79.5% (108.2 -> 22.2 MB)
- consistent: tracemalloc peak / T=256 B=8 packed / numpy -79.4% (108.2 -> 22.27 MB)
- consistent: peak RSS / T=256 B=8 causal / numpy -78.2% (125.2 -> 27.32 MB)
- consistent: peak RSS / T=256 B=8 packed / numpy -78.2% (125.3 -> 27.33 MB)
- consistent: backward / T=64 B=32 packed / numpy +47.4% (0.013 -> 0.019 s)
- consistent: forward / T=1024 B=2 packed / numpy -45.0% (0.190 -> 0.104 s)
- ... 13 more consistent rows (report --md)
- 1 rows within noise (1 separated inside their spread), max |Δ| 3.4%

### forward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| T=64 B=32 causal / numpy | 0.013 (0.013-0.013) | 0.012 (0.012-0.012) | -6.0% | 0.013, 0.013, 0.013 / 0.012, 0.012, 0.012 | consistent |
| T=64 B=32 packed / numpy | 0.014 (0.014-0.014) | 0.013 (0.013-0.013) | -11.0% | 0.014, 0.014, 0.014 / 0.013, 0.013, 0.013 | consistent |
| T=256 B=8 causal / numpy | 0.041 (0.041-0.042) | 0.033 (0.032-0.033) | -21.5% | 0.041, 0.042, 0.041 / 0.033, 0.032, 0.033 | consistent |
| T=256 B=8 packed / numpy | 0.046 (0.046-0.046) | 0.032 (0.032-0.032) | -30.9% | 0.046, 0.046, 0.046 / 0.032, 0.032, 0.032 | consistent |
| T=1024 B=2 causal / numpy | 0.178 (0.178-0.179) | 0.105 (0.105-0.105) | -40.9% | 0.178, 0.179, 0.178 / 0.105, 0.105, 0.105 | consistent |
| T=1024 B=2 packed / numpy | 0.190 (0.189-0.191) | 0.104 (0.104-0.105) | -45.0% | 0.190, 0.191, 0.189 / 0.105, 0.104, 0.104 | consistent |
| T=64 B=32 causal / rust | 0.010 (0.010-0.010) | 0.010 (0.010-0.010) | +7.0% | 0.010, 0.010, 0.010 / 0.010, 0.010, 0.010 | separated, inside spread (control) |
| T=64 B=32 packed / rust | 0.010 (0.010-0.010) | 0.010 (0.010-0.010) | +4.0% | 0.010, 0.010, 0.010 / 0.010, 0.010, 0.010 | consistent (control) |
| T=256 B=8 causal / rust | 0.030 (0.030-0.030) | 0.035 (0.035-0.035) | +18.0% | 0.030, 0.030, 0.030 / 0.035, 0.035, 0.035 | consistent (control) |
| T=256 B=8 packed / rust | 0.032 (0.032-0.032) | 0.032 (0.032-0.032) | -1.0% | 0.032, 0.032, 0.032 / 0.032, 0.032, 0.032 | within noise (control) |
| T=1024 B=2 causal / rust | 0.183 (0.182-0.184) | 0.185 (0.184-0.186) | +0.8% | 0.182, 0.184, 0.183 / 0.184, 0.185, 0.186 | separated, inside spread (control) |
| T=1024 B=2 packed / rust | 0.192 (0.191-0.194) | 0.193 (0.193-0.194) | +0.8% | 0.191, 0.194, 0.192 / 0.193, 0.194, 0.193 | within noise (control) |

### backward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| T=64 B=32 causal / numpy | 0.013 (0.013-0.013) | 0.018 (0.018-0.018) | +42.6% | 0.013, 0.013, 0.013 / 0.018, 0.018, 0.018 | consistent |
| T=64 B=32 packed / numpy | 0.013 (0.013-0.013) | 0.019 (0.018-0.019) | +47.4% | 0.013, 0.013, 0.013 / 0.019, 0.018, 0.019 | consistent |
| T=256 B=8 causal / numpy | 0.032 (0.031-0.032) | 0.039 (0.039-0.039) | +23.8% | 0.032, 0.032, 0.031 / 0.039, 0.039, 0.039 | consistent |
| T=256 B=8 packed / numpy | 0.032 (0.032-0.032) | 0.040 (0.040-0.040) | +25.4% | 0.032, 0.032, 0.032 / 0.040, 0.040, 0.040 | consistent |
| T=1024 B=2 causal / numpy | 0.114 (0.114-0.115) | 0.119 (0.119-0.119) | +4.3% | 0.114, 0.115, 0.114 / 0.119, 0.119, 0.119 | consistent |
| T=1024 B=2 packed / numpy | 0.113 (0.112-0.114) | 0.117 (0.115-0.117) | +3.4% | 0.113, 0.114, 0.112 / 0.117, 0.115, 0.117 | separated, inside spread |
| T=64 B=32 causal / rust | 0.010 (0.010-0.010) | 0.010 (0.010-0.010) | +3.7% | 0.010, 0.010, 0.010 / 0.010, 0.010, 0.010 | separated, inside spread (control) |
| T=64 B=32 packed / rust | 0.010 (0.010-0.010) | 0.010 (0.010-0.010) | +1.3% | 0.010, 0.010, 0.010 / 0.010, 0.010, 0.010 | separated, inside spread (control) |
| T=256 B=8 causal / rust | 0.024 (0.024-0.024) | 0.024 (0.024-0.024) | +1.3% | 0.024, 0.024, 0.024 / 0.024, 0.024, 0.024 | separated, inside spread (control) |
| T=256 B=8 packed / rust | 0.024 (0.023-0.024) | 0.024 (0.024-0.024) | +2.3% | 0.024, 0.023, 0.024 / 0.024, 0.024, 0.024 | within noise (control) |
| T=1024 B=2 causal / rust | 0.146 (0.144-0.148) | 0.145 (0.144-0.147) | -1.0% | 0.144, 0.146, 0.148 / 0.144, 0.145, 0.147 | within noise (control) |
| T=1024 B=2 packed / rust | 0.146 (0.144-0.148) | 0.145 (0.144-0.146) | -0.9% | 0.144, 0.146, 0.148 / 0.146, 0.145, 0.144 | within noise (control) |

### peak RSS

| case | old median (min-max) MB | new median (min-max) MB | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| T=64 B=32 causal / numpy | 42.52 (41.64-42.67) | 27.18 (27.16-27.23) | -36.1% | 42.52, 42.67, 41.64 / 27.18, 27.16, 27.23 | consistent |
| T=64 B=32 packed / numpy | 42.59 (42.59-42.66) | 27.17 (27.12-27.18) | -36.2% | 42.59, 42.59, 42.66 / 27.17, 27.18, 27.12 | consistent |
| T=256 B=8 causal / numpy | 125.2 (125.2-125.3) | 27.32 (27.31-27.39) | -78.2% | 125.3, 125.2, 125.2 / 27.31, 27.32, 27.39 | consistent |
| T=256 B=8 packed / numpy | 125.3 (125.3-125.4) | 27.33 (27.32-27.34) | -78.2% | 125.3, 125.3, 125.4 / 27.32, 27.34, 27.33 | consistent |
| T=1024 B=2 causal / numpy | 403.9 (403.9-404) | 29.07 (28.76-29.92) | -92.8% | 403.9, 403.9, 404 / 28.76, 29.07, 29.92 | consistent |
| T=1024 B=2 packed / numpy | 404.1 (403.6-404.1) | 28.47 (28.46-29.33) | -93.0% | 404.1, 403.6, 404.1 / 28.47, 29.33, 28.46 | consistent |
| T=64 B=32 causal / rust | 29.75 (29.72-29.77) | 29.72 (29.68-30.72) | -0.1% | 29.72, 29.77, 29.75 / 29.72, 29.68, 30.72 | within noise (control) |
| T=64 B=32 packed / rust | 30.27 (30.26-30.27) | 30.26 (30.21-31.27) | -0.0% | 30.27, 30.26, 30.27 / 30.21, 30.26, 31.27 | within noise (control) |
| T=256 B=8 causal / rust | 53.97 (53.95-53.99) | 53.99 (53.98-54.02) | +0.0% | 53.99, 53.97, 53.95 / 54.02, 53.99, 53.98 | within noise (control) |
| T=256 B=8 packed / rust | 54.46 (54.44-54.48) | 54.49 (54.46-54.51) | +0.1% | 54.44, 54.46, 54.48 / 54.46, 54.49, 54.51 | within noise (control) |
| T=1024 B=2 causal / rust | 222.4 (222.4-222.4) | 222.5 (222.4-222.5) | +0.0% | 222.4, 222.4, 222.4 / 222.5, 222.4, 222.5 | separated, inside spread (control) |
| T=1024 B=2 packed / rust | 222.8 (222.8-222.9) | 222.8 (222.7-222.9) | +0.0% | 222.8, 222.8, 222.9 / 222.9, 222.8, 222.7 | within noise (control) |

### tracemalloc peak

| case | old median (min-max) MB | new median (min-max) MB | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| T=64 B=32 causal / numpy | 36.11 (36.11-36.11) | 21.79 (21.79-21.79) | -39.7% | 36.11, 36.11, 36.11 / 21.79, 21.79, 21.79 | consistent |
| T=64 B=32 packed / numpy | 36.16 (36.16-36.16) | 21.86 (21.86-21.86) | -39.5% | 36.16, 36.16, 36.16 / 21.86, 21.86, 21.86 | consistent |
| T=256 B=8 causal / numpy | 108.2 (108.2-108.2) | 22.2 (22.2-22.2) | -79.5% | 108.2, 108.2, 108.2 / 22.2, 22.2, 22.2 | consistent |
| T=256 B=8 packed / numpy | 108.2 (108.2-108.2) | 22.27 (22.27-22.27) | -79.4% | 108.2, 108.2, 108.2 / 22.27, 22.27, 22.27 | consistent |
| T=1024 B=2 causal / numpy | 397.2 (397.2-397.2) | 22.44 (22.44-22.44) | -94.4% | 397.2, 397.2, 397.2 / 22.44, 22.44, 22.44 | consistent |
| T=1024 B=2 packed / numpy | 397.3 (397.3-397.3) | 22.17 (22.17-22.17) | -94.4% | 397.3, 397.3, 397.3 / 22.17, 22.17, 22.17 | consistent |
