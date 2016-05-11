import numpy as np
import functions as rr
from constants import const
import h5py
import time
from sklearn.externals import joblib
# from sklearn import svm
# from sklearn import neighbors
from sklearn import tree


def regress(ns, set_id):

    st = time.time()

    C = const()

    """load the feature data"""
    f = h5py.File("pre_regress_%s.hdf5" % set_id, 'r')
    X = f.get('X')[...]
    f.close()

    """load the dependent variable data"""
    f = h5py.File("responses.hdf5", 'r')
    y = f.get('fip_%s' % set_id)[...]
    y = y.reshape((C['n_samp']))
    f.close()

    # clf = svm.SVR()
    # clf = neighbors.KNeighborsRegressor(n_neighbors=1, weights='uniform')
    clf = tree.DecisionTreeRegressor(max_depth=10)

    clf.fit(X, y)

    joblib.dump(clf, 'modelfit.pkl')

    timeE = np.round(time.time()-st, 1)
    msg = "fit completed: %s s" % timeE
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    ns = 2
    wrt_file = "test.txt"

    regress(ns, wrt_file)
