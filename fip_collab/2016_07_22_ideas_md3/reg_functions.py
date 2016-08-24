# -*- coding: utf-8 -*-
import numpy as np
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


def standard(x_cal, x_val, y_cal, y_val, n_pc, n_poly):

    coef = regression(x_cal, y_cal, n_pc, n_poly)

    y_cal_predict = prediction(x_cal, coef, n_pc, n_poly)
    y_val_predict = prediction(x_val, coef, n_pc, n_poly)

    err = np.abs(y_cal-y_cal_predict)
    meanerr_cal = err.mean()
    maxerr_cal = err.max()

    # tmp = str([meanerr_cal, maxerr_cal])
    # msg = "y_cal mean and max error: %s" % tmp
    # WP(msg, C['wrt_file'])
    # tmp = str([y_cal.min(), y_cal.mean(), y_cal.max()])
    # msg = "y_cal min mean and max: %s" % tmp
    # WP(msg, C['wrt_file'])
    # tmp = str([y_cal_predict.min(), y_cal_predict.mean(), y_cal_predict.max()])
    # msg = "y_cal_predict min mean and max: %s" % tmp
    # WP(msg, C['wrt_file'])

    err = np.abs(y_val-y_val_predict)
    meanerr_val = err.mean()
    maxerr_val = err.max()

    # tmp = str([meanerr_val, maxerr_val])
    # msg = "y_val mean and max error: %s" % tmp
    # WP(msg, C['wrt_file'])
    # tmp = str([y_cal.min(), y_val.mean(), y_val.max()])
    # msg = "y_val min mean and max: %s" % tmp
    # WP(msg, C['wrt_file'])
    # tmp = str([y_val_predict.min(), y_val_predict.mean(), y_val_predict.max()])
    # msg = "y_val_predict min mean and max: %s" % tmp
    # WP(msg, C['wrt_file'])

    return [y_cal_predict, y_val_predict,
            meanerr_cal, meanerr_val,
            maxerr_cal, maxerr_val,
            coef]


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
