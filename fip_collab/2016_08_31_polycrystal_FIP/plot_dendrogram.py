import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as hie
from constants import const
import h5py


def pltdend(ns_set, sid_set, names_set, H):

    C = const()

    fig = plt.figure(figsize=[5, 5])

    y = np.zeros([len(sid_set), C['n_pc_tot']])
    # y = np.zeros([len(sid_set), 2])

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % H, 'r')

    for ii in xrange(len(sid_set)):

        reduced = f_red.get('reduced_%s' % sid_set[ii])[...]

        y[ii, :] = np.mean(reduced, axis=0)
        # y[ii, :] = np.mean(reduced[:, :2], axis=0)

    f_red.close()

    Z = hie.linkage(y, method='average')

    hie.dendrogram(Z, labels=names_set, orientation='right', distance_sort='ascending')

    plt.xlabel('Euclidean distance')

    plt.tight_layout()

    fig_name = 'dendrogram_L%s.png' % H
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':
    C = const()
    ns_set = C['ns_val']
    sid_set = C['sid_val']
    names_set = C['names_val']

    pltdend(ns_set, sid_set, names_set)

    plt.show()
