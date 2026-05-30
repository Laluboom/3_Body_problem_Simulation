import math
import matplotlib.pyplot as plt  # noqa: F401
from matplotlib.animation import FuncAnimation  # noqa: F401

# convert all values into SI units (fix g indirectly?)
# find the lagrange points and closest one error rate
# is there a aspect of mass or size to the simulation
# add in the error rates or uncertainities in the simulation
# search and find limits of time in prediction using the Lyapunov exponent

class Planet:
    def __init__(self, x, y, z, radius, color, mass, vx=0, vy=0, vz=0):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.color = color
        self.mass = mass
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.orbit_rk = [(x, y, z)]

def update_position(planet, dt):
    planet.x += planet.vx * dt
    planet.y += planet.vy * dt
    planet.z += planet.vz * dt

def update_velocity(planet, force, dt):
    ax = force[0] / planet.mass
    ay = force[1] / planet.mass
    az = force[2] / planet.mass
    planet.vx += ax * dt
    planet.vy += ay * dt
    planet.vz += az * dt

G = 1 * 10**-11

def gravitational_force(planet1, planet2):
    dx = planet2.x - planet1.x
    dy = planet2.y - planet1.y
    dz = planet2.z - planet1.z
    distance_squared = dx**2 + dy**2 + dz**2
    distance = math.sqrt(distance_squared)
    force_magnitude = G * planet1.mass * planet2.mass / distance_squared
    force_x = force_magnitude * dx / distance
    force_y = force_magnitude * dy / distance
    force_z = force_magnitude * dz / distance
    return (force_x, force_y, force_z)

def runge_kutta_step(planet, dt, planets):
    vx_backup, vy_backup, vz_backup = planet.vx, planet.vy, planet.vz
    x_backup, y_backup, z_backup = planet.x, planet.y, planet.z
    # Calculate forces at the initial position
    initial_force = calculate_total_force(planet, planets)
    # Update velocity using Runge-Kutta metho
    k1x, k1y, k1z = (
        initial_force[0] / planet.mass,
        initial_force[1] / planet.mass,
        initial_force[2] / planet.mass,
    )
    planet.vx = vx_backup + k1x * dt / 2
    planet.vy = vy_backup + k1y * dt / 2
    planet.vz = vz_backup + k1z * dt / 2
    planet.x = x_backup + planet.vx * dt / 2
    planet.y = y_backup + planet.vy * dt / 2
    planet.z = z_backup + planet.vz * dt / 2
    
    second = calculate_total_force(planet, planets)
    k2x, k2y, k2z = (
        second[0] / planet.mass,
        second[1] / planet.mass,
        second[2] / planet.mass,
    )
    planet.vx = vx_backup + k2x * dt / 2
    planet.vy = vy_backup + k2y * dt / 2
    planet.vz = vz_backup + k2z * dt / 2
    planet.x = x_backup + planet.vx * dt / 2
    planet.y = y_backup + planet.vy * dt / 2
    planet.z = z_backup + planet.vz * dt / 2

    third = calculate_total_force(planet, planets)
    k3x, k3y, k3z = (
        third[0] / planet.mass,
        third[1] / planet.mass,
        third[2] / planet.mass,
    )
    planet.vx = vx_backup + k3x * dt / 2
    planet.vy = vy_backup + k3y * dt / 2
    planet.vz = vz_backup + k3z * dt / 2
    planet.x = x_backup + planet.vx * dt / 2
    planet.y = y_backup + planet.vy * dt / 2
    planet.z = z_backup + planet.vz * dt / 2
    last = calculate_total_force(planet, planets)
    k4x, k4y, k4z = last[0] / planet.mass, last[1] / planet.mass, last[2] / planet.mass
    planet.vx = vx_backup + (k1x + 2 * k2x + 2 * k3x + k4x) * dt / 6
    planet.vy = vy_backup + (k1y + 2 * k2y + 2 * k3y + k4y) * dt / 6
    planet.vz = vz_backup + (k1z + 2 * k2z + 2 * k3z + k4z) * dt / 6
    # Update position
    update_position(planet, dt)
    # Append the updated position to the orbit
    planet.orbit_rk.append((planet.x, planet.y, planet.z))


def calculate_total_force(planet, planets):
    total_force = [0, 0, 0]
    for other_planet in planets:
        if planet != other_planet:
            force_component = gravitational_force(planet, other_planet)
            total_force[0] += force_component[0]
            total_force[1] += force_component[1]
            total_force[2] += force_component[2]
    return total_force

def simulate(planets, dt, method):
    for planet in planets:
        runge_kutta_step(planet, dt, planets)

def animate(frame, planets, ax, method):
    dt = 0.01
    simulate(planets, dt, method)
    ax.clear()
    ax.set_box_aspect([1,1,1])
    for planet in planets:
        orbit = planet.orbit_rk
        ax.scatter(
            planet.x,
            planet.y,
            planet.z,
            color=planet.color,
            s=100
        )
        updated_points = list(zip(*orbit))
        ax.plot(
            updated_points[0],
            updated_points[1],
            updated_points[2],
            color=planet.color,
            linewidth=2,
        )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_facecolor("black")
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.xaxis._axinfo["grid"].update({"linewidth": 0.0})
    ax.yaxis._axinfo["grid"].update({"linewidth": 0.0})
    ax.zaxis._axinfo["grid"].update({"linewidth": 0.0})
    # ax.figure(figsize=(8, 8))
    ax.grid(False)

# x, y, z, radius, color, mass, vx=0, vy=0, vz=0
planet_A = Planet(1, 1, 2, 0.1, "red", 1, 0, 1, 0)
planet_B = Planet(1, 2, 1, 0.1, "green", 3, 1, 0, 0)
planet_C = Planet(2, 1, 1, 0.1, "blue", 4, 0, 0, 1)
earth = Planet( 1.496e11, 0, 0, 6.371e6, "blue", 5.972e24, 29297, 0)
mars = Planet( 2.067e11, 0, 0, 3.397e6, "red", 6.42e23, 24130, 0)
planets = [planet_A, planet_B, planet_C]

fig = plt.figure()
ax_rk = fig.add_subplot(111, projection="3d")

ani_rk = FuncAnimation(
    fig,
    animate,
    frames=range(100),
    fargs=(planets, ax_rk, "runge_kutta"),
    interval=50
)

plt.show()

plt.show()
