# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 13:52:33 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt

def results(el,ns,set_id,typ):

    ## vector of the indicial forms of the tensor components 
    real_comp = '11'
    
    mks_R = np.load('mksR_%s%s.npy' %(ns,set_id))
    resp = np.load('r_%s%s.npy' %(ns,set_id)).reshape([ns,el,el,el])

    ### VISUALIZATION OF MKS VS. FEM ###
    
    ## pick a slice perpendicular to the x-direction
    slc = 24
    sn = 2

    ## Plot slices of the response
    plt.figure(num=2,figsize=[12,4])
    
    plt.subplot(121)
    ax = plt.imshow(mks_R[sn,slc,:,:], origin='lower', interpolation='none',
        cmap='jet')#, vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('MKS $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))
    
    plt.subplot(122)
    ax = plt.imshow(resp[sn,slc,:,:], origin='lower', interpolation='none',
        cmap='jet')#, vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('CPFEM $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))
    
    print np.mean(mks_R)
    print np.mean(resp)
    print np.std(mks_R)
    print np.std(resp)

    plt.show()	
    

if __name__ == '__main__':
    results(25,5,'val25el','sigma')
 