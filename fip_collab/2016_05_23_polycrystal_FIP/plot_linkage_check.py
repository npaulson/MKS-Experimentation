import numpy as np
import matplotlib.pyplot as plt
from constants import const
import h5py


def plot_check(ns_set, names_set, par):

    # colormat = np.random.rand(len(set_id_set), 3)
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

    """find n_pc, n_poly for the minumum average prediction error"""

    indx = f_reg.get('maxerr_val_%s' % (par))[...].argmin()
    n_pc, n_poly = f_reg.get('order_%s' % par)[indx, :]

    print "n_pc: %s" % n_pc
    print "n_poly: %s" % n_poly

    """load the simulated and predicted responses"""
    Rsim = f_reg.get('Rsim_val_%s' % par)[...]
    Rpred = f_reg.get('Rpred_val_%s' % par)[indx, :]

    """plot the prediction equal to simulation line"""
    plt.figure(num=7, figsize=[8, 7])

    minval = np.min([Rsim, Rpred])
    maxval = np.max([Rsim, Rpred])

    valrange = maxval-minval
    minval += -0.5*valrange
    maxval += 0.5*valrange
    line = np.array([minval, maxval])

    plt.plot(line, line, 'k-')

    for ii in xrange(len(ns_set)):

        name = names_set[ii]
        Rsim_tmp = Rsim[ii]
        Rpred_tmp = Rpred[ii]

        plt.plot(Rsim_tmp, Rpred_tmp,
                 marker='o', markersize=7, color=colormat[ii, :],
                 linestyle='', label=name)

    plt.title("predicted versus simulated %s" % par)
    plt.xlabel("simulation")
    plt.ylabel("prediction")
    plt.legend(loc='upper left', shadow=True, fontsize='medium')

    plt.xticks(rotation=20)
    plt.yticks(rotation=20)

    minval = np.min([Rsim, Rpred])
    maxval = np.max([Rsim, Rpred])
    valrange = maxval-minval
    minval += -0.1*valrange
    maxval += 0.1*valrange

    plt.axis([minval, maxval, minval, maxval])

    f_reg.close()

    plt.show()


if __name__ == '__main__':
    C = const()
    ns_set = C['ns_val']
    names_set = C['names_val']
    par = "c0"

    plot_check(ns_set, names_set, par)
