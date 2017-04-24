import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
import h5py


def plot_check(par, flvl, H, erv):

    C = const()

    """define the colors of interest"""
    n_col = len(C['sid'])
    clis = np.linspace(0, 1, n_col)
    colormat = cm.rainbow(clis)
    markermat = ['o', 'v', 'p',
                 's', '>', 'P',
                 '*', '<', 'X',
                 'D', 'd', '^']
    sizemat = [7, 7, 7,
               6, 7, 8,
               11, 7, 8,
               6, 7, 7]

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
    fig = plt.figure(figsize=[6.5, 5])

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
             alpha=.5, label='%s%%\nerror\nbounds' % erv)
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

        # plt.text(Rsim_tmp.mean(), Rpred_tmp.mean()+0.05*valrange, C['sid'][ii],
        #          horizontalalignment='center',
        #          verticalalignment='center')

        # mfc = np.zeros((4,))
        # mfc[:3] = 0.999*colormat[ii, :3]
        # mfc[3] = 0.5  # marker face alpha

        # mec = np.zeros((4,))
        # mec[:3] = 0.6*colormat[ii, :3]
        # mec[3] = 0.8  # marker edge alpha

        mfc = np.zeros((4,))
        mfc[:3] = colormat[ii, :3] + .3*(1-colormat[ii, :3])
        mfc[3] = 1  # marker face alpha

        mec = np.zeros((4,))
        mec[:3] = 0.7*colormat[ii, :3]
        mec[3] = 1  # marker edge alpha

        plt.plot(Rsim_tmp, Rpred_tmp,
                 marker=markermat[ii], markersize=sizemat[ii],
                 mfc=mfc,
                 mec=mec,
                 linestyle='', label=C['sid'][ii])

        # plt.plot(Rsim_tmp, Rpred_tmp,
        #          marker='o', markersize=7, color=colormat[ii, :],
        #          alpha=0.7, linestyle='', label= C['names_plt'][ii])

    minbnd = minval - 0.1*valrange
    maxbnd = maxval + 0.1*valrange

    plt.axis([minbnd, maxbnd, minbnd, maxbnd])
    plt.axes().set_aspect('equal')

    plt.xlabel(r'$\mathrm{simulation,} ln\left(\%s\right)$' % par,
               fontsize=16)
    plt.ylabel(r'$\mathrm{prediction,} ln\left(\%s\right)$' % par,
               fontsize=16)

    plt.xticks(fontsize=13, rotation=45)
    plt.yticks(fontsize=13, rotation=45)

    # plt.legend(loc='upper left', shadow=True, fontsize='small', ncol=1)
    # fig.tight_layout()

    plt.legend(bbox_to_anchor=(1.02, 1), loc=2,
               shadow=False, fontsize='medium',
               fancybox=False)
    fig.tight_layout(rect=(0, 0, .85, 1))

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
