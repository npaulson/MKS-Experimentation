import numpy as np
import matplotlib.pyplot as plt


np.random.seed(6)

"""initialize randomly distributed points in square"""
sl = 2  # side length of square
rawdata = sl*np.random.random((1000, 2))-np.array([[sl/2., sl/2.]])
n_pts = 500
rawdata = rawdata[:n_pts, :]

"""plot intial points"""
fig = plt.figure()
plt.scatter(rawdata[:, 0], rawdata[:, 1],
            s=20, c='k', edgecolors=None,
            linewidths=0.0, alpha=0.15,
            label='original')

"""plot samples from multivariate gaussian distribution in this region"""
n_tgt = 30

targets_ = np.zeros((n_tgt, 2))
targets_[:, 0] = np.random.normal(loc=0,
                                  scale=0.04+.2*np.random.rand(),
                                  size=n_tgt)
targets_[:, 1] = np.random.normal(loc=0,
                                  scale=0.2+0.2*np.random.rand(),
                                  size=n_tgt)

"""rotate the cloud"""
ang = 2*np.pi*np.random.rand()
rmat = np.array([[np.cos(ang), -np.sin(ang)],
                 [np.sin(ang), np.cos(ang)]])

targets = np.einsum('ij,jk', targets_, rmat)

plt.scatter(targets[:, 0], targets[:, 1],
            marker='s', s=30, c='b', edgecolors=None,
            linewidths=0.0, alpha=0.5,
            label='target')

"""identify closest original points to each target point
each time an original point is selected remove it from the pool so
that points are not double counted. Randomly selelect target points
so that there is no bias."""

newpts = np.zeros((n_tgt, 2))
rawdata_ = rawdata

for ii in xrange(n_tgt):
    dist = np.sum((rawdata_-targets[ii, :])**2, 1)
    indx = np.argmin(dist)
    newpts[ii, :] = rawdata_[indx, :]
    rawdata_ = np.delete(rawdata_, indx, axis=0)

    x = np.array([targets[ii, 0], newpts[ii, 0]])
    y = np.array([targets[ii, 1], newpts[ii, 1]])
    plt.plot(x, y, 'r:')

plt.scatter(newpts[:, 0], newpts[:, 1],
            marker='x', s=40, c='r', edgecolors=None,
            linewidths=1.0, alpha=0.5,
            label='selected')

print "covariance of target points:"
print np.cov(targets, rowvar=False)
print "covariance of selected points:"
print np.cov(newpts, rowvar=False)

tgt = 0.5
plt.axis(tgt*np.array([-sl, sl, -sl, sl]))
# xmin = np.min([np.min(targets[:, 0]), np.min(newpts[:, 0])])
# xmax = np.max([np.max(targets[:, 0]), np.max(newpts[:, 0])])
# ymin = np.min([np.min(targets[:, 1]), np.min(newpts[:, 1])])
# ymax = np.max([np.max(targets[:, 1]), np.max(newpts[:, 1])])
# xrng = xmax-xmin
# yrng = ymax-ymin
# fc = 0.2
# plt.axis([xmin-2*fc*xrng, xmax+3*fc*xrng, ymin-fc*yrng, ymax+fc*yrng])

plt.axes().set_aspect('equal')
plt.legend(loc='upper right', shadow=True, fontsize='medium', ncol=1)
fig.tight_layout()

plt.show()
