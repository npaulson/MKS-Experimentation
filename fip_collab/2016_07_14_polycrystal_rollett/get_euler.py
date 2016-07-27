# -*- coding: utf-8 -*-
import functions as rr
import numpy as np
from constants import const
import h5py
import time
import os
import sys


def read_euler(set_id, newdir):

    start = time.time()

    C = const()

    # nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    # """read the euler angle file"""
    # tmp = np.loadtxt('%s.txt' % set_id)

    # """in euler the first 3 columns are for euler angles,
    # the last is for the phase id"""
    # """phase id 1 is for beta phase, phase id 2 is for alpha phase"""
    # euler = np.zeros([C['el']**3, 4])
    # euler[:, :3] = tmp[:, :3]*(np.pi/180.)
    # euler[:, 3] = tmp[:, 7]
    # euler = euler.reshape([C['el'], C['el'], C['el'], 4])
    # euler = euler.swapaxes(0, 2)
    # euler = euler.reshape([C['el']**3, 4])

    """read the file"""
    """file format: phi1, phi, phi2, x, y, z, grain_id, phase_id"""
    f = open('%s.txt' % set_id, 'r')
    linelist = f.readlines()

    """in euler the first 3 columns are for euler angles,
    the last is for the phase id"""
    """phase id 1 is for beta phase, phase id 2 is for alpha phase"""
    euler = np.zeros([C['el'], C['el'], C['el'], 4])

    for ii in xrange(C['el']**3):
        tmp = np.float32(np.array(linelist[ii].split()))
        i0 = tmp[3]-1
        i1 = tmp[4]-1
        i2 = tmp[5]-1
        euler[i0, i1, i2, :3] = tmp[:3]*(np.pi/180.)
        euler[i0, i1, i2, 3] = tmp[7]

    euler = euler.reshape([C['el']**3, 4])

    os.chdir('..')

    f = h5py.File("euler_%s.hdf5" % set_id, 'w')
    f.create_dataset('euler', data=euler)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'euler angles read from file for %s: %s seconds' \
          % (set_id, timeE)
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    tnum = np.int16(sys.argv[1])
    C = const()
    set_id = C['set_id'][tnum]
    newdir = C['dir_micr']
    read_euler(set_id, newdir)

    f_flag = open("flag%s" % str(tnum).zfill(5), 'w')
    f_flag.close()
