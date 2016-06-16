# -*- coding: utf-8 -*-
import numpy as np
from constants import const
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model


def regression(x, y, n_pc, n_poly):
    """compute the data matrices with dimensions
    n_samp x n_feat where the features contain all polynomial terms
    up to the specified degree"""

    poly = PolynomialFeatures(degree=(n_poly-1))
    X = poly.fit_transform(x[:, :n_pc])

    """set up the regression model"""
    clf = linear_model.LinearRegression(normalize=False)
    """fit the regression model"""
    clf.fit(X, y)
    coef = clf.coef_

    return clf, coef


def prediction(x, clf, n_pc, n_poly):
    """compute the data matrices with dimensions
    n_samp x n_feat where the features contain all polynomial terms
    up to the specified degree"""

    poly = PolynomialFeatures(degree=(n_poly-1))
    X = poly.fit_transform(x[:, :n_pc])
    return clf.predict(X)


def loocv(x, y, n_pc, n_poly):
    err_raw = np.zeros((y.size,))
    for ii in xrange(y.size):

        tmp = np.ones((y.size,), dtype='bool')
        tmp[ii] = 0

        tmp_inv = tmp == 0

        clf, coef = regression(x[tmp, :], y[tmp], n_pc, n_poly)
        ypred = prediction(x[tmp_inv, :], clf, n_pc, n_poly)

        err_raw[ii] = np.abs(y[tmp_inv]-ypred)

    return err_raw.mean(), err_raw.std()


# def regress(x_cal, x_val, y_cal, y_val, n_pc, n_poly):

#     C = const()

#     """compute the data matrices with dimensions
#     n_samp x n_feat where the features contain all polynomial terms
#     up to the specified degree"""
#     poly = PolynomialFeatures(degree=(n_poly-1))
#     X_cal = poly.fit_transform(x_cal[:, :n_pc])
#     X_val = poly.fit_transform(x_val[:, :n_pc])

#     """set up the regression model"""
#     clf = linear_model.LinearRegression(normalize=False)
#     """fit the regression model"""
#     clf.fit(X_cal, y_cal)
#     coef = clf.coef_

#     """validate with the calibration data"""
#     y_cal_predict = clf.predict(X_cal)

#     err = np.abs(y_cal-y_cal_predict)
#     meanerr_cal = err.mean()
#     maxerr_cal = err.max()

#     tmp = str([meanerr_cal, maxerr_cal])
#     msg = "y_cal mean and max error: %s" % tmp
#     rr.WP(msg, C['wrt_file'])
#     tmp = str([y_cal.min(), y_cal.mean(), y_cal.max()])
#     msg = "y_cal min mean and max: %s" % tmp
#     rr.WP(msg, C['wrt_file'])
#     tmp = str([y_cal_predict.min(), y_cal_predict.mean(), y_cal_predict.max()])
#     msg = "y_cal_predict min mean and max: %s" % tmp
#     rr.WP(msg, C['wrt_file'])

#     """cross-validate with the validation data"""
#     y_val_predict = clf.predict(X_val)

#     err = np.abs(y_val-y_val_predict)
#     meanerr_val = err.mean()
#     maxerr_val = err.max()

#     tmp = str([meanerr_val, maxerr_val])
#     msg = "y_val mean and max error: %s" % tmp
#     rr.WP(msg, C['wrt_file'])
#     tmp = str([y_cal.min(), y_val.mean(), y_val.max()])
#     msg = "y_val min mean and max: %s" % tmp
#     rr.WP(msg, C['wrt_file'])
#     tmp = str([y_val_predict.min(), y_val_predict.mean(), y_val_predict.max()])
#     msg = "y_val_predict min mean and max: %s" % tmp
#     rr.WP(msg, C['wrt_file'])

#     return [y_cal_predict, y_val_predict,
#             meanerr_cal, meanerr_val,
#             maxerr_cal, maxerr_val,
#             coef]