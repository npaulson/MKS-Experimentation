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


def micr_func(ns,set_id,step,wrt_file):
    
    start = time.time()    
    
    el = 21
    ## specify the number of local states you are using
    H = 15
    
    ## import microstructures
    micr = np.zeros([el,el,el,ns,H], dtype = 'complex128')
    pre_micr = np.load('euler_GSH_%s%s_s%s.npy' %(ns,set_id,step))
    for h in xrange(H):
        for sn in range(ns):
            micr[:,:,:,sn,h] = np.swapaxes(np.reshape(np.flipud
                                    (pre_micr[:,sn,h]), [el,el,el]),1,2)
    
    del pre_micr    
    
    end = time.time()
    timeE = np.round((end - start),3)
    msg = "generate real-space microstructure function from GSH-coefficients: %s seconds" %timeE
    rr.WP(msg,wrt_file)
    
    ## Microstructure functions in frequency space
    start = time.time()
    
    M = np.fft.fftn(micr, axes = [0,1,2])
    del micr
    size = M.nbytes
    np.save('M_%s%s_s%s' %(ns,set_id,step),M)
    
    end = time.time()
    timeE = np.round((end - start),3)
    
    msg = "FFT3 conversion of micr to M_%s%s_s%s: %s seconds" %(ns,set_id,step,timeE)
    rr.WP(msg,wrt_file)
    msg = 'Size of M_%s%s_s%s: %s bytes' %(ns,set_id,step,size)
    rr.WP(msg,wrt_file)