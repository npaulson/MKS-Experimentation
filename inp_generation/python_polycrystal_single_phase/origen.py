# -*- coding: utf-8 -*-
"""
Created on Wed Sep 03 12:30:03 2014

@author: nhpnp3
"""

import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

el = 21
set_id = 'test'
ii = 5
ns = 1

ori = np.zeros([3,3,el**3,ns])

orih = sio.loadmat('extremeorientv_hexa.mat')['extremeorienth']
orih_fr = sio.loadmat('extremeorientv_hexa.mat')['extremeorienth_fr']


ct = np.zeros([el**3, ns])

for sn in xrange(ns):
    
    c = np.round((len(orih[:,0]) - 1)*np.random.rand(el**3)).astype('int16')
    ct[:,sn] = c

    print c    
    
    euler = orih[c,:]    
    
#    fig = plt.figure()
#    ax3D = fig.add_subplot(111, projection='3d')
#    p3d = ax3D.scatter(euler[:1000,0],euler[:1000,1],euler[:1000,2])
    
    g = np.zeros([3,3,el**3])
    
    for ii in xrange(el**3):
        
        Z1=[[ cos(euler[ii,0]), sin(euler[ii,0]),                0],
            [-sin(euler[ii,0]), cos(euler[ii,0]),                0],
            [                0,                0,                1]]

        X= [[                1,                0,                0],
            [                0, cos(euler[ii,1]), sin(euler[ii,1])],
            [                0,-sin(euler[ii,1]), cos(euler[ii,1])]]

        Z2=[[ cos(euler[ii,2]), sin(euler[ii,2]),                0],
            [-sin(euler[ii,2]), cos(euler[ii,2]),                0],
            [                0,                0,                1];
        
        g[:,:,ii] = Z2*X*Z1;        