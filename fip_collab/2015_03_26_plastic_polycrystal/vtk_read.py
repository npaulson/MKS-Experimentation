# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 11:32:08 2014

@author: nhpnp3
"""

import functions as rr
import numpy as np
import time
import os
import tables as tb


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

    # return to the original directory
    os.chdir('..')

    # open HDF5 file
    base = tb.open_file("ref_%s%s_s%s.h5" % (ns, set_id, step), mode="a")
    # initialize array for the euler angles
    base.create_array('/msf',
                      'euler',
                      euler,
                      'euler angle of the original microstructures')
    # close the HDF5 file
    base.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'euler angles read from .vtk file for %s: %s seconds' % (set_id,
                                                                   timeE)
    rr.WP(msg, wrt_file)


def read_meas(el, ns, set_id, step, comp, tensor_id, newdir, wrt_file):

    start = time.time()

    typ = ['sigma', 'epsilon', 'epsilon_p']

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

    # return to the original directory
    os.chdir('..')

    # open HDF5 file
    base = tb.open_file("ref_%s%s_s%s.h5" % (ns, set_id, step), mode="a")
    # create a group one level below root called r[comp]
    group = base.create_group('/%s' % typ[tensor_id],
                              'r%s' % comp,
                              'comp %s response fields' % comp)
    # initialize array for the euler angles
    base.create_array(group,
                      'r_fem',
                      r_fem,
                      'FEM generated response fields')
    # close the HDF5 file
    base.close()

    # FFT OF RESPONSE FIELD

    # open HDF5 file
    base = tb.open_file("D_%s%s_s%s.h5" % (ns, set_id, step), mode="a")
    # create a group one level below root called r[comp]
    group = base.create_group('/%s' % typ[tensor_id],
                              'r%s' % comp,
                              'FFTs of comp %s response fields' % comp)
    # initialize array for the euler angles
    base.create_array(group,
                      'r_fft',
                      np.fft.fftn(r_fem, axes=[1, 2, 3]),
                      'FFT of FEM generated response fields')
    # close the HDF5 file
    base.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'The measure of interest has been read from .vtk file' \
          'for %s, set %s: %s seconds' % (set_id, comp, timeE)
    rr.WP(msg, wrt_file)
