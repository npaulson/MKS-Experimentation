# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import matplotlib.cm as cm
from constants import const
from matplotlib.ticker import AutoMinorLocator
import get_linkage as gl
import reg_functions as rf
import h5py
import sys


def predict_evd_full(H, par, flvl):

    C = const()
    n_sid = len(C['sid'])

    """obtain S-P linkage coefficients and associated indices"""
    f = h5py.File('regression_results_L%s.hdf5' % H, 'r')
    coef = f.get('coef_%s' % par)[flvl, :(flvl+1)]
    indxsel = f.get('indxsel_%s' % par)[:(flvl+1)]
    f.close()

    """obtain centers and spreads for microstructure classes"""
    loc = np.zeros((n_sid, C['n_pc_max']))
    var = np.zeros((n_sid, C['n_pc_max']))

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % H, 'r')

    for ii in xrange(n_sid):
        sid = C['sid'][ii]
        reduced = f_red.get('reduced_%s' % sid)[:, :C['n_pc_max']]
        loc[ii, :] = np.mean(reduced, 0)
        var[ii, :] = np.var(reduced, 0)

    f_red.close()

    """do preanalysis on centers and spreads"""
    X, names = gl.preanalysis(loc, var)

    """predict parameter values"""
    Rpred = rf.prediction(X[:, indxsel], coef)

    return np.exp(Rpred)


def pltevd(flvl_mu, H_mu, flvl_sigma, H_sigma):

    C = const()
    n_sid = len(C['sid'])

    """obtain parameter values"""
    mu = predict_evd_full(H_mu, 'mu', flvl_mu)
    sigma = predict_evd_full(H_sigma, 'sigma', flvl_sigma)

    """define the colors of interest"""
    colormat = cm.plasma(np.linspace(0, .9, 4))
    # colormat = cm.viridis(np.linspace(0.2, 0.9, 4))
    linemat = ['-', '--', ':']

    fig, ax = plt.subplots(figsize=[5.5, 4])

    f = h5py.File("responses.hdf5", 'r')
    c_ = 0
    for ii in xrange(n_sid):
        c = c_
        c_ = c + C['n_sc']

        sid = C['sid'][ii]
        name = C['names_plt'][ii]

        """get the x, y data for plotting the evd"""
        x = f.get('evd_%s' % sid)[...][...]

        if ii == 0:
            xmin = np.log(x).min()
            xmax = np.log(x).max()
        else:
            xmin = np.min([xmin, np.log(x).min()])
            xmax = np.max([xmax, np.log(x).max()])
        xrng = np.abs(xmax - xmin)

        tmp = np.linspace(xmin-.5*xrng, xmax+.5*xrng, 200)
        x_ = np.exp(tmp)
        y_ = ss.gamma.cdf(x_, 0.8, loc=mu[ii], scale=sigma[ii])

        tmp = y_ > 0
        x_ = x_[tmp]
        # y_ = y_[tmp]
        y_ = (y_[tmp]*(1-C['pcnt']))+C['pcnt']

        ll = np.int8(np.mod(ii, 3))
        nn = np.int8(np.floor(ii/3.))

        # plt.plot(np.log(x_), y_,
        #          linestyle=linemat[ll], color=colormat[nn, :],
        #          lw=1.5, alpha=.99, label=name)

        plt.semilogy(np.log(x_), 1-y_,
                     linestyle=linemat[ll], color=colormat[nn, :],
                     lw=1.5, alpha=.99, label=name)

    f.close()

    plt.xlabel("ln(FIP)", fontsize=14)
    plt.ylabel("Probability of exceedance", fontsize=14)
    lgd = plt.legend(bbox_to_anchor=(1, 1), loc='upper left',
                     ncol=1, fontsize=12, fancybox=False)

    plt.xticks(np.arange(np.floor(xmin), np.ceil(xmax)), fontsize=14)
    plt.yticks(fontsize=14)
    # minor_locator = AutoMinorLocator(2)
    # ax.xaxis.set_minor_locator(minor_locator)

    # xmin = np.round(xmin)-0.25
    # xmax = np.round(xmax)+0.25
    rng = xmax-xmin
    xmin = xmin - .1*rng
    xmax = xmax + .1*rng

    plt.xlim((xmin, xmax))

    ymin = 1/np.float64(C['ns'][0]*C['el']**3)
    ymax = (1-C['pcnt'])
    plt.ylim((ymin, ymax))

    fig_name = 'evd_pred.png'
    fig.canvas.set_window_title(fig_name)
    fig.savefig(fig_name, bbox_extra_artists=(lgd,), bbox_inches='tight')


if __name__ == '__main__':
    sid = sys.argv[1]
    pltevd(sid)
    plt.show()
