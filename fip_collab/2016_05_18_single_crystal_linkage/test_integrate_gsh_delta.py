import numpy as np
# import hex_0_6_real as gsh
import gsh_cub_tri_L0_40 as gsh
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
phi2max = 90.  # max phi2 angle (deg) for integration domain
inc = 3.  # degree increment for euler angle generation
L_trunc = 16  # truncation level in the l index for the GSH

indxvec = gsh.gsh_basis_info()
N_L = np.sum(indxvec[:, 0] <= L_trunc)
indxvec = indxvec[:N_L, :]
print "N_L = %s" % N_L

euler, n_tot = euler_grid_center(inc, phi1max, phimax, phi2max)

""" Generate Y """

np.random.seed(1)
indxrand = np.random.randint(n_tot)
euler_d = euler[indxrand, :]
"location of delta: %s" % str(euler_d)
Y = np.zeros((n_tot,))
Y[indxrand] = 1  # assign delta response

""" Perform the integration / validation simuletaneously """

coef = np.zeros(N_L, dtype='complex128')

# domain_eul_sz is the integration domain in radians
domain_sz = phi1max*phimax*phi2max*(np.pi/180.)**3
# full_eul_sz is the size of euler space in radians
full_sz = (2*np.pi)*(np.pi)*(2*np.pi)
eul_frac = domain_sz/full_sz
fzsz = 1./(eul_frac*8.*np.pi**2)
bsz = domain_sz/n_tot

Y_ = np.zeros(euler.shape[0], dtype='complex128')

for ii in xrange(N_L):

    if np.mod(ii, 100) == 0:
        print "integration for basis %s completed" % ii

    Xtmp = np.squeeze(gsh.gsh_eval(euler, [ii]))

    l = indxvec[ii, 0]
    tmp = (1./(2.*l+1.))*np.sum(Y*Xtmp.conj()*np.sin(euler[:, 1]))*bsz*fzsz
    Y_ += tmp*Xtmp
    coef[ii] = tmp

Y_ = Y_.real

# print "coefficients from integration: %s" % str(coef)

""" plot a visual representation of the coefficients """

# fig = plt.figure(num=1, figsize=[12, 8])
# plt.plot(np.arange(N_L), coef.real, 'rx')
# plt.title("coefficients from integration")

# plt.xticks(np.arange(0, N_L_new, 1), rotation='vertical')
# plt.yticks(np.arange(-11, 11, 1))

# plt.show()

""" Plot the regression results """

ang_sel = euler[:, 2] == euler_d[2]

fig = plt.figure(num=2, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(euler[ang_sel, 0], euler[ang_sel, 1], Y[ang_sel], c='b')

ax.set_xlabel("$\phi_1$")
ax.set_ylabel("$\Phi$")
ax.set_zlabel("y")

fig = plt.figure(num=3, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(euler[ang_sel, 0], euler[ang_sel, 1], Y_[ang_sel], c='r')

ax.set_xlabel("$\phi_1$")
ax.set_ylabel("$\Phi$")
ax.set_zlabel("y")

plt.show()

ang_sel = euler[:, 1] == euler_d[1]

fig = plt.figure(num=4, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(euler[ang_sel, 0], euler[ang_sel, 2], Y[ang_sel], c='b')

ax.set_xlabel("$\phi_1$")
ax.set_ylabel("$\phi_2$")
ax.set_zlabel("y")

fig = plt.figure(num=5, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(euler[ang_sel, 0], euler[ang_sel, 2], Y_[ang_sel], c='r')

ax.set_xlabel("$\phi_1$")
ax.set_ylabel("$\phi_2$")
ax.set_zlabel("y")

plt.show()
