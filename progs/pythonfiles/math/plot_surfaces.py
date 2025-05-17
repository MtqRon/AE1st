import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# グリッドの準備
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)

# 2つの曲面を計算
Z1 = X**2 + Y**2     # z = x^2 + y^2
Z2 = 2 * X           # z = 2x

# 3Dプロットの作成
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 曲面のプロット
surf1 = ax.plot_surface(X, Y, Z1, cmap=cm.coolwarm, alpha=0.7, linewidth=0, antialiased=True, label='z = x^2 + y^2')
surf2 = ax.plot_surface(X, Y, Z2, cmap=cm.viridis, alpha=0.7, linewidth=0, antialiased=True, label='z = 2x')

# 交線の計算と表示
# x^2 + y^2 = 2x となる点を見つける
# x^2 - 2x + y^2 = 0
# (x-1)^2 + y^2 = 1 これは中心(1,0)、半径1の円
theta = np.linspace(0, 2 * np.pi, 400)
intersect_x = 1 + np.cos(theta)
intersect_y = np.sin(theta)
intersect_z = 2 * intersect_x  # または intersect_x**2 + intersect_y**2 (どちらも同じ値になる)

# 交線のプロット
ax.plot(intersect_x, intersect_y, intersect_z, 'r-', linewidth=3, label='交線')

# ラベルと凡例
ax.set_xlabel('x軸')
ax.set_ylabel('y軸')
ax.set_zlabel('z軸')
ax.set_title('z = x^2 + y^2 と z = 2x の3Dプロット')

# 凡例用のダミープロット（surfaceオブジェクトは通常の凡例では扱えないため）
dummy_surf1 = plt.Rectangle((0, 0), 1, 1, fc=cm.coolwarm(0.5), alpha=0.7)
dummy_surf2 = plt.Rectangle((0, 0), 1, 1, fc=cm.viridis(0.5), alpha=0.7)
ax.legend([dummy_surf1, dummy_surf2, plt.Line2D([0], [0], color='red', linewidth=3)], 
          ['z = x^2 + y^2', 'z = 2x', '交線'])

# 視点の調整
ax.view_init(elev=30, azim=45)

plt.tight_layout()
plt.show() 