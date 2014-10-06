# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script evaluates the success of a given MKS calibration and validation
through metrics like MASE and maximum error as well as plotting strain
fields and histograms.

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt


def results_comp(ns,set_id,comp,typ):
    
    ## vector of the indicial forms of the tensor components 
    real_comp_desig = ['11','12','13','21','22','23','31','32','33','vm']    
    real_comp = real_comp_desig[comp]

    mks_R = np.load('mksR%s_%s%s.npy' %(comp,ns,set_id))
    resp = np.load('r%s_%s%s.npy' %(comp,ns,set_id))

    
    ### VISUALIZATION OF MKS VS. FEM ###
    
    plt.close('all')
    
    ## pick a slice perpendicular to the x-direction
    slc = 11
    sn = 20
    
    
    ## find the min and max of both datasets for the slice of interest
    #(needed to scale both images the same) 
    dmin = np.amin([resp[:,:,slc,sn],mks_R[:,:,slc,sn]])
    dmax = np.amax([resp[:,:,slc,sn],mks_R[:,:,slc,sn]])
    
    
    ## Plot slices of the response
    plt.figure(num=1,figsize=[12,4])
    
    plt.subplot(121)
    ax = plt.imshow(mks_R[slc,:,:,sn], origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('MKS $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))
    
    plt.subplot(122)
    ax = plt.imshow(resp[slc,:,:,sn], origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('CPFEM $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))
    
    plt.savefig('field_comp%s_%s%s.png' %(comp,ns,set_id))                

          
if __name__ == '__main__':
    results_comp(50,'val',0,'sigma')