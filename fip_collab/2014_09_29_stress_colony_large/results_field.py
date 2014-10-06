# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 13:52:33 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt

def results(el,ns,set_id,step,comp,typ):


    ## vector of the indicial forms of the tensor components 
    real_comp_desig = ['11','12','13','21','22','23','31','32','33','vm']    
         
    real_comp = real_comp_desig[comp]
    
    mks_R = np.load('mksR%s_%s%s_step%s.npy' %(comp,ns,set_id,step))
    resp = np.load('r%s_%s%s_s%s.npy' %(comp,ns,set_id,step))
    

    ### VISUALIZATION OF MKS VS. FEM ###

    
    ## pick a slice perpendicular to the x-direction
    slc = 11
    sn = 0


    ## Plot slices of the response
    plt.figure(num=2,figsize=[12,4])
    
    plt.subplot(121)
    ax = plt.imshow(mks_R[slc,:,:,sn], origin='lower', interpolation='none',
        cmap='jet')#, vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('MKS $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))
    
    plt.subplot(122)
    ax = plt.imshow(resp[slc,:,:,sn], origin='lower', interpolation='none',
        cmap='jet')#, vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('CPFEM $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))