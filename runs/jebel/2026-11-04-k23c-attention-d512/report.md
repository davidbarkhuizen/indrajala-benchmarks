Old `bb60c11` against new `bb60c11`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/attention_timing.py --no-memory --repeats 2 --tokens 256 --features 512 --heads 8 --masks causal --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `10aa3e5` (extension sha256 `24bdf26aceef`) and new crate `3bb2a40` (extension sha256 `bb3d5611c37d`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 2.34 (HIGH); busy processes: none. Each row pools 3 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- 4 rows within noise, max |Δ| 0.7%

### forward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| d=512 T=256 B=8 causal / numpy | 0.169 (0.168-0.169) | 0.170 (0.169-0.172) | +0.5% | 0.169, 0.168, 0.169 / 0.170, 0.169, 0.172 | within noise |
| d=512 T=256 B=8 causal / rust | 0.079 (0.079-0.079) | 0.079 (0.079-0.080) | +0.7% | 0.079, 0.079, 0.079 / 0.079, 0.079, 0.080 | within noise |

### backward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| d=512 T=256 B=8 causal / numpy | 0.276 (0.275-0.276) | 0.276 (0.275-0.277) | +0.1% | 0.275, 0.276, 0.276 / 0.277, 0.275, 0.276 | within noise |
| d=512 T=256 B=8 causal / rust | 0.144 (0.143-0.148) | 0.144 (0.142-0.146) | -0.4% | 0.148, 0.143, 0.144 / 0.146, 0.144, 0.142 | within noise |
