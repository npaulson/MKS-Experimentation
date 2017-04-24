import numpy as np
import h5py
import time
from sklearn.model_selection import cross_val_predict
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process.kernels import ConstantKernel as Const


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

    n_ii = C['n_pc_max']
    n_jj = C['n_poly_max']

    f_reg = h5py.File("regression_results_L%s.hdf5" % C['H'], 'a')

    Rpred_cal_set = f_reg.create_dataset('Rpred_cal_%s' % par,
                                         (n_ii*n_jj, ns_cal_tot),
                                         dtype='float64')

    Rpred_cv_set = f_reg.create_dataset('Rpred_cv_%s' % par,
                                        (n_ii*n_jj, ns_cal_tot),
                                        dtype='float64')

    Rpred_val_set = f_reg.create_dataset('Rpred_val_%s' % par,
                                         (n_ii*n_jj, ns_val_tot),
                                         dtype='float64')

    sigma_val_set = f_reg.create_dataset('sigma_val_%s' % par,
                                         (n_ii*n_jj, ns_val_tot),
                                         dtype='float64')

    f_reg.create_dataset('Rsim_cal_%s' % par, data=response_cal_tot_)

    f_reg.create_dataset('Rsim_val_%s' % par, data=response_val_tot_)


    order_set = f_reg.create_dataset('order_%s' % par,
                                     (n_ii*n_jj, 2),
                                     dtype='int64')

    # kernel = Const(1.0, (1e-3, 1e3)) * RBF(0.5, (1e-5, 1e5))
    kernel = RBF(0.7, (1e-5, 1e5))
    model = GaussianProcessRegressor(kernel=kernel)

    meanc = response_cal_tot.std()
    c = 0

    for ii in xrange(n_ii):
        for jj in xrange(n_jj):
            n_pc = ii+1
            n_poly = jj+2

            order_set[c, :] = np.array([n_pc, n_poly])

            Rpred_cv = cross_val_predict(model, reduced_cal_tot[:, :n_pc],
                                         response_cal_tot, cv=10)
            Rpred_cv_set[c, :] = (Rpred_cv*std_res)+mean_res

            # print "number of PCs: %s" % n_pc
            # print "degree of polynomial: %s" % str(n_poly-1)
            # print "cv.mean(): %s" % str(np.mean(np.abs(Rpred_cv - response_cal_tot))/meanc)

            model.fit(reduced_cal_tot[:, :n_pc], response_cal_tot)
            tmp = model.predict(reduced_cal_tot[:, :n_pc])
            Rpred_cal_set[c, :] = (tmp*std_res)+mean_res
            tmp = model.predict(reduced_val_tot[:, :n_pc], return_std=True)
            Rpred_val_set[c, :] = (tmp[0]*std_res)+mean_res
            sigma_val_set[c, :] = tmp[1]*std_res

            c += 1

    f_reg.close()

    timeE = np.round(time.time()-st, 1)
    print "regressions and cross-validations completed: %s s" % timeE


if __name__ == '__main__':
    par = 'c0'

    linkage(par)
