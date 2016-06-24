import numpy as np
import matplotlib.pyplot as plt
import h5py


def variance():

    f = h5py.File("pca_data.hdf5", 'r')
    ratios = f.get('ratios')[...]
    f.close()

    plt.figure(2, figsize=[6, 5])
    plt.plot(np.arange(ratios.size)+1, np.cumsum(ratios), 'k.-')
    plt.xlabel('pc number')
    tc = np.int16(np.ceil(ratios.size/10.))
    plt.xticks(np.arange(0, ratios.size+tc, tc))
    plt.axis([0, ratios.size, 98, 100.1])
    plt.ylabel('pca cumulative explained variance (%)')
    plt.title('pca cumulative explained variance plot')
    plt.tight_layout()

if __name__ == '__main__':
    variance()
    plt.show()
