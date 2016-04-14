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
    f = h5py.File("spatial.hdf5", 'a')
    euler = f.get('euler_%s' % set_id)[...]

    indxvec = gsh.gsh_basis_info()

    mf = np.zeros([ns, H, el**3], dtype='complex128')
    for h in xrange(H):
        tmp = gsh.gsh_eval(euler.swapaxes(1, 2), [h])
        tmp = np.squeeze(tmp)
        mf[:, h, :] = (2*indxvec[h, 0]+1)*tmp.conj()

    end = time.time()
    timeE = np.round((end - start), 3)

    f.create_dataset('mf_%s' % set_id, data=mf)
    f.close()

    msg = "Conversion from Euler angles to GSH coefficients completed:" + \
          " %s seconds" % timeE
    rr.WP(msg, wrt_file)
