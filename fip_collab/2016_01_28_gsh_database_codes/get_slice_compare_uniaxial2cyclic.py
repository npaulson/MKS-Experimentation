import numpy as np
import h5py


f = h5py.File('var_extract_total_uniaxial.hdf5', 'r')
data = f.get('var_set')[...].real
f.close()

fC = h5py.File('var_extract_total_cyclic.hdf5', 'r')
dataC = fC.get('var_set')[...].real
fC.close()

ang_sel = (data[:, 4] == 0.0080)

print "minimum uniaxial value: %s" % data[ang_sel, 5].min()
print "minimum cyclic value: %s" % dataC[:, 5].min()

print "mean uniaxial value: %s" % data[ang_sel, 5].mean()
print "mean cyclic value: %s" % dataC[:, 5].mean()

print "maximum uniaxial value: %s" % data[ang_sel, 5].max()
print "maximum cyclic value: %s" % dataC[:, 5].max()

error = np.abs(data[ang_sel, :]-dataC)
print "mean difference: %s" % error.mean()
print "maximum difference: %s" % error.max()

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
en = 0.0080
# en = en_U[np.int64(np.random.rand()*en_U.size)]

parameters = np.array([th, phi2, en])

print "theta: %s" % th
print "phi2: %s" % phi2
print "en: %s" % en

ang_sel_uni = (data[:, 0] == th) * \
    (data[:, 3] == phi2) * \
    (data[:, 4] == en)

slice_uni = data[ang_sel_uni, :]

ang_sel_cyc = (dataC[:, 0] == th) * \
    (dataC[:, 3] == phi2) * \
    (dataC[:, 4] == en)

slice_cyc = dataC[ang_sel_cyc, :]

f = h5py.File('slice.hdf5', 'w')
f.create_dataset('slice_uni', data=slice_uni)
f.create_dataset('slice_cyc', data=slice_cyc)
f.create_dataset('parameters', data=parameters)
f.close()
