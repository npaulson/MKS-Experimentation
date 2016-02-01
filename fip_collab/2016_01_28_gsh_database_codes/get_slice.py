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
print theta_U
phi2_U = np.unique(data[:, 3])
print phi2_U
en_U = np.unique(data[:, 4])

ang_sel = (data[:, 0] == theta_U[13]) * \
    (data[:, 3] == phi2_U[15]) * \
    (data[:, 4] == en_U[-1])

slice = data[ang_sel, :]
print slice.shape

f = h5py.File('slice.hdf5', 'w')
f.create_dataset('slice', data=slice)
f.close()
