Old `1854b89` against new `1854b89`, run with `scripts/measurement/ab.py`: passes in the order ONNONO. Each pass ran `python scripts/measurement/window_recurrent_timing.py --repeats 3` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `690bce8` (extension sha256 `7ba3057a73f7`) and new crate `5a19b18` (extension sha256 `84ec4e85d91b`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 3.10 (HIGH); busy processes: none. Each row pools 9 runs per side.

- CONTROL MOVED: 1 of 1 control rows consistent, e.g. per step / matmul 256 -46.9%: changes about that size can't be resolved here (next: epoch_op_profile.py)
- consistent, small: per step / learn family p7 f32 B64 W16 +1.0% (0.022 -> 0.023 s)
- 5 rows within noise (2 separated inside their spread), max |Δ| 3.4%

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4, 6) / new (2, 3, 5) | verdict |
|---|---|---|---|---|---|
| k1 s4 m16 B32 W12 | 0.004 (0.004-0.004) | 0.004 (0.004-0.004) | +3.4% | 0.004, 0.004, 0.004 / 0.004, 0.004, 0.004 | separated, inside spread |
| k4 s4 m16 B32 W5 | 0.004 (0.004-0.004) | 0.004 (0.004-0.005) | +2.9% | 0.004, 0.004, 0.004 / 0.004, 0.004, 0.005 | separated, inside spread |
| learn linear k1 s16 m16 B64 W19 | 0.003 (0.003-0.003) | 0.003 (0.003-0.003) | +0.6% | 0.003, 0.003, 0.003 / 0.003, 0.003, 0.003 | within noise |
| learn family p7 f32 B64 W16 | 0.022 (0.022-0.022) | 0.023 (0.023-0.023) | +1.0% | 0.022, 0.022, 0.022 / 0.023, 0.023, 0.023 | consistent, small |
| forward linear k1 s16 m16 n1024 | 1.134 (1.130-1.143) | 1.142 (1.136-1.146) | +0.7% | 1.133, 1.143, 1.132 / 1.137, 1.144, 1.142 | within noise |
| forward family p7 f32 n1024 | 3.398 (3.385-3.410) | 3.405 (3.394-3.432) | +0.2% | 3.398, 3.400, 3.386 / 3.419, 3.395, 3.405 | within noise |
| matmul 256 | 0.001 (0.001-0.001) | 0.000 (0.000-0.000) | -46.9% | 0.001, 0.001, 0.001 / 0.000, 0.000, 0.000 | consistent (control) |
