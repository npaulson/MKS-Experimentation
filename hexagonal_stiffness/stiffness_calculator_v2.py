# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 09:52:43 2014

@author: nhpnp3
"""

import numpy as np

C11 = 154
C12 = 86
C13 = 67
C33 = 183
C44 = 46

phi = np.array([25,45,12]); # Bunge Euler angles, ie phi1,Phi,phi2 in degrees
phi = phi*(np.pi/180); # Bunge Euler angles in radians

z1 = np.array([[    np.cos(phi[0]), np.sin(phi[0]), 0],
               [ -1*np.sin(phi[0]), np.cos(phi[0]), 0],
               [                 0,              0, 1]])

x = np.array([[ 1,                 0,              0],
               [ 0,    np.cos(phi[1]), np.sin(phi[1])],
               [ 0, -1*np.sin(phi[1]), np.cos(phi[1])]])
               
z2 = np.array([[    np.cos(phi[2]), np.sin(phi[2]), 0],
               [ -1*np.sin(phi[2]), np.cos(phi[2]), 0],
               [                 0,              0, 1]])
               
g = np.dot(z2,np.dot(x,z1))

print g

Cs = np.zeros([3,3,3,3])

#for cc in xrange(3**4):
#    [ii,jj,kk,ll] = np.unravel_index(cc,[3,3,3,3])
    
    
for ii in xrange(3):
    for jj in xrange(3):
        for kk in xrange(3):
            for ll in xrange(3):

                A1 = 0    
                for tt in xrange(3):    
#                    A1 += g[ii,tt]*g[jj,tt]*g[kk,tt]*g[ll,tt] 
                    A1 = A1 +  g[ii,tt]*g[jj,tt]*g[kk,tt]*g[ll,tt] 

                
                A2 = 0.5*(g[ii,0]*g[jj,1]*g[kk,0]*g[ll,1] + 
                          g[ii,0]*g[jj,1]*g[kk,1]*g[ll,0] + 
                          g[ii,1]*g[jj,0]*g[kk,0]*g[ll,1] + 
                          g[ii,1]*g[jj,0]*g[kk,1]*g[ll,0])    
                
                A =  A1 + A2 
            #    print A    
                
                B = 0
                
                for tt in xrange(2):
                    B += g[ii,tt]*g[jj,tt]*g[kk,2]*g[ll,2]
                    + g[ii,2]*g[jj,2]*g[kk,tt]*g[ll,tt]
            #    print B
            
                D = g[ii,2]*g[jj,2]*g[kk,2]*g[ll,2]
            #    print D    
                
                
                Cs[ii,jj,kk,ll] = C12 * int(ii==jj) * int(kk==ll)
                + C44 * (int(ii==kk) * int(jj==ll) + int(ii==ll) * int(kk==jj))
                + (C11 - C12 - 2*C44) * A
                + (C13 - C12) * B
                + (C33 - C11) * D


CsM = np.array([[Cs[0,0,0,0],Cs[0,0,1,1],Cs[0,0,2,2],Cs[0,0,1,2],Cs[0,0,0,2],Cs[0,0,0,1]],
                [Cs[0,0,1,1],Cs[1,1,1,1],Cs[1,1,2,2],Cs[1,1,1,2],Cs[1,1,0,2],Cs[1,1,0,1]],
                [Cs[0,0,2,2],Cs[1,1,2,2],Cs[2,2,2,2],Cs[2,2,1,2],Cs[2,2,0,2],Cs[2,2,0,1]],
                [Cs[0,0,1,2],Cs[1,1,1,2],Cs[2,2,1,2],Cs[1,2,1,2],Cs[1,2,0,2],Cs[1,2,0,1]],
                [Cs[0,0,0,2],Cs[1,1,0,2],Cs[2,2,0,2],Cs[1,2,0,2],Cs[0,2,0,2],Cs[0,2,0,1]],
                [Cs[0,0,0,1],Cs[1,1,0,1],Cs[2,2,0,1],Cs[1,2,0,1],Cs[0,2,0,1],Cs[0,1,0,1]]])
                
print CsM