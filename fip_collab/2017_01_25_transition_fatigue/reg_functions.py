# -*- coding: utf-8 -*-
import numpy as np
from constants import const
from sklearn.preprocessing import PolynomialFeatures


def regression(x, y, deg):
    """compute the data matrices with dimensions
    n_samp x n_feat where the features contain all polynomial terms
    up to the specified degree"""

    poly = PolynomialFeatures(degree=deg)
    X = poly.fit_transform(x)
    xmax = X.shape[1]

    XhX = np.dot(X.T, X)

    XhY = np.zeros(xmax, dtype='float64')
    for ii in xrange(xmax):
        XhY[ii] = np.dot(X[:, ii], y)

    coef = np.linalg.lstsq(XhX, XhY)[0]

    return coef


def prediction(x, coef, deg):
    """compute the data matrices with dimensions
    n_samp x n_feat where the features contain all polynomial terms
    up to the specified degree"""

    poly = PolynomialFeatures(degree=deg)
    X = poly.fit_transform(x)
    return np.dot(coef, X.T)


def loocv(x, y, deg):
    err = np.zeros((y.size,))
    for ii in xrange(y.size):

        tmp = np.ones((y.size,), dtype='bool')
        tmp[ii] = 0

        tmp_inv = tmp == 0

        coef = regression(x[tmp, :], y[tmp], deg)
        ypred = prediction(x[tmp_inv, :], coef, deg)

        err[ii] = np.abs(y[tmp_inv]-ypred)

    return err


# def standard(x_cal, y_cal, x_val, y_val, n_pc, deg):

#     C = const()

#     coef = regression(x_cal, y_cal, n_pc, deg)

#     y_predict_cal = prediction(x_cal, coef, n_pc, deg)
#     y_predict_val = prediction(x_val, coef, n_pc, deg)

#     err = np.abs(y_cal-y_predict_cal)
#     err = np.abs(y_cal-y_predict_cal)
#     meanerr_cal = err.mean()
#     maxerr_cal = err.max()

#     # tmp = str([meanerr, maxerr])
#     # msg = "y mean and max error: %s" % tmp
#     # WP(msg, C['wrt_file'])
#     # tmp = str([y.min(), y.mean(), y.max()])
#     # msg = "y min mean and max: %s" % tmp
#     # WP(msg, C['wrt_file'])
#     # tmp = str([y_predict.min(), y_predict.mean(), y_predict.max()])
#     # msg = "y_predict min mean and max: %s" % tmp
#     # WP(msg, C['wrt_file'])

#     return [y_predict_cal, y_predict_val, meanerr_cal, maxerr, coef]


def WP(msg, filename):
    """
    Summary:
        This function takes an input message and a filename, and appends that
        message to the file. This function also prints the message
    Inputs:
        msg (string): the message to write and print.
        filename (string): the full name of the file to append to.
    Outputs:
        both prints the message and writes the message to the specified file
    """
    fil = open(filename, 'a')
    print msg
    fil.write(msg)
    fil.write('\n')
    fil.close()
