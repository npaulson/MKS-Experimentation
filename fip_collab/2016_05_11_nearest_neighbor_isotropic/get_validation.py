import numpy as np
import functions as rr
# import matplotlib.pyplot as plt
from constants import const
from sklearn.externals import joblib
import h5py
import time


def validate(ns, set_id):

    st = time.time()

    C = const()

    """load the feature data"""
    f = h5py.File("pre_regress_%s.hdf5" % set_id, 'r')
    X = f.get('X')[...]
    f.close()

    """gather the dependent variable data"""
    f = h5py.File("responses.hdf5", 'r')
    r_sim = f.get('y_sim_%s' % set_id)[...]
    r_sim = r_sim.reshape((ns*C['el']**3))
    f.close()

    """retrieve the fit from the regression"""
    clf = joblib.load('modelfit.pkl')

    """evalute the fit response"""
    r_fit = clf.predict(X)

    f = h5py.File('validation_%s.hdf5' % set_id, 'w')
    f.create_dataset('r_fit', data=r_fit)
    f.close()

    """evalute error metrics"""
    err = np.abs(r_sim-r_fit)
    err_mean = err.mean()
    err_max = err.max()

    r_sim_mmm = np.array([r_sim.min(), r_sim.mean(), r_sim.max()])
    r_fit_mmm = np.array([r_fit.min(), r_fit.mean(), r_fit.max()])

    print "r_sim min, mean and max: %s" % str(r_sim_mmm)
    print "r_fit min, mean and max: %s" % str(r_fit_mmm)

    print "mean error: %s" % err_mean
    print "max error: %s" % err_max

    timeE = np.round(time.time()-st, 1)
    msg = "validation completed for %s: %s s" % (set_id, timeE)
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    ns = 2
    set_id = "val"

    validate(ns, set_id)
