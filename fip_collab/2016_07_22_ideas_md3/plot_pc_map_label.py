import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
import h5py
import sys


def pltmap(C, H, pcA, pcB):

    fig = plt.figure(figsize=[7.5, 5])

    """define the colors of interest"""
    n_col = len(C['set_id_val'])-len(C['set_id_cal'])
    colormat = cm.rainbow(np.linspace(0, 1, n_col))
    gray = [.7, .7, .7]

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % H, 'r')

    """plot SVE sets for cal"""

    for ii in xrange(len(C['set_id_cal'])):

        set_id = C['set_id_cal'][ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]
        meanA = reduced[:, pcA].mean()
        meanB = reduced[:, pcB].mean()

        plt.plot(reduced[:, pcA], reduced[:, pcB],
                 marker='s', markersize=6, color=gray,
                 alpha=0.4, linestyle='')
        plt.plot(meanA, meanB,
                 marker='s', markersize=8, color=gray,
                 linestyle='')

        # varmat = np.var(reduced, axis=0)
        # msg = "total variance for %s: %s" % (set_id, varmat.sum())
        # rr.WP(msg, C['wrt_file'])

    """plot SVE sets for val"""

    c = 0

    for ii in xrange(len(C['set_id_val'])):

        set_id = C['set_id_val'][ii]
        name = C['names_val'][ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]
        meanA = reduced[:, pcA].mean()
        meanB = reduced[:, pcB].mean()

        plt.text(meanA, meanB+4, C['names_val'][ii],
                 horizontalalignment='center',
                 verticalalignment='center')

        # plt.text(txtm[ii, 0], txtm[ii, 1], C['names_val'][ii],
        #          horizontalalignment='center',
        #          verticalalignment='center')

        if np.any(np.array(C['names_cal']) == name):
            plt.plot(reduced[:, pcA], reduced[:, pcB],
                     marker='o', markersize=6, color=gray,
                     alpha=0.4, linestyle='')
            plt.plot(meanA, meanB,
                     marker='o', markersize=8, color=gray,
                     linestyle='')
        else:
            plt.plot(reduced[:, pcA], reduced[:, pcB],
                     marker='o', markersize=6, color=colormat[c, :],
                     alpha=0.4, linestyle='')
            plt.plot(meanA, meanB,
                     marker='o', markersize=8, color=colormat[c, :],
                     linestyle='')
            c += 1

        # varmat = np.var(reduced, axis=0)
        # msg = "total variance for %s: %s" % (set_id, varmat.sum())
        # rr.WP(msg, C['wrt_file'])

    plt.margins(.2)

    plt.xlabel("PC%s" % str(pcA+1))
    plt.ylabel("PC%s" % str(pcB+1))

    plt.grid(linestyle='-', alpha=0.15)

    """create a legend based on points not plotted"""
    p1 = plt.plot(0, 0, marker='s', markersize=6,
                  color=gray, linestyle='', label='calibration')
    p2 = plt.plot(0, 0, marker='o', markersize=6,
                  color=gray, linestyle='', label='validation')
    plt.legend(shadow=True, fontsize='medium', ncol=2)
    p1[0].remove()
    p2[0].remove()

    fig.tight_layout()

    # plt.legend(bbox_to_anchor=(1.02, 1), loc=2, shadow=True, fontsize='medium')
    # fig.tight_layout(rect=(0, 0, .7, 1))

    f_red.close()


if __name__ == '__main__':

    C = const()

    H = np.int64(sys.argv[1])
    pcA = np.int64(sys.argv[2])
    pcB = np.int64(sys.argv[3])

    pltmap(C, H, pcA, pcB)

    plt.show()
