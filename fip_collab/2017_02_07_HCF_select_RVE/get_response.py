import numpy as np
import functions as rr
from constants import const
import scipy.stats as ss
import sklearn.metrics as sm
import h5py
import time


# def fit_gamma_robust(tail):
#     r2s = []
#     diff_stats = []
#     s_f = 0.8

#     for j in range(2):
#         if j == 0:
#             stats = ss.gamma.fit(tail, a=s_f, floc=np.min(tail)*.999)
#             print "j==0"
#         else:
#             stats = ss.gamma.fit(tail, fa=s_f)
#             print "j!=0"
#         # x_old = np.linspace(np.min(tail), np.max(tail), 100)
#         # x = np.log(x_old)
#         cdf = (np.arange(len(tail)) + 1) / float(len(tail))
#         pred_ys = ss.gamma.cdf(tail, *stats)
#         # tail_log = np.log(tail)
#         r2 = sm.r2_score(pred_ys, cdf)
#         temp_stats = (len(tail),) + stats + (r2,)
#         r2s.append(r2)
#         diff_stats.append(temp_stats)

#     if r2s[0] > r2s[1]:
#         return diff_stats[0][1:4]

#     return diff_stats[1][1:4]


def fit_gamma_robust(tail):
    s_f = 1.16

    # # fit 0 (original)
    # # fix the start location (mu_g) slightly  left of the
    # # lowest tail value. Provide a guess for the shape (alpha)
    # # at s_f
    # stats = ss.gamma.fit(tail, a=s_f, floc=np.min(tail)*.999)

    # # fit 1 (original)
    # # fix the shape as s_f
    # stats = ss.gamma.fit(tail, fa=s_f)

    # # fit 2 (alternate)
    # stats = ss.gamma.fit(tail)

    # # fit 3 (alternate)
    # stats = ss.gamma.fit(tail, fa=s_f, floc=np.min(tail)*.999)

    # # fit 4 (alternate)
    # stats = ss.gamma.fit(tail, fa=s_f, floc=np.min(tail)*.99999)

    # fit 5 (help pick alpha)
    stats = ss.gamma.fit(tail, a=s_f, floc=np.min(tail)*.99999)

    # # fit 5 (help pick alpha)
    # stats = ss.gamma.fit(tail)

    # calculate the r**2 for the CDF fit
    cdf = (np.arange(len(tail)) + 1) / float(len(tail))

    if np.any(np.isnan(stats)):
        stats = (1, 1, 1)
        r2 = 0
    else:
        pred_ys = ss.gamma.cdf(tail, *stats)
        r2 = sm.r2_score(pred_ys, cdf)

    # otherwise return the second set of parameters
    return stats, r2


def resp(ns, ns_max, set_id):

    start = time.time()

    C = const()
    np.random.seed(0)
    rvec = np.arange(ns_max)
    np.random.shuffle(rvec)
    rvec = np.sort(rvec[:ns])

    f1 = h5py.File("raw_responses.hdf5", 'r')
    tmp = f1.get('fip_%s' % set_id)[rvec, :]
    rawfip = tmp.reshape((ns*C['el']**3,))

    f2 = h5py.File("responses.hdf5", 'a')

    x = np.sort(rawfip)

    # cut off by percentage
    x = x[np.int64(C['pcnt']*x.size):, None]

    # # cut off my number of locations
    # x = x[-1000:, None]

    gamma_stats, r2 = fit_gamma_robust(x)

    coefs = f2.get('gamma_coefs')
    coefs[ns-1, :3] = gamma_stats
    coefs[ns-1, 3] = r2

    f2.close()
    f1.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'fips processed for %s, ns %s: %s seconds' \
          % (set_id, ns, timeE)
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    C = const()
    ns = C['ns_cal'][0]
    set_id = C['set_id_cal'][0]

    resp(ns, set_id)
