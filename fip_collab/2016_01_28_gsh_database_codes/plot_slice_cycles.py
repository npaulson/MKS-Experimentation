import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import h5py


f = h5py.File('slice.hdf5', 'r')
slc = f.get('slice')[...]
par = f.get('parameters')[...]
meanvec = f.get('meanvec')[...]
f.close()

th = np.round(par[0]*180./np.pi, 2)
Phi = np.round(par[1]*180./np.pi, 0)
phi2 = np.round(par[2]*180./np.pi, 0)
en = np.round(par[3], 4)

fig = plt.figure(num=1, figsize=[14, 8])
ax = fig.add_subplot(111, projection='3d')

ax.scatter(slc[:, 1], slc[:, 4], slc[:, 5].real, c='b')

title_text = "theta = %s, Phi = %s, phi2 = %s, en = %s" % (th, Phi, phi2, en)
ax.set_title(title_text)
ax.set_ylabel('cycles')
ax.set_xlabel('phi1')
ax.set_zlabel('FIP')

plt.figure(num=2, figsize=[8, 6])
plt.plot(np.arange(meanvec.size), meanvec, 'rx-')
plt.xlabel('cycle number')
plt.ylabel('mean FIP value')
plt.title('mean FIP value versus number of cycles')

plt.show()
