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
Xold = np.linspace(xmin, xmax, n_pts)
Adens, Ndens = getdens(Xold)
plt.show()

"""evaluate the difference between estimated and desired densities"""
for ii in xrange(100):

    idx = np.random.randint(n_pts)
    err = Ndens[idx] - Adens[idx]

    dist = Xold[idx] - Xold

    modifier = normal(dist)/normal(0)
    modifier[idx] = 0
    modifier[idx+1:] = -1*modifier[idx+1:]

    if idx == 0:
        spacing = Xold[1] - Xold[0]
    elif idx == n_pts-1:
        spacing = Xold[-1] - Xold[-2]
    else:
        spacing = (Xold[idx+1]-Xold[idx-1])/2.

    print idx
    print spacing

    Xnew = Xold + np.sign(err)*0.5*spacing*modifier
    Xold = Xnew

    Adens, Ndens = getdens(Xnew)
    plt.show()
