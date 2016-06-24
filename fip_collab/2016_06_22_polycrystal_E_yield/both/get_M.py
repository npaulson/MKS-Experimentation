# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:45:46 2014

@author: nhpnp3
"""

import numpy as np
import hex_0_6_real as gsh
import functions as rr
from constants import const
import time
import h5py


def get_M(ns, set_id):

    start = time.time()

    C = const()

    """get the euler angle files"""
    f = h5py.File("spatial_L%s.hdf5" % C['H'], 'a')
    euler = f.get('euler_%s' % set_id)[...]

    mf = np.zeros([ns, C['H'], C['el']**3], dtype='float64')

    indxvec = gsh.gsh_basis_info()

    c = 0
    for h in xrange(C['H']):
        tmp = gsh.gsh_eval(euler.swapaxes(1, 2), [h])
        tmp = np.squeeze(tmp)
        mf[:, c, :] = tmp.real/(2.*indxvec[h, 0]+1.)
        c += 1
        # mf[:, h, :] = (2*indxvec[h, 0]+1)*tmp # 2*l+1 included in maple generator

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "Conversion from Euler angles to GSH coefficients completed:" + \
          " %s seconds" % timeE
    rr.WP(msg, C['wrt_file'])

    mf = mf.reshape([ns, C['H'], C['el'], C['el'], C['el']])

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
    rr.WP(msg, C['wrt_file'])
    msg = 'Size of M: %s gb' % str(M.nbytes/(1e9))
    rr.WP(msg, C['wrt_file'])
