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

    """pick the number of principal components used based on
    explained variance"""

    f_ev = h5py.File("pca_data.hdf5", 'r')
    ratios = f_ev.get('ratios')[...]
    f_ev.close()

    tmp = np.cumsum(ratios)
    print tmp

    tmp1 = tmp >= C['ev_lvl']
    tmp2 = np.arange(len(tmp1))[tmp1]

    ii = tmp2[0]

    print ii

    n_pc = ii + 1

    """pick the number of polynomial coefficeints"""
    n_poly = 2

    """perform the regressions"""

    # coefmax = (ii+1)

    f_reg = h5py.File("regression_results.hdf5", 'a')

    Rpred_cal_set = f_reg.create_dataset('Rpred_cal_%s' % par,
                                         (ns_cal_tot,),
                                         dtype='float64')

    Rpred_val_set = f_reg.create_dataset('Rpred_val_%s' % par,
                                         (ns_val_tot,),
                                         dtype='float64')

    f_reg.create_dataset('Rsim_cal_%s' % par, data=response_cal_tot)

    f_reg.create_dataset('Rsim_val_%s' % par, data=response_val_tot)

    order_set = f_reg.create_dataset('order_%s' % par,
                                     (2,),
                                     dtype='int64')

    # coef_set = f_reg.create_dataset('coef_%s' % par,
    #                                 (coefmax,),
    #                                 dtype='float64')

    msg = "number of PCs: %s" % n_pc
    rr.WP(msg, C['wrt_file'])
    msg = "degree of polynomial: %s" % str(n_poly-1)
    rr.WP(msg, C['wrt_file'])
    tmp = rr.regress(reduced_cal_tot, reduced_val_tot,
                     response_cal_tot, response_val_tot,
                     n_pc, n_poly)

    Rpred_cal = tmp[0]
    Rpred_val = tmp[1]
    # coef = tmp[6]

    Rpred_cal_set[:] = Rpred_cal
    Rpred_val_set[:] = Rpred_val

    order_set[:] = np.array([n_pc, n_poly])
    # coef_set[:len(coef)] = coef

    c += 1

    timeE = np.round(time.time()-st, 1)
    msg = "regressions and cross-validations completed: %s s" % timeE
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    par = 'c0'

    linkage(par)
