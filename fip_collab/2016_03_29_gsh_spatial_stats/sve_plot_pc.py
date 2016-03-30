import numpy as np
import matplotlib.pyplot as plt
import h5py


def pltPC(el, ns_set, set_id_set, step, pcA, pcB):

    plt.figure(num=2, figsize=[14, 12])

    # colormat = np.random.rand(len(set_id_set), 3)
    colormat = np.array([[.3, .3, 1.],
                         [.3, 1., .3],
                         [1., .2, .2],
                         [0., .7, .7],
                         [.7, .0, .7],
                         [.7, .7, .0]])

    for ii in xrange(len(set_id_set)):

        f_temp = h5py.File("ref_%s%s_s%s.hdf5" %
                           (ns_set[ii], set_id_set[ii], step), 'a')

        pc_corr = f_temp.get('pc_corr')[...]

        f_temp.close()

        # plt.plot(pc_corr[:, pcA], pc_corr[:, pcB],
        #          marker='o', markersize=7, color=colormat[ii, :],
        #          linestyle='', label=set_id_set[ii])

        # plt.plot(pc_corr[:, pcA].mean(), pc_corr[:, pcB].mean(),
        #          marker='D', markersize=8, color=colormat[ii, :],
        #          linestyle='')

        plt.subplot(211)

        plt.plot(pc_corr[:, pcA].real, pc_corr[:, pcB].real,
                 marker='o', markersize=7, color=colormat[ii, :],
                 linestyle='', label=set_id_set[ii])

        plt.plot(pc_corr[:, pcA].real.mean(), pc_corr[:, pcB].real.mean(),
                 marker='D', markersize=8, color=colormat[ii, :],
                 linestyle='')

        plt.title("SVE sets in PC space (real)")
        plt.xlabel("PC%s" % pcA)
        plt.ylabel("PC%s" % pcB)
        plt.legend(loc='upper right', shadow=True, fontsize='medium')

        plt.subplot(212)

        plt.plot(pc_corr[:, pcA].imag, pc_corr[:, pcB].imag,
                 marker='o', markersize=7, color=colormat[ii, :],
                 linestyle='', label=set_id_set[ii])

        plt.plot(pc_corr[:, pcA].imag.mean(), pc_corr[:, pcB].imag.mean(),
                 marker='D', markersize=8, color=colormat[ii, :],
                 linestyle='')

        plt.title("SVE sets in PC space (imaginary)")
        plt.xlabel("PC%s" % pcA)
        plt.ylabel("PC%s" % pcB)
        plt.legend(loc='upper right', shadow=True, fontsize='medium')

    plt.show()


if __name__ == '__main__':
    el = 21
    ns_cal = [10, 10, 10]
    set_id_cal = ['randomD3D', 'transverseD3D', 'basaltransD3D']
    step = 0
    pcA = 0
    pcB = 1

    pltPC(el, ns_cal, set_id_cal, step, pcA, pcB)
