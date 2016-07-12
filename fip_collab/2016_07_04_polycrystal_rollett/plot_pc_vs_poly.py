import numpy as np
import matplotlib.pyplot as plt
from constants import const
import h5py


def pltpcpoly(par, typ):

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

    plotmat = np.zeros((rlen, 3))
    plotmat[:, :2] = f.get('order_%s' % par)[...]
    plotmat[:, 2] = f.get('meanerr_%s_%s' % (typ, par))[...]
    n_fac = f.get('Rpred_%s_%s' % (typ, par))[...].mean()

    pc_range = len(np.unique(plotmat[:, 0]))
    poly_range = len(np.unique(plotmat[:, 1]))

    plotmat_ = plotmat.reshape((pc_range, poly_range, 3))

    err = 100*plotmat_[..., 2]/n_fac

    fig = plt.figure(figsize=[6, 4])

    for ii in xrange(poly_range):
        deg = ii + 1
        plt.plot(np.arange(pc_range)+1, err[:, ii],
                 marker='o', markersize=3, color=colormat[ii, :],
                 linestyle='-', label="degree = %s" % deg)

    # spc = np.int16(np.ceil(pc_range/10.))
    # plt.xticks(np.arange(0, pc_range+spc, spc))
    # plt.axis([0, pc_range, 0, 1.1*err.max()])

    plt.axis([0, 20, 0, 1.1*err.max()])
    plt.grid(True)
    # plt.legend(loc='upper right', shadow=True, fontsize='medium')

    # if typ == 'cal':
    #     plt.title("mean prediction error with calibration data for %s" % par)
    # elif typ == 'val':
    #     plt.title("mean prediction error with validation data for %s" % par)

    plt.xlabel("number of PCs")
    plt.ylabel("percentage error")

    fig_name = 'selection_%s_%s_L%s.png' % (typ, par, C['H'])
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)

    plt.tight_layout()

    f.close()


if __name__ == '__main__':
    prop = "yield"
    bc = "bc1"
    pltpcpoly(prop, bc)
    plt.show()
