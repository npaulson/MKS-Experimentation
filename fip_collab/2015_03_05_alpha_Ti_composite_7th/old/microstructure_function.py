# -*- coding: utf-8 -*-
"""
This script reads a set of microstructures designated by the set-ID and saves
the microstructure function in real and frequency space.

Written by Noah Paulson Fri March 5 2015
"""

import time
import os
import numpy as np
import functions as rr
import scipy.io as sio
import itertools as it


def msf(el, ns, Hi, order, set_id, direc, wrt_file):

    st = time.time()

    # import microstructures
    tmp = np.zeros([Hi, ns, el**3])
    microstructure = sio.loadmat('M_%s%s.mat' % (ns, set_id))['M']
    microstructure = microstructure.swapaxes(0, 1)

    for h in xrange(Hi):
        tmp[h, ...] = (microstructure == h).astype(int)

    del microstructure

    tmp = tmp.swapaxes(0, 1)
    pre_micr = tmp.reshape([ns, Hi, el, el, el])

    del tmp

    np.save('pre_msf_%s%s' % (ns, set_id), pre_micr)

    # setsz: number of microstructures per set
    setsz = 50.
    # setnum the total number of sets
    setnum = np.ceil(ns/setsz).astype('int')

    # nwd = os.getcwd() + '/' + direc  # for unix
    nwd = os.getcwd() + '\\' + direc
    os.chdir(nwd)

    for ii in xrange(setnum):

        ss = int(ii*setsz)  # sn for start of set

        if ii == setnum - 1:
            se = ns
        else:
            se = int((ii+1)*setsz)  # sn for end of set

        # real space microstructure coefficients
        [micr, H] = mf(pre_micr[ss:se, ...], el, se-ss, Hi, order)

        # take FFT of microstructure coefficients
        M = np.fft.fftn(micr, axes=[2, 3, 4])

        print M.shape

        M = M.reshape([se-ss, H, el**3])

        for k in xrange(el**3):
            filename = 'M_%s%s_fq%s' % (ns, set_id, k)
            f = open(filename, 'a')

            for sn in xrange(se-ss):
                b = ''
                for h in xrange(M.shape[1]):
                    b += str(M[sn, h, k]) + ' '
                f.write(b + '\n')

        # np.save('M_%s%s_%s-%s' % (ns, set_id, ss, se), M)

    os.chdir('..')

    msg = "generate real space microstructure and perform FFT:"\
          " %s seconds" % np.round((time.time() - st), 3)
    rr.WP(msg, wrt_file)

    return H


def mf(micr, el, ns, Hi, order):

#    ## microstructure functions
#    pm = np.zeros([ns,Hi,el,el,el])
#    pm[:,0,...] = (micr == 0)
#    pm[:,1,...] = (micr == 1)
#    pm = pm.astype(int)
#
#    if order == 1:
#        m = pm
#
#    if order == 2:
#
#        hs = np.array([[1,1],[0,0],[1,0],[0,1]])
#        vec = np.array([[1,0],[1,1],[1,2]])
#
#        k = 0
#        m = np.zeros([ns,H,el,el,el])
#        for hh in xrange(hs.shape[0]):
#            for t in xrange(vec.shape[0]):
#                a1 = pm[:,hs[hh,0],...]
#                a2 = np.roll(pm[:,hs[hh,1],...],vec[t,0],vec[t,1])
#                m[:,k,...] = a1 * a2
#                k = k + 1
#
#    if order ==7:
#
#        hs = np.array(list(it.product([0,1],repeat=7)))
#        vec = np.array([[1,0],[1,1],[1,2],[-1,0],[-1,1],[-1,2]])
#
#        vlen = vec.shape[0]
#        m = np.zeros([ns,H,el,el,el])
#
#        for hh in xrange(H):
#            a1 = pm[:,hs[hh,0],...]
#            pre_m = a1
#            for t in xrange(vlen):
#                a_n = np.roll(pm[:,hs[hh,t+1],...],vec[t,0],vec[t,1])
#                pre_m = pre_m * a_n
#            m[:,hh,...] = pre_m

    if order == 1:
        H = Hi
        m = micr

    if order == 2:

        hs = np.array([[1, 1], [0, 0], [1, 0], [0, 1]])
        vec = np.array([[1, 0], [1, 1], [1, 2]])

        H = hs.shape[0] * vec.shape[0]

        k = 0
        m = np.zeros([ns, H, el, el, el])
        for hh in xrange(hs.shape[0]):
            for t in xrange(vec.shape[0]):
                a1 = micr[:, hs[hh, 0], ...]
                a2 = np.roll(micr[:, hs[hh, 1], ...], vec[t, 0], vec[t, 1])
                m[:, k, ...] = a1 * a2
                k = k + 1

    if order == 7:

        hs = np.array(list(it.product([0, 1], repeat=7)))
        vec = np.array([[1, 0], [1, 1], [1, 2], [-1, 0], [-1, 1], [-1, 2]])

        vlen = vec.shape[0]
        H = vlen

        m = np.zeros([ns, H, el, el, el])

        for hh in xrange(H):
            a1 = micr[:, hs[hh, 0], ...]
            pre_m = a1
            for t in xrange(vlen):
                a_n = np.roll(micr[:, hs[hh, t+1], ...], vec[t, 0], vec[t, 1])
                pre_m = pre_m * a_n
            m[:, hh, ...] = pre_m

    m = m.astype(int)

    return m, H
