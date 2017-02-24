import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors.kde import KernelDensity
from scipy.stats import norm


def normal(X):
    return np.exp(-0.5*X**2)/np.sqrt(2*np.pi)


def getdensKDE(X, X_, bw):
    kde = KernelDensity(kernel='gaussian', bandwidth=bw).fit(X[:, np.newaxis])
    Adens = np.exp(kde.score_samples(X_[:, np.newaxis]))
    Ndens = normal(X_)
    return Adens, Ndens

xmin = -3
xmax = 3
npts = 1000
nsel = 100
mutgt = 1
sigtgt = 0.7

"""generate random points with uniform distribution"""
Xorig = np.random.uniform(low=xmin, high=xmax, size=npts)

# """generate gaussian random points"""
# Xorig = np.random.normal(loc=0, scale=2, size=npts)

# """generate uniformly distributed points"""
# Xorig = np.linspace(xmin, xmax, npts)

Xorig = np.sort(Xorig)
X = Xorig

plt.figure(1)

target_d = norm.pdf(Xorig, loc=mutgt, scale=sigtgt)
plt.plot(Xorig, target_d, 'r-')
maxdens = target_d.max()

# """select closest nsel points to mutgt"""
# dist = np.abs(X-mutgt)
# tmp = np.argsort(dist)[:nsel]

"""randomly select nsel points"""
tmp = np.zeros((npts,), dtype='bool')
tmp[:nsel] = 1
np.random.shuffle(tmp)

sel = X[tmp]
sel = np.sort(sel)

print "current mu: " + str(sel.mean())
print "current sig: " + str(sel.std())

"""remove selected points from X"""
X = np.delete(X, tmp)

Adens = norm.pdf(Xorig, loc=sel.mean(), scale=sel.std())
plt.plot(Xorig, Adens, 'b-')

"""iterate and try and improve the fit"""
"""find the maximum differences between the histogram and target probability
densities"""

olderr = 1.
# for ii in xrange(X.size):
for ii in xrange(100):

    # if np.mod(ii, 5) == 0:
    #     # plt.plot(Xorig, y, 'r-')
    #     # plt.plot(sel, 0*np.ones(sel.shape), 'k.')
    #     plt.plot(Xorig, Adens, 'k-', alpha=0.5)
    #     # plt.show()

    err = Adens - target_d

    newerr = np.max(np.abs(err))/maxdens
    if newerr < olderr:
        selbest = np.sort(sel)
        olderr = newerr

    """remove point in sel closest to location of max error and add
    point from the original distribution with the miniumum error"""
    """add a bit of noise to this calculation"""

    tmp = np.arange(err.size)[err > 0]
    tmp = tmp[np.random.random_integers(0, tmp.size-1)]
    tmpmax = np.argmin(np.abs(sel-Xorig[tmp]))

    tmp = np.arange(err.size)[err < 0]
    tmp = tmp[np.random.random_integers(0, tmp.size-1)]
    tmpmin = np.argmin(np.abs(X-Xorig[tmp]))

    # tmpmax = np.argmin(np.abs(sel-Xorig[np.argmax(err)]))
    # tmpmin = np.argmin(np.abs(X-Xorig[np.argmin(err)]))

    # print ii
    # print sel[tmpmax]
    # print X[tmpmin]

    oldv = sel[tmpmax]
    sel[tmpmax] = X[tmpmin]
    sel = np.sort(sel)

    X = np.delete(X, tmpmin)
    X = np.append(X, oldv)

    # print X.size

    Adens = norm.pdf(Xorig, loc=sel.mean(), scale=sel.std())

print np.unique(selbest).size

Adens = norm.pdf(Xorig, loc=selbest.mean(), scale=selbest.std())
plt.plot(selbest, -0.05*np.ones(selbest.shape), 'k.')
plt.plot(Xorig, Adens, 'k-')

print "current mu: " + str(selbest.mean())
print "current sig: " + str(selbest.std())

plt.show()
