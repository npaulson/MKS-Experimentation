import numpy as np
import h5py
from sklearn.neural_network import MLPClassifier


def loaddata(fname):

    f = h5py.File('digits.hdf5', 'r')
    X = f.get('X')[...]
    y = f.get('y')[...]
    f.close()

    return X, y


def getsets(X, y, cv_frac, test_frac):

    ns = y.size

    """scramble data"""
    seed = 0
    np.random.seed(seed=seed)

    tmp = np.arange(ns)
    np.random.shuffle(tmp)

    X = X[tmp, :]
    y = y[tmp]

    """split data into calibration, cross-validation and test sets"""
    l1 = np.int64((1-cv_frac-test_frac)*ns)
    l2 = np.int64((1-test_frac)*ns)

    X_cal = X[:l1, :]
    y_cal = y[:l1]
    X_cv = X[l1:l2, :]
    y_cv = y[l1:l2]
    X_test = X[l2:, :]
    y_test = y[l2:]

    return X_cal, y_cal, X_cv, y_cv, X_test, y_test


def modeltype(C):

    l_sizes = (125,)
    model = MLPClassifier(hidden_layer_sizes=l_sizes, activation='relu',
                          alpha=C, max_iter=200, solver='lbfgs')

    C_vec = np.arange(-7, 1)
    C_vec = 10. ** C_vec  # contains regularization parameter options

    return C_vec, model


X, y = loaddata('digits.hdf5')

cv_frac = 0.1
test_frac = 0.1
X_cal, y_cal, X_cv, y_cv, X_test, y_test = getsets(X, y, cv_frac, test_frac)

C_vec, model = modeltype(0)
n_C = len(C_vec)

acc_cv = np.zeros(n_C)
acc_test = np.zeros(n_C)

"""find best regularization constant with CV data"""
for ii in xrange(n_C):

    C = C_vec[ii]

    tmp, model = modeltype(C)
    model.fit(X_cal, y_cal)

    """measure prediction accuracy"""
    y_cv_pred = model.predict(X_cv)

    acc = np.mean(y_cv_pred == y_cv)
    acc_ = np.round(100*acc, 3)
    acc_cv[ii] = acc_

    print "prediction accuracy, cross-validation data (C=%s): %s%%" % (C, acc_)

"""evaluate prediction accuracy with test data"""
inx = np.argmax(acc_cv)
C = C_vec[inx]

tmp, model = modeltype(C)
model.fit(X_cal, y_cal)

y_test_pred = model.predict(X_test)

acc = np.mean(y_test_pred == y_test)
acc = np.round(100*acc, 3)

print "prediction accuracy, test data (C=%s): %s%%" % (C, acc)

print "first 10 true digits followed by predicted digits:"
print y_test[:10]
print y_test_pred[:10]
