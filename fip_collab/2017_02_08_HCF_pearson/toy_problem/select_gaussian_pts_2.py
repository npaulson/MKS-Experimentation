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

xmin = -2
xmax = 4
npts = 1000
nsel = 100
mutgt = 0
sigtgt = 0.5

X = np.random.uniform(low=xmin, high=xmax, size=npts)
X = np.sort(X)

plt.figure(1)
plt.plot(X, norm.pdf(X, loc=mutgt, scale=sigtgt), 'r-')


"""select closest nsel points to mutgt"""
dist = np.abs(X-mutgt)
tmp = np.argsort(dist)[:nsel]

sel = X[tmp]
print X.shape
X = np.delete(X, tmp)
print X.shape

hist, bin_edges = np.histogram(sel, bins=50, range=(xmin, xmax), density=True)
binw = bin_edges[1] - bin_edges[0]
bin_centers = bin_edges[:-1]+0.5*binw

plt.plot(bin_centers, hist, 'b-')
# plt.hist(sel, bins=50, normed=1, alpha=0.1, range=(xmin, xmax))
# plt.plot(X, -.01*np.ones(X.shape), marker='.', markersize=10, color='k', alpha=0.3)

"""iterate and try and improve the fit"""
"""find the maximum differences between the histogram and target probability
densities"""

print "current mu: " + str(sel.mean())
print "current sig: " + str(sel.std())

print sel.shape
target_d = norm.pdf(bin_centers, loc=mutgt, scale=sigtgt)
err = hist - target_d

maxerr = np.argmax(err)
minerr = np.argmin(err)


"""remove point in sel closest to bin center with max error and replace
it with a point from the original distribution closest to bin center
with min error"""
tmpmax = np.argmin(np.abs(sel-bin_centers[maxerr]))
tmpmin = np.argmin(np.abs(X-bin_centers[minerr]))

sel[tmpmax] = X[tmpmin]

hist, bin_edges = np.histogram(sel, bins=50, range=(xmin, xmax), density=True)
binw = bin_edges[1] - bin_edges[0]
bin_centers = bin_edges[:-1]+0.5*binw

plt.plot(bin_centers, hist, 'k-')

print "current mu: " + str(sel.mean())
print "current sig: " + str(sel.std())

plt.show()
