# -*- coding: utf-8 -*-
"""
Functions connected to 3D, isotropic MKS analyses

In general these functions are not for parallel processing or chunking of data

Noah Paulson, 5/9/2014
"""

import numpy as np
import time
import itertools as it
import scipy.io as sio


def calib(k,M,resp_fft,p,H,el,ns):
    """
    Summary: This function calibrates the influence coefficients from the 
        frequency space calibration microstructures and FEM responses
    Inputs:
        M: (el,el,el,ns,H) The microstructure function in frequency space.
        Includes all local states (from any order terms)
        resp_fft: (el,el,el,ns) The response of the calibration FEM analyses
        after fftn
        H: (scalar) The number of local states in the microstructure function
        el: (scalar) The number of elements per side of the 'cube'
        ns: (scalar) The number of samples (assumed to be n-1 calibration and 1 
        validation)
        filename (string): The filename to write messages to
    Outputs:
        specinfc_k:(H) influence coefficients in frequency space for the k'th
        frequency
    """    
    
    [u,v,w] = np.unravel_index(k,[el,el,el])

    MM = np.zeros((H,H),dtype = 'complex128')
    PM = np.zeros((H,1),dtype = 'complex128')
    
    for n in xrange(ns-1):

        mSQ = np.array(M[u,v,w,n,:])     
        mSQc = np.conj(mSQ[None,:])
        mSQt = mSQ[:,None]
        
        MM = MM + np.dot(mSQt, mSQc)
        PM[:,0] = PM[:,0] + np.dot(resp_fft[u,v,w,n],mSQc)
 
    if k < 2:
        p = independent_columns(MM, .001)
        print p

    calred = MM[p,:][:,p]
    resred = PM[p,0].conj().T
    
    specinfc_k = np.zeros(H,dtype = 'complex64')
    specinfc_k[p] = np.linalg.solve(calred, resred)
    
    if k == 1:
        return specinfc_k, p
    else:
        return specinfc_k


def eval_meas(mks_R,resp_val,el):
    """
    Summary:
    Inputs:
        mks_R: (el,el,el) The response predicted by the MKS for the validation
        microstructure
        resp: (el,el,el,ns) the FEM responses of all microstructures
        el: (scalar) The number of elements per side of the 'cube'
    Outputs:
        avgE: (scalar)
        MASE: (scalar)
    """
    avgE = np.average(mks_R[:,:,:])
    MASE = 0
    for k in xrange(el**3):
        [u,v,w] = np.unravel_index(k,[el,el,el])
        MASE = MASE + ((np.abs(resp_val[u,v,w] - mks_R[u,v,w]))/(avgE * el**3))
        
    return avgE, MASE

def gen_micr(filename1,filename2,read_dat,ns,el,H):
    """
    Summary:
        This function reads the microstructures for all samples (calibration
        and validation) from a matlab data file, rearanges them into ns # of
        el x el x el cubes, and saves them in the .npy file format
    Inputs:
        file_name (string): the filename for the matlab '.mat' file
        read_dat (int): if read_dat = 1 the '.mat' file is read and rearanged,
        if read_dat = 0 micr is simply loaded from the '.npy' file
        ns (int): the total number of microstructures (for calibration and 
        validation)
        el (int): the number of elements per side of the microstructure cube
    Output:
        micr ([el,el,el,ns],int8): The binary microstructures for calibration
        and validation
    """
    if read_dat == 1:        
        
        start = time.time()

        ## convert the matlab files arrays in python        
        
        micr_flag_BASE = sio.loadmat(filename2)
        ## micr_flag contains 9261 flags for each sample microsturcture,
        ## each representing an orientation. The number in these flags
        ## corresponds with an orientation in ex_ori_fr
        micr_flag = micr_flag_BASE['ct']         

        ex_ori_BASE = sio.loadmat(filename1)    
        ## ex_ori_fr contains 522 sets of 15 GSH coefficients, where each 
        ## set corresponds with an orientation on the surface of the
        ## hexagonal-triclinic fundamental zone.        
        ex_ori_fr = ex_ori_BASE['extremeorienth_fr']  
               
        pre_micr = np.zeros((el**3,ns,H),dtype = 'complex64')
        for k in range(el**3):
            for n in range(ns):
                pre_micr[k,n,:] = ex_ori_fr[micr_flag[k,n]-1,:]
        
        ## here we perform flips and reshapes to enact the proper arrangement 
        ## of spatial locations in the 3D cub
        micr = np.zeros((el,el,el,ns,H),dtype = 'complex64') 
        for n in range(ns):
            for h in range(H):
                micr[:,:,:,n,h] = np.swapaxes(np.reshape(
                            np.flipud(pre_micr[:,n,h]), [el,el,el]),1,2)
    
        ## save the microstructure array
        np.save('micr_%s' %ns,micr)

        end = time.time()
        timeE = np.round((end - start),3)
    
    else:        

        start = time.time()
        micr = np.load('micr_%s.npy' %ns)
        end = time.time()
        timeE = np.round((end - start),3)
    
    return [micr, timeE]


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

