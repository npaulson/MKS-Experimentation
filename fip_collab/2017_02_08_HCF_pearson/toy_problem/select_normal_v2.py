import numpy as np
import scipy.stats as ss
from scipy.optimize import brentq
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def m_radius(z, mu, Sig):
    """mahalanobis find the mahalanobis radius for a point z
    for a multivariate normal distribution with mean mu and
    covariance matrix Sig.
    * z and mu must be vectors
    * Sig must be a 2d array"""
    zmmu = z - mu
    SigI = np.linalg.inv(Sig)
    return np.sqrt(np.einsum('...i,ij,...j', zmmu, SigI, zmmu))


def spheroid_vol(R, ndim):
    return np.pi*R**2


# np.random.seed(6)

"""initialize randomly distributed points in square"""
sl = 2  # side length of square
rawdata = sl*np.random.random((1000, 2))-np.array([[sl/2., sl/2.]])
n_pts = 1000
n_sel = 100
dof = 2  # number of spatial dimensions
rawdata = rawdata[:n_pts, :]

"""plot intial points"""
fig = plt.figure()
plt.scatter(rawdata[:, 0], rawdata[:, 1],
            s=20, c='k', edgecolors=None,
            linewidths=0.0, alpha=0.15,
            label='original')

"""select target statistics for new point cloud"""
Sig = np.diag(np.array([.4, .2])**2)
mu = np.array([0, 0])

"""figure out the probability that a random point will
further away from the mean than each point"""
r = m_radius(rawdata, mu, Sig)
cdf = ss.chi2.cdf(r**2, df=dof, loc=0, scale=1)

"""select the bin edges (for the hypersphere) such that each annulus
has equal volume"""
n_bin = 10
binr = np.zeros((n_bin+1,))
rtmp = ss.chi2.ppf(np.array([.7]), df=1, loc=0, scale=1)
print rtmp
Vtgt = spheroid_vol(rtmp, ndim=dof)

for ii in xrange(1, n_bin+1):

    g = lambda R2: spheroid_vol(R2, 2)-spheroid_vol(binr[ii-1], 2)-Vtgt
    binr[ii] = brentq(g, binr[ii-1], binr[ii-1]+rtmp)

print binr
bine = ss.chi2.cdf(binr**2, df=dof, loc=0, scale=1)
print bine

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

"""plot which point is in which bin"""
colormat = cm.plasma(np.linspace(0, 1, n_bin))

for ii in xrange(n_bin):
    tmp = rawdata[ptbins[ii], :]

    p1 = np.round(bine[ii], 2)
    p2 = np.round(bine[ii+1], 2)
    plt.scatter(tmp[:, 0], tmp[:, 1],
                s=20, c=colormat[ii, :], edgecolors=None,
                linewidths=0.0, alpha=0.7,
                label='%s-%s CDF bin' % (p1, p2))

"""randomly select the correct number of points from each bin"""
selected = np.zeros((n_sel, dof))
nn_ = 0
for ii in xrange(n_bin):
    tmp = ptbins[ii]
    np.random.shuffle(tmp)

    inc = np.int16(np.round(n_sel*(bine[ii+1]-bine[ii])))
    nn = nn_
    nn_ = nn + inc
    print nn
    print nn_
    selected[nn:nn_, :] = rawdata[tmp[:inc], :]

"""mark the selected points"""
plt.scatter(selected[:, 0], selected[:, 1],
            marker='x', s=40, c='k', edgecolors=None,
            linewidths=2.0, alpha=0.7,
            label='selected points')

"""output the mean and standard deviation of the selected points"""
print 'mean of selected points: %s' % str(np.mean(selected, 0))
print 'std. dev. of selected points: %s' % str(np.std(selected, 0))

tgt = 0.5
plt.axis(tgt*np.array([-sl, sl, -sl, sl]))

plt.axes().set_aspect('equal')
plt.legend(loc='upper right', shadow=True, fontsize='medium', ncol=1)
fig.tight_layout()

plt.show()
