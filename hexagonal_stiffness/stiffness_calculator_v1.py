# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 09:52:43 2014

@author: nhpnp3
"""

import numpy as np
import itertools as it

C11 = 154
C12 = 86
C13 = 67
C33 = 183
C44 = 46

phi = np.array([172,8828,-54]); # Bunge Euler angles, ie phi1,Phi,phi2 in degrees
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

A = np.zeros([3,3,3,3])
B = np.zeros([3,3,3,3])
D = np.zeros([3,3,3,3])

for cc in xrange(3**4):
    [ii,jj,kk,ll] = np.unravel_index(cc,[3,3,3,3])
    
    A1 = 0    
    for tt in xrange(3):    
        A1 += g[ii,tt]*g[jj,tt]*g[kk,tt]*g[ll,tt] 
    
    A2 = 0.5*(g[ii,1]*g[jj,2]*g[kk,1]*g[ll,2] + 
              g[ii,1]*g[jj,2]*g[kk,2]*g[ll,1] + 
              g[ii,2]*g[jj,1]*g[kk,1]*g[ll,2] + 
              g[ii,2]*g[jj,1]*g[kk,2]*g[ll,1])    
    
    A[ii,jj,kk,ll] = A1 + A2 
    
    
    for tt in xrange(2):
        B += g[ii,tt]*g[jj,tt]*g[kk,3]*g[ll,3] + g[ii,3]*g[jj,3]*g[kk,tt]*g[ll,tt]

    D[ii,jj,kk,ll] = g[ii,3]*g[jj,3]*g[kk,3]*g[ll,3]