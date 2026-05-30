# TODOs

1. **Fix README run command** — `README.md` line 35 says `python simulation.py` but the entry point is `Runge_kutta.py`. Update the README so someone can actually run it on first read.

2. **Remove or complete `formulas.py`** — `runge_kutta_step_2()` at line 22 is an empty stub (`return` with no body) and `runge_kutta_step_1()` computes `k1`/`l1` but also returns nothing. Either finish this as a standalone reference implementation or delete it to avoid confusion with the working code in `Runge_kutta.py`.

3. **Guard the Tk-specific zoom call** — `Runge_kutta.py` line 171 calls `figManager.window.state('zoomed')` which crashes on non-Tk matplotlib backends. Wrap it in `try/except AttributeError` or replace with `plt.tight_layout()`.
