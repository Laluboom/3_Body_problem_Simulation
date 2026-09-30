# TODOs — 3 Body Problem Simulation

**Verdict 2026-09-30: REVIVE.** There is real hand-written physics here (~290 LOC), and
the gap between "stub" and "working" is one session, because "working" is now a number:
make the figure-eight orbit close. See `reference.md` for the measurements behind these
tasks. The theme: the simulation runs without error but does not simulate gravity.

---

### 1. `[DONE 2026-09-30]` Set `G = 1.0` at `Runge_kutta.py:37`

`G = 1 * 10**-11` with the toy masses (1, 3, 4) and separations (~1.4) gives an
acceleration of **3.0e-11**. The initial speeds are 1.0. Over the entire 100-frame run
(`Runge_kutta.py:171`, dt=0.01, so t_end = 1.0) gravity changes each velocity by ~1e-11 —
eleven orders of magnitude below the motion already present. **The three bodies currently
fly apart in dead straight lines; the animation shows no gravitational interaction at
all.** Measured: positions match a zero-gravity straight-line prediction to 8 decimals.

`reference.md` used to claim this value was "scaled for the toy planet coordinates." It
was not. For masses ~1 at distances ~1, geometric units (`G = 1.0`) give accelerations
~1.5 and an orbital timescale of a few time units — which is what the coordinates want.

One line. Run it after and you see curved paths for the first time. Do this one first;
every task below is easier to judge once gravity is visibly on.

### 2. `[BUG]` Stop advancing position 1.5× per step — `Runge_kutta.py:88-100`

The four RK stages each leave `planet.x/y/z` at `x_backup + v*dt/2` (lines 91-93). Line
100 then calls `update_position(planet, dt)`, which adds `vx*dt` **on top of that
leftover half-step** — the backup position is never restored. Net effect: every body
travels `1.5 * v * dt` per step.

Verified: `planet_A` starts at y=1 with vy=1; after t=1.0 it sits at **y=2.5**, not
y=2.0. Exactly 1.5×.

Same block, second defect: stage 4 (lines 88-93) sets up with `dt/2`, so `k4` is
evaluated at the midpoint instead of the endpoint. RK4 requires the full `dt` there.

Fix: restore `x_backup, y_backup, z_backup` before the final position update, use the
full `dt` for the stage-4 setup, and advance position with the RK4-weighted velocity
rather than the end-of-step velocity.

### 3. `[BUG]` Advance all bodies from the same state — `Runge_kutta.py:115-117`

`simulate()` loops `for planet in planets: runge_kutta_step(planet, dt, planets)`, and
each step permanently mutates that planet before the next one is stepped. So `planet_B`
computes its forces against `planet_A`'s **already-updated** position, and `planet_C`
against both. The pair forces are no longer equal and opposite, and momentum is not
conserved — measured x-momentum drift of 4.0e-13 against a total velocity change of
3e-11, i.e. ~1% of the interaction, and it grows with G.

Fix: compute every body's acceleration from the current state first, then apply all
updates. This is also the structural precondition for task 4 — a per-planet integrator
cannot be correct for a coupled system.

### 4. `[TEST]` Add the figure-eight closure test — the definition of "working"

The Chenciner–Montgomery periodic three-body orbit is a free acceptance test: G=1, all
masses 1, period T = 6.32591398, and

```
body0 pos (0.97000436, -0.24308753)   vel (0.46620369, 0.43236573)
body1 pos (-0.97000436, 0.24308753)   vel (0.46620369, 0.43236573)
body2 pos (0, 0)                      vel (-0.93240737, -0.86473146)
```

Integrate one period and check the bodies return to their start. Measured with dt=0.001:

| | closure error | energy drift |
|---|---|---|
| correct all-bodies RK4 | 5.5e-05 | 2.7e-14 |
| **this repo's integrator today** | **1.67** | **45%** |

A closure error of 1.67 on an orbit of radius ~1 means the figure-eight falls apart
completely, and losing 45% of the system energy in one period is the clearest possible
proof that the integrator labelled RK4 is not RK4. Assert closure < 1e-3 and relative
energy drift < 1e-10. When this passes, the repo genuinely works — and it will keep
passing, which is worth more here than any amount of visual inspection.

### 5. `[IMPROVEMENT]` Pin the axis limits in `animate()` — `Runge_kutta.py:122`

`ax.clear()` runs every frame and the limits are never set, so matplotlib autoscales to
whatever the bodies currently span. The ticks are also stripped (lines 141-143), so
there is no remaining visual cue that the frame rescaled. The result is that bodies which
are flying apart look like they are hovering in place. Set explicit `set_xlim/ylim/zlim`
(roughly ±1.5 for the figure-eight) so motion and escape are actually visible. Without
this, task 4's figure-eight will be hard to confirm by eye.

---

## Deferred — real, but low value next to the above

Carried from the previous todo.md; still true, still not worth a session:

- `formulas.py:16-24` — `runge_kutta_step_1/2` are stubs that `return` nothing;
  `runge_kutta_step_1` takes `force` as a scalar and divides by mass. Dead earlier draft
  that also prints on import (`formulas.py:45-46`). Delete the file.
- `Runge_kutta.py:176-178` — `plt.show()` called twice; the second is a no-op.
- `Runge_kutta.py:161-162` — `earth` and `mars` are built but never added to `planets`
  (line 163). They are also physically wrong: both sit on the +x axis with velocity
  purely along +x, i.e. radial, so they would fly straight outward rather than orbit.
  Real SI values also cannot share dt=0.01 s with the toy bodies. Delete or rewrite
  with tangential velocities and their own dt.
- `Runge_kutta.py:115,119` — `simulate()` and `animate()` take a `method` parameter that
  is never read; vestige of an intended Euler-vs-RK4 comparison.
- `Position_Vector_Subtraction.java` — 50 lines of Java vector arithmetic, unused by the
  Python simulation and duplicating what `gravitational_force` already does inline.
- `matplotlib_guide.py` — scratch file; its `Axes3D` import (line 2) is unnecessary on
  modern matplotlib.
