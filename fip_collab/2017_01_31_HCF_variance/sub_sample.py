import numpy as np
import functions as rr
from constants import const
import scipy.stats as ss
import sklearn.metrics as sm
from sklearn.cluster import KMeans
import h5py
import time


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

    """use KMeans to identify subcluster seeds"""
    np.random.seed(3)
    kmeans = KMeans(n_clusters=C['n_sc']).fit(reduced)
    seeds = kmeans.cluster_centers_

    f2 = h5py.File("sample_L%s.hdf5" % C['H'], 'a')

    mu = f2.create_dataset("mu_%s" % sid, (C['n_sc'],), dtype='float32')
    sigma = f2.create_dataset("sigma_%s" % sid, (C['n_sc'],), dtype='float32')
    r2 = f2.create_dataset("r2_%s" % sid, (C['n_sc'],), dtype='float32')
    samp = f2.create_dataset("samp_%s" % sid,
                             (C['n_sc'], C['n_samp'], C['n_pc_tot']),
                             dtype='float32')

    for sc in xrange(C['n_sc']):

        """idenfify closest n_cluster points to seed"""
        dist2seed = np.sqrt(np.sum((reduced - seeds[sc, :])**2, 1))
        sort_inx = np.argsort(dist2seed)[:C['n_samp']]
        samp_ = reduced[sort_inx, :]
        fip_ = allfip[sort_inx, :]

        """find the fip evd and parameters for samp1"""
        evd_, mu_, sigma_, r2_ = resp(fip_, C['n_samp'])

        """write to the data summary file"""
        mu[sc] = np.log(mu_)
        sigma[sc] = np.log(sigma_)
        r2[sc] = r2_
        samp[sc, ...] = samp_
        f2.create_dataset('evd%s_%s' % (sc, sid),
                          data=evd_)

    f2.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'samples extracted for %s: %s seconds' \
          % (sid, timeE)
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    C = const()
    ns = C['ns'][0]
    sid = C['sid'][0]

    f2 = h5py.File("sample.hdf5", 'w')
    f2.close()

    sample(ns, sid)
