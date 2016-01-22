import numpy as np
import gsh_hex_tri_L0_16 as gsh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def angles_grid(inc, thmax, phi1max, phimax, phi2max):

    n_th = (60/inc)+1
    n_p1 = (360/inc)  # number of phi1 samples for FZ
    n_P = (90/inc)+1  # number of Phi samples for FZ
    n_p2 = (60/inc)  # number of phi2 samples for FZ

    n_tot = n_th*n_p1*n_P*n_p2

    inc2rad = inc*np.pi/180.

    thvec = np.arange(n_th)*inc2rad
    phi1vec = np.arange(n_p1)*inc2rad
    phivec = np.arange(n_P)*inc2rad
    phi2vec = np.arange(n_p2)*inc2rad

    th, phi1, phi, phi2 = np.meshgrid(thvec, phi1vec, phivec, phi2vec)

    angles = np.zeros([n_tot, 4], dtype='float64')
    angles[:, 0] = th.reshape(n_tot)
    angles[:, 1] = phi1.reshape(n_tot)
    angles[:, 2] = phi.reshape(n_tot)
    angles[:, 3] = phi2.reshape(n_tot)

    return angles, n_th, n_p1, n_P, n_p2


def angles_grid_center(inc, thmax, phi1max, phimax, phi2max):

    n_th = (60/inc)
    n_p1 = (360/inc)  # number of phi1 samples for FZ
    n_P = (90/inc)  # number of Phi samples for FZ
    n_p2 = (60/inc)  # number of phi2 samples for FZ

    n_tot = n_th*n_p1*n_P*n_p2

    inc2rad = inc*np.pi/180.

    thvec = (np.arange(n_th)+0.5)*inc2rad
    phi1vec = (np.arange(n_p1)+0.5)*inc2rad
    phivec = (np.arange(n_P)+0.5)*inc2rad
    phi2vec = (np.arange(n_p2)+0.5)*inc2rad

    # print thvec.min()
    # print thvec.max()

    # print phi1vec.min()
    # print phi1vec.max()

    # print phivec.min()
    # print phivec.max()

    # print phi2vec.min()
    # print phi2vec.max()

    th, phi1, phi, phi2 = np.meshgrid(thvec, phi1vec, phivec, phi2vec)

    angles = np.zeros([n_tot, 4], dtype='float64')
    angles[:, 0] = th.reshape(n_tot)
    angles[:, 1] = phi1.reshape(n_tot)
    angles[:, 2] = phi.reshape(n_tot)
    angles[:, 3] = phi2.reshape(n_tot)

    return angles, n_th, n_p1, n_P, n_p2


def angles_rand(n_tot, thmax, phi1max, phimax, phi2max):

    th = np.random.rand(n_tot)*thmax
    phi1 = np.random.rand(n_tot)*phi1max
    phi = np.random.rand(n_tot)*phimax
    phi2 = np.random.rand(n_tot)*phi2max

    angles = np.zeros([n_tot, 4], dtype='float64')
    angles[:, 0] = th.reshape(th.size)
    angles[:, 1] = phi1.reshape(phi1.size)
    angles[:, 2] = phi.reshape(phi.size)
    angles[:, 3] = phi2.reshape(phi2.size)

    return angles

thmax = np.pi/3
phi1max = 2*np.pi
phimax = np.pi/2.
phi2max = np.pi/3.

L_th = thmax

inc = 6.
angles, n_th, n_p1, n_P, n_p2 = angles_grid_center(inc,
                                                   thmax,
                                                   phi1max,
                                                   phimax,
                                                   phi2max)

# inc = 5.
# angles, n_th, n_p1, n_P, n_p2 = angles_grid(inc,
#                                             thmax,
#                                             phi1max,
#                                             phimax,
#                                             phi2max)

inc2rad = inc*(np.pi/180.)
n_eul = n_p1*n_P*n_p2
n_tot = n_eul*n_th

N_p = 15
N_q = 8

cmax = N_p*N_q
cmat = np.unravel_index(np.arange(cmax), [N_p, N_q])
cmat = np.array(cmat).T

""" Generate Y """

bvec = [0,  15, 25, 60, 85, 115]
bval = [40., 20., -10., 6., -4., 2.]

