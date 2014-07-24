# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script evaluates the success of a given MKS calibration and validation
through metrics like MASE and maximum error as well as plotting strain
fields and histograms.

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt

## el is the # of elements per side of the cube 
el = 21 

## the number of sample microstructures for validation.
ns = 50
## specify the set designation (string format)
set_id = 'val'


resp = np.load('E11_%s%s.npy' %(ns,set_id))


### VISUALIZATION OF MKS VS. FEM ###

plt.close()

## pick a slice perpendicular to the x-direction
slc = 0
sn = 48


## find the min and max of both datasets for the slice of interest
#(needed to scale both images the same) 
dmin = np.amin([resp[0,:,:,sn],resp[1,:,:,sn],resp[2,:,:,sn],resp[3,:,:,sn],resp[17,:,:,sn],resp[18,:,:,sn],resp[19,:,:,sn],resp[20,:,:,sn]])
dmax = np.amax([resp[0,:,:,sn],resp[1,:,:,sn],resp[2,:,:,sn],resp[3,:,:,sn],resp[17,:,:,sn],resp[18,:,:,sn],resp[19,:,:,sn],resp[20,:,:,sn]])


## Plot slices of the response

plt.subplot(241)
ax = plt.imshow(resp[slc,:,:,sn], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)

plt.subplot(242)
ax = plt.imshow(resp[slc+1,:,:,sn], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)

plt.subplot(243)
ax = plt.imshow(resp[slc+2,:,:,sn], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)

plt.subplot(244)
ax = plt.imshow(resp[slc+3,:,:,sn], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)

plt.subplot(245)
ax = plt.imshow(resp[el-4,:,:,sn], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)

plt.subplot(246)
ax = plt.imshow(resp[el-3,:,:,sn], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)

plt.subplot(247)
ax = plt.imshow(resp[el-2,:,:,sn], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)

plt.subplot(248)
ax = plt.imshow(resp[el-1,:,:,sn], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
