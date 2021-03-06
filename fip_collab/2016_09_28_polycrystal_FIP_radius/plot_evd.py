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
    colormat = cm.plasma(np.linspace(0, .9, 4))
    linemat = ['-', '--', ':']

    f = h5py.File("responses.hdf5", 'r')

    fig = plt.figure(figsize=[5.5, 4])

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
        xrng = np.abs(xmax - xmin)

        y = (np.arange(x.size)+1)/np.float32(x.size)

        ll = np.int8(np.mod(ii, 3))
        nn = np.int8(np.floor(ii/3.))

        """plot the original data and the fits"""
        plt.plot(np.log(x), y,
                 linestyle=linemat[ll], color=colormat[nn, :],
                 lw=1.5, label=sid)

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
