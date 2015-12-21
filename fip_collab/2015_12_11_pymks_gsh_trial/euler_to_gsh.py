# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:45:46 2014

@author: nhpnp3
"""

import numpy as np
import gsh_hex_tri_L0_4_alt as gsh
import pickle
import functions as rr
import time
import tables as tb


def euler_to_gsh(X, el, H, ns, set_id, wrt_file):

    start = time.time()

    X_GSH = np.zeros([ns, el, el, el, H], dtype='complex128')

    for sn in xrange(ns):
        X_GSH[sn, ...] = gsh.gsh_eval(X[sn, ...], np.arange(H))

    print X_GSH.shape
    pickle.dump(X_GSH, open('X_GSH_%s_NP.pkl' % set_id,'w'))

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "Conversion from Euler angles to GSH coefficients completed:" + \
          " %s seconds" % timeE
    rr.WP(msg, wrt_file)

    # MICROSTRUCTURE FUNCTIONS IN FREQUENCY SPACE
    start = time.time()

    M = np.fft.fftn(X_GSH, axes=[1, 2, 3])
    del X_GSH

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "FFT3 conversion of micr to M_%s%s: %s seconds" % \
          (ns, set_id, timeE)
    rr.WP(msg, wrt_file)

    msg = 'Size of M_%s%s: %s Gb' % (ns, set_id, M.nbytes/(1E9))
    rr.WP(msg, wrt_file)

    return M