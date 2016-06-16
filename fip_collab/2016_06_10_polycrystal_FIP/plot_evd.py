# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import sklearn.metrics as sm
from constants import const
import h5py
import sys


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


def pltevd(set_id_set, indx, pltnum):

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

    plt.figure(pltnum, figsize=[7, 5])

    f = h5py.File("responses.hdf5", 'r')

    for ii in xrange(len(set_id_set)):
        set_id = set_id_set[ii]

        """get the x, y data for plotting the evd"""

        x = f.get('evd_%s' % set_id)[...]

        y = (np.arange(x.size)+1)/np.float32(x.size)

        """retrieve the predicted coefficients"""
        mu = f_reg.get('Rpred_val_mu')[indx, ii]
        sigma = f_reg.get('Rpred_val_sigma')[indx, ii]

        # """retrieve the coefficients for validation"""
        # mu = f.get('mu_%s' % set_id)[...]
        # sigma = f.get('sigma_%s' % set_id)[...]

        """plot the original data and the fits"""
        plt.plot(np.log(x), y, '.', markersize=1, color=colormat[ii, :])

        tmp = np.linspace(np.log(x).min(), np.log(x).max(), 100)
        x_ = np.exp(tmp)

        plt.plot(np.log(x_), ss.gamma.cdf(x_, 0.8, loc=mu, scale=sigma),
                 '-', color=colormat[ii, :], lw=1, label=set_id)

    f.close()
    f_reg.close()

    plt.xlabel("ln(FIP)")
    plt.ylabel("CDF")
    plt.legend(loc='lower right', shadow=True, fontsize='medium')

    ymin = y.min()
    ymax = y.max()
    rng = ymax - ymin
    ymin += -0.1*rng
    ymax += 0.1*rng

    plt.ylim((ymin, ymax))
    plt.tight_layout()


if __name__ == '__main__':
    set_id = sys.argv[1]
    pltevd(set_id)
    plt.show()
