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

    colormat = cm.rainbow(np.linspace(0, 1, len(C['set_id'])))

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % H, 'r')

    """plot microstructures"""

    for ii in xrange(len(C['set_id'])):

        set_id = C['set_id'][ii]

        reduced = f_red.get('reduced_%s' % set_id)[...]

        plt.plot(reduced[:, pcA], reduced[:, pcB],
                 marker='s', markersize=6, color=colormat[ii, :], alpha=0.4,
                 linestyle='', label=C['names'][ii])

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
