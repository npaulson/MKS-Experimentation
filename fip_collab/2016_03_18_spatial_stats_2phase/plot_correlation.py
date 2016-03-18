import numpy as np
import matplotlib.pyplot as plt
import h5py


def pltcorr(el, ns, set_id, step, sn):

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    sves = f.get('sves')[sn, ...]
    f.close()

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    auto = f.get('ff')[sn, ...]
    f.close()

    corr_centered = np.fft.fftshift(auto)

    """Plot slices of the response"""
    plt.figure(num=1, figsize=[11, 2.7])

    plt.subplot(121)
    ax = plt.imshow(sves[10, :, :], origin='lower',
                    interpolation='none', cmap='magma')
    plt.colorbar(ax)
    plt.title('phi1 field')

    plt.subplot(122)
    ax = plt.imshow(corr_centered[10, :, :], origin='lower',
                    interpolation='none', cmap='viridis')
    plt.colorbar(ax)
    plt.title('ff')

    plt.show()


if __name__ == '__main__':
    el = 21
    ns = 10
    set_id = 'random'
    step = 0
    sn = 0

    pltcorr(el, ns, set_id, step, sn)
