import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import h5py


f = h5py.File('regression_results.hdf5', 'r')
data = f.get('results')[...].real

theta_U = np.unique(data[:, 0])
print theta_U
phi2_U = np.unique(data[:, 3])
print phi2_U

ang_sel = (data[:, 0] == theta_U[2])*(data[:, 3] == phi2_U[0])

fig = plt.figure(num=2, figsize=[10, 6])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(data[ang_sel, 1], data[ang_sel, 2], data[ang_sel, 4].real, c='b')
ax.scatter(data[ang_sel, 1], data[ang_sel, 2], data[ang_sel, 5].real, c='r')

f.close()
plt.show()
