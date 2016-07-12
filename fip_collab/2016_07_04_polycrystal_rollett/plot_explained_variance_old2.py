import numpy as np
import matplotlib.pyplot as plt
from constants import const
import h5py


def variance():

    C = const()

    f = h5py.File("pca_data_L%s.hdf5" % C['H'], 'r')
    ratios = f.get('ratios')[...]
    f.close()

    fig = plt.figure(figsize=[6, 5])

    data = np.zeros((ratios.size+1,))
    data[1:] = np.cumsum(ratios)

    plt.plot(np.arange(data.size), data, 'k.-')
    plt.xlabel('pc number')

    # tc = np.int16(np.ceil(ratios.size/10.))
    # plt.xticks(np.arange(0, ratios.size+tc, tc))

    plt.yticks(np.arange(0, 110, 10))
    plt.axis([0, 20, 0, 105.])
    # plt.axis([0, ratios.size, 98, 100.1])

    plt.ylabel('pca cumulative explained variance (%)')
    # plt.title('pca cumulative explained variance plot')
    plt.tight_layout()

    plt.grid(True)

    fig_name = 'explained_variance_L%s.png' % C['H']
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':
    variance()
    plt.show()
