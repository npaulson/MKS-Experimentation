# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script reads a set of microstructures designated by the set-ID and saves
the microstructure function in real and frequency space.

@author: nhpnp3
"""

import time
import numpy as np
import functions_composite as rr
import scipy.io as sio

def msf(el,ns,H,set_id,wrt_file):
    
    start = time.time()    
    
    ## import microstructures
    pre_micr = np.zeros([el**3,ns,H])
    microstructure = sio.loadmat('M_%s%s.mat' %(ns,set_id))['M']
    
    for h in xrange(H):
        pre_micr[...,h] = (microstructure == h).astype(int)
    
    del microstructure

    micr = np.swapaxes(pre_micr[::-1,...].reshape([el,el,el,ns,H]),1,2)    
    
    del pre_micr    

    np.save('msf_%s%s' %(ns,set_id),micr)
    
    end = time.time()
    timeE = np.round((end - start),3)
    msg = "generate real-space microstructure function from GSH-coefficients: %s seconds" %timeE
    rr.WP(msg,wrt_file)
    
    ## Microstructure functions in frequency space
    start = time.time()
    
    M = np.fft.fftn(micr, axes = [0,1,2])    
    del micr
    size = M.nbytes
    np.save('M_%s%s' %(ns,set_id),M)
    
    end = time.time()
    timeE = np.round((end - start),3)
    
    msg = "FFT3 conversion of micr to M_%s%s: %s seconds" %(ns,set_id,timeE)
    rr.WP(msg,wrt_file)
    msg = 'Size of M_%s%s: %s bytes' %(ns,set_id,size)
    rr.WP(msg,wrt_file)