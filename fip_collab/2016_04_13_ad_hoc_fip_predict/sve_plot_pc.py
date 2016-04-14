import numpy as np
import matplotlib.pyplot as plt
import h5py
import sys


def pltPC(el, set_id, pcA):

    plt.figure(num=2, figsize=[14, 12])

    # colormat = np.random.rand(len(set_id_set), 3)
    colormat = np.array([[.3, .3, 1.],
                         [.3, 1., .3],
                         [1., .2, .2],
                         [0., .7, .7],
                         [.7, .0, .7],
                         [.7, .7, .0]])

    f = h5py.File("spatial.hdf5", 'r')

    reduced = f.get('reduced_%s' % set_id)[...]

    plt.plot(reduced[:, pcA].real, reduced[:, pcA].imag,
             marker='o', markersize=7, color=colormat[0, :],
             linestyle='', label=set_id)

    plt.plot(reduced[:, pcA].mean().real, reduced[:, pcA].mean().imag,
             marker='D', markersize=8, color=colormat[0, :],
             linestyle='')

    plt.title("neighbor sets for PC: %s" % str(pcA+1))
    plt.xlabel("real part")
    plt.ylabel("imaginary part")
    plt.legend(loc='upper right', shadow=True, fontsize='medium')

    f.close()

    plt.show()


if __name__ == '__main__':
    el = 21
    set_id_val = 'val'

    pcA = np.int64(sys.argv[1])

    pltPC(el, set_id_val, pcA)
