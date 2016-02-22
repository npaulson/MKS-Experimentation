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


def read_euler(el, ns, set_id, step, newdir, wrt_file, funit):

    start = time.time()

    euler = np.zeros([ns, 3, el**3])

#    nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    sn = 0
    for filename in os.listdir(nwd):
        if filename.endswith('%s.vtk' % step):
            euler[sn, :, :] = rr.read_vtk_vector(filename=filename)
            sn += 1

    if funit == 1:
        euler = euler * (np.pi/180.)

    """return to the original directory"""
    os.chdir('..')

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    f.create_dataset('euler', data=euler)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'euler angles read from .vtk file for %s: %s seconds' % (set_id,
                                                                   timeE)
    rr.WP(msg, wrt_file)


def read_fip(el, ns, set_id, step, newdir, wrt_file):

    start = time.time()

    fip = np.zeros([ns, el**3])

#    nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    sn = 0
    for filename in os.listdir(nwd):
        if filename.endswith('%s.vtk' % step):
            fip[sn, :] = rr.read_vtk_scalar(filename=filename)
            sn += 1

    """return to the original directory"""
    os.chdir('..')

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    f.create_dataset('fip', data=fip)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'fip values read from .vtk file for %s: %s seconds' % (set_id,
                                                                 timeE)
    rr.WP(msg, wrt_file)


def read_meas(el, ns, set_id, step, comp, tensor_id, newdir, wrt_file):

    start = time.time()

    typ = ['sigma', 'epsilon_t', 'epsilon_p']

#    nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    compd = {'11': 0, '22': 4, '33': 8, '12': 1, '13': 6, '23': 5}
    compp = compd[comp]

    r_fem = np.zeros([ns, el, el, el])

    sn = 0
    for filename in os.listdir(nwd):
        if filename.endswith('%s.vtk' % step):
            r_temp = rr.read_vtk_tensor(filename=filename,
                                        tensor_id=tensor_id,
                                        comp=compp)
            r_fem[sn, ...] = r_temp.reshape([el, el, el])
            sn += 1

    """return to the original directory"""
    os.chdir('..')

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    f.create_dataset('r%s_%s' % (comp, typ[tensor_id]), data=r_fem)
    f.close()

    """FFT OF RESPONSE FIELD"""

    f = h5py.File("D_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    tmp = np.fft.fftn(r_fem, axes=[1, 2, 3])

    print tmp.shape

    f.create_dataset('rfft%s_%s' % (comp, typ[tensor_id]), data=tmp)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'The measure of interest has been read from .vtk file' \
          ' for %s, set %s: %s seconds' % (set_id, comp, timeE)
    rr.WP(msg, wrt_file)
