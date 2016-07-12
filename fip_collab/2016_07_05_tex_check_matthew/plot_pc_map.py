import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
import functions as rr
import h5py
import sys


def pltmap(H, pcA, pcB):

    C = const()

    fig = plt.figure(figsize=[9, 5])

    # colormat = np.array([[.3, .3, 1.],
    #                      [.3, 1., .3],
    #                      [1., .2, .2],
    #                      [0., .7, .7],
    #                      [.7, .0, .7],
    #                      [.7, .7, .0],
    #                      [.5, .3, .1],
    #                      [.3, .5, .1],
    #                      [.1, .3, .5]])

    # colormat = cm.rainbow(np.linspace(0, 1, len(C['set_id_val'])))
    colormat = cm.Set1(np.linspace(0, 1, len(C['set_id_cal'])+1))
    markervec = ['s', '^', 'D', '8', 'p']

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % H, 'r')

    """plot SVE sets for cal"""

    for ii in xrange(len(C['set_id_cal'])):

        set_id = C['set_id_cal'][ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]

        plt.plot(reduced[:, pcA], reduced[:, pcB],
                 marker='o', markersize=6, color=colormat[ii, :], alpha=0.5,
                 linestyle='', label="%s (calibration)" % C['names_cal'][ii])

        varmat = np.var(reduced, axis=0)

        msg = "total variance for %s: %s" % (set_id, varmat.sum())
        rr.WP(msg, C['wrt_file'])
        # msg = "variance for %s in PC%s: %s" % (set_id, str(pcA+1), varmat[0])
        # rr.WP(msg, C['wrt_file'])
        # msg = "variance for %s in PC%s: %s" % (set_id, str(pcB+1), varmat[1])
        # rr.WP(msg, C['wrt_file'])

    """plot SVE sets for val"""

    for ii in xrange(len(C['set_id_val'])):

        set_id = C['set_id_val'][ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]

        plt.plot(reduced[:, pcA], reduced[:, pcB],
                 marker=markervec[ii], markersize=6, color=colormat[-1, :], alpha=0.5,
                 linestyle='', label="%s (validation)" % C['names_val'][ii])

        varmat = np.var(reduced, axis=0)

        msg = "total variance for %s: %s" % (set_id, varmat.sum())
        rr.WP(msg, C['wrt_file'])
        # msg = "variance for %s in PC%s: %s" % (set_id, str(pcA+1), varmat[0])
        # rr.WP(msg, C['wrt_file'])
        # msg = "variance for %s in PC%s: %s" % (set_id, str(pcB+1), varmat[1])
        # rr.WP(msg, C['wrt_file'])

    plt.margins(.1)

    plt.xlabel("PC%s" % str(pcA+1))
    plt.ylabel("PC%s" % str(pcB+1))

    plt.grid(True)

    plt.legend(bbox_to_anchor=(1.02, 1), loc=2, shadow=True, fontsize='medium')

    fig.tight_layout(rect=(0, 0, .6, 1))

    f_red.close()

    fig_name = 'pc%s_pc%s_L%s.png' % (pcA+1, pcB+1, H)
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':

    C = const()

    H = C['H']

    pcA = np.int64(sys.argv[1])
    pcB = np.int64(sys.argv[2])

    pltmap(H, pcA, pcB)

    plt.show()
