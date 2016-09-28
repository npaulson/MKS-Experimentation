# -*- coding: utf-8 -*-
import numpy as np
from constants import const
from sklearn.preprocessing import PolynomialFeatures


def regression(x, y, n_pc, n_poly):
    """compute the data matrices with dimensions
    n_samp x n_feat where the features contain all polynomial terms
    up to the specified degree"""

    poly = PolynomialFeatures(degree=(n_poly-1))
    X = poly.fit_transform(x[:, :n_pc])
    xmax = X.shape[1]

    XhX = np.dot(X.T, X)

    XhY = np.zeros(xmax, dtype='float64')
    for ii in xrange(xmax):
        XhY[ii] = np.dot(X[:, ii], y)

    coef = np.linalg.lstsq(XhX, XhY)[0]

    return coef


def prediction(x, coef, n_pc, n_poly):
    """compute the data matrices with dimensions
    n_samp x n_feat where the features contain all polynomial terms
    up to the specified degree"""

    poly = PolynomialFeatures(degree=(n_poly-1))
    X = poly.fit_transform(x[:, :n_pc])
    return np.dot(coef, X.T)


def loocv(x, y, n_pc, n_poly):
    err_raw = np.zeros((y.size,))
    for ii in xrange(y.size):

        tmp = np.ones((y.size,), dtype='bool')
        tmp[ii] = 0

        tmp_inv = tmp == 0

        coef = regression(x[tmp, :], y[tmp], n_pc, n_poly)
        ypred = prediction(x[tmp_inv, :], coef, n_pc, n_poly)

        err_raw[ii] = np.abs(y[tmp_inv]-ypred)

    return err_raw.mean(), err_raw.std()


def standard(x, y, n_pc, n_poly):

    C = const()

    coef = regression(x, y, n_pc, n_poly)

    y_predict = prediction(x, coef, n_pc, n_poly)

    err = np.abs(y-y_predict)
    meanerr = err.mean()
    maxerr = err.max()

    tmp = str([meanerr, maxerr])
    msg = "y mean and max error: %s" % tmp
    WP(msg, C['wrt_file'])
    tmp = str([y.min(), y.mean(), y.max()])
    msg = "y min mean and max: %s" % tmp
    WP(msg, C['wrt_file'])
    tmp = str([y_predict.min(), y_predict.mean(), y_predict.max()])
    msg = "y_predict min mean and max: %s" % tmp
    WP(msg, C['wrt_file'])

    return [y_predict, meanerr, maxerr, coef]


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
