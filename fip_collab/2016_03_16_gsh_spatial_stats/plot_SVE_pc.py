import numpy as np
import matplotlib.pyplot as plt
import h5py


def pltPC(el, ns_set, set_id_set, step, pcA, pcB):

    plt.figure(num=2, figsize=[9, 2.7])

    style = ['ro', 'bv', 'gs', 'p+']

    for ii in xrange(len(set_id_set)):

        f_temp = h5py.File("D_%s%s_s%s.hdf5" %
                           (ns_set[ii], set_id_set[ii], step), 'a')

        pc_corr = f_temp.get('pc_corr')[...]

        f_temp.close()

        plt.plot(pc_corr[:, pcA].real, pc_corr[:, pcB].real, style[ii])

    plt.title("SVE sets in PC space")
    plt.xlabel("PC%s" % pcA)
    plt.xlabel("PC%s" % pcA)

    plt.show()


if __name__ == '__main__':
    el = 21
    ns_set = [10, 10, 10]
    set_id_set = ['random', 'transverse', 'basaltrans']
    step = 0
    pcA = 0
    pcB = 1

    pltPC(el, ns_set, set_id_set, step, pcA, pcB)
