import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
import h5py


def variance(pltshape, Hvec):

    C = const()

    colormat = cm.plasma(np.linspace(0, .8, len(Hvec)))
    # colormat = cm.rainbow(np.linspace(0, .9, len(Hvec)))
    # colormat = np.array([[0, 0, .9],
    #                      [0, .8, 0],
    #                      [.9, 0, 0]])

    fig = plt.figure(figsize=[6, 4])

    for ii in xrange(len(Hvec)):

        f = h5py.File("ratios_L%s.hdf5" % Hvec[ii], 'r')
        ratios = f.get('ratios')[...]
        f.close()

        data = np.cumsum(ratios)

        plt.plot(np.arange(data.size)+1, data, color=colormat[ii, :],
                 marker='D', markersize=5,
                 linewidth=2, linestyle='-',
                 alpha=.7,
                 label='L=%s' % Hvec[ii])

    tc = np.int16(np.ceil(pltshape[1]/15.))
    plt.xticks(np.arange(0, pltshape[1]+tc, tc))
    # plt.axis([0, ratios.size, 98, 100.1])

    plt.axis(pltshape)

    plt.xlabel('pc number')
    plt.ylabel('pca cumulative explained variance (%)')
    # plt.title('pca cumulative explained variance plot')

    plt.grid(linestyle='-', alpha=0.15)
    plt.legend(loc='lower right', shadow=True, fontsize='medium')

    plt.tight_layout()

    fig_name = 'explained_variance_npc%s.png' % pltshape[1]
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':
    pltshape = [.5, 15, 40, 105]
    Hvec = [6, 15, 41, 90]
    variance(pltshape, Hvec)
    plt.show()
