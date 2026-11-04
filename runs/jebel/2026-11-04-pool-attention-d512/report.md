Old `0b17d22` against new `0b17d22`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/attention_timing.py --no-memory --repeats 2 --tokens 256 --features 512 --heads 8 --masks causal --json <pass output>` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `edce2de` (extension sha256 `f72612f402e8`) and new crate `51a2baf` (extension sha256 `7194f34f6ce9`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 1.62 (HIGH); busy processes: none. Each row pools 3 runs per side.

- controls: none (--control-backend reads the other backend's rows as controls)
- 4 rows within noise (2 separated inside their spread), max |Δ| 7.2%

### forward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| d=512 T=256 B=8 causal / numpy | 0.170 (0.170-0.171) | 0.171 (0.170-0.171) | +0.3% | 0.170, 0.171, 0.170 / 0.171, 0.170, 0.171 | within noise |
| d=512 T=256 B=8 causal / rust | 0.076 (0.076-0.076) | 0.074 (0.073-0.074) | -2.9% | 0.076, 0.076, 0.076 / 0.074, 0.073, 0.074 | separated, inside spread |

### backward

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| d=512 T=256 B=8 causal / numpy | 0.280 (0.280-0.281) | 0.281 (0.279-0.283) | +0.1% | 0.281, 0.280, 0.280 / 0.281, 0.279, 0.283 | within noise |
| d=512 T=256 B=8 causal / rust | 0.146 (0.142-0.150) | 0.136 (0.135-0.136) | -7.2% | 0.142, 0.150, 0.146 / 0.136, 0.135, 0.136 | separated, inside spread |
