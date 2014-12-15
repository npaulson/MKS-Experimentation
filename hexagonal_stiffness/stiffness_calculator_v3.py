# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 09:52:43 2014

The following python code generates the elastic stiffness tensor and matrix
for a single hexagonal crystal given Bunge-Euler angles and the relevant
elastic stiffness constants in the reference frame.

@author: nhpnp3
"""

import numpy as np

def stiffness_calc(phi):
## phi: vector of bunge euler angles [phi1,Phi,phi2]
## Cs: 3x3x3x3 stiffness tensor
## CsM: 6x6 stiffness matrix

    # These are the Elastic Stiffness Constants
    C11 = 154
    C12 = 86
    C13 = 67
    C33 = 183
    C44 = 46

        
    z1 = np.array([[    np.cos(phi[0]), np.sin(phi[0]), 0],
                   [ -1*np.sin(phi[0]), np.cos(phi[0]), 0],
                   [                 0,              0, 1]])
    
    x = np.array([[ 1,                 0,              0],
                   [ 0,    np.cos(phi[1]), np.sin(phi[1])],
                   [ 0, -1*np.sin(phi[1]), np.cos(phi[1])]])
                   
    z2 = np.array([[    np.cos(phi[2]), np.sin(phi[2]), 0],
                   [ -1*np.sin(phi[2]), np.cos(phi[2]), 0],
                   [                 0,              0, 1]])
                   
    
    g = np.transpose(np.dot(z2,np.dot(x,z1))) # transformation matrix from crystal to sample
    
#    g = np.zeros([3,3])    
#    
#    g[0,0] = np.cos(phi[0])*np.cos(phi[2])-np.sin(phi[0])*np.sin(phi[2])*np.cos(phi[1]);
#    g[0,1] = np.sin(phi[0])*np.cos(phi[2])+np.cos(phi[0])*np.sin(phi[2])*np.cos(phi[1]);
#    g[0,2] = np.sin(phi[2])*np.sin(phi[1]);
#    g[1,0] = -np.cos(phi[0])*np.sin(phi[2])-np.sin(phi[0])*np.cos(phi[2])*np.cos(phi[1]);
#    g[1,1] = -np.sin(phi[0])*np.sin(phi[2])+np.cos(phi[0])*np.cos(phi[2])*np.cos(phi[1]);
#    g[1,2] = np.cos(phi[2])*np.sin(phi[1]);
#    g[2,0] = np.sin(phi[0])*np.sin(phi[1]);
#    g[2,1] = -np.cos(phi[0])*np.sin(phi[1]);
#    g[2,2] = np.cos(phi[1]);    
    
    Cs = np.zeros([3,3,3,3])
    
    for cc in xrange(3**4):
        [ii,jj,kk,ll] = np.unravel_index(cc,[3,3,3,3])
        
    
        A1 = 0    
        for tt in xrange(3):    
            A1 += g[ii,tt]*g[jj,tt]*g[kk,tt]*g[ll,tt] 
        
        A2 = 0.5*(g[ii,0]*g[jj,1]*g[kk,0]*g[ll,1]
                + g[ii,0]*g[jj,1]*g[kk,1]*g[ll,0]
                + g[ii,1]*g[jj,0]*g[kk,0]*g[ll,1]
                + g[ii,1]*g[jj,0]*g[kk,1]*g[ll,0])    
        
        A =  A1 + A2 
        
        B = 0
        
        for tt in xrange(2):
            B += g[ii,tt]*g[jj,tt]*g[kk,2]*g[ll,2]
            + g[ii,2]*g[jj,2]*g[kk,tt]*g[ll,tt]
    
        D = g[ii,2]*g[jj,2]*g[kk,2]*g[ll,2]    
        
        Cs[ii,jj,kk,ll] = C12 * int(ii==jj) * int(kk==ll) + C44 * (int(ii==kk) * \
                          int(jj==ll) + int(ii==ll) * int(kk==jj)) + (C11 - C12 -
                          2*C44) * A + (C13 - C12) * B + (C33 - C11) * D
    
    
    CsM = np.array([[Cs[0,0,0,0],Cs[0,0,1,1],Cs[0,0,2,2],Cs[0,0,1,2],Cs[0,0,0,2],Cs[0,0,0,1]],
                    [Cs[0,0,1,1],Cs[1,1,1,1],Cs[1,1,2,2],Cs[1,1,1,2],Cs[1,1,0,2],Cs[1,1,0,1]],
                    [Cs[0,0,2,2],Cs[1,1,2,2],Cs[2,2,2,2],Cs[2,2,1,2],Cs[2,2,0,2],Cs[2,2,0,1]],
                    [Cs[0,0,1,2],Cs[1,1,1,2],Cs[2,2,1,2],Cs[1,2,1,2],Cs[1,2,0,2],Cs[1,2,0,1]],
                    [Cs[0,0,0,2],Cs[1,1,0,2],Cs[2,2,0,2],Cs[1,2,0,2],Cs[0,2,0,2],Cs[0,2,0,1]],
                    [Cs[0,0,0,1],Cs[1,1,0,1],Cs[2,2,0,1],Cs[1,2,0,1],Cs[0,2,0,1],Cs[0,1,0,1]]])
                    
    return Cs, CsM
    
    
if __name__ == '__main__':
    [Cs,CsM] = stiffness_calc([0,0,0])
    print CsM