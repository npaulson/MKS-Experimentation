# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

@author: nhpnp3
"""

import time
import numpy as np
import functions as rr
import scipy.io as sio

def fegrab(el,ns,set_id,wrt_file):
    
    ### FINITE ELEMENT RESPONSES ###
    start = time.time()    

    ori_mat = sio.loadmat('orientation_%s_%s.mat' %(set_id,ns))['orientation'];    
    
    resp = np.zeros([ns,el**3])   
    for sn in xrange(ns):
        filename = "%s_%s.dat" %(set_id,sn+1)        
        resp[sn,...] = rr.res_red(ori_mat,filename,el,sn)
    
    np.save('r_%s%s' %(ns,set_id),resp)  
    
    end = time.time()
    timeE = np.round((end - start),3)    
    msg = 'Load FE results from .dat files for set %s%s: %s seconds' %(ns,set_id,timeE)
    rr.WP(msg,wrt_file)
    
    ## responses in frequency space
    start = time.time()
    
    resp_fft = np.fft.fftn(resp.reshape([ns,el,el,el]), axes = [1,2,3]) 
    del resp
    np.save('r_fft_%s%s' %(ns,set_id),resp_fft)  
    
    end = time.time()
    timeE = np.round((end - start),3)
    msg = 'Convert FE results to frequency space for set %s%s: %s seconds' %(ns,set_id,timeE)
    rr.WP(msg,wrt_file)