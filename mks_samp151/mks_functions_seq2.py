# -*- coding: utf-8 -*-
"""
Functions connected to 3D, isotropic MKS analyses
Noah Paulson, 3/27/2014
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import itertools as it
import os

def calibrator(M,resp_fft,H,el=21,ns=151):
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
    Outputs:
        specinfc:(el**3,H) influence coefficients in frequency space
        timeE: (scalar) Total elapsed time for this function
        miscelaneous: Prints a message when certain frequencies have been 
        completed
    """    
    start = time.time()
    specinfc = np.zeros((el**3,H),dtype = 'complex64')
    for k in xrange(el**3):
        
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
#        else:
#            p = [0,1,2,3]
#        if np.array_equal(p,[0,1,2,3]) == False:
#            print "at frequency %s, p = %s" %(k,p)
    
        calred = MM[p,:][:,p]
        resred = PM[p,0].conj().T
        specinfc[k, p] = np.linalg.solve(calred, resred)
    
        if k % 1000 == 0:
            print "frequency completed: %s" %k
    
    end = time.time()
    timeE = np.round((end - start),3)
    
    return(specinfc,timeE)


def eval_meas(mks_R, resp, el=21):
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
        MASE = MASE + ((np.abs(resp[u,v,w,-1] - mks_R[u,v,w]))/(avgE * el**3))
        
    return avgE, MASE

def independent_columns(A, tol = 1e-05):
    """
    This function is from: http://stackoverflow.com/q/13312498

    Returns an array composed of independent columns of A.

    Note that answer may not be unique; this function returns one of many
    possible answers.
    """
    Q, R = np.linalg.qr(A)
    independent = np.where(np.abs(R.diagonal()) > tol)[0]
    return independent

def load_fe(read_dat=0,ns=151,el=21):
    """    
    responses of the black and white delta microstructures and random
    microstructures.

    if read_dat == 1 the program will reload all of the .dat files and save them
    to FE_results.npy
    """    

    if read_dat == 1:
        start = time.time()    
        
        os.chdir("C:\mks_data\order7_dat_151")
        
        resp = np.zeros((el,el,el,ns))
        for n in xrange(ns):
            filename = "sq21_5cont_%s.dat" %(n+1) 
            resp[:,:,:,n] = res_red(filename)
            print "%s is loaded" %filename 
        
        os.chdir("C:/Users/nhpnp3/Documents/GitHub/MKS_repository/MKS_7th")
        np.save('FE_results_151',resp)    
        
        end = time.time()
        timeE = np.round((end - start),1)
        print "Import FE results: %s seconds" %timeE
    
    ## if read_dat == 0 the script will simply reload the results from a 
    ## previously saved FE_results.npy
    else:
        resp = np.load('FE_results_151.npy')
        print "FE results loaded"  
    
    return resp

def mf(micr_sn, el=21, order=1):
   
    ## microstructure functions
    pm = np.zeros([el,el,el,2])
    pm[:,:,:,0] = (micr_sn == 0)
    pm[:,:,:,1] = (micr_sn == 1)
    pm = pm.astype(int)

    if order == 1:

        m_sn = pm        
        H = 2    
        
    if order == 2:
        
        hs = np.array([[1,1],[0,0],[1,0],[0,1]])
        vec = np.array([[1,0],[1,1],[1,2]])
        
        k = 0
        # H is the # of conformations of location and phase
        H = len(hs[:,0]) * len(vec[:,0])
        m_sn = np.zeros([el,el,el,H])
        for hh in xrange(len(hs[:,0])):
            for t in xrange(len(vec[:,0])):
                a1 = pm[:,:,:,hs[hh,0]]
                a2 = np.roll(pm[:,:,:,hs[hh,1]],vec[t,0],vec[t,1])
                m_sn[:,:,:,k] = a1 * a2
                k = k + 1
        
    if order == 7:            
        
        hs = np.array(list(it.product([0,1],repeat=7)))
        vec = np.array([[1,0],[1,1],[1,2],[-1,0],[-1,1],[-1,2]])
        
        # H is the # of conformations of location and phase
        H = len(hs[:,0])
        vlen = len(vec[:,0])
        print "Number of local states: %s" %H
        m_sn = np.zeros([el,el,el,H])
        
        for hh in xrange(H):  
            a1 = pm[:,:,:,hs[hh,0]]    
            pre_m = a1  
            for t in xrange(vlen):      
                a_n = np.roll(pm[:,:,:,hs[hh,t+1]],vec[t,0],vec[t,1])
                pre_m = pre_m * a_n  
            m_sn[:,:,:,hh] = pre_m
            
    m_sn = m_sn.astype(int)
   
    return m_sn

