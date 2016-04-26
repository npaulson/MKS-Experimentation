# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:45:46 2014

@author: nhpnp3
"""

import numpy as np
import hex_0_6_real as gsh
import functions as rr
import time
import h5py


def get_M(el, H, ns, set_id, step, wrt_file):

    start = time.time()

    """get the euler angle files"""
    f = h5py.File("spatial_stats.hdf5", 'a')
    euler = f.get('euler_%s' % set_id)[...]

    mf = np.zeros([ns, H, el**3], dtype='float64')
    for h in xrange(H):
        tmp = gsh.gsh_eval(euler.swapaxes(1, 2), [h])
        tmp = np.squeeze(tmp)
        mf[:, h, :] = tmp
        # mf[:, h, :] = (2*indxvec[h, 0]+1)*tmp # 2*l+1 included in maple generator

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "Conversion from Euler angles to GSH coefficients completed:" + \
          " %s seconds" % timeE
    rr.WP(msg, wrt_file)

    mf = mf.reshape([ns, H, el, el, el])

    # MICROSTRUCTURE FUNCTIONS IN FREQUENCY SPACE
    start = time.time()

    M = np.fft.fftn(mf, axes=[2, 3, 4])
    del mf

    f.create_dataset('M_%s' % set_id, data=M)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "FFT3 conversion of mf to M for %s: %s seconds" % \
          (set_id, timeE)
    rr.WP(msg, wrt_file)
    msg = 'Size of M: %s mb' % str(M.nbytes/(1e6))
    rr.WP(msg, wrt_file)
