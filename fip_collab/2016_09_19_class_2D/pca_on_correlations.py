import functions as rr
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import time
import h5py


def doPCA(el, ns_set, H, set_id_set, wrt_file):

    n_corr = H-1

    """combine the spatial statistics into one data matrix"""
    st = time.time()

    ns_tot = np.sum(ns_set)
    f_master = h5py.File("sve_reduced_all.hdf5", 'w')

    f_master.create_dataset("allcorr",
                            (ns_tot, n_corr*el**2),
                            dtype='float64')

    allcorr = f_master.get('allcorr')

    f_stats = h5py.File("spatial_stats.hdf5", 'a')

    c = 0
    for ii in xrange(len(set_id_set)):

        tmp = f_stats.get('ff_%s' % set_id_set[ii])[...]
        ff = tmp.reshape(ns_set[ii], n_corr*el**2)

        allcorr[c:c+ns_set[ii], ...] = ff

        c += ns_set[ii]

    """perform principal component analysis"""
    n_pc = 10
    pca = PCA(n_components=n_pc)
    pca.fit(allcorr[...])
    ratios = 100*pca.explained_variance_ratio_
    ratios_c = np.cumsum(ratios)

    """plot the cumulative explained variance"""
    plt.figure(figsize=[6, 4])
    plt.plot(np.arange(ratios_c.size)+1, ratios_c,
             marker='D', markersize=5,
             linewidth=2, linestyle='-',
             alpha=.7)
    plt.xlabel('PC number')
    plt.ylabel('PCA cumulative explained variance (%)')
    plt.grid(linestyle='-', alpha=0.15)
    plt.axis([.5, n_pc+.5, np.min(ratios_c)-1, 101])
    plt.tight_layout()
    plt.show()

    f_master.close()

    """transform the spatial statistics to PC space"""
    f_red = h5py.File("sve_reduced.hdf5", 'w')

    for ii in xrange(len(set_id_set)):

        ff = f_stats.get('ff_%s' % set_id_set[ii])[...]
        ff = ff.reshape(ns_set[ii], n_corr*el**2)

        tmp = pca.transform(ff)

        f_red.create_dataset('reduced_%s' % set_id_set[ii],
                             data=tmp,
                             dtype='float64')

    f_red.close()
    f_stats.close()

    msg = "PCA completed: %ss" % np.round(time.time()-st, 5)
    rr.WP(msg, wrt_file)


if __name__ == '__main__':
    el = 21
    H = 15
    ns_set = [10, 10, 10]
    set_id_set = ['random', 'transverse', 'basaltrans']
    step = 0
    wrt_file = 'test.txt'

    doPCA(el, H, ns_set, set_id_set, step, wrt_file)
