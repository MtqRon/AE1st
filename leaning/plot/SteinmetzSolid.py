import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# finer grid
theta = np.linspace(0, 2*np.pi, 120)
h = np.linspace(-1, 1, 120)
theta_grid, h_grid = np.meshgrid(theta, h)

# Cylinder 1 (axis z)
x1 = np.cos(theta_grid)
y1 = np.sin(theta_grid)
z1 = h_grid

# Cylinder 2 (axis y)
x2 = np.cos(theta_grid)
z2 = np.sin(theta_grid)
y2 = h_grid

# Mask for overlapping region
mask1 = x1**2 + z1**2 <= 1 + 1e-8   # inside cylinder 2
mask2 = x2**2 + y2**2 <= 1 + 1e-8   # inside cylinder 1

# create masked arrays with NaNs where not overlapping
x1_m = np.where(mask1, x1, np.nan)
y1_m = np.where(mask1, y1, np.nan)
z1_m = np.where(mask1, z1, np.nan)

x2_m = np.where(mask2, x2, np.nan)
y2_m = np.where(mask2, y2, np.nan)
z2_m = np.where(mask2, z2, np.nan)

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')

# Overlapping surfaces
ax.plot_surface(x1_m, y1_m, z1_m, color='orange', alpha=0.8, linewidth=0, antialiased=False)
ax.plot_surface(x2_m, y2_m, z2_m, color='orange', alpha=0.8, linewidth=0, antialiased=False)

# Optionally show outlines of full cylinders lightly for context
ax.plot_surface(x1, y1, z1, color='grey', alpha=0.1, linewidth=0)
ax.plot_surface(x2, y2, z2, color='grey', alpha=0.1, linewidth=0)

ax.set_xlim(-1.1,1.1)
ax.set_ylim(-1.1,1.1)
ax.set_zlim(-1.1,1.1)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('Overlap region coloured (Steinmetz solid surface)')
ax.view_init(elev=25, azim=30)
plt.tight_layout()
plt.show()
