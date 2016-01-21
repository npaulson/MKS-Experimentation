import numpy as np
import gsh_hex_tri_L0_16 as gsh
import matplotlib.pyplot as plt
import time
from mpl_toolkits.mplot3d import Axes3D


def euler_grid(inc, phi1max, phimax, phi2max):

    n_p1 = (360/inc)  # number of phi1 samples for FZ
    n_P = (90/inc)+1  # number of Phi samples for FZ
    n_p2 = (60/inc)  # number of phi2 samples for FZ

    n_tot = n_p1*n_P*n_p2

    inc2rad = inc*np.pi/180.

    phi1vec = np.arange(n_p1)*inc2rad
    phivec = np.arange(n_P)*inc2rad
    phi2vec = np.arange(n_p2)*inc2rad

    phi1, phi, phi2 = np.meshgrid(phi1vec, phivec, phi2vec)

    euler = np.zeros([n_tot, 3], dtype='float64')
    euler[:, 0] = phi1.reshape(phi1.size)
    euler[:, 1] = phi.reshape(phi.size)
    euler[:, 2] = phi2.reshape(phi2.size)

    return euler, n_tot


def euler_grid_center(inc, phi1max, phimax, phi2max):

    n_p1 = (360/inc)  # number of phi1 samples for FZ
    n_P = (90/inc)  # number of Phi samples for FZ
    n_p2 = (60/inc)  # number of phi2 samples for FZ

    n_tot = n_p1*n_P*n_p2

    inc2rad = inc*np.pi/180.

    phi1vec = (np.arange(n_p1)+0.5)*inc2rad
    phivec = (np.arange(n_P)+0.5)*inc2rad
    phi2vec = (np.arange(n_p2)+0.5)*inc2rad

    print phi1vec.min()
    print phi1vec.max()

    print phivec.min()
    print phivec.max()

    print phi2vec.min()
    print phi2vec.max()

    phi1, phi, phi2 = np.meshgrid(phi1vec, phivec, phi2vec)

    euler = np.zeros([n_tot, 3], dtype='float64')
    euler[:, 0] = phi1.reshape(phi1.size)
    euler[:, 1] = phi.reshape(phi.size)
    euler[:, 2] = phi2.reshape(phi2.size)

    return euler, n_tot


def euler_rand(n_tot, phi1max, phimax, phi2max):

    phi1 = np.random.rand(n_tot)*phi1max
    phi = np.random.rand(n_tot)*phimax
    phi2 = np.random.rand(n_tot)*phi2max

    euler = np.zeros((n_tot, 3))
    euler[:, 0] = phi1
    euler[:, 1] = phi
    euler[:, 2] = phi2

    return euler


N_L = 500

phi1max = 2*np.pi
phimax = np.pi/2.
phi2max = np.pi/3.

# n_tot = 1944000
# euler = euler_rand(n_tot, phi1max, phimax, phi2max)

# inc = 5.
# euler, n_tot = euler_grid_center(inc, phi1max, phimax, phi2max)

inc = 5.
euler, n_tot = euler_grid(inc, phi1max, phimax, phi2max)

""" Generate Y """

bvec = [0,  10, 20, 60, 140, 290, 320, 460]
bval = [40., 20., -10., 6., -4., 1., 2., -1.]

# bvec = [0, 1, 5, 8, 10, 12]
# bval = [5., 3., 3., 1., 2., 1.]

Y = np.zeros(n_tot, dtype='complex128')

for ii in xrange(len(bvec)):
    Y += bval[ii]*gsh.gsh_eval(euler, [bvec[ii]])[:, 0]

""" Perform the regression """

coeff = np.zeros(N_L, dtype='complex128')

indxvec = gsh.gsh_basis_info()

fzsz = 3./(2.*np.pi**2)
bsz = phi1max*phimax*phi2max/n_tot
print "esz: %s" % bsz
print "n_tot: %s" % n_tot
print "Y size: %s" % Y.size

for ii in xrange(N_L):
    if np.mod(ii, 10) == 0:
        print ii

    l = indxvec[ii, 0]
    X_ = gsh.gsh_eval(euler, [ii])[:, 0]
    tmp = (1./(2.*l+1.))*np.sum(Y*X_.conj()*np.sin(euler[:, 1]))*bsz*fzsz
    coeff[ii] = tmp

""" plot a visual representation of the coefficients """

fig = plt.figure(num=1, figsize=[12, 8])
plt.bar(np.arange(N_L), coeff.real)
plt.title("coefficients from integration")
plt.grid(True)

plt.xticks(np.arange(0, 500, 10), rotation='vertical')
plt.yticks(np.arange(-12, 42, 2))

""" To check the regression accuracy first lets generate a set of euler
angles"""

del Y, euler, n_tot

inc = 3.0

# euler is the array of euler angles for the purposes of validation
euler, n_tot = euler_grid(inc, phi1max, phimax, phi2max)

print euler.shape

# Y is the set of true values from our function for the validation
# data points
Y = np.zeros(n_tot, dtype='complex128')

for ii in xrange(len(bvec)):
    Y += bval[ii]*gsh.gsh_eval(euler, [bvec[ii]])[:, 0]

# Y_ is the set of predictions from the regression fit for the validation
# data points
Y_ = np.zeros(n_tot, dtype='complex128')

for ii in xrange(N_L):
    if np.mod(ii, 10) == 0:
        print ii

    Y_ += coeff[ii]*gsh.gsh_eval(euler, [ii])[:, 0]

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

ang_sel = np.abs(euler[:, 2] - np.pi/5) < thr

fig = plt.figure(num=2, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(euler[ang_sel, 0], euler[ang_sel, 1], Y[ang_sel].real, c='b')
ax.scatter(euler[ang_sel, 0], euler[ang_sel, 1], Y_[ang_sel].real, c='r')

ang_sel = np.abs(euler[:, 1] - np.pi/2) < thr

fig = plt.figure(num=3, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(euler[ang_sel, 0], euler[ang_sel, 2], Y[ang_sel].real, c='b')
ax.scatter(euler[ang_sel, 0], euler[ang_sel, 2], Y_[ang_sel].real, c='r')

plt.show()
