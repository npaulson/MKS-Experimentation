import numpy as np
import functions as rr
import reg_functions as rf
from constants import const
import h5py
import time


def linkage(par):

    st = time.time()

    C = const()

    # f_red = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'r')
    f_link = h5py.File("sample_L%s.hdf5" % C['H'], 'r')

    """gather the calibration data"""

    n_tot = len(C['sid'])

    ns_tot = n_tot*2*C['n_pc_samp']
    response_tot = np.zeros(ns_tot, dtype='float64')
    reduced_tot = np.zeros((ns_tot, C['n_pc_tot']), dtype='float64')

    c = 0
    p = 2*C['n_pc_samp']

    for ii in xrange(n_tot):
        c_ = c + p
        sid = C['sid'][ii]

        dset_name = "%s_%s" % (par, sid)
        response_tot[c:c_] = f_link.get(dset_name)[...]

        tmp = f_link.get('samp_%s' % sid)[...]
        reduced_tot[c:c_, :] = np.mean(tmp, 1)

        c = c_

    # f_red.close()
    f_link.close()

    """perform the regressions"""
    n_ii = C['n_pc_max']
    n_jj = C['deg_max']

    f_reg = h5py.File("regression_results_L%s.hdf5" % C['H'], 'a')

    Rpred_set = f_reg.create_dataset('Rpred_%s' % par,
                                     (n_ii*n_jj, ns_tot),
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

    loocv_mean = f_reg.create_dataset('LOOCVmean_%s' % par,
                                      (n_ii*n_jj,),
                                      dtype='float64')

    loocv_std = f_reg.create_dataset('LOOCVstd_%s' % par,
                                     (n_ii*n_jj,),
                                     dtype='float64')

    # coef_set = f_reg.create_dataset('coef_%s' % par,
    #                                 (n_ii*n_jj, coefmax),
    #                                 dtype='float64')

    c = 0
    for ii in xrange(n_ii):
        for jj in xrange(n_jj):
            n_pc = ii+1
            deg = jj+1

            msg = "number of PCs: %s" % n_pc
            rr.WP(msg, C['wrt_file'])
            msg = "degree of polynomial: %s" % str(deg)
            rr.WP(msg, C['wrt_file'])

            tmp = rf.standard(reduced_tot,
                              response_tot,
                              n_pc, deg)

            loocv_m, loocv_s = rf.loocv(reduced_tot,
                                        response_tot,
                                        n_pc, deg)

            Rpred = tmp[0]
            meanerr = tmp[1]
            maxerr = tmp[2]
            # coef = tmp[3]

            meanerr_set[c] = meanerr
            maxerr_set[c] = maxerr
            loocv_mean[c] = loocv_m
            loocv_std[c] = loocv_s
            msg = "loocv.mean(): %s" % loocv_m
            rr.WP(msg, C['wrt_file'])

            Rpred_set[c, :] = Rpred

            order_set[c, :] = np.array([n_pc, deg])
            # coef_set[c, :len(coef)] = coef

            c += 1

    f_reg.close()

    timeE = np.round(time.time()-st, 1)
    msg = "regressions and cross-validations completed: %s s" % timeE
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    par = 'mu'
    linkage(par)
