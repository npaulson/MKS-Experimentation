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


def read(ns, strt, set_id, newdir):

    start = time.time()

    C = const()

    tmp = np.loadtxt("micr.txt", dtype='int16', delimiter=',').T
    micr = tmp[strt:strt+ns, :]

    f = h5py.File("spatial.hdf5", 'a')
    f.create_dataset('micr_%s' % set_id, data=micr)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'microstructures read from .txt file for %s: %s seconds' % (set_id,
                                                                      timeE)
    rr.WP(msg, C['wrt_file'])
