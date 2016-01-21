import numpy as np
import gsh_tri_tri_L0_13 as gsh
import itertools as it
import matplotlib.pyplot as plt
import time
from mpl_toolkits.mplot3d import Axes3D

inc = 5  # degree increment for angular variables
N_L = 10

sub2rad = inc*np.pi/180.


n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (180/inc)+1  # number of Phi samples for FZ
n_p2 = 360/inc  # number of phi2 samples for FZ


phi1max = 2*np.pi
phimax = np.pi
phi2max = 2*np.pi

phi1vec = np.linspace(0, phi1max, n_p1)
phivec = np.linspace(0, phimax, n_P)
phi2vec = np.linspace(0, phi2max, n_p2)

phi1, phi, phi2 = np.meshgrid(phi1vec, phivec, phi2vec)

phi1 = phi1.reshape(phi1.size)
phi = phi.reshape(phi.size)
phi2 = phi2.reshape(phi2.size)

euler = np.zeros((phi1.shape[0], 3), dtype='float64')
euler[:, 0] = phi1
euler[:, 1] = phi
euler[:, 2] = phi2

print euler.shape

""" Calculate X """

st = time.time()

X = gsh.gsh_eval(euler, np.arange(N_L))

print "basis evaluation complete: %ss" % np.round(time.time()-st, 3)


""" Generate Y """

bvec = [0, 1, 3, 7, 9]
bval = [5., 3., .2, .2, .3]

Y = np.zeros(phi1.shape, dtype='complex128')

for ii in xrange(len(bvec)):
    Y += bval[ii]*X[:, bvec[ii]]

print np.mean(Y.real)
print np.mean(Y.imag)
print np.std(Y.imag)

""" Calculate XhX """

tmp = it.combinations_with_replacement(np.arange(N_L), 2)
Imat = np.array(list(tmp))
ImatL = Imat.shape[0]

XhX = np.zeros((N_L, N_L), dtype='complex128')

for I in xrange(ImatL):

    ii, jj = Imat[I, :]

    # dotvec = np.dot(X[:, ii].conj(), X[:, jj])
    dotvec = np.sum(X[:, ii].conj()*X[:, jj]*np.sin(phi))

    if ii == jj:
        XhX[ii, ii] = dotvec
    else:
        XhX[ii, jj] = dotvec
        XhX[jj, ii] = dotvec

print "rank(XhX): %s" % np.linalg.matrix_rank(XhX)

plt.figure(1)

plt.subplot(121)

ax = plt.imshow(np.real(XhX), origin='lower',
                interpolation='none', cmap='jet')
plt.title("real(XhX): GSH")
plt.colorbar(ax)

plt.subplot(122)

ax = plt.imshow(np.imag(XhX), origin='lower',
                interpolation='none', cmap='jet')
plt.title("imag(XhX): GSH")
plt.colorbar(ax)

""" Calculate XhY """

XhY = np.zeros(N_L, dtype='complex128')

for ii in xrange(N_L):
    # XhY[ii] = np.dot(X[:, ii].conj(), Y)
    XhY[ii] = np.sum(X[:, ii].conj()*Y*np.sin(phi))


""" Perform the regression """

coeff = np.linalg.solve(XhX, XhY)
print "coefficients from regression: %s\n" % str(np.round(coeff, 4))

""" Check the regression accuracy """

# Y_ is the set of predictions from the regression fit for the calibration
# data points
# Y_ = np.zeros(Y.shape, dtype='complex128')
# for ii in xrange(N_L):
#     Y_ += coeff[ii]*np.squeeze(gsh.gsh_eval(euler, [ii]))
Y_ = np.dot(coeff, X.T)

print "min(Y): %s" % np.min(Y)
print "mean(Y): %s" % np.mean(Y)
print "max(Y): %s" % np.max(Y)
print "std(Y): %s" % np.std(Y)
print "\n"

error = np.abs(Y_.real - Y.real)

print "mean error: %s" % np.mean(error)
print "std of error: %s" % np.std(error)
print "max error: %s" % np.max(error)

""" Plot the regression results """

ang_vec = np.unique(phi2)
print ang_vec

ang_sel = phi2 == ang_vec[3]

fig = plt.figure(num=2, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(phi1[ang_sel], phi[ang_sel], Y[ang_sel].real, c='b')
ax.scatter(phi1[ang_sel], phi[ang_sel], Y_[ang_sel].real, c='r')

ang_vec = np.unique(phi)
print ang_vec
ang_sel = phi == ang_vec[5]

fig = plt.figure(num=3, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(phi1[ang_sel], phi2[ang_sel], Y[ang_sel].real, c='b')
ax.scatter(phi1[ang_sel], phi2[ang_sel], Y_[ang_sel].real, c='r')

# fig = plt.figure(num=2, figsize=[10, 6])
# ax = fig.add_subplot(111, projection='3d')

# ax.scatter(phi1, phi2, Y.real, c='b')
# ax.scatter(phi1, phi2, Y_.real, c='r')

plt.show()
