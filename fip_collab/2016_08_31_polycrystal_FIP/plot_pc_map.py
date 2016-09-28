import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
import h5py
import sys


def pltmap(H, pcA, pcB):

    C = const()

    fig = plt.figure(figsize=[7.5, 5])

    """define the colors of interest"""
    n_col = len(C['sid_cal_split'] + C['sid_val_split'])
    colormat = cm.rainbow(np.linspace(0, 1, n_col))
    gray = [.7, .7, .7]

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % H, 'r')

    """plot SVE sets for cal"""

    c = 0

    for ii in xrange(len(C['sid_cal_split'])):

        sid = C['sid_cal_split'][ii]

        reduced = f_red.get('reduced_%s' % sid)[...]
        meanA = reduced[:, pcA].mean()
        meanB = reduced[:, pcB].mean()

        plt.text(meanA, meanB+4, C['names_cal_split'][ii],
                 horizontalalignment='center',
                 verticalalignment='center')

        plt.plot(reduced[:, pcA], reduced[:, pcB],
                 marker='s', markersize=6, color=colormat[c, :],
                 alpha=0.4, linestyle='')
        plt.plot(meanA, meanB,
                 marker='s', markersize=8, color=colormat[c, :],
                 linestyle='')

        # varmat = np.var(reduced, axis=0)
        # msg = "total variance for %s: %s" % (sid, varmat.sum())
        # rr.WP(msg, C['wrt_file'])

        c += 1

    """plot SVE sets for val"""

    for ii in xrange(len(C['sid_val_split'])):

        sid = C['sid_val_split'][ii]

        reduced = f_red.get('reduced_%s' % sid)[...]
        meanA = reduced[:, pcA].mean()
        meanB = reduced[:, pcB].mean()

        plt.text(meanA, meanB+4, C['names_val_split'][ii],
                 horizontalalignment='center',
                 verticalalignment='center')

        # plt.text(txtm[ii, 0], txtm[ii, 1], C['names_val'][ii],
        #          horizontalalignment='center',
        #          verticalalignment='center')

        plt.plot(reduced[:, pcA], reduced[:, pcB],
                 marker='o', markersize=6, color=colormat[c, :],
                 alpha=0.4, linestyle='')
        plt.plot(meanA, meanB,
                 marker='o', markersize=8, color=colormat[c, :],
                 linestyle='')

        # varmat = np.var(reduced, axis=0)
        # msg = "total variance for %s: %s" % (sid, varmat.sum())
        # rr.WP(msg, C['wrt_file'])

        c += 1

    plt.margins(.2)

    plt.xlabel("PC%s" % str(pcA+1))
    plt.ylabel("PC%s" % str(pcB+1))

    plt.grid(linestyle='-', alpha=0.15)

    """create a legend based on points not plotted"""
    p1 = plt.plot(0, 0, marker='s', markersize=6,
                  color=gray, linestyle='', label='calibration')
    p2 = plt.plot(0, 0, marker='o', markersize=6,
                  color=gray, linestyle='', label='validation')
    plt.legend(loc='upper left', shadow=True, fontsize='medium', ncol=2)
    p1[0].remove()
    p2[0].remove()

    fig.tight_layout()

    # plt.legend(bbox_to_anchor=(1.02, 1), loc=2, shadow=True, fontsize='medium')
    # fig.tight_layout(rect=(0, 0, .7, 1))

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
