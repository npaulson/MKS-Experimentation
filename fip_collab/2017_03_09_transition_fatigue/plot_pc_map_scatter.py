import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from constants import const
import h5py
import sys


def pltmap(H, pcA, pcB):

    C = const()

    fig = plt.figure(figsize=[7.5, 5])
    ax = fig.add_subplot(111)

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

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % H, 'r')

    """plot SVE sets for cal"""
    ns_tot = np.sum(C['ns'])
    posA = np.zeros((ns_tot,))
    posB = np.zeros((ns_tot,))
    m_v = np.zeros((ns_tot,), dtype='str')
    s_v = np.zeros((ns_tot,))
    mfc_v = np.zeros((ns_tot, 4))
    mec_v = np.zeros((ns_tot, 4))

    c = 0
    for ii in xrange(len(C['sid'])):
        c_ = c + C['ns'][ii]

        sid = C['sid'][ii]
        reduced = f_red.get('reduced_%s' % sid)[...]

        posA[c:c_] = reduced[:, pcA]
        posB[c:c_] = reduced[:, pcB]
        m_v[c:c_] = markermat[ii]
        s_v[c:c_] = sizemat[ii]

        mfc = np.zeros((4,))
        mfc[:3] = colormat[ii, :3] + .3*(1-colormat[ii, :3])
        mfc[3] = 1  # marker face alpha

        mec = np.zeros((4,))
        mec[:3] = 0.7*colormat[ii, :3]
        mec[3] = 1  # marker edge alpha

        mfc_v[c:c_, :] = mfc
        mec_v[c:c_, :] = mec

        # plt.plot(reduced[:, pcA], reduced[:, pcB],
        #          marker=markermat[ii], markersize=sizemat[ii],
        #          mfc=mfc, mec=mec,
        #          linestyle='')

        c = c_

    idxvec = np.arange(ns_tot)
    np.random.shuffle(idxvec)
    for ii in idxvec:
        plt.scatter(posA[ii], posB[ii], s=s_v[ii]**2, marker=m_v[ii],
                    c=mfc_v[ii, :], edgecolors=mec_v[ii, :])

    for ii in xrange(len(C['sid'])):

        sid = C['sid'][ii]
        name = C['names_plt'][ii]

        reduced = f_red.get('reduced_%s' % sid)[...]
        meanA = reduced[:, pcA].mean()
        meanB = reduced[:, pcB].mean()

        plt.text(meanA, meanB+8, name,
                 horizontalalignment='center',
                 verticalalignment='center',
                 fontsize=20,
                 weight='semibold',
                 color=[0.15, 0.15, 0.15],
                 alpha=0.99)

    plt.margins(.1)

    plt.xlabel("PC%s" % str(pcA+1), fontsize='large')
    plt.ylabel("PC%s" % str(pcB+1), fontsize='large')
    plt.xticks(fontsize='large')
    plt.yticks(fontsize='large')

    plt.grid(linestyle='-', alpha=0.15)

    gr = 1.00
    ax.patch.set_facecolor([gr, gr, gr])

    fig.tight_layout()

    f_red.close()

    fig_name = 'pc%s_pc%s_L%s.png' % (pcA+1, pcB+1, H)
    fig.canvas.set_window_title(fig_name)
    plt.savefig(fig_name)


if __name__ == '__main__':
    H = np.int64(sys.argv[1])
    pcA = np.int64(sys.argv[2])
    pcB = np.int64(sys.argv[3])

    pltmap(H, pcA, pcB)

    plt.show()
