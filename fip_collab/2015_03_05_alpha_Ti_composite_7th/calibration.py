# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

@author: nhpnp3
"""

import time
import os
import numpy as np
import functions as rr


# @profile
def calibration_main(el, ns, H, set_id, setsz, wrt_file):

    st = time.time()

    r_fft = np.load('r_fft_%s%s.npy' % (ns, set_id)).reshape([ns, el**3])

    p = 0
    specinfc = np.zeros((H, el**3), dtype='complex64')

    # setsz: number of microstructures per set
    setsz = 50.
    # setnum the total number of sets
    setnum = np.ceil(ns/setsz).astype('int')

    for k in xrange(el**3):

        MM = np.zeros((H, H), dtype='complex128')
        PM = np.zeros(H, dtype='complex128')

        for ii in xrange(setnum):

            ss = int(ii*setsz)  # sn for start of set

            if ii == setnum - 1:
                se = ns
            else:
                se = int((ii+1)*setsz)  # sn for end of set

            r_fft_k = r_fft[ss:se, k]

            direc = 'M_%s%s_%s-%s' % (ns, set_id, ss, se)
            nwd = os.getcwd() + '/' + direc  # for unix
            # nwd = os.getcwd() + '\\' + direc
            os.chdir(nwd)
            Mk = np.load('M_%s%s_%s-%s_frq%s.npy' % (ns, set_id, ss, se, k))
            os.chdir('..')

            [MM, PM] = gen_MM_PM(Mk, r_fft_k, MM, PM, H, se-ss)

        [specinfc[:, k], p] = do_regress(k, MM, PM, H, p)

        if k % 500 == 0:
            print 'frequency %s completed' % k

    np.save('specinfc_%s%s' % (ns, set_id), specinfc)

    msg = 'Calibration: %s seconds' % np.round((time.time() - st), 3)
    rr.WP(msg, wrt_file)


def gen_MM_PM(Mk, r_fft_k, MM, PM, H, ns):
    """
    Summary:
    Inputs:
        k (int): The frequency on which to perform the calibration.
        M ([el,el,el,ns,H], complex): The microstructure function in
        frequency space. Includes all local states (from any order terms)
        r_fft ([el,el,el,ns],complex): The response of the calibration
        FEM analyses after fftn
        MM:
        PM:
        r_fft:
        H (int): The number of local states in the microstructure function
        el (int): The number of elements per side of the 'cube'
        ns (int): The number of calibration samples
    Outputs:
        MM, PM
    """

    # for sn in xrange(ns-1):
    for sn in xrange(ns):

        # mSQ = np.array(M[sn, :, u, v, w])
        mSQ = Mk[sn, :]

        mSQc = np.conj(mSQ)

        MM += np.outer(mSQ, mSQc)
        PM += np.dot(r_fft_k[sn], mSQc)

    return MM, PM


def do_regress(k, MM, PM, H, p):
    """
    Summary: This function calibrates the influence coefficients from the
        frequency space calibration microstructures and FEM responses for a
        specific frequency
    Inputs:
        k (int): The frequency on which to perform the calibration.
        MM:
        PM:
        H (int): The number of local states in the microstructure function
        p: ([p],int) the locations of the independent columns for the 1st
        frequency. It is expected that all rows and columns but the 0th
        should be independent for frequencies 1 through (el^3 - 1)
    Outputs:
        specinfc_k:([H],complex) influence coefficients in frequency space
        for the k'th frequency
        p
    """

    if k < 2:
        p = independent_columns(MM, .001)

    calred = MM[p, :][:, p]
    resred = PM[p].conj()

    specinfc_k = np.zeros(H, dtype='complex64')
    specinfc_k[p] = np.linalg.solve(calred, resred)

    return specinfc_k, p


def independent_columns(A, tol=1e-05):
    """
    Summary:
        This function returns an vector of the independent columns of a matrix
        Note: the answer may not be unique; this function returns one of many
        possible answers.
        Source: http://stackoverflow.com/q/1331249
    Inputs:
        A (generic array {numerical})
        tol (float): This number specifies how numerically close two columns
        must be to be dependent.
    Outputs:
        independent (vector of int): vector containing the indices of the
        independent columns of A
    """
    Q, R = np.linalg.qr(A)
    independent = np.where(np.abs(R.diagonal()) > tol)[0]
    return independent

if __name__ == "__main__":
    st = time.time()
    calibration_main(21, 200, 128, 'calRpc', 'M', 'test.txt')
    print "elapsed time: %s" % (time.time() - st)
