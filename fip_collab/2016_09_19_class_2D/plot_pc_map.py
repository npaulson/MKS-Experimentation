import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import h5py


def pltmap(ns_set, set_id_set, pcA, pcB):

    fig = plt.figure(figsize=[7.5, 5])

    """define the colors of interest"""
    n_col = len(ns_set)
    colormat = cm.rainbow(np.linspace(0, 1, n_col))

    f_red = h5py.File("sve_reduced.hdf5", 'r')

    """plot SVE sets for cal"""

    for ii in xrange(len(ns_set)):

        sid = set_id_set[ii]

        reduced = f_red.get('reduced_%s' % sid)[...]
        meanA = reduced[:, pcA].mean()
        meanB = reduced[:, pcB].mean()

        plt.text(meanA, meanB+0.2, set_id_set[ii],
                 horizontalalignment='center',
                 verticalalignment='center')

        plt.plot(reduced[:, pcA], reduced[:, pcB],
                 marker='s', markersize=6, color=colormat[ii, :],
                 alpha=0.4, linestyle='')
        plt.plot(meanA, meanB,
                 marker='s', markersize=8, color=colormat[ii, :],
                 linestyle='')

    plt.margins(.2)

    plt.xlabel("PC%s" % str(pcA+1))
    plt.ylabel("PC%s" % str(pcB+1))

    plt.grid(linestyle='-', alpha=0.15)

    fig.tight_layout()

    f_red.close()

    plt.show()


if __name__ == '__main__':
    ns = [10, 30, 30]
    set_id = ['incl1', 'bicrystal_orthog', 'improcess']
    pcA = 0
    pcB = 1

    pltmap(ns, set_id, pcA, pcB)
