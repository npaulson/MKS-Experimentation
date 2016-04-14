import functions as rr
import numpy as np
# from sklearn.decomposition import PCA
# from sklearn.decomposition import TruncatedSVD
from scipy.linalg.interpolative import svd
import time
import h5py


def new_space(el, ns, H, set_id, step, wrt_file):

    st = time.time()

    f = h5py.File("spatial.hdf5", 'a')

    raw = f.get('neig_%s' % set_id)[...]
    print "shape of raw data: %s" % str(raw.shape)

    # subtract out the mean feature values from corr_tmp
    raw_mean = np.mean(raw, 0)[None, :]
    raw_tmp = raw-raw_mean

    n_samp = raw_tmp.shape[0]

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

    U, S, V = svd(raw_tmp, 100)
    print "V.shape: %s" % str(V.shape)
    f.create_dataset('raw_mean', data=raw_mean)
    f.create_dataset('U', data=U)
    f.create_dataset('S', data=S)
    f.create_dataset('V', data=V)

    print S

    # """check variance after whitening"""
    # V_norm = V/(S[None, :]*np.sqrt(n_samp))
    # corr_tmp_wht = np.dot(corr_tmp, V_norm)
    # tmp_var = np.var(corr_tmp_wht, axis=0)
    # print "variance for each pc axis: %s" % str(tmp_var)

    """calculate percentage explained variance"""
    transform = np.dot(raw_tmp, V)
    exp_var = np.var(transform, axis=0)
    full_var = np.var(raw_tmp, axis=0).sum()
    ratios = np.round(100*(exp_var/full_var), 1)
    print ratios.sum()
    msg = "pca explained variance: %s%%" % str(ratios)
    rr.WP(msg, wrt_file)
    f.create_dataset('ratios', data=ratios)

    f.close()

    msg = "PCA completed: %ss" % np.round(time.time()-st, 5)
    rr.WP(msg, wrt_file)


if __name__ == '__main__':
    el = 21
    H = 15
    ns = 2
    set_id = 'cal'
    step = 0
    wrt_file = 'test.txt'

    reduce(el, H, ns, set_id, step, wrt_file)
