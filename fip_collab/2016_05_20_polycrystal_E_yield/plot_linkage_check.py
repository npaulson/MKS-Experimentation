import numpy as np
import matplotlib.pyplot as plt
import h5py


def plot_check(ns_set, names_set, prop, bc):

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

    dset_name = 'meanerr_val_%s_%s' % (prop, bc)
    indx = f_reg.get(dset_name)[...].argmin()
    n_pc, n_poly = f_reg.get('order')[indx, :]
    print "n_pc: %s" % n_pc
    print "n_poly: %s" % n_poly
    print "mean error: %s" % f_reg.get(dset_name)[...].min()
    dset_name = 'maxerr_val_%s_%s' % (prop, bc)
    print "max error: %s" % f_reg.get(dset_name)[...].min()

    """load the simulated and predicted responses"""
    Rsim = f_reg.get('Rsim_val_%s_%s' % (prop, bc))[...]
    Rpred = f_reg.get('Rpred_val_%s_%s' % (prop, bc))[indx, :]

    """plot the prediction equal to simulation line"""
    plt.figure(num=7, figsize=[8, 7])

    minval = np.min([Rsim, Rpred])
    maxval = np.max([Rsim, Rpred])

    valrange = maxval-minval
    minval += -0.5*valrange
    maxval += 0.5*valrange
    line = np.array([minval, maxval])

    plt.plot(line, line, 'k-')

    c = 0
    for ii in xrange(len(ns_set)):

        c_ = c + ns_set[ii]
        name = names_set[ii]
        Rsim_tmp = Rsim[c:c_]
        Rpred_tmp = Rpred[c:c_]
        c = c_

        ax = plt.plot(Rsim_tmp, Rpred_tmp,
                      marker='o', markersize=7, color=colormat[ii, :],
                      linestyle='', label=name)

    plt.title("predicted versus simulated %s %s" % (prop, bc))
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
    el = 21
    ns_val = [10, 10, 10, 10]
    set_id_val = ['randomD3D_val', 'transverseD3D_val',
                  'basaltransD3D_val', 'actualD3D_val']

    resptyp = 'Eeff'

    plot_check(el, ns_val, set_id_val, resptyp)
