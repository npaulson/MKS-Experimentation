import numpy as np
import functions as rr
from constants import const
import h5py
import time


def linkage(par):

    st = time.time()

    C = const()

    f_red = h5py.File("spatial_reduced.hdf5", 'r')
    f_link = h5py.File("responses.hdf5", 'r')

    """gather the calibration data"""

    n_cal_tot = len(C['set_id_cal'])

    response_cal_tot = np.zeros(n_cal_tot, dtype='float64')
    reduced_cal_tot = np.zeros((n_cal_tot, C['n_pc_tot']), dtype='float64')

    for ii in xrange(n_cal_tot):
        set_id = C['set_id_cal'][ii]
        dset_name = "%s_%s" % (par, set_id)
        response_cal_tot[ii] = f_link.get(dset_name)[...]

        tmp = f_red.get('reduced_%s' % set_id)[...]
        tmp = np.mean(tmp, axis=0)
        reduced_cal_tot[ii, :] = tmp

    """gather the validation data"""

    n_val_tot = len(C['set_id_val'])

    response_val_tot = np.zeros(n_val_tot, dtype='float64')
    reduced_val_tot = np.zeros((n_val_tot, C['n_pc_tot']), dtype='float64')

    for ii in xrange(n_val_tot):
        set_id = C['set_id_val'][ii]
        dset_name = "%s_%s" % (par, set_id)
        response_val_tot[ii] = f_link.get(dset_name)[...]

        tmp = f_red.get('reduced_%s' % set_id)[...]
        tmp = np.mean(tmp, axis=0)
        reduced_val_tot[ii, :] = tmp

    f_red.close()
    f_link.close()

    """perform the regressions"""
    n_ii = C['n_pc_max']
    n_jj = C['n_poly_max']

    f_reg = h5py.File("regression_results.hdf5", 'a')

    Rpred_cal_set = f_reg.create_dataset('Rpred_cal_%s' % par,
                                         (n_ii*n_jj, n_cal_tot),
                                         dtype='float64')

    Rpred_val_set = f_reg.create_dataset('Rpred_val_%s' % par,
                                         (n_ii*n_jj, n_val_tot),
                                         dtype='float64')

    f_reg.create_dataset('Rsim_cal_%s' % par, data=response_cal_tot)

    f_reg.create_dataset('Rsim_val_%s' % par, data=response_val_tot)

    order_set = f_reg.create_dataset('order_%s' % par,
                                     (n_ii*n_jj, 2),
                                     dtype='int64')

    meanerr_cal_set = f_reg.create_dataset('meanerr_cal_%s' % par,
                                           (n_ii*n_jj,),
                                           dtype='float64')

    meanerr_val_set = f_reg.create_dataset('meanerr_val_%s' % par,
                                           (n_ii*n_jj,),
                                           dtype='float64')

    maxerr_cal_set = f_reg.create_dataset('maxerr_cal_%s' % par,
                                          (n_ii*n_jj,),
                                          dtype='float64')

    maxerr_val_set = f_reg.create_dataset('maxerr_val_%s' % par,
                                          (n_ii*n_jj,),
                                          dtype='float64')

    # coef_set = f_reg.create_dataset('coef_%s' % par,
    #                                 (n_ii*n_jj, coefmax),
    #                                 dtype='float64')

    c = 0
    for ii in xrange(n_ii):
        for jj in xrange(n_jj):
            n_pc = ii+1
            n_poly = jj+2

            msg = "number of PCs: %s" % n_pc
            rr.WP(msg, C['wrt_file'])
            msg = "degree of polynomial: %s" % str(n_poly-1)
            rr.WP(msg, C['wrt_file'])
            tmp = rr.regress(reduced_cal_tot, reduced_val_tot,
                             response_cal_tot, response_val_tot,
                             n_pc, n_poly)

            Rpred_cal = tmp[0]
            Rpred_val = tmp[1]
            meanerr_cal = tmp[2]
            meanerr_val = tmp[3]
            maxerr_cal = tmp[4]
            maxerr_val = tmp[5]
            # coef = tmp[6]

            meanerr_cal_set[c] = meanerr_cal
            meanerr_val_set[c] = meanerr_val
            maxerr_cal_set[c] = maxerr_cal
            maxerr_val_set[c] = maxerr_val

            Rpred_cal_set[c, :] = Rpred_cal
            Rpred_val_set[c, :] = Rpred_val

            order_set[c, :] = np.array([n_pc, n_poly])
            # coef_set[c, :len(coef)] = coef

            c += 1

    f_reg.close()

    timeE = np.round(time.time()-st, 1)
    msg = "regressions and cross-validations completed: %s s" % timeE
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    par = 'c0'

    linkage(par)
