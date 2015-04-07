# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

@author: nhpnp3
"""

import time
import os
import numpy as np
import functions as rr
import tables as tb


def fegrab(el, ns, set_id, direc, wrt_file):

    # FINITE ELEMENT RESPONSES
    st = time.time()

    r_fem_t = np.zeros([ns, el**3])
    r_fem_p = np.zeros([ns, el**3])

    nwd = os.getcwd() + '/' + direc  # for unix
    # nwd = os.getcwd() + '\\' + direc
    os.chdir(nwd)

    for sn in xrange(ns):
        filename = "sq%s_%s%s_%s.dat" % (el, ns, set_id, sn+1)
        r_fem_t[sn, ...], r_fem_p[sn, ...] = res_red(filename, el, sn)

    r_fem_t = r_fem_t.reshape(ns, el, el, el)
    r_fem_p = r_fem_p.reshape(ns, el, el, el)

    os.chdir('..')

    # open HDF5 file
    base = tb.open_file("ref_%s%s.h5" % (ns, set_id), mode="a")
    # create a group one level below root called epsilon
    group = base.create_group("/", 'epsilon', 'total strain field')
    # initialize  array
    base.create_array(group,
                      'r_fem',
                      r_fem_t,
                      'fem response fields')
    # create a group one level below root called epsilon
    group = base.create_group("/", 'epsilon_p', 'plastic strain field')
    # initialize  array
    base.create_array(group,
                      'r_fem',
                      r_fem_p,
                      'fem response fields')

    del r_fem_p

    # close HDF5 file
    base.close()

    msg = 'Load FE results from .dat files for set %s%s: %s seconds' \
        % (ns, set_id, np.round((time.time() - st), 3))
    rr.WP(msg, wrt_file)

    # responses in frequency space
    st = time.time()

    # resp_fft = np.fft.fftn(resp.reshape([ns, el, el, el]), axes=[1, 2, 3])
    resp_fft = np.fft.fftn(r_fem_t, axes=[1, 2, 3])

    del r_fem_t

    # open HDF5 file
    base = tb.open_file("D_%s%s.h5" % (ns, set_id), mode="a")
    # create a group one level below root called response
    group = base.create_group("/", 'epsilon', 'DFT of total strain field')
    # initialize  array
    base.create_array(group,
                      'resp_fft',
                      resp_fft,
                      'DFT of the response fields')
    # close HDF5 file
    base.close()

    msg = 'Convert FE results to frequency space for set %s%s: %s seconds' \
        % (ns, set_id, np.round((time.time() - st), 3))
    rr.WP(msg, wrt_file)


def res_red(filename, el, sn):
    """
    Summary:
        This function reads the E11 values from a .dat file and reorganizes
        the data into a el x el x el array with the correct organization
        It will also plot a certain x-slice in the dataset if called within
        this script.
    Inputs:
        filename (string): the name of the '.dat' file containing the
        FEM response
        el (int): the number of elements per side of the microstructure cube
    Outputs:
        r_mat ([el,el,el],float): the FEM response of the '.dat' file of
        interest
    """
    f = open(filename, "r")

    linelist = f.readlines()

    # finds a location several lines above the start of the data
    # linelist[n] reads the entire line at location n
    for ln in xrange(1000):
        if 'THE FOLLOWING TABLE' in linelist[ln]:
            break

    # line0 is the index of first line of the data
    line0 = ln + 5

    r_mat1 = np.zeros([el**3, 8])
    r_mat2 = np.zeros([el**3, 8])
    c = -1

    # this series of loops generates a 9261x8 dataset of E11s
    # (element x integration point)
    for k in xrange(el**3):
        for jj in xrange(8):
            c += 1
            r_mat1[k, jj] = linelist[line0 + c].split()[2]
            r_mat2[k, jj] = linelist[line0 + c].split()[3]

    f.close()

    # here we average all 8 integration points in each element cell
    r_mat1 = np.mean(r_mat1, axis=1)
    r_mat2 = np.mean(r_mat2, axis=1)

    return r_mat1, r_mat2
