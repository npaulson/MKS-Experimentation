import numpy as np
import matplotlib.pyplot as plt
import h5py


def plt_stiffness(el, ns_set, set_id_set, step, pcA):

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
        Eeff = f_link.get('Eeff_%s' % set_id_set[ii])[...]

        plt.plot(reduced[:, pcA], Eeff,
                 marker='D', markersize=8, color=colormat[ii, :],
                 linestyle='', label=set_id_set[ii])

        plt.title("Effective stiffness verus principal components")
        plt.xlabel("PC %s" % str(pcA+1))
        plt.ylabel("Effective Stiffness")
        plt.legend(loc='upper right', shadow=True, fontsize='medium')

    f_red.close()
    f_link.close()

    plt.show()


if __name__ == '__main__':
    el = 21
    ns_cal = [10, 10, 10]
    set_id_cal = ['randomD3D', 'transverseD3D', 'basaltransD3D']
    step = 0
    pcA = 0

    plt_stiffness(el, ns_cal, set_id_cal, step, pcA)
