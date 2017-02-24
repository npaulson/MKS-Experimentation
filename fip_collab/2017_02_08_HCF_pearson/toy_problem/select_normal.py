import numpy as np
import scipy.stats as ss
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

print r[:10]
print cdf[:10]

"""identify the point ids for points within certain probability bins"""
ptbins = []
bine = np.array([0, .1, .2, .3, .4, .5, .6, .7, .8, .9, .99])

for ii in xrange(10):
    tmp1 = cdf >= bine[ii]
    tmp2 = cdf < bine[ii+1]
    idx = tmp1*tmp2
    pts = np.sum(idx)
    print "points in %s-%s bin: %s" % (bine[ii], bine[ii+1], pts)
    ptbins += [np.arange(n_pts)[idx]]

"""plot which point is in which bin"""
colormat = cm.plasma(np.linspace(0, 1, len(ptbins)))

for ii in xrange(len(ptbins)):
    tmp = rawdata[ptbins[ii], :]
    plt.scatter(tmp[:, 0], tmp[:, 1],
                s=20, c=colormat[ii, :], edgecolors=None,
                linewidths=0.0, alpha=0.7,
                label='%s-%s CDF bin' % (bine[ii], bine[ii+1]))

"""randomly select 10 points from each bin"""
selected = np.zeros((n_sel, dof))
for ii in xrange(len(ptbins)):
    tmp = ptbins[ii]
    np.random.shuffle(tmp)
    selected[10*ii:10*(ii+1), :] = rawdata[tmp[:10], :]

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
