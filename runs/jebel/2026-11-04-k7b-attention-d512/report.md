Old `0d91d1a` against new `0d91d1a`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/attention_timing.py --no-memory --repeats 2 --tokens 256 --features 512 --heads 8 --masks causal --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `6a8190c` (extension sha256 `84ec4e85d91b`) and new crate `7b9878f` (extension sha256 `21b07c2bef84`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.48; busy processes: none. Each row pools 3 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- consistent: backward / d=512 T=256 B=8 causal / rust -20.8% (0.184 -> 0.146 s)
- 3 rows within noise, max |Δ| 1.2%

### forward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| d=512 T=256 B=8 causal / numpy | 0.169 (0.169-0.170) | 0.171 (0.169-0.176) | +1.2% | 0.169, 0.169, 0.170 / 0.169, 0.176, 0.171 | within noise |
| d=512 T=256 B=8 causal / rust | 0.079 (0.079-0.080) | 0.079 (0.079-0.080) | -0.2% | 0.079, 0.080, 0.079 / 0.080, 0.079, 0.079 | within noise |

### backward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| d=512 T=256 B=8 causal / numpy | 0.275 (0.275-0.276) | 0.277 (0.276-0.295) | +0.5% | 0.275, 0.275, 0.276 / 0.276, 0.295, 0.277 | within noise |
| d=512 T=256 B=8 causal / rust | 0.184 (0.182-0.186) | 0.146 (0.145-0.148) | -20.8% | 0.186, 0.182, 0.184 / 0.148, 0.146, 0.145 | consistent |
