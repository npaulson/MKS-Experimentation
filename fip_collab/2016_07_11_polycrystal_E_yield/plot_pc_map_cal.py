import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
import h5py
import sys


def pltmap(H, pcA, pcB):

    C = const()

    fig = plt.figure(figsize=[7.5, 5])

    colormat = cm.rainbow(np.linspace(0, 1, len(C['set_id_cal'])))
    # colormat = cm.rainbow(np.linspace(0, 1, len(C['set_id_val'])))

    # txtm is for pc1 vs pc2
    txtm = np.array([[-45, -8], [-30, -25], [7, 38],
                     [-50, 18], [53, 5], [20, 27],
                     [63, -23]])

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % H, 'r')

    for ii in xrange(len(C['set_id_cal'])):

        set_id = C['set_id_cal'][ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]
        meanA = reduced[:, pcA].mean()
        meanB = reduced[:, pcB].mean()

        plt.plot(reduced[:, pcA], reduced[:, pcB],
                 marker='s', markersize=6, color=colormat[ii, :],
                 alpha=0.4, linestyle='')

        plt.text(txtm[ii, 0], txtm[ii, 1], C['names_plt_cal'][ii],
                 horizontalalignment='center',
                 verticalalignment='center')

    for ii in xrange(len(C['set_id_cal'])):

        set_id = C['set_id_cal'][ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]
        meanA = reduced[:, pcA].mean()
        meanB = reduced[:, pcB].mean()

        plt.plot(meanA, meanB,
                 marker='s', markersize=8, color=colormat[ii, :],
                 linestyle='')

    plt.margins(.1)

    plt.xlabel("PC%s" % str(pcA+1))
    plt.ylabel("PC%s" % str(pcB+1))

    plt.grid(linestyle='-', alpha=0.15)

    fig.tight_layout()

    f_red.close()

    fig_name = 'pc%s_pc%s_cal_L%s.png' % (pcA+1, pcB+1, H)
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':

    C = const()

    H = np.int64(sys.argv[1])
    pcA = np.int64(sys.argv[2])
    pcB = np.int64(sys.argv[3])

    pltmap(H, pcA, pcB)

    plt.show()
