import numpy as np
import matplotlib.pyplot as plt
import itertools as it
from mpl_toolkits.mplot3d import Axes3D


def ftest(x1, x2):
    return .5*np.cos(x1)-.2*np.cos(3*x1)*np.cos(2*x2)+.3*np.cos(x2)

inc = 5

deg2rad = np.pi/180.
rad2deg = 180./np.pi
inc2rad = inc*deg2rad

x1max = 2*np.pi
x2max = 2*np.pi

n_x1 = np.int64(x1max*rad2deg/np.float64(inc))
n_x2 = np.int64(x2max*rad2deg/np.float64(inc))

x1vec = np.arange(n_x1)*inc2rad
x2vec = np.arange(n_x2)*inc2rad

x1, x2 = np.meshgrid(x1vec, x2vec)
x1 = x1.swapaxes(0, 1)
x2 = x2.swapaxes(0, 1)


y = ftest(x1, x2)
print y.shape

""" Perform the regression """

Nii = 5
Njj = 5
Imax = Nii*Njj

Imat = np.unravel_index(np.arange(Imax), [Nii, Njj])
Imat = np.array(Imat).T

coeff = np.zeros(Imax, dtype='float64')

for I in xrange(Imax):

    ii, jj = Imat[I, :]

    print str([ii, jj])

    basis = np.cos(ii*x1) * np.cos(jj*x2)

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

y_ = np.zeros(y.shape, dtype='float64')

for I in xrange(Imax):

    ii, jj = Imat[I, :]

    basis = np.cos(ii*x1) * np.cos(jj*x2)

    y_ += coeff[I] * basis

fig = plt.figure(num=2, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x1, x2, y, c='b')
ax.scatter(x1, x2, y_, c='r')


plt.show()

print coeff[:16]

# inc = 5  # degree increment for angular variables
# deg2rad = np.pi/180.
# rad2deg = 180./np.pi
# inc2rad = inc*deg2rad

# N_L = 15

# # phi1max = 2*np.pi
# # phimax = np.pi/2.
# # phi2max = np.pi/3.

# n_p1 = (360/inc)+1  # number of phi1 samples for FZ
# n_P = (90/inc)+1  # number of Phi samples for FZ
# n_p2 = (60/inc)+1  # number of phi2 samples for FZ

# n_tot = n_p1*n_P*n_p2
# print n_tot

# phi1vec = np.arange(n_p1)*inc2rad
# phivec = np.arange(n_P)*inc2rad
# phi2vec = np.arange(n_p2)*inc2rad

# print phi1vec.min()
# print phi1vec.max()

# print phivec.min()
# print phivec.max()

# print phi2vec.min()
# print phi2vec.max()

# phi1, phi, phi2 = np.meshgrid(phi1vec, phivec, phi2vec)
# phi1 = phi1.swapaxes(0, 1)
# phi = phi.swapaxes(0, 1)
# phi2 = phi2.swapaxes(0, 1)

# euler = np.zeros(np.hstack([phi1.shape, 3]), dtype='float64')
# euler[..., 0] = phi1
# euler[..., 1] = phi
# euler[..., 2] = phi2

# print euler.shape

# """ Calculate X """

# st = time.time()

# X = gsh.gsh_eval(euler, np.arange(N_L))

# print "basis evaluation complete: %ss" % np.round(time.time()-st, 3)


# """ Generate Y """

# bvec = [0, 1, 5, 8, 10, 12]
# bval = [5., 3., 3., 1., 2., 1.]

# Y = np.zeros(phi1.shape, dtype='complex128')

# for ii in xrange(len(bvec)):
#     Y += bval[ii]*X[..., bvec[ii]]

# print np.mean(Y.real)
# print np.mean(Y.imag)
# print np.std(Y.imag)

# """ Perform the regression """

# coeff = np.zeros(N_L, dtype='complex128')

# indxvec = gsh.gsh_basis_info()

# for ii in xrange(N_L):

#     l_prt = 1./(2*indxvec[ii, 0]+1.)
#     const = 3./(2.*np.pi**2)

#     tmp = Y*X[..., ii].conj()*np.sin(phi)*inc2rad**3
#     TMP = np.zeros(tmp.shape, dtype='complex128')

#     rollmat = np.array(list(it.product([0.1], repeat=3)))

#     for jj in xrange(rollmat.shape[0]):

#         if rollmat[jj, 0] == 1:
#             tmp = np.roll(tmp, -1, axis=0)
#         if rollmat[jj, 1] == 1:
#             tmp = np.roll(tmp, -1, axis=1)
#         if rollmat[jj, 2] == 1:
#             tmp = np.roll(tmp, -1, axis=2)

#         TMP += tmp

#         interior = TMP[:-1, :-1, :-1]/rollmat.shape[0]

#     coeff[ii] = l_prt*np.sum(interior)*const

# print "coefficients from regression: %s\n" % str(np.round(coeff, 10))

# """ Check the regression accuracy """

# # Y_ is the set of predictions from the regression fit for the calibration
# # data points
# Y_ = np.zeros(Y.shape, dtype='complex128')
# for ii in xrange(N_L):
#     Y_ += coeff[ii]*X[..., ii]

# print "min(Y): %s" % np.min(Y)
# print "mean(Y): %s" % np.mean(Y)
# print "max(Y): %s" % np.max(Y)
# print "std(Y): %s" % np.std(Y)
# print "\n"

# error = np.abs(Y_.real - Y.real)

# print "mean error: %s" % np.mean(error)
# print "std of error: %s" % np.std(error)
# print "max error: %s" % np.max(error)

# """ Plot the regression results """

# ang_vec = np.unique(phi2)
# print ang_vec

# ang_sel = phi2 == ang_vec[-1]

# fig = plt.figure(num=2, figsize=[10, 6])
# ax = fig.add_subplot(111, projection='3d')

# ax.scatter(phi1[ang_sel], phi[ang_sel], Y[ang_sel].real, c='b')
# ax.scatter(phi1[ang_sel], phi[ang_sel], Y_[ang_sel].real, c='r')

# ang_vec = np.unique(phi)
# print ang_vec
# ang_sel = phi == ang_vec[-1]

# fig = plt.figure(num=3, figsize=[10, 6])
# ax = fig.add_subplot(111, projection='3d')

# ax.scatter(phi1[ang_sel], phi2[ang_sel], Y[ang_sel].real, c='b')
# ax.scatter(phi1[ang_sel], phi2[ang_sel], Y_[ang_sel].real, c='r')

# plt.show()
