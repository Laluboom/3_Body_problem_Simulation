# 2026-09-30 Cron Brief — 3_Body_problem_Simulation

## What I looked at

All four source files (`Runge_kutta.py`, `formulas.py`, `matplotlib_guide.py`, the stray
Java class), the README, the three prior tracking files, and `_INDEX.md:60` for the tier
decision. `matplotlib` is not installed on this machine and there is no `pip`, so I could
not run the animation. Instead I transcribed the integrator from `Runge_kutta.py:51-117`
verbatim into a throwaway pure-Python harness and measured it directly. Not a browser
project, so no browser check.

## What I found

**The simulation runs without error and does not simulate gravity.** `G = 1 * 10**-11`
(`Runge_kutta.py:37`) against masses of 1, 3 and 4 at separations of ~1.4 produces an
acceleration of 3.0e-11, while the bodies start with speeds of 1.0. Over the entire
100-frame run the total velocity change from gravity is about 1e-11. Final positions match
a zero-gravity straight-line prediction to eight decimal places. Whatever this program has
been drawing, it is three straight lines. Every prior review of this repo — including the
two automation passes — missed that, because nothing before checked a number.

Second, position advances 1.5× too fast. The RK stages leave `planet.x` at
`x_backup + v*dt/2`, and `update_position` at line 100 then adds `v*dt` on top without
restoring the backup. `planet_A` starts at y=1 with vy=1 and arrives at y=2.5 at t=1.0
rather than y=2.0 — exactly 1.5×. Stage 4 also sets up with `dt/2` instead of the full
`dt` (lines 88-93), so `k4` samples the midpoint. And `simulate()` steps each planet in
place one at a time (lines 115-117), so B and C respond to positions that have already
moved, which breaks the equal-and-opposite pairing and drifts momentum.

To put a number on the integrator overall I ran it against the Chenciner–Montgomery
figure-eight orbit, a known periodic three-body solution. Over one period a correct
all-bodies RK4 returns to its starting point with a closure error of 5.5e-05 and energy
drift of 2.7e-14. This code gives a closure error of **1.67** on an orbit of radius ~1,
and loses **45% of the system energy**. The thing labelled RK4 is not RK4.

## What I am proposing, and why

**Verdict: REVIVE** — and I mean it, for a specific reason. This is not a note pretending
to be a project: `e333961` is ~290 lines of real hand-written physics, and the tier triage
nine days ago already kept it on purpose. More importantly, the figure-eight gives this
repo something most stubs never get — an unambiguous, self-verifying definition of done.
That converts "revive it sometime" into one session with a pass/fail at the end.

So the ranked tasks are the smallest path to a simulation that actually works: set `G` to
1.0 (a one-line quick win that makes gravity visible for the first time), fix the position
double-advance and the stage-4 half-step, advance all bodies from one shared state, then
adopt the figure-eight closure and energy-drift assertions as the test. A fifth task pins
the axis limits, because `ax.clear()` with autoscaling and no ticks currently makes bodies
that are flying apart look like they are hovering — worth fixing before anyone tries to
confirm an orbit by eye.

The old TODO's three items (delete `formulas.py`, drop the duplicate `plt.show()`, resolve
the unused earth/mars presets) are all still true and all still cosmetic. I kept them in a
deferred section rather than let them occupy slots above the physics. One correction worth
recording: `reference.md` previously claimed the tiny `G` was "scaled for the toy planet
coordinates." It was not — it is eleven orders of magnitude too small, and that claim is
probably why the bug survived two reviews.
