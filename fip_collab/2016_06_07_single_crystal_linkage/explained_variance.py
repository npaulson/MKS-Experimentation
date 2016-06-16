import numpy as np
import matplotlib.pyplot as plt
import h5py


def variance(ns_tot):

    f = h5py.File("pca_data.hdf5", 'r')
    ratios = f.get('ratios')[...]
    f.close()

    plt.figure(2)
    plt.plot(np.arange(ratios.size)+1, np.cumsum(ratios), 'kx-', markersize=4)
    plt.xlabel('pc number')
    plt.xticks(np.arange(0, ratios.size, np.int16(ratios.size/10))+1)
    plt.ylabel('pca cumulative explained variance (%)')
    plt.title('pca cumulative explained variance plot')
    plt.show()

    plt.show()


if __name__ == '__main__':
    ns_tot = 90
    variance(ns_tot)
