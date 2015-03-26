# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 11:32:08 2014

@author: nhpnp3
"""

import functions as rr
import numpy as np
import time
import os
import vtk
import tables as tb


def read_vtk(filename, tensor_id, retsig):
    """
    Summary:
        Much of this code was taken from Matthew Priddy's example
        file.
    Inputs:
    Outputs:
    """

    # Initialize the reading of the VTK microstructure created by Dream3D
    reader = vtk.vtkDataSetReader()
    reader.SetFileName(filename)
    reader.ReadAllTensorsOn()
    reader.ReadAllVectorsOn()
    reader.ReadAllScalarsOn()
    reader.Update()
    data = reader.GetOutput()
    dim = data.GetDimensions()
    vec = list(dim)
    vec = [i-1 for i in dim]

    el = vec[0]

    # if meas == 0, we read the stress tensor
    # if meas == 1, we read the strain tensor
    # if meas == 2, we read the plastic strain tensor

    meas = data.GetCellData().GetArray(reader.GetTensorsNameInFile(1))
    epsilon = np.zeros([6, el**3])

    for ii in xrange(el**3):
        epsilon[0, ii] = meas.GetValue(ii*9 + 0)
        epsilon[1, ii] = meas.GetValue(ii*9 + 4)
        epsilon[2, ii] = meas.GetValue(ii*9 + 8)
        epsilon[3, ii] = meas.GetValue(ii*9 + 5)
        epsilon[4, ii] = meas.GetValue(ii*9 + 6)
        epsilon[5, ii] = meas.GetValue(ii*9 + 1)

    euler = data.GetCellData().GetArray(reader.GetVectorsNameInFile(0))

    euler_py = np.zeros([3, el**3])

    for ii in xrange(el**3):
        euler_py[0, ii] = euler.GetValue(ii*3 + 0)
        euler_py[1, ii] = euler.GetValue(ii*3 + 1)
        euler_py[2, ii] = euler.GetValue(ii*3 + 2)

    if retsig == 1:

        meas = data.GetCellData().GetArray(reader.GetTensorsNameInFile(0))
        sigma = np.zeros([6, el**3])

        for ii in xrange(el**3):
            sigma[0, ii] = meas.GetValue(ii*9 + 0)
            sigma[1, ii] = meas.GetValue(ii*9 + 4)
            sigma[2, ii] = meas.GetValue(ii*9 + 8)
            sigma[3, ii] = meas.GetValue(ii*9 + 5)
            sigma[4, ii] = meas.GetValue(ii*9 + 6)
            sigma[5, ii] = meas.GetValue(ii*9 + 1)

        return [euler_py, epsilon, sigma]

    else:

        return [euler_py, epsilon]


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

#    nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    compd = {'11': 0, '22': 4, '33': 8, '23': 5, '13': 6, '12': 1}
    compp = compd[comp]

    r_fem = np.zeros([ns, el, el, el])

    sn = 0
    for filename in os.listdir(nwd):
        if filename.endswith('%s.vtk' % step):
            r_temp = rr.read_vtk_tensor(filename=filename, tensor_id=tensor_id,
                                        comp=compp)
            r_fem[sn, ...] = r_temp.reshape([el, el, el])
            sn += 1

    # return to the original directory
    os.chdir('..')

    # open HDF5 file
    base = tb.open_file("ref_%s%s_s%s.h5" % (ns, set_id, step), mode="a")
    # create a group one level below root called r[comp]
    group = base.create_group('/',
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
    group = base.create_group('/',
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

    msg = 'The measure of interest has been read from .vtk file for %s, set %s: %s seconds' % (set_id, comp, timeE)
    rr.WP(msg, wrt_file)
