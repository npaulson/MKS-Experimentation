import numpy as np
import gsh_hex_tri_L0_16 as gsh
import matplotlib.pyplot as plt
import time
from mpl_toolkits.mplot3d import Axes3D

inc = 5  # degree increment for angular variables
deg2rad = np.pi/180.
rad2deg = 180./np.pi
inc2rad = inc*deg2rad

N_L = 15

# phi1max = 2*np.pi
# phimax = np.pi/2.
# phi2max = np.pi/3.

n_p1 = (360/inc)  # number of phi1 samples for FZ
n_P = (90/inc)  # number of Phi samples for FZ
n_p2 = (60/inc)  # number of phi2 samples for FZ

n_tot = n_p1*n_P*n_p2

phi1vec = np.arange(n_p1)*inc2rad
phivec = np.arange(n_P)*inc2rad
phi2vec = np.arange(n_p2)*inc2rad

print phi1vec.min()
print phi1vec.max()

print phivec.min()
print phivec.max()

print phi2vec.min()
print phi2vec.max()

phi1, phi, phi2 = np.meshgrid(phi1vec, phivec, phi2vec)

euler = np.zeros(np.hstack([phi1.shape, 3]), dtype='float64')
euler[..., 0] = phi1
euler[..., 1] = phi
euler[..., 2] = phi2

print euler.shape

""" Calculate X """

st = time.time()

X = gsh.gsh_eval(euler, np.arange(N_L))

print "basis evaluation complete: %ss" % np.round(time.time()-st, 3)


""" Generate Y """

bvec = [0, 1, 5, 8, 10, 12]
bval = [5., 3., 3., 1., 2., 1.]

Y = np.zeros(phi1.shape, dtype='complex128')

for ii in xrange(len(bvec)):
    Y += bval[ii]*X[..., bvec[ii]]

print np.mean(Y.real)
print np.mean(Y.imag)
print np.std(Y.imag)

""" Perform the regression """

coeff = np.zeros(N_L, dtype='complex128')

indxvec = gsh.gsh_basis_info()

for ii in xrange(N_L):

    l_prt = 1./(2*indxvec[ii, 0]+1.)
    # const = (3.*n_tot*inc2rad**3)/(2.*np.pi**2)
    const = 3./(2.*np.pi**2)

    # interior = Y*X[..., ii].conj()*np.sin(phi)
    interior = Y*X[..., ii].conj()*np.sin(phi)*inc2rad**3

    tmp = l_prt*np.sum(interior)*const
    coeff[ii] = tmp

print "coefficients from regression: %s\n" % str(np.round(coeff, 10))

""" Check the regression accuracy """

# Y_ is the set of predictions from the regression fit for the calibration
# data points
Y_ = np.zeros(Y.shape, dtype='complex128')
for ii in xrange(N_L):
    Y_ += coeff[ii]*X[..., ii]

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

ang_sel = phi2 == ang_vec[-1]

fig = plt.figure(num=2, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(phi1[ang_sel], phi[ang_sel], Y[ang_sel].real, c='b')
ax.scatter(phi1[ang_sel], phi[ang_sel], Y_[ang_sel].real, c='r')

ang_vec = np.unique(phi)
print ang_vec
ang_sel = phi == ang_vec[-1]

fig = plt.figure(num=3, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(phi1[ang_sel], phi2[ang_sel], Y[ang_sel].real, c='b')
ax.scatter(phi1[ang_sel], phi2[ang_sel], Y_[ang_sel].real, c='r')

plt.show()