Y = np.zeros(n_tot, dtype='complex128')

for ii in xrange(len(bvec)):

    p, q = cmat[bvec[ii], :]

    basis_p = gsh.gsh_eval(angles[:, 1:4], [p])
    basis_q = np.cos(q*np.pi*angles[:, 0]/L_th)

    Y += bval[ii]*np.squeeze(basis_p)*basis_q

""" Perform the integration """

coeff = np.zeros(cmax, dtype='complex128')

indxvec = gsh.gsh_basis_info()

# constants for integration
bsz_gsh = ((np.pi**3)/3)/n_eul
bsz_cos = L_th/n_th

for ii in xrange(cmax):
    if np.mod(ii, 10) == 0:
        print ii

    p, q = cmat[ii, :]

    basis_p = gsh.gsh_eval(angles[:, 1:4], [p])
    basis_q = np.cos(q*np.pi*angles[:, 0]/L_th)

    ep_set = np.squeeze(basis_p)*basis_q

    l = indxvec[p, 0]
    c_gsh = (1./(2.*l+1.))*(3./(2.*np.pi**2))

    if q == 0:
        c_cos = 1./L_th
    else:
        c_cos = 2./L_th

    c_tot = c_gsh*c_cos*bsz_gsh*bsz_cos

    tmp = c_tot*np.sum(Y*ep_set.conj()*np.sin(angles[:, 2]))

    del ep_set

    coeff[ii] = tmp


""" plot a visual representation of the coefficients """

fig = plt.figure(num=1, figsize=[12, 8])
plt.bar(np.arange(cmax), coeff.real)
plt.title("coefficients from integration")
plt.grid(True)

plt.xticks(np.arange(0, cmax, 5), rotation='vertical')
plt.yticks(np.arange(-12, 42, 2))

""" check the integration accuracy """

Y_ = np.zeros(n_tot, dtype='complex128')

for ii in xrange(cmax):
    if np.mod(ii, 10) == 0:
        print ii

    p, q = cmat[ii, :]

    basis_p = gsh.gsh_eval(angles[:, 1:4], [p])
    basis_q = np.cos(q*np.pi*angles[:, 0]/L_th)

    ep_set = np.squeeze(basis_p)*basis_q

    Y_ += coeff[ii]*ep_set

print "min(Y): %s" % np.min(Y)
print "mean(Y): %s" % np.mean(Y)
print "max(Y): %s" % np.max(Y)
print "std(Y): %s" % np.std(Y)
print "\n"

print "mean(Y_): %s" % np.mean(Y_)

error = np.abs(Y_.real - Y.real)

print "mean error: %s" % np.mean(error)
print "std of error: %s" % np.std(error)
print "max error: %s" % np.max(error)

""" Plot the regression results """

# thr = (1E3)/n_tot
# print "selection zone: %s" % thr

# tmp1 = np.isclose(angles[:, 0], 5*inc2rad)
# tmp2 = np.isclose(angles[:, 3], 5*inc2rad)

# print np.sum(tmp1)
# print np.sum(tmp2)

# ang_sel = tmp1*tmp2
# print np.sum(ang_sel)

# del tmp1, tmp2

theta_U = np.unique(angles[:, 0])
print theta_U
phi2_U = np.unique(angles[:, 3])
print phi2_U

ang_sel = (angles[:, 0] == theta_U[5])*(angles[:, 3] == phi2_U[5])

fig = plt.figure(num=2, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(angles[ang_sel, 1], angles[ang_sel, 2], Y[ang_sel].real, c='b')
ax.scatter(angles[ang_sel, 1], angles[ang_sel, 2], Y_[ang_sel].real, c='r')

# ang_sel = np.abs(euler[:, 1] - np.pi/2) < thr

# fig = plt.figure(num=3, figsize=[10, 6])
# ax = fig.add_subplot(111, projection='3d')

# ax.scatter(euler[ang_sel, 0], euler[ang_sel, 2], Y[ang_sel].real, c='b')
# ax.scatter(euler[ang_sel, 0], euler[ang_sel, 2], Y_[ang_sel].real, c='r')

plt.show()
