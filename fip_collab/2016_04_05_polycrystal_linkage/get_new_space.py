import functions as rr
import numpy as np
# from sklearn.decomposition import PCA
# from sklearn.decomposition import TruncatedSVD
from scipy.linalg.interpolative import svd
import time
import h5py


def new_space(el, ns_set, H, set_id_set, step, wrt_file):

    st = time.time()

    print "H: %s" % H
    n_corr = H**2

    ns_tot = np.sum(ns_set)
    f_master = h5py.File("sve_reduced_all.hdf5", 'w')

    f_master.create_dataset("allcorr",
                            (ns_tot, n_corr*el**3),
                            dtype='complex128')

    # f_master.create_dataset("allcorr",
    #                         (ns_tot, n_corr*el**3),
    #                         dtype='float64')

    allcorr = f_master.get('allcorr')

    f_stats = h5py.File("spatial_stats.hdf5", 'a')

    c = 0
    for ii in xrange(len(set_id_set)):

        tmp = f_stats.get('ff_%s' % set_id_set[ii])[...]
        ff = tmp.reshape(ns_set[ii], n_corr*el**3)

        allcorr[c:c+ns_set[ii], ...] = ff

        c += ns_set[ii]

    msg = "correlations combined"
    rr.WP(msg, wrt_file)

    corr_tmp = allcorr[...]
    # subtract out the mean feature values from corr_tmp
    corr_mean = np.mean(corr_tmp, 0)[None, :]
    corr_tmp = corr_tmp-corr_mean

    n_samp = corr_tmp.shape[0]

    # pca = PCA(n_components=20)
    # pca.fit(corr_tmp)
    # ratios = np.round(100*pca.explained_variance_ratio_, 1)
    # msg = "pca explained variance: %s%%" % str(ratios)
    # rr.WP(msg, wrt_file)

    # pca = TruncatedSVD(n_components=20)
    # pca.fit(corr_tmp)
    # ratios = np.round(100*pca.explained_variance_ratio_, 1)
    # msg = "pca explained variance: %s%%" % str(ratios)
    # rr.WP(msg, wrt_file)

    # print "corr_tmp.shape: %s" % str(corr_tmp.shape)
    # print "corr_mean.shape: %s" % str(corr_mean.shape)

    U, S, V = svd(corr_tmp, 20)
    print "V.shape: %s" % str(V.shape)
    f_master.create_dataset('corr_mean', data=corr_mean)
    f_master.create_dataset('U', data=U)
    f_master.create_dataset('S', data=S)
    f_master.create_dataset('V', data=V)

    # """check variance after whitening"""
    # V_norm = V/(S[None, :]*np.sqrt(n_samp))
    # corr_tmp_wht = np.dot(corr_tmp, V_norm)
    # tmp_var = np.var(corr_tmp_wht, axis=0)
    # print "variance for each pc axis: %s" % str(tmp_var)

    """calculate percentage explained variance"""
    # X_transformed = np.dot(U, np.diag(S))
    # exp_var = np.var(X_transformed, axis=0)
    exp_var = (S**2)/n_samp
    # full_var = np.var(corr_tmp, axis=0).sum()
    full_var = exp_var.sum()
    ratios = np.round(100*(exp_var/full_var), 1)
    print ratios.sum()
    msg = "pca explained variance: %s%%" % str(ratios)
    rr.WP(msg, wrt_file)
    f_master.create_dataset('ratios', data=ratios)

    f_master.close()

    msg = "PCA completed: %ss" % np.round(time.time()-st, 5)
    rr.WP(msg, wrt_file)


if __name__ == '__main__':
    el = 21
    H = 15
    ns_set = [10, 10, 10]
    set_id_set = ['random', 'transverse', 'basaltrans']
    step = 0
    wrt_file = 'test.txt'

    reduce(el, H, ns_set, set_id_set, step, wrt_file)
