Old `7837558` against new `8bb8977`, run with `scripts/measurement/ab.py`: passes in the order ONNO. Each pass ran `python /home/david/code/indrajala-studies/scripts/measurement/window_study_timing.py` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `857aff8` (extension sha256 `18304f7c5a63`) and new crate `bb05ca1` (extension sha256 `5f29e9f8c99e`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity matches (i7-9700k.json); max 1-min load 0.31 (measured just after this run's crate builds); busy processes: none. Each row pools 10 runs per side.

- CONTROL MOVED: 1 of 1 control rows consistent, e.g. per step / matmul 256 -22.9%: changes about that size can't be resolved here (next: epoch_op_profile.py)
- shifted: pass 1 (old, fast -3.3%), pass 2 (new, fast -2.6%); balanced
- 1 rows within noise, max |Δ| 0.0%

### per step

| case | old median (min-max) s | new median (min-max) s | Δ median | per-pass medians old (1, 4) / new (2, 3) | verdict |
|---|---|---|---|---|---|
| long test family p7 f32 U1 n1024 c1023 | 10.706 (10.696-10.730) | 10.704 (10.675-10.726) | -0.0% | 10.706, 10.710 / 10.683, 10.717 | within noise |
| matmul 256 | 0.001 (0.000-0.001) | 0.000 (0.000-0.000) | -22.9% | 0.000, 0.001 / 0.000, 0.000 | consistent (control) |
