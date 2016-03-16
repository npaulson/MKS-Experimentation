import numpy as np
import matplotlib.pyplot as plt
import h5py


def pltA(el, ns, set_id, step, sn, hval):

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    euler = f.get('euler')[sn, 0, :].reshape(el, el, el)
    f.close()

    f = h5py.File("D_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    auto = f.get('ff_auto')[sn, hval, ...]
    f.close()

    auto_centered = np.fft.fftshift(auto)

    """Plot slices of the response"""
    plt.figure(num=1, figsize=[9, 2.7])

    plt.subplot(121)
    ax = plt.imshow(euler[0, :, :], origin='lower',
                    interpolation='none', cmap='magma')
    plt.colorbar(ax)
    plt.title('phi1 field')

    plt.subplot(122)
    ax = plt.imshow(auto_centered[10, :, :].real, origin='lower',
                    interpolation='none', cmap='viridis')
    plt.colorbar(ax)
    plt.title('real(autocorrelation), basis %s' % hval)

    plt.show()


if __name__ == '__main__':
    el = 21
    ns = 10
    set_id = 'random'
    step = 0
    sn = 0
    hval = 1

    pltA(el, ns, set_id, step, sn, hval)
