import functions as rr
import numpy as np
# from sklearn.decomposition import PCA
# from sklearn.decomposition import TruncatedSVD
import time
import h5py


def transform(el, ns, H, set_id, step, wrt_file):

    st = time.time()

    f = h5py.File("spatial.hdf5", 'a')
    V = f.get('V')[...]
    raw_mean = f.get('raw_mean')[...]

    neig = f.get('neig_%s' % set_id)[...]
    # subtract out the mean feature values
    neig_r = neig
    neig_r = neig_r - raw_mean
    # tmp = pca.transform(ff_r)
    # calculate the pc scores for ff_r
    tmp = np.dot(neig_r, V)
    f.create_dataset('reduced_%s' % set_id,
                     data=tmp,
                     dtype='complex128')
    # f_red.create_dataset('reduced_%s' % set_id_set[ii],
    #                      data=tmp,
    #                      dtype='float64')

    f.close()

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
