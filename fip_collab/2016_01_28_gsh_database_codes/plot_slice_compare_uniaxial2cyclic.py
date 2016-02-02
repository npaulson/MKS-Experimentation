import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import h5py


f = h5py.File('slice.hdf5', 'r')
slc_uni = f.get('slice_uni')[...].real
slc_cyc = f.get('slice_cyc')[...].real
par = f.get('parameters')[...]
f.close()

th = np.round(par[0]*180./np.pi, 2)
phi2 = np.round(par[1]*180./np.pi, 0)
en = np.round(par[2], 4)

fig = plt.figure(num=1, figsize=[14, 8])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(slc_uni[:, 1], slc_uni[:, 2], slc_uni[:, 5], c='b')
ax.scatter(slc_cyc[:, 1], slc_cyc[:, 2], slc_cyc[:, 5], c='r')

title_text = "theta = %s, phi2 = %s, en = %s" % (th, phi2, en)
ax.set_title(title_text)
ax.set_xlabel('phi1')
ax.set_ylabel('Phi')
ax.set_zlabel('FIP')

plt.show()
