# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script predicts the FE response of a set of microstructures designated by
a specific set-ID using a previously calibrated MKS

@author: nhpnp3
"""

import time
import numpy as np
import functions_polycrystal as rr

def validation_procedure(ns_cal,ns_val,set_id_cal,set_id_val,step,comp,wrt_file):

    start = time.time()

    ## el is the # of elements per side of the cube 
    el = 21
    ## H is the number of GSH coefficients    
    H = 15
    
    M = np.load('M_%s%s.npy' %(ns_val,set_id_val))
    specinfc = np.load('specinfc%s_%s%s_s%s.npy' %(comp,ns_cal,set_id_cal,step))
    
    mks_R = np.zeros([el,el,el,ns_val])
    
    for sn in xrange(ns_val):
        mks_R[:,:,:,sn] = rr.validate(M[:,:,:,sn,:],specinfc,H,el)
    
    np.save('mksR%s_%s%s_step%s_cal%s' %(comp,ns_val,set_id_val,step,ns_cal), mks_R)

    end = time.time()
    timeE = np.round((end - start),3)

    msg = 'validation performed for component %s: %s seconds' %(comp, timeE)
    rr.WP(msg,wrt_file)