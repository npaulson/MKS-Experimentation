import numpy as np
import h5py
import time
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_predict


def linkage(C, par, typ):

    st = time.time()

    np.random.seed(0)

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

    f_reg.create_dataset('Rsim_cal_%s' % par, data=response_cal_tot)

    f_reg.create_dataset('Rsim_val_%s' % par, data=response_val_tot)

    order_set = f_reg.create_dataset('order_%s' % par,
                                     (n_ii*n_jj, 2),
                                     dtype='int64')

    if typ == 'NeuralNetwork':
        model = MLPRegressor(hidden_layer_sizes=(100,), activation='relu',
                             alpha=.01, max_iter=500, solver='lbfgs')
    elif typ == 'SupportVectorMachine':
        model = SVR(C=10, kernel='linear')
    elif typ == 'RandomForest':
        model = RandomForestRegressor(n_estimators=100)
    elif typ == 'KNeighbors':
        model = KNeighborsRegressor(n_neighbors=3)
    elif typ == 'Ridge':
        model = Ridge(alpha=0)  # when alpha=0 it is normal linear regression

    meanc = response_cal_tot.mean()
    c = 0

    for ii in xrange(n_ii):
        for jj in xrange(n_jj):
            n_pc = ii+1
            n_poly = jj+2

            order_set[c, :] = np.array([n_pc, n_poly])

            Rpred_cv = cross_val_predict(model, reduced_cal_tot[:, :n_pc],
                                         response_cal_tot, cv=10)
            Rpred_cv_set[c, :] = Rpred_cv

            # print "number of PCs: %s" % n_pc
            # print "degree of polynomial: %s" % str(n_poly-1)
            # print "cv.mean(): %s" % str(np.mean(np.abs(Rpred_cv - response_cal_tot))/meanc)

            model.fit(reduced_cal_tot[:, :n_pc], response_cal_tot)
            Rpred_cal_set[c, :] = model.predict(reduced_cal_tot[:, :n_pc])
            Rpred_val_set[c, :] = model.predict(reduced_val_tot[:, :n_pc])

            c += 1

    f_reg.close()

    timeE = np.round(time.time()-st, 1)
    print "regressions and cross-validations completed: %s s" % timeE


if __name__ == '__main__':
    par = 'c0'

    linkage(par)
