import numpy as np
import functions as rr
from constants import const
import scipy.stats as ss
import sklearn.metrics as sm
from sklearn import linear_model
import h5py
import time


def fit_gamma_robust(tail):
    r2s = []
    diff_stats = []
    s_f = 0.8

    for j in range(2):
        if j == 0:
            stats = ss.gamma.fit(tail, a=s_f, floc=np.min(tail)*.999)
        else:
            stats = ss.gamma.fit(tail, fa=s_f)
        # x_old = np.linspace(np.min(tail), np.max(tail), 100)
        # x = np.log(x_old)
        cdf = (np.arange(len(tail)) + 1) / float(len(tail))
        pred_ys = ss.gamma.cdf(tail, *stats)
        # tail_log = np.log(tail)
        r2 = sm.r2_score(pred_ys, cdf)
        temp_stats = (len(tail),) + stats + (r2,)
        r2s.append(r2)
        diff_stats.append(temp_stats)

    if r2s[0] > r2s[1]:
        return diff_stats[0][1:4]

    return diff_stats[1][1:4]


def resp(ns, set_id):

    start = time.time()

    C = const()

    f1 = h5py.File("raw_responses.hdf5", 'r')
    rawfip = f1.get('fip_%s' % set_id)

    f2 = h5py.File("responses.hdf5", 'a')

    # c0 = f2.create_dataset('c0_%s' % set_id, (ns,), dtype='float64')
    # c1 = f2.create_dataset('c1_%s' % set_id, (ns,), dtype='float64')
    # c2 = f2.create_dataset('c2_%s' % set_id, (ns,), dtype='float64')

    # for sn in xrange(ns):
    #     x = np.sort(rawfip[sn, :])
    #     x = x[np.int64(C['pcnt']*x.size):, None]
    #     gamma_stats = fit_gamma_robust(x)
    #     c0[sn] = gamma_stats[0]
    #     c1[sn] = gamma_stats[1]
    #     c2[sn] = gamma_stats[2]

    c0 = f2.create_dataset('c0_%s' % set_id, (ns,), dtype='float64')
    c1 = f2.create_dataset('c1_%s' % set_id, (ns,), dtype='float64')
    c2 = f2.create_dataset('c2_%s' % set_id, (ns,), dtype='float64')

    n_p = 3

    for sn in xrange(ns):
        x = np.sort(rawfip[sn, :])
        y = (np.arange(x.size)+1)/np.float32(x.size)
        xl = np.log(x)

        xlmax = xl.max()
        xlmin = xl.min()
        L_p = xlmax-xlmin

        X = np.zeros((x.size, n_p), dtype='float64')

        for ii in xrange(n_p):
            X[:, ii] = np.squeeze(np.cos((ii*np.pi*(xl-xlmin))/L_p))

        # clf = linear_model.LinearRegression()
        # clf.fit(X, y)
        # coef = clf.coef_

        XhX = np.dot(X.T, X)
        Xhy = np.dot(X.T, y)
        coef = np.linalg.lstsq(XhX, Xhy)[0]

        c0[sn] = coef[0]
        c1[sn] = coef[1]
        c2[sn] = coef[2]

        # tmp = np.sort(rawfip[sn, :])
        # c1[sn] = tmp[-43:].mean()

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
