import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors.kde import KernelDensity
from scipy.optimize import brentq


def normal(X):
    return np.exp(-0.5*X**2)/np.sqrt(2*np.pi)


def getdens(X):
    kde = KernelDensity(kernel='gaussian', bandwidth=0.01).fit(X[:, np.newaxis])
    Adens = np.exp(kde.score_samples(X[:, np.newaxis]))
    Ndens = normal(X)
    return Adens, Ndens


xmin = -3
xmax = 3
xrng = xmax-xmin
n_pts = 1000
n_hlf = n_pts/2

# binA = 1/np.float32(n_pts+2)
binA = 1/np.float32(2*n_pts)

X = np.zeros(n_pts)
binwV = np.zeros(n_pts)
binSr = 0
binSl = 0
binW = 1
for ii in xrange(n_hlf):

    g = lambda binE: normal((binSr+binE)/2.)*(binE-binSr)-binA

    binE = brentq(f=g, a=binSr, b=binSr+2*binW)

    binW = binE-binSr

    X[n_hlf-1-ii] = binSr + 0.5*binW
    X[n_hlf+ii] = binSl - 0.5*binW
    binSr += binW
    binSl -= binW
    # print ii
    # print binSr
    # print normal(binSr)

X = X/(binA*n_pts)
# print "std(X): " + str(X.std())

"""plot the various distributions"""

Xplt = np.linspace(xmin, xmax, 1000)
Ndens = normal(Xplt)
plt.plot(Xplt, Ndens, 'r-')

# kde = KernelDensity(kernel='gaussian', bandwidth=0.5).fit(X[:, np.newaxis])
# Adens = np.exp(kde.score_samples(Xplt[:, np.newaxis]))
# plt.plot(Xplt, Adens, 'k.')

plt.hist(X, bins=50, normed=1, alpha=0.1, range=(xmin, xmax))
plt.plot(X, -.01*np.ones(X.shape), marker='.', markersize=10, color='k', alpha=0.3)

plt.show()
