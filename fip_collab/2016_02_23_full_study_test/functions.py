# -*- coding: utf-8 -*-
"""
Functions connected to 3D, isotropic MKS analyses

In general these functions are not for parallel processing or chunking of data

Noah Paulson, 5/28/2014
"""

import numpy as np
import vtk
import h5py
import gsh_hex_tri_L0_16 as gsh


def eval_func(theta, X, et_norm):
    """
    Summary: performs evaluation of calibrated function
    Inputs:
        theta ([el**3], float): vector of deformation modes for each SVE
        X ([el**3, 3], float): array of euler angles for each SVE
        et_norm ([el**3], float): vector of norm(et_dev) for each SVE
    Outputs:
        Y ([el**3], float): vector of values calculated by function
    """

    thr = 0.00001  # threshold on coefs w/rt maximum magnitude coef
    LL_p = 16  # LL_p: gsh truncation level

    a = 0.00485  # start for en range
    b = 0.00905  # end for en range

    # N_p: number of GSH bases to evaluate
    indxvec = gsh.gsh_basis_info()
    N_p = np.sum(indxvec[:, 0] <= LL_p)
    N_q = 40  # number of cosine bases to evaluate for theta
    N_r = 14  # number of cosine bases to evaluate for en

    L_th = np.pi/3.
    L_en = b-a

    # filename = 'log_final_results9261.txt'

    f = h5py.File('coeff_total.hdf5', 'r')
    coeff = f.get('coeff')[...]
    f.close()

    N_pts = theta.size

    """Select the desired set of coefficients"""

    cmax = N_p*N_q*N_r  # total number of permutations of basis functions

    # fn.WP(str(cmax), filename)

    cmat = np.unravel_index(np.arange(cmax), [N_p, N_q, N_r])
    cmat = np.array(cmat).T

    cuttoff = thr*np.abs(coeff).max()
    indxvec = np.arange(cmax)[np.abs(coeff) > cuttoff]

    # N_coef = indxvec.size
    # pct_coef = 100.*N_coef/cmax
    # fn.WP("number of coefficients retained: %s" % N_coef, filename)
    # fn.WP("percentage of coefficients retained %s%%"
    #       % np.round(pct_coef, 4), filename)

    """Evaluate the parts of the basis function individually"""

    p_U = np.unique(cmat[indxvec, 0])
    q_U = np.unique(cmat[indxvec, 1])
    r_U = np.unique(cmat[indxvec, 2])

    # fn.WP("number of p basis functions used: %s" % p_U.size, filename)
    # fn.WP("number of q basis functions used: %s" % q_U.size, filename)
    # fn.WP("number of r basis functions used: %s" % r_U.size, filename)

    all_basis_p = np.zeros([N_pts, N_p], dtype='complex128')
    for p in p_U:
        all_basis_p[:, p] = np.squeeze(gsh.gsh_eval(X, [p]))

    all_basis_q = np.zeros([N_pts, N_q], dtype='complex128')
    for q in q_U:
        all_basis_q[:, q] = np.cos(q*np.pi*theta/L_th)

    all_basis_r = np.zeros([N_pts, N_r], dtype='complex128')
    for r in r_U:
        all_basis_r[:, r] = np.cos(r*np.pi*(et_norm-a)/L_en)

    """Perform the prediction"""

    Y_ = np.zeros(theta.size, dtype='complex128')

    for ii in indxvec:

        p, q, r = cmat[ii, :]
        basis_p = all_basis_p[:, p]
        basis_q = all_basis_q[:, q]
        basis_r = all_basis_r[:, r]

        ep_set = basis_p*basis_q*basis_r

        Y_ += coeff[ii]*ep_set

    return Y_


def calib(k, M, r_fft, p, H, el, ns):
    """
    Summary: This function calibrates the influence coefficients from the
        frequency space calibration microstructures and FEM responses for a
        specific frequency
    Inputs:
        k (int): The frequency on which to perform the calibration.
        M ([el,el,el,ns,H], complex): The microstructure function in
        frequency space. Includes all local states (from any order terms)
        resp_fft ([el,el,el,ns],complex): The response of the calibration
        FEM analyses after fftn
        H (int): The number of local states in the microstructure function
        el (int): The number of elements per side of the 'cube'
        ns (int): The number of calibration samples
    Outputs:
        specinfc_k:([H],complex) influence coefficients in frequency space
        for the k'th frequency
        p: ([p],int) the locations of the independent columns for the 1st
        frequency. It is expected that all rows and columns but the 0th
        should be independent for frequencies 1 through (el^3 - 1)
    """

    [u, v, w] = np.unravel_index(k, [el, el, el])

    MM = np.zeros((H, H), dtype='complex128')
    PM = np.zeros(H, dtype='complex128')

    for n in xrange(ns-1):

        mSQ = np.array(M[n, :, u, v, w])
        mSQc = np.conj(mSQ)

        MM += np.outer(mSQ, mSQc)
        PM += np.dot(r_fft[n, u, v, w], mSQc)

    if k < 2:
        p = independent_columns(MM, .001)

    calred = MM[p, :][:, p]
    resred = PM[p].conj()

    specinfc_k = np.zeros(H, dtype='complex64')
    specinfc_k[p] = np.linalg.solve(calred, resred)

    if k == 1:
        return specinfc_k, p
    else:
        return specinfc_k


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


def read_vtk_tensor(filename, tensor_id, comp):
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

    # if tensor_id == 0:
    #     # if meas == 0, we read the stress tensor
    #     meas = data.GetCellData().GetArray(reader.GetTensorsNameInFile(0))
    # elif tensor_id == 1:
    #     # if meas == 1, we read the strain tensor
    #     meas = data.GetCellData().GetArray(reader.GetTensorsNameInFile(1))
    # elif tensor_id == 2:
    #     # if meas == 2, we read the plastic strain tensor
    #     meas = data.GetCellData().GetArray(reader.GetTensorsNameInFile(2))

    # if meas == 0, we read the stress tensor
    # if meas == 1, we read the strain tensor
    # if meas == 2, we read the plastic strain tensor
    meas = data.GetCellData().GetArray(reader.GetTensorsNameInFile(tensor_id))

    meas_py = np.zeros([el**3])

    for ii in xrange(el**3):
        meas_py[ii] = meas.GetValue(ii*9 + comp)

    return meas_py


def read_vtk_scalar(filename):
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

    # Calculate the total number of elements
    el_total = el**3

    # print reader.GetScalarsNameInFile

    Scalar = data.GetCellData().GetArray(reader.GetScalarsNameInFile(1))

    scalar_py = np.zeros([el_total])

    for ii in xrange(el_total):
        scalar_py[ii] = Scalar.GetValue(ii)

    return scalar_py


def read_vtk_vector(filename):
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

    Euler = data.GetCellData().GetArray(reader.GetVectorsNameInFile(0))

    euler_py = np.zeros([3, el**3])

    for ii in xrange(el**3):
        euler_py[0, ii] = Euler.GetValue(ii*3 + 0)
        euler_py[1, ii] = Euler.GetValue(ii*3 + 1)
        euler_py[2, ii] = Euler.GetValue(ii*3 + 2)

    return euler_py


def WP(msg, filename):
    """
    Summary:
        This function takes an input message and a filename, and appends that
        message to the file. This function also prints the message
    Inputs:
        msg (string): the message to write and print.
        filename (string): the full name of the file to append to.
    Outputs:
        both prints the message and writes the message to the specified file
    """
    fil = open(filename, 'a')
    print msg
    fil.write(msg)
    fil.write('\n')
    fil.close()
