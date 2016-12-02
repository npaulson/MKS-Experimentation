import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import functions as rr
from constants import const
import h5py


def plot_check(par, n_pc, n_poly, H):

    C = const()

    colormat = cm.rainbow(np.linspace(0, 1, 5))
    # colormat = cm.Set1(np.linspace(0, 1, len(C['set_id_val'])))
    gray = [.7, .7, .7]

    f_reg = h5py.File("regression_results_L%s.hdf5" % H, 'r')
    order = f_reg.get('order_%s' % par)[...]

    """explicitly define #PCs"""
    tmp = (order[:, 0] == n_pc)*(order[:, 1] == n_poly)
    indx = np.arange(order.shape[0])[tmp]

    # """calculate # PCs required to reach desired explained variance"""
    # f_pc = h5py.File("pca_data_L%s.hdf5" % H, 'r')
    # ratios = f_pc.get('ratios')[...]
    # f_pc.close()

    # tmp = np.cumsum(ratios)
    # tmp = np.arange(tmp.size)[tmp >= C["ev_lvl"]]
    # # max_ev = tmp.max()
    # # print "max explained variance: %s" % max_ev
    # # tmp = np.arange(tmp.size)[tmp >= max_ev]
    # n_pc = tmp[0] + 1

    # tmp = (order[:, 0] == n_pc)*(order[:, 1] == n_poly)

    # indx = np.arange(order.shape[0])[tmp]

    # """calculate # PCs to minimize LOOCV mean error"""
    # indx = np.argmin(f_reg.get('loocv_err_%s' % par))
    # n_pc = order[indx, 0]

    msg = par
    rr.WP(msg, C['wrt_file'])
    msg = "n_pc, n_poly: %s" % str(order[indx, :])
    rr.WP(msg, C['wrt_file'])

    """find the results associated with the desired n_pc, n_poly"""

    """load the simulated and predicted responses"""

    if par == 'modulus':
        RsimC = f_reg.get('Rsim_cal_%s' % par)[...]*(1e-3)
        RpredC = f_reg.get('Rpred_cal_%s' % par)[indx, :]*(1e-3)
        RsimV = f_reg.get('Rsim_val_%s' % par)[...]*(1e-3)
        RpredV = f_reg.get('Rpred_val_%s' % par)[indx, :]*(1e-3)
    else:
        RsimC = f_reg.get('Rsim_cal_%s' % par)[...]
        RpredC = f_reg.get('Rpred_cal_%s' % par)[indx, :]
        RsimV = f_reg.get('Rsim_val_%s' % par)[...]
        RpredV = f_reg.get('Rpred_val_%s' % par)[indx, :]



    """write out the associated error"""
    n_fac = RsimC.mean()

    errC = 100.*np.abs(RpredC-RsimC)/n_fac
    msg = "mean %% error for cal: %s" % errC.mean()
    rr.WP(msg, C['wrt_file'])
    msg = "max %% error for cal: %s" % errC.max()
    rr.WP(msg, C['wrt_file'])

    errV = 100.*np.abs(RpredV-RsimV)/n_fac
    msg = "mean %% error for val: %s" % errV.mean()
    rr.WP(msg, C['wrt_file'])
    msg = "max %% error for val: %s" % errV.max()
    rr.WP(msg, C['wrt_file'])

    """plot the prediction equal to simulation line"""
    fig = plt.figure(figsize=[6.25, 6])

    minval = np.min([np.min([RsimC, RpredC]), np.min([RsimV, RpredV])])
    maxval = np.max([np.max([RsimC, RpredC]), np.max([RsimV, RpredV])])

    valrange = maxval-minval
    minln = minval - 0.5*valrange
    maxln = maxval + 0.5*valrange
    line = np.array([minln, maxln])

    plt.plot(line, line, 'k-')

    """plot the % error lines"""
    if par == 'modulus':
        erv = 1
    elif par == 'strength':
        erv = 5
    else:
        erv = 5

    offs = 0.01*erv*n_fac

    plt.plot(line+offs, line, 'k--',
             alpha=.5, label='%s%% error bounds' % erv)
    plt.plot(line, line+offs, 'k--',
             alpha=.5)

    # c = 0
    # for ii in xrange(len(C['ns_cal'])):

    #     c_ = c + C['ns_cal'][ii]
    #     Rsim_tmp = RsimC[c:c_]
    #     Rpred_tmp = RpredC[c:c_]
    #     c = c_

    #     if ii == 0:
    #         plt.plot(Rsim_tmp, Rpred_tmp,
    #                  marker='o', markersize=7, color=gray,
    #                  alpha=0.3, linestyle='',
    #                  label="calibration data")
    #     else:
    #         plt.plot(Rsim_tmp, Rpred_tmp,
    #                  marker='o', markersize=7, color=gray,
    #                  alpha=0.3, linestyle='')

    c = 0
    for ii in xrange(len(C['ns_val'])):

        c_ = c + C['ns_val'][ii]
        name = C['names_plt_val'][ii]
        Rsim_tmp = RsimV[c:c_]
        Rpred_tmp = RpredV[c:c_]
        c = c_

        if ii == 0:
            plt.plot(Rsim_tmp, Rpred_tmp,
                     marker='o', markersize=9, color=gray,
                     alpha=0.3, linestyle='')
            # plt.plot(Rsim_tmp, Rpred_tmp,
            #          marker='s', markersize=7, color=gray,
            #          alpha=0.3, linestyle='',
            #          label="validation data")
        elif ii <= 6:
            plt.plot(Rsim_tmp, Rpred_tmp,
                     marker='o', markersize=9, color=gray,
                     alpha=0.3, linestyle='')
        else:
            plt.plot(Rsim_tmp, Rpred_tmp,
                     marker='o', markersize=9, color=colormat[ii-7, :],
                     alpha=0.5, linestyle='',
                     label=name)

    minbnd = minval - 0.1*valrange
    maxbnd = maxval + 0.1*valrange

    plt.axis([minbnd, maxbnd, minbnd, maxbnd])
    plt.axes().set_aspect('equal')

    if par == 'modulus':
        plt.xlabel("simulation (GPa)", fontsize='large')
        plt.ylabel("prediction (GPa)", fontsize='large')
    else:
        plt.xlabel("simulation (MPa)", fontsize='large')
        plt.ylabel("prediction (MPa)", fontsize='large')

    plt.xticks(fontsize='large')
    plt.yticks(fontsize='large')

    plt.legend(loc='upper left', shadow=True, fontsize='large')
    fig.tight_layout()

    # plt.legend(bbox_to_anchor=(1.02, 1), loc=2, shadow=True, fontsize='medium')
    # fig.tight_layout(rect=(0, 0, .8, 1))

    fig_name = 'prediction_%s_npc%s_npoly%s_L%s.png' % (par, n_pc, n_poly, H)
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)

    f_reg.close()


if __name__ == '__main__':
    C = const()
    par = "strength"
    n_pc = 6
    n_poly = 2
    H = 41
    plot_check(par, n_pc, n_poly, H)
    plt.show()
