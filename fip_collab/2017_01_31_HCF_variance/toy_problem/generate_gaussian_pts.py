import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors.kde import KernelDensity


def normal(X):
    return np.exp(-0.5*X**2)/np.sqrt(2*np.pi)


def getdens(X):
    kde = KernelDensity(kernel='gaussian', bandwidth=0.5).fit(X[:, np.newaxis])
    Adens = np.exp(kde.score_samples(X[:, np.newaxis]))
    Ndens = normal(X)

    """plot the various distributions"""
    plt.plot(X, -0.2*np.ones(X.shape), 'k.')
    plt.plot(X, Adens, 'k.')
    plt.plot(X, Ndens, 'ro')

    return Adens, Ndens


xmin = -3
xmax = 3
xrng = xmax-xmin
n_pts = 21
spacing = xrng/np.float32(n_pts)
Xold = np.linspace(xmin, xmax, n_pts)
Adens, Ndens = getdens(Xold)
plt.show()

"""evaluate the difference between estimated and desired densities"""
err = Adens-Ndens

idxmax = np.argmax(err)
idxmin = np.argmin(err)

Xnew = Xold

dist = Xold[idxmin] - Xold

# n_hlf = np.int16(np.floor(n_pts/2.))
# tmp = normal(dist)/normal(0)
# modifier = np.zeros((n_pts,))
# for ii in xrange(n_hlf):
#     modifier[ii] = np.sum(tmp[ii:idxmin])
# for ii in xrange(n_hlf):
#     modifier[n_pts-ii-1] = -np.sum(tmp[ii:idxmin])

modifier = normal(dist)/normal(0)
modifier[idxmin] = 0
modifier[idxmin+1:] = -1*modifier[idxmin+1:]
print modifier

Xnew = Xold + 0.5*spacing*modifier

# Xnew[:idxmin] = Xold[:idxmin] + 0.5*spacing*modifier[:idxmin]
# Xnew[idxmin+1:] = Xold[idxmin+1:] + 0.5*spacing*modifier[:idxmin]

Adens, Ndens = getdens(Xnew)

plt.show()
