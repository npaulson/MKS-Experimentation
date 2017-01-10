import numpy as np
import h5py
from sklearn import linear_model


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
l1 = np.int64(0.6*ns)
l2 = np.int64(0.8*ns)

X_cal = X[:l1, :]
y_cal = y[:l1]
X_cv = X[l1:l2, :]
y_cv = y[l1:l2]
X_test = X[l2:, :]
y_test = y[l2:]

"""try vector of regularization constants"""
C_vec = np.arange(-3, 4)
C_vec = 10. ** C_vec
err_vec = np.zeros(C_vec.size)

"""train and evaluate logistic classifiers"""
logreg = linear_model.LogisticRegression(C=1E1)
logreg.fit(X_cal, y_cal)

"""measure prediction accuracy for CV set"""
y_cv_pred = logreg.predict(X_cv)

err = np.mean(y_cv_pred == y_cv)
err_ = np.round(100*err, 3)

print "first 10 true digits followed by predicted digits:\n"
print y_cv[:10]
print y_cv_pred[:10]

print "prediction accuracy for cross-validation data: %s%%" % err_
