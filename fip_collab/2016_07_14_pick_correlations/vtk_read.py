# -*- coding: utf-8 -*-

import functions as rr
import numpy as np
from constants import const
import h5py
import time
import os


def read_euler(strt, ns, set_id, newdir, funit):

    start = time.time()

    C = const()

    euler = np.zeros([ns, 3, C['el']**3])

    # nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    for ii in xrange(ns):
        sn = strt + ii + 1
        filename = "Ti64_Dream3D_v01_Output_%s.vtk" % sn
        euler[ii, :, :] = rr.read_vtk_vector(filename=filename)

    if funit == 1:
        euler = euler * (np.pi/180.)

    # return to the original directory
    os.chdir('..')

    f = h5py.File("spatial_L%s.hdf5" % C['H'], 'a')
    dset_name = 'euler_%s' % set_id
    f.create_dataset(dset_name, data=euler)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'euler angles read from .vtk file for %s: %s seconds' \
          % (set_id, timeE)
    rr.WP(msg, C['wrt_file'])
