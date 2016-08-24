# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from constants import const
import h5py
import sys


def pltevd(set_id_set):

    C = const()

    colormat = np.array([[.3, .3, 1.],
                         [.3, 1., .3],
                         [1., .2, .2],
                         [0., .7, .7],
                         [.7, .0, .7],
                         [.7, .7, .0],
                         [.5, .3, .1],
                         [.3, .5, .1],
                         [.1, .3, .5]])

    f_reg = h5py.File("regression_results.hdf5", 'r')

    plt.figure(figsize=[5.5, 4])

    f = h5py.File("responses.hdf5", 'r')

    for ii in xrange(len(set_id_set)):
        set_id = set_id_set[ii]

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


if __name__ == '__main__':
    set_id = sys.argv[1]
    pltevd(set_id)
    plt.show()
