import numpy as np
import matplotlib.pyplot as plt
from constants import const
import sys
import h5py


def pltresponse(ns_set, set_id_set, prop, bc, pcA):

    plt.figure(num=4, figsize=[10, 7])

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
    f_link = h5py.File("responses.hdf5", 'r')

    for ii in xrange(len(set_id_set)):

        reduced = f_red.get('reduced_%s' % set_id_set[ii])[...]

        dset_name = "%s_%s_%s" % (prop, bc, set_id_set[ii])
        response = f_link.get(dset_name)[...]

        plt.plot(reduced[:, pcA], response,
                 marker='D', markersize=8, color=colormat[ii, :],
                 linestyle='', label=set_id_set[ii])

        plt.title("%s for %s verus principal components" % (prop, bc))
        plt.xlabel("PC %s" % str(pcA+1))
        plt.ylabel(prop)
        plt.legend(loc='upper right', shadow=True, fontsize='medium')

    f_red.close()
    f_link.close()

    plt.show()


if __name__ == '__main__':

    C = const()
    ns_set = C['ns_val']
    set_id_set = C['set_id_val']

    prop = 'yield'
    bc = 'bc1'
    pcA = np.int64(sys.argv[1])

    pltresponse(ns_set, set_id_set, prop, bc, pcA)
