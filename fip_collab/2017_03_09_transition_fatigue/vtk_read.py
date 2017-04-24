# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 11:32:08 2014

@author: nhpnp3
"""

import functions as rr
import numpy as np
from constants import const
import time
import os
import h5py


def read_euler(strt, ns, sid, funit):

    start = time.time()

    C = const()

    # nwd = os.getcwd() + '\\' + sid
    nwd = os.getcwd() + '/' + sid  # for unix
    os.chdir(nwd)

    """get list of files in directory"""
    flist = np.array(os.listdir(nwd))
    euler = np.zeros([ns, 3, C['el']**3], dtype='float64')
    ii = 0

    for filename in flist[strt:strt+ns]:
        euler[ii, :, :] = rr.read_vtk_vector(filename=filename)
        ii += 1

    if funit == 1:
        euler = euler * (np.pi/180.)

    """return to the original directory"""
    os.chdir('..')

    f = h5py.File("euler.hdf5", 'a')
    f.create_dataset('euler_%s' % sid, data=euler)
    f.create_dataset('flist_%s' % sid, data=flist)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'euler angles read from .vtk file for %s: %s seconds' \
          % (sid, timeE)
    rr.WP(msg, C['wrt_file'])


def read_fip(strt, ns, sid):

    start = time.time()

    C = const()

    # nwd = os.getcwd() + '\\' + sid
    nwd = os.getcwd() + '/' + sid  # for unix
    os.chdir(nwd)

    """get list of files in directory"""
    flist = np.array(os.listdir(nwd))
    fip = np.zeros([ns, C['el']**3])
    ii = 0

    for filename in flist[strt:strt+ns]:
        fip[ii, :] = rr.read_vtk_scalar(filename=filename)
        ii += 1

    """return to the original directory"""
    os.chdir('..')

    f = h5py.File("raw_responses.hdf5", 'a')
    f.create_dataset('fip_%s' % sid, data=fip)
    f.create_dataset('flist_%s' % sid, data=flist)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'fip values read from .vtk file for %s: %s seconds' % (sid,
                                                                 timeE)
    rr.WP(msg, C['wrt_file'])
