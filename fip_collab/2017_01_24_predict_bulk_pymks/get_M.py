# -*- coding: utf-8 -*-
import numpy as np
import time


def get_M(X):

    start = time.time()

    ns = X.shape[0]
    H = len(np.unique(X))
    el = X.shape[1]

    """compute microstructure function"""

    mf = np.zeros([ns, H, el, el], dtype='float64')

    for h in xrange(H):
        mf[:, h, :] = X == h

    """put microstructure function in frequency space"""
    M = np.fft.fftn(mf, axes=[2, 3])
    del mf

    end = time.time()
    timeE = np.round((end - start), 3)

    print "calculation of microstructure function: %s seconds" % \
          timeE

    return M
