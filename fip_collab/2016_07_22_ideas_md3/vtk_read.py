# -*- coding: utf-8 -*-
import functions as rr
import numpy as np
import h5py
import os


def read_euler(C, strt, ns, set_id, newdir, funit):

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

    f = h5py.File("euler_all.hdf5", 'a')
    dset_name = 'euler_%s' % set_id
    f.create_dataset(dset_name, data=euler)
    f.close()
