# Reference — 3 Body Problem Simulation

## Purpose
A 3D gravitational N-body simulation: Newtonian pair forces between `Planet` objects,
integrated forward and drawn as a live matplotlib animation with orbit trails. Geometric
units (`G = 1`), not SI.

## Stack
Python 3 (tested against 3.14.4) · `matplotlib` (3D axes + `FuncAnimation`) · `math`.
No numpy.

## Entry point
```bash
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python3 Runge_kutta.py
```
The venv step is not optional on this machine: the system Python has neither `matplotlib`
nor `pip` (`python3 -m pip` → `No module named pip`), so the bare `python Runge_kutta.py`
in `README.md:35` exits with `ModuleNotFoundError: No module named 'matplotlib'`.
Still true as of 2026-11-01.

## Key files
| File | Role |
|------|------|
| `Runge_kutta.py` | The project. `Planet`, force calc, integrator, animation (179 lines) |
| `formulas.py` | Abandoned earlier draft; RK helpers are empty stubs, prints on import |
| `matplotlib_guide.py` | Matplotlib 3D scratch file, not imported by anything |
| `Position_Vector_Subtraction.java` | Standalone Java vector class, unused |

## Current state — gravity is on, the integrator is wrong
Measured 2026-11-01 by transcribing the integrator verbatim and running it in pure Python
(no matplotlib needed). The 2026-09-30 `G = 1.0` fix landed in `10dd819`, so the old
"three straight lines" finding is **resolved** — and the real defects are now visible.

Shipped config, dt=0.01, 100 frames (t=1.0): relative energy drift **145.6%**, total
momentum drift **0.727** against `|P| = 5.099` (**14%**).

Three confirmed defects, in value order:

- **Position advances 1.5× per step** — `Runge_kutta.py:88-100`. The RK stages leave
  position at `x_backup + v*dt/2` and line 100 adds `v*dt` on top without restoring the
  backup. Isolated: one free body, `v=1`, `dt=0.01`, one step → `x = 0.0150`, not 0.0100.
  Same block: stage 4 is set up with `dt/2`, so `k4` is sampled at the midpoint not the
  endpoint; and position uses the end-of-step velocity, not the RK4-weighted average.
- **Bodies advance sequentially, not simultaneously** — `Runge_kutta.py:115-117`. Each
  body reacts to its predecessors' already-committed positions, so pair forces are not
  equal and opposite and momentum is not conserved.
- **The frame hides the motion** — `ax.clear()` every frame (`:122`) with no
  `set_xlim/ylim/zlim` anywhere in the file, and ticks stripped (`:141-143`). Meanwhile
  the shipped config has `v_com = (0.375, 0.125, 0.5)`, so the whole triple coasts out of
  frame while the autoscale chases it.

Benchmark — Chenciner–Montgomery figure-eight (G=1, m=1, T=6.32591398), one period:

| | closure error | relative energy drift |
|---|---|---|
| this repo today | 2.95 | 44.9% |
| + position fix only | 1.3e-03 | 2.8e-10 |
| + simultaneous stepping | 1.1e-04 | 2.0e-14 |

That test is the cheapest available definition of "working" here; `todo.md` item 3
proposes adopting it, with threshold caveats.

Non-obvious and worth keeping: the shipped config's positions and velocities are cyclic
permutations, and under a correct integrator the three pair separations stay identical to
9 decimal places — a bounded, cyclic-symmetric equilateral triple, not the escape it
currently resembles.

## History
Five commits. `e333961` (2026-05-30) is the only substantial code — all of it, in one
push. `10dd819` (2026-09-30) is a one-line physics fix from the doer agent. The other
three are automation doc passes. `_INDEX.md:60` lists this repo at "289 LOC, Runge-Kutta
integrator"; ~110 of those lines are the dead files above, and the integrator is the part
that does not work.
