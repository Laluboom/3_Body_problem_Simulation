# Daily brief — 3_Body_problem_Simulation — 2026-11-01

**Verdict: REVIVE.** Same as last time, but the target is much smaller now.

## What I looked at

`git log` (5 commits), `Runge_kutta.py` in full, `formulas.py`, `matplotlib_guide.py`,
`Position_Vector_Subtraction.java`, `README.md`, `requirements.txt`, `.gitignore`, the
existing `todo.md`/`reference.md`, and `_INDEX.md:60`.

matplotlib still isn't installed here and `python3 -m pip` still reports no pip module, so
I couldn't run the animation. Instead I transcribed `Runge_kutta.py:11-117` verbatim into
a dependency-free script and measured the integrator directly — energy, momentum, and the
Chenciner–Montgomery figure-eight closure. Not a web project, so no browser check.

## What changed since 2026-09-30

Last review's task 1 shipped: `10dd819` set `G = 1.0`. That was correct and it mattered.
With `G = 1e-11` the three bodies flew in dead straight lines and every other defect was
masked by eleven orders of magnitude. Gravity is on now, and the integrator's actual
behaviour is loud: **145.6% energy drift and 14% momentum loss over the shipped 100-frame
run.** Tasks 2-5 from the old list were never touched.

## The finding worth acting on

The headline bug is bookkeeping, not physics. In `runge_kutta_step`, each RK stage leaves
`planet.x/y/z` at `x_backup + v*dt/2` and nothing restores the backup, so when line 100
calls `update_position(planet, dt)` it adds `v*dt` on top of the leftover half-step. I
isolated this with gravity completely out of the picture — one free body, `v=1`,
`dt=0.01`, one step — and it lands at `x = 0.0150` instead of `0.0100`. Exactly 1.5×,
every step, for every body.

Fixing that one function (restore the backup, give stage 4 the full `dt`, and advance
position with the RK4-weighted stage velocities) takes the figure-eight closure error from
**2.95 to 1.3e-03** and energy drift from **44.9% to 2.8e-10**. That is 99.96% of the win
for one function. Then hoisting the stage loop so all three bodies advance from a shared
state (`simulate()` currently commits each planet before stepping the next) takes it to
**1.1e-04 / 2.0e-14** and makes momentum conservation exact.

One detail I want on record because it would otherwise burn a session: the thresholds the
last review proposed for the figure-eight test (closure < 1e-3, drift < 1e-10) **fail by a
hair with the position fix alone** — 1.3e-03 and 2.8e-10. Fix both bugs before asserting,
or stage the thresholds.

## Two things that look like bugs and aren't

The shipped three-body config appears to fly apart. It doesn't. Its positions and
velocities are cyclic permutations, and under a correct integrator the three pair
separations stay identical to nine decimal places — a bounded, cyclic-symmetric
equilateral triple. What actually happens is that total momentum is `(3, 1, 4)`, so the
centre of mass coasts at `|v_com| = 0.637` and drags the system out of frame, while
`ax.clear()` with no `set_xlim` anywhere in the file autoscales to follow it and the
stripped ticks hide the rescale. Subtracting `v_com` and pinning the limits is ~15
minutes and makes the whole thing watchable — worth doing before you try to judge the
integrator fixes by eye.

## Proposed, in order

1. `[BUG]` the position/stage-4/weighted-velocity fix in `runge_kutta_step` (`:88-100`)
2. `[BUG]` synchronized stepping in `simulate()` (`:115-117`)
3. `[TEST]` the figure-eight closure test, with honest thresholds
4. `[QUICK WIN ~15min]` pin axis limits, zero the net momentum (`:122`, `:158-163`)
5. `[CHORE]` delete ~110 lines of dead weight — `formulas.py` (empty stubs, prints on
   import, contradictory `G`), the Java file, the matplotlib scratch file, the unused
   `earth`/`mars`, the unread `method` parameter, the duplicate `plt.show()`

Items 1-3 are one session and the repo genuinely works afterwards. That's why this is a
REVIVE and not a PARK.
