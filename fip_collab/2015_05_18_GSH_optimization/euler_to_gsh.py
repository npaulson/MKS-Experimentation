# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:45:46 2014

@author: nhpnp3
"""

import numpy as np
import gsh_hex_tri_L0_8 as gsh
import functions as rr
import time
import tables as tb


def euler_to_gsh(el, Hset, ns, set_id, step, wrt_file):

    start = time.time()

    # open HDF5 file
    base = tb.open_file("ref_%s%s_s%s.h5" % (ns, set_id, step), mode="r")
    euler = base.root.msf.euler[...]
    # close the HDF5 file
    base.close()

    # euler_GSH = np.zeros([ns, Hset.size, el**3], dtype='complex128')
    euler_GSH = np.zeros([ns, Hset.size, el**3], dtype='float64')

    for sn in xrange(ns):
        tmp = gsh.gsh(euler[sn, :, :])

        # euler_GSH[sn, ...] = tmp[Hset, :]

        tmp2 = np.zeros([90, el**3], dtype='float64')
        # L = 0 - 2
        tmp2[0:4, :] = np.real(tmp[0:4, :])
        tmp2[4:6, :] = np.imag(tmp[4:6, :])
        # L = 4
        tmp2[6:11, :] = np.real(tmp[6:11, :])
        tmp2[11:15, :] = np.imag(tmp[11:15, :])
        # L = 6
        tmp2[15:29, :] = np.real(tmp[15:29, :])
        tmp2[29:41, :] = np.imag(tmp[29:41, :])
        # L = 7
        tmp2[41:49, :] = np.real(tmp[41:49, :])
        tmp2[49:56, :] = np.imag(tmp[49:56, :])
        # L = 8
        tmp2[56:74, :] = np.real(tmp[56:74, :])
        tmp2[74:90, :] = np.imag(tmp[74:90, :])

        # if sn == 0:
        #     print(tmp[:, 0])
        #     # print(tmp2[:, 0])

        del tmp
        euler_GSH[sn, ...] = tmp2[Hset, :]

        # if sn == 0:
        #     print(euler_GSH[sn, :, 0])

        del tmp2

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "Conversion from Euler angles to GSH coefficients completed:" + \
          " %s seconds" % timeE
    rr.WP(msg, wrt_file)

    euler_GSH = euler_GSH.reshape([ns, Hset.size, el, el, el])

    # MICROSTRUCTURE FUNCTIONS IN FREQUENCY SPACE
    start = time.time()

    M = np.fft.fftn(euler_GSH, axes=[2, 3, 4])
    del euler_GSH

    size = M.nbytes

    # open HDF5 file
    base = tb.open_file("gsh_try_%s%s_s%s.h5" % (ns, set_id, step),
                        mode="a")
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
