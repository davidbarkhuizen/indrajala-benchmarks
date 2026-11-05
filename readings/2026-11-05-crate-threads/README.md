# The crate's threads: readings, 2026-11-04 and 11-05

The tables behind indrajala-ml's crate performance workplan's stages 8 and 12, retired 2026-11-05 (`git show 4176d10:docs/workplans/infrastructure/crate-performance-workplan.md`; its close-out in that repository's `docs/next-steps.md`, its parked work in `docs/workplans/infrastructure/jebel-parked-workplan.md`). A/As: they choose work and claim nothing.

| directory | what |
|---|---|
| `thread-readings/{jebel,stone,klip}/` | `ab.py report --pooled` of `thread_cost_probe.py`'s `calls`, `scaling`, `epochs` (stage 8, crate `362e34c`). `jebel`'s were at PL2 120 W |
| `stage12/{klip,stone}/` | OpenBLAS 1 against its default in Rust runs, and klip's sequence benchmark on kernel -42 (crate `d6ff3e4`) |
| `litshe-readings/` | The same set on `litshe`, fan pinned (crate `d6ff3e4`) |
| `litshe-curve/` | `thermal_probe.py`, each second, with the active cooler: 1, 2 and 4 cores pinned, 4 on the stock curve |
| `window-processes/` | Window networks at 1, 2, 4 (and on stone 8) processes, one thread each, the probe's lines; run at once on the three machines |
| `jebel-resets/` | `coretemp` each second, on pyramidon, up to some of `jebel`'s resets |
| `census-stage7-238a017.txt`, `pool.log` | The census behind stage 7's order; `ab_all.sh`'s output for crate #115 |

Raw runs of these remain on the machines. Tier 2 runs are under `runs/`.
