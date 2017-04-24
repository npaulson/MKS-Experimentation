import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
from matplotlib.ticker import AutoMinorLocator
import h5py


def plterr(par, lowbnd, upbnd, H):

    C = const()

    # colormat = cm.viridis(np.array([0.3, 0.7]))
    colormat = cm.plasma(np.array([0.0, 0.4]))

    fig, ax = plt.subplots(figsize=[5.5, 3.25])

    f = h5py.File("regression_results_L%s.hdf5" % H, 'r')

    iscal = f.get('iscal_%s' % par)[...]
    pred = f.get('Rpred_%s' % par)[...]
    sim = f.get('Rsim_%s' % par)[...]
    predCV = f.get('RpredCV_%s' % par)[...]

    """plot calibration error"""
    tmpA = pred[:, iscal]
    tmpB = sim[iscal]
    err_tmp = np.mean(np.abs(tmpA - tmpB), 1)
    err = 100*np.abs(err_tmp/sim.mean())

    plt.plot(np.arange(C['fmax'])+1, err,
             marker='', markersize=8,
             color=colormat[0, :], alpha=0.7,
             linestyle='-', linewidth=2,
             label='training')

    """plot cv error"""
    tmpA = predCV
    tmpB = sim[iscal]
    err_tmp = np.mean(np.abs(tmpA - tmpB), 1)
    err = 100*np.abs(err_tmp/sim.mean())

    plt.plot(np.arange(C['fmax'])+1, err,
             marker='', markersize=8,
             color=colormat[1, :], alpha=0.7,
             linestyle='-', linewidth=2,
             label='cross-validation')

    f.close()

    spc = np.int16(np.ceil(C['fmax']/10.))
    plt.xticks(np.arange(0, C['fmax']+spc, spc))

    minor_locator = AutoMinorLocator(2)
    ax.xaxis.set_minor_locator(minor_locator)
    plt.grid(linestyle='-', alpha=0.15)
    plt.grid(which='minor', linestyle='-', alpha=0.2)

    plt.axis([.5, C['fmax']+.5, lowbnd, upbnd])

    plt.legend(loc='upper center', shadow=False,
               fontsize='medium', ncol=3, fancybox=False)

    plt.xlabel("number of features", fontsize='large')
    plt.ylabel("mean error (%)", fontsize='large')

    plt.xticks(fontsize='large')
    plt.yticks(fontsize='large')

    plt.tight_layout()

    fig_name = 'selection_%s_fmax%s.png' % (par, C['fmax'])
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
