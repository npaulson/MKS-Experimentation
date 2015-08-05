import numpy as np
import h5py
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D






# open file containing Matthew's data
filename = 'ep_set.hdf5'
f = h5py.File(filename, 'r')

euler = f.get('euler_set')[...]
ep = f.get('ep_set')[...]

# X = np.transpose(ep)
X = ep

print X.shape

pca = PCA()
X_pc = pca.fit(X).transform(X)  # mean is subracted as a part of this


print(pca.explained_variance_ratio_)
print X_pc.shape

fig = plt.figure(1, figsize=[14, 10])

tmp0 = .6*np.ones(euler.shape[0])
# tmp0 = euler[:, 0]/np.max(euler[:, 0])

tmp1 = .3*np.ones(euler.shape[0])
# tmp1 = euler[:, 1]/np.max(euler[:, 1])

# tmp2 = 0*np.ones(euler.shape[0])
tmp2 = euler[:, 2]/np.max(euler[:, 2])


ax = fig.add_subplot(111, projection='3d')

colors = np.transpose(np.array([tmp0, tmp1, tmp2]))
print colors.shape

# plt.scatter(X_pc[:, 0], X_pc[:, 2], c=colors)
# Axes3D.scatter(X_pc[:, 0], X_pc[:, 2], X_pc[:, 3], c=colors)
ax.scatter(X_pc[::10, 0], X_pc[::10, 1], X_pc[::10, 2])


ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_zlabel("PC3")
ax.set_title("$|\epsilon_{t}|$ vs. $|\epsilon_{p}|$ in PC space")

plt.show()
