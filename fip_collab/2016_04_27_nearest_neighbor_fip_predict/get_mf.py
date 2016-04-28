# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:45:46 2014

@author: nhpnp3
"""

import numpy as np
import hex_0_16_real as gsh
import functions as rr
import time
import h5py


def get_mf(el, H, ns, set_id, step, wrt_file):

    st = time.time()

    """get the euler angle files"""
    f = h5py.File("spatial.hdf5", 'a')
    euler = f.get('euler_%s' % set_id)[...]

    mf = np.zeros([ns, H, el**3], dtype='float64')
    for h in xrange(H):
        tmp = gsh.gsh_eval(euler.swapaxes(1, 2), [h])
        tmp = np.squeeze(tmp)
        mf[:, h, :] = tmp  # 2*l+1 included in maple generator

    f.create_dataset('mf_%s' % set_id, data=mf)
    f.close()

    end = time.time()
    timeE = np.round((end - st), 3)

    msg = "Conversion from Euler angles to GSH coefficients completed:" + \
          " %s seconds" % timeE
    rr.WP(msg, wrt_file)
