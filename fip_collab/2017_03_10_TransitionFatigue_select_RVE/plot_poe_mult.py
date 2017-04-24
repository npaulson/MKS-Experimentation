# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import sklearn.metrics as sm
from constants import const
from matplotlib.ticker import AutoMinorLocator
import matplotlib.cm as cm
import h5py
import sys


def fit_gamma_robust(tail):
    s_f = 1.16

    # # fit 4 (alternate)
    # stats = ss.gamma.fit(tail, fa=s_f, floc=np.min(tail)*.99999)

    # fit 4 (alternate)
    stats = ss.gamma.fit(tail, a=s_f, floc=np.min(tail)*.99999)

    # calculate the r**2 for the CDF fit
    cdf = (np.arange(len(tail)) + 1) / float(len(tail))
    pred_ys = ss.gamma.cdf(tail, *stats)
    r2 = sm.r2_score(pred_ys, cdf)

    # otherwise return the second set of parameters
    return stats, r2


def pltevd(sid, ns):

    f = h5py.File("raw_responses.hdf5", 'r')
    tmp = f.get('fip_%s' % sid)[:ns, :]
    f.close()
    rawfip = tmp.reshape((tmp.size,))

    x = np.sort(rawfip)

    pcntv = [.99, .999, .9999]
    colorv = cm.rainbow(np.linspace(0, .3, len(pcntv)))

    fig, ax = plt.subplots(figsize=[5, 6.5])

    xmin = 1e9
    xmax = -1e9

    y = (np.arange(x.size)+1)/np.float32(x.size)
    plt.semilogy(np.log(x), 1-y,
                 linestyle='-', color='k',
                 lw=1.5, alpha=.99, label='true FIP EVD')

    # plt.semilogy(np.log(x), 1-y,
    #              marker='.', color='k', markersize=5, linestyle='',
    #              alpha=.6, label='true FIP EVD')

    for ii in xrange(len(pcntv)):

        pcnt = pcntv[ii]

        # cut off by percentage
        x_tmp = x[np.int64(pcnt*x.size):, None]

        gamma_stats, r2 = fit_gamma_robust(x_tmp)

        alpha = gamma_stats[0]
        mu = gamma_stats[1]
        sigma = gamma_stats[2]

        if np.log(x_tmp).min() < xmin:
            xmin = np.log(x_tmp).min()
        if np.log(x_tmp).max() > xmax:
            xmax = np.log(x_tmp).max()

        tmp = np.linspace(xmin, xmax, 200)

        x_ = np.exp(tmp)
        y_ = ss.gamma.cdf(x_, alpha, loc=mu, scale=sigma)

        tmp = y_ > 0
        x_ = x_[tmp]
        y_ = (y_[tmp]*(1-pcnt))+pcnt

        txt = str(np.round(100*pcnt, 2))
        plt.semilogy(np.log(x_), 1-y_,
                     linestyle='-', color=colorv[ii, :],
                     lw=2, alpha=.99, label='%sth %%ile fit' % txt)

    plt.xlabel("ln(FIP)", fontsize=13)
    plt.ylabel("Probability of exceedance", fontsize=13)

    plt.xticks(fontsize=12.5, rotation='0')
    plt.yticks(fontsize=12.5)

    plt.legend(loc='lower left',
               ncol=1, fontsize='medium')

    plt.tight_layout()


if __name__ == '__main__':
    sid = sys.argv[1]
    ns = np.int64(sys.argv[2])
    pltevd(sid, ns)
    plt.show()
