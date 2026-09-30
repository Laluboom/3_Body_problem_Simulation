# Reference — 3 Body Problem Simulation

## Purpose
A 3D gravitational N-body simulation: Newtonian pair forces between `Planet` objects,
integrated forward and drawn as a live matplotlib animation with orbit trails.

## Stack
Python 3 (tested against 3.14.4) · `matplotlib` (3D axes + `FuncAnimation`) · `math`.
No numpy.

## Entry point
```bash
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python3 Runge_kutta.py
```
The venv step is not optional in practice: this machine's system Python has neither
`matplotlib` nor `pip`, so the bare `python Runge_kutta.py` in `README.md:35` exits with
`ModuleNotFoundError: No module named 'matplotlib'`.

## Key files
| File | Role |
|------|------|
| `Runge_kutta.py` | The project. `Planet`, force calc, integrator, animation (179 lines) |
| `formulas.py` | Abandoned earlier draft; RK helpers are empty stubs, prints on import |
| `matplotlib_guide.py` | Matplotlib 3D scratch file, not imported by anything |
| `Position_Vector_Subtraction.java` | Standalone Java vector class, unused |

## Current state — runs, but does not simulate gravity
Measured 2026-09-30 by transcribing the integrator and running it (no matplotlib needed):

- **Gravity is negligible.** `G = 1 * 10**-11` (`Runge_kutta.py:37`) against masses 1/3/4
  at separations ~1.4 gives `|a| = 3.0e-11`, while initial speeds are 1.0. Across the
  whole 100-frame run (t_end = 1.0) velocities change by ~1e-11. Final positions match a
  zero-gravity straight-line prediction to 8 decimals. **The output is three straight
  lines.**
- **Position advances 1.5× per step.** The RK stages leave position at
  `x_backup + v*dt/2` and `update_position` (`Runge_kutta.py:100`) then adds `v*dt` on
  top without restoring the backup. `planet_A` (y=1, vy=1) reaches y=2.5 at t=1.0
  instead of 2.0.
- **Stage 4 uses `dt/2`** (`Runge_kutta.py:88-93`), so `k4` is sampled at the midpoint,
  not the endpoint. With the position defect above, the scheme is not RK4 in any sense.
- **Bodies are advanced sequentially, not simultaneously** (`Runge_kutta.py:115-117`),
  so each body reacts to its predecessors' already-updated positions. Pair forces stop
  being equal and opposite; x-momentum drifts 4.0e-13.

Benchmark on the Chenciner–Montgomery figure-eight orbit (G=1, m=1, T=6.32591398,
dt=0.001), one full period:

| | closure error | relative energy drift |
|---|---|---|
| correct all-bodies RK4 | 5.5e-05 | 2.7e-14 |
| this repo's integrator | 1.67 | 45% |

That test is the cheapest available definition of "working" for this project, and
`todo.md` item 4 proposes adopting it.

## History
Three commits. `e333961` (2026-05-30) is the only real code — all of it, in one push by
Visesh. `fa2003a` and `1700cf5` are automation passes that touched only docs and added a
one-line `requirements.txt`. **No source code has changed since the initial commit.**

`_INDEX.md:60` lists this repo as surviving the 2026-09-21 tier triage on the strength of
its "Runge-Kutta integrator." The integrator is the part that does not work; the idea and
the scaffolding around it are fine.
