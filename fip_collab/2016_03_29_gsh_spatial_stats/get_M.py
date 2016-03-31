# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:45:46 2014

@author: nhpnp3
"""

import numpy as np
import gsh_hex_tri_L0_16 as gsh
import functions as rr
import time
import h5py


def get_M(el, H, ns, set_id, step, wrt_file):

    start = time.time()

    """get the euler angle files"""
    f = h5py.File("spatial_stats.hdf5", 'a')
    euler = f.get('euler_%s' % set_id)[...]

    indxvec = gsh.gsh_basis_info()

    """evaluate the gsh basis functions at the point of interest
    note that we do not keep redundant information due to symmetry in
    the complex arguments"""

    # mf = np.zeros([ns, H, el**3], dtype='float64')
    # for h in xrange(H):
    #     tmp = gsh.gsh_eval(euler.swapaxes(1, 2), [h])
    #     if indxvec[h, 1] >= 0:
    #         tmp = np.squeeze(tmp).real
    #     elif indxvec[h, 1] < 0:
    #         tmp = np.squeeze(tmp).imag
    #     mf[:, h, :] = (2*indxvec[h, 0]+1)*tmp.conj()

    mf = np.zeros([ns, H, el**3], dtype='complex128')
    for h in xrange(H):
        tmp = gsh.gsh_eval(euler.swapaxes(1, 2), [h])
        tmp = np.squeeze(tmp)
        mf[:, h, :] = (2*indxvec[h, 0]+1)*tmp.conj()

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

    size = M.nbytes

    f.create_dataset('M_%s' % set_id, data=M)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "FFT3 conversion of micr to M_%s%s_s%s: %s seconds" % \
          (ns, set_id, step, timeE)
    rr.WP(msg, wrt_file)
    msg = 'Size of M_%s%s_s%s: %s bytes' % (ns, set_id, step, size)
    rr.WP(msg, wrt_file)
