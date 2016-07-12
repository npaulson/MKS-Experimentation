import numpy as np
import gsh_hex_tri_L0_16 as gsh_old
#import hex_0_8_real as gsh_new
import gsh_hex_tri_L0_16 as gsh_new
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def euler_grid_center(inc, phi1max, phimax, phi2max):

    n_p1 = (phi1max/inc)  # number of phi1 samples for FZ
    n_P = (phimax/inc)  # number of Phi samples for FZ
    n_p2 = (phi2max/inc)  # number of phi2 samples for FZ

    n_tot = n_p1*n_P*n_p2

    inc2rad = inc*np.pi/180.

    phi1vec = (np.arange(n_p1)+0.5)*inc2rad
    phivec = (np.arange(n_P)+0.5)*inc2rad
    phi2vec = (np.arange(n_p2)+0.5)*inc2rad

    # print phi1vec.min()
    # print phi1vec.max()

    # print phivec.min()
    # print phivec.max()

    # print phi2vec.min()
    # print phi2vec.max()

    phi1, phi, phi2 = np.meshgrid(phi1vec, phivec, phi2vec)

    euler = np.zeros([n_tot, 3], dtype='float64')
    euler[:, 0] = phi1.reshape(phi1.size)
    euler[:, 1] = phi.reshape(phi.size)
    euler[:, 2] = phi2.reshape(phi2.size)

    return euler, n_tot

"""Initialize the important constants"""

phi1max = 360.  # max phi1 angle (deg) for integration domain
phimax = 90.  # max phi angle (deg) for integration domain
phi2max = 60.  # max phi2 angle (deg) for integration domain
inc = 3.  # degree increment for euler angle generation
L_trunc = 6  # truncation level in the l index for the GSH

indxvec_old = gsh_old.gsh_basis_info()
N_L_old = np.sum(indxvec_old[:, 0] <= L_trunc)
indxvec_old = indxvec_old[:N_L_old, :]
print "N_L_old = %s" % N_L_old

indxvec_new = gsh_new.gsh_basis_info()
N_L_new = np.sum(indxvec_new[:, 0] <= L_trunc)
indxvec_new = indxvec_new[:N_L_new, :]
print "N_L_new = %s" % N_L_new

euler, n_tot = euler_grid_center(inc, phi1max, phimax, phi2max)

""" Generate Y """

np.random.seed(141)

bvec = np.arange(N_L_old)
bval = np.random.normal(scale=1.0, size=bvec.shape)**3

Y = np.zeros(euler.shape[0], dtype='complex128')
for indx in bvec:
    Xtmp = np.squeeze(gsh_old.gsh_eval(euler, [indx]))
    Y += bval[indx]*Xtmp

Y = Y.real

print "bval.min(): %s" % bval.min()
print "bval.mean(): %s" % bval.mean()
print "bval.max(): %s" % bval.max()


""" Perform the integration """

coef = np.zeros(N_L_new, dtype='complex128')

indxvec = gsh_new.gsh_basis_info()

# domain_eul_sz is the integration domain in radians
domain_sz = phi1max*phimax*phi2max*(np.pi/180.)**3
# full_eul_sz is the size of euler space in radians
full_sz = (2*np.pi)*(np.pi)*(2*np.pi)
eul_frac = domain_sz/full_sz
fzsz = 1./(eul_frac*8.*np.pi**2)
bsz = domain_sz/n_tot

for ii in xrange(N_L_new):

    if np.mod(ii, 100) == 0:
        print "integration for basis %s completed" % ii

    Xtmp = np.squeeze(gsh_new.gsh_eval(euler, [ii]))

    l = indxvec_new[ii, 0]
    tmp = (1./(2.*l+1.))*np.sum(Y*Xtmp.conj()*np.sin(euler[:, 1]))*bsz*fzsz
    coef[ii] = tmp

# print "coefficients from integration: %s" % str(coef)

""" plot a visual representation of the coefficients """

fig = plt.figure(num=1, figsize=[12, 8])
plt.plot(np.arange(N_L_old), bval, 'bx')
plt.plot(np.arange(N_L_new), coef.real, 'rx')
plt.title("coefficients from integration")

# plt.xticks(np.arange(0, N_L_new, 1), rotation='vertical')
# plt.yticks(np.arange(-11, 11, 1))

""" To check the regression accuracy first lets generate a set of euler
angles"""

del Y, euler, n_tot

inc = 5.0

# euler is the array of euler angles for the purposes of validation
euler, n_tot = euler_grid_center(inc, phi1max, phimax, phi2max)

Y = np.zeros(euler.shape[0], dtype='complex128')
for indx in bvec:
    Xtmp = np.squeeze(gsh_old.gsh_eval(euler, [indx]))
    Y += bval[indx]*Xtmp

Y = Y.real

Y_ = np.zeros(euler.shape[0], dtype='complex128')
for indx in xrange(N_L_new):
    Xtmp = np.squeeze(gsh_new.gsh_eval(euler, [indx]))
    Y_ += coef[indx]*Xtmp

Y_ = Y_.real

print "min(Y): %s" % np.min(Y)
print "mean(Y): %s" % np.mean(Y)
print "max(Y): %s" % np.max(Y)
print "\n"

error = np.abs(Y_ - Y)

print "mean error: %s" % np.mean(error)
print "std of error: %s" % np.std(error)
print "max error: %s" % np.max(error)

""" Plot the regression results """

phi_u = np.unique(euler[:, 1])
phi2_u = np.unique(euler[:, 2])


# thr = (1E3)/n_tot
# print "selection zone: %s" % thr

# ang_sel = np.abs(euler[:, 2] - np.pi/5) < thr

ang_sel = euler[:, 2] == phi2_u[np.int64(len(phi2_u)/2.)]

fig = plt.figure(num=2, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(euler[ang_sel, 0], euler[ang_sel, 1], Y[ang_sel], c='b')
ax.scatter(euler[ang_sel, 0], euler[ang_sel, 1], Y_[ang_sel], c='r')

# ang_sel = np.abs(euler[:, 1] - np.pi/2) < thr
ang_sel = euler[:, 1] == phi_u[np.int64(len(phi_u)/2.)]

fig = plt.figure(num=3, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(euler[ang_sel, 0], euler[ang_sel, 2], Y[ang_sel], c='b')
ax.scatter(euler[ang_sel, 0], euler[ang_sel, 2], Y_[ang_sel], c='r')

plt.show()
