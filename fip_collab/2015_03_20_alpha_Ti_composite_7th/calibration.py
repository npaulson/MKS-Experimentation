# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

@author: nhpnp3
"""

import time
import numpy as np
import functions as rr
import tables as tb


# @profile
def calibration_main(el, ns, H, set_id, wrt_file):

    st = time.time()

    p = 0
    specinfc = np.zeros((H, el**3), dtype='complex64')

    # open HDF5 file
    base = tb.open_file("D_%s%s.h5" % (ns, set_id), mode="r")
    # define an object for the microstructure function array
    M_all = base.root.msf.M_all
    # load the frequency space response into memory
    r_fft = base.root.response.resp_fft[...].reshape(ns, el**3)

    for indx in xrange(el):
        sk = indx*el**2
        ek = sk + el**2

        Mk = M_all[:, :, sk:ek]

        if indx == 0:
            msg = 'size of Mk: %s Mb' % (Mk.nbytes/(10**6))
            rr.WP(msg, wrt_file)

        for ki in xrange(el**2):

            k = sk + ki

            MM = np.zeros((H, H), dtype='complex128')
            PM = np.zeros(H, dtype='complex128')

            for sn in xrange(ns):

                mSQ = Mk[sn, :, ki]

                mSQc = np.conj(mSQ)

                MM += np.outer(mSQ, mSQc)
                PM += np.dot(r_fft[sn, k], mSQc)

            [specinfc[:, k], p] = do_regress(k, MM, PM, H, p)

        msg = 'frequency %s completed' % ek
        rr.WP(msg, wrt_file)

    # close the HDF5 file
    base.close()

    # open HDF5 file
    base = tb.open_file("ref_%s%s.h5" % (ns, set_id), mode="a")
    # create a group one level below root called response
    group = base.create_group("/", 'infl_coef', 'influence coefficients')
    # initialize  array
    base.create_array(group,
                      'specinfc',
                      specinfc,
                      'incluence coefficients')
    # close HDF5 file
    base.close()

    msg = 'Calibration: %s seconds' % np.round((time.time() - st), 3)
    rr.WP(msg, wrt_file)


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
