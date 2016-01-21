import numpy as np
import gsh_hex_tri_L0_16 as gsh
import matplotlib.pyplot as plt
import time
from mpl_toolkits.mplot3d import Axes3D

n_tot = 18031
N_L = 15

phi1max = 2*np.pi
phimax = np.pi/2.
phi2max = np.pi/3.

phi1 = np.random.rand(n_tot)*phi1max
phi = np.random.rand(n_tot)*phimax
phi2 = np.random.rand(n_tot)*phi2max

euler = np.zeros((n_tot, 3))
euler[:, 0] = phi1
euler[:, 1] = phi
euler[:, 2] = phi2

""" Calculate X """

st = time.time()

X = gsh.gsh_eval(euler, np.arange(N_L))

print "basis evaluation complete: %ss" % np.round(time.time()-st, 3)


""" Generate Y """

bvec = [0, 1, 5, 8, 10, 12]
bval = [5., 3., 3., 1., 2., 1.]

Y = np.zeros(phi1.shape, dtype='complex128')

for ii in xrange(len(bvec)):
    Y += bval[ii]*X[:, bvec[ii]]

""" Perform the regression """

coeff = np.zeros(N_L, dtype='complex128')

indxvec = gsh.gsh_basis_info()

# fzsz = 3./(2.*np.pi**2)
# esz = phi1max*phimax*phi2max
# bsz = esz/n_tot

# for ii in xrange(N_L):

#     l = indxvec[ii, 0]
#     tmp = (1./(2.*l+1.))*np.sum(Y*X[:, ii].conj()*np.sin(phi)*bsz)*fzsz
#     coeff[ii] = tmp

fzsz = 3./(2.*np.pi**2)
bsz = phi1max*phimax*phi2max/n_tot
print "esz: %s" % bsz
print "n_tot: %s" % n_tot
print "Y size: %s" % Y.size

for ii in xrange(N_L):

    l = indxvec[ii, 0]
    tmp = (1./(2.*l+1.))*np.sum(Y*X[:, ii].conj()*np.sin(phi))*bsz*fzsz
    coeff[ii] = tmp

print "coefficients from regression: %s\n" % str(np.round(coeff, 10))

""" Check the regression accuracy """

# Y_ is the set of predictions from the regression fit for the calibration
# data points
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

thr = (1E3)/n_tot
print "selection zone: %s" % thr

ang_sel = np.abs(phi2 - np.pi/5) < thr

fig = plt.figure(num=2, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(phi1[ang_sel], phi[ang_sel], Y[ang_sel].real, c='b')
ax.scatter(phi1[ang_sel], phi[ang_sel], Y_[ang_sel].real, c='r')

ang_sel = np.abs(phi - np.pi/2) < thr

fig = plt.figure(num=3, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(phi1[ang_sel], phi2[ang_sel], Y[ang_sel].real, c='b')
ax.scatter(phi1[ang_sel], phi2[ang_sel], Y_[ang_sel].real, c='r')

plt.show()
