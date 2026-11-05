Old `239db3a` against new `239db3a`, run with `scripts/measurement/ab.py`: passes in the order ON. Each pass ran `python scripts/measurement/sequence_training_timing.py --windows 1024 --repeats 2` (the script from the new tree) in its own process tree, from a neutral working directory with only its side's tree on `PYTHONPATH`. Before each pass a probe checked that the trainer module imported from that tree and that the crate extension was that side's release build: old crate `d6ff3e4` (extension sha256 `7194f34f6ce9`) and new crate `d6ff3e4` (extension sha256 `7194f34f6ce9`), each a cached wheel installed with `pip --target` into a directory on `PYTHONPATH` after the tree, so the venv was never touched. Machine check: profile: identity changed (allowed) (ryzen7-3700u-klip.json); max 1-min load 1.06; busy processes: none. Each row pools 1 runs per side.

- too few complete passes for verdicts: they need 2+ a side (ab.py extend)
- controls: none (a probe row can carry "control": true)
- 4 rows within noise, max |Δ| 0.2%
- spread of per-pass medians over 4 rows: median 0.1%, 90th percentile 0.2%, max 0.2%
- pass shifts (median over rows of pass median / pooled median): 1 +0.0%, 2 +0.0%

### epoch

| case | median (min-max) s | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 2-layer rotary numpy W=1024 | 7.298 (7.289-7.306) | 7.289, 7.306 | 0.2% |
| 2-layer rotary rust W=1024 | 4.038 (4.035-4.041) | 4.041, 4.035 | 0.1% |

### held-out nats

| case | median (min-max) nats | per-pass medians (1, 2) | spread |
|---|---|---|---|
| 2-layer rotary numpy W=1024 | 2.925 (2.925-2.925) | 2.925, 2.925 | 0.0% |
| 2-layer rotary rust W=1024 | 2.925 (2.925-2.925) | 2.925, 2.925 | 0.0% |
