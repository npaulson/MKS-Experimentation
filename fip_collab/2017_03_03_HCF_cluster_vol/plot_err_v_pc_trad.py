import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
from matplotlib.ticker import AutoMinorLocator
import h5py


def plterr(par, lowbnd, upbnd, deg, Tvec, Hvec):

    C = const()

    colormat = cm.viridis(np.linspace(0.2, 0.9, len(Hvec)))
    linemat = ['-', '--', ':']

    maxpc = C['pcdeg'][C['pcdeg'][:, 1] == deg, 0][-1]

    fig, ax = plt.subplots(figsize=[5.5, 3.25])

    for ii in xrange(len(Hvec)):
        for jj in xrange(len(Tvec)):

            f = h5py.File("regression_results_L%s.hdf5" % Hvec[ii], 'r')
            isdeg = (C['pcdeg'][:, 1] == deg)

            iscal = f.get('iscal_%s' % par)[...]

            pred = f.get('Rpred_%s' % par)[...]
            sim = f.get('Rsim_%s' % par)[...]
            predCV = f.get('RpredCV_%s' % par)[...]

            if Tvec[jj] == 'cal':
                label = 'L=%s'
                tmpA = pred[isdeg, :][:, iscal]
                tmpB = sim[iscal]
                err_tmp = np.mean(np.abs(tmpA - tmpB), 1)

            elif Tvec[jj] == 'val':
                label = 'L=%s'
                tmpA = pred[isdeg, :][:, iscal == 0]
                tmpB = sim[iscal == 0]
                # tmpA = pred[isdeg, :]
                # tmpB = sim
                err_tmp = np.mean(np.abs(tmpA - tmpB), 1)

            elif Tvec[jj] == 'loocv':
                label = 'L=%s'
                tmpA = predCV[isdeg, :]
                tmpB = sim[iscal]
                err_tmp = np.mean(np.abs(tmpA - tmpB), 1)

            else:
                label = 'null'
                err_tmp = np.zeros((maxpc,))

            err = 100*np.abs(err_tmp/sim.mean())

            plt.plot(np.arange(maxpc)+1, err,
                     marker='', markersize=8,
                     color=colormat[ii, :], alpha=0.7,
                     linestyle=linemat[jj], linewidth=2,
                     label=label % Hvec[ii])

            f.close()

    spc = np.int16(np.ceil(maxpc/10.))
    plt.xticks(np.arange(0, maxpc+spc, spc))

    minor_locator = AutoMinorLocator(2)
    ax.xaxis.set_minor_locator(minor_locator)
    plt.grid(linestyle='-', alpha=0.15)
    plt.grid(which='minor', linestyle='-', alpha=0.2)

    plt.axis([.5, maxpc+.5, lowbnd, upbnd])

    plt.legend(loc='upper center', shadow=False,
               fontsize='medium', ncol=3, fancybox=False)

    plt.xlabel("number of PCs", fontsize='large')
    plt.ylabel("mean error (%)", fontsize='large')

    plt.xticks(fontsize='large')
    plt.yticks(fontsize='large')

    plt.tight_layout()

    typs = ''.join(Tvec)
    fig_name = 'selection_%s_%s_deg%s_npc%s.png' % (typs, par, deg, maxpc)
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
