Old `4176d10` against new `4176d10`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/sequence_training_timing.py --windows 1024 --repeats 2` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was the venv's (sha256 `17d1c27f71b0`) on both sides. Machine check: profile: identity matches (raspberry-pi-5.json); passes peaked at 51.2-51.2 C; max 1-min load 11.07 (HIGH); busy processes: none. Each row pools 1 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: none (a probe row can carry "control": true)
- 4 rows within noise, max |Δ| 3.9%
- spread of per-pass medians over 4 rows: median 0.1%, 90th percentile 3.8%, max 3.8%
- pass shifts (median over rows of pass median / pooled median): 1 -0.0%, 2 +0.0%

### epoch

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 2-layer rotary numpy W=1024 | 9.886 (9.696-10.076) | 9.696, 10.076 | 3.8% |
| 2-layer rotary rust W=1024 | 5.688 (5.685-5.691) | 5.685, 5.691 | 0.1% |

### held-out nats

| case | median (min-max) nats | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 2-layer rotary numpy W=1024 | 2.925 (2.925-2.925) | 2.925, 2.925 | 0.0% |
| 2-layer rotary rust W=1024 | 2.925 (2.925-2.925) | 2.925, 2.925 | 0.0% |
