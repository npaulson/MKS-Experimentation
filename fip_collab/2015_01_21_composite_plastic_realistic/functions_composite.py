# -*- coding: utf-8 -*-
"""
Functions connected to 3D, isotropic MKS analyses

In general these functions are not for parallel processing or chunking of data

Noah Paulson, 5/28/2014
"""

import numpy as np
import itertools as it


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
    avgr_mks = np.average(mks_R_indv)
    avgr_fe= np.average(resp_indv)
    MASE = 0
    for k in xrange(el**3):
        [u,v,w] = np.unravel_index(k,[el,el,el])
        MASE += ((np.abs(resp_indv[u,v,w] - mks_R_indv[u,v,w]))/(avgr_fe * el**3))
        
    return avgr_fe,avgr_mks, MASE


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


def mf(micr,el,ns,Hi,H,order):
   
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
        m = micr        
        
    if order == 2:
        
        hs = np.array([[1,1],[0,0],[1,0],[0,1]])
        vec = np.array([[1,0],[1,1],[1,2]])
        
        k = 0
        m = np.zeros([ns,H,el,el,el])
        for hh in xrange(hs.shape[0]):
            for t in xrange(vec.shape[0]):
                a1 = micr[:,hs[hh,0],...]
                a2 = np.roll(micr[:,hs[hh,1],...],vec[t,0],vec[t,1])
                m[:,k,...] = a1 * a2
                k = k + 1
        
    if order ==7:            
        
        hs = np.array(list(it.product([0,1],repeat=7)))
        vec = np.array([[1,0],[1,1],[1,2],[-1,0],[-1,1],[-1,2]])
        
        vlen = vec.shape[0]
        m = np.zeros([ns,H,el,el,el])
        
        for hh in xrange(H):  
            a1 = micr[:,hs[hh,0],...]    
            pre_m = a1  
            for t in xrange(vlen):      
                a_n = np.roll(micr[:,hs[hh,t+1],...],vec[t,0],vec[t,1])
                pre_m = pre_m * a_n  
            m[:,hh,...] = pre_m                 
                 
                 
    m = m.astype(int)

    return m


def res_red(filename,el,sn):
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
    line0 = ln + 5;      

    r_mat = np.zeros([el**3,8])
    c = -1

    # this series of loops generates a 9261x8 dataset of E11s (element x integration point) 
    for k in xrange(el**3):
        for jj in xrange(8):
            c += 1                        
            r_mat[k,jj] = linelist[line0 + c].split()[2]
    
    f.close()    
    
    # here we average all 8 integration points in each element cell
    r_mat = np.mean(r_mat, axis=1)

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




