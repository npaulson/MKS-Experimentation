# -*- coding: utf-8 -*-

import functions as rr
import numpy as np
import h5py
import time
import os


def read_euler(el, ns, set_id, step, newdir, wrt_file, funit):

    start = time.time()

    euler = np.zeros([ns, 3, el**3])

    # nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    sn = 0

    # for filename in os.listdir(nwd):
    #     if filename.endswith('%s.vtk' % step):
    #         euler[sn, :, :] = rr.read_vtk_vector(filename=filename)
    #         sn += 1

    for sn in xrange(ns):
        filename = "Ti64_Dream3D_v01_Output_%s.vtk" % str(sn+1)
        euler[sn, :, :] = rr.read_vtk_vector(filename=filename)

    if funit == 1:
        euler = euler * (np.pi/180.)

    # return to the original directory
    os.chdir('..')

    f = h5py.File("data.hdf5", 'a')
    dset_name = 'euler_%s%s_s%s' % (ns, set_id, step)
    f.create_dataset(dset_name, data=euler)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'euler angles read from .vtk file for %s: %s seconds' \
          % (set_id, timeE)
    rr.WP(msg, wrt_file)


def read_meas(el, ns, set_id, step, comp, tensor_id, newdir, wrt_file):

    start = time.time()

    # nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    compd = {'11': 0, '22': 4, '33': 8, '23': 5, '12': 1, '13': 6}
    compp = compd[comp]

    r_real = np.zeros([ns, el, el, el])

    sn = 0

    # for filename in os.listdir(nwd):
    #     if filename.endswith('%s.vtk' % step):
    #         r_temp = rr.read_vtk_tensor(filename=filename,
    #                                     tensor_id=tensor_id,
    #                                     comp=compp)
    #         r_real[sn, ...] = r_temp.reshape([el, el, el])
    #         sn += 1

    for sn in xrange(ns):
        filename = "Ti64_Dream3D_v01_Output_%s.vtk" % str(sn+1)
        r_temp = rr.read_vtk_tensor(filename=filename,
                                    tensor_id=tensor_id,
                                    comp=compp)
        r_real[sn, ...] = r_temp.reshape([el, el, el])

    # return to the original directory
    os.chdir('..')

    typ = ['sigma', 'epsilon', 'epsilonp']

    f = h5py.File("data.hdf5", 'a')
    dset_name = '%s%s_fem_%s%s_s%s' % (typ[tensor_id], comp, ns, set_id, step)
    f.create_dataset(dset_name, data=r_real)

    # fftn of response fields
    r_fft = np.fft.fftn(r_real, axes=[1, 2, 3])
    del r_real
    dset_name = '%s%s_fft_fem_%s%s_s%s' % (typ[tensor_id], comp,
                                           ns, set_id, step)
    f.create_dataset(dset_name, data=r_fft)

    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'The measure of interest has been read from .vtk file for %s, component %s: %s seconds' % (set_id, comp, timeE)
    rr.WP(msg, wrt_file)


def read_scalar(el, ns, set_id, step, newdir, wrt_file):

    start = time.time()

    grain = np.zeros([ns, el**3])

    # nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    sn = 0

    # for filename in os.listdir(nwd):
    #     if filename.endswith('%s.vtk' % step):
    #         grain[sn, :] = rr.read_vtk_scalar(filename=filename)
    #         sn += 1

    for sn in xrange(ns):
        filename = "Ti64_Dream3D_v01_Output_%s.vtk" % str(sn+1)
        grain[sn, :] = rr.read_vtk_scalar(filename=filename)

    # return to the original directory
    os.chdir('..')

    f = h5py.File("data.hdf5", 'a')
    dset_name = 'gID_%s%s_s%s' % (ns, set_id, step)
    f.create_dataset(dset_name, data=grain)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'The scalar of interest has been read from .vtk file for %s: %s seconds' % (set_id, timeE)
    rr.WP(msg, wrt_file)
