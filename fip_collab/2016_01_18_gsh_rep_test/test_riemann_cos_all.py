import numpy as np
import matplotlib.pyplot as plt


def test_func(xsamp):

    ysamp = 0.3+0.5*np.cos(3*xsamp) - \
        0.25*np.cos(2*3*xsamp) + \
        0.1*np.cos(4*3*xsamp)

    return ysamp


""" generate test function """

inc = 3

n_th = (120/inc)  # number of phi2 samples for FZ

inc2rad = inc*np.pi/180.

thvec = np.arange(n_th)*inc2rad

print thvec
y = test_func(thvec)

""" perform integration for coefficients """

n_l = 5
L = 2*np.pi/3.

coeff = np.zeros(n_l, dtype='float64')

bsz = L/y.size

for ii in xrange(n_l):

    if ii == 0:
        const = 1./L
    else:
        const = 2./L

    tmp = const*bsz*np.sum(y*np.cos(ii*3*thvec))
    coeff[ii] = tmp

print "coefficients from integration: %s" % np.str(coeff)

""" reconstruct the function """

y_ = np.zeros(y.size, dtype='float64')

for ii in xrange(n_l):

    y_ += coeff[ii]*np.cos(ii*3*thvec)


""" plot function and reconstruction """

plt.figure(1)

plt.plot(thvec, y, 'b')
plt.plot(thvec, y_, 'rx')

plt.show()
