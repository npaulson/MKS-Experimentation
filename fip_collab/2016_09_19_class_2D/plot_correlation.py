import numpy as np
import matplotlib.pyplot as plt
import h5py


def pltcorr(el, ns, set_id, sn, iA):

    f = h5py.File("spatial_stats.hdf5", 'r')
    sves = f.get('sves_%s' % set_id)[sn, ...]
    corr = f.get('ff_%s' % set_id)[sn, iA, ...]
    f.close()

    corr_centered = np.fft.fftshift(corr)

    """Plot slices of the response"""
    plt.figure(num=1, figsize=[10, 4])

    plt.subplot(121)
    ax = plt.imshow(sves, origin='lower',
                    interpolation='none', cmap='gray')
    plt.colorbar(ax)
    plt.title('microstructure')

    plt.subplot(122)
    ax = plt.imshow(corr_centered, origin='lower',
                    interpolation='none', cmap='jet')
    plt.colorbar(ax)
    plt.title('correlation: 0, %s' % iA)

    plt.show()


if __name__ == '__main__':
    el = 21
    ns = 60
    set_id = 'improcess'
    step = 0
    sn = 29
    iA = 1

    pltcorr(el, ns, set_id, step, sn, iA)
