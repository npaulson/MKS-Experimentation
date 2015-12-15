import numpy as np
import matplotlib.pyplot as plt


def testfunc(x):
    return -.75*np.cos(x)+.25*np.sin(4*x)+0.53
    # return np.cos(x)**10


L = 2.*np.pi

N = 100  # number of samples
# xsamp = np.linspace(0, L, N)
xsamp = np.sort(np.random.rand(N))*L

ysamp = testfunc(xsamp)

Y = ysamp

# P = np.int64(np.floor(0.5*N))
P = 10

coeff = np.zeros(P, dtype=np.complex64)

X = np.zeros((N, P), dtype=np.complex64)

for p in xrange(P):

    p_ = p - np.floor(0.5*P)
    print p_
    print p

    X[:, p] = np.exp((1j*2*np.pi*p_*xsamp)/L)

Xc = X.conj().transpose()

XtX = np.dot(Xc, X)
XtY = np.dot(Xc, Y)

coeff = np.linalg.solve(XtX, XtY)

print np.round(coeff, 5)

plt.figure(1)

plt.subplot(121)
ax = plt.imshow(np.real(XtX), origin='lower',
                interpolation='none', cmap='jet')
plt.colorbar(ax)

plt.subplot(122)
ax = plt.imshow(np.imag(XtX), origin='lower',
                interpolation='none', cmap='jet')
plt.colorbar(ax)

plt.figure(2)

xplt = np.linspace(0, L, 150)
yplt = testfunc(xplt)

plt.plot(xplt, yplt, 'r-')
plt.plot(xsamp, ysamp, 'ro')

xtest = np.linspace(0, L, 2*N)
ytest = np.zeros(xtest.shape, dtype=np.complex64)

for p in xrange(P):
    p_ = p - np.floor(0.5*P)
    ytest += coeff[p]*np.exp((1j*2*np.pi*p_*xtest)/L)

plt.plot(xtest, np.real(ytest), 'bx')

plt.show()
