import numpy as np
import matplotlib.pyplot as plt


def chebyshev_nodes(a, b, N):

    kk = np.arange(1, N+1)
    xk = 0.5*(a+b)+0.5*(b-a)*np.cos(((2*kk - 1)*np.pi)/(2*N))

    return xk


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


def select_nodes(a, b, ai, bi, st_e, N, etvec, yvar):

    xk = np.round(chebyshev_nodes(a, b, N), 4)

    sample_indx = np.unique(np.int8(xk/st_e) - 1 - ai)

    xnode = etvec[sample_indx]

    ynode = yvar[sample_indx]

    return xnode, ynode


if __name__ == "__main__":

    et_norm = np.load('et_norm.npy')
    ep = np.load('ep.npy')

    a = .0060  # start of range for legendre interpolation
    b = .0100  # end of range for legendre interpolation

    N = 20

    st_e = 0.0001

    # the following vector closely matches that of et_norm
    etvec = np.arange(a, b + st_e, st_e)

    ai = np.int8(np.round(a/st_e))-1
    bi = np.int8(np.round(b/st_e))-1

    xvar = et_norm[ai:bi+1]
    yvar = ep[ai:bi+1, 0]

    xnode, ynode = select_nodes(a, b, ai, bi, st_e, N, etvec, yvar)

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
