Old `515849f` against new `515849f`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/attention_timing.py --no-memory --repeats 2 --tokens 256 --features 512 --heads 8 --masks causal --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `cba601e` (extension sha256 `bc8a4a1fc83d`) and new crate `480cebc` (extension sha256 `5b3d1d17cea4`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 2.10 (HIGH); busy processes: none. Each row pools 3 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- 4 rows within noise, max |Δ| 0.7%

### forward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| d=512 T=256 B=8 causal / numpy | 0.169 (0.168-0.169) | 0.169 (0.168-0.169) | -0.1% | 0.169, 0.169, 0.168 / 0.169, 0.168, 0.169 | within noise |
| d=512 T=256 B=8 causal / rust | 0.075 (0.075-0.076) | 0.076 (0.075-0.076) | +0.3% | 0.075, 0.075, 0.076 / 0.076, 0.076, 0.075 | within noise |

### backward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| d=512 T=256 B=8 causal / numpy | 0.274 (0.274-0.277) | 0.274 (0.273-0.275) | +0.0% | 0.274, 0.277, 0.274 / 0.275, 0.274, 0.273 | within noise |
| d=512 T=256 B=8 causal / rust | 0.145 (0.144-0.145) | 0.146 (0.144-0.148) | +0.7% | 0.145, 0.145, 0.144 / 0.146, 0.148, 0.144 | within noise |
