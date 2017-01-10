import numpy as np
import h5py
from sklearn.ensemble import GradientBoostingClassifier


"""Gradient Boosting Classification"""

"""load data"""
f = h5py.File('digits.hdf5', 'r')
X_ = f.get('X')[...]
y_ = f.get('y')[...]
f.close()

ns = y_.size

"""scramble data"""
seed = 0
np.random.seed(seed=seed)

tmp = np.arange(ns)
np.random.shuffle(tmp)

X = X_[tmp, :]
y = y_[tmp]

"""split data into calibration, cross-validation and test sets"""
l1 = np.int64(0.8*ns)
l2 = np.int64(0.9*ns)

X_cal = X[:l1, :]
y_cal = y[:l1]
X_cv = X[l1:l2, :]
y_cv = y[l1:l2]
X_test = X[l2:, :]
y_test = y[l2:]

"""try different numbers of decision trees in classifier"""
C_vec = np.arange(10, 200, 20)

n_C = len(C_vec)
acc_cv = np.zeros(n_C)
acc_test = np.zeros(n_C)

"""find best regularization constant with CV data"""
for ii in xrange(n_C):

    C = C_vec[ii]

    model = GradientBoostingClassifier(n_estimators=C)
    model.fit(X_cal, y_cal)

    """measure prediction accuracy"""
    y_cv_pred = model.predict(X_cv)
    y_test_pred = model.predict(X_test)

    acc = np.mean(y_cv_pred == y_cv)
    acc_ = np.round(100*acc, 3)
    acc_cv[ii] = acc_

    print "prediction accuracy, cross-validation data (C=%s): %s%%" % (C, acc_)

    acc = np.mean(y_test_pred == y_test)
    acc_ = np.round(100*acc, 3)
    acc_test[ii] = acc_

"""evaluate prediction accuracy with test data"""
inx = np.argmax(acc_cv)
acc_ = acc_test[inx]
C = C_vec[inx]

print "prediction accuracy, test data (C=%s): %s%%" % (C, acc_)

print "first 10 true digits followed by predicted digits:"
print y_test[:10]
print y_test_pred[:10]
