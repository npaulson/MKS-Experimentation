import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import h5py


def pltPC(el, ns_set, set_id_set, step):

    plt.figure(num=3, figsize=[10, 7])

    # colormat = np.random.rand(len(set_id_set), 3)
    colormat = np.array([[.3, .3, 1.],
                         [.3, 1., .3],
                         [1., .2, .2],
                         [0., .7, .7],
                         [.7, .0, .7],
                         [.7, .7, .0]])

    n_sets = len(set_id_set)

    """find the internal and external set distances for the first set"""
    f = h5py.File("ref_%s%s_s%s.hdf5" %
                  (ns_set[0], set_id_set[0], step), 'a')
    set1 = f.get('pc_corr')[...]
    f.close()

    for ii in xrange(n_sets):
        f = h5py.File("ref_%s%s_s%s.hdf5" %
                      (ns_set[ii], set_id_set[ii], step), 'a')
        set2 = f.get('pc_corr')[...]
        f.close()

        dist = cdist(set1, set2)

        plt.hist(dist.reshape(dist.size),
                 bins=20, histtype='step', color=colormat[ii, :],
                 label=set_id_set[ii])

    plt.title("Euclidean PC distance histograms for set %s versus other sets" % set_id_set[0])
    plt.xlabel("Euclidean PC distance")
    plt.ylabel("count")
    plt.legend(loc='upper right', shadow=True, fontsize='medium')

    plt.show()


if __name__ == '__main__':
    el = 21
    ns_cal = [10, 10, 10]
    set_id_cal = ['randomD3D', 'transverseD3D', 'basaltransD3D']
    step = 0

    pltPC(el, ns_cal, set_id_cal, step)
