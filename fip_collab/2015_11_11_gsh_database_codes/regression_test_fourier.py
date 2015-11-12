import numpy as np
import matplotlib.pyplot as plt


def testfunc(x):
    return -.75*np.cos(x)+.25*np.cos(4*x)

L = 2.*np.pi

N = 20  # number of samples
xsamp = np.linspace(0, L/2, N)

ysamp = testfunc(xsamp)

Y = ysamp

P = 4
coeff = np.zeros(P+1, dtype=np.complex64)

X = np.zeros((N, P+1))

for p in xrange(P+1):

    X[:, p] = np.exp((1j*2*np.pi*p*xsamp)/L)

Xc = X.conj().transpose()

coeff = np.linalg.solve(np.dot(Xc, X), np.dot(Xc, Y))

print np.round(coeff, 2)

plt.figure(1)

xplt = np.linspace(0, L, 150)
yplt = testfunc(xplt)

plt.plot(xplt, yplt, 'r-')

xtest = np.linspace(0, L, 20)

ytest = np.zeros(xtest.shape, dtype=np.complex64)
for p in xrange(P+1):
    ytest += coeff[p]*np.exp((1j*2*np.pi*p*xtest)/L)

plt.plot(xtest, np.real(ytest), 'bx')

plt.show()