import numpy as np
import matplotlib.pyplot as plt
from constants import const
import functions as rr
import h5py
import sys


def pltmap(ns_set, set_id_set, pcA, pcB):

    C = const()

    plt.figure(num=3, figsize=[6, 5.75])

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

        set_id = set_id_set[ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]

        plt.plot(reduced[:, pcA], reduced[:, pcB],
                 marker='o', markersize=7, color=colormat[ii, :],
                 linestyle='', label=set_id_set[ii])

        plt.plot(reduced[:, pcA].mean(), reduced[:, pcB].mean(),
                 marker='D', markersize=8, color=colormat[ii, :],
                 linestyle='')

        plt.title("SVE sets in PC space")
        plt.xlabel("PC%s" % str(pcA+1))
        plt.ylabel("PC%s" % str(pcB+1))
        plt.legend(loc='upper right', shadow=True, fontsize='medium')

        varA = np.var(reduced[:, pcA])
        msg = "variance for %s in PC%s: %s" % (set_id, str(pcA+1), varA)
        rr.WP(msg, C['wrt_file'])

        varB = np.var(reduced[:, pcB])
        msg = "variance for %s in PC%s: %s" % (set_id, str(pcB+1), varB)
        rr.WP(msg, C['wrt_file'])

    plt.tight_layout()
    f_red.close()


if __name__ == '__main__':

    C = const()
    ns_set = C['ns_cal']
    set_id_set = C['set_id_cal']

    pcA = np.int64(sys.argv[1])
    pcB = np.int64(sys.argv[2])

    pltmap(ns_set, set_id_set, pcA, pcB)

    plt.show()
