import functions as rr
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import time
import h5py


def doPCA(el, ns_set, H, set_id_set, step, wrt_file):

    st = time.time()

    print H
    n_corr = H**2

    ns_tot = np.sum(ns_set)
    f_master = h5py.File("ref_%s%s_s%s.hdf5" % (ns_tot, 'allsets', step), 'w')

    f_master.create_dataset("allcorr",
                            (ns_tot, n_corr*el**3),
                            dtype='float64')

    # f_master.create_dataset("allcorr",
    #                         (ns_tot, n_corr*el**3),
    #                         dtype='complex128')

    allcorr = f_master.get('allcorr')

    c = 0
    for ii in xrange(len(set_id_set)):

        f_temp = h5py.File("ref_%s%s_s%s.hdf5" %
                           (ns_set[ii], set_id_set[ii], step), 'a')

        tmp = f_temp.get('ff')[...]
        ff = tmp.reshape(ns_set[ii], n_corr*el**3)

        allcorr[c:c+ns_set[ii], ...] = ff

        c += ns_set[ii]

        f_temp.close()

    msg = "correlations combined"
    rr.WP(msg, wrt_file)

    pca = PCA(n_components=20)
    pca.fit(allcorr[...])
    ratios = np.round(100*pca.explained_variance_ratio_, 1)
    msg = "pca explained variance: %s%%" % str(ratios)
    rr.WP(msg, wrt_file)

    plt.figure(10)
    plt.plot(np.arange(ratios.size), ratios)
    plt.xlabel('pc number')
    plt.ylabel('pca explained variance (%)')
    plt.title('pca explained variance plot')
    plt.show()

    f_master.close()

    for ii in xrange(len(set_id_set)):

        f_temp = h5py.File("ref_%s%s_s%s.hdf5" %
                           (ns_set[ii], set_id_set[ii], step), 'a')
        ff = f_temp.get('ff')[...].reshape(ns_set[ii], n_corr*el**3)

        tmp = pca.transform(ff)

        f_temp.create_dataset('pc_corr', data=tmp, dtype='float64')
        # f_temp.create_dataset('pc_corr', data=tmp, dtype='complex128')

        f_temp.close()

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
