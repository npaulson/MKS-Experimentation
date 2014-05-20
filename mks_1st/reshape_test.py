# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 10:08:22 2014

This script helped me make sure that I was indexing my 3d matrices the same
way Yuksel does when he generates his FE results. As of 4/9/14 I am not sure 
whether I will eventually switch to a more intuitive (for me) data format.

@author: nhpnp3
"""
import matplotlib.pyplot as plt
import numpy as np

plt.close()

c = np.flipud(np.arange(3**3))
print c
d = np.reshape(c,[3,3,3])
g = np.swapaxes(d,1,2)
print g[2,:,:]
print g[0,0,0]
print g[2,2,2]
print g[2,1,2]

#gfft = np.fft.fftn(g)
#print gfft[0,:,:]
#print gfft

g_lin = np.reshape(g,[1,27])
print g_lin

g_lin_cube = np.reshape(g_lin,[3,3,3])
print g_lin_cube[2,:,:]

fig = plt.figure()
x = np.linspace(-np.pi,np.pi,100)
y = 2*np.sin(x)

ax = fig.add_subplot(1,2,1)
ax.plot(x,y)

ax = fig.add_subplot(1,2,2)
ax.plot(x,2*y)

#print np.amax([g, 2*g])