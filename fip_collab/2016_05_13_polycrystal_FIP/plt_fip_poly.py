# -*- coding: utf-8 -*-
import functions as rr
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
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
    poly = PolynomialFeatures(degree=20)
    X = poly.fit_transform(np.log(x))
    clf = linear_model.LinearRegression()
    clf.fit(X, y)
    y_ = clf.predict(X)

    """plot the original data and the fits"""

    plt.figure()

    plt.plot(np.log(x), y, 'b.', markersize=3)
    plt.plot(np.log(x), y_, 'r-')

    ymin = y.min()
    ymax = y.max()
    rng = ymax - ymin
    ymin += -0.1*rng
    ymax += 0.1*rng

    plt.ylim((ymin, ymax))

    plt.show()
