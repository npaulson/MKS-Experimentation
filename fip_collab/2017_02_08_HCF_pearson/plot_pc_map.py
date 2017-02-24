import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
import h5py
import sys


def pltmap(H, pcA, pcB):

    C = const()

    fig = plt.figure(figsize=[7.5, 5])
    ax = fig.add_subplot(111)

    """define the colors of interest"""
    n_col = len(C['sid'])
    clis = np.linspace(0, 1, n_col)
    np.random.seed(0)
    np.random.shuffle(clis)
    colormat = cm.rainbow(clis)

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % H, 'r')

    """plot SVE sets for cal"""

    for ii in xrange(len(C['sid'])):

        sid = C['sid'][ii]
        name = C['names_plt'][ii]

        reduced = f_red.get('reduced_%s' % sid)[...]
        meanA = reduced[:, pcA].mean()
        meanB = reduced[:, pcB].mean()

        plt.text(meanA, meanB+5, name,
                 horizontalalignment='center',
                 verticalalignment='center',
                 fontsize=20,
                 color=[0.15, 0.15, 0.15],
                 alpha=0.99)

        plt.plot(reduced[:, pcA], reduced[:, pcB],
                 marker='o', markersize=6, color=colormat[ii, :],
                 alpha=0.2, linestyle='')
        plt.plot(meanA, meanB,
                 marker='D', markersize=8, color=colormat[ii, :],
                 linestyle='')

        # varmat = np.var(reduced, axis=0)
        # msg = "total variance for %s: %s" % (sid, varmat.sum())
        # rr.WP(msg, C['wrt_file'])

    plt.margins(.2)

    # plt.xlabel("PC%s" % str(pcA+1))
    # plt.ylabel("PC%s" % str(pcB+1))
    plt.xlabel("PC%s" % str(pcA+1), fontsize='large')
    plt.ylabel("PC%s" % str(pcB+1), fontsize='large')
    plt.xticks(fontsize='large')
    plt.yticks(fontsize='large')

    plt.grid(linestyle='-', alpha=0.15)

    gr = 1.00
    ax.patch.set_facecolor([gr, gr, gr])

    fig.tight_layout()

    f_red.close()

    fig_name = 'pc%s_pc%s_L%s.png' % (pcA+1, pcB+1, H)
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':
    H = np.int64(sys.argv[1])
    pcA = np.int64(sys.argv[2])
    pcB = np.int64(sys.argv[3])

    pltmap(H, pcA, pcB)

    plt.show()
