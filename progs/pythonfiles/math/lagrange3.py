import numpy as np
import matplotlib.pyplot as plt

# Constants (feel free to modify)
a, b, c = 3.0, 1.5, 1.0   # semi‑axes of the ellipsoid
l, m, n = 1.0, 2.0, 1.0   # coefficients of F(x,y,z)=lx+my+nz

# Compute extreme points analytically
S = np.sqrt(a**2 * l**2 + b**2 * m**2 + c**2 * n**2)
P_max = np.array([a**2 * l, b**2 * m, c**2 * n]) / S
P_min = -P_max

# Prepare the ellipsoid surface
u = np.linspace(0, np.pi, 60)
v = np.linspace(0, 2 * np.pi, 60)
U, V = np.meshgrid(u, v)
X = a * np.sin(U) * np.cos(V)
Y = b * np.sin(U) * np.sin(V)
Z = c * np.cos(U)

# Prepare a line through the extreme points
t = np.linspace(-1.1, 1.1, 100)
line = np.outer(t, P_max)  # line along ±P_max

# Prepare the plane l x + m y + n z = 0 for reference
xx, yy = np.meshgrid(np.linspace(-2, 2, 10), np.linspace(-2, 2, 10))
plane_z = (-l * xx - m * yy) / n

# Plotting
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Ellipsoid
ax.plot_surface(X, Y, Z, alpha=0.45, linewidth=0)

# Plane
ax.plot_surface(xx, yy, plane_z, alpha=0.2)

# Line through extreme points
ax.plot(line[:, 0], line[:, 1], line[:, 2], linestyle='--')

# Extreme points
ax.scatter(*P_max, s=60, label='Max point')
ax.scatter(*P_min, s=60, label='Min point')

# Gradient vector from origin
ax.quiver(0, 0, 0, l, m, n, length=1.5, arrow_length_ratio=0.1, label='Gradient ∇F')

# Labels & title
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('Extrema of F(x,y,z)=lx+my+nz on an Ellipsoid')

# Make sure the plot is scaled roughly equally
max_range = np.array([X.max() - X.min(), Y.max() - Y.min(), Z.max() - Z.min()]).max() / 2.0
mid_x = (X.max() + X.min()) * 0.5
mid_y = (Y.max() + Y.min()) * 0.5
mid_z = (Z.max() + Z.min()) * 0.5
ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)

ax.legend()
ax.view_init(elev=25, azim=35)
plt.tight_layout()
plt.show()
