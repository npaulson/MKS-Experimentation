# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import sklearn.metrics as sm
import matplotlib.cm as cm
from constants import const
from matplotlib.ticker import AutoMinorLocator
import h5py
import sys


def fit_gamma_robust(tail):

    C = const()

    s_f = C['alpha']

    # fit 4 (alternate)
    stats = ss.gamma.fit(tail, fa=s_f, floc=np.min(tail)*.99999)

    # calculate the r**2 for the CDF fit
    cdf = (np.arange(len(tail)) + 1) / float(len(tail))
    pred_ys = ss.gamma.cdf(tail, *stats)
    r2 = sm.r2_score(pred_ys, cdf)

    # otherwise return the second set of parameters
    return stats, r2


def pltevd(H):

    C = const()

    """define the colors of interest"""
    n_col = len(C['sid'])
    colormat = cm.plasma(np.linspace(0, .9, 4))
    linemat = ['-', '--', ':']

    f = h5py.File("responses.hdf5", 'r')

    fig, ax = plt.subplots(figsize=[5.5, 4])

    for ii in xrange(n_col):

        sid = C['sid'][ii]

        """get the x, y data for plotting the evd"""
        x = f.get('evd_%s' % sid)[...][...]

        if ii == 0:
            xmin = np.log(x).min()
            xmax = np.log(x).max()
        else:
            xmin = np.min([xmin, np.log(x).min()])
            xmax = np.max([xmax, np.log(x).max()])

        y = (np.arange(x.size)+1)/np.float32(x.size)

        ll = np.int8(np.mod(ii, 3))
        nn = np.int8(np.floor(ii/3.))

        """plot the original data and the fits"""
        # plt.plot(np.log(x), y,
        #          linestyle=linemat[ll], color=colormat[nn, :],
        #          lw=1.5, label=sid)

        plt.semilogy(np.log(x), 1-y,
                     linestyle=linemat[ll], color=colormat[nn, :],
                     lw=1.5, label=sid)

    f.close()

    plt.xlabel("ln(FIP)")
    plt.ylabel("Probability of exceedance")
    lgd = plt.legend(bbox_to_anchor=(1, 1), loc='upper left',
                     ncol=1, fontsize='small')

    plt.xticks(np.arange(np.floor(xmin), np.ceil(xmax)))
    minor_locator = AutoMinorLocator(2)
    ax.xaxis.set_minor_locator(minor_locator)

    # xmin = np.round(xmin)-0.25
    # xmax = np.round(xmax)+0.25
    rng = xmax-xmin
    xmin = xmin - .1*rng
    xmax = xmax + .1*rng
    plt.xlim((xmin, xmax))

    ymin = 1/np.float64((1-C['pcnt'])*C['ns'][0]*C['el']**3)
    plt.ylim((ymin, 1))

    fig_name = 'evd_orig_L%s.png' % H
    fig.canvas.set_window_title(fig_name)
    fig.savefig(fig_name, bbox_extra_artists=(lgd,), bbox_inches='tight')


if __name__ == '__main__':
    sid = sys.argv[1]
    pltevd(sid)
    plt.show()