def mf_old(micr,el=21,ns=151, order=1):
   
    start = time.time()      

    ## microstructure functions
    pm = np.zeros([el,el,el,ns,2])
    pm[:,:,:,:,0] = (micr == 0)
    pm[:,:,:,:,1] = (micr == 1)
    pm = pm.astype(int)

    if order == 1:
        m = pm        
        H = 2    
        
    if order == 2:
        
        hs = np.array([[1,1],[0,0],[1,0],[0,1]])
        vec = np.array([[1,0],[1,1],[1,2]])
        
        k = 0
        # H is the # of conformations of location and phase
        H = len(hs[:,0]) * len(vec[:,0])
        m = np.zeros([el,el,el,ns,H])
        for hh in xrange(len(hs[:,0])):
            for t in xrange(len(vec[:,0])):
                a1 = pm[:,:,:,:,hs[hh,0]]
                a2 = np.roll(pm[:,:,:,:,hs[hh,1]],vec[t,0],vec[t,1])
                m[:,:,:,:,k] = a1 * a2
                k = k + 1
        
    if order ==7:            
        
        hs = np.array(list(it.product([0,1],repeat=7)))
        vec = np.array([[1,0],[1,1],[1,2],[-1,0],[-1,1],[-1,2]])
        
        # H is the # of conformations of location and phase
        H = len(hs[:,0])
        vlen = len(vec[:,0])
        print "Number of local states: %s" %H
        m = np.zeros([el,el,el,ns,H])
        
        for hh in xrange(H):  
            a1 = pm[:,:,:,:,hs[hh,0]]    
            pre_m = a1  
            for t in xrange(vlen):      
                a_n = np.roll(pm[:,:,:,:,hs[hh,t+1]],vec[t,0],vec[t,1])
                pre_m = pre_m * a_n  
            m[:,:,:,:,hh] = pre_m
            
    m = m.astype(int)

    end = time.time()
    timeE = np.round((end - start),2)        
    return [m,H,pm,timeE]


def pha_loc(filename="msf.txt",read_dat=0,el=21):   
    """
    Opens file with microstructure info where is column represents a single
    microstructure. Converts each microstructure column vector into a 
    cube data structure with indexing which matches that of the 
    Finite Element structure
    
    Inputs: 'filename', 'ns'== number of microstructures

    Output: 21x21x21xns array where ns is the microstructure index    
    
    """
    start = time.time()     
    
    if read_dat == 1:
       
        f = open(filename, "r")
    
        linelist = f.readlines()
        
        ns = len(linelist[0].split())    
        pre_micr1 = np.zeros((21**3,ns), dtype = 'int8')    
        
        for ii in xrange(21**3):
            for jj in xrange(ns):
                pre_micr1[ii,jj] = linelist[ii].split()[jj]
    
        f.close()
                
        # element 4630 is at the centroid of a 21x21x21 dataset
        #print e11cond[4630]
    
        # here we reshape the data from a 9261 length vector to a 21x21x21 3D matrix
            
        pre_micr2 = np.zeros((21,21,21,ns), dtype = 'int8')
        micr = np.zeros((21,21,21,ns), dtype = 'int8')
        
        for jj in range(ns):    
            pre_micr2 = np.reshape(np.flipud(pre_micr1[:,jj]), [21,21,21])
            micr[:,:,:,jj] = np.swapaxes(pre_micr2,1,2)
            
        np.save('cur_micr',[micr,ns])

    else:    
        [micr, ns] = np.load('cur_micr.npy')
        print "Microstructure loaded"         
        
    
    end = time.time()
    timeE = np.round((end - start),2)
        
    return [micr, ns, timeE]

   
def remzer(r_ini):  
    """
    This function shrinks a vector by removing the zeros.
    NOTE: Find a better way to do this    
    """
    c = 0
    r = np.zeros(len(r_ini))
    for ii in range(len(r_ini)):
        if r_ini[ii] != 0:
            
            r[c] = r_ini[ii]        
            
            c = c + 1
    
    return np.trim_zeros(r)


def res_red(filename = "21_1_noah.dat", el = 21, slc = 10):
    """
    This function reads the E11 values from a .dat file and reorganizes the
    data into a el x el x el array with the correct organization
    
    It will also plot a certain x-slice in the dataset if called within this
    script
    """
    f = open(filename, "r")

    linelist = f.readlines()

    # finds a location several lines above the start of the data
    # linelist[n] reads the entire line at location n
    for n in range(1000):
        if 'THE FOLLOWING TABLE' in linelist[n]:
            break

    # line0 is the index of first line of the data
    line0 = n + 5;      

    e11 = np.zeros((21**3,8))
    c = 0

    # this series of loops generates a 9261x8 dataset of E11s (element x integration point) 
    for ii in range(21**3):
        for jj in range(8):
            e11pre = linelist[line0 + c].split()[2]
            c = c + 1
            e11[ii,jj] = float(e11pre)
    
    f.close()    
    
    # here we average all 8 integration points in each element cell
    e11cond = np.flipud(np.mean(e11, axis=1))
    # element 4630 is at the centroid of a 21x21x21 dataset
    #print e11cond[4630]

    # here we reshape the data from a 9261 length vector to a 21x21x21 3D matrix
    pre_e11mat = np.reshape(e11cond, [21,21,21])
    e11mat = np.swapaxes(pre_e11mat,1,2)

    

    # here we generate an image and scalebar for a particular slice of the 3D matrix
    if __name__ == '__main__':
        
        plt.clf()        
                
        plt.imshow(e11mat[slc,:,:], origin='lower', interpolation='none',
                   cmap='jet')
        
        plt.colorbar()
        
    else:
        return e11mat

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