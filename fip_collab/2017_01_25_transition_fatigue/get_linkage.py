import numpy as np
import functions as rr
import reg_functions as rf
from constants import const
import h5py
import time
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import PolynomialFeatures
from sklearn import model_selection


def linkage(par, typ):

    st = time.time()

    C = const()
    p = C['n_sc']

    f_link = h5py.File("sample_L%s.hdf5" % C['H'], 'r')

    """gather the calibration data"""

    n_tot = len(C['sid'])
    ns_tot = n_tot*p
    groups = np.zeros(ns_tot, dtype='int16')
    response_tot = np.zeros(ns_tot, dtype='float64')
    reduced_tot = np.zeros((ns_tot, C['n_pc_tot']), dtype='float64')
    iscal = np.zeros((ns_tot,), dtype='bool')

    c = 0

    for ii in xrange(n_tot):
        c_ = c + p
        sid = C['sid'][ii]

        """flag elements of the calibration set"""
        if sid in C['sid_cal']:
            iscal[c:c_] = True

        groups[c:c_] = 2*ii+np.round(np.random.random((p,)))

        dset_name = "%s_%s" % (par, sid)
        response_tot[c:c_] = f_link.get(dset_name)[...]

        tmp = f_link.get('samp_%s' % sid)[...]

        reduced_tot[c:c_, :] = np.mean(tmp, 1)

        c = c_

    print groups

    f_link.close()

    """perform the regressions"""
    n_ii = C['deg_max']
    n_jj = C['n_pc_max']

    f_reg = h5py.File("regression_results_L%s.hdf5" % C['H'], 'a')

    order_set = f_reg.create_dataset('order_%s' % par,
                                     (n_ii*n_jj, 2),
                                     dtype='int64')

    f_reg.create_dataset('Rsim_%s' % par, data=response_tot)

    f_reg.create_dataset('iscal_%s' % par, data=iscal)

    Rpred_set = f_reg.create_dataset('Rpred_%s' % par,
                                     (n_ii*n_jj, ns_tot),
                                     dtype='float64')

    RpredCV_set = f_reg.create_dataset('RpredCV_%s' % par,
                                       (n_ii*n_jj, p*len(C['sid_cal'])),
                                       dtype='float64')

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
        model = Ridge(alpha=5)  # when alpha=0 it is normal linear regression

    # meanc = response_tot[iscal].mean()
    c = 0
    for ii in xrange(n_ii):
        for jj in xrange(n_jj):
            deg = ii+1
            n_pc = jj+1

            ords = np.array([deg, n_pc])
            order_set[c, :] = ords

            poly = PolynomialFeatures(deg)
            red = poly.fit_transform(reduced_tot[:, :n_pc])

            # gen = model_selection.KFold(n_splits=20)

            logo = model_selection.LeaveOneGroupOut()
            gen = logo.split(red[iscal, :], response_tot[iscal], groups[iscal])

            RpredCV = cross_val_predict(model, red[iscal, :],
                                        response_tot[iscal], cv=gen)

            RpredCV_set[c, :] = RpredCV

            model.fit(red[iscal, :], response_tot[iscal])
            Rpred_set[c, :] = model.predict(red)

            # loocv_err = rf.loocv(reduced_tot[iscal, :n_pc],
            #                      response_tot[iscal],
            #                      deg)
            # coef = rf.regression(reduced_tot[iscal, :n_pc],
            #                      response_tot[iscal],
            #                      deg)
            # pred = rf.prediction(reduced_tot[:, :n_pc],
            #                      coef,
            #                      deg)
            # loocv_set[c, :] = loocv_err
            # Rpred_set[c, :] = pred

            msg = "[deg, #PCs]: %s complete" % str(ords)
            rr.WP(msg, C['wrt_file'])
            # print "cv.mean(): %s" % str(np.mean(np.abs(RpredCV - response_tot[iscal]))/meanc)

            c += 1

    f_reg.close()

    timeE = np.round(time.time()-st, 1)
    msg = "regressions and cross-validations completed: %s s" % timeE
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    par = 'mu'
    linkage(par)
