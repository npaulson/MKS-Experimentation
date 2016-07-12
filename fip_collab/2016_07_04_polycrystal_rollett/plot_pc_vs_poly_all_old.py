import numpy as np
import matplotlib.pyplot as plt
from constants import const
import h5py


def pltpcpoly(par, n_pc_max):

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

    f = h5py.File("regression_results_L%s.hdf5" % C['H'], 'r')

    rlen = f.get('order_%s' % par).shape[0]
    n_fac = f.get('Rpred_cal_%s' % par)[...].mean()

    fig = plt.figure(figsize=[7, 5])

    """plot the prediction error versus number of pc for
    calibration data"""

    plotmat = np.zeros((rlen, 3))
    plotmat[:, :2] = f.get('order_%s' % par)[...]
    plotmat[:, 2] = f.get('meanerr_cal_%s' % par)[...]

    pc_range = len(np.unique(plotmat[:, 0]))
    poly_range = len(np.unique(plotmat[:, 1]))

    plotmat_ = plotmat.reshape((pc_range, poly_range, 3))

    err = 100*plotmat_[..., 0, 2]/n_fac

    plt.plot(np.arange(pc_range)+1, err,
             marker='', markersize=3, color='k',
             linestyle='-', linewidth=1, label="calibration")

    """plot the prediction error versus number of pc for
    validations data"""

    plotmat = np.zeros((rlen, 3))
    plotmat[:, :2] = f.get('order_%s' % par)[...]
    plotmat[:, 2] = f.get('meanerr_val_%s' % par)[...]

    pc_range = len(np.unique(plotmat[:, 0]))
    poly_range = len(np.unique(plotmat[:, 1]))

    plotmat_ = plotmat.reshape((pc_range, poly_range, 3))

    err = 100*plotmat_[..., 0, 2]/n_fac

    plt.plot(np.arange(pc_range)+1, err,
             marker='', markersize=3, color='k',
             linestyle='--', linewidth=1, label="validation")

    """plot the prediction error versus number of pc for
    LOOCV data"""

    plotmat = np.zeros((rlen, 3))
    plotmat[:, :2] = f.get('order_%s' % par)[...]
    plotmat[:, 2] = f.get('loocv_err_%s' % par)[...]

    pc_range = len(np.unique(plotmat[:, 0]))
    poly_range = len(np.unique(plotmat[:, 1]))

    plotmat_ = plotmat.reshape((pc_range, poly_range, 3))

    err = 100*plotmat_[..., 2]/n_fac

    plt.plot(np.arange(n_pc_max)+1, err[:n_pc_max],
             marker='', markersize=3, color='k',
             linestyle=':', linewidth=1, label="LOOCV")

    spc = np.int16(np.ceil(n_pc_max/15.))
    plt.xticks(np.arange(0, n_pc_max+spc, spc))

    plt.axis([0, n_pc_max, 0, 1.1*err.max()])

    # plt.grid(True)
    plt.legend(loc='upper right', shadow=True, fontsize='medium')

    # if typ == 'cal':
    #     plt.title("mean prediction error with calibration data for %s" % par)
    # elif typ == 'val':
    #     plt.title("mean prediction error with validation data for %s" % par)

    plt.xlabel("number of PCs")
    plt.ylabel("mean error (%)")

    fig_name = 'selection_%s_npc%s_L%s.png' % (par, n_pc_max, C['H'])
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)

    plt.tight_layout()

    f.close()


if __name__ == '__main__':
    prop = "yield"
    bc = "bc1"
    pltpcpoly(prop, bc)
    plt.show()
