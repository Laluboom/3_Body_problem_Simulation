# TODOs — 3 Body Problem Simulation

**Verdict 2026-11-01: REVIVE** (unchanged from 2026-09-30, now with a smaller target).

Last review's task 1 shipped (`10dd819`, `G = 1.0`), and it was the right call — gravity is
now on, and that turned a silent nothing into a loud, measurable wrongness. Re-measured
today: the integrator loses **44.9% of the system energy** and **14% of total momentum**
in one time unit. It is no longer "runs but simulates nothing"; it is "simulates something
violently non-physical."

The good news is that the remaining gap is one function. Measured today with the
Chenciner–Montgomery figure-eight (dt=0.001, one period T=6.32591398):

| integrator | closure error | relative energy drift |
|---|---|---|
| this repo today | **2.95** | **44.9%** |
| with task 1 below only | 1.3e-03 | 2.8e-10 |
| with tasks 1 + 2 | 1.1e-04 | 2.0e-14 |

Task 1 alone buys ~99.96% of the win and touches one function. Tasks 1 → 2 → 3 is one
session, and the repo genuinely works at the end of it.

---

### 1. `[BUG]` Restore the position backup in `runge_kutta_step` — `Runge_kutta.py:88-100`

The single highest-value line of work in this repo.

Each RK stage leaves `planet.x/y/z` sitting at `x_backup + v*dt/2` (lines 91-93) and
nothing ever puts them back. Line 100 then calls `update_position(planet, dt)`, which
*adds* `vx*dt` on top of that leftover half-step. Net: **every body moves 1.5× further
than its own velocity says it should, every single step.**

Isolated and confirmed today: a single free body with `v=1`, `dt=0.01`, one call to
`runge_kutta_step` with no other bodies present, ends at `x = 0.0150`. Not 0.0100.
Exactly 1.5×, with gravity entirely out of the picture — so this is a pure bookkeeping
bug, not a physics one.

Same block, second defect: lines 88-93 prepare the stage-4 state with `dt/2`, so `k4`
is sampled at the midpoint. RK4 requires the **full `dt`** there.

Third: position is advanced with the end-of-step velocity, not the RK4-weighted average
of the four stage velocities. That alone caps the scheme at first order in position no
matter how good the velocity update is.

The fix is all three together:
- restore `x_backup, y_backup, z_backup` before the final position update
- use the full `dt` for the stage-4 setup at lines 88-93
- set `planet.x = x_backup + (v1 + 2*v2 + 2*v3 + v4) * dt / 6`, keeping each stage's
  velocity as you go, rather than calling `update_position`

Measured payoff: closure error 2.95 → 1.3e-03, energy drift 44.9% → 2.8e-10. Do this
first; everything below is easier to judge once the integrator is roughly honest.

### 2. `[BUG]` Advance all three bodies from the same state — `Runge_kutta.py:115-117`

`simulate()` does `for planet in planets: runge_kutta_step(planet, dt, planets)`, and
each step permanently commits that planet's new position before the next one is stepped.
So `planet_B` computes its forces against `planet_A`'s **already-advanced** position, and
`planet_C` against both. Pair forces stop being equal and opposite.

Measured on the shipped three-body config (dt=0.01, t=1.0), with task 1 already applied:
total momentum drifts by **0.109** against `|P| = 5.099` — a 2% violation of a quantity
that is supposed to be conserved exactly, in machine arithmetic, forever. Today, with the
position bug still in, the same drift is **0.727** (14%).

Fix: hoist the stage loop out of the per-planet function. Compute every body's `k1` from
the current state, then every body's `k2` from the shared midpoint state, and so on —
four synchronized sweeps, then one commit. A per-planet integrator cannot be correct for
a coupled system; this is structural, not a tweak.

Payoff: closure 1.3e-03 → 1.1e-04, energy drift 2.8e-10 → 2.0e-14, momentum drift → 0.

### 3. `[TEST]` Adopt the figure-eight closure test as the definition of "working"

The Chenciner–Montgomery periodic orbit is a free acceptance test — G=1, all masses 1,
period T = 6.32591398:

```
body0 pos (0.97000436, -0.24308753)   vel (0.46620369, 0.43236573)
body1 pos (-0.97000436, 0.24308753)   vel (0.46620369, 0.43236573)
body2 pos (0, 0)                      vel (-0.93240737, -0.86473146)
```

Integrate one period at dt=0.001 and assert each body returns to its start.

