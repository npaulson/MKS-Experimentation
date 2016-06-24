import numpy as np
import matplotlib.pyplot as plt
from constants import const
import h5py


def pltdist():

    C = const()

    """load the distance matrices"""
    f = h5py.File("dist_L%s.hdf5" % C['H'], 'r')
    d_cal = f.get('dist_cal')[...]
    d_val = f.get('dist_val')[...]
    f.close()

    """find the range of values for plotting later"""
    vmin = np.min([d_cal.min(), d_val.min()])
    vmax = np.max([d_cal.max(), d_val.max()])

    fig = plt.figure(figsize=[8, 3])

    """Plot distance chart for cal"""
    plt.subplot(121)

    ax = plt.imshow(d_cal, origin='lower',
                    interpolation='none',
                    vmin=vmin, vmax=vmax,
                    cmap='magma')

    plt.xticks(np.arange(d_cal.shape[0]),
               C['names_cal'], rotation=90)
    plt.yticks(np.arange(d_cal.shape[0]),
               C['names_cal'], rotation=0)

    plt.colorbar(ax)

    """Plot distance chart for val"""
    plt.subplot(122)

    ax = plt.imshow(d_val, origin='lower',
                    interpolation='none',
                    vmin=vmin, vmax=vmax,
                    cmap='magma')

    plt.xticks(np.arange(d_val.shape[0]),
               C['names_val'], rotation=90)
    plt.yticks(np.arange(d_val.shape[0]),
               C['names_val'], rotation=0)

    plt.colorbar(ax)

    plt.tight_layout()

    fig_name = 'dist_L%s.png' % C['H']
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':
    pltdist()
    plt.show()
