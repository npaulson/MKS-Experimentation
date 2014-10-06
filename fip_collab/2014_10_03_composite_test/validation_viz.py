# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script predicts the FE response of a set of microstructures designated by
a specific set-ID using a previously calibrated MKS

@author: nhpnp3
"""

import time
import numpy as np
import functions_composite as rr
import matplotlib.pyplot as plt

def validation_zero_pad(el_cal,el_val,ns_cal,ns_val,H,set_id_cal,set_id_val,wrt_file):

    start = time.time()

    ## zero-pad the influence coefficients    
    pre_pre_specinfc = np.load('specinfc_%s%s.npy' %(ns_cal,set_id_cal)) 
    
    pre_specinfc= np.zeros([el_cal,el_cal,el_cal,H],dtype='complex64')
#    pre_specinfc = np.fft.ifftn(np.reshape(pre_specinfc,[el_cal,el_cal,el_cal,H]))  
    for h in xrange(H):
        pre_specinfc[:,:,:,h] = np.fft.ifftn(np.reshape(pre_pre_specinfc[:,h],[el_cal,el_cal,el_cal]))
    
    h_comp = 0
    plt.figure(num=1,figsize=[12,8])
    dmin = np.amin(pre_specinfc[0,:,:,h_comp].real)
    dmax = np.amax(pre_specinfc[0,:,:,h_comp].real)
    
    plt.subplot(221)
    ax = plt.imshow(pre_specinfc[0,:,:,h_comp].real, origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('original influence coefficients')  
    
    
    shift = np.floor(0.5*el_cal).astype(int)
    pre_specinfc = np.roll(np.roll(np.roll(pre_specinfc, shift, 0),shift,1),shift,2)   
    edgeHvec = pre_specinfc[0,0,0,:]  
    

    plt.subplot(222)
    slc = np.floor(0.5*el_cal).astype(int)
    ax = plt.imshow(pre_specinfc[slc,:,:,h_comp].real, origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('centered influence coefficients')  
    
    specinfc_pad = np.zeros([el_val,el_val,el_val, H],dtype='complex64')

#    for h in xrange(H):    
#        specinfc_pad[:,:,:,h] = edgeHvec[h]
    
    specinfc_pad[:el_cal,:el_cal,:el_cal,:] = pre_specinfc


    plt.subplot(223)
    slc = np.floor(0.5*el_cal).astype(int)
    ax = plt.imshow(specinfc_pad[slc,:,:,h_comp].real, origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('padded/centered influence coefficients')  
   
   
    specinfc_pad = np.roll(np.roll(np.roll(specinfc_pad, -shift, 0),-shift,1),-shift,2)
     
     
    plt.subplot(224)
    ax = plt.imshow(specinfc_pad[0,:,:,h_comp].real, origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('padded influence coefficients')    
    
    
    del pre_specinfc
    
#    specinfc = np.reshape(np.fft.fftn(specinfc_pad, axes = [0,1,2]),[el_large**3,H])
    specinfc = np.fft.fftn(specinfc_pad, axes = [0,1,2])
#    specinfc = specinfc_pad    
    
    del specinfc_pad


    ## debug section
    pre_specinfc2 = np.load('specinfc_%s%s.npy' %(ns_cal,set_id_cal))
    specinfc2 = np.reshape(pre_specinfc2,[el_cal,el_cal,el_cal,H])

    a = [0,0,1]
    print specinfc[a[0],a[1],a[2],:]
    print specinfc2[a[0],a[1],a[2],:]


    ## perform the prediction procedure    
    
    M = np.load('M_%s%s.npy' %(ns_val,set_id_val))
    
    mks_R = np.zeros([el_val,el_val,el_val,ns_val])
    
    for sn in xrange(ns_val):
#        specinfc_sqr = np.reshape(specinfc,[el_large,el_large,el_large,H])
#        mks_F = np.sum(np.conjugate(specinfc_sqr) * M[:,:,:,sn,:],3)
        mks_F = np.sum(np.conjugate(specinfc) * M[:,:,:,sn,:],3)
        mks_R[:,:,:,sn] = np.fft.ifftn(mks_F).real

    
    np.save('mksR_%s%s' %(ns_val,set_id_val), mks_R)

    end = time.time()
    timeE = np.round((end - start),3)

    msg = 'validation performed: %s seconds' %timeE
    rr.WP(msg,wrt_file)