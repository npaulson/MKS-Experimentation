import functions as rr
import numpy as np
# from sklearn.decomposition import PCA
from constants import const
import time
import h5py


def transform(set_id, pca):

    st = time.time()

    C = const()

    n_corr = C['H']**2

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'a')
    f_stats = h5py.File("spatial_L%s.hdf5" % C['H'], 'r')

    ff = f_stats.get('ff_%s' % set_id)[...]
    ff = ff.reshape(n_corr*C['vmax']**3)

    ff_red = pca.transform(ff)

    f_red.create_dataset('reduced_%s' % set_id,
                         data=ff_red,
                         dtype='float64')

    f_red.close()
    f_stats.close()

    """calculate the error incurred in the PCA representation"""
    ff_ = pca.inverse_transform(ff_red)

    err = np.sqrt(np.sum((ff-ff_)**2))/ff.size
    msg = "PCA representation error for %s: %s" % (set_id, err)
    rr.WP(msg, C['wrt_file'])

    timeE = np.round(time.time()-st, 2)
    msg = "transform to low dimensional space, %s: %s s" % (set_id, timeE)
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    ns = 10
    set_id = 'random'

    reduce(ns, set_id)
