import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def ftest(x1, x2):
    return .5*np.cos(x1)-.2*np.cos(3*x1)*np.cos(2*x2)+.3*np.cos(x2)


def basis(x1, x2, ii, jj, x1max, x2max):
    return np.cos((2*np.pi*ii*x1)/x1max) *\
        np.cos((2*np.pi*jj*x2)/x2max)


def standard_reg(X, Y, Imat):

    Imax = Imat.shape[0]

    Xc = X.conj().transpose()

    XhX = np.dot(Xc, X)
    XhY = np.dot(Xc, Y)

    plt.figure(num=10, figsize=[4, 4])

    coeff = np.linalg.solve(XhX, XhY)

    coeff_ = coeff.reshape(np.sqrt(Imax), np.sqrt(Imax))
    plt.imshow(coeff_, origin='lower',
               interpolation='none', cmap='jet')
    plt.title("Fourier Coefficients")
    plt.colorbar()

    return coeff


def orthogonal_reg(X, y, Imat):

    Imax = Imat.shape[0]

    coeff = np.zeros(Imax, dtype='float64')

    for I in xrange(Imax):

        beval = X[:, I]

        # XhX = np.sum(beval.conj()*beval)
        # XhY = np.sum(beval.conj()*y)

        XhX = np.sum(beval[:-1].conj()*beval[:-1])
        XhY = np.sum(beval[:-1].conj()*y[:-1])

        print XhX

        coeff[I] = XhY/XhX

    return coeff


def NC0(X, y, Imat):

    Imax = Imat.shape[0]
    coeff = np.zeros(Imax, dtype='float64')

    for I in xrange(Imax):

        beval = X[:, I]

        interior = np.sum(beval[:-1].conj()*y[:-1])

        ii, jj = Imat[I, :]

        if ii == 0 and jj == 0:
            const = (1.*inc**2)/(.5*x1max*.5*x2max)
        elif ii == 0 or jj == 0:
            const = (2.*inc**2)/(.5*x1max*.5*x2max)
        else:
            const = (4.*inc**2)/(.5*x1max*.5*x2max)

        print 1./const

        coeff[I] = const*interior

    return coeff


x1max = 2*np.pi
x2max = 2*np.pi

n_x1 = 41
n_x2 = 41

x1vec = np.linspace(0, x1max/2., n_x1)
x2vec = np.linspace(0, x2max/2., n_x2)

inc = x1vec[1] - x1vec[0]
print "inc: %s" % inc
print "inc**2: %s" % inc**2
print "(.25*x1max*x2max)/(inc**2): %s" % str((.25*x1max*x2max)/(inc**2))

x1, x2 = np.meshgrid(x1vec, x2vec)
x1 = x1.swapaxes(0, 1)
x2 = x2.swapaxes(0, 1)

# n_tot = n_x1*n_x2
# x1 = np.random.rand(n_tot)*x1max/2.
# x2 = np.random.rand(n_tot)*x2max/2.

y = ftest(x1, x2)
print y.shape


""" Perform the regression """

Nii = 4
Njj = 4

Imax = Nii*Njj

Imat = np.unravel_index(np.arange(Imax), [Nii, Njj])
Imat = np.array(Imat).T

x1_ = x1.reshape(x1.size)
x2_ = x2.reshape(x2.size)

X = np.zeros((x1.size, Imax), dtype=np.float64)

for I in xrange(Imax):

    ii, jj = Imat[I, :]

    X[:, I] = basis(x1_, x2_, ii, jj, x1max, x2max)

y_ = y.reshape(y.size)

coeff1 = NC0(X, y_, Imat)
# coeff = standard_reg(X, y_, Imat)
coeff2 = orthogonal_reg(X, y_, Imat)


""" Reconstruct the Function """

y_ = np.zeros(y.shape, dtype='float64')

for I in xrange(Imax):

    ii, jj = Imat[I, :]

    beval = basis(x1, x2, ii, jj, x1max, x2max)

    y_ += coeff1[I] * beval

fig = plt.figure(num=1, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x1, x2, y, c='b')
ax.scatter(x1, x2, y_, c='r')

y_ = np.zeros(y.shape, dtype='float64')

for I in xrange(Imax):

    ii, jj = Imat[I, :]

    beval = basis(x1, x2, ii, jj, x1max, x2max)

    y_ += coeff2[I] * beval

fig = plt.figure(num=2, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x1, x2, y, c='b')
ax.scatter(x1, x2, y_, c='r')

plt.show()
