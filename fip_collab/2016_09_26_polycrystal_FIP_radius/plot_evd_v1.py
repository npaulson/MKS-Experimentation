# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import sklearn.metrics as sm
import matplotlib.cm as cm
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


def pltevd(H):

    C = const()

    """define the colors of interest"""
    n_col = len(C['sid'])
    colormat = cm.Set1(np.linspace(0, 1, n_col))

    f = h5py.File("sample_L%s.hdf5" % H, 'r')

    fig = plt.figure(figsize=[5.5, 4])

    for ii in xrange(n_col):

        sid = C['sid'][ii]

        """get the x, y data for plotting the evd"""

        x_tmp = []

        for jj in xrange(2*C['n_pc_samp']):
            tmp = f.get('evd_pc%s_%s' % (jj, sid))[...]
            x_tmp = x_tmp + list(tmp)

        x = np.sort(np.array(x_tmp))

        if ii == 0:
            xmin = np.log(x).min()
            xmax = np.log(x).max()
        else:
            xmin = np.min([xmin, np.log(x).min()])
            xmax = np.max([xmax, np.log(x).max()])
        xrng = np.abs(xmax - xmin)

        y = (np.arange(x.size)+1)/np.float32(x.size)

        """retrieve the predicted coefficients"""

        mu_tmp = f.get('mu_%s' % sid)[...]
        sigma_tmp = f.get('sigma_%s' % sid)[...]
        mu = mu_tmp.mean()
        sigma = sigma_tmp.mean()

        # """plot the original data and the fits"""
        # plt.plot(np.log(x), y, '.', markersize=1, color=colormat[ii, :])

        tmp = np.linspace(xmin-.5*xrng, xmax+.5*xrng, 200)
        x_ = np.exp(tmp)
        y_ = ss.gamma.cdf(x_, 0.8, loc=mu, scale=sigma)

        tmp = y_ > 0
        x_ = x_[tmp]
        y_ = y_[tmp]

        plt.plot(np.log(x_), y_,
                 '-', color=colormat[ii, :], lw=1.5, label=sid)

    f.close()

    plt.xlabel("ln(FIP)")
    plt.ylabel("CDF")
    plt.legend(loc='lower right', shadow=True, fontsize='small')

    xmin += -0.01*xrng
    xmax += 0.01*xrng
    plt.xlim((xmin, xmax))

    ymin = y.min()
    ymax = y.max()
    rng = ymax - ymin
    ymin = 0
    ymax += 0.01*rng
    plt.ylim((ymin, ymax))

    plt.tight_layout()

    fig_name = 'evd_orig_L%s.png' % H
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':
    sid = sys.argv[1]
    pltevd(sid)
    plt.show()
