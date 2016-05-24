# -*- coding: utf-8 -*-
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


def pltevd(set_id_set):

    C = const()

    colormat = np.array([[.3, .3, 1.],
                         [.3, 1., .3],
                         [1., .2, .2],
                         [0., .7, .7],
                         [.7, .0, .7],
                         [.7, .7, .0],
                         [.5, .3, .1],
                         [.3, .5, .1],
                         [.1, .3, .5]])

    f_reg = h5py.File("regression_results.hdf5", 'r')
    indx_c0 = f_reg.get('maxerr_val_c0')[...].argmin()
    indx_c1 = f_reg.get('maxerr_val_c1')[...].argmin()
    indx_c2 = f_reg.get('maxerr_val_c2')[...].argmin()

    plt.figure(6)

    f = h5py.File("responses.hdf5", 'r')

    for ii in xrange(len(set_id_set)):
        set_id = set_id_set[ii]

        """get the x, y data for plotting the evd"""

        x = f.get('evd_%s' % set_id)[...]

        y = (np.arange(x.size)+1)/np.float32(x.size)

        """retrieve the predicted coefficients"""
        c0 = f_reg.get('Rpred_val_c0')[indx_c0, ii]
        c1 = f_reg.get('Rpred_val_c1')[indx_c1, ii]
        c2 = f_reg.get('Rpred_val_c2')[indx_c2, ii]

        # """retrieve the coefficients for validation"""
        # c0 = f.get('c0_%s' % set_id)[...]
        # c1 = f.get('c1_%s' % set_id)[...]
        # c2 = f.get('c2_%s' % set_id)[...]

        """plot the original data and the fits"""
        plt.plot(np.log(x), y, '.', markersize=3, color=colormat[ii, :])

        tmp = np.linspace(np.log(x).min(), np.log(x).max(), 100)
        x_ = np.exp(tmp)

        plt.plot(np.log(x_), ss.gamma.cdf(x_, c0, loc=c1, scale=c2),
                 '-', color=colormat[ii, :], lw=2, label=set_id)

    f.close()
    f_reg.close()

    plt.xlabel("ln(FIP)")
    plt.ylabel("CDF")
    plt.legend(loc='upper left', shadow=True, fontsize='medium')

    ymin = y.min()
    ymax = y.max()
    rng = ymax - ymin
    ymin += -0.1*rng
    ymax += 0.1*rng

    plt.ylim((ymin, ymax))


if __name__ == '__main__':
    set_id = sys.argv[1]
    pltevd(set_id)
    plt.show()
