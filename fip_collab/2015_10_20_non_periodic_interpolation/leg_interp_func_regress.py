import numpy as np
import numpy.polynomial.legendre as leg
import matplotlib.pyplot as plt


def get_coeff(x_inp, y_inp, a, b, N):

    coeff_set = np.zeros(N+1)

    x_inp_S = 2.0*((x_inp-a)/(b-a))-1.0

    X = np.zeros([y_inp.size, N+1])

    for ii in xrange(N+1):

        cvec = np.zeros(N+1)
        cvec[ii] = 1

        X[:, ii] = leg.legval(x_inp_S, cvec)

    Xc = X.conj().transpose()

    coeff_set = np.linalg.solve(np.dot(Xc, X), np.dot(Xc, y_inp))

    return coeff_set


def get_interp(xinterp, coeff_set, a, b):

    # calculate locations of the desired interpolation points scaled into the
    # range [-1,1]
    xtemp = 2.0*((xinterp-a)/(b-a))-1.0
    yinterp = leg.legval(xtemp, coeff_set)

    return yinterp


if __name__ == "__main__":

    et_norm = np.load('et_norm.npy')
    ep11 = np.load('ep.npy')[:, 0]

    a = .0064  # start of range for legendre interpolation
    b = .0096  # end of range for legendre interpolation

    # highest order legendre polynomial in the fourier representation
    N = 20

    coeff_set = get_coeff(et_norm[63:96], ep11[63:96], a, b, N)

    ytest = get_interp(et_norm[63:96], coeff_set, a, b)

    # calculate error in this approach based on sampled values
    error = 100*np.abs((ep11[63:96] - ytest)/et_norm[63:96])

    print coeff_set
    print error
    print "mean error: %s%%" % np.mean(error)
    print "maximum error: %s%%" % np.max(error)

    plt.figure(num=1, figsize=[10, 6])

    plt.plot(et_norm, ep11, 'bx')

    # # calculate locations of the legendre nodes scaled into the range [a, b]
    # nodes_usc = 0.5*(nodes + 1.0)*(b-a)+a
    # plt.plot(nodes_usc, rootsamp, 'bo')

    xplt = np.linspace(a, b, 150)
    yplt = get_interp(xplt, coeff_set, a, b)

    plt.plot(xplt, yplt, 'r')

    plt.show()
