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


def pltevd(indx1, indx2, H):

    C = const()

    """define the colors of interest"""
    n_col = len(C['set_id_cal'] + C['set_id_val'])
    colormat = cm.rainbow(np.linspace(0, 1, n_col))
    gray = [.7, .7, .7]

    f_reg = h5py.File("regression_results_L%s.hdf5" % H, 'r')

    fig = plt.figure(figsize=[5.5, 4])

    f = h5py.File("responses.hdf5", 'r')

    c = 0

    for ii in xrange(len(C['set_id_cal'])):
        set_id = C['set_id_cal'][ii]

        """get the x, y data for plotting the evd"""

        x = f.get('evd_%s' % set_id)[...]

        if ii == 0:
            xmin = np.log(x).min()
            xmax = np.log(x).max()
        else:
            xmin = np.min([xmin, np.log(x).min()])
            xmax = np.max([xmax, np.log(x).max()])
        xrng = np.abs(xmax - xmin)

        y = (np.arange(x.size)+1)/np.float32(x.size)

        """retrieve the predicted coefficients"""
        mu = f_reg.get('Rpred_cal_mu')[indx1, ii]
        sigma = f_reg.get('Rpred_cal_sigma')[indx2, ii]

        # """retrieve the coefficients for validation"""
        # mu = f.get('mu_%s' % set_id)[...]
        # sigma = f.get('sigma_%s' % set_id)[...]

        # """plot the original data and the fits"""
        # plt.plot(np.log(x), y, '.', markersize=1, color=colormat[ii, :])

        tmp = np.linspace(xmin-.5*xrng, xmax+.5*xrng, 200)
        x_ = np.exp(tmp)
        y_ = ss.gamma.cdf(x_, 0.8, loc=mu, scale=sigma)

        tmp = y_ > 0
        x_ = x_[tmp]
        y_ = y_[tmp]

        plt.plot(np.log(x_), y_,
                 '-', color=colormat[c, :], lw=1, label=set_id)

        c += 1

    for ii in xrange(len(C['set_id_val'])):
        set_id = C['set_id_val'][ii]

        """get the x, y data for plotting the evd"""

        x = f.get('evd_%s' % set_id)[...]

        xmin = np.min([xmin, np.log(x).min()])
        xmax = np.max([xmax, np.log(x).max()])
        xrng = np.abs(xmax - xmin)

        y = (np.arange(x.size)+1)/np.float32(x.size)

        """retrieve the predicted coefficients"""
        mu = f_reg.get('Rpred_val_mu')[indx1, ii]
        sigma = f_reg.get('Rpred_val_sigma')[indx2, ii]

        # """retrieve the coefficients for validation"""
        # mu = f.get('mu_%s' % set_id)[...]
        # sigma = f.get('sigma_%s' % set_id)[...]

        # """plot the original data and the fits"""
        # plt.plot(np.log(x), y, '.', markersize=1, color=colormat[ii, :])

        tmp = np.linspace(xmin-.5*xrng, xmax+.5*xrng, 200)
        x_ = np.exp(tmp)
        y_ = ss.gamma.cdf(x_, 0.8, loc=mu, scale=sigma)

        tmp = y_ > 0
        x_ = x_[tmp]
        y_ = y_[tmp]

        plt.plot(np.log(x_), y_,
                 '-', color=colormat[c, :], lw=1, label=set_id)

        c += 1

    f.close()
    f_reg.close()

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

    fig_name = 'evd_pred_L%s.png' % H
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':
    set_id = sys.argv[1]
    pltevd(set_id)
    plt.show()
