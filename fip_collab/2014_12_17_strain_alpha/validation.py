# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script predicts the FE response of a set of microstructures designated by
a specific set-ID using a previously calibrated MKS

@author: nhpnp3
"""

import time
import numpy as np
import functions as rr

def validation_procedure(ns_cal,ns_val,set_id_cal,set_id_val,step,comp,wrt_file):

    start = time.time()

    ## el is the # of elements per side of the cube 
    el = 21
    ## H is the number of GSH coefficients    
    H = 15
    
    M = np.load('M_%s%s_s%s.npy' %(ns_val,set_id_val,step))
    specinfc = np.load('specinfc%s_%s%s_s%s.npy' %(comp,ns_cal,set_id_cal,step))
    specinfc = np.reshape(specinfc,[el,el,el,H]) 
    
    mks_R = np.zeros([el,el,el,ns_val])
    
    for sn in xrange(ns_val):
        mks_F = np.sum(np.conjugate(specinfc) * M[:,:,:,sn,:],3)
        mks_R[:,:,:,sn] = np.fft.ifftn(mks_F).real  
    
    
    np.save('mksR%s_%s%s_s%s' %(comp,ns_val,set_id_val,step), mks_R)

    end = time.time()
    timeE = np.round((end - start),3)

    msg = 'validation performed for component %s: %s seconds' %(comp, timeE)
    rr.WP(msg,wrt_file)