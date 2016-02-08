import numpy as np
import h5py


f = h5py.File('var_extract_total.hdf5', 'r')
data = f.get('var_set')[...].real
f.close()

en = 0.0080
n_cyc = 10

"""Perform analysis on statistics cycle to cycle"""

ang_sel = data[:, 4] == 0
min_cyc0 = data[ang_sel, 5].min()
min_cyc0 = data[ang_sel, 5].min()
min_cyc0 = data[ang_sel, 5].min()

minvec = np.zeros(n_cyc)
meanvec = np.zeros(n_cyc)
maxvec = np.zeros(n_cyc)

for cyc in xrange(n_cyc):

    ang_sel = data[:, 4] == cyc
    minvec[cyc] = data[ang_sel, 5].min()
    meanvec[cyc] = data[ang_sel, 5].mean()
    maxvec[cyc] = data[ang_sel, 5].max()

print "minimum FIP per cycle: %s" % str(minvec)
print "mean FIP per cycle: %s" % str(meanvec)
print "maximum FIP per cycle: %s" % str(maxvec)

diffvec = np.zeros(n_cyc - 1)

for cyc in xrange(1, n_cyc):

    ang_sel_prev = data[:, 4] == cyc - 1
    ang_sel_curr = data[:, 4] == cyc

    diff = np.abs(data[ang_sel_curr, 5] - data[ang_sel_prev, 5])

    diffvec[cyc-1] = diff.mean()

print "mean of absolute value of FIP difference per cycle: %s" % str(diffvec)

"""Select the slice"""

theta_U = np.unique(data[:, 0])
print "unique theta: %s" % str(theta_U)
phi1_U = np.unique(data[:, 1])
print "unique phi1: %s" % str(phi1_U)
Phi_U = np.unique(data[:, 2])
print "unique Phi: %s" % str(Phi_U)
phi2_U = np.unique(data[:, 3])
print "unique phi2: %s" % str(phi2_U)
cyc_U = np.unique(data[:, 4])
print "unique cyc: %s" % str(cyc_U)

np.random.seed()

th = theta_U[np.int64(np.random.rand()*theta_U.size)]
# phi1 = phi1_U[np.int64(np.random.rand()*phi1_U.size)]
Phi = Phi_U[np.int64(np.random.rand()*Phi_U.size)]
phi2 = phi2_U[np.int64(np.random.rand()*phi2_U.size)]
# cyc = cyc_U[np.int64(np.random.rand()*en_U.size)]

parameters = np.array([th, Phi, phi2, en])

print "theta: %s" % th
print "Phi: %s" % Phi
print "phi2: %s" % phi2
print "en: %s" % en

ang_sel = (data[:, 0] == th) * \
    (data[:, 2] == Phi) * \
    (data[:, 3] == phi2)

slice = data[ang_sel, :]

f = h5py.File('slice.hdf5', 'w')
f.create_dataset('slice', data=slice)
f.create_dataset('parameters', data=parameters)
f.create_dataset('minvec', data=minvec)
f.create_dataset('meanvec', data=meanvec)
f.create_dataset('maxvec', data=maxvec)
f.create_dataset('diffvec', data=diffvec)
f.close()
