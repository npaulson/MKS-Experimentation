import numpy as np
import matplotlib.pyplot as plt


def chebyshev_nodes(a, b, ai, en_inc, N):

    kk = np.arange(1, N+1)
    tmp = 0.5*(a+b)+0.5*(b-a)*np.cos(((2*kk - 1)*np.pi)/(2*N))
    xk = np.round(tmp, 4)
    sample_indx = np.unique(np.int64(xk/en_inc) - 1 - ai)


    return sample_indx


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


if __name__ == "__main__":

    et_norm = np.load('et_norm.npy')
    ep = np.load('ep.npy')

    a = .0060  # start of range for legendre interpolation
    b = .0100  # end of range for legendre interpolation

    N = 10

    en_inc = 0.0001

    # the following vector closely matches that of et_norm
    etvec = np.arange(a, b + en_inc, en_inc)

    ai = np.int8(np.round(a/en_inc))-1
    bi = np.int8(np.round(b/en_inc))-1

    xvar = et_norm[ai:bi+1]
    yvar = ep[ai:bi+1, 0]

    sample_indx = chebyshev_nodes(a, b, ai, en_inc, N)
    xnode = etvec[sample_indx]
    ynode = yvar[sample_indx]

    ytest = lagrange_interp(xnode, ynode, xvar)

    # calculate error in this approach based on sampled values
    error = 100*np.abs((yvar - ytest)/xvar)

    print "number of samples: %s" % N
    print "mean error: %s%%" % np.mean(error)
    print "maximum error: %s%%" % np.max(error)

    plt.figure(num=1, figsize=[10, 6])

    plt.plot(xnode, ynode, 'bo')
    plt.plot(xvar, yvar, 'bx')

    xplt = np.linspace(a, b, 150)
    yplt = lagrange_interp(xnode, ynode, xplt)
    plt.plot(xplt, yplt, 'r')

    plt.show()