def load_fe(filename,read_dat,ns,el):
    """    
    Summary:        
        This function loads the finite element (FE) responses from '.dat' 
        files. This version is used for files with orientation information
    Inputs:
        filename (string): The '.mat' file containing orientation information
        for the set of microstructures        
        read_dat (int): if read_dat = 1 the '.dat' files are read and compiled,
        if read_dat = 0 resp is simply loaded from an existing '.npy' file
        ns (int): the total number microstructures (calibration or validation)
        el (int): the number of elements per side of the microstructure cube        
    Outputs:
        resp ([el,el,el,ns],float): The FEM responses of all calibration or 
        validation microstructures
        msg (string): A message detailing how resp was loaded
    """    

    if read_dat == 1:
        start = time.time()    

        micr_flag_BASE = sio.loadmat(filename)
        ## ori_mats contains a 3x3 orientation matrix for each spatial location
        ## in each sample microstructure
        ori_mat = micr_flag_BASE['orientation']
        
        resp = np.zeros((el,el,el,6,ns),dtype = 'float64')
        for sn in xrange(ns):
            filename = "hcp_21el_200s_%s.dat" %(sn+1) 
            resp[:,:,:,:,sn] = res_red(filename,ori_mat,el,sn)
        
        np.save('FE_results_%s' %ns,resp)    
        
        end = time.time()
        timeE = np.round((end - start),1)
        msg = "Import FE results: %s seconds" %timeE
    
    ## if read_dat == 0 the script will simply reload the results from a 
    ## previously saved FE_results_#.npy
    else:
        resp = np.load('FE_results_%s.npy' %ns)
        msg = "FE results loaded"  
    
    return [resp,msg]



def mf(micr_sub,el,order, H):
   
    ## microstructure functions
        
    sub_len = len(micr_sub[0,0,0,:])
    pm = np.zeros([el,el,el,sub_len,2])
    pm[:,:,:,:,0] = (micr_sub == 0)
    pm[:,:,:,:,1] = (micr_sub == 1)
    pm = pm.astype(int)

    if order == 1:
        m_sub = pm         
        
    if order == 2:
        
        hs = np.array([[1,1],[0,0],[1,0],[0,1]])
        vec = np.array([[1,0],[1,1],[1,2]])
        
        k = 0
        m_sub = np.zeros([el,el,el,sub_len,H])
        for hh in xrange(len(hs[:,0])):
            for t in xrange(len(vec[:,0])):
                a1 = pm[:,:,:,:,hs[hh,0]]
                a2 = np.roll(pm[:,:,:,:,hs[hh,1]],vec[t,0],vec[t,1])
                m_sub[:,:,:,:,k] = a1 * a2
                k = k + 1
        
    if order ==7:            
        
        hs = np.array(list(it.product([0,1],repeat=7)))
        vec = np.array([[1,0],[1,1],[1,2],[-1,0],[-1,1],[-1,2]])
        
        vlen = len(vec[:,0])
        m_sub = np.zeros([el,el,el,sub_len,H])
        
        for hh in xrange(H):  
            a1 = pm[:,:,:,:,hs[hh,0]]    
            pre_m = a1  
            for t in xrange(vlen):      
                a_n = np.roll(pm[:,:,:,:,hs[hh,t+1]],vec[t,0],vec[t,1])
                pre_m = pre_m * a_n  
            m_sub[:,:,:,:,hh] = pre_m
            
    m_sub = m_sub.astype(int)
     
    return m_sub

