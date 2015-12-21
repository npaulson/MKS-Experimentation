import numpy as np
import matplotlib.pyplot as plt


def testfunc(x):
    return -.75*np.cos(x)+.25*np.cos(4*x)
    # return np.cos(x)**10


L = 2.*np.pi

N = 20  # number of samples
xsamp = np.linspace(0, L/2, N)

ysamp = testfunc(xsamp)

Y = ysamp

P = 10
coeff = np.zeros(P, dtype=np.complex64)

X = np.zeros((N, P), dtype=np.float64)

for p in xrange(P):

    # X[:, p] = np.exp((1j*2*np.pi*p*xsamp)/L).real
    X[:, p] = np.cos((2*np.pi*p*xsamp)/L)

Xc = X.conj().transpose()

XhX = np.dot(Xc, X)
XhY = np.dot(Xc, Y)

coeff = np.linalg.solve(XhX, XhY)

print np.round(coeff, 5)

plt.figure(1)

ax = plt.imshow(np.real(XhX), origin='lower',
                interpolation='none', cmap='jet')
plt.colorbar(ax)

plt.figure(2)

xplt = np.linspace(0, L, 150)
yplt = testfunc(xplt)

plt.plot(xplt, yplt, 'r-')

plt.plot(xsamp, ysamp, 'ro')

xtest = np.linspace(0, L, 2*N-1)

ytest = np.zeros(xtest.shape, dtype=np.complex64)
for p in xrange(P):
    # ytest += coeff[p]*np.exp((1j*2*np.pi*p*xtest)/L)
    ytest += coeff[p]*np.cos((2*np.pi*p*xtest)/L)

plt.plot(xtest, np.real(ytest), 'bx')

plt.show()
