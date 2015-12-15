import numpy as np
import matplotlib.pyplot as plt


def testfunc(x):
    return -.75*np.cos(x)+.25*np.sin(4*x)
    # return np.cos(x)**10


L = 2.*np.pi

N = 40  # number of samples
xsamp = np.linspace(0, L, N)

ysamp = testfunc(xsamp)

Y = ysamp

P = N/2
coeff = np.zeros(P, dtype=np.complex64)

X = np.zeros((N, P))

for p in xrange(P):

    X[:, p] = np.exp((1j*2*np.pi*p*xsamp)/L)

Xc = X.conj().transpose()

coeff = np.linalg.solve(np.dot(Xc, X), np.dot(Xc, Y))

print np.round(coeff, 2)

plt.figure(1)

xplt = np.linspace(0, L, 150)
yplt = testfunc(xplt)

plt.plot(xplt, yplt, 'r-')

xtest = np.linspace(0, L, 2*N)

ytest = np.zeros(xtest.shape, dtype=np.complex64)
for p in xrange(P):
    ytest += coeff[p]*np.exp((1j*2*np.pi*p*xtest)/L)

plt.plot(xtest, np.real(ytest), 'bx')

plt.show()
