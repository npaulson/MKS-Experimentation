import numpy as np
from sklearn.decomposition import PCA
import h5py


def new_space(C, ns_set, set_id_set):

    n_corr = C['cmax']

    ns_tot = np.sum(ns_set)

    allcorr = np.zeros((ns_tot, n_corr*C['vmax']**3), dtype='float64')

    f_stats = h5py.File("spatial_L%s.hdf5" % C['H'], 'a')

    """here we will treat the real and imaginary parts of ff as
    separate dimensions prior to applying PCA"""

    c = 0
    for ii in xrange(len(set_id_set)):

        tmp = f_stats.get('ff_%s' % set_id_set[ii])[...]
        ff = tmp.reshape(ns_set[ii], n_corr*C['vmax']**3)

        allcorr[c:c+ns_set[ii], ...] = ff

        c += ns_set[ii]

    f_stats.close()

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
    ratios = np.round(ratios, 1)

    f_master.close()

    return pca


if __name__ == '__main__':
    ns_set = [10, 10, 10]
    set_id_set = ['random', 'transverse', 'basaltrans']

    reduce(ns_set, set_id_set)
