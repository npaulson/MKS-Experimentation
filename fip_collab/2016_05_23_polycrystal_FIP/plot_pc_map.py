import numpy as np
import matplotlib.pyplot as plt
from constants import const
import h5py
import sys


def pltmap(set_id_set, pcA, pcB):

    plt.figure(num=3, figsize=[10, 8])

    # colormat = np.random.rand(len(set_id_set), 3)
    colormat = np.array([[.3, .3, 1.],
                         [.3, 1., .3],
                         [1., .2, .2],
                         [0., .7, .7],
                         [.7, .0, .7],
                         [.7, .7, .0],
                         [.5, .3, .1],
                         [.3, .5, .1],
                         [.1, .3, .5]])

    f_red = h5py.File("spatial_reduced.hdf5", 'r')

    for ii in xrange(len(set_id_set)):

        reduced = f_red.get('reduced_%s' % set_id_set[ii])[...]

        plt.plot(reduced[:, pcA], reduced[:, pcB],
                 marker='o', markersize=7, color=colormat[ii, :],
                 linestyle='', label=set_id_set[ii])

        plt.title("SVE sets in PC space")
        plt.xlabel("PC%s" % str(pcA+1))
        plt.ylabel("PC%s" % str(pcB+1))
        plt.legend(loc='upper right', shadow=True, fontsize='medium')

    f_red.close()

    plt.show()


if __name__ == '__main__':

    C = const()
    ns_set = C['ns_val']
    set_id_set = C['set_id_val']

    pcA = 0
    pcB = np.int64(sys.argv[1])

    pltmap(ns_set, set_id_set, pcA, pcB)
