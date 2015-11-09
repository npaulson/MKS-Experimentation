import numpy as np
import numpy.polynomial.legendre as leg
from scipy import interpolate
# import matplotlib.pyplot as plt


def get_nodes(xsamp, ysamp, a, b, N):

    tck = interpolate.splrep(xsamp, ysamp, k=3)

    # calculate legendre nodes and weights
    [xnode, weights] = leg.leggauss(N+1)

    # calculate locations of the legendre nodes scaled into the range [a,b]
    nodes_usc = 0.5*(xnode + 1.0)*(b-a)+a

    # calculate the strain value at the node locations
    ynode = interpolate.splev(nodes_usc, tck, der=0)

    return xnode, ynode, weights


def get_coeff(nodes, weights, rootsamp, N):

    coeff_set = np.zeros(N+1)

    for kk in xrange(0, N+1):

        # Pk is the 'kk'-th order legendre polynomial evaluated at the nodes of
        # the 'N+1'-st order legendre polynomial
        c = np.zeros(N+1)
        c[kk] = 1
        Pk = leg.legval(nodes, c)

        tmp = 0

        for ii in xrange(0, N+1):

            tmp += weights[ii]*rootsamp[ii]*Pk[ii]

        coeff_set[kk] = 0.5*(2*kk+1)*tmp

    return coeff_set


def get_interp(xinterp, coeff_set, a, b):

    # calculate locations of the desired interpolation points scaled into the
    # range [-1,1]
    xtemp = 2.0*((xinterp-a)/(b-a))-1.0
    yinterp = leg.legval(xtemp, coeff_set)

    return yinterp


if __name__ == "__main__":

    et_norm = np.load('et_norm.npy')
    ep = np.load('ep.npy')

    a = .0060  # start of range for legendre interpolation
    b = .0100  # end of range for legendre interpolation

    # highest order legendre polynomial in the fourier representation
    N = 20

    st_e = 0.0001

    # the following vector closely matches that of et_norm
    etvec = np.arange(a, b + st_e, st_e)

    ai = np.int8(np.round(a/st_e))-1
    bi = np.int8(np.round(b/st_e))-1

    xvar = et_norm[ai:bi+1]
    yvar = ep[ai:bi+1, 0]

    xnode, ynode, weights = get_nodes(etvec, yvar, a, b, N)

    coeff_set = get_coeff(xnode, ynode, weights, N)

    ytest = get_interp(xvar, coeff_set, a, b)

    # calculate error in this approach based on sampled values
    error = 100*np.abs((yvar - ytest)/xvar)

    print "number of samples: %s" % N
    print "mean error: %s%%" % np.mean(error)
    print "maximum error: %s%%" % np.max(error)

    # plt.figure(num=1, figsize=[10, 6])

    # plt.plot(xvar, yvar, 'bx')

    # # calculate locations of the legendre nodes scaled into the range [a, b]
    # nodes_usc = 0.5*(xnode + 1.0)*(b-a)+a
    # plt.plot(nodes_usc, ynode, 'bo')

    # xplt = np.linspace(a, b, 150)
    # yplt = get_interp(xplt, coeff_set, a, b)
    # plt.plot(xplt, yplt, 'r')

    # plt.show()
