import numpy as np
import matplotlib.pyplot as plt
from constants import const
import h5py


def variance():

    C = const()

    f = h5py.File("pca_data_L%s.hdf5" % C['H'], 'r')
    ratios = f.get('ratios')[...]
    f.close()

    # fig = plt.figure(figsize=[6, 5])

    data = np.zeros((ratios.size+1,))
    data[1:] = np.cumsum(ratios)

    # plt.plot(np.arange(data.size), data, 'k.-')

    fig, (ax, ax2) = plt.subplots(1, 2, sharey=True)

    # plot the same data on both axes
    ax.plot(np.arange(data.size), data, 'k.-')
    ax2.plot(np.arange(data.size), data, 'k.-')

    # zoom-in / limit the view to different portions of the data
    ax.set_xlim(0, 20)  # most of the data
    ax2.set_xlim(120, 140)  # outliers only

    # hide the spines between ax and ax2
    ax.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax.yaxis.tick_left()
    ax.tick_params(labeltop='off')  # don't put tick labels at the top
    ax2.yaxis.tick_right()

    # Make the spacing between the two axes a bit smaller
    plt.subplots_adjust(wspace=0.15)

    d = .015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass plot, just so we don't keep repeating them
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    ax.plot((1-d, 1+d), (-d, +d), **kwargs)  # top-left diagonal
    ax.plot((1-d, 1+d), (1-d, 1+d), **kwargs)  # bottom-left diagonal

    kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
    ax2.plot((-d, d), (-d, +d), **kwargs)  # top-right diagonal
    ax2.plot((-d, d), (1-d, 1+d), **kwargs)  # bottom-right diagonal

    ax.grid(True)
    ax2.grid(True)
    ax.set_ylim(0, 105)
    ax2.set_ylim(0, 105)

    # # tc = np.int16(np.ceil(ratios.size/10.))
    # # plt.xticks(np.arange(0, ratios.size+tc, tc))

    # plt.yticks(np.arange(0, 110, 10))
    # plt.axis([0, 20, 0, 105.])
    # # plt.axis([0, ratios.size, 98, 100.1])

    ax.set_ylabel('pca cumulative explained variance (%)')
    # # plt.title('pca cumulative explained variance plot')
    plt.tight_layout()

    fig_name = 'explained_variance_L%s.png' % C['H']
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':
    variance()
    plt.show()
