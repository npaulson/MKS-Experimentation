# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 11:32:08 2014

@author: nhpnp3
"""

import functions as rr
import numpy as np
import time
import os
import h5py


def read_euler(el, ns, set_id, newdir, wrt_file, funit):

    start = time.time()

    euler = np.zeros([ns, 3, el**3])

#    nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    sn = 0
    for sn in np.arange(ns):
        fname = "trial_GrainID_%s.txt" % str(sn+1)
        tmp = np.loadtxt(fname)[:, 1:]
        euler[sn, :, :] = tmp.T
        sn += 1

    if funit == 1:
        euler = euler * (np.pi/180.)

    """return to the original directory"""
    os.chdir('..')

    f = h5py.File("spatial_stats.hdf5", 'a')
    f.create_dataset('euler_%s' % set_id, data=euler)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'euler angles read from .txt file for %s: %s seconds' % (set_id,
                                                                   timeE)
    rr.WP(msg, wrt_file)
