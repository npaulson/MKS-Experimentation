import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
import h5py


def variance(C, pltshape, Hvec):

    colormat = cm.plasma(np.linspace(0, .8, len(Hvec)))

    plt.figure(figsize=[6, 4])

    for ii in xrange(len(Hvec)):

        f = h5py.File("pca_data_L%s.hdf5" % Hvec[ii], 'r')
        ratios = f.get('ratios')[...]
        f.close()

        data = np.zeros((ratios.size+1,))
        data[1:] = np.cumsum(ratios)

        plt.plot(np.arange(data.size), data, color=colormat[ii, :],
                 marker='D', markersize=5,
                 linewidth=2, linestyle='-',
                 alpha=.7,
                 label='L=%s' % Hvec[ii])

    tc = np.int16(np.ceil(pltshape[1]/15.))
    plt.xticks(np.arange(0, pltshape[1]+tc, tc))
    # plt.axis([0, ratios.size, 98, 100.1])

    plt.axis(pltshape)

    plt.xlabel('PC number', fontsize='large')
    plt.ylabel('PCA cumulative explained variance (%)', fontsize='large')

    plt.grid(linestyle='-', alpha=0.15)
    plt.legend(loc='lower right', shadow=True, fontsize='large')

    plt.tight_layout()


if __name__ == '__main__':
    C = const()
    pltshape = [0, 15, 40, 105]
    Hvec = [6, 15, 41, 90]
    variance(C, pltshape, Hvec)
    plt.show()
