# -*- coding: utf-8 -*-
import time
import os
import h5py
import numpy as np
import functions as rr
from constants import const


def fegrab(ns, strt, set_id, dir):

    # FINITE ELEMENT RESPONSES
    st = time.time()

    C = const()

    r_fem = np.zeros([ns, C['el']**3])

    nwd = os.getcwd() + '/' + dir  # for unix
    # nwd = os.getcwd() + '\\' + direc
    os.chdir(nwd)

    for ii in xrange(ns):
        sn = strt + ii + 1
        filename = 'sq21_50test_%s.dat' % sn
        r_fem[ii, ...] = res_red(filename)

    r_fem = r_fem.reshape(ns, C['el'], C['el'], C['el'])

    os.chdir('..')

    f = h5py.File('responses.hdf5', 'a')
    f.create_dataset('y_sim_%s' % set_id, data=r_fem)
    f.close()

    msg = 'Load FE results from .dat files for set %s%s: %s seconds' \
        % (ns, set_id, np.round((time.time() - st), 3))
    rr.WP(msg, C['wrt_file'])


def res_red(filename):
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

    C = const()

    f = open(filename, "r")

    linelist = f.readlines()

    # finds a location several lines above the start of the data
    # linelist[n] reads the entire line at location n
    for ln in xrange(1000):
        if 'THE FOLLOWING TABLE' in linelist[ln]:
            break

    # line0 is the index of first line of the data
    line0 = ln + 5

    r_mat = np.zeros([C['el']**3, 8])
    c = -1

    # this series of loops generates a 9261x8 dataset of E11s
    # (element x integration point)
    for k in xrange(C['el']**3):
        for jj in xrange(8):
            c += 1
            r_mat[k, jj] = linelist[line0 + c].split()[2]

    f.close()

    # here we average all 8 integration points in each element cell
    r_mat = np.mean(r_mat, axis=1)

    return r_mat
