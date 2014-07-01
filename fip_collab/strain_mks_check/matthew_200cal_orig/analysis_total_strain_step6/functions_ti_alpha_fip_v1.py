# -*- coding: utf-8 -*-
"""
Functions connected to 3D, isotropic MKS analyses

In general these functions are not for parallel processing or chunking of data

Noah Paulson, 5/28/2014
"""

import numpy as np
import vtk


def calib(k,M,E11_fft,p,H,el,ns):
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
#    PM = np.zeros((H,1),dtype = 'complex128')
    PM = np.zeros(H,dtype = 'complex128')

    
    for n in xrange(ns-1):

        mSQ = np.array(M[u,v,w,n,:])     
#        mSQc = np.conj(mSQ[None,:])
        mSQc = np.conj(mSQ)        
#        mSQt = mSQ[:,None]
        
#        MM += np.dot(mSQt, mSQc)
        MM += np.outer(mSQ, mSQc)

#        PM[:,0] += np.dot(fip_fft[u,v,w,n],mSQc)
        PM += np.dot(E11_fft[u,v,w,n],mSQc)

 
    if k < 2:
        p = independent_columns(MM, .001)

    calred = MM[p,:][:,p]
#    resred = PM[p,0].conj().T
    resred = PM[p].conj()

    
    specinfc_k = np.zeros(H,dtype = 'complex64')
    specinfc_k[p] = np.linalg.solve(calred, resred)
    
    if k == 1:
        return specinfc_k, p
    else:
        return specinfc_k


def eval_meas(mks_R_indv,resp_indv,el):
    """
    Summary: Calculates the MASE and average error
    Inputs:
        mks_R ([el,el,el],float): The response predicted by the MKS for
        validation microstructures
        resp ([el,el,el],float): the FEM responses of all microstructures
        el (int): The number of elements per side of the 'cube'
    Outputs:
        avgE (float): The average strain value for the microstructure
        MASE (float): Mean Absolute Square Error
    """
    avgE_mks = np.average(mks_R_indv)
    avgE_fe= np.average(resp_indv)
    MASE = 0
    for k in xrange(el**3):
        [u,v,w] = np.unravel_index(k,[el,el,el])
        MASE += ((np.abs(resp_indv[u,v,w] - mks_R_indv[u,v,w]))/(avgE_fe * el**3))
        
    return avgE_fe,avgE_mks, MASE


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


def read_vtk(filename):
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
    
    elx = vec[0]
    	
    # Calculate the total number of elements
    el_total = elx * elx * elx

    Euler   = data.GetCellData().GetArray(reader.GetVectorsNameInFile(0))
#    grain_ID = data.GetCellData().GetArray(reader.GetScalarsNameInFile(0))    
#    FIP_FS  = data.GetCellData().GetArray(reader.GetScalarsNameInFile(1))
    E11  = data.GetCellData().GetArray(reader.GetTensorsNameInFile(1))    
    
    
#    fip_py = np.zeros([el_total])
#    grain_id_py = np.zeros([el_total])
    euler_py = np.zeros([el_total, 3])    
    E11_py = np.zeros([el_total])        
        
#    for ii in range(el_total):
#        grain_id_py[ii] = grain_ID.GetValue(ii)        
    
#    for ii in xrange(el_total):
#        fip_py[ii] = FIP_FS.GetValue(ii)
    
    # Example of storing vector data# Note: check and make sure this is done correctly.
    for ii in xrange(el_total):
        euler_py[ii,0] = Euler.GetValue(ii*3 + 0)
        euler_py[ii,1] = Euler.GetValue(ii*3 + 1)
        euler_py[ii,2] = Euler.GetValue(ii*3 + 2)
    
    for ii in xrange(el_total):
        E11_py[ii] = E11.GetValue(ii*9)
#        tensor1[ii,0] = StressT_Max.GetValue(ii*9 + 0)
#        tensor1[ii,1] = StressT_Max.GetValue(ii*9 + 1)
#        tensor1[ii,2] = StressT_Max.GetValue(ii*9 + 2)
#        tensor1[ii,3] = StressT_Max.GetValue(ii*9 + 3)
#        tensor1[ii,4] = StressT_Max.GetValue(ii*9 + 4)
#        tensor1[ii,5] = StressT_Max.GetValue(ii*9 + 5)
#        tensor1[ii,6] = StressT_Max.GetValue(ii*9 + 6)
#        tensor1[ii,7] = StressT_Max.GetValue(ii*9 + 7)
#        tensor1[ii,8] = StressT_Max.GetValue(ii*9 + 8)

    
    return [euler_py, E11_py]


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

def validate(M_val,specinfc,H,el=21):
    ## vectorize the frequency-space microstructure function for the validation
    ## dataset
    lin_M = np.zeros((el**3,H),dtype = 'complex64')
    for h in xrange(H):
        lin_M[:,h] = np.reshape(M_val[:,:,:,h],el**3)
    
    ## find the frequency-space response of the validation microstructure
    ## and convert to the real space
    lin_sum = np.sum(np.conjugate(specinfc) * lin_M, 1)
    mks_F = np.reshape(lin_sum,[21,21,21])
    mks_R = np.fft.ifftn(mks_F).real
    
    return mks_R