def mf_sn(micr_sn, el, order, H):
    """
    Summary:
        This function takes in a single microstructure, and generates all of
        the local states based on the desired order of terms. It does this by
        shifting the microstructure in pre-defined directions, and then
        performing an element-wise multiplication. This reveals the
        conformation for a higher order local state.
    Inputs:
        micr_sn ([el,el,el],int8): the arangement of black and white cells in
        the cube for a single microstructure (from the micr variable)
        el (int): the number of elements per side of the microstructure cube
        H (int): the total number of local states in the microstructure
        function (including higher order comformations)
        order (int): the order of the terms used for 
    Output:
        m_sn ([el,el,el,H],int): The microstructure function for a single
        microstructure, including higher order local state conformations
    """
    ## 1st order microstructure function generation
    pm = np.zeros([el,el,el,2])
    pm[:,:,:,0] = (micr_sn == 0)
    pm[:,:,:,1] = (micr_sn == 1)
    pm = pm.astype(int)

    if order == 1:
        ## pm already represents the microstructure function for first order
        ## terms        
        m_sn = pm          
        
    if order == 2:
        ## in hs, the first element of each row represents the desired local
        ## state of the original cell (black or white), and the second is
        ## the desired local state after the microstructure is shifted.
        hs = np.array([[1,1],[0,0],[1,0],[0,1]])
        ## in vec, the first element of each row represents the number of 
        ## elements to shift the microstructure, and the second is the
        ## dimension along which the microstructure should be shifted
        vec = np.array([[1,0],[1,1],[1,2]])
        
        ## in the generation of the microstructure for second order
        ## localization terms the microstructure is rolled in a single
        ## direction for each term.
        k = 0
        m_sn = np.zeros([el,el,el,H])
        for hh in xrange(len(hs[:,0])):
            for t in xrange(len(vec[:,0])):
                a1 = pm[:,:,:,hs[hh,0]]
                a2 = np.roll(pm[:,:,:,hs[hh,1]],vec[t,0],vec[t,1])
                m_sn[:,:,:,k] = a1 * a2
                k = k + 1
        
    if order == 7:            
        ## Here hs is automatically generated
        hs = np.array(list(it.product([0,1],repeat=7)))
        vec = np.array([[1,0],[1,1],[1,2],[-1,0],[-1,1],[-1,2]])
        
        vlen = len(vec[:,0])
        m_sn = np.zeros([el,el,el,H])
        
        ## in the generation of the microstructure for seventh order terms
        ## the microstructure is rolled in all 6 directions. These 7 
        ## microstructures are all multiplied together.
        for hh in xrange(H):  
            a1 = pm[:,:,:,hs[hh,0]]    
            pre_m = a1  
            for t in xrange(vlen):      
                a_n = np.roll(pm[:,:,:,hs[hh,t+1]],vec[t,0],vec[t,1])
                pre_m = pre_m * a_n  
            m_sn[:,:,:,hh] = pre_m
            
    m_sn = m_sn.astype(int)
   
    return m_sn


def res_red(filename,ori_mat,el,sn):
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
        e11mat ([el,el,el],float): the FEM response of the '.dat' file of
        interest
    """
    f = open(filename, "r")

    linelist = f.readlines()

    # finds a location several lines above the start of the data
    # linelist[n] reads the entire line at location n
    for ln in range(1000):
        if 'THE FOLLOWING TABLE' in linelist[ln]:
            break

    # line0 is the index of first line of the data
    line0 = ln + 5;      

    E = np.zeros((21**3,8,6))
    c = -1

    # this series of loops generates a 9261x8 dataset of E11s (element x integration point) 
    for k in range(21**3):
        for jj in range(8):
            c += 1                        
            E[k,jj,:] = linelist[line0 + c].split()[3:]
    
    f.close()    
    
    # here we average all 8 integration points in each element cell
    E = np.mean(E, axis=1)
    
    Etot = np.zeros([el**3,6])
    # here we convert the strain tensor at each location from crystal to 
    # sample frame
    for k in range(21**3):
        # E_ten_cry is the strain tensor at the spatial location of interest
        # in the crystal frame
        E_ten_cry = np.array([[    E[k,0], 0.5*E[k,3], 0.5*E[k,4]],
                              [0.5*E[k,3],     E[k,1], 0.5*E[k,5]],
                              [0.5*E[k,4], 0.5*E[k,5],     E[k,2]]])
        # Here we convert from crystal to sample frame
        E_ten_samp = np.dot(ori_mat[:,:,k,sn].T ,np.dot(E_ten_cry,ori_mat[:,:,k,sn]))
                
        Etot[k,:] = [E_ten_samp[0,0],E_ten_samp[1,1],E_ten_samp[2,2],
                     E_ten_samp[0,1],E_ten_samp[1,2],E_ten_samp[1,2]]
    
    # here we reshape the data from a 9261 length vector to a 21x21x21 3D matrix     
    Emat = np.zeros([el,el,el,6])   
    for r in range(6):    
        Emat[:,:,:,r] = np.swapaxes(np.reshape(np.flipud(Etot[:,r]), [el,el,el]),1,2)

    return Emat


def WP(msg,filename):
    """
    Summary:
        This function takes an input message and a filename, and appends that
        message to the file. This function also prints the message
    Inputs:
        msg (string): the message to write and print.
        filename (string): the full name of the file to append to.
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

    #np.save('MKS_2stOrd_resp',mks_R) 
    
    return mks_R