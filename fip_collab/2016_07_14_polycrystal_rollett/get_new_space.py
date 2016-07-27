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

    n_corr = C['cmax']

    ns_tot = len(set_id_set)

    allcorr = np.zeros((ns_tot, n_corr*C['vmax']**3), dtype='float64')

    f_stats = h5py.File("spatial_L%s.hdf5" % C['H'], 'a')

    """here we will treat the real and imaginary parts of ff as
    separate dimensions prior to applying PCA"""

    for ii in xrange(ns_tot):

        tmp = f_stats.get('ff_%s' % set_id_set[ii])[...]
        ff = tmp.reshape(n_corr*C['vmax']**3)

        allcorr[ii, ...] = ff

    f_stats.close()

    msg = "correlations combined"
    rr.WP(msg, C['wrt_file'])

    f_master = h5py.File("pca_data_L%s.hdf5" % C['H'], 'w')

    """Note that when whiten=True the information about the
    relative variances of the pc vectors. This may be desirable
    when using regression to find a linkage to reduce some
    numerical issues"""
    pca = PCA(n_components=C['n_pc_tot'])
    pca.fit(allcorr)

    f_master.create_dataset('components', data=pca.components_)
    f_master.create_dataset('mean', data=pca.mean_)

    ratios = 100*pca.explained_variance_ratio_
    f_master.create_dataset('ratios', data=ratios)
    f_ratios = h5py.File('ratios_L%s.hdf5' % C['H'], 'w')
    f_ratios.create_dataset('ratios', data=ratios)
    f_ratios.close()

    ratios = np.round(ratios, 1)

    msg = "pca explained variance: %s%%" % str(ratios)
    rr.WP(msg, C['wrt_file'])

    f_master.close()

    msg = "PCA completed: %ss" % np.round(time.time()-st, 5)
    rr.WP(msg, C['wrt_file'])

    return pca


if __name__ == '__main__':
    ns_set = [10, 10, 10]
    set_id_set = ['random', 'transverse', 'basaltrans']

    reduce(set_id_set)
