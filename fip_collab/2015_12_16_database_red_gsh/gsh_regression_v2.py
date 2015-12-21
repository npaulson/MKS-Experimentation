import numpy as np
import gsh_hex_tri_L0_4 as gsh
import itertools as it
import matplotlib.pyplot as plt
import h5py
import time
from mpl_toolkits.mplot3d import Axes3D


inc = 6
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ
en = 0.0085

N_L = 15

f = h5py.File('var_extract.hdf5', 'r')
var_set = f.get('var_set')
print "var_set shape: %s" % str(var_set.shape)

euler = np.float64(var_set[:, 0:3])

Y = np.float64(var_set[:, 3])

f.close

""" Calculate X """

st = time.time()

X = np.zeros((euler.shape[0], N_L), dtype='complex128')

for L in xrange(N_L):

    X[:, L] = np.squeeze(gsh.gsh_eval(euler, [L]))

print "basis evaluation complete: %ss" % np.round(time.time()-st, 3)

""" Calculate XhX """

tmp = it.combinations_with_replacement(np.arange(N_L), 2)
Imat = np.array(list(tmp))
ImatL = Imat.shape[0]

XhX = np.zeros((N_L, N_L), dtype='complex128')

for I in xrange(ImatL):

    ii, jj = Imat[I, :]

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
print "coefficients from regression: %s\n" % str(coeff)

""" Check the regression accuracy """

# Y_ is the set of predictions from the regression fit for the calibration
# data points
Y_ = np.zeros(Y.shape, dtype='complex128')

for ii in xrange(N_L):
    Y_ += coeff[ii]*np.squeeze(gsh.gsh_eval(euler, [L]))

print "min(Y): %s" % np.min(Y)
print "mean(Y): %s" % np.mean(Y)
print "max(Y): %s" % np.max(Y)
print "\n"

error = np.abs(np.real(Y_) - Y)

print "mean error: %s" % np.mean(error)
print "std of error: %s" % np.std(error)
print "max error: %s" % np.max(error)

""" Plot the regression results """

fig = plt.figure(num=2, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

phi2vec = euler[:, 2] == 0

ax.scatter(euler[phi2vec, 0], euler[phi2vec, 1], Y[phi2vec], c='b')

fig = plt.figure(num=3, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

phi2vec = euler[:, 2] == 0

ax.scatter(euler[phi2vec, 0], euler[phi2vec, 1], Y_[phi2vec].real, c='r')


plt.show()
