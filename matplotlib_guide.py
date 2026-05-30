import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create a 3D figure and axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot some data
ax.scatter([1, 2, 3], [4, 5, 6], [7, 8, 9], color='white')

# Remove axis ticks and set background color
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.set_facecolor("black")

plt.show()
