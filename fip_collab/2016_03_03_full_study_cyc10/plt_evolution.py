import h5py
import numpy as np
import matplotlib.pyplot as plt

el = 21
slc = 1

filename = 'Results_Ti64_Dream3D_XdirLoad_210microns_9261el_AbqInp_PowerLaw' +\
           '_LCF_10cycles_1.hdf5'

f = h5py.File(filename, 'r')

"""
file format:
21 datasets (e.g. step 1 is the min of the first cycle, step 2 is the max)
for each step there is an array of shape [21**3, 24]

for the dataset data_## the columns are as follows:
data_##[#, 0]: grainID
data_##[#, 1:4]: phi1, Phi, phi2
data_##[#, 4-6]: FIP per element, FIP volume averaged
data_##[#, 6:12]: stess components
data_##[#, 12:18]: strain components
data_##[#, 18:24]: plastic strain components
"""

cyc_vec = np.arange(1, 21, 2)
n_cyc = cyc_vec.size

slc_mat = np.zeros([n_cyc, el, el])

for ii in xrange(n_cyc):
    key = 'data_' + str(cyc_vec[ii]).zfill(2)
    rawdata = f.get(key)
    tmp = rawdata[:, 6].reshape(el, el, el)
    slc_mat[ii, ...] = tmp[slc, ...]

"""Find the minumum and maximum of the slices"""
dmin = slc_mat.min()
dmax = slc_mat.max()

fig, axs = plt.subplots(2, 5, figsize=(5*3, 2*3))

"""Plot slices of the response"""
for ii in xrange(n_cyc):

    ax = plt.subplot(2, 5, ii+1)
    im = ax.imshow(slc_mat[ii, ...], origin='lower',
                   interpolation='none', cmap='jet', vmin=dmin, vmax=dmax)
    plt.title('cycle %s' % (ii+1))

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
fig.colorbar(im, cax=cbar_ax)

plt.show()
f.close()
