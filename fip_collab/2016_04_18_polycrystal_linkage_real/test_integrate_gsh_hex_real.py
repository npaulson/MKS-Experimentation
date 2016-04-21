import numpy as np
import hex_complex_0_16 as gsh_old
# import hex_complex_0_16 as gsh_new
import hex_0_4_real as gsh_new
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def euler_grid(inc, phi1max, phimax, phi2max):

    n_p1 = (phi1max/inc)  # number of phi1 samples for FZ
    n_P = (phimax/inc)+1  # number of Phi samples for FZ
    n_p2 = (phi2max/inc)  # number of phi2 samples for FZ

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

    n_p1 = (phi1max/inc)  # number of phi1 samples for FZ
    n_P = (phimax/inc)  # number of Phi samples for FZ
    n_p2 = (phi2max/inc)  # number of phi2 samples for FZ

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

    phi1 = np.random.rand(n_tot)*phi1max*(np.pi/180.)
    phi = np.random.rand(n_tot)*phimax*(np.pi/180.)
    phi2 = np.random.rand(n_tot)*phi2max*(np.pi/180.)

    euler = np.zeros((n_tot, 3))
    euler[:, 0] = phi1
    euler[:, 1] = phi
    euler[:, 2] = phi2

    return euler


indxvec_complex = gsh_old.gsh_basis_info()
N_L_complex = np.sum(indxvec_complex[:, 0] <= 4)

indxvec_real = gsh_new.gsh_basis_info()
N_L_real = np.sum(indxvec_real[:, 0] <= 4)

print "N_L_complex = %s" % N_L_complex

phi1max = 360.
phimax = 90.
phi2max = 60.

inc = 10.
euler, n_tot = euler_grid_center(inc, phi1max, phimax, phi2max)

""" Generate Y """

# bvec = [0,  1, 5, 7, 13, 18, 38]
# bval = [40., 10., 10., 4, 4, 24, 24]

bvec = [0, 1, 5]
bval = [40., 20., 20.]

Y = np.zeros(euler.shape[0], dtype='complex128')
for ii in xrange(len(bvec)):
    Xtmp = np.squeeze(gsh_old.gsh_eval(euler, [bvec[ii]]))
    Y += bval[ii]*Xtmp

""" Perform the regression """

coef = np.zeros(N_L_real, dtype='complex128')

indxvec = gsh_new.gsh_basis_info()

# domain_eul_sz is the integration domain in radians
domain_sz = phi1max*phimax*phi2max*(np.pi/180.)**3
# full_eul_sz is the size of euler space in radians
full_sz = (2*np.pi)*(np.pi)*(2*np.pi)
eul_frac = domain_sz/full_sz
fzsz = 1./(eul_frac*8.*np.pi**2)
bsz = domain_sz/n_tot

for ii in xrange(N_L_real):

    Xtmp = np.squeeze(gsh_new.gsh_eval(euler, [ii]))

    l = indxvec_real[ii, 0]
    tmp = (1./(2.*l+1.))*np.sum(Y*Xtmp.conj()*np.sin(euler[:, 1]))*bsz*fzsz
    coef[ii] = tmp

print "coefficients from integration: %s" % str(coef)

""" plot a visual representation of the coefficients """

fig = plt.figure(num=1, figsize=[12, 8])
plt.bar(np.arange(N_L_real), coef.real)
plt.title("coefficients from integration")
plt.grid(True)

plt.xticks(np.arange(0, N_L_real, 2), rotation='vertical')
plt.yticks(np.arange(-12, 42, 2))

""" To check the regression accuracy first lets generate a set of euler
angles"""

del Y, euler, n_tot

inc = 5.0

# euler is the array of euler angles for the purposes of validation
euler, n_tot = euler_grid(inc, phi1max, phimax, phi2max)

print euler.shape

Y = np.zeros(euler.shape[0], dtype='complex128')
for ii in xrange(len(bvec)):
    Xtmp = np.squeeze(gsh_old.gsh_eval(euler, [bvec[ii]]))
    Y += bval[ii]*Xtmp

Y_ = np.zeros(euler.shape[0], dtype='complex128')
for ii in xrange(N_L_real):
    Xtmp = np.squeeze(gsh_new.gsh_eval(euler, [ii]))
    Y_ += coef[ii]*Xtmp

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
