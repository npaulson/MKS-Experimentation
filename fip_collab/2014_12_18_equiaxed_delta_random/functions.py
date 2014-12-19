# -*- coding: utf-8 -*-
"""
Functions connected to 3D, isotropic MKS analyses

In general these functions are not for parallel processing or chunking of data

Noah Paulson, 5/28/2014
"""

import numpy as np


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


def res_red(ori_mat,filename,el,sn):
    """
    Summary:    
        This function reads the E11 values from a .dat file and reorganizes
        the data into a el x el x el array with the correct organization
        It will also plot a certain x-slice in the dataset if called within
        this script.
    Inputs:
        filename (string): the name of the '.dat' file containing the 
        FEM response
        ori_mat ([3,3,el^3,ns],float): an array containing the orientation
        matrices (g) for each spatial location of each RVE in the set      
        el (int): the number of elements per side of the microstructure cube
    Outputs:
        Emat ([el,el,el],float): the FEM response of the '.dat' file of
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
    line0 = ln + 5;      

    E = np.zeros((21**3,8,6))
    c = -1

    # this series of loops generates a 9261x8 dataset of E11s (element x integration point) 
    for k in xrange(21**3):
        for jj in xrange(8):
            c += 1                        
            E[k,jj,:] = linelist[line0 + c].split()[3:]
    
    f.close()    
    
    # here we average all 8 integration points in each element cell
    E = np.mean(E, axis=1)
    
    Etot = np.zeros([el**3,6])
    # here we convert the strain tensor at each location from crystal to 
    # sample frame
    for k in xrange(21**3):
        # E_ten_cry is the strain tensor at the spatial location of interest
        # in the crystal frame
        E_ten_cry = np.array([[    E[k,0], 0.5*E[k,3], 0.5*E[k,4]],
                              [0.5*E[k,3],     E[k,1], 0.5*E[k,5]],
                              [0.5*E[k,4], 0.5*E[k,5],     E[k,2]]])
        # Here we convert from crystal to sample frame
        E_ten_samp = np.dot(ori_mat[:,:,k,sn].T ,np.dot(E_ten_cry,ori_mat[:,:,k,sn]))
                
#        Etot[k] = E_ten_samp[0,0]
        Etot[k,:] = [E_ten_samp[0,0],E_ten_samp[1,1],E_ten_samp[2,2],
                     E_ten_samp[0,1],E_ten_samp[1,2],E_ten_samp[1,2]]
          
    r_mat =  Etot[:,0]

    return r_mat
    
    
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




