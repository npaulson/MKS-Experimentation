import numpy as np
import functions as rr
import h5py


def linkage(el, ns_set, set_id_set, wrt_file):

    """gather the input data"""

    f_red = h5py.File("sve_reduced.hdf5", 'a')
    f_link = h5py.File("linkage.hdf5", 'a')

    ns_tot = np.sum(ns_set)

    Eeff_tot = np.zeros(ns_tot, dtype='float64')
    reduced_tot = np.zeros((ns_tot, 20), dtype='complex128')

    c = 0
    for ii in xrange(len(set_id_set)):
        c_ = c + ns_set[ii]
        Eeff_tot[c:c_] = f_link.get('Eeff_%s' % set_id)[...]
        reduced_tot[c:c_, :] = f_red.get('reduced_%s' % set_id)[...]
        c = c_

    f_red.close()
    f_link.close()

    for pc in xrange(5):
        for deg in xrange(5):
            msg = "number of PCs: %s" % pc
            rr.WP(msg, wrt_file)
            msg = "degree of polynomial: %s" % deg
            rr.WP(msg, wrt_file)
             = rr.regress(reduced_tot, Eeff_tot, pc, deg)


if __name__ == '__main__':
    el = 21
    ns = 10
    set_id = 'transverseD3D'
    step = 1
    newdir = 'transverseD3D'
    wrt_file = 'test.txt'

    linkage(el, ns, set_id, step, newdir, wrt_file)
