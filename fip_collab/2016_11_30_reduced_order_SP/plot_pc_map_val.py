import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
import h5py
import sys


def pltmap(H, pcA, pcB):

    C = const()

    fig = plt.figure(figsize=[7.5, 5])

    colormat = cm.rainbow(np.linspace(0, 1, 5))
    # colormat = cm.Set1(np.linspace(0, 1, len(C['set_id_val'])))
    gray = [.7, .7, .7]

    # txtm is for pc1 vs pc2
    txtm = np.array([[-45, -8], [-30, -25], [7, 38],
                     [-50, 18], [53, 5], [20, 27],
                     [63, -23], [-10, 10], [10, -30],
                     [13, -10], [45, -25], [58, -11]])

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % H, 'r')

    """plot SVE sets for val"""

    for ii in xrange(len(C['set_id_val'])):

        set_id = C['set_id_val'][ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]
        meanA = reduced[:, pcA].mean()
        meanB = reduced[:, pcB].mean()

        # plt.text(meanA, meanB+8, C['names_val'][ii],
        #          horizontalalignment='center',
        #          verticalalignment='center')

        plt.text(txtm[ii, 0], txtm[ii, 1], C['names_plt_val'][ii],
                 horizontalalignment='center',
                 verticalalignment='center',
                 fontsize='large')

        if ii == 0:
            plt.plot(reduced[:, pcA], reduced[:, pcB],
                     marker='o', markersize=8, color=gray,
                     alpha=0.4, linestyle='')
            plt.plot(meanA, meanB,
                     marker='o', markersize=10, color=gray,
                     linestyle='')
        elif ii <= 6:
            plt.plot(reduced[:, pcA], reduced[:, pcB],
                     marker='o', markersize=8, color=gray,
                     alpha=0.4, linestyle='')
            plt.plot(meanA, meanB,
                     marker='o', markersize=10, color=gray,
                     linestyle='')
        else:
            plt.plot(reduced[:, pcA], reduced[:, pcB],
                     marker='o', markersize=8, color=colormat[ii-7, :],
                     alpha=0.4, linestyle='')
            plt.plot(meanA, meanB,
                     marker='o', markersize=10, color=colormat[ii-7, :],
                     linestyle='')

    for ii in xrange(len(C['set_id_val'])):

        set_id = C['set_id_val'][ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]
        meanA = reduced[:, pcA].mean()
        meanB = reduced[:, pcB].mean()

        if ii == 0:
            plt.plot(meanA, meanB,
                     marker='o', markersize=10, color=gray,
                     linestyle='')
        elif ii <= 6:
            plt.plot(meanA, meanB,
                     marker='o', markersize=10, color=gray,
                     linestyle='')
        else:
            plt.plot(meanA, meanB,
                     marker='o', markersize=10, color=colormat[ii-7, :],
                     linestyle='')

    plt.margins(.1)

    plt.xlabel("PC%s" % str(pcA+1), fontsize='large')
    plt.ylabel("PC%s" % str(pcB+1), fontsize='large')
    plt.xticks(fontsize='large')
    plt.yticks(fontsize='large')

    plt.grid(linestyle='-', alpha=0.15)
    fig.tight_layout()

    f_red.close()

    fig_name = 'pc%s_pc%s_val_L%s.png' % (pcA+1, pcB+1, H)
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':

    C = const()

    H = np.int64(sys.argv[1])
    pcA = np.int64(sys.argv[2])
    pcB = np.int64(sys.argv[3])

    pltmap(H, pcA, pcB)

    plt.show()
