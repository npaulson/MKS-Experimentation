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


# def fit_gamma_robust(tail):
#     s_f = 0.8

#     # fit 4 (alternate)
#     stats = ss.gamma.fit(tail, fa=s_f, floc=np.min(tail)*.99999)

#     # calculate the r**2 for the CDF fit
#     cdf = (np.arange(len(tail)) + 1) / float(len(tail))
#     pred_ys = ss.gamma.cdf(tail, *stats)
#     r2 = sm.r2_score(pred_ys, cdf)

#     # otherwise return the second set of parameters
#     return stats, r2

def fit_gamma_robust(tail):
    # fit 4 (alternate)
    stats = ss.gamma.fit(tail, floc=np.min(tail)*.99999)

    # calculate the r**2 for the CDF fit
    cdf = (np.arange(len(tail)) + 1) / float(len(tail))
    pred_ys = ss.gamma.cdf(tail, *stats)
    r2 = sm.r2_score(pred_ys, cdf)

    # otherwise return the second set of parameters
    return stats, r2


def pltevd(sid):

    C = const()

    fig, ax = plt.subplots(figsize=[7, 6])

    """get the x, y data for plotting the evd"""

    f = h5py.File("raw_responses.hdf5", 'r')
    fip = f.get('fip_%s' % sid)[...]
    f.close()

    fip = fip.reshape((C['ns'][0]*C['el']**3,))
    x_ = np.sort(fip)
    y_ = (np.arange(x_.size)+1)/np.float32(x_.size)
    xmin = np.log(x_).min()
    xmax = np.log(x_).max()

    # pctile = [0.0, 0.9, 0.99, 0.999, 0.9999]
    pctile = [0.99, 0.999, 0.9999]

    """define the colors of interest"""
    colormat = cm.plasma(np.linspace(0, .9, len(pctile)))

    for ii in xrange(len(pctile)):

        x = x_[np.int64(pctile[ii]*x_.size):, None]
        y = y_[np.int64(pctile[ii]*y_.size):]

        """fit the data"""
        gamma_stats, r2 = fit_gamma_robust(x)
        alpha = gamma_stats[0]
        mu = gamma_stats[1]
        sigma = gamma_stats[2]
        yf = ss.gamma.sf(x, 0.8, loc=mu, scale=sigma)*(1-pctile[ii])

        """plot the original data"""
        plt.semilogy(np.log(x), 1-y,
                     linestyle='-', color=colormat[ii, :],
                     lw=1.5,
                     label=r'$\mathrm{%s^{th}\:percentile,}\alpha=%s$' % (str(100*pctile[ii]), np.round(alpha,2)))

        """plot the fitted data"""
        plt.semilogy(np.log(x), yf,
                     linestyle='-', color=colormat[ii, :],
                     lw=1.5, alpha=0.5)

    plt.xlabel("ln(FIP)")
    plt.ylabel("Probability of exceedance")
    # lgd = plt.legend(bbox_to_anchor=(1, 1), loc='upper left',
    #                  ncol=1, fontsize='large')
    plt.legend(loc='lower left', ncol=1, fontsize='large')

    plt.xticks(np.arange(np.floor(xmin), np.ceil(xmax)+1))
    minor_locator = AutoMinorLocator(2)
    ax.xaxis.set_minor_locator(minor_locator)

    xmin = np.round(xmin)-0.25
    xmax = np.round(xmax)+1
    plt.xlim((xmin, xmax))

    ymin = 1/np.float64((1-C['pcnt'])*C['ns'][0]*C['el']**3)
    plt.ylim((ymin*0.0001, 1))

    fig_name = 'evd_test_L%s.png' % C['H']
    fig.canvas.set_window_title(fig_name)
    # fig.savefig(fig_name, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.tight_layout()
    fig.savefig(fig_name)


if __name__ == '__main__':
    sid = sys.argv[1]
    pltevd(sid)
    plt.show()
