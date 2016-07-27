import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
from constants import const
import h5py
import sys


def pltmap(C, H, pcA, pcB, pcC):

    fig = plt.figure(figsize=[9, 5.5])
    ax = fig.add_subplot(111, projection='3d')

    # colormat = cm.rainbow(np.linspace(0, 1, len(C['set_id_val'])))
    colormat = cm.Set1(np.linspace(0, 1, len(C['set_id_val'])))

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'r')

    """plot SVE sets for cal"""

    for ii in xrange(len(C['set_id_cal'])):

        set_id = C['set_id_cal'][ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]

        ax.scatter(reduced[:, pcA], reduced[:, pcB], reduced[:, pcC],
                   c=colormat[ii, :], marker='o', s=40, alpha=.4,
                   label="%s (calibration)" % C['names_cal'][ii])

        # varmat = np.var(reduced, axis=0)
        # msg = "total variance for %s: %s" % (set_id, varmat.sum())
        # rr.WP(msg, C['wrt_file'])

    """plot SVE sets for val"""

    for ii in xrange(len(C['set_id_val'])):

        set_id = C['set_id_val'][ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]

        ax.scatter(reduced[:, pcA], reduced[:, pcB], reduced[:, pcC],
                   c=colormat[ii, :], marker='^', s=40, alpha=.4,
                   label="%s (validation)" % C['names_val'][ii])

        # meanA = reduced[:, pcA].mean()
        # meanB = reduced[:, pcB].mean()
        # meanC = reduced[:, pcC].mean()

        # ax.text(meanA, meanB, meanC+8, C['names_val'][ii],
        #         horizontalalignment='center',
        #         verticalalignment='center')

        # varmat = np.var(reduced, axis=0)
        # msg = "total variance for %s: %s" % (set_id, varmat.sum())
        # rr.WP(msg, C['wrt_file'])

    plt.margins(.1)

    ax.set_xlabel("PC%s" % str(pcA+1))
    ax.set_ylabel("PC%s" % str(pcB+1))
    ax.set_zlabel("PC%s" % str(pcC+1))

    plt.grid(True)

    plt.legend(bbox_to_anchor=(1.02, 1), loc=2, shadow=True, fontsize='medium')

    fig.tight_layout(rect=(0, 0, .7, 1))

    f_red.close()


if __name__ == '__main__':

    C = const()

    H = np.int64(sys.argv[1])
    pcA = np.int64(sys.argv[2])
    pcB = np.int64(sys.argv[3])
    pcC = np.int64(sys.argv[4])
    pltmap(C, H, pcA, pcB, pcC)
    plt.show()
