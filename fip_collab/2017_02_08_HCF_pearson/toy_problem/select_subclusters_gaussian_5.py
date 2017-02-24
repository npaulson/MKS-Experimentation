import numpy as np
import matplotlib.pyplot as plt
from numpy.random import multivariate_normal as mn

n_cloud = 200
n_tgt = 100

"""generate the original point cloud"""
var = np.array([3, 1])**2
original = mn(mean=np.array([0, 0]), cov=np.diag(var), size=n_cloud)

mu = np.mean(original, 0)
sig = np.std(original, 0)

print "original std, PC1: " + str(sig[0])
print "original std, PC2: " + str(sig[1])

plt.scatter(original[:, 0], original[:, 1],
            marker='o', s=20,
            color='k', linewidths=0.0, edgecolors=None, alpha=.3)

"""randomly select a secondary point cloud"""
mu_ = mu + (2*np.random.rand(2)-1)*sig
sig_ = 0.5*(sig+np.random.rand(2)*(sig-np.abs(mu_-mu)))

"""generate the new point cloud"""
target = mn(mean=mu_, cov=np.diag(sig_**2), size=n_tgt)

plt.scatter(target[:, 0], target[:, 1],
            marker='s', s=15,
            color='b', linewidths=0.0, edgecolors=None, alpha=.5)

"""identify closest original points to each target point
each time an original point is selected remove it from the pool so
that points are not double counted. Randomly selelect target points
so that there is no bias."""

newpts = np.zeros((n_tgt, 2))
original_ = original

for ii in xrange(n_tgt):
    dist = np.sum((original_-target[ii, :])**2, 1)
    indx = np.argmin(dist)
    newpts[ii, :] = original_[indx, :]
    original_ = np.delete(original_, indx, axis=0)

    x = np.array([target[ii, 0], newpts[ii, 0]])
    y = np.array([target[ii, 1], newpts[ii, 1]])
    plt.plot(x, y, 'r:')

plt.scatter(newpts[:, 0], newpts[:, 1],
            marker='x', s=40, c='r', edgecolors=None,
            linewidths=1.0, alpha=0.5,
            label='selected')
print "desired std. dev.: "
print sig_
print "std. dev. of target points:"
print np.std(target, 0)
print "std. dev. of selected points:"
print np.std(newpts, 0)

x_min, x_max = original[:, 0].min() - 1, original[:, 0].max() + 1
y_min, y_max = original[:, 1].min() - 1, original[:, 1].max() + 1
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

plt.axes().set_aspect('equal')
plt.tight_layout()

plt.show()
