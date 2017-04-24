# -*- coding: utf-8 -*-
import numpy as np
from constants import const


def regression(X, y):
    """compute the data matrices with dimensions
    n_samp x n_feat"""

    xmax = X.shape[1]

    XhX = np.dot(X.T, X)

    XhY = np.zeros(xmax, dtype='float64')
    for ii in xrange(xmax):
        XhY[ii] = np.dot(X[:, ii], y)

    coef = np.linalg.lstsq(XhX, XhY)[0]

    return coef


def prediction(X, coef):
    """compute the data matrices with dimensions
    n_samp x n_feat"""

    return np.dot(coef, X.T)


def cv(x, y, groups):
    pred = np.zeros((y.size,))

    for ii in np.unique(groups):
        ingrp = groups == ii
        outgrp = groups != ii

        coef = regression(x[outgrp, :], y[outgrp])
        ypred = prediction(x[ingrp, :], coef)

        pred[ingrp] = ypred

    return pred


def loocv(x, y):
    pred = np.zeros((y.size,))
    for ii in xrange(y.size):

        tmp = np.ones((y.size,), dtype='bool')
        tmp[ii] = 0

        tmp_inv = tmp == 0

        coef = regression(x[tmp, :], y[tmp])
        ypred = prediction(x[tmp_inv, :], coef)

        pred[ii] = ypred

    return pred


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
