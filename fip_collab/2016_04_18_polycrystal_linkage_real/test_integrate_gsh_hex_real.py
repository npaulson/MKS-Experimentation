import numpy as np
import gsh_hex_tri_L0_16 as gsh_old
# import hex_complex_0_16 as gsh_new
import hex_0_6_complex as gsh_new
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
N_L_complex = np.sum(indxvec_complex[:, 0] <= 6)
indxvec_complex = indxvec_complex[:N_L_complex, :]

indxvec_real = gsh_new.gsh_basis_info()
N_L_real = np.sum(indxvec_real[:, 0] <= 6)
indxvec_real = indxvec_complex[:N_L_real, :]

print "N_L_complex = %s" % N_L_complex

phi1max = 360.
phimax = 90.
phi2max = 60.

inc = 3.
euler, n_tot = euler_grid_center(inc, phi1max, phimax, phi2max)

""" Generate Y """

indxlist = np.arange(N_L_complex)
bvec = [0]
bval = [40]

for ii in xrange(100):
    indx1 = np.random.choice(indxlist)
    print "indx1: %s" % indx1

    if np.any(bvec == indx1):
        continue

    indxset1 = indxvec_complex[indx1, :]
    print "indxset1: %s" % str(indxset1)

    val = np.random.randint(-20, 21)
    # print "val: %s" % val

    if indxset1[1] == 0:
        bvec.append(indx1)
        bval.append(val)
    else:
        indxset2 = indxset1*[1, -1, 1]

        loc = (indxvec_complex[:, 0] == indxset2[0]) * \
              (indxvec_complex[:, 1] == indxset2[1]) * \
              (indxvec_complex[:, 2] == indxset2[2])
        indx2 = np.argmax(loc)

        print "indx2: %s" % indx2
        print "indxset2: %s" % str(indxvec_complex[indx2, :])

        bvec.append(indx1)
        bvec.append(indx2)
        bval.append(val)
        bval.append(val)

    if len(bvec) > 5:
        break

print bvec
print bval

# bvec = [0, 1, 5]
# bval = [40., 20., 20.]

Y = np.zeros(euler.shape[0], dtype='complex128')
for ii in xrange(len(bvec)):
    Xtmp = np.squeeze(gsh_old.gsh_eval(euler, [bvec[ii]]))
    Y += bval[ii]*Xtmp

Y = Y.real

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
# plt.yticks(np.arange(np.int64(), 1))

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

Y = Y.real

Y_ = np.zeros(euler.shape[0], dtype='complex128')
for ii in xrange(N_L_real):
    Xtmp = np.squeeze(gsh_new.gsh_eval(euler, [ii]))
    Y_ += coef[ii]*Xtmp

print "min(Y.real): %s" % np.min(Y.real)
print "mean(Y.real): %s" % np.mean(Y.real)
print "max(Y.real): %s" % np.max(Y.real)

print "min(Y.imag): %s" % np.min(Y.imag)
print "mean(Y.imag): %s" % np.mean(Y.imag)
print "max(Y.imag): %s" % np.max(Y.imag)
print "\n"

if np.max(np.abs(Y.imag)) > 1:
    print "WARNING: test function has significant imaginary components"

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
