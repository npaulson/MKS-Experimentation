import numpy as np
import matplotlib.pyplot as plt
from constants import const
import h5py


def variance():

    C = const()

    f = h5py.File("pca_data_L%s.hdf5" % C['H'], 'r')
    ratios = f.get('ratios')[...]
    f.close()

    data = np.zeros((ratios.size+1,))
    data[1:] = np.cumsum(ratios)

    fig = plt.figure(figsize=[7, 4])
    plt.plot(np.arange(data.size), data, color='k',
             linestyle='-', marker='.', markersize=3)
    plt.xlabel('pc number')

    tc = np.int16(np.ceil(ratios.size/15.))
    plt.xticks(np.arange(0, ratios.size+tc, tc))
    # plt.axis([0, ratios.size, 98, 100.1])

    plt.axis([0, ratios.size, 0, 102])

    plt.ylabel('pca cumulative explained variance (%)')
    # plt.title('pca cumulative explained variance plot')
    plt.tight_layout()

    fig_name = 'explained_variance_L%s.png' % C['H']
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':
    variance()
    plt.show()
