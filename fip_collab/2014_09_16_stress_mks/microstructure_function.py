# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script reads a set of microstructures designated by the set-ID and saves
the microstructure function in real and frequency space.

@author: nhpnp3
"""

import time
import numpy as np
import functions_polycrystal_strain as rr


def micr_func(ns,set_id,comp,wrt_file):
    
    start = time.time()    
    
    el = 21
    ## specify the number of local states you are using
    H = 15
    
    ## import microstructures
    micr = np.zeros([el,el,el,ns,H], dtype = 'complex128')
    pre_micr = np.load('euler_GSH_%s%s.npy' %(ns,set_id))
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
    np.save('M%s_%s%s' %(comp,ns,set_id),M)
    
    end = time.time()
    timeE = np.round((end - start),3)
    
    msg = "FFT3 conversion of micr to M%s_%s%s: %s seconds" %(comp,ns,set_id,timeE)
    rr.WP(msg,wrt_file)
    msg = 'Size of M%s_%s%s: %s bytes' %(comp,ns,set_id,size)
    rr.WP(msg,wrt_file)