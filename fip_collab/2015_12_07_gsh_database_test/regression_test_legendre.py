import numpy as np
import numpy.polynomial.legendre as leg
import matplotlib.pyplot as plt


def testfunc(x):
    # return -.75*np.cos(x)+.25*np.cos(4*x)
    return np.cos(0.5*x)**10


def real2comm(x, a, b):
    return 2*((x-a)/(b-a))-1


def comm2real(x, a, b):
    return 0.5*(x+1)*(b-a)+a


a = 0
b = np.pi
L = b-a

print real2comm(3*(np.pi/4), a, b)
print comm2real(0.5, a, b)

N = 40  # number of samples
xsamp = np.linspace(0, L, N)  # x samples
ysamp = testfunc(xsamp)  # function value

Y = ysamp

P = 20  # order of highest order legendre polynomial used
coeff = np.zeros(P+1, dtype=np.complex64)

# X in Xt*X*B=Xt*Y
X = np.zeros((N, P+1))

for p in xrange(P+1):

    p_vec = np.zeros(p+1)
    p_vec[p] = 1
    X[:, p] = leg.legval(xsamp, p_vec)

Xc = X.conj().transpose()

# coeff: coefficients in legendre series used to represent function
coeff = np.linalg.solve(np.dot(Xc, X), np.dot(Xc, Y))
print coeff

plt.figure(1)

xplt = np.linspace(0, L, 1000)
yplt = testfunc(xplt)

plt.plot(xplt, yplt, 'r-')

xtest = np.linspace(0, L, 2*N)

ytest = np.zeros(xtest.shape, dtype=np.complex64)
for p in xrange(P+1):
    p_vec = np.zeros(p+1)
    p_vec[p] = 1
    ytest += coeff[p]*leg.legval(xtest, p_vec)

plt.plot(xtest, np.real(ytest), 'bx')

plt.show()
