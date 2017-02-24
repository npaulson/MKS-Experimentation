import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt
import matplotlib.cm as cm
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
n_pts = 10000
rawdata = sl*np.random.random((n_pts, 2))-np.array([[sl/2., sl/2.]])
n_sel = 100
dof = 2  # number of spatial dimensions
n_bin = 3

"""plot intial points"""
fig = plt.figure()
plt.scatter(rawdata[:, 0], rawdata[:, 1],
            c='k',
            alpha=0.15, edgecolors=None,
            marker='o', s=20, lw=0.0,
            label='original')


"""select target statistics for new point cloud"""
Sig = np.diag(np.array([.4, .2])**2)
mu = np.array([0, 0])

"""figure out the probability that a random point will
further away from the mean than each point"""
r = m_radius(rawdata, mu, Sig)
cdf = ss.chi2.cdf(r**2, df=dof, loc=0, scale=1)

"""select the bin edges (for the hypersphere) such that they are equally
spaced"""
binr = np.linspace(0, 3, n_bin+1)
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
for ii in xrange(n_bin):
    tmp = rawdata[ptbins[ii], :]

    p1 = np.round(bine[ii], 2)
    p2 = np.round(bine[ii+1], 2)
    plt.scatter(tmp[:, 0], tmp[:, 1],
                c=ii*np.ones(tmp.shape[0]), cmap='plasma',
                vmin=0, vmax=n_bin-1,
                alpha=0.3, edgecolors=None,
                marker='o', s=20, lw=0.0,
                label='%s-%s CDF bin' % (p1, p2))

"""use K-Means to identify best target points"""
selected = np.zeros((n_sel, dof))
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

    plt.scatter(seeds[:, 0], seeds[:, 1],
                c=ii*np.ones(inc), cmap='plasma',
                vmin=0, vmax=n_bin-1,
                alpha=1.0, edgecolors=None,
                marker='x', s=40, lw=2.0)

"""output the mean and standard deviation of the selected points"""
print 'mean of selected points: %s' % str(np.mean(selected, 0))
print 'std. dev. of selected points: %s' % str(np.std(selected, 0))

tgt = 0.5
plt.axis(tgt*np.array([-sl, sl, -sl, sl]))

plt.axes().set_aspect('equal')
plt.legend(loc='upper right', shadow=True, fontsize='medium', ncol=1)
fig.tight_layout()

plt.show()
