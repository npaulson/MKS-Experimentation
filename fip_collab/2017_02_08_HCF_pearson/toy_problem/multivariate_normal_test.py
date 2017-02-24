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

Sig = np.diag(np.array([3, 1])**2)
mu = np.array([[0, 0]])
z = np.array([[3, 0], [0, 1], [3, 1]])

r = m_radius(z, mu, Sig)

print Sig
print z
print r

Sig = np.array([[4]])
mu = np.array([0])
z = np.array([1])
print m_radius(z, mu, Sig)

"""check the multivariate normal CDF against the standard normal CDF for
one dimension. Specifically check at which intervals from the mean the
specified percentage of the PDF is captured"""
print np.sqrt(ss.chi2.ppf(np.array([.7, .8, .9]), df=1, loc=0, scale=1))
print ss.norm.ppf(np.array([.7+.3/2., .8+.2/2., .9+.1/2.]), loc=0, scale=1)

"""check the multivariate normal CDF against the standard normal CDF for
one dimension. Note that the CDFs are for an interval of +- r from the
mean of the normal distribution. Also plot the higher dimension
normal distributions"""
plt.figure()

dofmax = 5

r = np.linspace(0, 3, 1000)
colormat = cm.plasma(np.linspace(0.1, 0.9, dofmax))

plt.plot(r, ss.norm.cdf(r, loc=0, scale=1)-ss.norm.cdf(-1*r, loc=0, scale=1),
         color=[0, 0, 0], alpha=0.7,
         linestyle='--', linewidth=3,
         label='Direct CDF, dof: 1')

for dof in xrange(1, dofmax+1):

    cdf = ss.chi2.cdf(r**2, df=dof, loc=0, scale=1)
    plt.plot(r, cdf,
             marker='',
             color=colormat[dof-1, :], alpha=0.7,
             linestyle='-', linewidth=2,
             label='dof: %s' % dof)

plt.legend(loc='upper left', shadow=True, fontsize='medium', ncol=1)
plt.tight_layout()

plt.show()
