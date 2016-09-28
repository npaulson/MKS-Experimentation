import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import h5py


def dist_complex(set1, set2):

    s1len = set1.shape[0]
    s2len = set2.shape[0]

    dist = np.zeros((s1len, s2len))

    for ii in xrange(s1len):
        for jj in xrange(s2len):

            tmp = set1[ii, :] - set2[jj, :]
            tmp = np.sqrt(np.sum(tmp**2))
            # tmp = np.sqrt(np.sum(tmp.conj()*tmp))

            dist[ii, jj] = tmp

    return dist


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

    f_red = h5py.File("sve_reduced.hdf5", 'r')
    set1 = f_red.get('reduced_%s' % set_id_set[0])[...]

    for ii in xrange(n_sets):
        set2 = f_red.get('reduced_%s' % set_id_set[ii])[...]

        # dist = cdist(set1, set2)
        dist = dist_complex(set1, set2)

        plt.hist(dist.reshape(dist.size),
                 bins=20, histtype='step', color=colormat[ii, :],
                 label=set_id_set[ii])

    f_red.close()

    plt.title("Euclidean PC distance histograms for set %s versus other sets" % set_id_set[0])
    plt.xlabel("Euclidean PC distance")
    plt.ylabel("count")
    plt.legend(loc='upper right', shadow=True, fontsize='medium')

    plt.show()


if __name__ == '__main__':
    el = 21
    ns_cal = [30, 30, 30]
    set_id_cal = ['incl1', 'incl2', 'incl3']
    step = 0

    pltPC(el, ns_cal, set_id_cal, step)