**Important, and the reason this task is worth writing down rather than guessing:** the
thresholds the last review proposed (closure < 1e-3, drift < 1e-10) **fail with task 1
alone** — I measured 1.3e-03 and 2.8e-10, both just over the line. Future-you would fix
task 1 correctly and conclude the fix didn't work. Either do tasks 1 and 2 together and
assert `closure < 5e-4` / `drift < 1e-12`, or stage the thresholds. Don't guess them.

Convergence data for picking dt, measured against a correct reference integrator:

| dt | steps/period | closure | energy drift |
|---|---|---|---|
| 0.02 | 316 | 7.5e-03 | 8.4e-08 |
| 0.01 | 633 | 5.2e-03 | 2.6e-09 |
| 0.005 | 1265 | 1.2e-03 | 8.2e-11 |
| 0.001 | 6326 | 1.1e-04 | 2.0e-14 |

Note what this says about the animation: `animate()` hardcodes `dt = 0.01`
(`Runge_kutta.py:120`) and `FuncAnimation` requests `frames=range(100)`
(`Runge_kutta.py:171`), i.e. t_end = 1.0 — **16% of one figure-eight period.** If you make
the figure-eight the default demo config, you need ~633 frames to see it close.

### 4. `[QUICK WIN ~15min]` Make the animation legible — `Runge_kutta.py:122, 158-163`

Two tiny changes that are correct regardless of the integrator's state, and that you need
in place before you can judge tasks 1-3 by eye.

**Pin the axis limits.** `ax.clear()` runs every frame (line 122) and `set_xlim/ylim/zlim`
are never called anywhere in the file — confirmed, zero occurrences. matplotlib therefore
autoscales to whatever the bodies currently span. The ticks are also stripped (lines
141-143), so there is no remaining cue that the frame rescaled. Add explicit limits
(±2 suits the shipped config; ±1.5 suits the figure-eight).

**Zero the net momentum of the shipped config.** `planets` (lines 158-163) has total
momentum `P = (3, 1, 4)` and total mass 8, so the centre of mass coasts at
`v_com = (0.375, 0.125, 0.5)`, `|v_com| = 0.637`. Over t=8 the COM alone travels 5.1
units while the bodies stay only 0.4–1.4 apart from each other. Subtract `v_com` from all
three initial velocities and the triple sits still and orbits in view.

Worth knowing while you're in there: under a *correct* integrator this config is not the
scatter it looks like. Positions (1,1,2),(1,2,1),(2,1,1) and velocities (0,1,0),(1,0,0),
(0,0,1) are cyclic permutations, and the three pair separations stay **identical to 9
decimal places** for the whole run (1.1307 at t=1, 1.3981 at t=3, 0.4304 at t=6). It is a
bounded, cyclic-symmetric equilateral triple. The only reason it looks like it is flying
apart is the COM drift plus the autoscaling frame. Keep it — it's a nicer demo than it
appears, and it's a decent second test case.

### 5. `[CHORE]` Delete the dead weight — four files, ~110 lines

Nothing here has been touched since the initial commit (`git log` on these paths returns
only `e333961`). It is all first-draft residue and it makes the repo look larger and more
confused than it is:

- `formulas.py` — an earlier, abandoned draft of the same physics. `runge_kutta_step_1/2`
  (lines 16-24) are empty stubs that `return` nothing; `runge_kutta_step_1` takes `force`
  as a scalar and divides it by mass. It also **prints on import** (lines 45-46) and still
  carries `G = 6.67408e-11` (line 3), now contradicting `Runge_kutta.py:37`. Delete it.
- `Position_Vector_Subtraction.java` — 49 lines of Java vector arithmetic, unused by the
  Python simulation, duplicating what `gravitational_force` does inline.
- `matplotlib_guide.py` — 17-line scratch file; its `Axes3D` import (line 2) has been
  unnecessary on matplotlib for years.
- `Runge_kutta.py:161-162` — `earth` and `mars` are constructed and never added to
  `planets` (line 163). They are also wrong: both sit on the +x axis with velocity purely
  along +x, i.e. radial, so they would fly straight outward rather than orbit. And SI
  values cannot share `dt = 0.01 s` with the toy bodies anyway.
- `Runge_kutta.py:115,119` — `simulate()` and `animate()` take a `method` parameter that
  is never read; a vestige of an intended Euler-vs-RK4 comparison. Either implement the
  comparison or drop the argument.
- `Runge_kutta.py:176-178` — `plt.show()` is called twice; the second is a no-op.
