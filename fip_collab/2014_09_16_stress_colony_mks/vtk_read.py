# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 11:32:08 2014

@author: nhpnp3
"""

import functions_polycrystal_strain as rr
import numpy as np
import time
import os


def read_euler(ns, set_id, vtk_filename, newdir, wrt_file):

    start = time.time()        
    
    ## el is the # of elements per side of the cube 
    el = 21 
    
    euler = np.zeros([el**3,ns,3])

    ## change to directory with the .vtk files    
    cwd = os.getcwd()
    os.chdir(cwd + '\\' + newdir)
#    os.chdir(cwd + '/' + newdir) #for unix 
    
    for sn in xrange(ns):
        l_sn = str(sn+1).zfill(5)  
        euler[:,sn,:] = rr.read_vtk_vector(filename = vtk_filename %l_sn)

    ## return to the original directory
    os.chdir('..')
    
    np.save('euler_%s%s' %(ns,set_id), euler)
    
    end = time.time()
    timeE = np.round((end - start),3)

    
    msg = 'euler angles read from .vtk file for %s: %s seconds' %(set_id, timeE)
    rr.WP(msg,wrt_file)

    
def read_meas(ns, set_id, comp, vtk_filename, tensor_id, newdir, wrt_file):

    start = time.time() 

    ## el is the # of elements per side of the cube 
    el = 21 
    
    r_real = np.zeros([el,el,el,ns])
    
    ## change to directory with the .vtk files
    cwd = os.getcwd()
    os.chdir(cwd + '\\' + newdir)    
#    os.chdir(cwd + '/' + newdir) #for unix   
    
    for sn in xrange(ns):
        l_sn = str(sn+1).zfill(5)  
        r_temp = rr.read_vtk_tensor(filename = vtk_filename %l_sn, tensor_id = tensor_id, comp = comp)
        r_real[:,:,:,sn] = np.swapaxes(np.reshape(np.flipud(r_temp), [el,el,el]),1,2)

    ## return to the original directory    
    os.chdir('..')    
    
    np.save('r%s_%s%s' %(comp,ns,set_id), r_real)

    ## fftn of response fields    
    r_fft = np.fft.fftn(r_real, axes = [0,1,2]) 
    del r_real
    np.save('r%s_fft_%s%s' %(comp,ns,set_id),r_fft)  
    

    end = time.time()
    timeE = np.round((end - start),3)
    
    msg = 'The measure of interest has been read from .vtk file for %s, set %s: %s seconds' %(set_id,comp,timeE)
    rr.WP(msg,wrt_file)