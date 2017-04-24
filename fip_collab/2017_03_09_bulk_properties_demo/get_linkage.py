import numpy as np
import h5py
import time
import reg_functions as rf
from sklearn.preprocessing import PolynomialFeatures


def linkage(C, par):

    st = time.time()

    np.random.seed(0)

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'r')
    f_link = h5py.File("responses.hdf5", 'r')

    """gather the calibration data"""

    ns_cal_tot = np.sum(C['ns_cal'])

    response_cal_tot_ = np.zeros(ns_cal_tot, dtype='float64')
    reduced_cal_tot_ = np.zeros((ns_cal_tot, C['n_pc_tot']), dtype='float64')

    c = 0
    for ii in xrange(len(C['ns_cal'])):
        c_ = c + C['ns_cal'][ii]
        set_id = C['set_id_cal'][ii]
        dset_name = "%s_%s" % (par, set_id)
        response_cal_tot_[c:c_] = f_link.get(dset_name)[...]
        reduced_cal_tot_[c:c_, :] = f_red.get('reduced_%s' % set_id)[...]
        c = c_

    """gather the validation data"""

    ns_val_tot = np.sum(C['ns_val'])

    response_val_tot_ = np.zeros(ns_val_tot, dtype='float64')
    reduced_val_tot_ = np.zeros((ns_val_tot, C['n_pc_tot']), dtype='float64')

    c = 0
    for ii in xrange(len(C['ns_val'])):
        c_ = c + C['ns_val'][ii]
        set_id = C['set_id_val'][ii]
        dset_name = "%s_%s" % (par, set_id)
        response_val_tot_[c:c_] = f_link.get(dset_name)[...]
        reduced_val_tot_[c:c_, :] = f_red.get('reduced_%s' % set_id)[...]
        c = c_

    f_red.close()
    f_link.close()

    """scale pc scores so that mean and standard deviation
    of the calibration scores are 0 and 1 respectively (for each PC)"""
    mean_red = np.mean(reduced_cal_tot_, 0)
    std_red = np.std(reduced_cal_tot_, 0)
    reduced_cal_tot = (reduced_cal_tot_ - mean_red)/std_red
    reduced_val_tot = (reduced_val_tot_ - mean_red)/std_red

    """scale responses so that mean and standard deviation
    of the calibration responses are 0 and 1 respectively"""
    mean_res = np.mean(response_cal_tot_)
    std_res = np.std(response_cal_tot_)
    response_cal_tot = (response_cal_tot_ - mean_res)/std_res

    """perform the regressions"""

    f_reg = h5py.File("regression_results_L%s.hdf5" % C['H'], 'a')

    Rpred_cal_set = f_reg.create_dataset('Rpred_cal_%s' % par,
                                         (C['pcdeg'].shape[0], ns_cal_tot),
                                         dtype='float64')

    Rpred_cv_set = f_reg.create_dataset('Rpred_cv_%s' % par,
                                        (C['pcdeg'].shape[0], ns_cal_tot),
                                        dtype='float64')

    Rpred_val_set = f_reg.create_dataset('Rpred_val_%s' % par,
                                         (C['pcdeg'].shape[0], ns_val_tot),
                                         dtype='float64')

    f_reg.create_dataset('Rsim_cal_%s' % par, data=response_cal_tot_)

    f_reg.create_dataset('Rsim_val_%s' % par, data=response_val_tot_)

    order_set = f_reg.create_dataset('order_%s' % par,
                                     (C['pcdeg'].shape[0], 2),
                                     dtype='int64')

    for ii in xrange(C['pcdeg'].shape[0]):

        n_pc = C['pcdeg'][ii, 0]
        deg = C['pcdeg'][ii, 1]

        order_set[ii, :] = np.array([n_pc, deg])

        poly = PolynomialFeatures(deg)
        Xcal = poly.fit_transform(reduced_cal_tot[:, :n_pc])
        Xval = poly.fit_transform(reduced_val_tot[:, :n_pc])

        Rpred_cv = rf.loocv(Xcal, response_cal_tot)
        Rpred_cv_set[ii, :] = (Rpred_cv*std_res)+mean_res

        coef = rf.regression(Xcal, response_cal_tot)

        tmp = rf.prediction(Xcal, coef)
        Rpred_cal_set[ii, :] = (tmp*std_res)+mean_res

        tmp = rf.prediction(Xval, coef)
        Rpred_val_set[ii, :] = (tmp*std_res)+mean_res

    f_reg.close()

    timeE = np.round(time.time()-st, 1)
    print "regressions and cross-validations completed: %s s" % timeE


if __name__ == '__main__':
    par = 'c0'

    linkage(par)
