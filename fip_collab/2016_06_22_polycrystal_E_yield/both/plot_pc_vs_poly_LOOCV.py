import numpy as np
import matplotlib.pyplot as plt
from constants import const
import h5py


def pltpcpoly(par):

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

    """plot the prediction error versus number of pc/poly for
    calibration data"""
    rlen = f.get('order_%s' % par).shape[0]

    plotmat = np.zeros((rlen, 4))
    plotmat[:, :2] = f.get('order_%s' % par)[...]
    plotmat[:, 2] = f.get('loocv_err_%s' % par)[...]

    pc_range = len(np.unique(plotmat[:, 0]))
    poly_range = len(np.unique(plotmat[:, 1]))

    plotmat_ = plotmat.reshape((pc_range, poly_range, 4))

    fig = plt.figure(figsize=[6, 4])

    n_fac = f.get('Rpred_cal_%s' % par)[...].mean()
    err = 100*plotmat_[..., 2]/n_fac

    for ii in xrange(poly_range):
        deg = ii + 1
        plt.plot(np.arange(pc_range)+1, err[:, ii],
                 marker='', markersize=3, color=colormat[ii, :],
                 linestyle='-', linewidth=2,
                 label="degree = %s" % deg)

    spc = np.int16(np.ceil(pc_range/10.))
    plt.xticks(np.arange(0, pc_range+spc, spc))

    plt.axis([0, pc_range, 0, 1.1*err.max()])

    plt.grid(True)
    # plt.legend(loc='upper right', shadow=True, fontsize='medium')

    # plt.title("mean LOOCV error with calibration data for %s" % par)
    plt.xlabel("number of PCs")
    plt.ylabel("percentage error")

    plt.tight_layout()

    fig_name = 'selection_LOOCV_%s_L%s.png' % (par, C['H'])
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)

    f.close()


if __name__ == '__main__':
    prop = "yield"
    bc = "bc1"
    pltpcpoly(prop, bc)
    plt.show()
