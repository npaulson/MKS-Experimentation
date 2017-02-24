import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
from constants import const
import h5py
import sys


def pltcount(H, pcA, pcB):

    C = const()

    fig = plt.figure(figsize=[7.5, 5])
    ax = fig.add_subplot(111)

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % H, 'r')
    f_ev = h5py.File("responses.hdf5", 'r')

    """find max number of extreme fips per SVE"""
    max_count = 0
    for ii in xrange(len(C['sid'])):
        sid = C['sid'][ii]
        ev_count = f_ev.get("ev_count_%s" % sid)[...]
        tmp = np.max(ev_count)

        if tmp > max_count:
            max_count = tmp

    print "max ev count per SVE: %s" % max_count

    """plot ev counts per SVE in all micr classes"""
    for ii in xrange(len(C['sid'])):

        sid = C['sid'][ii]

        ev_count = f_ev.get("ev_count_%s" % sid)[...]
        reduced = f_red.get('reduced_%s' % sid)[...]
        meanA = reduced[:, pcA].mean()
        meanB = reduced[:, pcB].mean()

        plt.text(meanA, meanB+7, C['sid'][ii],
                 horizontalalignment='center',
                 verticalalignment='center')

        # cm_ = plt.cm.get_cmap('viridis')
        cm_ = plt.cm.get_cmap('plasma')

        # sc = plt.scatter(reduced[:, pcA], reduced[:, pcB],
        #                  c=ev_count+1), cmap=cm_,
        #                  vmin=0, vmax=max_count),
        #                  alpha=0.7,
        #                  s=25, lw=0)

        sc = ax.scatter(reduced[:, pcA], reduced[:, pcB],
                        c=ev_count+1, cmap=cm_,
                        norm=colors.LogNorm(vmin=1, vmax=max_count+1),
                        s=10, lw=0)

    plt.colorbar(sc)

    plt.margins(.05)

    plt.xlabel("PC%s" % str(pcA+1))
    plt.ylabel("PC%s" % str(pcB+1))

    plt.grid(linestyle='-', alpha=0.15)

    gr = 0.3
    ax.patch.set_facecolor([gr, gr, gr])

    fig.tight_layout()

    f_red.close()

    fig_name = 'pc%s_pc%s_count_L%s.png' % (pcA+1, pcB+1, H)
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':
    H = np.int64(sys.argv[1])
    pcA = np.int64(sys.argv[2])
    pcB = np.int64(sys.argv[3])

    pltcount(H, pcA, pcB)

    plt.show()
