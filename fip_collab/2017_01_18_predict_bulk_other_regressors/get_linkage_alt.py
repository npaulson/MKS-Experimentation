import numpy as np
import functions as rr
from constants import const
import h5py
import time
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import cross_val_predict


def linkage(par):

    st = time.time()

    C = const()

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

    f_reg = h5py.File("regression_results_L%s.hdf5" % C['H'], 'a')

    Rpred_cal_set = f_reg.create_dataset('Rpred_cal_%s' % par,
                                         (C['nC'], ns_cal_tot),
                                         dtype='float64')

    Rpred_val_set = f_reg.create_dataset('Rpred_val_%s' % par,
                                         (C['nC'], ns_val_tot),
                                         dtype='float64')

    f_reg.create_dataset('Rsim_cal_%s' % par, data=response_cal_tot)

    f_reg.create_dataset('Rsim_val_%s' % par, data=response_val_tot)

    for ii in xrange(C['nC']):

        C = C['Cset'][ii]

        # msg = "value of C: " + str(C)
        # rr.WP(msg, C['wrt_file'])

        model = MLPRegressor(hidden_layer_sizes=C, activation='relu',
                             alpha=0.0001, max_iter=200, solver='lbfgs')

        Rpred_cal = cross_val_predict(model, reduced_cal_tot,
                                      response_cal_tot, cv=3)
        Rpred_cal_set[ii, :] = Rpred_cal

        print "cv.mean(): %s" % np.mean(np.abs(Rpred_cal - response_cal_tot))

        model.fit(reduced_cal_tot, response_cal_tot)
        Rpred_val_set[ii, :] = model.predict(reduced_val_tot)

    f_reg.close()

    timeE = np.round(time.time()-st, 1)
    msg = "regressions and cross-validations completed: %s s" % timeE
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    par = 'c0'

    linkage(par)
