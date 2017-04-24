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
    colormat = cm.rainbow(clis)
    markermat = ['o', 'v', 'p',
                 's', '>', 'P',
                 '*', '<', 'X',
                 'D', 'd', '^']
    sizemat = [7, 7, 7,
               6, 7, 8,
               11, 7, 8,
               6, 7, 7]

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % H, 'r')

    """plot SVE sets for cal"""

    for ii in xrange(len(C['sid'])):

        sid = C['sid'][ii]

        reduced = f_red.get('reduced_%s' % sid)[...]
        meanA = reduced[:, pcA].mean()
        meanB = reduced[:, pcB].mean()

        plt.text(meanA, meanB+8, sid,
                 horizontalalignment='center',
                 verticalalignment='center',
                 fontsize=20,
                 weight='semibold',
                 color=[0.15, 0.15, 0.15],
                 alpha=0.99)

        # mfc = np.zeros((4,))
        # mfc[:3] = 0.999*colormat[ii, :3]
        # mfc[3] = 0.2  # marker face alpha

        # mec = np.zeros((4,))
        # mec[:3] = 0.7*colormat[ii, :3]
        # mec[3] = 0.8  # marker edge alpha

        mfc = np.zeros((4,))
        mfc[:3] = colormat[ii, :3] + .3*(1-colormat[ii, :3])
        mfc[3] = 1  # marker face alpha

        mec = np.zeros((4,))
        mec[:3] = 0.7*colormat[ii, :3]
        mec[3] = 1  # marker edge alpha

        plt.plot(reduced[:, pcA], reduced[:, pcB],
                 marker=markermat[ii], markersize=sizemat[ii],
                 mfc=mfc, mec=mec,
                 linestyle='', label=sid)

        # plt.plot(reduced[:, pcA], reduced[:, pcB],
        #          marker='o', markersize=6, color=colormat[ii, :],
        #          alpha=0.2, linestyle='')
        # plt.plot(meanA, meanB,
        #          marker='D', markersize=8, color=colormat[ii, :],
        #          linestyle='')

        # varmat = np.var(reduced, axis=0)
        # msg = "total variance for %s: %s" % (sid, varmat.sum())
        # rr.WP(msg, C['wrt_file'])

    plt.margins(.1)

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
