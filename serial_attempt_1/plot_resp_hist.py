# -*- coding: utf-8 -*-
"""
Created on Thu May 08 14:40:31 2014

@author: nhpnp3
"""

import numpy as np
import mks_functions_serial as rr
import matplotlib.pyplot as plt

el = 21
ns = 1001
order = 7

micr = np.load('micr_%s.npy' %ns)
resp_val = np.load('resp_val.npy')
mks_R = np.load('mks_R_ord%s_%s.npy' %(order,ns))
mks_R1st = np.load('mks_R_ord%s_%s.npy' %(1,ns))

### VISUALIZATION OF MKS VS. FEM ###

plt.close()

## pick a slice perpendicular to the x-direction
slc = 7


## find the min and max of both datasets for the slice of interest
#(needed to scale both images the same) 
dmin = np.amin([resp_val[slc,:,:],mks_R[slc,:,:],mks_R1st[slc,:,:]])
dmax = np.amax([resp_val[slc,:,:],mks_R[slc,:,:],mks_R1st[slc,:,:]])

## Plot slices of the response
plt.subplot(231)
ax = plt.imshow(mks_R1st[slc,:,:], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('MKS, 1st order terms, E11')

plt.subplot(232)
ax = plt.imshow(mks_R[slc,:,:], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('MKS, 7th order terms, E11')

plt.subplot(233)
ax = plt.imshow(resp_val[slc,:,:], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('FE response, E11')   

# Plot a histogram representing the frequency of strain levels with separate
# channels for each phase of each type of response.
plt.subplot(212)

## find the min and max of both datasets (in full)
dmin = np.amin([resp_val,mks_R[:,:,:],mks_R1st[:,:,:]])
dmax = np.amax([resp_val,mks_R[:,:,:],mks_R1st[:,:,:]])

pm = np.zeros([el,el,el,ns,2])
pm[:,:,:,:,0] = (micr == 0)
pm[:,:,:,:,1] = (micr == 1)

# separating each response by phase
feb = rr.remzer(np.reshape(resp_val*pm[:,:,:,-1,1],el**3))
few = rr.remzer(np.reshape(resp_val*pm[:,:,:,-1,0],el**3))
mks1b = rr.remzer(np.reshape(mks_R1st[:,:,:]*pm[:,:,:,-1,1],el**3))
mks1w = rr.remzer(np.reshape(mks_R1st[:,:,:]*pm[:,:,:,-1,0],el**3))
mks2b = rr.remzer(np.reshape(mks_R[:,:,:]*pm[:,:,:,-1,1],el**3))
mks2w = rr.remzer(np.reshape(mks_R[:,:,:]*pm[:,:,:,-1,0],el**3))

del pm

# select the desired number of bins in the histogram
bn = 40

# FEM histogram
n, bins, patches = plt.hist(feb, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
bincenters = 0.5*(bins[1:]+bins[:-1])
febp, = plt.plot(bincenters,n,'k', linestyle = '--', lw = 1.5)

n, bins, patches = plt.hist(few, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
fewp, = plt.plot(bincenters,n,'k')

# 1st order terms MKS histogram
n, bins, patches = plt.hist(mks1b, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
mks1bp, = plt.plot(bincenters,n,'b', linestyle = '--', lw = 1.5)

n, bins, patches = plt.hist(mks1w, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
mks1wp, = plt.plot(bincenters,n,'b')

# 2nd order terms MKS histogram
n, bins, patches = plt.hist(mks2b, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
mks2bp, = plt.plot(bincenters,n,'r', linestyle = '--', lw = 1.5)

n, bins, patches = plt.hist(mks2w, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
mks2wp, = plt.plot(bincenters,n,'r')

plt.grid(True)

plt.legend([febp,fewp,mks1bp,mks1wp,mks2bp,mks2wp], ["FE - stiff phase", 
           "FE - compliant phase", "MKS, 1st order terms - stiff phase",
           "MKS, 1st order terms - compliant phase",
           "MKS, 7th order terms - stiff phase",
           "MKS, 7th order terms - compliant phase"])

plt.xlabel("Strain")
plt.ylabel("Frequency")
plt.title("Frequency comparison of order 1 and %s MKS with FE results" %order)

del micr,resp_val,mks_R,mks_R1st 
del febp,fewp,mks1bp,mks1wp,mks2bp,mks2wp

#### For plotting the delta and random microstructures
##
###plt.subplot(221)
###ax = plt.imshow(micr[slice,:,:,0], origin='lower', interpolation='none',
###    cmap='binary')
###plt.colorbar(ax)
###plt.title('Black delta microstructure')
###
###plt.subplot(222)
###ax = plt.imshow(micr[slice,:,:,1], origin='lower', interpolation='none',
###    cmap='binary')
###plt.colorbar(ax)
###plt.title('White delta microstructure')
###
###plt.subplot(223)
###ax = plt.imshow(micr[slice,:,:,2], origin='lower', interpolation='none',
###    cmap='binary')
###plt.colorbar(ax)
###plt.title('Validation microstructure')
##
###resp_fft_lin = np.reshape(resp_fft[:,:,:,-1],el**3).real
###freq = range(el**3)
###plt.plot(freq,resp_fft_lin,'b')