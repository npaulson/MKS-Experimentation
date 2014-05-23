# -*- coding: utf-8 -*-
"""
Created on Thu May 08 14:40:31 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt

el = 21
ns = 200
ns_val = 50
order = 1

micr_cal = np.load('micr_%s.npy' %ns)
micr_val = np.load('micr_%sval.npy' %ns_val )
resp_val = np.load('FE_results_50val.npy')
mks_R = np.load('MKS_R_ord%s_%s_old.npy' %(order,ns_val))

### VISUALIZATION OF MKS VS. FEM ###

plt.close()

## pick a slice perpendicular to the x-direction
slc = 6
sn = 49


## find the min and max of both datasets for the slice of interest
#(needed to scale both images the same) 
dmin = np.amin([resp_val[slc,:,:,0,sn],mks_R[slc,:,:,sn]])
dmax = np.amax([resp_val[slc,:,:,0,sn],mks_R[slc,:,:,sn]])


## Plot slices of the response
plt.subplot(221)
ax = plt.imshow(mks_R[slc,:,:,sn], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('MKS, 1st order terms, E11')

plt.subplot(222)
ax = plt.imshow(resp_val[slc,:,:,0,sn], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('FE response, E11')


# Plot a histogram representing the frequency of strain levels with separate
# channels for each phase of each type of response.
plt.subplot(212)

## find the min and max of both datasets (in full)
dmin = np.amin([resp_val[:,:,:,0,:],mks_R])
dmax = np.amax([resp_val[:,:,:,0,:],mks_R])

#pm = np.zeros([el,el,el,ns,2])
#pm[:,:,:,:,0] = (micr == 0)
#pm[:,:,:,:,1] = (micr == 1)
#
## separating each response by phase
#feb = rr.remzer(np.reshape(resp_val*pm[:,:,:,-1,1],el**3))
#few = rr.remzer(np.reshape(resp_val*pm[:,:,:,-1,0],el**3))
#mks1b = rr.remzer(np.reshape(mks_R[:,:,:]*pm[:,:,:,-1,1],el**3))
#mks1w = rr.remzer(np.reshape(mks_R[:,:,:]*pm[:,:,:,-1,0],el**3))
#
#del pm

fe = np.reshape(resp_val[:,:,:,0,:],ns_val*(el**3))
mks = np.reshape(mks_R,ns_val*(el**3))


# select the desired number of bins in the histogram
bn = 100

# FEM histogram
n, bins, patches = plt.hist(fe, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
bincenters = 0.5*(bins[1:]+bins[:-1])
fe, = plt.plot(bincenters,n,'k', linestyle = '-', lw = 1.5)

#n, bins, patches = plt.hist(few, bins = bn, histtype = 'step', hold = True,
#                            range = (dmin, dmax), color = 'white')
#fewp, = plt.plot(bincenters,n,'k')

# 1st order terms MKS histogram
n, bins, patches = plt.hist(mks, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
mks, = plt.plot(bincenters,n,'b', linestyle = '-', lw = 1.5)

#n, bins, patches = plt.hist(mks1w, bins = bn, histtype = 'step', hold = True,
#                            range = (dmin, dmax), color = 'white')
#mks1wp, = plt.plot(bincenters,n,'b')
#
## 2nd order terms MKS histogram
#n, bins, patches = plt.hist(mks2b, bins = bn, histtype = 'step', hold = True,
#                            range = (dmin, dmax), color = 'white')
#mks2bp, = plt.plot(bincenters,n,'r', linestyle = '--', lw = 1.5)
#
#n, bins, patches = plt.hist(mks2w, bins = bn, histtype = 'step', hold = True,
#                            range = (dmin, dmax), color = 'white')
#mks2wp, = plt.plot(bincenters,n,'r')

plt.grid(True)

plt.legend([fe, mks], ["FE response", "MKS, 1st order terms"])

plt.xlabel("Strain")
plt.ylabel("Frequency")
plt.title("Frequency comparison of 1st order MKS with FE results")

del micr_cal,micr_val,resp_val,mks_R

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