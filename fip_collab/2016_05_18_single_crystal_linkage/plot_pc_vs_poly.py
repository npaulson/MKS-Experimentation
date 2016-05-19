import numpy as np
import matplotlib.pyplot as plt
import h5py


def pltpcpoly(par):

    f = h5py.File("regression_results.hdf5", 'r')

    """plot the prediction error versus number of pc/poly for
    calibration data"""
    rlen = f.get('order_%s' % par).shape[0]

    plotmat = np.zeros((rlen, 4))
    plotmat[:, :2] = f.get('order_%s' % par)[...]
    plotmat[:, 2] = f.get('meanerr_cal_%s' % par)[...]
    n_pc_min = plotmat[:, 0].min()
    n_pc_max = plotmat[:, 0].max()
    n_poly_min = plotmat[:, 1].min()
    n_poly_max = plotmat[:, 1].max()
    pc_range = len(np.unique(plotmat[:, 0]))
    poly_range = len(np.unique(plotmat[:, 1]))

    # print plotmat
    plotmat = plotmat.reshape((pc_range, poly_range, 4))
    print plotmat.shape

    plt.figure(num=5, figsize=[9, 3])

    extent = [n_pc_min-0.5, n_pc_max+0.5, n_poly_min-1.5, n_poly_max-0.5]

    ax = plt.imshow(plotmat[:, :, 2].T, origin='lower',
                    interpolation='none', cmap='rainbow', extent=extent)

    plt.colorbar(ax)

    plt.xticks(np.arange(1, n_pc_max+1, np.int16((n_pc_max+1)/10.)+1))
    plt.yticks(np.arange(1, n_poly_max, np.int16(n_poly_max/10.)+1))

    plt.ylabel("degree of polynomial")
    plt.xlabel("number of PCs")
    plt.title("mean prediction error with calibration data for %s" % par)

    """plot the prediction error versus number of pc/poly for
    validation data"""
    rlen = f.get('order_%s' % par).shape[0]

    plotmat = np.zeros((rlen, 4))
    plotmat[:, :2] = f.get('order_%s' % par)[...]
    plotmat[:, 2] = f.get('meanerr_val_%s' % par)[...]
    n_pc_min = plotmat[:, 0].min()
    n_pc_max = plotmat[:, 0].max()
    n_poly_min = plotmat[:, 1].min()
    n_poly_max = plotmat[:, 1].max()
    pc_range = len(np.unique(plotmat[:, 0]))
    poly_range = len(np.unique(plotmat[:, 1]))

    # print plotmat
    plotmat = plotmat.reshape((pc_range, poly_range, 4))
    print plotmat.shape

    plt.figure(num=6, figsize=[9, 3])

    extent = [n_pc_min-0.5, n_pc_max+0.5, n_poly_min-1.5, n_poly_max-0.5]

    ax = plt.imshow(plotmat[:, :, 2].T, origin='lower',
                    interpolation='none', cmap='rainbow', extent=extent)

    plt.colorbar(ax)

    plt.xticks(np.arange(1, n_pc_max+1, np.int16((n_pc_max+1)/10.)+1))
    plt.yticks(np.arange(1, n_poly_max, np.int16(n_poly_max/10.)+1))

    plt.ylabel("degree of polynomial")
    plt.xlabel("number of PCs")
    plt.title("mean prediction error with validation data for %s" % par)

    f.close()

    plt.show()


if __name__ == '__main__':
    par = "c0"
    pltpcpoly(par)
