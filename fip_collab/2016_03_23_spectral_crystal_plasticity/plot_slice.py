import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import h5py


f = h5py.File('slice.hdf5', 'r')
slc = f.get('slice')[...]
par = f.get('parameters')[...]
f.close()

var = par[0]
th = np.round(np.float(par[1])*180./np.pi, 2)
phi2 = np.round(np.float(par[2])*180./np.pi, 0)

fig = plt.figure(num=1, figsize=[14, 8])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(slc[::3, 1], slc[::3, 2], slc[::3, 4].real, c='b')
ax.scatter(slc[::3, 1], slc[::3, 2], slc[::3, 5].real, c='r')

title_text = "%s, theta = %s, phi2 = %s" % (var, th, phi2)
ax.set_title(title_text)
ax.set_xlabel('phi1')
ax.set_ylabel('Phi')
ax.set_zlabel('param')

plt.show()
