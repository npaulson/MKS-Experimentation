import numpy as np
import functions as rr
import reg_functions as rf
from constants import const
import h5py
import time


def linkage(par):

    st = time.time()

    C = const()

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'r')
    f_link = h5py.File("responses.hdf5", 'r')

    """gather the calibration data"""

    n_tot = len(C['sid_split'])

    response_tot = np.zeros(n_tot, dtype='float64')
    reduced_tot = np.zeros((n_tot, C['n_pc_tot']), dtype='float64')

    for ii in xrange(n_tot):
        sid = C['sid_split'][ii]
        dset_name = "%s_%s" % (par, sid)
        response_tot[ii] = f_link.get(dset_name)[...]

        tmp = f_red.get('reduced_%s' % sid)[...]
        tmp = np.mean(tmp, axis=0)
        reduced_tot[ii, :] = tmp

    f_red.close()
    f_link.close()

    """perform the regressions"""
    n_ii = C['n_pc_max']
    n_jj = C['deg_max']

    f_reg = h5py.File("regression_results_L%s.hdf5" % C['H'], 'a')

    Rpred_set = f_reg.create_dataset('Rpred_%s' % par,
                                     (n_ii*n_jj, n_tot),
                                     dtype='float64')

    f_reg.create_dataset('Rsim_%s' % par, data=response_tot)

    order_set = f_reg.create_dataset('order_%s' % par,
                                     (n_ii*n_jj, 2),
                                     dtype='int64')

    meanerr_set = f_reg.create_dataset('meanerr_%s' % par,
                                       (n_ii*n_jj,),
                                       dtype='float64')

    maxerr_set = f_reg.create_dataset('maxerr_%s' % par,
                                      (n_ii*n_jj,),
                                      dtype='float64')

    loocv_err = f_reg.create_dataset('LOOCV_%s' % par,
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

            tmp = rf.standard(reduced_tot,
                              response_tot,
                              n_pc, n_poly)

            loocv_mean, loocv_std = rf.loocv(reduced_tot,
                                             response_tot,
                                             n_pc, n_poly)

            Rpred = tmp[0]
            meanerr = tmp[1]
            maxerr = tmp[2]
            # coef = tmp[6]

            meanerr_set[c] = meanerr
            maxerr_set[c] = maxerr
            loocv_err[c] = loocv_mean
            print "loocv.mean(): %s" % loocv_mean

            Rpred_set[c, :] = Rpred

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
