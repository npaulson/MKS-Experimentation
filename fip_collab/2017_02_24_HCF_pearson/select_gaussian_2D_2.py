import numpy as np
import matplotlib.pyplot as plt
from numpy.random import multivariate_normal as mnR
from scipy.stats import multivariate_normal as mnP
from sklearn.neighbors.kde import KernelDensity


def normal(X):
    return np.exp(-0.5*X**2)/np.sqrt(2*np.pi)


def getdensKDE(X, X_, bw):
    kde = KernelDensity(kernel='gaussian', bandwidth=bw).fit(X)
    Adens = np.exp(kde.score_samples(X_))
    Ndens = normal(X_)
    return Adens, Ndens

# np.random.seed(0)

ncld = 200
nsel = 100
dof = 2

"""generate the original point cloud"""
var = np.array([3, 1])**2
Xorig = mnR(mean=np.array([0, 0]), cov=np.diag(var), size=ncld)

plt.scatter(Xorig[:, 0], Xorig[:, 1],
            marker='o', s=20,
            color='k', linewidths=0.0, edgecolors=None, alpha=.3)

"""randomly select a secondary point cloud"""
mu = np.mean(Xorig, 0)
sig = np.std(Xorig, 0)

mu_ = mu + (2*np.random.rand(2)-1)*sig
sig_ = 0.5*(sig+np.random.rand(2)*(sig-np.abs(mu_-mu)))

"""generate the new point cloud"""

"""randomly select nsel points"""
tmp = np.zeros((ncld,), dtype='bool')
tmp[:nsel] = 1
np.random.shuffle(tmp)
sel = Xorig[tmp, :]

"""remove selected points from X"""
X = Xorig
X = np.delete(X, np.arange(ncld)[tmp], axis=0)

for ii in xrange(ncld):

    bw = sel.std()*(0.25*nsel*(dof+2.))**(-1./(dof+4.))
    Adens, Ndens = getdensKDE(sel, Xorig, np.random.uniform(0.05, 0.5)*bw)
    # Adens, Ndens = getdensKDE(sel, Xorig, 0.33*bw)

    target_d = mnP.pdf(Xorig, mean=mu_, cov=np.diag(sig_**2))
    err = Adens - target_d

    """remove point in sel closest to location of max error and add
    point from the original distribution with the miniumum error"""
    dist1 = np.sqrt(np.sum((sel-Xorig[np.argmax(err), :])**2, 1))
    tmpmax = np.argmin(dist1)
    dist2 = np.sqrt(np.sum((X-Xorig[np.argmin(err), :])**2, 1))
    tmpmin = np.argmin(dist2)

    oldv = np.copy(sel[tmpmax, :])
    sel[tmpmax, :] = X[tmpmin, :]

    X = np.delete(X, tmpmin, axis=0)
    X = np.append(X, oldv[None, :], axis=0)

plt.scatter(sel[:, 0], sel[:, 1],
            marker='x', s=40, c='r', edgecolors=None,
            linewidths=1.0, alpha=0.5,
            label='selected')

print "desired mean: " + str(mu_)
print "desired std. dev.: " + str(sig_)
print "selected mean: " + str(np.mean(sel, 0))
print "selected std. dev.: " + str(np.std(sel, 0))

x_min, x_max = Xorig[:, 0].min() - 1, Xorig[:, 0].max() + 1
y_min, y_max = Xorig[:, 1].min() - 1, Xorig[:, 1].max() + 1
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

plt.axes().set_aspect('equal')
plt.tight_layout()

plt.show()
