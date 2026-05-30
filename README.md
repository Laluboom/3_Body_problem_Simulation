# N-Body Gravitational Simulation in 3D

This project simulates gravitational interactions between celestial bodies (planets) in three-dimensional space. The simulation uses Newton's law of gravitation and integrates the system using a 4th-order Runge-Kutta (RK4) method.

## Features

- 3D visualization using matplotlib
- RK4 integration for more accurate position and velocity updates
- Simple gravitational force model (Newtonian)
- Orbit trail tracking for each body
- Customizable bodies (mass, velocity, color, position, etc.)

## How It Works

Each `Planet` object has mass, radius, velocity, position, and a color for plotting. Gravitational forces are calculated between all unique pairs of planets.

The core integration step is done using the `runge_kutta_step()` function, which:
- Calculates acceleration from total gravitational force
- Updates velocity and position in four sub-steps (RK4)
- Stores updated positions to plot orbit paths

The animation uses matplotlib's `FuncAnimation` to update the 3D scene over time.

## Usage

### Dependencies
- Python 3
- `matplotlib`
- `math` (standard library)

### Run the simulation
Just run the script:

```bash
python simulation.py
