# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 13:52:33 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt

def results(el,ns,set_id,step,comp,typ):

    
    mks_R = np.load('mksR%s_%s%s_s%s.npy' %(comp,ns,set_id,step))
    resp = np.load('r%s_%s%s_s%s.npy' %(comp,ns,set_id,step))

    maxerr = (np.max(np.abs(resp - mks_R))/np.mean(resp))*100
    print maxerr

    ### VISUALIZATION OF MKS VS. FEM ###

    ## pick a slice perpendicular to the x-direction
    slc = 10
    sn = 0

    dmin = np.min([mks_R[slc,:,:,sn],resp[slc,:,:,sn]])
    dmax = np.max([mks_R[slc,:,:,sn],resp[slc,:,:,sn]])


    ## Plot slices of the response
    plt.figure(num=2,figsize=[12,4])
    
    plt.subplot(121)
    ax = plt.imshow(mks_R[slc,:,:,sn], origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('MKS $\%s_{%s}$ response, slice %s' %(typ,comp,slc))
    
    plt.subplot(122)
    ax = plt.imshow(resp[slc,:,:,sn], origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('CPFEM $\%s_{%s}$ response, slice %s' %(typ,comp,slc))
    
if __name__ == '__main__':
    results(21,50,'val',1,'11','sigma')