import numpy as np
import gsh_hex_tri_L0_16_old as gsh
import itertools as it
import matplotlib.pyplot as plt
import h5py
import time
from mpl_toolkits.mplot3d import Axes3D


phi1max = 2*np.pi
phimax = np.pi/2.
phi2max = np.pi/3.

N_L = 100

f = h5py.File('var_extract_th60_3deg_fip.hdf5', 'r')
var_set = f.get('var_set')
print "var_set shape: %s" % str(var_set.shape)

phi1_lt_pi = var_set[:, 0] < phi1max

phi1 = np.float64(var_set[phi1_lt_pi, 0])
phi = np.float64(var_set[phi1_lt_pi, 1])
phi2 = np.float64(var_set[phi1_lt_pi, 2])
Y = np.float64(var_set[phi1_lt_pi, 3])

f.close

euler = np.zeros((phi1.shape[0], 3), dtype='float64')
euler[:, 0] = phi1
euler[:, 1] = phi
euler[:, 2] = phi2

""" Calculate XhY """

st = time.time()

X = gsh.gsh(euler.T).T
X = X[:, :N_L]
print X.shape

print "basis evaluation complete: %ss" % np.round(time.time()-st, 3)

""" Calculate XhX """

tmp = it.combinations_with_replacement(np.arange(N_L), 2)
Imat = np.array(list(tmp))
ImatL = Imat.shape[0]

XhX = np.zeros((N_L, N_L), dtype='complex128')

for I in xrange(ImatL):

    ii, jj = Imat[I, :]

    if np.mod(I, ImatL/10) == 0:
        print "%s%% complete" % (100*I/ImatL)

    dotvec = np.dot(X[:, ii].conj(), X[:, jj])

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
    XhY[ii] = np.dot(X[:, ii].conj(), Y)

""" Perform the regression """

coeff = np.linalg.solve(XhX, XhY)
# print "coefficients from regression: %s\n" % str(coeff)

""" Check the regression accuracy """

# Y_ is the set of predictions from the regression fit for the calibration
# data points
Y_ = np.zeros(Y.shape, dtype='complex128')

for ii in xrange(N_L):
    Y_ += coeff[ii]*X[:, ii]

print "min(Y): %s" % np.min(Y)
print "mean(Y): %s" % np.mean(Y)
print "max(Y): %s" % np.max(Y)
print "\n"

error = np.abs(Y_.real - Y)

print "mean error: %s" % np.mean(error)
print "std of error: %s" % np.std(error)
print "max error: %s" % np.max(error)

""" Plot the regression results """

ang_vec = np.unique(phi2)
print ang_vec

ang_sel = phi2 == ang_vec[-3]

fig = plt.figure(num=2, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(phi1[ang_sel], phi[ang_sel], Y[ang_sel], c='b')
ax.scatter(phi1[ang_sel], phi[ang_sel], Y_[ang_sel].real, c='r')

ang_vec = np.unique(phi)
print ang_vec
ang_sel = phi == ang_vec[-5]

fig = plt.figure(num=3, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(phi1[ang_sel], phi2[ang_sel], Y[ang_sel], c='b')
ax.scatter(phi1[ang_sel], phi2[ang_sel], Y_[ang_sel].real, c='r')

plt.show()
