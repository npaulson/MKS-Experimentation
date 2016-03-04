# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:45:46 2014

@author: nhpnp3
"""

import numpy as np
import gsh_hex_tri_L0_20 as gsh
import functions as rr
import time
import h5py


def euler_to_gsh(el, H, ns, set_id, step, wrt_file):

    start = time.time()

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'r')
    euler = f.get('euler')[...]
    f.close()

    euler_GSH = np.zeros([ns, H, el**3], dtype='complex128')

    for sn in xrange(ns):

        tmp = gsh.gsh_eval(euler[sn, ...].swapaxes(0, 1), np.arange(15))
        euler_GSH[sn, :, :] = tmp.swapaxes(0, 1)

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "Conversion from Euler angles to GSH coefficients completed:" + \
          " %s seconds" % timeE
    rr.WP(msg, wrt_file)

    euler_GSH = euler_GSH.reshape([ns, H, el, el, el])

    # MICROSTRUCTURE FUNCTIONS IN FREQUENCY SPACE
    start = time.time()

    M = np.fft.fftn(euler_GSH, axes=[2, 3, 4])
    del euler_GSH

    size = M.nbytes

    f = h5py.File("D_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    f.create_dataset('M', data=M)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "FFT3 conversion of micr to M_%s%s_s%s: %s seconds" % \
          (ns, set_id, step, timeE)
    rr.WP(msg, wrt_file)
    msg = 'Size of M_%s%s_s%s: %s bytes' % (ns, set_id, step, size)
    rr.WP(msg, wrt_file)
