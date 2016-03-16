import functions as rr
import numpy as np
from sklearn.decomposition import PCA
import time
import h5py


def doPCA(el, n_corr, ns_set, set_id_set, step, wrt_file):

    st = time.time()

    ns_tot = np.sum(ns_set)
    f_master = h5py.File("D_%s%s_s%s.hdf5" % (ns_tot, 'allsets', step), 'a')
    f_master.create_dataset("allcorr",
                            (ns_tot, n_corr*el**3),
                            dtype='complex128')
    allcorr = f_master.get('allcorr')

    # allcorr = np.zeros((ns_tot, n_corr*el**3), dtype='complex128')

    c = 0
    for ii in xrange(len(set_id_set)):

        f_temp = h5py.File("D_%s%s_s%s.hdf5" %
                           (ns_set[ii], set_id_set[ii], step), 'a')

        tmp = f_temp.get('ff_auto')[...]
        ff_auto = tmp.reshape(ns_set[ii], n_corr*el**3)

        allcorr[c:c+ns_set[ii], ...] = ff_auto

        c += ns_set[ii]

        f_temp.close()

    # f_master.create_dataset('allcorr', data=allcorr)

    pca = PCA(n_components=10)
    pca.fit(allcorr[...])
    print pca.explained_variance_ratio_

    f_master.close()

    for ii in xrange(len(set_id_set)):

        f_temp = h5py.File("D_%s%s_s%s.hdf5" %
                           (ns_set[ii], set_id_set[ii], step), 'a')
        ff_auto = f_temp.get('ff_auto')[...].reshape(ns_set[ii], n_corr*el**3)

        tmp = pca.transform(ff_auto)

        f_temp.create_dataset('pc_corr', data=tmp, dtype='complex128')

        f_temp.close()

    msg = "PCA completed: %ss" % np.round(time.time()-st, 5)
    rr.WP(msg, wrt_file)


if __name__ == '__main__':
    el = 21
    n_corr = 15
    ns_set = [10, 10, 10]
    set_id_set = ['random', 'transverse', 'basaltrans']
    step = 0
    wrt_file = 'test.txt'

    doPCA(el, n_corr, ns_set, set_id_set, step, wrt_file)
