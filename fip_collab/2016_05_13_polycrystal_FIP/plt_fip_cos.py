# -*- coding: utf-8 -*-
import functions as rr
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn import linear_model


if __name__ == '__main__':

    newdir = 'cal'
    pcnt = .0

    # nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    for filename in os.listdir(nwd):
        fip = rr.read_vtk_scalar(filename=filename)

    fip = np.sort(fip)

    """return to the original directory"""
    os.chdir('..')

    """get the data for the fit"""

    x = fip
    x = x[np.int64(pcnt*x.size):, None]

    y = (np.arange(x.size)+1)/np.float32(x.size)

    """get the desired fits"""
    xl = np.log(x)
    n_p = 5

    xlmax = xl.max()
    xlmin = xl.min()
    L_p = xlmax-xlmin

    X = np.zeros((x.size, n_p), dtype='float64')

    for ii in xrange(n_p):
        X[:, ii] = np.squeeze(np.cos((ii*np.pi*(xl-xlmin))/L_p))
        # X[:, ii] = np.squeeze(xl**ii)

    # XhX = np.dot(X.T, X)
    # Xhy = np.dot(X.T, y)
    # coef = np.linalg.lstsq(XhX, Xhy)[0]
    # print coef
    # y_ = np.dot(coef, X.T)

    weights = (1e-7)*np.ones(x.size, dtype='float64')
    weights[np.int16(.99*x.size):] = .01
    weights[0] = 1
    weights[-1] = 1

    # plt.figure(num=1)
    # plt.plot(xl, weights)

    clf = linear_model.LinearRegression()
    # clf.fit(X, y, sample_weight=weights)
    clf.fit(X, y)
    print clf.coef_
    y_ = clf.predict(X)

    """plot the original data and the fits"""

    plt.figure(num=2)

    plt.plot(xl, y, 'b.', markersize=3)
    plt.plot(xl, y_, 'r-')

    ymin = y.min()
    ymax = y.max()
    rng = ymax - ymin
    ymin += -0.1*rng
    ymax += 0.1*rng

    plt.ylim((ymin, ymax))

    plt.show()
