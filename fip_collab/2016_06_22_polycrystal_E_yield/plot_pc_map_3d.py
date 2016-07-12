import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from constants import const
import functions as rr
import h5py
import sys


def pltmap(H, pcA, pcB, pcC):

    C = const()

    fig = plt.figure(figsize=[9, 5])
    ax = fig.add_subplot(111, projection='3d')

    colormat = np.array([[.3, .3, 1.],
                         [.3, 1., .3],
                         [1., .2, .2],
                         [0., .7, .7],
                         [.7, .0, .7],
                         [.7, .7, .0],
                         [.5, .3, .1],
                         [.3, .5, .1],
                         [.1, .3, .5]])

    # colormat = np.array([[0, 0, 1.],
    #                      [0, 1, 0],
    #                      [1., 0, 0],
    #                      [0., 1, 1],
    #                      [1, .0, 1],
    #                      [1, 1, .0],
    #                      [1, .5, .3],
    #                      [.5, 1, .3],
    #                      [.3, .5, 1]])

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % H, 'r')

    """plot SVE sets for cal"""

    for ii in xrange(len(C['set_id_cal'])):

        set_id = C['set_id_cal'][ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]

        ax.scatter(reduced[:, pcA], reduced[:, pcB], reduced[:, pcC],
                   c=colormat[ii, :], marker='o', s=40, alpha=.4,
                   label="%s (calibration)" % C['names_cal'][ii])

        varmat = np.var(reduced, axis=0)

        msg = "total variance for %s: %s" % (set_id, varmat.sum())
        rr.WP(msg, C['wrt_file'])

    """plot SVE sets for val"""

    for ii in xrange(len(C['set_id_val'])):

        set_id = C['set_id_val'][ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]

        ax.scatter(reduced[:, pcA], reduced[:, pcB], reduced[:, pcC],
                   c=colormat[ii, :], marker='^', s=40, alpha=.4,
                   label="%s (validation)" % C['names_val'][ii])

        varmat = np.var(reduced, axis=0)

        msg = "total variance for %s: %s" % (set_id, varmat.sum())
        rr.WP(msg, C['wrt_file'])

    # """plot centers of SVE sets for cal"""

    # for ii in xrange(len(C['set_id_cal'])):

    #     set_id = C['set_id_cal'][ii]

    #     reduced = f_red.get('reduced_%s' % set_id)[...]

    #     ax.scatter(reduced[:, pcA], reduced[:, pcB], reduced[:, pcC],
    #                c=colormat[ii, :], marker='o', s=20)

    #     # plt.plot(reduced[:, pcA].mean(), reduced[:, pcB].mean(), alpha=0.99,
    #     #          marker='s', markersize=8, color=colormat[ii, :],
    #     #          linestyle='')

    # """plot centers of SVE sets for val"""

    # for ii in xrange(len(C['set_id_val'])):

    #     set_id = C['set_id_val'][ii]

    #     reduced = f_red.get('reduced_%s' % set_id)[...]

    #     ax.scatter(reduced[:, pcA], reduced[:, pcB], reduced[:, pcC],
    #                c=colormat[ii, :], marker='s', s=20)

    #     # plt.plot(reduced[:, pcA].mean(), reduced[:, pcB].mean(), alpha=0.99,
    #     #          marker='o', markersize=8, color=colormat[ii, :],
    #     #          linestyle='')

    plt.margins(.1)

    ax.set_xlabel("PC%s" % str(pcA+1))
    ax.set_ylabel("PC%s" % str(pcB+1))
    ax.set_zlabel("PC%s" % str(pcC+1))

    plt.grid(True)

    plt.legend(bbox_to_anchor=(1.02, 1), loc=2, shadow=True, fontsize='medium')

    fig.tight_layout(rect=(0, 0, .6, 1))

    f_red.close()

    fig_name = 'pc%s_pc%s_pc%s_L%s.png' % (pcA+1, pcB+1, pcC+1, H)
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':

    C = const()

    H = C['H']

    pcA = np.int64(sys.argv[1])
    pcB = np.int64(sys.argv[2])

    pltmap(H, pcA, pcB)

    plt.show()
