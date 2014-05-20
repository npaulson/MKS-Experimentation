# -*- coding: utf-8 -*-
"""
3D, Isotropic, 1st Order MKS

This script calibrates against reference datasets and plots the FE and MKS
response for a validation microstructure.

Noah Paulson, 3/27/2014
"""

import numpy as np
import res_red as rr
import matplotlib.pyplot as plt
from mks_func import *

# Generate the black and white delta microstructures. 
# Black cells = 1, White cells = 0
# The black delta has a high stiffness cell surrounded by low stiffness cells,
# The white delta has a low stiffness cell surrounded by high stiffness cells
el = 21
ns = 2
H = 2


### THE MICROSTRUCTURE FUNCTION ###

## import delta and random microstructures
micr = rr.pha_loc("msf.txt")

## microstructure functions
m = np.zeros((el,el,el,ns+1, H))
for h in range(H):
    m[:,:,:,:,h] = (micr[:,:,:,:] == h)
    
## Microstructure functions in frequency space
M = np.zeros((el, el, el, ns+1, H)) + 0j*np.zeros((el, el, el, ns+1, H))
for n in range(ns+1):
    for h in range(H):
        M[:,:,:,n,h] = np.fft.fftn(m[:,:,:,n,h])


### FINITE ELEMENT RESPONSES ###

## responses of the black and white delta microstructure and a random
## microstructure.
resp = np.zeros((el,el,el,ns+1))
for n in range(ns+1):
    filename = "21_%s_noah.dat" %(n+1) 
    resp[:,:,:,n] = rr.res_red(filename)
    print "%s is loaded" %filename 

## responses in frequency space
resp_fft = np.zeros((el,el,el,ns)) + 0j*np.zeros((el,el,el,ns))
for n in range(ns):
    resp_fft[:,:,:,n] = np.fft.fftn(resp[:,:,:,n])
    

### CALIBRATION OF INFLUENCE COEFFICIENTS ###

#MM = np.zeros((H,H,el**3)) + 0j*np.zeros((H,H,el**3))
#PM = np.zeros((H,el**3)) + 0j*np.zeros((H,el**3))
specinfc = np.zeros((el**3,H)) + 0j*np.zeros((el**3,H))
for k in range(el**3):
    
    [u,v,w] = np.unravel_index(k,[el,el,el])

    MM = np.zeros((H,H)) + 0j*np.zeros((H,H))
    PM = np.zeros((H,1)) + 0j*np.zeros((H,1))
    
    for n in range(ns):
        mSQc = np.conjugate(M[u,v,w,n,:])        
        mSQt = np.mat(M[u,v,w,n,:]).T  
        
#        MM[:, :, k] = MM[:, :, k] + np.outer(mSQt,mSQc)
        MM = MM + np.outer(mSQt,mSQc)
        
#        PM[:, k] = PM[:, k] + (resp_fft[u,v,w,n] * mSQc)
        PM = PM + (resp_fft[u,v,w,n] * mSQc)
        
    if k < 2:
#        p = independent_columns(MM[:, :, k], .001)
        p = independent_columns(MM, .001)
    
#    calred = MM[p,:, k][:,p]
#    resred = PM[p, k].conj().T
    calred = MM[p,:][:,p]
    resred = PM[p,0].conj().T

    ## for examining variables at desired frequency    
    if k == 0:
        print calred
        print resred
        print np.linalg.solve(calred,resred)
    
    specinfc[k, p] = np.linalg.solve(calred, resred)

    if k % 500 == 0:
        print "frequency completed: %s" % k

print "Calibration Completed"      


### VALIDATION WITH RANDOM ARRANGEMENT ###

## vectorize the frequency-space microstructure function for the validation
## dataset
lin_M = np.zeros((el**3,H)) + 0j*np.zeros((el**3,H))
for h in range(H):
    lin_M[:,h] = np.reshape(M[:,:,:,-1,h],el**3)

## find the frequency-space response of the validation microstructure
## and convert to the real space
lin_sum = np.sum(np.conjugate(specinfc) * lin_M, 1)
mks_F = np.reshape(lin_sum,[21,21,21])
mks_R = np.fft.ifftn(mks_F).real


### MEAN ABSOLUTE STRAIN ERROR (MASE) ###

MASE = 0
avgE = np.average(resp[:,:,:,-1])
print "The average strain is %s" %avgE

for k in range(el**3):
    
    [u,v,w] = np.unravel_index(k,[el,el,el])
    MASE = MASE + ((np.abs(resp[u,v,w,-1] - mks_R[u,v,w]))/(avgE * el**3))

print "The mean absolute strain error (MASE) is %s%%" %(MASE*100)


## VISUALIZATION OF MKS VS. FEM ###

plt.close()
#fig = plt.figure()

## pick a slice perpendicular to the x-direction
slice = 10

## find the min and max of both datasets (needed to scale both images the same) 
dmin = np.amin([resp[slice,:,:,-1],mks_R[slice,:,:]])
dmax = np.amax([resp[slice,:,:,-1],mks_R[slice,:,:]])

plt.subplot(131)
ax = plt.imshow(mks_R[slice,:,:], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('MKS approximation, E11')

plt.subplot(132)
ax = plt.imshow(resp[slice,:,:,-1], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('FE response, E11')   

plt.subplot(133)

feb = remzer(np.reshape(resp[:,:,:,-1]*m[:,:,:,-1,1],el**3))
few = remzer(np.reshape(resp[:,:,:,-1]*m[:,:,:,-1,0],el**3))
mksb = remzer(np.reshape(mks_R[:,:,:]*m[:,:,:,-1,1],el**3))
mksw = remzer(np.reshape(mks_R[:,:,:]*m[:,:,:,-1,0],el**3))
bn = 40

n, bins, patches = plt.hist(feb, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
bincenters = 0.5*(bins[1:]+bins[:-1])
febp, = plt.plot(bincenters,n,'k', linestyle = ':')

n, bins, patches = plt.hist(few, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
fewp, = plt.plot(bincenters,n,'k')

n, bins, patches = plt.hist(mksb, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
mksbp, = plt.plot(bincenters,n,'r', linestyle = ':')

n, bins, patches = plt.hist(mksw, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
mkswp, = plt.plot(bincenters,n,'r')

plt.grid(True)

plt.legend([febp,fewp,mksbp,mkswp], ["FE - stiff phase", 
           "FE - compliant phase", "MKS - stiff phase",
           "MKS - compliant phase"])

plt.xlabel("Strain")
plt.ylabel("Frequency")
plt.title("Frequency comparison of FE and MKS")

#plt.subplot(221)
#ax = plt.imshow(micr[slice,:,:,0], origin='lower', interpolation='none',
#    cmap='binary')
#plt.colorbar(ax)
#plt.title('Black delta microstructure')
#
#plt.subplot(222)
#ax = plt.imshow(micr[slice,:,:,1], origin='lower', interpolation='none',
#    cmap='binary')
#plt.colorbar(ax)
#plt.title('White delta microstructure')
#
#plt.subplot(223)
#ax = plt.imshow(micr[slice,:,:,2], origin='lower', interpolation='none',
#    cmap='binary')
#plt.colorbar(ax)
#plt.title('Validation microstructure')

#resp_fft_lin = np.reshape(resp_fft[:,:,:,-1],el**3).real
#freq = range(el**3)
#plt.plot(freq,resp_fft_lin,'b')