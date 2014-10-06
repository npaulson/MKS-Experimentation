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

def validation_zero_pad(el_large,ns_cal,ns_val,set_id_cal,set_id_val,step,comp,wrt_file):

    start = time.time()

    ## el is the # of elements per side of the calibration cube 
    el = 21
    ## H is the number of GSH coefficients    
    H = 15


    ## zero-pad the influence coefficients    
    pre_specinfc = np.load('specinfc%s_%s%s_s%s.npy' %(comp,ns_cal,set_id_cal,step))
        
    pre_specinfc = np.fft.ifftn(np.reshape(pre_specinfc,[el,el,el,H])).real
    
    shift = np.floor(0.5*el).astype(int)
    pre_specinfc =  np.roll(np.roll(np.roll(pre_specinfc, shift, 0),shift,1),shift,2)   
    
    specinfc_pad = np.zeros([el_large,el_large,el_large, H])
    
    specinfc_pad[:el,:el,:el,:] = pre_specinfc

    specinfc_pad = np.roll(np.roll(np.roll(specinfc_pad, -shift, 0),-shift,1),-shift,2)
   
    del pre_specinfc
    
    specinfc = np.reshape(np.fft.fftn(specinfc_pad, axes = [0,1,2]),[el_large**3,H])
    
    del specinfc_pad


    ## perform the prediction procedure    
    
    M = np.load('M_%s%s.npy' %(ns_val,set_id_val))
    
    mks_R = np.zeros([el_large,el_large,el_large,ns_val])
    
    for sn in xrange(ns_val):
        specinfc_sqr = np.reshape(specinfc,[el_large,el_large,el_large,H])
        mks_F = np.sum(np.conjugate(specinfc_sqr) * M[:,:,:,sn,:],3)
        mks_R[:,:,:,sn] = np.fft.ifftn(mks_F).real

    
    np.save('mksR%s_%s%s_step%s' %(comp,ns_val,set_id_val,step), mks_R)

    end = time.time()
    timeE = np.round((end - start),3)

    msg = 'validation performed for component %s: %s seconds' %(comp, timeE)
    rr.WP(msg,wrt_file)