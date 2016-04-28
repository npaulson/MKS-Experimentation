import numpy as np
import matplotlib.pyplot as plt
import sys
import h5py


def pltresponse(ns_set, set_id_set, resptyp, pcA):

    plt.figure(num=4, figsize=[10, 7])

    # colormat = np.random.rand(len(set_id_set), 3)
    colormat = np.array([[.3, .3, 1.],
                         [.3, 1., .3],
                         [1., .2, .2],
                         [0., .7, .7],
                         [.7, .0, .7],
                         [.7, .7, .0]])

    f_red = h5py.File("sve_reduced.hdf5", 'r')
    f_link = h5py.File("responses_for_linkage.hdf5", 'r')

    for ii in xrange(len(set_id_set)):

        reduced = f_red.get('reduced_%s' % set_id_set[ii])[...]
        response = f_link.get('%s_%s' % (resptyp, set_id_set[ii]))[...]

        plt.plot(reduced[:, pcA], response,
                 marker='D', markersize=8, color=colormat[ii, :],
                 linestyle='', label=set_id_set[ii])

        plt.title("%s verus principal components" % resptyp)
        plt.xlabel("PC %s" % str(pcA+1))
        plt.ylabel(resptyp)
        plt.legend(loc='upper right', shadow=True, fontsize='medium')

    f_red.close()
    f_link.close()

    plt.show()


if __name__ == '__main__':
    ns_cal = [20, 20, 20, 20]
    set_id_cal = ['randomD3D_cal', 'transverseD3D_cal',
                  'basaltransD3D_cal', 'actualD3D_cal']
    # ns_cal = [20]
    # set_id_cal = ['randomD3D_cal']

    resptyp = 'Eeff'
    pcA = np.int64(sys.argv[1])

    pltresponse(ns_cal, set_id_cal, resptyp, pcA)
