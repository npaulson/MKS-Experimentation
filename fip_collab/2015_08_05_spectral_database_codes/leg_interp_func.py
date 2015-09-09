import numpy as np
import numpy.polynomial.legendre as leg
from scipy import interpolate
import matplotlib.pyplot as plt


def get_nodes(xsamp, ysamp, a, b, N):

    tck = interpolate.splrep(xsamp, ysamp, k=3)

    y_spline = interpolate.splev(xsamp, tck, der=0)
    error = 100*np.abs((ysamp - y_spline)/ysamp[95])

    if np.mean(error) > 1E-10:
        print "mean error for splines: %s%%" % np.mean(error)

    # calculate legendre nodes and weights
    [nodes, weights] = leg.leggauss(N+1)

    # calculate locations of the legendre nodes scaled into the range [a,b]
    nodes_usc = 0.5*(nodes + 1.0)*(b-a)+a

    # calculate the strain value at the node locations
    rootsamp = interpolate.splev(nodes_usc, tck, der=0)

    return nodes, weights, rootsamp


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

    et_norm = np.load('et_norm_02.npy')
    ep11 = np.load('ep11_02.npy')
    coeff_set = np.load('coeff_set_02.npy')

    a = .0064  # start of range for legendre interpolation
    b = .0096  # end of range for legendre interpolation

    # highest order legendre polynomial in the fourier representation
    N = 8

    # nodes, weights, rootsamp = get_nodes(et_norm, ep11, a, b, N)

    # coeff_set = get_coeff(nodes, weights, rootsamp, N)

    ytest = get_interp(et_norm[63:96], coeff_set, a, b)

    # calculate error in this approach based on sampled values
    error = 100*np.abs((ep11[63:96] - ytest)/np.max(np.abs(ep11[63:96])))

    print coeff_set
    print error
    print np.mean(error)
    print np.max(error)

    plt.figure(num=1, figsize=[10, 6])

    plt.plot(et_norm, ep11, 'bx')

    # calculate locations of the legendre nodes scaled into the range [a,b]
    # nodes_usc = 0.5*(nodes + 1.0)*(b-a)+a
    # plt.plot(nodes_usc, rootsamp, 'bo')

    xplt = np.linspace(a, b, 150)
    yplt = get_interp(xplt, coeff_set, a, b)
    plt.plot(xplt, yplt, 'r')

    plt.show()
