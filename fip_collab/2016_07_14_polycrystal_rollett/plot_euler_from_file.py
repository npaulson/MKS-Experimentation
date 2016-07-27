import numpy as np
import matplotlib.pyplot as plt
from constants import const


def plt_slc(set_id, slc):

    C = const()

    parlist = ['phi1', 'Phi', 'phi2',
               'x', 'y', 'z',
               'grain_id', 'phase_id']

    tmp = np.loadtxt('%s.txt' % set_id)
    tmp = tmp.reshape((C['el'], C['el'], C['el'], 8))

    """Plot slices of the response"""
    plt.figure(num=1, figsize=[4, 3])

    par = 0

    ax = plt.imshow(tmp[slc, :, :, par], origin='lower',
                    interpolation='none', cmap='magma')
    plt.colorbar(ax)
    title = parlist[par]
    plt.title(title)

    par = 6

    plt.figure(num=2, figsize=[4, 3])

    ax = plt.imshow(tmp[slc, :, :, par], origin='lower',
                    interpolation='none', cmap='magma')
    plt.colorbar(ax)
    title = parlist[par]
    plt.title(title)

    par = 7

    plt.figure(num=3, figsize=[4, 3])

    ax = plt.imshow(tmp[slc, :, :, par], origin='lower',
                    interpolation='none', cmap='magma')
    plt.colorbar(ax)
    title = parlist[par]
    plt.title(title)

    plt.tight_layout()


if __name__ == '__main__':
    set_id = 'test_micr'
    slc = 0

    plt_slc(set_id, slc)
    plt.show()
