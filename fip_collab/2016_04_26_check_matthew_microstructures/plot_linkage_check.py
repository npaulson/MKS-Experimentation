import numpy as np
import matplotlib.pyplot as plt
import h5py


def plot_check(el, ns_set, set_id_set, resptyp):

    colormat = np.array([[.3, .3, 1.],
                         [.3, 1., .3],
                         [1., .2, .2],
                         [0., .7, .7],
                         [.7, .0, .7],
                         [.7, .7, .0]])

    f_reg = h5py.File("regression_results.hdf5", 'r')

    """find n_pc, n_poly for the minumum average prediction error"""

    indx = f_reg.get('meanerr')[...].argmin()
    n_pc, n_poly = f_reg.get('order')[indx, :]
    print "n_pc: %s" % n_pc
    print "n_poly: %s" % n_poly

    """plot the prediction error versus number of pc/poly"""
    rlen = f_reg.get('order').shape[0]

    plotmat = np.zeros((rlen, 4))
    plotmat[:, :2] = f_reg.get('order')[...]
    plotmat[:, 2] = f_reg.get('meanerr')[...]
    plotmat[:, 3] = f_reg.get('maxerr')[...]
    n_pc_min = plotmat[:, 0].min()
    n_pc_max = plotmat[:, 0].max()
    n_poly_min = plotmat[:, 1].min()
    n_poly_max = plotmat[:, 1].max()
    pc_range = len(np.unique(plotmat[:, 0]))
    poly_range = len(np.unique(plotmat[:, 1]))

    print plotmat
    plotmat = plotmat.reshape((pc_range, poly_range, 4))
    print plotmat.shape

    plt.figure(num=5, figsize=[6.5, 5])

    extent = [n_pc_min-0.5, n_pc_max+0.5, n_poly_min-1.5, n_poly_max-0.5]

    ax = plt.imshow(plotmat[:, :, 2], origin='lower',
                    interpolation='none', cmap='rainbow', extent=extent)

    plt.colorbar(ax)
    plt.xlabel("degree of polynomial")
    plt.ylabel("number of PCs")
    plt.title("mean error in prediction for %s" % resptyp)

    """load the simulated and predicted responses"""
    Rsim = f_reg.get('Rsim')[...]
    Rpred = f_reg.get('Rpred')[indx, :]

    """plot the prediction equal to simulation line"""
    plt.figure(num=6, figsize=[10, 7])

    minval = np.min([Rsim, Rpred])
    maxval = np.max([Rsim, Rpred])

    valrange = maxval-minval
    minval += -0.5*valrange
    maxval += 0.5*valrange
    line = np.array([minval, maxval])

    plt.plot(line, line, 'k-')

    c = 0
    for ii in xrange(len(set_id_set)):

        c_ = c + ns_set[ii]
        set_id = set_id_set[ii]
        Rsim_tmp = Rsim[c:c_]
        Rpred_tmp = Rpred[c:c_]
        c = c_

        ax = plt.plot(Rsim_tmp, Rpred_tmp,
                      marker='o', markersize=7, color=colormat[ii, :],
                      linestyle='', label=set_id)

    plt.title("predicted versus simulated %s" % resptyp)
    plt.xlabel("simulation")
    plt.ylabel("prediction")
    plt.legend(loc='upper right', shadow=True, fontsize='medium')

    plt.xticks(rotation=20)
    plt.yticks(rotation=20)

    f_reg.close()

    plt.show()


if __name__ == '__main__':
    el = 21
    ns_val = [10, 10, 10, 10]
    set_id_val = ['randomD3D_val', 'transverseD3D_val',
                  'basaltransD3D_val', 'actualD3D_val']

    resptyp = 'maximum FIP'

    plot_check(el, ns_val, set_id_val, resptyp)
