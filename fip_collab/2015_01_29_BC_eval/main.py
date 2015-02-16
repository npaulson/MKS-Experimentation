# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 16:46:35 2014

@author: nhpnp3
"""

import functions as rr
import numpy as np
import matplotlib.pyplot as plt


filename = 'Results_Ti64_Dream3D_XYdirLoad_210microns_9261el_AbqInp_AnisoLE_005_data_v2_01.vtk'

el = 21

tensor_ID = 1       
## The tensorID determines the type of tensor data read from the .vtk file
## if tensorID == 0, we read the stress tensor        
## if tensorID == 1, we read the strain tensor        
## if tensorID == 2, we read the plastic strain tensor 

compl = ['11','22','33','12','23','31']

compd = {'11':0,'22':4,'33':8,'12':1,'23':5,'31':6}    

r_real = np.zeros([np.size(compl),el,el,el])
c = 0

for comp in compl:

    compp = compd[comp]    
    
    r_temp = rr.read_vtk_tensor(filename = filename, tensor_id = tensor_ID, comp = compp)
    r_real[c,...] = r_temp.reshape([el,el,el])
        
    print compl
    print np.mean(r_real[c,...])
        
        
    c += 1
        
euler = rr.read_vtk_vector(filename).reshape([3,el,el,el])


for dispcomp in xrange(np.size(compl)):

    plt.close(dispcomp)
    
    ## Plot slices of the response
    plt.figure(num=dispcomp,figsize=[14,6])
     
    plt.subplot(231)
    ax = plt.imshow(euler[0,0,:,:], origin='lower', interpolation='none',
        cmap='jet')
    plt.colorbar(ax)
    plt.title('Microstructure, slice 0')
       
    plt.subplot(232)
    ax = plt.imshow(euler[0,np.floor(0.5*el),:,:], origin='lower', interpolation='none',
        cmap='jet')
    plt.colorbar(ax)
    plt.title('Microstructure, slice %s' % np.floor(0.5*el))
    
    plt.subplot(233)
    ax = plt.imshow(euler[0,el-1,:,:], origin='lower', interpolation='none',
        cmap='jet')
    plt.colorbar(ax)
    plt.title('Microstructure, slice %s' % (el-1))     
    
    dmin = np.min(r_real[dispcomp,...])
    dmax = np.max(r_real[dispcomp,...])
    
    plt.subplot(234)
    ax = plt.imshow(r_real[dispcomp,0,:,:], origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('Response, slice 0')
    
    plt.subplot(235)
    ax = plt.imshow(r_real[dispcomp,np.floor(0.5*el),:,:], origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('Response, slice %s' % np.floor(0.5*el))
    
    plt.subplot(236)
    ax = plt.imshow(r_real[dispcomp,el-1,:,:], origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('Response, slice %s' % (el-1))