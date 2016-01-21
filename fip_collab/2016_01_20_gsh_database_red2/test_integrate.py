import numpy as np
import gsh_hex_tri_L0_16 as gsh
import matplotlib.pyplot as plt
import h5py
from mpl_toolkits.mplot3d import Axes3D


phi1max = 2*np.pi
phimax = np.pi/2.
phi2max = np.pi/3.

N_L = 215

f = h5py.File('var_extract_6deg_fip.hdf5', 'r')
var_set = f.get('var_set')
print "var_set shape: %s" % str(var_set.shape)

phi1_lt_pi = var_set[:, 0] < phi1max

phi1 = np.float64(var_set[phi1_lt_pi, 0])
phi = np.float64(var_set[phi1_lt_pi, 1])
phi2 = np.float64(var_set[phi1_lt_pi, 2])
Y = np.float64(var_set[phi1_lt_pi, 3])

f.close

n_tot = phi1.shape[0]

euler = np.zeros((n_tot, 3), dtype='float64')
euler[:, 0] = phi1
euler[:, 1] = phi
euler[:, 2] = phi2

""" Calculate X """

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

plt.xticks(np.arange(0, N_L, 10), rotation='vertical')
# plt.yticks(np.arange(-12, 42, 2))

""" Check the regression accuracy """

Y_ = np.zeros(n_tot, dtype='complex128')

for ii in xrange(N_L):
    if np.mod(ii, 10) == 0:
        print ii

    Y_ += coeff[ii]*gsh.gsh_eval(euler, [ii])[:, 0]


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

ang_sel = phi2 == ang_vec[3]

fig = plt.figure(num=2, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(phi1[ang_sel], phi[ang_sel], Y[ang_sel], c='b')
ax.scatter(phi1[ang_sel], phi[ang_sel], Y_[ang_sel].real, c='r')

ang_vec = np.unique(phi)
print ang_vec
ang_sel = phi == ang_vec[4]

fig = plt.figure(num=3, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(phi1[ang_sel], phi2[ang_sel], Y[ang_sel], c='b')
ax.scatter(phi1[ang_sel], phi2[ang_sel], Y_[ang_sel].real, c='r')

plt.show()
