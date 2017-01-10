import numpy as np
import h5py
import pymks
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.decomposition import PCA


"""load data"""
f = h5py.File('digits.hdf5', 'r')
X = f.get('X')[...]
y = f.get('y')[...]
f.close()

ns = y.size
nf = X.shape[1]
el = np.int16(np.sqrt(nf))
n_dig = len(np.unique(y))
n_p_dig = ns/n_dig

"""rescale X"""
Xmin = np.amin(X, axis=1)[:, None]
Xmax = np.amax(X, axis=1)[:, None]
X = (X-Xmin)/(Xmax-Xmin)

"""compute spatial statistics"""
tmp = X.reshape([ns, el, el])
p_basis = pymks.PrimitiveBasis(n_states=2)
X_auto = pymks.stats.autocorrelate(tmp, p_basis, periodic_axes=(0, 1))

sn = 3200

plt.subplot(121)
ax = plt.imshow(tmp[sn, :, :].T, origin='upper',
                interpolation='none', cmap='magma')
plt.colorbar(ax)
plt.subplot(122)
ax = plt.imshow(X_auto[sn, :, :, 1].T, origin='upper',
                interpolation='none', cmap='magma')
plt.colorbar(ax)

plt.show()

X_auto = X_auto[..., 0].reshape([ns, nf])

"""perform PCA"""
n_components = 10

pca = PCA(n_components=n_components)
pca.fit(X_auto)
reduced = pca.transform(X_auto)

"""plot in PC space"""

colormat = cm.rainbow(np.linspace(0, 1, n_dig))

pcA = 0
pcB = 2

for ii in xrange(n_dig):

    stt = ii*n_p_dig
    end = (ii+1)*n_p_dig

    plt.plot(reduced[stt:end, pcA], reduced[stt:end, pcB],
             marker='o', markersize=6, color=colormat[ii, :],
             alpha=0.4, linestyle='', label=ii)

plt.legend(loc='upper right', shadow=True, fontsize='small', ncol=1)
plt.show()
