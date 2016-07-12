# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:45:46 2014

@author: nhpnp3
"""

import numpy as np
import cub_0_6_real as gsh_c
import hex_0_6_real as gsh_h
import functions as rr
from constants import const
import time
import h5py


def get_M(set_id):

    start = time.time()

    C = const()

    """get the euler angle files"""
    f = h5py.File("spatial_L%s.hdf5" % C['H'], 'a')
    euler = f.get('euler_%s' % set_id)[...]

    mf = np.zeros([C['H'], C['el']**3], dtype='float64')

    indxvec_c = gsh_c.gsh_basis_info()
    indxvec_h = gsh_c.gsh_basis_info()

    """calculate the microstructure coefficients for the cubic cells"""
    vec_c = euler[:, 3] == 1
    euler_c = euler[vec_c, :3]

    c = 0
    for h in xrange(C['H_cub']):
        tmp = gsh_c.gsh_eval(euler_c, [h])
        tmp = np.squeeze(tmp)
        mf[c, vec_c] = tmp.real/(2.*indxvec_c[h, 0]+1.)
        c += 1

    del vec_c, euler_c

    """calculate the microstructure coefficients for the hexagonal cells"""
    vec_h = euler[:, 3] == 2
    euler_h = euler[vec_h, :3]

    for h in xrange(C['H_hex']):
        tmp = gsh_h.gsh_eval(euler_h, [h])
        tmp = np.squeeze(tmp)
        mf[c, vec_h] = tmp.real/(2.*indxvec_h[h, 0]+1.)
        c += 1

    del vec_h, euler_h

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "Conversion from Euler angles to GSH coefficients completed:" + \
          " %s seconds" % timeE
    rr.WP(msg, C['wrt_file'])

    mf = mf.reshape([C['H'], C['el'], C['el'], C['el']])

    # MICROSTRUCTURE FUNCTIONS IN FREQUENCY SPACE
    start = time.time()

    M = np.fft.fftn(mf, axes=[1, 2, 3])
    del mf

    f.create_dataset('M_%s' % set_id, data=M)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "FFT3 conversion of mf to M for %s: %s seconds" % \
          (set_id, timeE)
    rr.WP(msg, C['wrt_file'])
    msg = 'Size of M: %s gb' % str(M.nbytes/(1e9))
    rr.WP(msg, C['wrt_file'])
