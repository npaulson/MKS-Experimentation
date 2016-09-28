import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
# import matplotlib.cm as cm


n_pts = 100
n_pts_hlf = np.floor(n_pts/2.)

rawdata_ = np.zeros((n_pts, 2))
rawdata_[:, 0] = np.random.normal(loc=0,
                                  scale=.1+np.random.rand(),
                                  size=n_pts)
rawdata_[:, 1] = np.random.normal(loc=0,
                                  scale=1.2+np.random.rand(),
                                  size=n_pts)

"""rotate the cluster"""
ang = 2*np.pi*np.random.rand()
rmat = np.array([[np.cos(ang), -np.sin(ang)],
                 [np.sin(ang), np.cos(ang)]])

rawdata = np.einsum('ij,jk', rawdata_, rmat)

"""plot the cluster"""
plt.figure(1)
plt.plot(rawdata[:, 0], rawdata[:, 1],
         marker='o', markersize=5, color='k',
         linestyle='', alpha=.2)

plt.margins(.05)
plt.axis('equal')

"""Isolate the cluster and perform PCA"""
pca = PCA(n_components=2)
pca.fit(rawdata)
data = pca.transform(rawdata)

"""plot the cluster"""
plt.figure(2)
plt.plot(data[:, 0], data[:, 1],
         marker='o', markersize=5, color='b',
         linestyle='', alpha=.2)


"""pick point at edge of cluster"""
I_seed1 = np.argmin(data[:, 0])

seed1 = data[I_seed1, :]
plt.plot(seed1[0], seed1[1],
         marker='s', markersize=7, color='r',
         linestyle='', alpha=.3)

"""Split cluster in half based on distance to seed"""
dist = np.zeros((n_pts,))
for ii in xrange(n_pts):
    point = data[ii, :]
    dist[ii] = np.sqrt(np.sum((seed1-point)**2))

I_sort = np.argsort(dist)
set1 = data[I_sort[:50], :]

"""plt the two sets"""

plt.plot(set1[:, 0], set1[:, 1],
         marker='o', markersize=5, color='r',
         linestyle='', alpha=.3)

plt.margins(.05)
plt.axis('equal')

plt.show()
