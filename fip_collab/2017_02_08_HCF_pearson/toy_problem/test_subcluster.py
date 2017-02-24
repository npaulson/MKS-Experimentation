import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import matplotlib.cm as cm
from numpy.random import multivariate_normal as mn


def m_radius(z, mu, Sig):
    """mahalanobis find the mahalanobis radius for a point z
    for a multivariate normal distribution with mean mu and
    covariance matrix Sig.
    * z and mu must be vectors
    * Sig must be a 2d array"""
    zmmu = z - mu
    SigI = np.linalg.inv(Sig)
    return np.sqrt(np.einsum('...i,ij,...j', zmmu, SigI, zmmu))


n_cloud = 200
n_tgt = 100
dof = 2
sigmax = 2

"""generate the original point cloud"""
np.random.seed(0)
var = np.array([1.0 + 2*np.random.rand(), 0.5+0.5*np.random.rand()])**2
original = mn(mean=np.array([0, 0]), cov=np.diag(var), size=n_cloud)

mu = np.mean(original, 0)
sig = np.std(original, 0)

plt.scatter(original[:, 0], original[:, 1],
            marker='o', s=20,
            color='k', linewidths=0.0, edgecolors=None, alpha=.3)

"""randomly select a secondary point cloud"""
np.random.seed()
mu_ = (2*np.random.rand(2)-1)*sig
sig_ = 0.5*(sig+np.random.rand(2)*(sig-np.abs(mu_-mu)))

print "original mean: " + str(mu)
print "desired mean: " + str(mu_)
print "original std. dev.: " + str(sig)
print "desired std. dev.: " + str(sig_)


"""figure out the probability that a random point will
further away from the mean than each point"""
Sig = np.diag(sig_**2)
r = m_radius(original, mu, Sig)
cdf = ss.chi2.cdf(r**2, df=dof, loc=0, scale=1)

"""select the bin edges (for the hypersphere) such that they are equally
spaced"""
n_bin = 3
binr = np.linspace(0, sigmax, n_bin+1)
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

    p1 = np.round(bine[ii], 2)
    p2 = np.round(bine[ii+1], 2)
    inc = np.int16(np.round(n_tgt*(bine[ii+1]-bine[ii])))
    print "%s-%s bin: desired #: %s, actual #: %s" % (p1, p2, inc, pts)

    ptbins += [np.arange(n_cloud)[idx]]

"""plot which point is in which bin"""
colormat = cm.plasma(np.linspace(0, 1, n_bin))

for ii in xrange(n_bin):
    tmp = original[ptbins[ii], :]

    p1 = np.round(bine[ii], 2)
    p2 = np.round(bine[ii+1], 2)
    plt.scatter(tmp[:, 0], tmp[:, 1],
                s=20, c=colormat[ii, :], edgecolors=None,
                linewidths=0.0, alpha=0.7,
                label='%s-%s CDF bin' % (p1, p2))

"""randomly select the correct number of points from each bin"""
selected = np.zeros((n_tgt, dof))
nn_ = 0
for ii in xrange(n_bin):
    tmp = ptbins[ii]
    np.random.shuffle(tmp)

    inc = np.int16(np.round(n_tgt*(bine[ii+1]-bine[ii])))
    nn = nn_
    nn_ = nn + inc

    p1 = np.round(bine[ii], 2)
    p2 = np.round(bine[ii+1], 2)
    print "# points reqired, %s-%s bin: %s" % (p1, p2, inc)

    selected[nn:nn_, :] = original[tmp[:inc], :]

"""mark the selected points"""
plt.scatter(selected[:, 0], selected[:, 1],
            marker='x', s=40, c='k', edgecolors=None,
            linewidths=2.0, alpha=0.7,
            label='selected points')

print "achieved mean: %s" % str(np.mean(selected, 0))
print "achieved std. dev.: %s" % str(np.std(selected, 0))

x_min, x_max = original[:, 0].min() - 1, original[:, 0].max() + 1
y_min, y_max = original[:, 1].min() - 1, original[:, 1].max() + 1
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

plt.axes().set_aspect('equal')
plt.tight_layout()

plt.show()
