import numpy as np
import h5py
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


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

plt.figure(1)
Nvec = np.arange(0, euler.shape[0])
plt.plot(Nvec, euler[:, 0], 'r')
plt.plot(Nvec, euler[:, 1], 'g')
# plt.plot(Nvec, euler[:, 2], 'b')

plt.figure(2, figsize=[14, 10])

# tmp1 = np.linspace(0.0, 1.0, euler.shape[0])
# tmp2 = 0*np.ones(euler.shape[0])
# tmp3 = 0*np.ones(euler.shape[0])

tmp0 = .6*np.ones(euler.shape[0])
#tmp0 = euler[:, 0]/np.max(euler[:, 0])

tmp1 = .3*np.ones(euler.shape[0])
# tmp1 = euler[:, 1]/np.max(euler[:, 1])

#tmp2 = 0*np.ones(euler.shape[0])
tmp2 = euler[:, 2]/np.max(euler[:, 2])

colors = np.transpose(np.array([tmp0, tmp1, tmp2]))
print colors.shape

plt.scatter(X_pc[:, 2], X_pc[:, 3], c=colors)
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("$|\epsilon_{t}|$ vs. $|\epsilon_{p}|$ in PC space")

plt.show()
