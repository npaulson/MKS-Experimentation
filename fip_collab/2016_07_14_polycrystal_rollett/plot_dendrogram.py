import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as hie
from constants import const
import h5py


def pltdend(set_id_set, names_set, H):

    C = const()

    fig = plt.figure(figsize=[6, 6])

    y = np.zeros([len(set_id_set), C['n_pc_tot']])
    # y = np.zeros([len(set_id_set), 2])

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % H, 'r')

    for ii in xrange(len(set_id_set)):

        reduced = f_red.get('reduced_%s' % set_id_set[ii])[...]
        y[ii, :] = reduced
        # y[ii, :] = reduced[:2]

    f_red.close()

    Z = hie.linkage(y, method='average')

    # hie.dendrogram(Z, orientation='top', distance_sort='ascending')
    # plt.xticks(10*np.arange(8)+5, names_set, rotation=45.0)

    hie.dendrogram(Z, labels=names_set, orientation='right', distance_sort='ascending')

    plt.xlabel('Euclidean distance')

    plt.tight_layout()

    fig_name = 'dendrogram_L%s.png' % H
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':

    C = const()
    ns_set = C['ns_val']
    set_id_set = C['set_id_val']
    names_set = C['names_val']

    pltdend(ns_set, set_id_set, names_set)

    plt.show()
