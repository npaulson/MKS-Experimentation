# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:45:46 2014

@author: nhpnp3
"""

import numpy as np
import GSH_func as gsh
import functions_polycrystal as rr
import time

def euler_to_gsh(el,ns,set_id,wrt_file):

    start = time.time()

    H = 15    
    
    euler = np.load('euler_%s%s.npy' %(ns,set_id))
    
    euler_GSH = np.zeros([el**3,ns,H], dtype= 'complex128')
    
    for sn in range(ns):
        for k in range(el**3):
            euler_GSH[k,sn,:] = gsh.GSH_Hexagonal_Triclinic(euler[k,sn,:])
        print sn
    
    np.save('euler_GSH_%s%s.npy' %(ns,set_id),euler_GSH)
    
    end = time.time()
    timeE = np.round((end - start),3)    
    
    msg = "Conversion from Euler angles to GSH coefficients completed: %s seconds" %timeE
    rr.WP(msg, wrt_file)