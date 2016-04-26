import numpy as np
import matplotlib.pyplot as plt
import h5py


def pltcorr(el, ns, set_id, step, sn, iA, iB):

    f = h5py.File("spatial_stats.hdf5", 'r')
    euler = f.get('euler_%s' % set_id)[sn, 0, :].reshape(el, el, el)
    corr = f.get('ff_%s' % set_id)[sn, iA, iB, ...]
    f.close()

    corr_centered = np.fft.fftshift(corr)

    """Plot slices of the response"""
    plt.figure(num=1, figsize=[8, 2.7])

    plt.subplot(121)
    ax = plt.imshow(euler[0, :, :], origin='lower',
                    interpolation='none', cmap='magma')
    plt.colorbar(ax)
    plt.title('phi1 field')

    plt.subplot(122)
    ax = plt.imshow(corr_centered[10, :, :], origin='lower',
                    interpolation='none', cmap='viridis')
    plt.colorbar(ax)
    plt.title('ff: %s, %s' % (iA, iB))

    plt.show()


if __name__ == '__main__':
    el = 21
    ns = 10
    set_id = 'bicrystal'
    step = 0
    sn = 5
    iA = 4
    iB = 2

    pltcorr(el, ns, set_id, step, sn, iA, iB)
