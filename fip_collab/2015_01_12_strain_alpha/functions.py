# -*- coding: utf-8 -*-
"""
Functions connected to 3D, isotropic MKS analyses

In general these functions are not for parallel processing or chunking of data

Noah Paulson, 5/28/2014
"""

import numpy as np
import vtk


def calib(k,M,r_fft,p,H,el,ns):
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
    
    [u,v,w] = np.unravel_index(k,[el,el,el])

    MM = np.zeros((H,H),dtype = 'complex128')
    PM = np.zeros(H,dtype = 'complex128')
    
    for n in xrange(ns-1):

        mSQ = np.array(M[n,:,u,v,w])     
        mSQc = np.conj(mSQ)        
        
        MM += np.outer(mSQ, mSQc)
        PM += np.dot(r_fft[n,u,v,w],mSQc)
 
    if k < 2:
        p = independent_columns(MM, .001)

    calred = MM[p,:][:,p]
    resred = PM[p].conj()
    
    specinfc_k = np.zeros(H,dtype = 'complex64')
    specinfc_k[p] = np.linalg.solve(calred, resred)
    
    if k == 1:
        return specinfc_k, p
    else:
        return specinfc_k


def independent_columns(A, tol = 1e-05):
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
    	
    # Calculate the total number of elements
    el_total = el**3

    if tensor_id == 0:
        # if meas == 0, we read the stress tensor        
        meas  = data.GetCellData().GetArray(reader.GetTensorsNameInFile(0))
    elif tensor_id == 1:
        # if meas == 1, we read the strain tensor        
        meas  = data.GetCellData().GetArray(reader.GetTensorsNameInFile(1))        
    elif tensor_id == 2:
        # if meas == 2, we read the plastic strain tensor        
        meas  = data.GetCellData().GetArray(reader.GetTensorsNameInFile(2))        
      
    meas_py = np.zeros([el_total])        
    
    for ii in xrange(el_total):
        meas_py[ii] = meas.GetValue(ii*9 + comp)
    
    return meas_py


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
    	
    # Calculate the total number of elements
    el_total = el**3

    Euler = data.GetCellData().GetArray(reader.GetVectorsNameInFile(0))      
    
    euler_py = np.zeros([3,el_total])       
    
    for ii in xrange(el_total):
        euler_py[0,ii] = Euler.GetValue(ii*3 + 0)
        euler_py[1,ii] = Euler.GetValue(ii*3 + 1)
        euler_py[2,ii] = Euler.GetValue(ii*3 + 2)
    
    return euler_py


def WP(msg,filename):
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