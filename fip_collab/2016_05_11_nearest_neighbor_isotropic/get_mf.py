# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:45:46 2014

@author: nhpnp3
"""

import numpy as np
import functions as rr
from constants import const
import time
import h5py


def get_mf(ns, set_id):

    st = time.time()

    C = const()

    """get the microstructure files"""
    f = h5py.File("spatial.hdf5", 'a')
    micr = f.get('micr_%s' % set_id)[...]

    mf = np.zeros([ns, C['H'], C['el']**3], dtype='int16')
    for h in xrange(C['H']):
        mf[:, h, :] = micr == h

    f.create_dataset('mf_%s' % set_id, data=mf)
    f.close()

    end = time.time()
    timeE = np.round((end - st), 3)

    msg = "mf calculated: %s seconds" % timeE
    rr.WP(msg, C['wrt_file'])
