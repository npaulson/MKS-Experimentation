import functions as rr
import numpy as np
from constants import const
import time
import h5py


def transform(ns, sid, pca):

    st = time.time()

    C = const()

    n_corr = C['cmax']

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'a')
    f_stats = h5py.File("spatial_L%s.hdf5" % C['H'], 'r')

    ff = f_stats.get('ff_%s' % sid)[...]
    ff = ff.reshape(ns, n_corr*C['vmax']**3)

    rawdata = pca.transform(ff)

    """split into two clusters"""

    varset = np.var(rawdata, axis=0)

    I_seed1 = np.argmin(rawdata[:, np.argmax(varset)])

    seed1 = rawdata[I_seed1, :]

    dist = np.zeros((ns,))
    for ii in xrange(ns):
        point = rawdata[ii, :]
        dist[ii] = np.sqrt(np.sum((seed1-point)**2))

    n_pts_hlf = np.floor(ns/2.)

    I_sort = np.argsort(dist)
    set1 = rawdata[I_sort[:n_pts_hlf], :]
    set2 = rawdata[I_sort[n_pts_hlf:], :]

    """save the clusters"""

    f_red.create_dataset('reduced_%sB' % sid,
                         data=set1,
                         dtype='float64')

    f_red.create_dataset('reduced_%sA' % sid,
                         data=set2,
                         dtype='float64')

    f_red.create_dataset('I_sort_%s' % sid,
                         data=I_sort,
                         dtype='int64')

    f_red.close()
    f_stats.close()

    timeE = np.round(time.time()-st, 2)
    msg = "transform to low dimensional space, %s: %s s" % (sid, timeE)
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    ns = 10
    sid = 'random'

    reduce(ns, sid)
