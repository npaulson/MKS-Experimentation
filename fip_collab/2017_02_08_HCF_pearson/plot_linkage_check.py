import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
import h5py


def plot_check(par, flvl, H, erv):

    C = const()

    """define the colors of interest"""
    n_col = len(C['sid'])
    colormat = cm.rainbow(np.linspace(0, 1, n_col))

    f_reg = h5py.File("regression_results_L%s.hdf5" % H, 'r')

    print par
    print "flvl: %s" % flvl

    """find the results associated with the desired n_pc, deg"""

    """load the simulated and predicted responses"""
    Rsim = f_reg.get('Rsim_%s' % par)[...]
    Rpred = f_reg.get('Rpred_%s' % par)[flvl, :]

    """write out the associated error"""
    n_fac = Rsim.mean()

    err = np.abs(100.*(Rpred-Rsim)/n_fac)
    print "mean %% error: %s" % err.mean()
    print "max %% error: %s" % err.max()

    """plot the prediction equal to simulation line"""
    fig = plt.figure(figsize=[6, 5.75])

    minval = np.min([Rsim, Rpred])
    maxval = np.max([Rsim, Rpred])

    valrange = maxval-minval
    minln = minval - 0.5*valrange
    maxln = maxval + 0.5*valrange
    line = np.array([minln, maxln])

    plt.plot(line, line, 'k-')

    """plot the % error lines"""
    offs = 0.01*erv*n_fac

    plt.plot(line+offs, line, 'k--',
             alpha=.5, label='%s%% error bounds' % erv)
    plt.plot(line, line+offs, 'k--',
             alpha=.5)

    c = 0
    for ii in xrange(len(C['sid'])):

        c_ = c + C['n_sc']
        Rsim_tmp = Rsim[c:c_]
        Rpred_tmp = Rpred[c:c_]
        c = c_

        # Rsim_tmp = Rsim[ii]
        # Rpred_tmp = Rpred[ii]

        plt.text(Rsim_tmp.mean(), Rpred_tmp.mean()+0.05*valrange, C['sid'][ii],
                 horizontalalignment='center',
                 verticalalignment='center')

        # plt.plot(Rsim_tmp, Rpred_tmp,
        #          marker='s', markersize=7, color=colormat[c, :],
        #          alpha=0.3, linestyle='', label=name)

        plt.plot(Rsim_tmp, Rpred_tmp,
                 marker='s', markersize=7, color=colormat[ii, :],
                 alpha=0.7, linestyle='')

    minbnd = minval - 0.1*valrange
    maxbnd = maxval + 0.1*valrange

    plt.axis([minbnd, maxbnd, minbnd, maxbnd])
    plt.axes().set_aspect('equal')

    plt.xlabel("simulation, ln($\%s_g$)" % par)
    plt.ylabel("prediction, ln($\%s_g$)" % par)

    # plt.legend(loc='upper left', shadow=True, fontsize='medium', ncol=1)

    fig.tight_layout()

    # plt.legend(bbox_to_anchor=(1.02, 1), loc=2, shadow=True, fontsize='medium')
    # fig.tight_layout(rect=(0, 0, .8, 1))

    f_reg.close()

    fig_name = 'prediction_%s_flvl%s_L%s.png' % (par, flvl, H)
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':
    par = "mu"
    n_pc = 2
    deg = 2
    H = 6
    erv = 10
    plot_check(par, n_pc, deg, H, erv)
    plt.show()
