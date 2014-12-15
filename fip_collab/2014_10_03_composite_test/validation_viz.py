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
    pre_specinfc = np.load('specinfc_%s%s.npy' %(ns_cal,set_id_cal)) 
    pre_specinfc = np.reshape(pre_specinfc,[el_cal,el_cal,el_cal,H])
    pre_specinfc = np.fft.ifftn(pre_specinfc,[el_cal,el_cal,el_cal],[0,1,2])
    
    h_comp = 0
    plt.figure(num=1,figsize=[12,8])
    dmin = np.amin(pre_specinfc[0,:,:,h_comp].real)
    dmax = np.amax(pre_specinfc[0,:,:,h_comp].real)
    
    plt.subplot(221)
    ax = plt.imshow(pre_specinfc[0,:,:,h_comp].real, origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('original influence coefficients')  
    
    pre_specinfc = np.fft.fftshift(pre_specinfc, axes = [0,1,2])    
    
#    edgeHvec = pre_specinfc[0,0,0,:]  

    plt.subplot(222)
    slc = np.floor(0.5*el_cal).astype(int)
    ax = plt.imshow(pre_specinfc[slc,:,:,h_comp].real, origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('centered influence coefficients')  
    
    specinfc_pad = np.zeros([el_val,el_val,el_val, H],dtype='complex64')

#    for h in xrange(H):    
#        specinfc_pad[:,:,:,h] = edgeHvec[h]

    el_gap = int(0.5*(el_val-el_cal))
    el_end = el_val - el_gap    
    specinfc_pad[el_gap:el_end,el_gap:el_end,el_gap:el_end,:] = pre_specinfc    
    del pre_specinfc

    plt.subplot(223)
    slc = np.floor(0.5*el_val).astype(int)
    ax = plt.imshow(specinfc_pad[slc,:,:,h_comp].real, origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('padded/centered influence coefficients')  
   
   
    specinfc_pad = np.fft.ifftshift(specinfc_pad, axes = [0,1,2])  
     
    plt.subplot(224)
    ax = plt.imshow(specinfc_pad[0,:,:,h_comp].real, origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('padded influence coefficients')    
   
    
    
    specinfc = np.fft.fftn(specinfc_pad, axes = [0,1,2])       
    

    ## perform the prediction procedure    
    
    M = np.load('M_%s%s.npy' %(ns_val,set_id_val))
    
    mks_R = np.zeros([el_val,el_val,el_val,ns_val])
    
    
    for sn in xrange(ns_val):
        mks_F = np.sum(np.conjugate(specinfc) * M[:,:,:,sn,:],3)
        mks_R[:,:,:,sn] = np.fft.ifftn(mks_F).real
    
#    print M.shape
#    temp = np.swapaxes(M,0,3)
#    print temp.shape
#    mks_R = np.sum(np.conjugate(specinfc) * temp, 4)
#    print mks_R.shape
#    mks_R = np.swapaxes(mks_R,0,3)
#    print mks_R.shape     
#    mks_R = np.fft.ifftn(mks_R,[el_val,el_val,el_val],[0,1,2]).real
#    print mks_R.shape    
 

    
    np.save('mksR_%s%s' %(ns_val,set_id_val), mks_R)

    end = time.time()
    timeE = np.round((end - start),3)

    msg = 'validation performed: %s seconds' %timeE
    rr.WP(msg,wrt_file)
    
    
#    # write to vtk file    
#    
#    from pyevtk.hl import gridToVTK    
#    
#    maxx = maxy = maxz = el_val + 1
#    x = np.arange(0, maxx, 1, dtype='float64')
#    y = np.arange(0, maxy, 1, dtype='float64') 
#    z = np.arange(0, maxz, 1, dtype='float64')
#    
#    gridToVTK("testvtk", x, y, z, cellData = {"specinfc_real" : specinfc_pad[:,:,:,0].real, "specinfc_imaginary" : specinfc_pad[:,:,:,0].imag})
