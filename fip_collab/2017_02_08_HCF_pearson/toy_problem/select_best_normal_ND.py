import numpy as np
import scipy.stats as ss
from sklearn.cluster import KMeans


def m_radius(z, mu, Sig):
    """mahalanobis find the mahalanobis radius for a point z
    for a multivariate normal distribution with mean mu and
    covariance matrix Sig.
    * z and mu must be vectors
    * Sig must be a 2d array"""
    zmmu = z - mu
    SigI = np.linalg.inv(Sig)
    return np.sqrt(np.einsum('...i,ij,...j', zmmu, SigI, zmmu))


# np.random.seed(6)

"""initialize randomly distributed points in square"""
sl = 3  # side length of square
n_pts = np.int64(1e6)
ndim = 5
rawdata = sl*(np.random.random((n_pts, ndim))-0.5*np.ones((ndim,)))
n_sel = 100  # number of seeds to identify
n_bin = 3
stdmax = 4


"""selec target statistics for new point cloud"""
sig = 0.05 + 0.35*np.random.random((ndim,))
Sig = np.diag(sig**2)
mu = np.zeros((ndim,))

"""figure out the probability that a random point will
further away from the mean than each point"""
r = m_radius(rawdata, mu, Sig)
cdf = ss.chi2.cdf(r**2, df=ndim, loc=0, scale=1)

"""select the bin edges (for the hypersphere) such that they are equally
spaced"""
binr = np.linspace(0, stdmax, n_bin+1)
bine = ss.chi2.cdf(binr**2, df=ndim, loc=0, scale=1)
print np.round(binr, 2)
print np.round(bine, 2)

"""identify the point ids for points within certain probability bins"""
ptbins = []

for ii in xrange(n_bin):
    tmp1 = cdf >= bine[ii]
    tmp2 = cdf < bine[ii+1]
    idx = tmp1*tmp2
    pts = np.sum(idx)

    ptbins += [np.arange(n_pts)[idx]]

    p1 = np.round(bine[ii], 2)
    p2 = np.round(bine[ii+1], 2)
    print "points in %s-%s bin: %s" % (p1, p2, pts)

"""use K-Means to identify best target points"""
selected = np.zeros((n_sel, ndim))
nn_ = 0
for ii in xrange(n_bin):
    tmp = ptbins[ii]
    inc = np.int16(np.round(n_sel*(bine[ii+1]-bine[ii])))
    nn = nn_
    nn_ = nn + inc
    print "\n"
    print inc
    print nn_

    kmeans = KMeans(n_clusters=inc).fit(rawdata[tmp, :])
    seeds = kmeans.cluster_centers_

    selected[nn:nn_, :] = seeds

"""output the mean and standard deviation of the selected points"""
tmp = str(np.round(sig, 3))
print 'target std. dev.: %s' % tmp
tmp = str(np.round(np.std(selected, 0), 3))
print 'std. dev. of selected points: %s' % tmp
tmp = str(np.round(np.mean(selected, 0), 3))
print 'mean of selected points: %s' % tmp
