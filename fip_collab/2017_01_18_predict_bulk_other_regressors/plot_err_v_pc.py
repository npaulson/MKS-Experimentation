import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
from matplotlib.ticker import AutoMinorLocator
import h5py


def plterr(par, n_pc_max, upbnd, typ, Hvec):

    C = const()

    colormat = cm.plasma(np.linspace(0, .8, len(Hvec)))

    fig, ax = plt.subplots(figsize=[5.5, 3.25])

    if typ == 'val':
        typ_p = 'val'
    else:
        typ_p = 'cal'

    for ii in xrange(len(Hvec)):

        f = h5py.File("regression_results_L%s.hdf5" % Hvec[ii], 'r')
        rlen = f.get('order_%s' % par).shape[0]
        n_fac = f.get('Rpred_cal_%s' % par)[...].mean()

        """plot the prediction error versus number of pc"""

        plotmat = np.zeros((rlen, 3))
        plotmat[:, :2] = f.get('order_%s' % par)[...]

        err = np.mean(np.abs(f.get('Rpred_%s_%s' % (typ, par))[...] -
                             f.get('Rsim_%s_%s' % (typ_p, par))[...]), 1)
        plotmat[:, 2] = err

        pc_range = len(np.unique(plotmat[:, 0]))
        poly_range = len(np.unique(plotmat[:, 1]))

        plotmat_ = plotmat.reshape((pc_range, poly_range, 3))

        err = 100*plotmat_[..., 0, 2]/n_fac

        plt.plot(np.arange(n_pc_max)+1, err[:n_pc_max],
                 marker='', markersize=8,
                 color=colormat[ii, :], alpha=0.7,
                 linestyle='-', linewidth=2,
                 label=r'$\tilde{L}=%s$' % Hvec[ii])

        f.close()

    spc = np.int16(np.ceil(n_pc_max/10.))
    plt.xticks(np.arange(0, n_pc_max+spc, spc), fontsize='small')
    plt.yticks(fontsize='small')

    minor_locator = AutoMinorLocator(3)
    ax.xaxis.set_minor_locator(minor_locator)
    plt.grid(linestyle='-', alpha=0.15)
    plt.grid(which='minor', linestyle='-', alpha=0.2)

    plt.axis([.5, n_pc_max+.5, 0, upbnd])

    plt.legend(loc='upper right', shadow=True, fontsize='large', ncol=2)

    plt.xlabel(r'$\tilde{R}$', fontsize='large')
    plt.ylabel("mean error (%)", fontsize='large')

    plt.xticks(fontsize='large')
    plt.yticks(fontsize='large')

    # if Tvec[0] == 'cal':
    #     etype = 'Calibration'
    # elif Tvec[0] == 'LOOCV':
    #     etype = 'LOOCV'
    # elif Tvec[0] == 'val':
    #     etype = 'Validation'
    # else:
    #     etype = 'Unknown'

    # if par == 'modulus':
    #     par_s = 'elastic stiffness'
    # if par == 'strength':
    #     par_s = 'yield strength'

    # plt.title('%s error, %s prediction' % (etype, par_s), fontsize='small')

    plt.tight_layout()

    fig_name = 'selection_%s_%s_npc%s.png' % (typ, par, n_pc_max)
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':
    par = "strength"
    n_pc_max = 50
    upbnd = 3
    Tvec = ['cal']
    Hvec = [6, 15, 41, 90]
    plterr(par, n_pc_max, upbnd, Tvec, Hvec)
    plt.show()
