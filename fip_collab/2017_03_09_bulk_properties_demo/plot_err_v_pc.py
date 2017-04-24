import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
from matplotlib.ticker import AutoMinorLocator
import h5py


def plterr(C, par, upbnd, deg, Tvec, Hvec):

    colormat = cm.plasma(np.linspace(0, .8, len(Hvec)))
    # colormat = cm.rainbow(np.linspace(0, .9, len(Hvec)))
    linemat = ['-', '--', ':']

    maxpc = C['pcdeg'][C['pcdeg'][:, 1] == deg, 0][-1]

    fig, ax = plt.subplots(figsize=[5.5, 3.25])

    for ii in xrange(len(Hvec)):
        for jj in xrange(len(Tvec)):

            f = h5py.File("regression_results_L%s.hdf5" % Hvec[ii], 'r')
            isdeg = (C['pcdeg'][:, 1] == deg)

            Rpred_cal = f.get('Rpred_cal_%s' % par)[...]
            Rpred_cv = f.get('Rpred_cv_%s' % par)
            Rpred_val = f.get('Rpred_val_%s' % par)[...]
            Rsim_cal = f.get('Rsim_cal_%s' % par)[...]
            Rsim_val = f.get('Rsim_val_%s' % par)[...]

            if Tvec[jj] == 'cal':
                label = 'calibration, L=%s'
                tmpA = Rpred_cal[isdeg, :]
                tmpB = Rsim_cal
                err_tmp = np.mean(np.abs(tmpA - tmpB), 1)

            elif Tvec[jj] == 'val':
                label = 'validation, L=%s'
                tmpA = Rpred_val[isdeg, :]
                tmpB = Rsim_val
                err_tmp = np.mean(np.abs(tmpA - tmpB), 1)

            elif Tvec[jj] == 'cv':
                label = 'CV, L=%s'
                tmpA = Rpred_cv[isdeg, :]
                tmpB = Rsim_cal
                err_tmp = np.mean(np.abs(tmpA - tmpB), 1)

            else:
                label = 'null'
                err_tmp = np.zeros((maxpc,))

            err = 100*np.abs(err_tmp/Rsim_cal.mean())

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

    plt.axis([.5, maxpc+.5, 0, upbnd])

    plt.legend(loc='upper right', shadow=True, fontsize='medium', ncol=3)

    plt.xlabel("number of PCs", fontsize='large')
    plt.ylabel("mean error (%)", fontsize='large')

    plt.xticks(fontsize='large')
    plt.yticks(fontsize='large')
    plt.title('%s %s' % (par, deg))

    plt.tight_layout()


if __name__ == '__main__':
    C = const()
    par = "strength"
    upbnd = 3
    Tvec = ['cal']
    Hvec = [6, 15, 41, 90]
    plterr(C, par, upbnd, Tvec, Hvec)
    plt.show()
