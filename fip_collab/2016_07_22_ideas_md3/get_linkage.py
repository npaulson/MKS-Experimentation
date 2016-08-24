import numpy as np
from constants import const
import reg_functions as rf
import h5py


def linkage(C, par):

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'r')
    f_link = h5py.File("responses.hdf5", 'r')

    """gather the calibration data"""

    ns_cal_tot = np.sum(C['ns_cal'])

    response_cal_tot = np.zeros(ns_cal_tot, dtype='float64')
    reduced_cal_tot = np.zeros((ns_cal_tot, C['n_pc_tot']), dtype='float64')

    c = 0
    for ii in xrange(len(C['ns_cal'])):
        c_ = c + C['ns_cal'][ii]
        set_id = C['set_id_cal'][ii]
        dset_name = "%s_%s" % (par, set_id)
        response_cal_tot[c:c_] = f_link.get(dset_name)[...]
        reduced_cal_tot[c:c_, :] = f_red.get('reduced_%s' % set_id)[...]
        c = c_

    """gather the validation data"""

    ns_val_tot = np.sum(C['ns_val'])

    response_val_tot = np.zeros(ns_val_tot, dtype='float64')
    reduced_val_tot = np.zeros((ns_val_tot, C['n_pc_tot']), dtype='float64')

    c = 0
    for ii in xrange(len(C['ns_val'])):
        c_ = c + C['ns_val'][ii]
        set_id = C['set_id_val'][ii]
        dset_name = "%s_%s" % (par, set_id)
        response_val_tot[c:c_] = f_link.get(dset_name)[...]
        reduced_val_tot[c:c_, :] = f_red.get('reduced_%s' % set_id)[...]
        c = c_

    f_red.close()
    f_link.close()

    """perform the regressions"""

    n_ii = C['n_pc_max']
    n_jj = 1
    # n_jj = C['n_poly_max']

    f_reg = h5py.File("regression_results_L%s.hdf5" % C['H'], 'a')

    Rpred_cal_set = f_reg.create_dataset('Rpred_cal_%s' % par,
                                         (n_ii*n_jj, ns_cal_tot),
                                         dtype='float64')

    Rpred_val_set = f_reg.create_dataset('Rpred_val_%s' % par,
                                         (n_ii*n_jj, ns_val_tot),
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

    loocv_err = f_reg.create_dataset('meanerr_LOOCV_%s' % par,
                                     (n_ii*n_jj,),
                                     dtype='float64')

    c = 0
    for ii in xrange(n_ii):
        for jj in xrange(n_jj):
            n_pc = ii+1
            n_poly = jj+2

            # msg = "number of PCs: %s" % n_pc
            # rr.WP(msg, C['wrt_file'])
            # msg = "degree of polynomial: %s" % str(n_poly-1)
            # rr.WP(msg, C['wrt_file'])

            tmp = rf.standard(reduced_cal_tot, reduced_val_tot,
                              response_cal_tot, response_val_tot,
                              n_pc, n_poly)

            loocv_mean, loocv_std = rf.loocv(reduced_cal_tot,
                                             response_cal_tot,
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
            loocv_err[c] = loocv_mean
            # print "loocv.mean(): %s" % loocv_mean

            Rpred_cal_set[c, :] = Rpred_cal
            Rpred_val_set[c, :] = Rpred_val

            order_set[c, :] = np.array([n_pc, n_poly])
            # coef_set[c, :len(coef)] = coef

            c += 1

    f_reg.close()


if __name__ == '__main__':

    C = const()
    par = 'modulus'
    linkage(C, par)
