import h5py
import numpy as np
import matplotlib.pyplot as plt

el = 21
slc = 1

filename = "theta_fields.hdf5"

f = h5py.File(filename, 'r')
slc_mat = f.get('alltheta')[:, :, slc, :]*(180/np.pi)
envec = f.get('envec')[...]

n_sub = envec.size

"""Find the minumum and maximum of the slices"""
dmin = slc_mat.min()
dmax = slc_mat.max()

fig, axs = plt.subplots(3, 4, figsize=(4*3, 3*3))

"""Plot slices of the response"""
for ii in xrange(n_sub):

    ax = plt.subplot(3, 4, ii+1)
    im = ax.imshow(slc_mat[ii, ...], origin='lower',
                   interpolation='none', cmap='jet', vmin=dmin, vmax=dmax)
    plt.title('$|\epsilon^t|$ = %s' % np.round(envec[ii], 5))

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
fig.colorbar(im, cax=cbar_ax)

plt.figure(2)

dmin = np.min([slc_mat[0, ...], slc_mat[-1, ...]])
dmax = np.max([slc_mat[0, ...], slc_mat[-1, ...]])

plt.subplot(131)

plt.imshow(slc_mat[0, ...], origin='lower',
           interpolation='none', cmap='plasma',
           vmin=dmin, vmax=dmax)
plt.title("theta field at first step")
plt.colorbar()

plt.subplot(132)

plt.imshow(slc_mat[-1, ...], origin='lower',
           interpolation='none', cmap='plasma',
           vmin=dmin, vmax=dmax)
plt.title("theta field at last step")
plt.colorbar()

plt.subplot(133)

diff = slc_mat[-1, ...]-slc_mat[0, ...]

bound = np.max(np.abs(diff))

plt.imshow(slc_mat[-1, ...]-slc_mat[0, ...], origin='lower',
           interpolation='none', cmap='seismic', vmin=-bound, vmax=bound)
plt.title("difference in theta")
plt.colorbar()

f.close()

plt.show()
