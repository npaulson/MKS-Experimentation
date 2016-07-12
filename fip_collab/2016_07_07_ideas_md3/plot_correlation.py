import numpy as np
import matplotlib.pyplot as plt
from constants import const
import h5py


def pltcorr(ns, set_id, sn, cnum):

    C = const()

    f = h5py.File("spatial_L%s.hdf5" % C['H'], 'r')
    corr = f.get('ff_%s' % set_id)[sn, cnum, ...]
    f.close()

    corr_centered = np.fft.fftshift(corr)

    """Plot slices of the response"""
    fig = plt.figure(figsize=[4, 3.5])

    slc = np.int16(np.floor(C['vmax']/2.))
    ax = plt.imshow(corr_centered[slc, :, :], origin='lower',
                    interpolation='none', cmap='viridis')
    plt.colorbar(ax)

    plt.title('correlation: %s, %s' % (C['cmat'][cnum, 0],
                                       C['cmat'][cnum, 1]))

    fig_name = 'correlation_%s_sn%s_L%s.png' % (set_id, sn, cnum)
    fig.canvas.set_window_title(fig_name)


if __name__ == '__main__':
    ns = 10
    set_id = 'bicrystal'
    step = 0
    sn = 5
    iA = 4
    iB = 2

    pltcorr(ns, set_id, step, sn, iA, iB)
    plt.show()
