import numpy as np
import h5py
import matplotlib.pyplot as plt


f = h5py.File('XtXtotal.hdf5', 'r')
XtX = f.get('XtX')[...]
f.close()

plt.figure(1)
ax = plt.imshow(XtX.real,
	            origin='lower',
	            interpolation='none',
	            cmap='bone')
plt.colorbar(ax)

plt.show()