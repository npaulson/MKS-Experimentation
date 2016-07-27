import numpy as np
import matplotlib.pyplot as plt
import h5py


def pltcorr(C, set_id, sn, iA):

    f = h5py.File("euler.hdf5", 'r')
    dset_name = 'euler_%s' % set_id
    euler = f.get(dset_name)[sn, 0, :].reshape(C['el'], C['el'], C['el'])
    f.close()

    f = h5py.File("spatial_L%s.hdf5" % C['H'], 'r')
    corr = f.get('ff_%s' % set_id)[sn, iA, ...]
    f.close()

    corr_centered = np.fft.fftshift(corr)

    """Plot slices of the response"""
    plt.figure(figsize=[8, 2.7])

    plt.subplot(121)
    ax = plt.imshow(euler[0, :, :], origin='lower',
                    interpolation='none', cmap='magma')
    plt.colorbar(ax)
    plt.title('phi1 field')

    plt.subplot(122)
    slc = np.int16(np.floor(C['vmax']/2.))
    ax = plt.imshow(corr_centered[slc, :, :], origin='lower',
                    interpolation='none', cmap='viridis')
    plt.colorbar(ax)
    plt.title('ff: %s, %s' % (C['cmat'][iA, 0], C['cmat'][iA, 1]))


if __name__ == '__main__':
    ns = 10
    set_id = 'bicrystal'
    step = 0
    sn = 5
    iA = 4
    iB = 2

    pltcorr(ns, set_id, step, sn, iA, iB)
    plt.show()
