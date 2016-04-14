import numpy as np
import functions as rr
import h5py
import time


def linkage(el, ns_cal_set, ns_val_set,
            set_id_cal_set, set_id_val_set, resptyp, wrt_file):

    st = time.time()

    f_red = h5py.File("sve_reduced.hdf5", 'r')
    f_link = h5py.File("linkage.hdf5", 'r')

    """gather the calibration data"""

    ns_cal_tot = np.sum(ns_cal_set)

    response_cal_tot = np.zeros(ns_cal_tot, dtype='float64')
    reduced_cal_tot = np.zeros((ns_cal_tot, 20), dtype='complex128')

    c = 0
    for ii in xrange(len(set_id_cal_set)):
        c_ = c + ns_cal_set[ii]
        set_id = set_id_cal_set[ii]
        response_cal_tot[c:c_] = f_link.get('%s_%s' % (resptyp, set_id))[...]
        reduced_cal_tot[c:c_, :] = f_red.get('reduced_%s' % set_id)[...]
        c = c_

    """gather the validation data"""

    ns_val_tot = np.sum(ns_val_set)

    response_val_tot = np.zeros(ns_val_tot, dtype='float64')
    reduced_val_tot = np.zeros((ns_val_tot, 20), dtype='complex128')

    c = 0
    for ii in xrange(len(set_id_val_set)):
        c_ = c + ns_val_set[ii]
        set_id = set_id_val_set[ii]
        response_val_tot[c:c_] = f_link.get('%s_%s' % (resptyp, set_id))[...]
        reduced_val_tot[c:c_, :] = f_red.get('reduced_%s' % set_id)[...]
        c = c_

    f_red.close()
    f_link.close()

    """perform the regressions"""

    n_ii = 5
    n_jj = 5
    coefmax = (n_ii+1)*(n_jj+2)

    f_reg = h5py.File("regression_results.hdf5", 'w')

    order_set = f_reg.create_dataset('order',
                                     (n_ii*n_jj, 2),
                                     dtype='int64')
    meanerr_set = f_reg.create_dataset('meanerr',
                                       (n_ii*n_jj,),
                                       dtype='float64')
    maxerr_set = f_reg.create_dataset('maxerr',
                                      (n_ii*n_jj,),
                                      dtype='float64')
    coef_set = f_reg.create_dataset('coef',
                                    (n_ii*n_jj, coefmax),
                                    dtype='complex128')
    resppred_set = f_reg.create_dataset('Rpred',
                                        (n_ii*n_jj, ns_val_tot),
                                        dtype='float64')

    f_reg.create_dataset('Rsim', data=response_val_tot)

    c = 0
    for ii in xrange(n_ii):
        for jj in xrange(n_jj):
            n_pc = ii+1
            n_poly = jj+2

            msg = "number of PCs: %s" % n_pc
            rr.WP(msg, wrt_file)
            msg = "degree of polynomial: %s" % str(n_poly-1)
            rr.WP(msg, wrt_file)
            tmp = rr.regress(reduced_cal_tot, reduced_val_tot,
                             response_cal_tot, response_val_tot,
                             n_pc, n_poly)

            err_mean = tmp[0]
            err_max = tmp[1]
            coef = tmp[2]
            response_val_tot_ = tmp[3]

            order_set[c, :] = np.array([n_pc, n_poly])
            meanerr_set[c] = err_mean
            maxerr_set[c] = err_max
            coef_set[c, :len(coef)] = coef
            resppred_set[c, :ns_val_tot] = response_val_tot_

            c += 1

    f_reg.close()

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
