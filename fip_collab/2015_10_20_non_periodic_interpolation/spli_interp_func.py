import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


def interp_prep(ai, bi, st_e, st_i, xvar, yvar):

    tmp = np.arange(ai, bi+1, st_i)
    tmp = (bi-tmp[-1]) + tmp
    node_indx = tmp - ai

    xnode = xvar[node_indx]
    ynode = yvar[node_indx]

    # tck = interpolate.splrep(xnode, ynode, k=5, s=0)
    tck = interpolate.splrep(xnode, ynode, k=3)

    return tck, ai, bi, xnode, ynode


if __name__ == "__main__":

    et_norm = np.load('et_norm.npy')
    ep = np.load('ep.npy')

    a = .0060  # start of range for legendre interpolation
    b = .0100  # end of range for legendre interpolation

    st_e = 0.0001
    st_i = 11

    # the following vector closely matches that of et_norm
    etvec = np.arange(a, b + st_e, st_e)

    ai = np.int8(np.round(a/st_e))-1
    bi = np.int8(np.round(b/st_e))-1

    xvar = et_norm[ai:bi+1]
    yvar = ep[ai:bi+1, 0]

    tck, ai, bi, xnode, ynode = interp_prep(ai, bi, st_e, st_i, etvec, yvar)

    N = xnode.size

    ytest = interpolate.splev(xvar, tck, der=0)

    # calculate error in this approach based on sampled values
    error = 100*np.abs((yvar - ytest)/xvar)

    print "number of samples: %s" % N
    print "mean error: %s%%" % np.mean(error)
    print "maximum error: %s%%" % np.max(error)

    # plot functions of interest
    plt.figure(num=1, figsize=[10, 6])

    plt.plot(xvar, yvar, 'bx')
    plt.plot(xnode, ynode, 'bo')

    xplt = np.linspace(a, b, 150)
    yplt = interpolate.splev(xplt, tck, der=0)
    plt.plot(xplt, yplt, 'r')

    plt.show()
