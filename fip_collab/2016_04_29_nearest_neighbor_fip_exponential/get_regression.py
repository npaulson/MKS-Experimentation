import numpy as np
import functions as rr
from constants import const
import h5py
import time


def regress(ns, set_id):

    st = time.time()

    C = const()

    """load the feature data"""
    f = h5py.File("pre_regress_%s.hdf5" % set_id, 'r')
    X = f.get('X')[...]
    f.close()

    """load the dependent variable data"""
    f = h5py.File("responses.hdf5", 'r')
    fip = f.get('fip_%s' % set_id)[...]
    fip = fip.reshape((C['n_samp']))
    f.close()

    """combine the parallel results to get XhX"""
    XhX = np.zeros((C['xmax'], C['xmax']), dtype='float64')

    for tnum in xrange(C['XhX_njobs']):
        f = h5py.File("XhX_%s.hdf5" % str(tnum).zfill(5), 'r')
        XhXvec = f.get('XhXvec')[...]
        f.close()

        for c in xrange(XhXvec.shape[0]):
            ii, jj, dotvec = XhXvec[c, :]
            ii = np.int64(ii)
            jj = np.int64(jj)
            # print ii, jj, dotvec

            if ii == jj:
                XhX[ii, ii] = dotvec
            else:
                XhX[ii, jj] = dotvec
                XhX[jj, ii] = dotvec

    f = h5py.File("XhX_total.hdf5", 'w')
    f.create_dataset('XhX', data=XhX)
    f.close()

    rank = np.linalg.matrix_rank(XhX)
    if rank != C['xmax']:

        msg = "WARNING: XhX is rank deficient"
        rr.WP(msg, C['wrt_file'])
        msg = "xmax: %s" % C['xmax']
        rr.WP(msg, C['wrt_file'])
        msg = "rank(XhX): %s" % rank
        rr.WP(msg, C['wrt_file'])

    """calculate XhY"""

    XhY = np.zeros(C['xmax'], dtype='float64')

    for ii in xrange(C['xmax']):
        XhY[ii] = np.dot(X[:, ii], np.log(fip))

    """perform the regression"""
    coef = np.linalg.lstsq(XhX, XhY)[0]

    f = h5py.File("regress_results.hdf5", 'w')
    f.create_dataset('coef', data=coef)
    f.close()

    timeE = np.round(time.time()-st, 1)
    msg = "regressions completed: %s s" % timeE
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    el = 21
    ns = 2
    H = 9
    ext = 3
    set_id = "cal"
    wrt_file = "test.txt"

    regress(el, ns, H, ext, set_id, wrt_file)
