import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def variance(pltshape, ratios):

    color = cm.plasma(0.5)

    fig = plt.figure(figsize=[6.5, 4.5])

    data = np.cumsum(ratios)

    plt.plot(np.arange(data.size)+1, data, color=color,
             marker='D', markersize=5,
             linewidth=2, linestyle='-',
             alpha=.7)

    tc = np.int16(np.ceil(pltshape[1]/15.))
    plt.xticks(np.arange(0, pltshape[1]+tc, tc), fontsize='large')
    plt.yticks(fontsize='large')
    # plt.axis([0, ratios.size, 98, 100.1])

    plt.axis(pltshape)

    plt.xlabel(r'$\tilde{R}$', fontsize='large')
    plt.ylabel('pca cumulative \nexplained variance (%)', fontsize='large')
    # plt.title('pca cumulative explained variance plot')

    plt.grid(linestyle='-', alpha=0.15)
    plt.legend(loc='lower right', shadow=True, fontsize='large')

    plt.tight_layout()


if __name__ == '__main__':
    pltshape = [.5, 15, 40, 105]
    Hvec = [6, 15, 41, 90]
    variance(pltshape, Hvec)
    plt.show()
