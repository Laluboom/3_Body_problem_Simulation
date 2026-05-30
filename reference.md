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
> Note: README incorrectly states `python simulation.py` — the actual file is `Runge_kutta.py`.

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
- `figManager.window.state('zoomed')` is Tk-backend-specific — will raise `AttributeError` on non-Tk matplotlib backends
- No `requirements.txt`; only external dependency is `matplotlib`
