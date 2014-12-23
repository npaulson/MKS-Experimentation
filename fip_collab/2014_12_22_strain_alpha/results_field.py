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
    
    
#    pre_euler = np.load('euler_%s%s_s%s.npy' %(ns,set_id,step))
#
#    euler = np.zeros([ns,3,el,el,el])
#    for h in xrange(3):
#        for sn in range(ns):
#            euler[sn,h,...] = np.swapaxes(np.reshape(np.flipud
#                                    (pre_euler[sn,h,:]), [el,el,el]),1,2)

    
    tmp = np.load('euler_%s%s_s%s.npy' %(ns,set_id,step))
    euler = tmp.reshape([ns,3,el,el,el])

    del tmp    
    

    maxerr = (np.max(np.abs(resp - mks_R))/np.mean(resp))*100
    print maxerr

    ### VISUALIZATION OF MKS VS. FEM ###

    ## pick a slice perpendicular to the x-direction
    slc = 0
    sn = 8

    plt.close(1)

    ## Plot slices of the response
    plt.figure(num=1,figsize=[18,4])
 
    plt.subplot(131)
    ax = plt.imshow(euler[sn,0,slc,:,:], origin='lower', interpolation='none',
        cmap='jet')
    plt.colorbar(ax)
    plt.title('Microstructure, slice %s' % slc)

    plt.subplot(132)
    ax = plt.imshow(mks_R[sn,slc,:,:], origin='lower', interpolation='none',
        cmap='jet')
    plt.colorbar(ax)
    plt.title('MKS $\%s_{%s}$ response, slice %s' %(typ,comp,slc))
    
    plt.subplot(133)
    ax = plt.imshow(resp[sn,slc,:,:], origin='lower', interpolation='none',
        cmap='jet')
    plt.colorbar(ax)
    plt.title('CPFEM $\%s_{%s}$ response, slice %s' %(typ,comp,slc))


#    dmin = np.min([mks_R[sn,slc,:,:],resp[sn,slc,:,:]])
#    dmax = np.max([mks_R[sn,slc,:,:],resp[sn,slc,:,:]])
#    
#    plt.subplot(132)
#    ax = plt.imshow(mks_R[sn,slc,:,:], origin='lower', interpolation='none',
#        cmap='jet', vmin=dmin, vmax=dmax)
#    plt.colorbar(ax)
#    plt.title('MKS $\%s_{%s}$ response, slice %s' %(typ,comp,slc))
#    
#    plt.subplot(133)
#    ax = plt.imshow(resp[sn,slc,:,:], origin='lower', interpolation='none',
#        cmap='jet', vmin=dmin, vmax=dmax)
#    plt.colorbar(ax)
#    plt.title('CPFEM $\%s_{%s}$ response, slice %s' %(typ,comp,slc))
    
    
if __name__ == '__main__':
    results(21,100,'val',1,'11','epsilon')