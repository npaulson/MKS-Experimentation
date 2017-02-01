import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def parity(Rsim, Rpred, order, sample_size, n_sets, n_pc, n_poly):

    colormat = cm.rainbow(np.linspace(0, 1, n_sets))
    # colormat = cm.Set1(np.linspace(0, 1, len(C['set_id_val'])))

    """explicitly define #PCs"""
    tmp = (order[:, 0] == n_pc)*(order[:, 1] == n_poly)
    indx = np.arange(order.shape[0])[tmp]
    Rpred = np.squeeze(Rpred[indx, :])

    print "n_pc, n_poly: %s, %s" % (order[indx, 0], order[indx, 1])

    """write out the associated error"""
    n_fac = Rsim.mean()

    err = 100.*np.abs(Rpred-Rsim)/n_fac
    print "mean %% error: %s" % err.mean()
    print "max %% error: %s" % err.max()

    """plot the prediction equal to simulation line"""
    fig = plt.figure(figsize=[6.25, 6])

    minval = np.min([Rsim, Rpred])
    maxval = np.max([Rsim, Rpred])

    valrange = maxval-minval
    minln = minval - 0.5*valrange
    maxln = maxval + 0.5*valrange
    line = np.array([minln, maxln])

    plt.plot(line, line, 'k-')

    """plot the % error lines"""
    erv = 5

    offs = 0.01*erv*n_fac

    plt.plot(line+offs, line, 'k--',
             alpha=.5, label='%s%% error bounds' % erv)
    plt.plot(line, line+offs, 'k--',
             alpha=.5)

    c = 0
    for ii in xrange(n_sets):

        c_ = c + sample_size
        Rsim_tmp = Rsim[c:c_]
        Rpred_tmp = Rpred[c:c_]
        c = c_

        plt.plot(Rsim_tmp, Rpred_tmp,
                 marker='o', markersize=7, color=colormat[ii, :],
                 alpha=0.3, linestyle='',
                 label="C%s" % ii)

    minbnd = minval - 0.1*valrange
    maxbnd = maxval + 0.1*valrange

    plt.axis([minbnd, maxbnd, minbnd, maxbnd])
    plt.axes().set_aspect('equal')

    plt.xlabel("simulation (GPa)", fontsize='large')
    plt.ylabel("prediction (GPa)", fontsize='large')

    plt.xticks(fontsize='large')
    plt.yticks(fontsize='large')

    plt.legend(loc='upper left', shadow=True, fontsize='large')
    fig.tight_layout()

    plt.legend(bbox_to_anchor=(1.02, 1), loc=2, shadow=True, fontsize='medium')
    fig.tight_layout(rect=(0, 0, .8, 1))


if __name__ == '__main__':
    par = "strength"
    n_pc = 6
    n_poly = 2
    H = 41
    parity(par, n_pc, n_poly, H)
    plt.show()
