import numpy as np
import matplotlib.pyplot as plt
import h5py


def pltPC(el, ns_set, set_id_set, pcA, pcB):

    plt.figure(num=2, figsize=[10, 7])

    # colormat = np.random.rand(len(set_id_set), 3)
    colormat = np.array([[.3, .3, 1.],
                         [.3, 1., .3],
                         [1., .2, .2],
                         [0., .7, .7],
                         [.7, .0, .7],
                         [.7, .7, .0]])

    f_red = h5py.File("sve_reduced.hdf5", 'r')

    for ii in xrange(len(set_id_set)):

        reduced = f_red.get('reduced_%s' % set_id_set[ii])[...]

        plt.plot(reduced[:, pcA], reduced[:, pcB],
                 marker='o', markersize=7, color=colormat[ii, :],
                 linestyle='', label=set_id_set[ii])

        plt.plot(reduced[:, pcA].mean(), reduced[:, pcB].mean(),
                 marker='D', markersize=8, color=colormat[ii, :],
                 linestyle='')

    f_red.close()

    plt.title("SVE sets in PC space")
    plt.xlabel("PC%s" % pcA)
    plt.ylabel("PC%s" % pcB)
    plt.legend(loc='upper right', shadow=True, fontsize='medium')

    plt.show()


if __name__ == '__main__':
    el = 21
    ns_cal = [10, 10, 10, 10, 40, 60]
    set_id_cal = ['incl1', 'rod1', 'rod2', 'rod3', 'bicrystal_orthog', 'improcess']
    step = 0
    pcA = 5
    pcB = 7

    pltPC(el, ns_cal, set_id_cal, step, pcA, pcB)
