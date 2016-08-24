import functions as rr
import numpy as np
from constants import const
import time
import h5py


def transform(ns, set_id, pca):

    st = time.time()

    C = const()

    n_corr = C['cmax']

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'a')
    f_stats = h5py.File("spatial_L%s.hdf5" % C['H'], 'r')

    ff = f_stats.get('ff_%s' % set_id)[...]
    ff = ff.reshape(ns, n_corr*C['vmax']**3)

    tmp = pca.transform(ff)

    f_red.create_dataset('reduced_%s' % set_id,
                         data=tmp,
                         dtype='float64')

    f_red.close()
    f_stats.close()

    timeE = np.round(time.time()-st, 2)
    msg = "transform to low dimensional space, %s: %s s" % (set_id, timeE)
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    ns = 10
    set_id = 'random'

    reduce(ns, set_id)
