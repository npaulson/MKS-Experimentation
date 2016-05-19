# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 11:32:08 2014

@author: nhpnp3
"""

import functions as rr
import numpy as np
from constants import const
import time
import h5py


def read(ns, set_id):

    start = time.time()

    C = const()

    f = h5py.File('data_%s.hdf5' % set_id, 'r')
    euler_raw = f.get('data')[:, :3]
    euler = euler_raw[..., None]*np.ones((1, 1, C['el']**3))
    msg = 'euler.shape: %s' % str(euler.shape)
    rr.WP(msg, C['wrt_file'])

    # euler = np.zeros([ns, 3, C['el']**3], dtype='float64')

    f = h5py.File("spatial.hdf5", 'a')
    dset_name = 'euler_%s' % set_id
    f.create_dataset(dset_name, data=euler)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'euler angles read for %s: %s seconds' \
          % (set_id, timeE)
    rr.WP(msg, C['wrt_file'])
