import numpy as np
import matplotlib.pyplot as plt
import h5py


def pltcorr(el, ns, set_id, step, sn, iA, iB):

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    euler = f.get('euler')[sn, 0, :].reshape(el, el, el)
    corr = f.get('ff')[sn, iA, iB, ...]
    f.close()

    corr_centered = np.fft.fftshift(corr)

    """Plot slices of the response"""
    plt.figure(num=1, figsize=[11, 2.7])

    plt.subplot(121)
    ax = plt.imshow(euler[10, :, :], origin='lower',
                    interpolation='none', cmap='magma')
    plt.colorbar(ax)
    plt.title('phi1 field')

    plt.subplot(122)
    ax = plt.imshow(corr_centered[10, :, :], origin='lower',
                    interpolation='none', cmap='viridis')
    plt.colorbar(ax)
    plt.title('ff: %s, %s' % (iA, iB))

    # plt.subplot(131)
    # ax = plt.imshow(euler[0, :, :], origin='lower',
    #                 interpolation='none', cmap='magma')
    # plt.colorbar(ax)
    # plt.title('phi1 field')

    # plt.subplot(132)
    # ax = plt.imshow(auto_centered[10, :, :].real, origin='lower',
    #                 interpolation='none', cmap='viridis')
    # plt.colorbar(ax)
    # plt.title('real(ff): %s, %s' % (iA, iB))

    # plt.subplot(133)
    # ax = plt.imshow(auto_centered[10, :, :].imag, origin='lower',
    #                 interpolation='none', cmap='viridis')
    # plt.colorbar(ax)
    # plt.title('imag(ff): %s, %s' % (iA, iB))

    plt.show()


if __name__ == '__main__':
    el = 21
    ns = 10
    set_id = 'bicrystal'
    step = 0
    sn = 3
    iA = 2
    iB = 1

    pltcorr(el, ns, set_id, step, sn, iA, iB)
