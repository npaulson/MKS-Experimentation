import numpy as np
import matplotlib.pyplot as plt
import h5py


def variance(el, ns_tot, step):

    f = h5py.File("sve_reduced_all.hdf5", 'r')
    ratios = f.get('ratios')[...]
    f.close()

    plt.figure(2)
    plt.plot(np.arange(ratios.size), ratios)
    plt.xlabel('pc number')
    plt.ylabel('pca explained variance (%)')
    plt.title('pca explained variance plot')
    plt.show()

    plt.show()


if __name__ == '__main__':
    el = 21
    ns_tot = 90
    step = 0

    variance(el, ns_tot, step)
