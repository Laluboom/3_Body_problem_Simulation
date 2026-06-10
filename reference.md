# Reference — 3 Body Problem Simulation

## Purpose
Physics N-body gravitational simulation in 3D. Uses Newton's law of gravitation and 4th-order Runge-Kutta (RK4) integration to compute trajectories, rendered as a live matplotlib animation with orbit trails.

## Stack
- Python 3
- `matplotlib` (3D axes, `FuncAnimation`)
- `math` (standard library)

## Entry Point
```bash
python Runge_kutta.py
```
> README now matches the actual entry point: `Runge_kutta.py`.

## Key Files
| File | Role |
|------|------|
| `Runge_kutta.py` | Main simulation — `Planet` class, full RK4 integrator, animation loop |
| `formulas.py` | Incomplete earlier draft — RK4 step 2 is a stub (`return` with no body) |
| `matplotlib_guide.py` | Matplotlib reference/scratch file |
| `Position_Vector_Subtraction.java` | Standalone Java vector subtraction — not used by the Python simulation |
| `README.md` | Project overview and feature list |

## Notable Details
- `G = 1 * 10**-11` in `Runge_kutta.py` (not the real SI value `6.674e-11`); scaled for the toy planet coordinates used
- Three toy planets (A/B/C) are the active simulation; Earth/Mars objects are defined but not added to the `planets` list
- `Runge_kutta.py` currently calls `plt.show()` twice at lines 176 and 178; that is redundant and should be reduced to one call
- `requirements.txt` now records the only external dependency: `matplotlib`

## 2026-06-10 Run Notes
- Added `requirements.txt` with `matplotlib`, grounded by the imports in `Runge_kutta.py:2-3`.
- Verified `requirements.txt` contains exactly one dependency entry: `matplotlib`.

## 2026-05-31 Run Notes
- Verified the README entry-point fix at `README.md:35`.
- `python3 -m py_compile Runge_kutta.py formulas.py` passed.
- `git pull --ff-only` could not reach the remote because local SSH config/remote access failed; no remote changes were fetched.
