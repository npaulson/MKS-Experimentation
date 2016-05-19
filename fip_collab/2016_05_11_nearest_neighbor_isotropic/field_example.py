import matplotlib.pyplot as plt
import numpy as np


slc = 10

MICR1 = np.random.random((21, 21, 21))
MICR2 = 1.5*np.random.random((21, 21, 21))

"""Plot slices of the response"""
plt.figure(num=1, figsize=[8, 3])

dmin = np.min([MICR1[slc, :, :], MICR2[slc, :, :]])
dmax = np.max([MICR1[slc, :, :], MICR2[slc, :, :]])

plt.subplot(121)
ax = plt.imshow(MICR1[slc, :, :], origin='lower',
                interpolation='none', cmap='viridis', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('microstructure 1, slice %s' % slc)

plt.subplot(122)
ax = plt.imshow(MICR2[slc, :, :], origin='lower',
                interpolation='none', cmap='viridis', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('microstructure 2, slice %s' % slc)

plt.show()
