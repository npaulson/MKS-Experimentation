import numpy as np
import matplotlib.pyplot as plt
import h5py
import sys


def pltPC(el, ns_set, set_id_set, pcA, pcB):

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

    f_red = h5py.File("sve_reduced.hdf5", 'r')

    for ii in xrange(len(set_id_set)):

        reduced = f_red.get('reduced_%s' % set_id_set[ii])[...]

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

    f_red.close()

    plt.show()


if __name__ == '__main__':
    el = 21
    ns_cal = [20, 20, 20, 20]
    set_id_cal = ['randomD3D_cal', 'transverseD3D_cal',
                  'basaltransD3D_cal', 'actualD3D_cal']

    pcA = np.int64(sys.argv[1])
    pcB = 1

    pltPC(el, ns_cal, set_id_cal, pcA, pcB)
