import numpy as np
from constants import const
from sklearn.decomposition import PCA
import h5py
import sys


def sample(ns, sid, pc, n_samp):

    C = const()

    f1 = h5py.File("raw_responses.hdf5", 'r')
    allfip = f1.get('fip_%s' % sid)[...]
    f1.close()

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'r')
    reduced = f_red.get('reduced_%s' % sid)[...]
    f_red.close()

    """perform PCA on the SVE cluster to identify its extreme boundaries"""

    pca = PCA()
    pca.fit(reduced)
    reduced_ = pca.transform(reduced)

    """pick points at the maximum and minimum extremes of the SVE cluster
    for each PC up to the specified level"""

    f2 = h5py.File("sample_rve.hdf5", 'a')

    """find the index of the minimum cluster bound
    in the new PC space"""
    I_seed1 = np.argmin(reduced_[:, pc])
    """find the index of the maximum cluster bound
    in the new PC space"""
    I_seed2 = np.argmax(reduced_[:, pc])

    """get seed1 in the original PC space"""
    seed1 = reduced[I_seed1, :]
    """get seed2 in the original PC space"""
    seed2 = reduced[I_seed2, :]

    """find the closest n_samp points to seed1"""
    dist = np.zeros((ns,))
    for ii in xrange(ns):
        point = reduced[ii, :]
        dist[ii] = np.sqrt(np.sum((seed1-point)**2))
        # dist[ii] = np.sqrt(np.sum((seed1[:2]-point[:2])**2))

    I_sort = np.argsort(dist)
    samp1 = reduced[I_sort[:n_samp], :]
    fip1 = allfip[I_sort[:n_samp], :]

    """find the closest n_samp points to seed2"""
    dist = np.zeros((ns,))
    for ii in xrange(ns):
        point = reduced[ii, :]
        dist[ii] = np.sqrt(np.sum((seed2-point)**2))
        # dist[ii] = np.sqrt(np.sum((seed2[:2]-point[:2])**2))

    I_sort = np.argsort(dist)
    samp2 = reduced[I_sort[:n_samp], :]
    fip2 = allfip[I_sort[:n_samp], :]

    f2.create_dataset('samp1', data=samp1)
    f2.create_dataset('samp2', data=samp2)
    f2.create_dataset('fip1', data=fip1)
    f2.create_dataset('fip2', data=fip2)

    f2.close()


if __name__ == '__main__':
    C = const()

    ns = np.int64(sys.argv[1])
    sid = sys.argv[2]
    pc = np.int64(sys.argv[3])
    n_samp = np.int64(sys.argv[4])

    f2 = h5py.File("sample_rve.hdf5", 'w')
    f2.close()

    sample(ns, sid, pc, n_samp)
