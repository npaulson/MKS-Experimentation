import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
from constants import const
import h5py
import sys


def pltmap(H, pcA, pcB, pcC):

    C = const()

    fig = plt.figure(figsize=[9, 5.5])
    ax = fig.add_subplot(111, projection='3d')

    n_col = len(C['sid_cal_split'] + C['sid_val_split'])
    colormat = cm.rainbow(np.linspace(0, 1, n_col))
    gray = [.7, .7, .7]

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'r')

    """plot SVE sets for cal"""

    c = 0

    for ii in xrange(len(C['sid_cal_split'])):

        sid = C['sid_cal_split'][ii]

        reduced = f_red.get('reduced_%s' % sid)[...]

        ax.scatter(reduced[:, pcA], reduced[:, pcB], reduced[:, pcC],
                   c=colormat[c, :], marker='o', s=40, alpha=.4,
                   label="%s (calibration)" % C['names_cal_split'][ii])

        # varmat = np.var(reduced, axis=0)
        # msg = "total variance for %s: %s" % (sid, varmat.sum())
        # rr.WP(msg, C['wrt_file'])

        c += 1

    """plot SVE sets for val"""

    for ii in xrange(len(C['sid_val_split'])):

        sid = C['sid_val_split'][ii]

        reduced = f_red.get('reduced_%s' % sid)[...]

        ax.scatter(reduced[:, pcA], reduced[:, pcB], reduced[:, pcC],
                   c=colormat[c, :], marker='^', s=40, alpha=.4,
                   label="%s (validation)" % C['names_val_split'][ii])

        # meanA = reduced[:, pcA].mean()
        # meanB = reduced[:, pcB].mean()
        # meanC = reduced[:, pcC].mean()

        # ax.text(meanA, meanB, meanC+8, C['names_val'][ii],
        #         horizontalalignment='center',
        #         verticalalignment='center')

        # varmat = np.var(reduced, axis=0)
        # msg = "total variance for %s: %s" % (sid, varmat.sum())
        # rr.WP(msg, C['wrt_file'])

        c += 1

    plt.margins(.1)

    ax.set_xlabel("PC%s" % str(pcA+1))
    ax.set_ylabel("PC%s" % str(pcB+1))
    ax.set_zlabel("PC%s" % str(pcC+1))

    plt.grid(True)

    plt.legend(bbox_to_anchor=(1.02, 1), loc=2, shadow=True, fontsize='medium')

    fig.tight_layout(rect=(0, 0, .7, 1))

    f_red.close()

    fig_name = 'pc%s_pc%s_pc%s_L%s.png' % (pcA+1, pcB+1, pcC+1, H)
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':
    H = np.int64(sys.argv[1])
    pcA = np.int64(sys.argv[2])
    pcB = np.int64(sys.argv[3])
    pcC = np.int64(sys.argv[4])
    pltmap(H, pcA, pcB, pcC)
    plt.show()
