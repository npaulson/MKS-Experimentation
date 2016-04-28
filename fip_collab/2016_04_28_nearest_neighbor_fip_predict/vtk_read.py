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


def read_euler(ns, set_id, newdir, funit):

    start = time.time()

    C = const()

    euler = np.zeros([ns, 3, C['el']**3])

#    nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    sn = 0
    for filename in os.listdir(nwd):
        if filename.endswith('%s.vtk' % C['step']):
            euler[sn, :, :] = rr.read_vtk_vector(filename=filename)
            sn += 1

    if funit == 1:
        euler = euler * (np.pi/180.)

    """return to the original directory"""
    os.chdir('..')

    f = h5py.File("spatial.hdf5", 'a')
    f.create_dataset('euler_%s' % set_id, data=euler)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'euler angles read from .vtk file for %s: %s seconds' % (set_id,
                                                                   timeE)
    rr.WP(msg, C['wrt_file'])


def read_fip(ns, set_id, newdir):

    start = time.time()

    C = const()

    fip = np.zeros([ns, C['el']**3])

#    nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    sn = 0
    for filename in os.listdir(nwd):
        if filename.endswith('%s.vtk' % C['step']):
            fip[sn, :] = rr.read_vtk_scalar(filename=filename)
            sn += 1

    """return to the original directory"""
    os.chdir('..')

    f = h5py.File("responses.hdf5", 'a')
    f.create_dataset('fip_%s' % set_id, data=fip)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'fip values read from .vtk file for %s: %s seconds' % (set_id,
                                                                 timeE)
    rr.WP(msg, C['wrt_file'])


def read_meas(ns, set_id, comp, tensor_id, newdir):

    start = time.time()

    C = const()

    typ = ['sigma', 'epsilon_t', 'epsilon_p']

    # nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    compd = {'11': 0, '22': 4, '33': 8, '12': 1, '13': 6, '23': 5}
    compp = compd[comp]

    r_fem = np.zeros([ns, C['el'], C['el'], C['el']])

    sn = 0
    for filename in os.listdir(nwd):
        if filename.endswith('%s.vtk' % C['step']):
            r_temp = rr.read_vtk_tensor(filename=filename,
                                        tensor_id=tensor_id,
                                        comp=compp)
            r_fem[sn, ...] = r_temp.reshape([C['el'], C['el'], C['el']])
            sn += 1

    """return to the original directory"""
    os.chdir('..')

    f = h5py.File("responses.hdf5", 'a')
    f.create_dataset('%s_%s' % (typ[tensor_id], set_id), data=r_fem)
    f.close()

    # """FFT OF RESPONSE FIELD"""

    # f = h5py.File("D_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    # tmp = np.fft.fftn(r_fem, axes=[1, 2, 3])

    # print tmp.shape

    # f.create_dataset('rfft%s_%s' % (comp, typ[tensor_id]), data=tmp)
    # f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'The measure of interest has been read from .vtk file' \
          ' for %s, component %s, type %s: %s seconds' % (set_id, comp,
                                                          typ[tensor_id],
                                                          timeE)
    rr.WP(msg, C['wrt_file'])
