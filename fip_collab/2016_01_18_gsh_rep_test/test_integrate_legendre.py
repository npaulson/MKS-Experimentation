import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.legendre as leg


def test_func(xsamp):

    # ysamp = 0.5*np.cos(3*xsamp) - \
    #     0.25*np.cos(2*3*xsamp) + \
    #     0.1*np.cos(4*3*xsamp)

    ysamp = np.exp(10*xsamp)

    return ysamp


def real2comm(x, a, b):
    return 2*((x-a)/(b-a))-1


def comm2real(x, a, b):
    return 0.5*(x+1)*(b-a)+a


""" generate test function """

inc = 1.
a = 0.
b = np.pi/3.
L = b-a
n_l = 10

n_th = (60/inc)  # number of phi2 samples for FZ

inc2rad = inc*np.pi/180.

thvec = (np.arange(n_th)+0.5)*inc2rad

print thvec
y = test_func(thvec)

""" perform integration for coefficients """

coeff = np.zeros(n_l, dtype='float64')

bsz = (np.pi/3.)/y.size

for ii in xrange(n_l):

    const = 2*ii+1

    p_vec = np.zeros(ii+1)
    p_vec[ii] = 1

    tmp = const*bsz*np.sum(y*leg.legval(real2comm(thvec, a, b), p_vec))
    coeff[ii] = tmp

print "coefficients from integration: %s" % np.str(coeff)

""" reconstruct the function """

y_ = np.zeros(y.size, dtype='float64')

for ii in xrange(n_l):

    p_vec = np.zeros(ii+1)
    p_vec[ii] = 1

    y_ += coeff[ii]*leg.legval(real2comm(thvec, a, b), p_vec)


""" plot function and reconstruction """

plt.figure(1)

plt.plot(thvec, y, 'b')
plt.plot(thvec, y_, 'rx')

plt.show()
