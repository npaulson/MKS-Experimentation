import numpy as np
import matplotlib.pyplot as plt
from constants import const
import h5py


def pltpcpoly(par, n_pc_max):

    C = const()

    # colormat = np.array([[0, 0, 0],
    #                      [.8, .8, .8],
    #                      [.4, .4, .4]])

    colormat = np.array([[0, 0, .9],
                         [0, .7, .1],
                         [.9, 0, 0]])

    # colormat = np.array([[.35, .02, 1],
    #                      [.63, .02, 1],
    #                      [.92, .15, 0]])

    # colormat = np.array([[.13, 0, .39],
    #                      [.35, .02, 1],
    #                      [.68, .52, 1],
    #                      [.24, 0, .39],
    #                      [.63, .02, 1],
    #                      [.82, .52, 1],
    #                      [.39, .07, 0],
    #                      [.92, .15, 0],
    #                      [1.0, .55, .46]])

    fig = plt.figure(figsize=[7, 5])

    H = [4, 9, 23]
    # H = [4]

    errmax = 0

    for ii in xrange(len(H)):

        f = h5py.File("regression_results_L%s.hdf5" % H[ii], 'r')

        rlen = f.get('order_%s' % par).shape[0]
        n_fac = f.get('Rpred_cal_%s' % par)[...].mean()

        """plot the prediction error versus number of pc for
        calibration data"""

        plotmat = np.zeros((rlen, 3))
        plotmat[:, :2] = f.get('order_%s' % par)[...]
        plotmat[:, 2] = f.get('meanerr_cal_%s' % par)[...]

        pc_range = len(np.unique(plotmat[:, 0]))
        poly_range = len(np.unique(plotmat[:, 1]))

        plotmat_ = plotmat.reshape((pc_range, poly_range, 3))

        err = 100*plotmat_[..., 0, 2]/n_fac
        if err.max() > errmax:
            errmax = err.max()

        plt.plot(np.arange(n_pc_max)+1, err[:n_pc_max],
                 marker='', markersize=8, color=colormat[ii, :], alpha=0.7,
                 linestyle='--', linewidth=1, label="calibration L=%s" % H[ii])

        """plot the prediction error versus number of pc for
        validations data"""

        plotmat = np.zeros((rlen, 3))
        plotmat[:, :2] = f.get('order_%s' % par)[...]
        plotmat[:, 2] = f.get('meanerr_val_%s' % par)[...]

        pc_range = len(np.unique(plotmat[:, 0]))
        poly_range = len(np.unique(plotmat[:, 1]))

        plotmat_ = plotmat.reshape((pc_range, poly_range, 3))

        err = 100*plotmat_[..., 0, 2]/n_fac
        if err.max() > errmax:
            errmax = err.max()

        plt.plot(np.arange(n_pc_max)+1, err[:n_pc_max],
                 marker='', markersize=8, color=colormat[ii, :], alpha=0.5,
                 linestyle='-', linewidth=1, label="validation L=%s" % H[ii])

        """plot the prediction error versus number of pc for
        LOOCV data"""

        plotmat = np.zeros((rlen, 3))
        plotmat[:, :2] = f.get('order_%s' % par)[...]
        plotmat[:, 2] = f.get('loocv_err_%s' % par)[...]

        pc_range = len(np.unique(plotmat[:, 0]))
        poly_range = len(np.unique(plotmat[:, 1]))

        plotmat_ = plotmat.reshape((pc_range, poly_range, 3))

        err = 100*plotmat_[..., 2]/n_fac
        if err.max() > errmax:
            errmax = err.max()

        plt.plot(np.arange(n_pc_max)+1, err[:n_pc_max],
                 marker='', markersize=7, color=colormat[ii, :], alpha=0.99,
                 linestyle=':', linewidth=1, label="LOOCV L=%s" % H[ii])

    spc = np.int16(np.ceil(n_pc_max/15.))
    plt.xticks(np.arange(0, n_pc_max+spc, spc))

    plt.axis([.5, n_pc_max+.5, 0, 1.1*errmax])

    # plt.grid(True)
    plt.legend(loc='upper right', shadow=True, fontsize='small', ncol=3)

    plt.xlabel("number of PCs")
    plt.ylabel("mean error (%)")

    fig_name = 'selection_%s_npc%s.png' % (par, n_pc_max)
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)

    plt.tight_layout()

    f.close()


if __name__ == '__main__':
    prop = "yield"
    bc = "bc1"
    pltpcpoly(prop, bc)
    plt.show()
