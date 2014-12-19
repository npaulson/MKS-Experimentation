# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 11:32:08 2014

@author: nhpnp3
"""

import functions as rr
import numpy as np
import time
import os


def read_euler(ns, set_id, step, newdir, wrt_file, funit):

    start = time.time()        
    
    ## el is the # of elements per side of the cube 
    el = 21 
    
    euler = np.zeros([el**3,ns,3])

#    nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir #for unix 
    os.chdir(nwd)

    sn = 0    
    for filename in os.listdir(nwd):
        if filename.endswith('%s.vtk' %step):  
            euler[:,sn,:] = rr.read_vtk_vector(filename = filename)
            sn += 1 

    if funit == 1:
        euler = euler * (np.pi/180.)

    ## return to the original directory
    os.chdir('..')
    
    np.save('euler_%s%s_s%s' %(ns,set_id,step), euler)
    
    end = time.time()
    timeE = np.round((end - start),3)

    
    msg = 'euler angles read from .vtk file for %s: %s seconds' %(set_id, timeE)
    rr.WP(msg,wrt_file)

    
def read_meas(ns, set_id, step, comp, tensor_id, newdir, wrt_file):

    start = time.time() 

    ## el is the # of elements per side of the cube 
    el = 21 
    
    r_real = np.zeros([el,el,el,ns])
    
#    nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir #for unix 
    os.chdir(nwd)

    compd = {'11':0,'22':4,'33':8,'12':1,'23':5,'31':6}    
    compp = compd[comp]    

    sn = 0    
    for filename in os.listdir(nwd):
        if filename.endswith('%s.vtk' %step):  
            r_temp = rr.read_vtk_tensor(filename = filename, tensor_id = tensor_id, comp = compp)
            r_real[:,:,:,sn] = np.swapaxes(np.reshape(np.flipud(r_temp), [el,el,el]),1,2)
            sn += 1             
            
    ## return to the original directory    
    os.chdir('..')    
    
    np.save('r%s_%s%s_s%s' %(comp,ns,set_id,step), r_real)

    ## fftn of response fields    
    r_fft = np.fft.fftn(r_real, axes = [0,1,2]) 
    del r_real
    np.save('r%s_fft_%s%s_s%s' %(comp,ns,set_id,step),r_fft)  
    

    end = time.time()
    timeE = np.round((end - start),3)
    
    msg = 'The measure of interest has been read from .vtk file for %s, set %s: %s seconds' %(set_id,comp,timeE)
    rr.WP(msg,wrt_file)