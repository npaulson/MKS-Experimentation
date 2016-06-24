import numpy as np
from constants import const
import h5py


def calc(ns_set, set_id_set, typ):

    C = const()

    """find the mean spatial stats for each microstructure"""

    n_tex = len(ns_set)

    corr_mean = np.zeros((n_tex, C['H'], C['H'], C['vmax'], C['vmax'], C['vmax']))

    f = h5py.File("spatial_L%s.hdf5" % C['H'], 'r')
    for ii in xrange(n_tex):
        set_id = set_id_set[ii]
        corr = f.get('ff_%s' % set_id)[...]
        corr_mean[ii, ...] = np.mean(corr, axis=0)
    f.close()

    """get pairwise distance matrix between all microstructures"""

    dist = np.zeros((n_tex, n_tex))
    S = (C['H']**2)*(C['vmax']**3)

    for ii in xrange(n_tex):
        for jj in xrange(ii, n_tex):
            tmp = np.sqrt(np.sum((corr_mean[ii, ...]-corr_mean[jj, ...])**2))/S
            dist[ii, jj] = tmp
            dist[jj, ii] = tmp

    f = h5py.File('dist_L%s.hdf5' % C['H'], 'a')
    f.create_dataset('dist_%s' % typ, data=dist)
    f.close()


if __name__ == '__main__':
    C = const()
    f = h5py.File('dist_L%s.hdf5' % C['H'], 'w')
    f.close()
    calc(C['ns_cal'], C['set_id_cal'], 'cal')
    calc(C['ns_val'], C['set_id_val'], 'val')
