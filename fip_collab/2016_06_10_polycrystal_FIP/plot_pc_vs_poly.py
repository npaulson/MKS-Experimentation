import numpy as np
import matplotlib.pyplot as plt
import h5py


def pltpcpoly(par, pltnum):

    colormat = np.array([[.3, .3, 1.],
                         [.3, 1., .3],
                         [1., .2, .2],
                         [0., .7, .7],
                         [.7, .0, .7],
                         [.7, .7, .0],
                         [.5, .3, .1],
                         [.3, .5, .1],
                         [.1, .3, .5]])

    f = h5py.File("regression_results.hdf5", 'r')

    """plot the prediction error versus number of pc/poly for
    calibration data"""
    rlen = f.get('order_%s' % par).shape[0]

    plotmat = np.zeros((rlen, 4))
    plotmat[:, :2] = f.get('order_%s' % par)[...]
    plotmat[:, 2] = f.get('meanerr_cal_%s' % par)[...]

    pc_range = len(np.unique(plotmat[:, 0]))
    poly_range = len(np.unique(plotmat[:, 1]))

    plotmat_ = plotmat.reshape((pc_range, poly_range, 4))

    plt.figure(num=pltnum, figsize=[14, 4])

    plt.subplot(121)

    for ii in xrange(poly_range):
        deg = ii + 1
        plt.plot(np.arange(pc_range)+1, plotmat_[:, ii, 2],
                 marker='o', markersize=3, color=colormat[ii, :],
                 linestyle='-', label="degree = %s" % deg)

    spc = np.int16(np.ceil(pc_range/20.))
    plt.xticks(np.arange(0, pc_range, spc)+1)
    # plt.grid(True)

    plt.legend(loc='upper right', shadow=True, fontsize='medium')

    plt.title("mean prediction error with calibration data for %s" % par)
    plt.xlabel("number of PCs")
    plt.ylabel("error")

    """plot the prediction error versus number of pc/poly for
    validation data"""
    plotmat[:, 2] = f.get('meanerr_val_%s' % par)[...]

    plotmat = plotmat.reshape((pc_range, poly_range, 4))

    plt.subplot(122)

    for ii in xrange(poly_range):
        deg = ii + 1
        plt.plot(np.arange(pc_range)+1, plotmat_[:, ii, 2],
                 marker='o', markersize=3, color=colormat[ii, :],
                 linestyle='-', label="degree = %s" % deg)

    plt.xticks(np.arange(0, pc_range, spc)+1)
    # plt.grid(True)

    plt.legend(loc='upper right', shadow=True, fontsize='medium')

    plt.title("mean prediction error with validation data for %s" % par)
    plt.xlabel("number of PCs")
    plt.ylabel("error")

    plt.tight_layout()

    f.close()


if __name__ == '__main__':
    prop = "yield"
    bc = "bc1"
    pltpcpoly(prop, bc)
    plt.show()