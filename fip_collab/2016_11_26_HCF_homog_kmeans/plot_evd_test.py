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
    s_f = 0.8

    # fit 4 (alternate)
    stats = ss.gamma.fit(tail, fa=s_f, floc=np.min(tail)*.99999)

    # calculate the r**2 for the CDF fit
    cdf = (np.arange(len(tail)) + 1) / float(len(tail))
    pred_ys = ss.gamma.cdf(tail, *stats)
    r2 = sm.r2_score(pred_ys, cdf)

    # otherwise return the second set of parameters
    return stats, r2


def pltevd(sid):

    C = const()

    fig, ax = plt.subplots(figsize=[5.5, 4])

    """get the x, y data for plotting the evd"""
    f = h5py.File("responses.hdf5", 'r')
    x_ = f.get('evd_%s' % sid)[...][...]
    y_ = (np.arange(x_.size)+1)/np.float32(x_.size)

    xmin = np.log(x_).min()
    xmax = np.log(x_).max()

    print x_

    f.close()

    pctile = [0.0, 0.8, 0.98, 0.998]
    pctile_write = [95, 99, 99.9, 99.99]

    """define the colors of interest"""
    colormat = cm.plasma(np.linspace(0, .9, len(pctile)))

    for ii in xrange(len(pctile)):

        x = x_[np.int64(pctile[ii]*x_.size):, :]
        y = y_[np.int64(pctile[ii]*y_.size):]

        # y = (np.arange(x.size)+1)/np.float32(x.size)

        """plot the original data and the fits"""
        plt.semilogy(np.log(x), 1-y,
                     linestyle='-', color=colormat[ii, :],
                     lw=1.5, label="%sth percentile" % pctile_write[ii])

    plt.xlabel("ln(FIP)")
    plt.ylabel("Probability of exceedance")
    lgd = plt.legend(bbox_to_anchor=(1, 1), loc='upper left',
                     ncol=1, fontsize='small')

    plt.xticks(np.arange(np.floor(xmin), np.ceil(xmax)))
    minor_locator = AutoMinorLocator(2)
    ax.xaxis.set_minor_locator(minor_locator)

    xmin = np.round(xmin)-0.25
    xmax = np.round(xmax)+0.25
    plt.xlim((xmin, xmax))

    ymin = 1/np.float64((1-C['pcnt'])*C['ns'][0]*C['el']**3)
    plt.ylim((ymin, 1))

    fig_name = 'evd_test_L%s.png' % C['H']
    fig.canvas.set_window_title(fig_name)
    fig.savefig(fig_name, bbox_extra_artists=(lgd,), bbox_inches='tight')


if __name__ == '__main__':
    sid = sys.argv[1]
    pltevd(sid)
    plt.show()
