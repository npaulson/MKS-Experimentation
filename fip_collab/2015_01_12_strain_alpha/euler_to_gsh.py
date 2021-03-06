# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:45:46 2014

@author: nhpnp3
"""

import numpy as np
import GSH_func as gsh
import functions as rr
import time

def euler_to_gsh(el,H,ns,set_id,step,wrt_file):

    start = time.time()
    
    euler = np.load('euler_%s%s_s%s.npy' %(ns,set_id,step))    
        
    euler_GSH = np.zeros([ns,H,el**3], dtype= 'complex128')
    
    for sn in range(ns):
        
        euler_GSH[sn,:,:] = gsh.GSH_Hexagonal_Triclinic(euler[sn,:,:])        
    
    np.save('euler_GSH_%s%s_s%s.npy' %(ns,set_id,step),euler_GSH)
    
    end = time.time()
    timeE = np.round((end - start),3)    
    
    msg = "Conversion from Euler angles to GSH coefficients completed: %s seconds" %timeE
    rr.WP(msg, wrt_file)
    