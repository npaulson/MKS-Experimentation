import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D


fig = plt.figure(figsize=[9, 5.5])
ax = fig.add_subplot(111, projection='3d')

bdim = 10
alpha = .5

p1_vec = np.arange(0, 360.1, bdim)
P_vec = np.arange(0, 90.1, bdim)
p2_vec = np.arange(0, 60.1, bdim)

for p1 in p1_vec:
    for P in P_vec:
        x = np.array([p1, p1])
        y = np.array([P, P])
        z = np.array([p2_vec[0], p2_vec[-1]])
        ax.plot(x, y, z, 'b', alpha=alpha)

for p1 in p1_vec:
    for p2 in p2_vec:
        x = np.array([p1, p1])
        y = np.array([P_vec[0], P_vec[-1]])
        z = np.array([p2, p2])
        ax.plot(x, y, z, 'b', alpha=alpha)

for P in P_vec:
    for p2 in p2_vec:
        x = np.array([p1_vec[0], p1_vec[-1]])
        y = np.array([P, P])
        z = np.array([p2, p2])
        ax.plot(x, y, z, 'b', alpha=alpha)

fz = 20
ax.set_xlabel('$\phi_1$', fontsize=fz)
ax.set_ylabel('$\Phi$', fontsize=fz)
ax.set_zlabel('$\phi_2$', fontsize=fz)

ax.set_xlim(0, 360)
ax.set_ylim(0, 90)
ax.set_zlim(0, 60)

plt.tight_layout()
plt.show()
