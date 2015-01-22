# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script reads a set of microstructures designated by the set-ID and saves
the microstructure function in real and frequency space.

@author: nhpnp3
"""

import time
import numpy as np
import functions as rr
import scipy.io as sio

def msf(el,ns,H,set_id,wrt_file):
    
    start = time.time()    
    
    ## import microstructures
    tmp = sio.loadmat('micr_H%s_%s.mat' %(H,set_id))['gshS']

#    #### 12/18/2014 CHANGE BACK
#        
#    tmp = np.swapaxes(tmp,0,2)
#    
#    tmp = tmp/np.array([[[1,5,5,5,5,5,9,9,9,9,9,9,9,9,9]]]).T #remove normalization
#
#    tmp = np.swapaxes(tmp,0,1)
#
#    ####

    tmp = np.swapaxes(np.swapaxes(tmp,0,2),0,1)

    micr = tmp.reshape([ns,H,el,el,el])    
    
    del tmp

    np.save('msf_%s%s' %(ns,set_id),micr)
    
    end = time.time()
    timeE = np.round((end - start),3)
    msg = "generate real-space microstructure function from GSH-coefficients: %s seconds" %timeE
    rr.WP(msg,wrt_file)
    
    ## Microstructure functions in frequency space
    start = time.time()
    
    M = np.fft.fftn(micr, axes = [2,3,4])    
    del micr
    size = M.nbytes
    np.save('M_%s%s' %(ns,set_id),M)
    
    end = time.time()
    timeE = np.round((end - start),3)
    
    msg = "FFT3 conversion of micr to M_%s%s: %s seconds" %(ns,set_id,timeE)
    rr.WP(msg,wrt_file)
    msg = 'Size of M_%s%s: %s bytes' %(ns,set_id,size)
    rr.WP(msg,wrt_file)