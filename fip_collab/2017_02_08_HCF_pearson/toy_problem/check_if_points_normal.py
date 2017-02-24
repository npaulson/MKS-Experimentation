import numpy as np
import scipy.stats as ss


def norm(x, mu, sigma):
    var = sigma**2
    c1 = (2*np.pi*var)**0.5
    c2 = -2*var
    return np.exp((x-mu)**2/c2)/c1


npts = 10000
mu = 0.
sigma = 1.

"""note that the likelyhood, P(X|mu,sigma)
is given by np.prod(norm(X, mu, sigma)). This presents issues
because for many points this product is expected to be
extremely small. Instead, take the log likelyhood which 
may be expressed as follows:
ln(P(X|mu,sigma))=np.sum(np.log(norm(X, mu, sigma)))"""

X = np.random.normal(loc=mu, scale=sigma, size=(npts,))
print ss.normaltest(X)
print np.sum(np.log(norm(X, mu, sigma)))

X = 0.0001*(2.*np.random.random((npts,))-1.)
print ss.normaltest(X)
print np.sum(np.log(norm(X, mu, sigma)))
