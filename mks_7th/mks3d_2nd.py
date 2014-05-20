# -*- coding: utf-8 -*-
"""
3D, Isotropic, 2st Order MKS

This script calibrates against reference datasets and plots the FE and MKS
response for a validation microstructure.

Noah Paulson, 4/8/2014
"""

import os
import time
import numpy as np
import mks7th_functions as rr
import matplotlib.pyplot as plt
#import scipy.io as sio

# el is the # of elements per side of the cube 
el = 21


### THE MICROSTRUCTURE FUNCTION ###

## import delta and random microstructures
start = time.time()

[micr, ns] = rr.pha_loc("cont5_micr151.txt", el)

end = time.time()
timeE = np.round((end - start),2)
print "Import microstructures: %s seconds" %timeE

# Black cells = 1, White cells = 0
# The black delta has a high stiffness cell surrounded by low stiffness cells,
# The white delta has a low stiffness cell surrounded by high stiffness cells

## microstructure functions
start = time.time()

pm = np.zeros([el,el,el,ns,2])
pm[:,:,:,:,0] = (micr == 0)
pm[:,:,:,:,1] = (micr == 1)
pm = pm.astype(int)

hs = np.array([[1,1],[0,0],[1,0],[0,1]])
vec = np.array([[1,0],[1,1],[1,2]])

k = 0
# H is the # of conformations of location and phase
H = len(hs[:,0]) * len(vec[:,0])
m = np.zeros([el,el,el,ns,H])
for hh in xrange(len(hs[:,0])):
    for t in xrange(len(vec[:,0])):
        a1 = pm[:,:,:,:,hs[hh,0]]
        a2 = np.roll(pm[:,:,:,:,hs[hh,1]],vec[t,0],vec[t,1])
        m[:,:,:,:,k] = a1 * a2
        k = k + 1

m = m.astype(int)

end = time.time()
timeE = np.round((end - start),2)
print "Microstructure function generation: %s seconds" %timeE
    
## Microstructure functions in frequency space
start = time.time()

M = np.zeros((el, el, el, ns, H),dtype = 'complex64')
for n in xrange(ns):
    for h in xrange(H):
        M[:,:,:,n,h] = np.fft.fftn(m[:,:,:,n,h])

end = time.time()
timeE = np.round((end - start),2)
print "Convert microstructure function to frequency space: %s seconds" %timeE


### FINITE ELEMENT RESPONSES ###

## responses of the black and white delta microstructures and random
## microstructures.

# if read_dat == 1 the program will reload all of the .dat files and save them
# to FE_results.npy
read_dat = 0
if read_dat == 1:
    start = time.time()    
    
    os.chdir("C:\mks_data\order7_dat_151")
    
    resp = np.zeros((el,el,el,ns))
    for n in xrange(ns):
        filename = "sq21_5cont_%s.dat" %(n+1) 
        resp[:,:,:,n] = rr.res_red(filename)
        print "%s is loaded" %filename 
    
    os.chdir("C:/Users/nhpnp3/Documents/GitHub/MKS_repository/MKS_7th")
    np.save('FE_results_151',resp)    
    
    end = time.time()
    timeE = np.round((end - start),1)
    print "Import FE results: %s seconds" %timeE

# if read_dat == 0 the script will simply reload the results from a previously
# saved FE_results.npy
else:
    resp = np.load('FE_results_151.npy')
    print "FE results loaded"    

## responses in frequency space
start = time.time()

resp_fft = np.zeros((el,el,el,ns),dtype = 'complex64')
for n in xrange(ns):
    resp_fft[:,:,:,n] = np.fft.fftn(resp[:,:,:,n])
    
end = time.time()
timeE = np.round((end - start),3)
print "Convert FE results to frequency space: "
print "%s seconds" %np.round((end - start),3)


### CALIBRATION OF INFLUENCE COEFFICIENTS ###

start = time.time()
timeEi = 0
specinfc = np.zeros((el**3,H),dtype = 'complex64')
for k in xrange(el**3):
    
    [u,v,w] = np.unravel_index(k,[el,el,el])

    MM = np.zeros((H,H),dtype = 'complex128')
    PM = np.zeros((H,1),dtype = 'complex128')
    
    for n in xrange(ns-1):

        mSQ = np.array(M[u,v,w,n,:])     
        mSQc = np.conj(mSQ[None,:])
        mSQt = mSQ[:,None]
        
        MM = MM + np.dot(mSQt, mSQc)
        PM[:,0] = PM[:,0] + np.dot(resp_fft[u,v,w,n],mSQc)
 
    if k < 2:
        p = rr.independent_columns(MM, .001)
#    else:
#        p = [0,1,2,3]
#    if np.array_equal(p,[0,1,2,3]) == False:
#        print "at frequency %s, p = %s" %(k,p)

    calred = MM[p,:][:,p]
    resred = PM[p,0].conj().T
    specinfc[k, p] = np.linalg.solve(calred, resred)

    if k % 500 == 0:
        print "frequency completed: %s" %k

end = time.time()
timeE = np.round((end - start),3)
print "Calibration: %s seconds" %timeE


### VALIDATION WITH RANDOM ARRANGEMENT ###

## vectorize the frequency-space microstructure function for the validation
## dataset
lin_M = np.zeros((el**3,H),dtype = 'complex64')
for h in xrange(H):
    lin_M[:,h] = np.reshape(M[:,:,:,-1,h],el**3)


## find the frequency-space response of the validation microstructure
## and convert to the real space
lin_sum = np.sum(np.conjugate(specinfc) * lin_M, 1)
mks_F = np.reshape(lin_sum,[21,21,21])
mks_R = np.fft.ifftn(mks_F).real

np.save('MKS_2stOrd_resp',mks_R) 

### MEAN ABSOLUTE STRAIN ERROR (MASE) ###

avgE = np.average(mks_R[:,:,:])
print "The average strain is %s" %avgE

MASE = 0
for k in xrange(el**3):
    [u,v,w] = np.unravel_index(k,[el,el,el])
    MASE = MASE + ((np.abs(resp[u,v,w,-1] - mks_R[u,v,w]))/(avgE * el**3))

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