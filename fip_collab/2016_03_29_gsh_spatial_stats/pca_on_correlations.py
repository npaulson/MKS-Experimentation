import functions as rr
import numpy as np
# from sklearn.decomposition import PCA
from scipy.linalg.interpolative import svd
import time
import h5py


def doPCA(el, H, ns_set, set_id_set, step, wrt_file):

    st = time.time()

    n_corr = H**2

    ns_tot = np.sum(ns_set)
    f_master = h5py.File("ref_%s%s_s%s.hdf5" % (ns_tot, 'allsets', step), 'w')

    # f_master.create_dataset("allcorr",
    #                         (ns_tot, n_corr*el**3),
    #                         dtype='float64')

    f_master.create_dataset("allcorr",
                            (ns_tot, n_corr*el**3),
                            dtype='complex128')

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

    # pca = PCA(n_components=50)
    # pca.fit(allcorr[...])
    # ratios = np.round(100*pca.explained_variance_ratio_, 2)

    # msg = "pca explained variance: %s%%" % str(ratios)
    # rr.WP(msg, wrt_file)

    # f_master.create_dataset('ratios', data=ratios)

    # f_master.close()

    corr_tmp = allcorr[...]
    # subtract out the mean feature values from corr_tmp
    corr_mean = np.mean(corr_tmp, 0)[None, :]
    corr_tmp += -corr_mean

    print "allcorr.dtype: %s" % str(corr_tmp.dtype)
    print "allcorr.shape: %s" % str(corr_tmp.shape)
    U, S, V = svd(corr_tmp, 29)
    print "V.shape: %s" % str(V.shape)

    """calculate percentage explained variance"""
    X_transformed = np.dot(U, np.diag(S))
    exp_var = np.var(X_transformed, axis=0)
    full_var = np.var(corr_tmp, axis=0).sum()
    ratios = np.round(100*(exp_var/full_var), 2)
    print ratios.sum()
    msg = "pca explained variance: %s%%" % str(ratios)
    rr.WP(msg, wrt_file)

    for ii in xrange(len(set_id_set)):

        f_temp = h5py.File("ref_%s%s_s%s.hdf5" %
                           (ns_set[ii], set_id_set[ii], step), 'a')
        ff = f_temp.get('ff')[...].reshape(ns_set[ii], n_corr*el**3)

        # tmp = pca.transform(ff)

        # subtract out the mean feature values
        ff_r = ff - corr_mean
        # perfrom whitening
        V_norm = V/(np.sqrt(S)[None, :])
        tmp = np.dot(ff_r, V_norm)

        f_temp.create_dataset('pc_corr', data=tmp, dtype='complex128')

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
