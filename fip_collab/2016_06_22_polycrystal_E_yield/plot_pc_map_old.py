import numpy as np
import matplotlib.pyplot as plt
from constants import const
import functions as rr
import h5py
import sys


def pltmap(ns_set, names_set, set_id_set, typ, H, pcA, pcB):

    C = const()

    fig = plt.figure(figsize=[8, 5])

    colormat = np.array([[.3, .3, 1.],
                         [.3, 1., .3],
                         [1., .2, .2],
                         [0., .7, .7],
                         [.7, .0, .7],
                         [.7, .7, .0],
                         [.5, .3, .1],
                         [.3, .5, .1],
                         [.1, .3, .5]])

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % H, 'r')

    for ii in xrange(len(set_id_set)):

        set_id = set_id_set[ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]

        plt.plot(reduced[:, pcA], reduced[:, pcB],
                 marker='o', markersize=7, color=colormat[ii, :], alpha=0.5,
                 linestyle='', label=names_set[ii])

        plt.plot(reduced[:, pcA].mean(), reduced[:, pcB].mean(), alpha=0.99,
                 marker='o', markersize=9, color=colormat[ii, :],
                 linestyle='')

        # plt.plot(reduced[:, pcA].mean(), reduced[:, pcB].mean(), alpha=0.99,
        #          marker='D', markersize=8, color=colormat[ii, :],
        #          linestyle='')

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

    fig.tight_layout(rect=(0, 0, .75, 1))

    f_red.close()

    fig_name = 'pc%s_pc%s_%s_L%s.png' % (pcA+1, pcB+1, typ, H)
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':

    C = const()
    ns_set = C['ns_cal']
    set_id_set = C['set_id_cal']

    pcA = np.int64(sys.argv[1])
    pcB = np.int64(sys.argv[2])

    pltmap(ns_set, set_id_set, pcA, pcB)

    plt.show()
