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

N = 10000  # number of samples
# xsamp = np.linspace(0, L, N)  # x samples
xsamp = np.random.rand(N)*L
ysamp = testfunc(xsamp)  # function value
xsamp = real2comm(xsamp, a, b)

Y = ysamp

P = 10  # order of highest order legendre polynomial used
coeff = np.zeros(P+1, dtype=np.complex64)

# X in Xt*X*B=Xt*Y
X = np.zeros((N, P+1))

for p in xrange(P+1):

    p_vec = np.zeros(p+1)
    p_vec[p] = 1
    X[:, p] = leg.legval(xsamp, p_vec)

Xc = X.conj().transpose()

XtX = np.dot(Xc, X)
print XtX[0, 0]
print XtX[-1, -1]
print XtX[0, -2]
print "XtX dimensions: %s" % XtX.shape[0]
print "rank(XtX): %s" % np.linalg.matrix_rank(XtX)

XtY = np.dot(Xc, Y)

# coeff: coefficients in legendre series used to represent function
coeff = np.linalg.solve(XtX, XtY)
print coeff

plt.figure(1)

ax = plt.imshow(XtX, origin='lower',
                interpolation='none', cmap='jet')
plt.colorbar(ax)
print XtX[0, 0]
print XtX[0, :]
print XtX[-2, 0]


plt.figure(2)

xplt = np.linspace(0, L, 1000)
yplt = testfunc(xplt)

plt.plot(xplt, yplt, 'r-')

xtest = np.linspace(0, L, 2*N)

ytest = np.zeros(xtest.shape, dtype=np.complex64)
for p in xrange(P+1):
    p_vec = np.zeros(p+1)
    p_vec[p] = 1
    ytest += coeff[p]*leg.legval(real2comm(xtest, a, b), p_vec)

plt.plot(xtest, np.real(ytest), 'bx')

plt.show()
