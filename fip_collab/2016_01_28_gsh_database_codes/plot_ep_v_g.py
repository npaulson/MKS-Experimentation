import h5py
import numpy as np
import matplotlib.pyplot as plt
import gsh_hex_tri_L0_16 as gsh
from mpl_toolkits.mplot3d import Axes3D


""" define important variables """

N_p = 100  # number of GSH bases to evaluate

inc_eul = 5.  # degree increment for angular variables

n_p1 = 360/inc_eul  # number of phi1 samples for FZ
n_P = 90/inc_eul  # number of Phi samples for FZ
n_p2 = 60/inc_eul  # number of phi2 samples for FZ

n_eul = n_p1*n_P*n_p2

f = h5py.File('var_extract_total.hdf5', 'r')
data = f.get('var_set')[...].real

theta_U = np.unique(data[:, 0])
print "unique theta: %s" % str(theta_U)
phi1_U = np.unique(data[:, 1])
print "unique phi1: %s" % str(phi1_U)
Phi_U = np.unique(data[:, 2])
print "unique Phi: %s" % str(Phi_U)
phi2_U = np.unique(data[:, 3])
print "unique phi2: %s" % str(phi2_U)
en_U = np.unique(data[:, 4])
print "unique en: %s" % str(en_U)

np.random.seed()

th = theta_U[np.int64(np.random.rand()*theta_U.size)]
# phi1 = phi1_U[np.int64(np.random.rand()*phi1_U.size)]
# Phi = Phi_U[np.int64(np.random.rand()*Phi_U.size)]
phi2 = phi2_U[np.int64(np.random.rand()*phi2_U.size)]
en = en_U[-2]
# en = en_U[np.int64(np.random.rand()*en_U.size)]

ang_sel = (data[:, 0] == th) * \
    (data[:, 4] == en)

X = data[ang_sel, 1:4]
Y = data[ang_sel, 5]

"""perform the integration and prediction"""

indxvec = gsh.gsh_basis_info()

bsz_eul = ((np.pi**3)/3)/n_eul

Y_ = np.zeros(Y.shape, dtype='complex128')

coeff = np.zeros(N_p, dtype='complex128')

for p in xrange(N_p):

    ep_set = np.squeeze(gsh.gsh_eval(X, [p]))

    l = indxvec[p, 0]
    c_eul = (1./(2.*l+1.))*(3./(2.*np.pi**2))

    c_tot = c_eul*bsz_eul

    tmp = c_tot*np.sum(Y*ep_set.conj()*np.sin(X[:, 1]))
    coeff[p] = tmp

    Y_ += tmp*ep_set

print "\nmin(Y): %s" % np.min(Y)
print "mean(Y): %s" % np.mean(Y)
print "max(Y): %s" % np.max(Y)

error = np.abs(Y_.real - Y.real)

print "mean error: %s" % np.mean(error)
print "std of error: %s" % np.std(error)
print "max error: %s" % np.max(error)

""" Plot the regression results """

ang_sel2 = (X[:, 2] == phi2)

fig = plt.figure(num=1, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(X[ang_sel2, 0], X[ang_sel2, 1], Y[ang_sel2].real, c='b')
ax.scatter(X[ang_sel2, 0], X[ang_sel2, 1], Y_[ang_sel2].real, c='r')

title_text = "theta = %s, phi2 = %s, en = %s" % (th, phi2, en)
ax.set_title(title_text)
ax.set_xlabel('phi1')
ax.set_ylabel('Phi')
ax.set_zlabel('FIP')

plt.show()
