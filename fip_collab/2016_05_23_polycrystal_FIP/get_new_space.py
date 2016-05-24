import functions as rr
import numpy as np
from sklearn.decomposition import PCA
# from sklearn.decomposition import TruncatedSVD
from constants import const
import time
import h5py


def new_space(set_id_set):

    st = time.time()

    C = const()

    print "H: %s" % C['H']
    n_corr = C['H']**2

    n_tot = len(set_id_set)

    allcorr = np.zeros((n_tot, n_corr*C['el']**3), dtype='float64')

    f_stats = h5py.File("spatial.hdf5", 'a')

    """here we will treat the real and imaginary parts of ff as
    separate dimensions prior to applying PCA"""

    for ii in xrange(len(set_id_set)):

        tmp = f_stats.get('ff_avg_%s' % set_id_set[ii])[...]
        ff = tmp.reshape(n_corr*C['el']**3)

        allcorr[ii, ...] = ff

    f_stats.close()

    msg = "correlations combined"
    rr.WP(msg, C['wrt_file'])

    f_master = h5py.File("pca_data.hdf5", 'w')

    print allcorr.shape

    """Note that when whiten=True the information about the
    relative variances of the pc vectors. This may be desirable
    when using regression to find a linkage to reduce some
    numerical issues"""
    pca = PCA(n_components=C['n_pc_tot'], whiten=True)
    pca.fit(allcorr)
    ratios = 100*pca.explained_variance_ratio_
    f_master.create_dataset('ratios', data=ratios)
    ratios = np.round(ratios, 1)

    msg = "pca explained variance: %s%%" % str(ratios)
    rr.WP(msg, C['wrt_file'])

    f_master.close()

    msg = "PCA completed: %ss" % np.round(time.time()-st, 5)
    rr.WP(msg, C['wrt_file'])

    return pca


if __name__ == '__main__':
    set_id_set = ['random', 'transverse', 'basaltrans']

    reduce(set_id_set)
