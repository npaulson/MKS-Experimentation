import numpy as np
import functions as rr
from constants import const
import scipy.stats as ss
import sklearn.metrics as sm
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


def resp(ns, set_id):

    start = time.time()

    C = const()

    f1 = h5py.File("raw_responses.hdf5", 'r')
    tmp = f1.get('fip_%s' % set_id)[...]
    rawfip = tmp.reshape((ns*C['el']**3,))

    f2 = h5py.File("responses.hdf5", 'a')

    x = np.sort(rawfip)

    x = x[np.int64(C['pcnt']*x.size):, None]
    f2.create_dataset('evd_%s' % set_id, data=x)

    gamma_stats, r2 = fit_gamma_robust(x)

    f2.create_dataset('mu_%s' % set_id, data=gamma_stats[1])
    f2.create_dataset('sigma_%s' % set_id, data=gamma_stats[2])
    f2.create_dataset('r2_%s' % set_id, data=r2)

    f2.close()
    f1.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'fips processed for %s: %s seconds' \
          % (set_id, timeE)
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    C = const()
    ns = C['ns_cal'][0]
    set_id = C['set_id_cal'][0]

    resp(ns, set_id)
