import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
from matplotlib.ticker import AutoMinorLocator
import h5py


def pltpcpoly(par, n_pc_max, upbnd, Hvec):

    C = const()

    colormat = cm.plasma(np.linspace(0, .8, len(Hvec)))
    # colormat = cm.rainbow(np.linspace(0, .9, len(Hvec)))

    # fig = plt.figure(figsize=[7, 5])
    fig, ax = plt.subplots(figsize=[7, 5])

    errmax = 0

    for ii in xrange(len(Hvec)):

        f = h5py.File("regression_results_L%s.hdf5" % Hvec[ii], 'r')

        rlen = f.get('order_%s' % par).shape[0]
        n_fac = f.get('Rpred_cal_%s' % par)[...].mean()

        """plot the prediction error versus number of pc for
        validation data"""

        plotmat = np.zeros((rlen, 3))
        plotmat[:, :2] = f.get('order_%s' % par)[...]
        plotmat[:, 2] = f.get('meanerr_val_%s' % par)[...]

        pc_range = len(np.unique(plotmat[:, 0]))
        poly_range = len(np.unique(plotmat[:, 1]))

        plotmat_ = plotmat.reshape((pc_range, poly_range, 3))

        err = 100*plotmat_[..., 0, 2]/n_fac
        if err.max() > errmax:
            errmax = err.max()

        plt.plot(np.arange(n_pc_max)+1, err[:n_pc_max],
                 marker='', markersize=8, color=colormat[ii, :], alpha=0.7,
                 linestyle='-', linewidth=2, label="calibration L=%s" % Hvec[ii])

    spc = np.int16(np.ceil(n_pc_max/15.))
    plt.xticks(np.arange(0, n_pc_max+spc, spc))

    minor_locator = AutoMinorLocator(2)
    ax.xaxis.set_minor_locator(minor_locator)
    plt.grid()
    plt.grid(which='minor')

    plt.axis([.5, n_pc_max+.5, 0, upbnd])

    plt.legend(loc='upper right', shadow=True, fontsize='small', ncol=2)

    plt.xlabel("number of PCs")
    plt.ylabel("mean error (%)")

    fig_name = 'selection_val_%s_npc%s.png' % (par, n_pc_max)
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)

    plt.tight_layout()

    f.close()


if __name__ == '__main__':
    par = "strength"
    n_pc_max = 50
    upbnd = 3
    Hvec = [6, 15, 41, 90]
    pltpcpoly(par, n_pc_max, upbnd, Hvec)
    plt.show()
