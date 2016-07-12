# -*- coding: utf-8 -*-

import functions as rr
import numpy as np
from constants import const
import h5py
import time
import os


def read_euler(set_id, newdir):

    start = time.time()

    C = const()

    """in euler the first 3 columns are for euler angles,
    the last is for the phase id"""
    """phase id 1 is for beta phase, phase id 2 is for alpha phase"""
    euler = np.zeros([C['el']**3, 4])

    # nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    """read the euler angle file"""
    tmp = np.loadtxt('%s.txt' % set_id)
    euler[:, :3] = tmp[:, :3]*(np.pi/180.)
    euler[:, 3] = tmp[:, 7]

    # return to the original directory
    os.chdir('..')

    f = h5py.File("spatial_L%s.hdf5" % C['H'], 'a')
    dset_name = 'euler_%s' % set_id
    f.create_dataset(dset_name, data=euler)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'euler angles read from file for %s: %s seconds' \
          % (set_id, timeE)
    rr.WP(msg, C['wrt_file'])
