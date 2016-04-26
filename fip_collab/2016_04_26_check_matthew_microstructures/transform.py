import functions as rr
import numpy as np
from sklearn.decomposition import PCA
# from sklearn.decomposition import TruncatedSVD
import time
import h5py


def transform(el, ns, H, set_id, step, pca, wrt_file):

    st = time.time()

    n_corr = H**2

    f_red = h5py.File("sve_reduced.hdf5", 'a')
    f_stats = h5py.File("spatial_stats.hdf5", 'r')
    f_master = h5py.File("sve_reduced_all.hdf5", 'r')
    # V = f_master.get('V')[...]
    corr_mean = f_master.get('corr_mean')[...]

    ff = f_stats.get('ff_%s' % set_id)[...]
    ff = ff.reshape(ns, n_corr*el**3)

    # subtract out the mean feature values
    ff_r = ff
    ff_r = ff_r - corr_mean

    tmp = pca.transform(ff_r)
    # calculate the pc scores for ff_r
    # tmp = np.dot(ff_r, V)

    f_red.create_dataset('reduced_%s' % set_id,
                         data=tmp,
                         dtype='float64')

    f_red.close()
    f_stats.close()
    f_master.close()

    timeE = np.round(time.time()-st, 2)
    msg = "transform to low dimensional space, %s: %s s" % (set_id, timeE)
    rr.WP(msg, wrt_file)


if __name__ == '__main__':
    el = 21
    H = 15
    ns_set = [10, 10, 10]
    set_id_set = ['random', 'transverse', 'basaltrans']
    step = 0
    wrt_file = 'test.txt'

    reduce(el, H, ns_set, set_id_set, step, wrt_file)
