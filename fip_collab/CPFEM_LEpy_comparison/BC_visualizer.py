# -*- coding: utf-8 -*-
"""
Written by Noah Paulson
7/29/2014

This script evaluates the success of a given MKS calibration and validation
through metrics like MASE and maximum error as well as plotting strain
fields and histograms.

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt

## el is the # of elements per side of the cube 
el = 21 


### READ DATA FROM TEXT FILE ###

filename = 'Results_Ti64_RandomMicroFZreducedNewBCs_21x21x21_AbqInp_AnisoLE_00001_data_strain_max_C3.txt'

f = open(filename, "r")

linelist = f.readlines()

# line0 is the index of first line of the data
line0 = 2;      

E11_pre = np.zeros((21**3))
c = -1

## This reads through all the lines in the file.
## column_num picks the component to save from the .txt file.
column_num = 3
 
for k in xrange(21**3):
    c += 1                        
    E11_pre[k] = linelist[line0 + c].split()[column_num]

f.close()    
     
resp = np.swapaxes(np.reshape(np.flipud(E11_pre), [el,el,el]),1,2)


### VISUALIZATION OF MKS VS. FEM ###

plt.close()

## pick a slice perpendicular to the x-direction
slc = 0

## find the min and max of both datasets for the slice of interest
#(needed to scale both images the same) 
dmin = np.amin([resp[:,:,0],resp[:,:,1],resp[:,:,2],resp[:,:,3],resp[:,:,17],resp[:,:,18],resp[:,:,19],resp[:,:,20]])
dmax = np.amax([resp[:,:,0],resp[:,:,1],resp[:,:,2],resp[:,:,3],resp[:,:,17],resp[:,:,18],resp[:,:,19],resp[:,:,20]])


## Plot slices of the response

plt.subplot(241)
ax = plt.imshow(resp[:,:,slc], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)

plt.subplot(242)
ax = plt.imshow(resp[:,:,slc+1], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)

plt.subplot(243)
ax = plt.imshow(resp[:,:,slc+2], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)

plt.subplot(244)
ax = plt.imshow(resp[:,:,slc+3], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)

plt.subplot(245)
ax = plt.imshow(resp[:,:,el-4], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)

plt.subplot(246)
ax = plt.imshow(resp[:,:,el-3], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)

plt.subplot(247)
ax = plt.imshow(resp[:,:,el-2], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)

plt.subplot(248)
ax = plt.imshow(resp[:,:,el-1], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
