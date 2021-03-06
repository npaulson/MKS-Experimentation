import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
import h5py
import sys


def pltmap(H, pcA, pcB):

    C = const()

    fig = plt.figure(figsize=[9, 5])

    colormat = cm.rainbow(np.linspace(0, 1, len(C['set_id_val'])))
    # colormat = cm.Set1(np.linspace(0, 1, len(C['set_id_val'])))

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % H, 'r')

    """plot SVE sets for cal"""

    for ii in xrange(len(C['set_id_cal'])):

        set_id = C['set_id_cal'][ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]

        plt.plot(reduced[:, pcA], reduced[:, pcB],
                 marker='s', markersize=6, color=colormat[ii, :], alpha=0.4,
                 linestyle='', label="%s (calibration)" % C['names_cal'][ii])

    """plot SVE sets for val"""

    for ii in xrange(len(C['set_id_val'])):

        set_id = C['set_id_val'][ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]

        plt.plot(reduced[:, pcA], reduced[:, pcB],
                 marker='o', markersize=6, color=colormat[ii, :], alpha=0.4,
                 linestyle='', label="%s (validation)" % C['names_val'][ii])

    """plot centers of SVE sets for cal"""

    for ii in xrange(len(C['set_id_cal'])):

        set_id = C['set_id_cal'][ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]

        plt.plot(reduced[:, pcA].mean(), reduced[:, pcB].mean(), alpha=0.99,
                 marker='s', markersize=8, color=colormat[ii, :],
                 linestyle='')

    """plot centers of SVE sets for val"""

    for ii in xrange(len(C['set_id_val'])):

        set_id = C['set_id_val'][ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]

        plt.plot(reduced[:, pcA].mean(), reduced[:, pcB].mean(), alpha=0.99,
                 marker='o', markersize=8, color=colormat[ii, :],
                 linestyle='')

    plt.margins(.1)

    plt.xlabel("PC%s" % str(pcA+1))
    plt.ylabel("PC%s" % str(pcB+1))

    plt.grid(True)

    plt.legend(bbox_to_anchor=(1.02, 1), loc=2, shadow=True, fontsize='medium')

    fig.tight_layout(rect=(0, 0, .6, 1))

    f_red.close()

    fig_name = 'pc%s_pc%s_L%s.png' % (pcA+1, pcB+1, H)
    fig.canvas.set_window_title(fig_name)


if __name__ == '__main__':

    C = const()

    H = C['H']

    pcA = np.int64(sys.argv[1])
    pcB = np.int64(sys.argv[2])

    pltmap(H, pcA, pcB)

    plt.show()
