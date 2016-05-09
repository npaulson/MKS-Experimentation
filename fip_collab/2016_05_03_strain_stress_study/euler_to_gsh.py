# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:45:46 2014

@author: nhpnp3
"""

import numpy as np
import gsh_hex_tri_L0_16 as gsh
import functions as rr
import h5py
import time


def euler_to_gsh(el, H, ns, set_id, step, wrt_file):

    start = time.time()

    f = h5py.File("data.hdf5", 'a')
    dset_name = 'euler_%s%s_s%s' % (ns, set_id, step)
    euler = f.get(dset_name)[...]
    euler = euler.swapaxes(1, 2)

    euler_GSH = np.zeros([ns, H, el**3], dtype='complex128')

    for sn in range(ns):

        tmp = gsh.gsh_eval(euler[sn, :, :], np.arange(H))
        euler_GSH[sn, :, :] = tmp.T

    dset_name = 'euler_GSH_%s%s_s%s.npy' % (ns, set_id, step)
    f.create_dataset(dset_name, data=euler_GSH)

    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "Conversion from Euler angles to GSH coefficients completed:"\
          " %s seconds" % timeE
    rr.WP(msg, wrt_file)
