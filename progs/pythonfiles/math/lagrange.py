import numpy as np
import matplotlib.pyplot as plt

# Prepare grid for the plane z = 3x - y
x = np.linspace(-1.5, 1.5, 100)
y = np.linspace(-1.5, 1.5, 100)
X, Y = np.meshgrid(x, y)
Z = 3 * X - Y

# Unit circle in the xy‑plane (z = 0) and lifted curve (z = f(x, y))
theta = np.linspace(0, 2 * np.pi, 400)
circle_x = np.cos(theta)
circle_y = np.sin(theta)
circle_z = np.zeros_like(theta)           # base circle (constraint)
lifted_z = 3 * circle_x - circle_y        # f on the circle

# Critical points
P_max = (3 / np.sqrt(10), -1 / np.sqrt(10), np.sqrt(10))
P_min = (-3 / np.sqrt(10), 1 / np.sqrt(10), -np.sqrt(10))

# Create the 3‑D plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Plot the plane surface
ax.plot_surface(X, Y, Z, alpha=0.5)

# Plot the circle and lifted curve
ax.plot(circle_x, circle_y, circle_z, linewidth=2, label='Constraint: $x^2+y^2=1$')
ax.plot(circle_x, circle_y, lifted_z, linewidth=2, label='Curve: $f$ on the circle')

# Plot the extreme points
ax.scatter(*P_max, s=60, label='Max point')
ax.scatter(*P_min, s=60, label='Min point')

# Formatting
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z (= f(x,y))')
ax.set_title('3‑D view of $f(x,y)=3x - y$ with constraint $x^2+y^2=1$')
ax.legend()

# Adjust the view for better perspective
ax.view_init(elev=30, azim=35)

plt.tight_layout()
plt.show()