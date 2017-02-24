# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import sklearn.metrics as sm
from constants import const
from matplotlib.ticker import AutoMinorLocator
import h5py
import sys


def fit_gamma_robust(tail):
    s_f = 1.16

    # fit 4 (alternate)
    stats = ss.gamma.fit(tail, fa=s_f, floc=np.min(tail)*.99999)

    # # fit 4 (alternate)
    # stats = ss.gamma.fit(tail, a=s_f, floc=np.min(tail)*.99999)

    # calculate the r**2 for the CDF fit
    cdf = (np.arange(len(tail)) + 1) / float(len(tail))
    pred_ys = ss.gamma.cdf(tail, *stats)
    r2 = sm.r2_score(pred_ys, cdf)

    # otherwise return the second set of parameters
    return stats, r2


def pltevd(sid, ns, pcnt):

    C = const()

    f = h5py.File("raw_responses.hdf5", 'r')
    tmp = f.get('fip_%s' % sid)[:ns, :]
    f.close()
    rawfip = tmp.reshape((tmp.size,))

    x = np.sort(rawfip)

    # cut off by percentage
    x = x[np.int64(pcnt*x.size):, None]

    gamma_stats, r2 = fit_gamma_robust(x)

    alpha = gamma_stats[0]
    mu = gamma_stats[1]
    sigma = gamma_stats[2]

    fig, ax = plt.subplots(figsize=[5.5, 4])

    xmin = np.log(x).min()
    xmax = np.log(x).max()
    xrng = xmax-xmin

    y = (np.arange(x.size)+1)/np.float32(x.size)

    """plot the original data and the fits"""
    # plt.plot(np.log(x), y,
    #          linestyle=':', color='b',
    #          lw=1.5, alpha=.5, label='original')
    plt.semilogy(np.log(x), 1-y,
                 linestyle=':', color='b',
                 lw=1.5, alpha=.5, label='original')

    tmp = np.linspace(xmin-.5*xrng, xmax+.5*xrng, 200)
    x_ = np.exp(tmp)
    y_ = ss.gamma.cdf(x_, alpha, loc=mu, scale=sigma)

    tmp = y_ > 0
    x_ = x_[tmp]
    y_ = y_[tmp]

    # plt.plot(np.log(x_), y_,
    #          linestyle='-', color='b',
    #          lw=1.5, alpha=.5, label='fit')
    plt.semilogy(np.log(x_), 1-y_,
                 linestyle='-', color='b',
                 lw=1.5, alpha=.5, label='fit')

    plt.xlabel("ln(FIP)", fontsize=13)
    plt.ylabel("Probability of exceedance", fontsize=13)
    # plt.ylabel("CDF", fontsize=13)

    plt.legend(loc='upper right',
               ncol=1, fontsize='large')

    xmin = np.round(xmin)-0.25
    xmax = np.round(xmax)+0.25

    mult = 4.
    plt.xticks(np.arange(np.floor(mult*xmin), np.ceil(mult*xmax))/mult, fontsize='medium')
    minor_locator = AutoMinorLocator(2)

    ax.xaxis.set_minor_locator(minor_locator)

    plt.xlim((xmin, xmax))

    print ns
    ymin = 1/np.float64((1-.99999)*ns*C['el']**3)
    plt.ylim((ymin, 1))
    print ymin

    plt.tight_layout()


if __name__ == '__main__':
    sid = sys.argv[1]
    ns = np.int64(sys.argv[2])
    pcnt = np.float(sys.argv[3])
    pltevd(sid, ns, pcnt)
    plt.show()
