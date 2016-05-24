# -*- coding: utf-8 -*-
import functions as rr
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import sklearn.metrics as sm
from constants import const
import h5py
import sys


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


def pltevd(sn, set_id):

    C = const()

    """get the x, y data for plotting the evd"""

    f = h5py.File("raw_responses.hdf5", 'r')
    rawfip = f.get('fip_%s' % set_id)

    x = np.sort(rawfip[sn, :])
    x = x[np.int64(C['pcnt']*x.size):, None]
    y = (np.arange(x.size)+1)/np.float32(x.size)

    f.close

    """retrieve the coefficients"""

    f = h5py.File("responses.hdf5", 'a')
    c0 = f.get('c0_%s' % set_id)[sn]
    c1 = f.get('c1_%s' % set_id)[sn]
    c2 = f.get('c2_%s' % set_id)[sn]
    f.close()

    """plot the original data and the fits"""

    plt.figure()

    plt.plot(np.log(x), y, 'b.', markersize=3)

    tmp = np.linspace(np.log(x).min(), np.log(x).max(), 100)
    x_ = np.exp(tmp)

    plt.plot(np.log(x_), ss.gamma.cdf(x_, c0, loc=c1, scale=c2),
             'r-', lw=2, label='gamma cdf')

    ymin = y.min()
    ymax = y.max()
    rng = ymax - ymin
    ymin += -0.1*rng
    ymax += 0.1*rng

    plt.ylim((ymin, ymax))

    plt.show()


if __name__ == '__main__':

    sn = np.int16(sys.argv[1])
    set_id = sys.argv[2]
    pltevd(sn, set_id)
