import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import AutoMinorLocator


def plterr(Rpred, Rsim, order, deg, n_pc_max, upbnd):

    color = cm.plasma(0.7)

    fig, ax = plt.subplots(figsize=[5.5, 3.25])

    rlen = order.shape[0]
    n_fac = Rsim.mean()

    """plot the prediction error versus number of pc"""

    plotmat = np.zeros((rlen, 3))
    plotmat[:, :2] = order

    err = np.mean(np.abs(Rpred - Rsim), 1)
    plotmat[:, 2] = err

    pc_range = len(np.unique(plotmat[:, 0]))
    poly_range = len(np.unique(plotmat[:, 1]))

    plotmat_ = plotmat.reshape((pc_range, poly_range, 3))

    err = 100*plotmat_[..., deg-1, 2]/n_fac

    plt.plot(np.arange(n_pc_max)+1, err[:n_pc_max],
             marker='', markersize=8,
             color=color, alpha=0.7,
             linestyle='-', linewidth=2)

    spc = np.int16(np.ceil(n_pc_max/10.))
    plt.xticks(np.arange(0, n_pc_max+spc, spc), fontsize='small')
    plt.yticks(fontsize='small')

    minor_locator = AutoMinorLocator(3)
    ax.xaxis.set_minor_locator(minor_locator)
    plt.grid(linestyle='-', alpha=0.15)
    plt.grid(which='minor', linestyle='-', alpha=0.2)

    plt.axis([.5, n_pc_max+.5, 0, upbnd])

    plt.xlabel(r'$\tilde{R}$', fontsize='large')
    plt.ylabel("mean error (%)", fontsize='large')

    plt.xticks(fontsize='large')
    plt.yticks(fontsize='large')

    plt.tight_layout()


if __name__ == '__main__':
    par = "strength"
    n_pc_max = 50
    upbnd = 3
    Tvec = ['cal']
    Hvec = [6, 15, 41, 90]
    plterr(par, n_pc_max, upbnd, Tvec, Hvec)
    plt.show()
