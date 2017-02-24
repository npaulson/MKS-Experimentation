import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors.kde import KernelDensity
from scipy.stats import norm


def normal(X):
    return np.exp(-0.5*X**2)/np.sqrt(2*np.pi)


def getdensKDE(X, bw):
    kde = KernelDensity(kernel='gaussian', bandwidth=bw).fit(X[:, np.newaxis])
    Adens = np.exp(kde.score_samples(X[:, np.newaxis]))
    Ndens = normal(X)
    return Adens, Ndens

xmin = -3
xmax = 3
npts = 500
nsel = 100
mutgt = 1
sigtgt = 0.5

Xorig = np.random.uniform(low=xmin, high=xmax, size=npts)
Xorig = np.sort(Xorig)
X = Xorig

plt.figure(1)
y = norm.pdf(Xorig, loc=mutgt, scale=sigtgt)
plt.plot(Xorig, y, 'r-')
maxdens = y.max()

"""select closest nsel points to mutgt"""
dist = np.abs(X-mutgt)
tmp = np.argsort(dist)[:nsel]

sel = X[tmp]
sel = np.sort(sel)

X = np.delete(X, tmp)

bw = ((4./3.)*(sel.std()**5/nsel))**0.2
print bw
Adens, Ndens = getdensKDE(sel, bw)
plt.plot(sel, Adens, 'b-')

"""iterate and try and improve the fit"""
"""find the maximum differences between the histogram and target probability
densities"""

print "current mu: " + str(sel.mean())
print "current sig: " + str(sel.std())

olderr = 1
for ii in xrange(100):

    target_d = norm.pdf(sel, loc=mutgt, scale=sigtgt)
    err = Adens - target_d

    newerr = np.max(np.abs(err))/maxdens
    if newerr < olderr:
        selbest = np.sort(sel)
        olderr = newerr

    """remove point in sel with max error and add point point from
    the original distribution closest to point in sel with min error"""
    tmpmin = np.argmin(np.abs(X-sel[np.argmin(err)]))
    sel[np.argmax(err)] = X[tmpmin]
    sel = np.sort(sel)

    X = np.delete(X, tmpmin)

    bw = ((4./3.)*(sel.std()**5/nsel))**0.2
    Adens, Ndens = getdensKDE(sel, bw)

    plt.plot(Xorig, y, 'r-')
    plt.plot(selbest, 0*np.ones(selbest.shape), 'k.')
    plt.plot(selbest, Adens, 'k-')
    plt.show()

print np.unique(selbest).size

bw = ((4./3.)*(selbest.std()**5/nsel))**0.2
Adens, Ndens = getdensKDE(selbest, bw)
plt.plot(selbest, 0*np.ones(selbest.shape), 'k.')
plt.plot(selbest, Adens, 'k-')

print "current mu: " + str(selbest.mean())
print "current sig: " + str(selbest.std())

plt.show()
