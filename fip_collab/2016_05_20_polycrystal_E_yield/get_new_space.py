import functions as rr
import numpy as np
from sklearn.decomposition import PCA
# from sklearn.decomposition import TruncatedSVD
from constants import const
import time
import h5py


def new_space(ns_set, set_id_set):

    st = time.time()

    C = const()

    print "H: %s" % C['H']
    n_corr = C['H']**2

    ns_tot = np.sum(ns_set)

    allcorr = np.zeros((ns_tot, n_corr*C['vmax']**3), dtype='float64')

    f_stats = h5py.File("spatial.hdf5", 'a')

    """here we will treat the real and imaginary parts of ff as
    separate dimensions prior to applying PCA"""

    c = 0
    for ii in xrange(len(set_id_set)):

        tmp = f_stats.get('ff_%s' % set_id_set[ii])[...]
        ff = tmp.reshape(ns_set[ii], n_corr*C['vmax']**3)

        allcorr[c:c+ns_set[ii], ...] = ff

        c += ns_set[ii]

    f_stats.close()

    msg = "correlations combined"
    rr.WP(msg, C['wrt_file'])

    f_master = h5py.File("pca_data.hdf5", 'w')

    """Note that when whiten=True the information about the
    relative variances of the pc vectors. This may be desirable
    when using regression to find a linkage to reduce some
    numerical issues"""
    pca = PCA(n_components=C['n_pc_tot'], whiten=True)
    pca.fit(allcorr)
    ratios = np.round(100*pca.explained_variance_ratio_, 1)
    f_master.create_dataset('ratios', data=ratios)
    msg = "pca explained variance: %s%%" % str(ratios)
    rr.WP(msg, C['wrt_file'])

    f_master.close()

    msg = "PCA completed: %ss" % np.round(time.time()-st, 5)
    rr.WP(msg, C['wrt_file'])

    return pca


if __name__ == '__main__':
    ns_set = [10, 10, 10]
    set_id_set = ['random', 'transverse', 'basaltrans']

    reduce(ns_set, set_id_set)
