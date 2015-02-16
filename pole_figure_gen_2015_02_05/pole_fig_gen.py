# -*- coding: utf-8 -*-
"""
Created on Thu Feb 05 14:35:08 2015

@author: nhpnp3
"""

#import scipy.io as sio
import bungemtrx as bm
import numpy as np
import matplotlib.pyplot as plt


#cubicsym = sio.loadmat('cubicsym.mat')['sym'].swapaxes(0,2)
#euler = sio.loadmat('euler_out.mat')['euler']
#np.save('cubicsym',cubicsym)
#np.save('euler_out', euler)

cubicsym = np.load('cubicsym.npy')
euler = np.load('euler_out.npy')

axes1 = np.array([[0,1.2],[1.2,0]])

plt.close()

fig = plt.figure(num=1,figsize=[7,7])

# plot axes
plt.plot([0,1.2],[0,0],'b')
plt.plot([0,0],[0,1.2],'b')

# plot circle
rads = np.linspace(0,2*np.pi,100)
circle = np.array([np.cos(rads),np.sin(rads)]).T;

plt.plot(circle[:,0],circle[:,1],'b')
plt.axis([-1.3, 1.3, -1.3, 1.3])

# label plot
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('BCC Pole Figure, Plane Strain Compression')

#normaldir = np.array([1,0,0]);
normaldir = np.array([1/np.sqrt(3), 1/np.sqrt(3), 1/np.sqrt(3)]);


g = bm.bungemtrx(np.array([[90,35,45]]),0)

for jj in xrange(24):
    
    g_ = np.dot(cubicsym[jj,...],g)
    H_ = np.dot(g_.T,normaldir)
    
    if H_[2] > -.0001:
            Theta = np.arccos(H_[2])
            Phi = np.arctan2(H_[1],H_[0])
            px = np.tan(Theta/2) * np.cos(Phi)
            py = np.tan(Theta/2) * np.sin(Phi)
            
            # plot3([0,H_(0)],[0,H_(1)],[0,H_(2)])
            plt.plot(px,py,'bo');
            
        


