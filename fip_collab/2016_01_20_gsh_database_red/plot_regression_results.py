import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import h5py


f = h5py.File('regression_results_6deg_p215_q9.hdf5', 'r')
# f = h5py.File('regression_results_p215_q19.hdf5', 'r')

data = f.get('results')[...].real

print "mean error: %s" % data[:, 6].mean()
print "maximum error: %s" % data[:, 6].max()

print "minimum function value: %s" % data[:, 4].min()
print "minimum reconstruction value: %s" % data[:, 5].min()

print "mean function value: %s" % data[:, 4].mean()
print "mean reconstruction value: %s" % data[:, 5].mean()

print "maximum function value: %s" % data[:, 4].max()
print "maximum reconstruction value: %s" % data[:, 5].max()

theta_U = np.unique(data[:, 0])
print theta_U
phi2_U = np.unique(data[:, 3])
print phi2_U

ang_sel = (data[:, 0] == theta_U[-1])*(data[:, 3] == phi2_U[-1])

fig = plt.figure(num=2, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(data[ang_sel, 1], data[ang_sel, 2], data[ang_sel, 4].real, c='b')
ax.scatter(data[ang_sel, 1], data[ang_sel, 2], data[ang_sel, 5].real, c='r')

# phi_U = np.unique(data[:, 2])
# print phi_U
# phi2_U = np.unique(data[:, 3])
# print phi2_U

# ang_sel = (data[:, 2] == phi_U[-1])*(data[:, 3] == phi2_U[-1])

# fig = plt.figure(num=2, figsize=[10, 6])
# ax = fig.add_subplot(111, projection='3d')

# ax.scatter(data[ang_sel, 0], data[ang_sel, 1], data[ang_sel, 4].real, c='b')
# ax.scatter(data[ang_sel, 0], data[ang_sel, 1], data[ang_sel, 5].real, c='r')

f.close()
plt.show()
