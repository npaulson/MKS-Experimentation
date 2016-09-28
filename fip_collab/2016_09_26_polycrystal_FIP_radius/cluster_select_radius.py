import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.cm as cm


n_pts = 100
n_pts_hlf = np.floor(n_pts/2.)

rawdata_ = np.zeros((n_pts, 2))
rawdata_[:, 0] = np.random.normal(loc=0,
                                  scale=1+np.random.rand(),
                                  size=n_pts)
rawdata_[:, 1] = np.random.normal(loc=0,
                                  scale=1+np.random.rand(),
                                  size=n_pts)

"""rotate the cluster"""
ang = 2*np.pi*np.random.rand()
rmat = np.array([[np.cos(ang), -np.sin(ang)],
                 [np.sin(ang), np.cos(ang)]])

rawdata = np.einsum('ij,jk', rawdata_, rmat)

"""plot the cluster"""

plt.plot(rawdata[:, 0], rawdata[:, 1],
         marker='o', markersize=5, color='k',
         linestyle='', alpha=.2)

"""Arbitrarily pick point in the cluster"""

I_seed = np.random.randint(n_pts)

seed = rawdata[I_seed, :]

plt.plot(seed[0], seed[1],
         marker='s', markersize=7, color='r',
         linestyle='', alpha=.3)

"""select set of points within specified radius of seed"""
dist = np.zeros((n_pts,))
for ii in xrange(n_pts):
    point = rawdata[ii, :]
    dist[ii] = np.sqrt(np.sum((seed-point)**2))

I_set = dist < 2.0
set = rawdata[I_set, :]

"""plot the set"""
plt.plot(set[:, 0], set[:, 1],
         marker='o', markersize=5, color='r',
         linestyle='', alpha=.3)

plt.margins(.05)
plt.axis('equal')

plt.show()
