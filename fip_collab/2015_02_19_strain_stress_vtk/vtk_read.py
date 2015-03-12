# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 11:32:08 2014

@author: nhpnp3
"""

import functions as rr
import numpy as np
import time
import os


def read_euler(el, ns, set_id, step, newdir, wrt_file, funit):

    start = time.time()

    euler = np.zeros([ns, 3, el**3])

#    nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    sn = 0
    for filename in os.listdir(nwd):
        if filename.endswith('.vtk'):
            euler[sn, :, :] = rr.read_vtk_vector(filename=filename)
            sn += 1

    if funit == 1:
        euler = euler * (np.pi/180.)

    # return to the original directory
    os.chdir('..')

    np.save('euler_%s%s_s%s' % (ns, set_id, step), euler)

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'euler angles read from .vtk file for %s: %s seconds' \
          % (set_id, timeE)
    rr.WP(msg, wrt_file)


def read_meas(el, ns, set_id, step, comp, tensor_id, newdir, wrt_file):

    start = time.time()

#    nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    compd = {'11': 0, '22': 4, '33': 8, '12': 1, '23': 5, '31': 6}
    compp = compd[comp]

    r_real = np.zeros([ns, el, el, el])

    sn = 0
    for filename in os.listdir(nwd):
        if filename.endswith('.vtk'):
            r_temp = rr.read_vtk_tensor(filename=filename, tensor_id=tensor_id,
                                        comp=compp)
            r_real[sn, ...] = r_temp.reshape([el, el, el])
            sn += 1

    # return to the original directory
    os.chdir('..')

    np.save('r%s_%s%s_s%s' % (comp, ns, set_id, step), r_real)

    # fftn of response fields
    r_fft = np.fft.fftn(r_real, axes=[1, 2, 3])
    del r_real
    np.save('r%s_fft_%s%s_s%s' % (comp, ns, set_id, step), r_fft)

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'The measure of interest has been read from .vtk file for %s, set %s: %s seconds' % (set_id, comp, timeE)
    rr.WP(msg, wrt_file)


def read_scalar(el, ns, set_id, step, newdir, wrt_file):

    grain = np.zeros([ns, el**3])

#    nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    sn = 0
    for filename in os.listdir(nwd):
        if filename.endswith('.vtk'):
            grain[sn, :] = rr.read_vtk_scalar(filename=filename)
            sn += 1

    # return to the original directory
    os.chdir('..')

    np.save('gID_%s%s_s%s' % (ns, set_id, step), grain)
