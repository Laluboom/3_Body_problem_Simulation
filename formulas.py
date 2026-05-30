import math

G = 6.67408 * (10**-11)
dt = 0.1

def GravitationalForce(Planet1, Planet2):
    r_distance = Distance(Planet1, Planet2)
    force_magnitude = G * Planet1.mass * Planet2.mass / r_distance**2
    force_x = force_magnitude * (Planet2.x - Planet1.x) / r_distance
    force_y = force_magnitude * (Planet2.y - Planet1.y) / r_distance
    force_z = force_magnitude * (Planet2.z - Planet1.z) / r_distance
    return (force_x, force_y, force_z)
def Distance(Planet1, Planet2):
    return math.sqrt((Planet2.x - Planet1.x)**2 + (Planet2.y - Planet1.y)**2 + (Planet2.z - Planet1.z)**2)

def runge_kutta_step_1(Planet1,force):
    k1 = dt * Planet1.vx
    l1 = dt * (force/Planet1.mass)
    # l1 = time step * (force/mass of relative planet)
    return
    
def runge_kutta_step_2():
    # new velocity k2 = time step* (velocity +l1/2)
    return

class Planet:
    def __init__(self, x, y, z, radius, color, mass, vx, vy, vz):
        self.radius = radius
        self.color = color
        self.mass = mass
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.orbit_rk = [(x, y, z)]
        
# x, y, z, radius, color, mass, vx=0, vy=0, vz=0
planet_A = Planet(0, 0, 100, 0.1, "red"  , 2, 0, 0, 0)
planet_B = Planet(160, 100, 0, 0.1, "green", 2, 0, 0, 0)
planet_C = Planet(158, 1, 1, 0.1, "blue" , 2, 0, 0, 0)
planets = [planet_A, planet_B, planet_C]

print(Distance(planet_A, planet_B),"meters")
print(GravitationalForce(planet_A,planet_B)[2])