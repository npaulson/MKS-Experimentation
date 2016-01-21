import numpy as np
import matplotlib.pyplot as plt
import itertools as it
from mpl_toolkits.mplot3d import Axes3D


def ftest(x1, x2):
    return .50*np.exp(-1*1j*x1)*np.exp(-0*1j*x2) +\
           .25*np.exp(-2*1j*x1)*np.exp(-1*1j*x2) -\
           .10*np.exp(-0*1j*x1)*np.exp(-2*1j*x2)

inc = 15

deg2rad = np.pi/180.
rad2deg = 180./np.pi
inc2rad = inc*deg2rad

x1max = np.pi
x2max = np.pi

n_x1 = np.int64(x1max*rad2deg/np.float64(inc))
n_x2 = np.int64(x2max*rad2deg/np.float64(inc))

x1vec = np.arange(0, n_x1)*inc2rad
x2vec = np.arange(0, n_x2)*inc2rad

x1, x2 = np.meshgrid(x1vec, x2vec)
x1 = x1.swapaxes(0, 1)
x2 = x2.swapaxes(0, 1)


y = ftest(x1, x2)
print y.shape

""" Perform the regression """

Nii = 10
Njj = 10
Imax = Nii*Njj

Imat = np.unravel_index(np.arange(-Imax, Imax), [Nii, Njj])
Imat = np.array(Imat).T

coeff = np.zeros(Imax, dtype='float64')

for I in xrange(Imax):

    ii, jj = Imat[I, :]

    print str([ii, jj])

    basis = np.exp(-ii*1j*x1)*np.exp(-ii*1j*x2)

    # interior = y *\
    #     basis.conj() *\
    #     inc2rad**2

    # coeff[I] = (1/(x1max*x2max))*np.sum(interior)

    XhX = np.sum(basis.conj()*basis)
    print XhX
    XhY = np.sum(basis.conj()*y)
    coeff[I] = XhY/XhX

# fig = plt.figure(num=1, figsize=[4, 4])

# plt.imshow(coeff, origin='lower',
#            interpolation='none', cmap='jet')
# plt.title("Fourier Coefficients")
# plt.colorbar()

""" Reconstruct the Function """

y_ = np.zeros(y.shape, dtype='complex128')

for I in xrange(Imax):

    ii, jj = Imat[I, :]

    basis = np.exp(-ii*1j*x1)*np.exp(-ii*1j*x2)

    y_ += coeff[I] * basis

fig = plt.figure(num=2, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x1, x2, y.real, c='b')
ax.scatter(x1, x2, y_.real, c='r')


plt.show()

print coeff[:16]
