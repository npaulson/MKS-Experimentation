import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sys


def pltmap(reduced, pcA, pcB, n_sets, sample_size):

    fig = plt.figure(figsize=[7.5, 5])

    colormat = cm.rainbow(np.linspace(0, 1, n_sets))

    for ii in xrange(n_sets):

        c = ii*sample_size
        c_ = (ii+1)*sample_size

        plt.plot(reduced[c:c_, pcA], reduced[c:c_, pcB],
                 marker='s', markersize=8, color=colormat[ii, :],
                 alpha=0.4, linestyle='')

    for ii in xrange(n_sets):

        c = ii*sample_size
        c_ = (ii+1)*sample_size

        meanA = reduced[c:c_, pcA].mean()
        meanB = reduced[c:c_, pcB].mean()
        plt.text(meanA, meanB, 'C%s' % ii,
                 horizontalalignment='center',
                 verticalalignment='center',
                 fontsize=20,
                 color='k')

    plt.margins(.1)

    plt.xlabel("PC%s" % str(pcA+1), fontsize='large')
    plt.ylabel("PC%s" % str(pcB+1), fontsize='large')
    plt.xticks(fontsize='large')
    plt.yticks(fontsize='large')

    plt.grid(linestyle='-', alpha=0.15)

    fig.tight_layout()


if __name__ == '__main__':

    H = np.int64(sys.argv[1])
    pcA = np.int64(sys.argv[2])
    pcB = np.int64(sys.argv[3])

    pltmap(H, pcA, pcB)

    plt.show()
