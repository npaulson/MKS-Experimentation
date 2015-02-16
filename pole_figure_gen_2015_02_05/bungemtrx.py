# -*- coding: utf-8 -*-
"""
Created on Thu Feb 05 15:06:31 2015

@author: nhpnp3
"""

import numpy as np

def bungemtrx(euler,israd):
    
    if israd != 1:    
        euler = euler * (np.pi/180)

    phi1 = euler[:,0]
    Phi = euler[:,1]
    phi2 = euler[:,2]
                        
    g = np.zeros([euler.shape[0],3,3])        
        
    g[:,0,0] = np.cos(phi1)*np.cos(phi2)-np.sin(phi1)*np.sin(phi2)*np.cos(Phi)
    g[:,0,1] = np.sin(phi1)*np.cos(phi2)+np.cos(phi1)*np.sin(phi2)*np.cos(Phi)
    g[:,0,2] = np.sin(phi2)*np.sin(Phi)
    g[:,1,0] = -np.cos(phi1)*np.sin(phi2)-np.sin(phi1)*np.cos(phi2)*np.cos(Phi)
    g[:,1,1] = -np.sin(phi1)*np.sin(phi2)+np.cos(phi1)*np.cos(phi2)*np.cos(Phi)
    g[:,1,2] = np.cos(phi2)*np.sin(Phi)
    g[:,2,0] = np.sin(phi1)*np.sin(Phi)
    g[:,2,1] = -np.cos(phi1)*np.sin(Phi)
    g[:,2,2] = np.cos(Phi)
    
    return g