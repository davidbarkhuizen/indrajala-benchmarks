Old `5cf590a` against new `5cf590a`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/attention_timing.py --no-memory --repeats 2 --tokens 256 --features 512 --heads 8 --masks causal --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `238a017` (extension sha256 `bb3d5611c37d`) and new crate `18ce111` (extension sha256 `bc8a4a1fc83d`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 2.02 (HIGH); busy processes: none. Each row pools 3 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: forward / d=512 T=256 B=8 causal / rust -4.8% (0.079 -> 0.076 s)
- 3 rows within noise, max |Δ| 0.9%

### forward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| d=512 T=256 B=8 causal / numpy | 0.167 (0.167-0.168) | 0.169 (0.167-0.169) | +0.9% | 0.168, 0.167, 0.167 / 0.169, 0.169, 0.167 | within noise |
| d=512 T=256 B=8 causal / rust | 0.079 (0.079-0.080) | 0.076 (0.075-0.076) | -4.8% | 0.079, 0.079, 0.080 / 0.076, 0.075, 0.076 | consistent |

### backward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| d=512 T=256 B=8 causal / numpy | 0.274 (0.273-0.276) | 0.275 (0.273-0.276) | +0.6% | 0.276, 0.273, 0.274 / 0.275, 0.276, 0.273 | within noise |
| d=512 T=256 B=8 causal / rust | 0.145 (0.145-0.146) | 0.146 (0.146-0.146) | +0.6% | 0.146, 0.145, 0.145 / 0.146, 0.146, 0.146 | within noise |
