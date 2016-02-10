import numpy as np
import h5py


f = h5py.File('final_results.hdf5', 'r')
data = f.get('results')[...].real

print "mean error: %s" % data[:, 7].mean()
print "maximum error: %s" % data[:, 7].max()

print "minimum function value: %s" % data[:, 5].min()
print "minimum reconstruction value: %s" % data[:, 6].min()

print "mean function value: %s" % data[:, 5].mean()
print "mean reconstruction value: %s" % data[:, 6].mean()

print "maximum function value: %s" % data[:, 5].max()
print "maximum reconstruction value: %s" % data[:, 6].max()

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
    (data[:, 3] == phi2) * \
    (data[:, 4] == en)

print "theta: %s" % th
print "phi2: %s" % phi2
print "en: %s" % en

parameters = np.array([th, phi2, en])

slice = data[ang_sel, :]
print slice.shape

f = h5py.File('slice.hdf5', 'w')
f.create_dataset('slice', data=slice)
f.create_dataset('parameters', data=parameters)
f.close()
