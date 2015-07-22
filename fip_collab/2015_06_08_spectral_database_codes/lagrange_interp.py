import numpy as np


def lagrange_interp(x, y, xx):
    """
    pseudocode from Numerical Methods for Engineers, Chapra and Canale 6th
    """

    n = len(x)-1
    summ = np.zeros(xx.shape)
    for ii in xrange(0, n+1):
        product = y[ii]*np.ones(xx.shape)

        for jj in xrange(0, n+1):

            if ii != jj:
                product = product*((xx-x[jj])/(x[ii]-x[jj]))

        summ += product

    return summ
