import numpy as np
import matplotlib.pyplot as plt


def testfunc(x):
    return -.75*np.cos(x)+.25*np.cos(4*x)+0.53
    # return np.cos(x)**10


L = 2.*np.pi
N = 22  # number of samples
P = 10

xsamp = np.linspace(0, L/2, N)

ysamp = testfunc(xsamp)

Y = ysamp

coeff = np.zeros(P, dtype=np.complex128)

for p in xrange(P):

    # p_ = p - np.floor(0.5*P)
    p_ = p

    X = np.exp((1j*2*np.pi*p_*xsamp)/L)
    XhY = np.dot(X.conj(), Y)
    XhX = np.dot(X.conj(), X)

    coeff[p] = np.real(XhY/XhX)

print np.round(coeff, 5)

plt.figure(1)

xplt = np.linspace(0, L, 150)
yplt = testfunc(xplt)

plt.plot(xplt, yplt, 'r-')

xtest = np.linspace(0, L, 2*N)
ytest = np.zeros(xtest.shape, dtype=np.complex64)

for p in xrange(P):
    p_ = p
    # p_ = p - np.floor(0.5*P)
    ytest += coeff[p]*np.exp((1j*2*np.pi*p_*xtest)/L)

plt.plot(xtest, np.real(ytest), 'bx')

plt.show()
