import numpy as np
import functions as rr
from constants import const
import scipy.stats as ss
import sklearn.metrics as sm
from sklearn.decomposition import PCA
import h5py
import time
from numpy.random import multivariate_normal as mn
import matplotlib.pyplot as plt


def fit_gamma_robust(tail):
    s_f = 0.8

    # fit 4 (alternate)
    stats = ss.gamma.fit(tail, fa=s_f, floc=np.min(tail)*.99999)

    # calculate the r**2 for the CDF fit
    cdf = (np.arange(len(tail)) + 1) / float(len(tail))
    pred_ys = ss.gamma.cdf(tail, *stats)
    r2 = sm.r2_score(pred_ys, cdf)

    # otherwise return the second set of parameters
    return stats, r2


def resp(fip_sample, ns):

    C = const()

    rawfip = fip_sample.reshape((ns*C['el']**3,))
    x = np.sort(rawfip)
    x = x[np.int64(C['pcnt']*x.size):, None]

    gamma_stats, r2 = fit_gamma_robust(x)

    mu = gamma_stats[1]
    sigma = gamma_stats[2]

    return x, mu, sigma, r2


def sample(ns, sid):

    C = const()

    start = time.time()

    f1 = h5py.File("raw_responses.hdf5", 'r')
    allfip = f1.get('fip_%s' % sid)[...]
    f1.close()

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'r')
    reduced = f_red.get('reduced_%s' % sid)[...]
    f_red.close()

    f2 = h5py.File("sample_L%s.hdf5" % C['H'], 'a')

    mu = f2.create_dataset("mu_%s" % sid, (C['n_sc'],), dtype='float32')
    sigma = f2.create_dataset("sigma_%s" % sid, (C['n_sc'],), dtype='float32')
    r2 = f2.create_dataset("r2_%s" % sid, (C['n_sc'],), dtype='float32')
    samp = f2.create_dataset("samp_%s" % sid,
                             (C['n_sc'], C['n_samp'], C['n_pc_tot']),
                             dtype='float32')

    for sc in xrange(C['n_sc']):

        """extract indices of selected subsample"""
        samp_, fip_ = select_sample(reduced, allfip)

        # """idenfify closest n_cluster points to seed"""
        # samp_ = reduced[sort_inx, :]
        # fip_ = allfip[sort_inx, :]

        # """find the fip evd and parameters for samp1"""
        # evd_, mu_, sigma_, r2_ = resp(fip_, C['n_samp'])

        # """write to the data summary file"""
        # mu[sc] = np.log(mu_)
        # sigma[sc] = np.log(sigma_)
        # r2[sc] = r2_
        # samp[sc, ...] = samp_
        # f2.create_dataset('evd%s_%s' % (sc, sid),
        #                   data=evd_)

    f2.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'samples extracted for %s: %s seconds' \
          % (sid, timeE)
    rr.WP(msg, C['wrt_file'])


def select_sample(reduced, allfip):

    """perform PCA on the original point cloud to find the directions of
    maximum variance"""
    n_components = 100
    pca = PCA(n_components=n_components)
    red = pca.fit_transform(reduced)

    """find the std. dev. of the original point cloud in each dimension
    the means are all zero due to the PCA algorithm"""
    sig = np.std(red, 0)

    """randomly select the mean and std. dev. of the new point cloud."""
    mu_ = (2*np.random.rand(n_components)-1)*sig
    sig_ = 0.5*(sig+np.random.rand(n_components)*(sig-np.abs(mu_)))

    """generate the new point cloud"""
    target = mn(mean=mu_, cov=np.diag(sig_**2), size=C['n_samp'])

    """identify closest original points to each target point
    each time an original point is selected remove it from the pool so
    that points are not double counted. Randomly selelect target points
    so that there is no bias."""

    samp_ = np.zeros(target.shape)
    fip_ = np.zeros((C['n_samp'], allfip.shape[1],))
    red_ = red
    allfip_ = allfip

    for ii in xrange(C['n_samp']):
        dist = np.sum((red_-target[ii, :])**2, 1)
        indx = np.argmin(dist)

        samp_[ii, :] = red_[indx, :]
        fip_[ii, :] = allfip_[indx, :]

        red_ = np.delete(red_, indx, axis=0)
        allfip_ = np.delete(allfip_, indx, axis=0)

        x = np.array([target[ii, 0], samp_[ii, 0]])
        y = np.array([target[ii, 1], samp_[ii, 1]])
        plt.plot(x, y, 'r:')

    plt.scatter(red[:, 0], red[:, 1],
                marker='o', s=20,
                color='k', linewidths=0.0, edgecolors=None, alpha=.3)

    plt.scatter(target[:, 0], target[:, 1],
                marker='s', s=15,
                color='b', linewidths=0.0, edgecolors=None, alpha=.5)

    plt.scatter(samp_[:, 0], samp_[:, 1],
                marker='x', s=40, c='r', edgecolors=None,
                linewidths=1.0, alpha=0.5,
                label='selected')

    plt.axes().set_aspect('equal')
    plt.tight_layout()
    plt.show()

    # while np.any(err) > 0.5:
    #     indx = np.zeros((C['n_samp'],))

    return samp_, fip_


if __name__ == '__main__':
    C = const()
    ns = C['ns'][0]
    sid = C['sid'][0]

    f2 = h5py.File("sample_L%s.hdf5" % C['H'], 'w')
    f2.close()

    sample(ns, sid)
