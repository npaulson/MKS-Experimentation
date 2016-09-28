import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
from matplotlib.ticker import AutoMinorLocator
import h5py


def plterr(par, upbnd, deg, Tvec, Hvec):

    C = const()

    colormat = cm.plasma(np.linspace(0, .8, len(Hvec)))
    # colormat = cm.rainbow(np.linspace(0, .9, len(Hvec)))
    linemat = ['-', '--', ':']

    fig, ax = plt.subplots(figsize=[7, 5])

    for ii in xrange(len(Hvec)):
        for jj in xrange(len(Tvec)):

            f = h5py.File("regression_results_L%s.hdf5" % Hvec[ii], 'r')
            rlen = f.get('order_%s' % par).shape[0]
            n_fac = f.get('Rpred_%s' % par)[...].mean()

            """plot the prediction error versus number of pc"""

            plotmat = np.zeros((rlen, 3))
            plotmat[:, :2] = f.get('order_%s' % par)[...]
            plotmat[:, 2] = f.get('%s_%s' % (Tvec[jj], par))[...]

            pc_range = len(np.unique(plotmat[:, 0]))
            poly_range = len(np.unique(plotmat[:, 1]))

            plotmat_ = plotmat.reshape((pc_range, poly_range, 3))

            err = np.abs(100*plotmat_[..., deg-1, 2]/n_fac)

            if Tvec[jj] == 'meanerr':
                label = 'calibration, L=%s'
            elif Tvec[jj] == 'LOOCV':
                label = 'LOOCV, L=%s'
            else:
                label = 'L=%s'

            plt.plot(np.arange(C['n_pc_max'])+1, err[:C['n_pc_max']],
                     marker='', markersize=8,
                     color=colormat[ii, :], alpha=0.7,
                     linestyle=linemat[jj], linewidth=2,
                     label=label % Hvec[ii])

            f.close()

    spc = np.int16(np.ceil(C['n_pc_max']/15.))
    plt.xticks(np.arange(0, C['n_pc_max']+spc, spc))

    minor_locator = AutoMinorLocator(2)
    ax.xaxis.set_minor_locator(minor_locator)
    plt.grid(linestyle='-', alpha=0.15)
    plt.grid(which='minor', linestyle='-', alpha=0.2)

    plt.axis([.5, C['n_pc_max']+.5, 0, upbnd])

    plt.legend(loc='upper right', shadow=True, fontsize='small', ncol=3)

    plt.xlabel("number of PCs")
    plt.ylabel("mean error (%)")

    plt.tight_layout()

    typs = ''.join(Tvec)
    fig_name = 'selection_%s_%s_npc%s.png' % (typs, par, C['n_pc_max'])
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':
    C = const()
    par = "strength"
    upbnd = 3
    Tvec = ['cal']
    Hvec = [6, 15, 41, 90]
    plterr(C, par, upbnd, Tvec, Hvec)
    plt.show()
