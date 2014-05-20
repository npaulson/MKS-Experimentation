# -*- coding: utf-8 -*-
"""
3D, Isotropic, 2st Order MKS

This script calibrates against reference datasets and plots the FE and MKS
response for a validation microstructure.

I have made most of the essential peices of code into functions so that this
code is effective for varying order analyses

Noah Paulson, 4/28/2014
"""

import time
import numpy as np
import mks_functions as rr
import matplotlib.pyplot as plt
#import scipy.io as sio

## el is the # of elements per side of the cube 
el = 21 
## select which order terms with nearest neighbors you would like to analyze
order = 1

 
### THE MICROSTRUCTURE FUNCTION ###

## import delta and random microstructures
[micr, ns, timeE] = rr.pha_loc("cont5_micr151.txt",1,el)
print "Import microstructures: %s seconds" %timeE

# Black cells = 1, White cells = 0
# The black delta has a high stiffness cell surrounded by low stiffness cells,
# The white delta has a low stiffness cell surrounded by high stiffness cells

## microstructure functions
[m,H,pm,timeE] = rr.mf(micr,el,ns,order)
print "Microstructure function generation: %s seconds" %timeE

    
## Microstructure functions in frequency space
start = time.time()
M = np.fft.fftn(m, axes = [0,1,2])
end = time.time()
timeE = np.round((end - start),2)
print "Convert microstructure function to frequency space: %s seconds" %timeE


### FINITE ELEMENT RESPONSES ###
resp = rr.load_fe(0,ns,el) 
## responses in frequency space
start = time.time()
resp_fft = np.fft.fftn(resp, axes = [0,1,2]) 
end = time.time()
timeE = np.round((end - start),3)
print "Convert FE results to frequency space: %s seconds" %timeE


### CALIBRATION OF INFLUENCE COEFFICIENTS ###
[specinfc,timeE] = rr.calibrator(M, resp_fft, H, el, ns)
print "Calibration: %s seconds" %timeE

print specinfc.nbytes

### VALIDATION WITH RANDOM ARRANGEMENT ###
mks_R = rr.validate(M,specinfc,H,el)
np.save('MKS_R', mks_R)

### MEAN ABSOLUTE STRAIN ERROR (MASE) ###
[avgE, MASE] = rr.eval_meas(mks_R,resp,el)
print "The average strain is %s" %avgE
print "The mean absolute strain error (MASE) is %s%%" %(MASE*100)


### VISUALIZATION OF MKS VS. FEM ###

plt.close()

## pick a slice perpendicular to the x-direction
slc = 10

## load the 1st order terms results
mks_R1st = np.load('MKS_1stOrd_resp.npy')

## find the min and max of both datasets for the slice of interest
#(needed to scale both images the same) 
dmin = np.amin([resp[slc,:,:,-1],mks_R[slc,:,:],mks_R1st[slc,:,:]])
dmax = np.amax([resp[slc,:,:,-1],mks_R[slc,:,:],mks_R1st[slc,:,:]])

## Plot slices of the response
plt.subplot(231)
ax = plt.imshow(mks_R1st[slc,:,:], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('MKS 1st order terms, E11')

plt.subplot(232)
ax = plt.imshow(mks_R[slc,:,:], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('MKS 2nd order terms, E11')

plt.subplot(233)
ax = plt.imshow(resp[slc,:,:,-1], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('FE response, E11')   

# Plot a histogram representing the frequency of strain levels with separate
# channels for each phase of each type of response.
plt.subplot(212)

## find the min and max of both datasets (in full)
dmin = np.amin([resp[:,:,:,-1],mks_R[:,:,:],mks_R1st[:,:,:]])
dmax = np.amax([resp[:,:,:,-1],mks_R[:,:,:],mks_R1st[:,:,:]])

# separating each response by phase
feb = rr.remzer(np.reshape(resp[:,:,:,-1]*pm[:,:,:,-1,1],el**3))
few = rr.remzer(np.reshape(resp[:,:,:,-1]*pm[:,:,:,-1,0],el**3))
mks1b = rr.remzer(np.reshape(mks_R1st[:,:,:]*pm[:,:,:,-1,1],el**3))
mks1w = rr.remzer(np.reshape(mks_R1st[:,:,:]*pm[:,:,:,-1,0],el**3))
mks2b = rr.remzer(np.reshape(mks_R[:,:,:]*pm[:,:,:,-1,1],el**3))
mks2w = rr.remzer(np.reshape(mks_R[:,:,:]*pm[:,:,:,-1,0],el**3))

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
           "MKS, 2nd order terms - stiff phase",
           "MKS, 2nd order terms - compliant phase"])

plt.xlabel("Strain")
plt.ylabel("Frequency")
plt.title("Frequency comparison of 1st and 2nd order MKS with FE results")

#del MM, PM, M, lin_M, specinfc, lin_sum, mks_F, m, micr, pm
#del febp, fewp, mksbp, mkswp, ax

### For plotting the delta and random microstructures
#
##plt.subplot(221)
##ax = plt.imshow(micr[slice,:,:,0], origin='lower', interpolation='none',
##    cmap='binary')
##plt.colorbar(ax)
##plt.title('Black delta microstructure')
##
##plt.subplot(222)
##ax = plt.imshow(micr[slice,:,:,1], origin='lower', interpolation='none',
##    cmap='binary')
##plt.colorbar(ax)
##plt.title('White delta microstructure')
##
##plt.subplot(223)
##ax = plt.imshow(micr[slice,:,:,2], origin='lower', interpolation='none',
##    cmap='binary')
##plt.colorbar(ax)
##plt.title('Validation microstructure')
#
##resp_fft_lin = np.reshape(resp_fft[:,:,:,-1],el**3).real
##freq = range(el**3)
##plt.plot(freq,resp_fft_lin,'b')