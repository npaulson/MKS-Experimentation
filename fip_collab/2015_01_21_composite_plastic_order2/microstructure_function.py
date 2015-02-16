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

def msf(el,ns,Hi,H,order,set_id,wrt_file):
    
    start = time.time()    
    
    ## import microstructures
    tmp = np.zeros([Hi,ns,el**3])
    microstructure = sio.loadmat('M_%s%s.mat' %(ns,set_id))['M']
    microstructure = microstructure.swapaxes(0,1)
    
    for h in xrange(Hi):
        tmp[h,...] = (microstructure == h).astype(int)
    
    del microstructure

    tmp = tmp.swapaxes(0,1)
    pre_micr = tmp.reshape([ns,Hi,el,el,el])    
    
    del tmp

    np.save('pre_msf_%s%s' %(ns,set_id),pre_micr)

    micr = rr.mf(pre_micr, el, ns, Hi, H, order)
    del pre_micr


    np.save('msf_%s%s' %(ns,set_id),micr)
    
    end = time.time()
    timeE = np.round((end - start),3)
    msg = "generate real-space microstructure function: %s seconds" %timeE
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