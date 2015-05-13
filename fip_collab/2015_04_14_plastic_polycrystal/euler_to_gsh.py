# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:45:46 2014

@author: nhpnp3
"""

import numpy as np
import GSH_func_L6 as gsh
import functions as rr
import time
import tables as tb


def euler_to_gsh(el, H, ns, set_id, step, wrt_file):

    start = time.time()

    # open HDF5 file
    base = tb.open_file("ref_%s%s_s%s.h5" % (ns, set_id, step), mode="r")
    euler = base.root.msf.euler[...]
    # close the HDF5 file
    base.close()

    euler_GSH = np.zeros([ns, H, el**3], dtype='complex128')

    for sn in xrange(ns):
        euler_GSH[sn, :, :] = gsh.gsh(euler[sn, :, :])

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

    # open HDF5 file
    base = tb.open_file("D_%s%s_s%s.h5" % (ns, set_id, step), mode="a")
    # initialize array for the euler angles
    base.create_array('/msf',
                      'M',
                      M,
                      'FFT of GSH microstructure function')
    # close the HDF5 file
    base.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "FFT3 conversion of micr to M_%s%s_s%s: %s seconds" % \
          (ns, set_id, step, timeE)
    rr.WP(msg, wrt_file)
    msg = 'Size of M_%s%s_s%s: %s bytes' % (ns, set_id, step, size)
    rr.WP(msg, wrt_file)
