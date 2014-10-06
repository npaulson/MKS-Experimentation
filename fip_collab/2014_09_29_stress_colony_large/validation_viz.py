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
import matplotlib.pyplot as plt

def validation_zero_pad(el_large,ns_cal,ns_val,set_id_cal,set_id_val,step,comp,wrt_file):

    start = time.time()

    ## el is the # of elements per side of the calibration cube 
    el = 21
    ## H is the number of GSH coefficients    
    H = 15

    ## zero-pad the influence coefficients    
    pre_specinfc = np.load('specinfc%s_%s%s_s%s.npy' %(comp,ns_cal,set_id_cal,step)) 
    
#    pre_specinfc = np.fft.ifftn(np.reshape(pre_specinfc,[el,el,el,H])).real
    pre_specinfc = np.fft.ifftn(np.reshape(pre_specinfc,[el,el,el,H]))
    
    print 'pre_specinfc[1,1,1,:]'
    print pre_specinfc[1,1,1,:]
    print pre_specinfc[11,11,11,:]    
    
    h_comp = 12
    plt.figure(num=1,figsize=[12,8])
    dmin = np.amin(pre_specinfc[0,:,:,h_comp].real)
    dmax = np.amax(pre_specinfc[0,:,:,h_comp].real)
    
    plt.subplot(221)
    ax = plt.imshow(pre_specinfc[0,:,:,h_comp].real, origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('original influence coefficients')  
    
    
    shift = np.floor(0.5*el).astype(int)
    pre_specinfc = np.roll(np.roll(np.roll(pre_specinfc, shift, 0),shift,1),shift,2)   
    edgeHvec = pre_specinfc[0,0,0,:]  
    
    print edgeHvec

    plt.subplot(222)
    slc = np.floor(0.5*el).astype(int)
    ax = plt.imshow(pre_specinfc[slc,:,:,h_comp].real, origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('centered influence coefficients')  
    
    specinfc_pad = np.zeros([el_large,el_large,el_large, H], dtype = 'complex64')

#    for h in xrange(H):    
#        specinfc_pad[:,:,:,h] = edgeHvec[h]
    
    specinfc_pad[:el,:el,:el,:] = pre_specinfc


    plt.subplot(223)
    slc = np.floor(0.5*el).astype(int)
    ax = plt.imshow(specinfc_pad[slc,:,:,h_comp].real, origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('padded/centered influence coefficients')  
   
   
    specinfc_pad = np.roll(np.roll(np.roll(specinfc_pad, -shift, 0),-shift,1),-shift,2)
    print 'specinfc_pad[1,1,1,:]'    
    print specinfc_pad[1,1,1,:]
     
    plt.subplot(224)
    ax = plt.imshow(specinfc_pad[0,:,:,h_comp].real, origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('padded influence coefficients')    
    
    
    del pre_specinfc
    
#    specinfc = np.reshape(np.fft.fftn(specinfc_pad, axes = [0,1,2]),[el_large**3,H])
    specinfc = np.fft.fftn(specinfc_pad, axes = [0,1,2])
    
    del specinfc_pad


    ## perform the prediction procedure    
    
    M = np.load('M_%s%s.npy' %(ns_val,set_id_val))
    
    mks_R = np.zeros([el_large,el_large,el_large,ns_val])
    
    for sn in xrange(ns_val):
#        specinfc_sqr = np.reshape(specinfc,[el_large,el_large,el_large,H])
#        mks_F = np.sum(np.conjugate(specinfc_sqr) * M[:,:,:,sn,:],3)
        mks_F = np.sum(np.conjugate(specinfc) * M[:,:,:,sn,:],3)
        mks_R[:,:,:,sn] = np.fft.ifftn(mks_F).real

    
    np.save('mksR%s_%s%s_step%s' %(comp,ns_val,set_id_val,step), mks_R)

    end = time.time()
    timeE = np.round((end - start),3)

    msg = 'validation performed for component %s: %s seconds' %(comp, timeE)
    rr.WP(msg,wrt_file)