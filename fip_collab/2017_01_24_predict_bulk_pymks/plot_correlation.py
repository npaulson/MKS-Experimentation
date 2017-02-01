import numpy as np
import matplotlib.pyplot as plt


def pltcorr(micr, corr):

    corr_centered = np.fft.fftshift(corr)

    """Plot slices of the response"""
    plt.figure(figsize=[8, 2.7])

    plt.subplot(121)
    ax = plt.imshow(micr, origin='lower',
                    interpolation='none', cmap='magma')
    plt.colorbar(ax)
    plt.title('microstructure')

    plt.subplot(122)
    ax = plt.imshow(corr_centered, origin='lower',
                    interpolation='none', cmap='viridis')
    plt.colorbar(ax)
    plt.title('correlation')


if __name__ == '__main__':
    ns = 10
    set_id = 'bicrystal'
    step = 0
    sn = 5
    iA = 4
    iB = 2

    pltcorr(ns, set_id, step, sn, iA, iB)
    plt.show()
