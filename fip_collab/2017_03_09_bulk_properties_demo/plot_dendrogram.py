import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as hie
from constants import const
import h5py


def pltdend(C, ns_set, set_id_set, names_set, H):

    plt.figure(figsize=[5, 5])

    y = np.zeros([len(set_id_set), C['n_pc_tot']])
    # y = np.zeros([len(set_id_set), 2])

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % H, 'r')

    for ii in xrange(len(set_id_set)):

        reduced = f_red.get('reduced_%s' % set_id_set[ii])[...]

        y[ii, :] = np.mean(reduced, axis=0)
        # y[ii, :] = np.mean(reduced[:, :2], axis=0)

    f_red.close()

    Z = hie.linkage(y, method='average')

    hie.dendrogram(Z, labels=names_set, orientation='right', distance_sort='ascending')

    plt.xlabel('Euclidean distance')

    plt.tight_layout()


if __name__ == '__main__':

    C = const()
    ns_set = C['ns_val']
    set_id_set = C['set_id_val']
    names_set = C['names_val']

    pltdend(C, ns_set, set_id_set, names_set)

    plt.show()
