import numpy as np
import matplotlib.pyplot as plt
from constants import const
import h5py


def variance(pltshape):

    C = const()

    colormat = np.array([[0, 0, .9],
                         [0, .8, 0],
                         [.9, 0, 0]])

    # H = [4, 9, 23]
    H = [9]

    fig = plt.figure(figsize=[7, 4])

    for ii in xrange(len(H)):

        f = h5py.File("pca_data_L%s.hdf5" % H[ii], 'r')
        ratios = f.get('ratios')[...]
        f.close()

        data = np.zeros((ratios.size+1,))
        data[1:] = np.cumsum(ratios)

        plt.plot(np.arange(data.size), data, color=colormat[ii, :],
                 linestyle='-', marker='x', markersize=6, label='L=%s' % H[ii])

    tc = np.int16(np.ceil(pltshape[1]/15.))
    plt.xticks(np.arange(0, pltshape[1]+tc, tc))
    # plt.axis([0, ratios.size, 98, 100.1])

    plt.axis(pltshape)

    plt.xlabel('pc number')
    plt.ylabel('pca cumulative explained variance (%)')
    # plt.title('pca cumulative explained variance plot')

    plt.grid(True)
    plt.legend(loc='lower right', shadow=True, fontsize='medium')

    plt.tight_layout()

    fig_name = 'explained_variance_npc%s.png' % pltshape[1]
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':
    variance()
    plt.show()
