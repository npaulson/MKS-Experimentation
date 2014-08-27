# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 15:59:54 2014

@author: nhpnp3
"""
import numpy as np
import functions_small as fs
import matplotlib.pyplot as plt

dat1 = fs.res_red(filename = 'Priddy_changed_BCs_and_NodeSets.dat')

dat2 = fs.res_red(filename = 'Yuksel_BCs.dat')

if np.all(dat1 == dat2) == True:
    print "fields are equal"
else:
    print "fields are not equal"

slc = 1
    
dmin = np.amin([dat1[slc,:,:,0],dat2[slc,:,:,0]])
dmax = np.amax([dat1[slc,:,:,0],dat2[slc,:,:,0]])

plt.subplot(121)
ax = plt.imshow(dat1[slc,:,:,0], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.title('MINED BCs')
plt.colorbar(ax)  

plt.subplot(122)
ax = plt.imshow(dat2[slc,:,:,0], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.title('GOALI Ti BCs')
plt.colorbar(ax)    