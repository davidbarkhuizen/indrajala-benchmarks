Old `cb31225` against new `cb31225`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/attention_timing.py --no-memory --repeats 2 --tokens 256 --features 512 --heads 8 --masks causal --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `690bce8` (extension sha256 `7ba3057a73f7`) and new crate `5a19b18` (extension sha256 `84ec4e85d91b`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.01; busy processes: none. Each row pools 3 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- shifted: pass 6 (old, slow +2.2%); unbalanced, next: ab.py extend --order NO
- consistent: backward / d=512 T=256 B=8 causal / rust -39.7% (0.300 -> 0.181 s)
- 3 rows within noise (1 separated inside their spread), max |Δ| 0.8%

### forward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| d=512 T=256 B=8 causal / numpy | 0.169 (0.168-0.169) | 0.169 (0.169-0.170) | +0.2% | 0.169, 0.169, 0.168 / 0.169, 0.170, 0.169 | within noise |
| d=512 T=256 B=8 causal / rust | 0.078 (0.077-0.081) | 0.079 (0.079-0.079) | +0.8% | 0.077, 0.078, 0.081 / 0.079, 0.079, 0.079 | within noise |

### backward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| d=512 T=256 B=8 causal / numpy | 0.273 (0.273-0.275) | 0.276 (0.275-0.276) | +0.8% | 0.273, 0.273, 0.275 / 0.275, 0.276, 0.276 | separated, inside spread |
| d=512 T=256 B=8 causal / rust | 0.300 (0.296-0.349) | 0.181 (0.178-0.182) | -39.7% | 0.300, 0.296, 0.349 / 0.178, 0.181, 0.182 | consistent |
