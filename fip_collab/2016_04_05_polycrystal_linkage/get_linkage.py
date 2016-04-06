import numpy as np
import functions as rr
import h5py
import time


def linkage(el, ns_cal_set, ns_val_set,
            set_id_cal_set, set_id_val_set, wrt_file):

    st = time.time()

    f_red = h5py.File("sve_reduced.hdf5", 'a')
    f_link = h5py.File("linkage.hdf5", 'a')

    """gather the calibration data"""

    ns_cal_tot = np.sum(ns_cal_set)

    Eeff_cal_tot = np.zeros(ns_cal_tot, dtype='float64')
    reduced_cal_tot = np.zeros((ns_cal_tot, 20), dtype='complex128')

    c = 0
    for ii in xrange(len(set_id_cal_set)):
        c_ = c + ns_cal_set[ii]
        set_id = set_id_cal_set[ii]
        Eeff_cal_tot[c:c_] = f_link.get('Eeff_%s' % set_id)[...]
        reduced_cal_tot[c:c_, :] = f_red.get('reduced_%s' % set_id)[...]
        c = c_

    """gather the validation data"""

    ns_val_tot = np.sum(ns_val_set)

    Eeff_val_tot = np.zeros(ns_val_tot, dtype='float64')
    reduced_val_tot = np.zeros((ns_val_tot, 20), dtype='complex128')

    c = 0
    for ii in xrange(len(set_id_val_set)):
        c_ = c + ns_val_set[ii]
        set_id = set_id_val_set[ii]
        Eeff_val_tot[c:c_] = f_link.get('Eeff_%s' % set_id)[...]
        reduced_val_tot[c:c_, :] = f_red.get('reduced_%s' % set_id)[...]
        c = c_

    f_red.close()

    """perform the regressions"""

    n_pc_max = 5
    n_poly_max = 5
    coefmax = n_pc_max*n_poly_max

    regression_results = np.zeros((n_pc_max, n_poly_max, coefmax+2),
                                  dtype='complex128')

    for n_pc in xrange(1, 3):
        for n_poly in xrange(2, 4):
            msg = "number of PCs: %s" % n_pc
            rr.WP(msg, wrt_file)
            msg = "degree of polynomial: %s" % str(n_poly-1)
            rr.WP(msg, wrt_file)
            err_mean, err_max, coef = rr.regress(reduced_cal_tot,
                                                 reduced_val_tot,
                                                 Eeff_cal_tot,
                                                 Eeff_val_tot,
                                                 n_pc, n_poly)

            regression_results[n_pc, n_poly, 0] = err_mean
            regression_results[n_pc, n_poly, 1] = err_max
            regression_results[n_pc, n_poly, 2:(2+len(coef))] = coef

    # f_link.create_dataset('regression_results', data=regression_results)
    f_link.close()

    timeE = np.round(time.time()-st, 1)
    msg = "regressions and cross-validations completed: %s s" % timeE
    rr.WP(msg, wrt_file)


if __name__ == '__main__':
    el = 21
    ns = 10
    set_id = 'transverseD3D'
    step = 1
    newdir = 'transverseD3D'
    wrt_file = 'test.txt'

    linkage(el, ns, set_id, step, newdir, wrt_file)
