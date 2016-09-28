# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
import h5py
import sys


def pltevd(H):

    C = const()

    """define the colors of interest"""
    n_col = len(C['set_id_cal'] + C['set_id_val'])
    colormat = cm.rainbow(np.linspace(0, 1, n_col))
    gray = [.7, .7, .7]

    f_reg = h5py.File("regression_results_L%s.hdf5" % H, 'r')

    fig = plt.figure(figsize=[5.5, 4])

    f = h5py.File("responses.hdf5", 'r')

    for ii in xrange(n_col):
        set_id = (C['set_id_cal']+C['set_id_val'])[ii]

        """get the x, y data for plotting the evd"""

        x = f.get('evd_%s' % set_id)[...]

        if ii == 0:
            xmin = np.log(x).min()
            xmax = np.log(x).max()
        else:
            xmin = np.min([xmin, np.log(x).min()])
            xmax = np.max([xmax, np.log(x).max()])

        y = (np.arange(x.size)+1)/np.float32(x.size)

        """plot the original data and the fits"""
        # plt.plot(np.log(x), y, '.', markersize=2, color=colormat[ii, :],
        #          label=set_id)
        plt.plot(np.log(x), y, '-', color=colormat[ii, :],
                 label=set_id)

    f.close()
    f_reg.close()

    plt.xlabel("ln(FIP)")
    plt.ylabel("CDF")
    plt.legend(loc='lower right', shadow=True, fontsize='small')

    rng = np.abs(xmax - xmin)
    xmin += -0.01*rng
    xmax += 0.01*rng
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
    set_id = sys.argv[1]
    pltevd(set_id)
    plt.show()
