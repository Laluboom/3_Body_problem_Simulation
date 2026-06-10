# TODOs

1. **Remove or complete `formulas.py`** — `formulas.py:16-24` contains RK helper stubs that return no usable values, so the file currently reads like a broken alternate implementation.

2. **Remove the duplicate display call** — `Runge_kutta.py:176-178` calls `plt.show()` twice; keep one call and verify the animation still opens normally.

3. **Either use or delete the unused planet presets** — `Runge_kutta.py:161-163` defines `earth` and `mars`, but `Runge_kutta.py:163` only simulates `planet_A`, `planet_B`, and `planet_C`.
