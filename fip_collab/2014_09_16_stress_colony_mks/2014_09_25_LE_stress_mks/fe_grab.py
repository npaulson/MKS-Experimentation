# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

@author: nhpnp3
"""

import time
import numpy as np
import os
import functions_polycrystal as rr

def fe_grab(ns, set_id, newdir, wrt_file):

    ## el is the # of elements per side of the cube 
    el = 21 
    
    ### FINITE ELEMENT RESPONSES ###

    ## change to directory with the .vtk files    
    cwd = os.getcwd()
#    os.chdir(cwd + '\\' + newdir)
    os.chdir(cwd + '/' + newdir) #for unix    
    
    [r_real_all, msg] = rr.load_fe('orientation_%s%s.mat' %(ns, set_id),set_id,ns,el)
    
    ## return to the original directory
    os.chdir('..')    
    
    
    start = time.time()    
    
    for comp in xrange(6):    
        
        np.save('r%s_%s%s' %(comp,ns,set_id), r_real_all[:,:,:,comp,:])   
        rr.WP(msg,wrt_file)
        
        ## responses in frequency space
        
        r_fft = np.fft.fftn(r_real_all[:,:,:,comp,:], axes = [0,1,2]) 
        np.save('r%s_fft_%s%s' %(comp,ns,set_id),r_fft)    
    
    end = time.time()
    timeE = np.round((end - start),3)
    
    msg = 'Convert FE results to frequency space: %s seconds' %timeE
    rr.WP(msg,wrt_file)