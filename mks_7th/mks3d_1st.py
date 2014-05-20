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

el = 21

# H is the number of conformations of location and phase
H = 2

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

m = np.zeros([el,el,el,ns,2])
m[:,:,:,:,0] = (micr == 0)
m[:,:,:,:,1] = (micr == 1)
m = m.astype(int)

end = time.time()
timeE = np.round((end - start),2)
print "Microstructure function generation: %s seconds" %timeE
    
## Microstructure functions in frequency space
start = time.time()

M = np.zeros((el, el, el, ns, H), dtype = 'complex64')
for n in xrange(ns):
    for h in xrange(H):
        M[:,:,:,n,h] = np.fft.fftn(m[:,:,:,n,h])
#M = np.fft.fftn(m, axes = [0,1,2])

end = time.time()
timeE = np.round((end - start),2)
print "Convert microstructure function to frequency space: %s seconds" %timeE


### FINITE ELEMENT RESPONSES ###

## responses of the black and white delta microstructure and a random
## microstructure.

# if read_dat == 1 the program will reload all of the .dat files and save them
# to FE_results.npy
read_dat = 0
if read_dat == 1:
    start = time.time()    
    
    os.chdir("C:\mks_data\order7_dat_151")
    
    resp = np.zeros((el,el,el,ns))
    for n in xrange(ns):
        filename = "sq21_%scont5.dat" %(n+1) 
        resp[:,:,:,n] = rr.res_red(filename)
        print "%s is loaded" %filename 
    
    os.chdir("C:/Users/nhpnp3/Documents/GitHub/MKS_repository/MKS_2nd")
    np.save('FE_results',resp)    
    
    end = time.time()
    timeE = np.round((end - start),1)
    print "Import FE results: %s seconds" %np.round((end - start),1)

# if read_dat == 0 the script will simply reload the results from a previously
# saved FE_results.npy
else:
    resp = np.load('FE_results_151.npy')
    print "FE results loaded"    

## responses in frequency space
start = time.time()

resp_fft = np.zeros((el,el,el,ns), dtype = 'complex64')
for n in xrange(ns):
    resp_fft[:,:,:,n] = np.fft.fftn(resp[:,:,:,n])
    
end = time.time()
timeE = np.round((end - start),3)
print "Convert FE results to frequency space: "
print "%s seconds" %np.round((end - start),3)

### CALIBRATION OF INFLUENCE COEFFICIENTS ###

start = time.time()

specinfc = np.zeros((el**3,H), dtype = 'complex64')
for k in xrange(el**3):
    
    [u,v,w] = np.unravel_index(k,[el,el,el])

    MM = np.zeros((H,H), dtype = 'complex128')
    PM = np.zeros((H,1), dtype = 'complex128')
    
    for n in xrange(ns-1):
        mSQc = np.conjugate(M[u,v,w,n,:])        
        mSQt = np.mat(M[u,v,w,n,:]).T  
        
        MM = MM + np.outer(mSQt,mSQc)
        PM = PM + (resp_fft[u,v,w,n] * mSQc)
        
    if k < 2:
        p = rr.independent_columns(MM, .001)
    
    calred = MM[p,:][:,p]
    resred = PM[p,0].conj().T

    ## for examining variables at desired frequency    
#    if k == 7:
#        print calred
#        print resred
#        print np.linalg.solve(calred,resred)
#        print specinfc[k, range(len(p))]

    if k % 500 == 0:
        print "frequency completed: %s" % k
    
    specinfc[k, p] = np.linalg.solve(calred, resred)   

end = time.time()
timeE = np.round((end - start),3)
print "Calibration: %s seconds" %np.round((end - start),1)

### VALIDATION WITH RANDOM ARRANGEMENT ###

## vectorize the frequency-space microstructure function for the validation
## dataset
lin_M = np.zeros((el**3,H)) + 0j*np.zeros((el**3,H))
for h in xrange(H):
    lin_M[:,h] = np.reshape(M[:,:,:,-1,h],el**3)


## find the frequency-space response of the validation microstructure
## and convert to the real space
lin_sum = np.sum(np.conjugate(specinfc) * lin_M, 1)
mks_F = np.reshape(lin_sum,[21,21,21])
mks_R = np.fft.ifftn(mks_F).real

np.save('MKS_1stOrd_resp',mks_R) 

### MEAN ABSOLUTE STRAIN ERROR (MASE) ###

MASE = 0
avgE = np.average(resp[:,:,:,-1])
print "The average strain is %s" %avgE

for k in xrange(el**3):
    
    [u,v,w] = np.unravel_index(k,[el,el,el])
    MASE = MASE + ((np.abs(resp[u,v,w,-1] - mks_R[u,v,w]))/(avgE * el**3))

print "The mean absolute strain error (MASE) is %s%%" %(MASE*100)


## VISUALIZATION OF MKS VS. FEM ###

plt.close()
#fig = plt.figure()

## pick a slice perpendicular to the x-direction
slc = 10

## find the min and max of both datasets (needed to scale both images the same) 
dmin = np.amin([resp[slc,:,:,-1],mks_R[slc,:,:]])
dmax = np.amax([resp[slc,:,:,-1],mks_R[slc,:,:]])

plt.subplot(221)
ax = plt.imshow(mks_R[slc,:,:], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('MKS approximation, E11')

plt.subplot(222)
ax = plt.imshow(resp[slc,:,:,-1], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('FE response, E11')   

plt.subplot(212)

feb = rr.remzer(np.reshape(resp[:,:,:,-1]*m[:,:,:,-1,1],el**3))
few = rr.remzer(np.reshape(resp[:,:,:,-1]*m[:,:,:,-1,0],el**3))
mksb = rr.remzer(np.reshape(mks_R[:,:,:]*m[:,:,:,-1,1],el**3))
mksw = rr.remzer(np.reshape(mks_R[:,:,:]*m[:,:,:,-1,0],el**3))

bn = 40

n, bins, patches = plt.hist(feb, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
bincenters = 0.5*(bins[1:]+bins[:-1])
febp, = plt.plot(bincenters,n,'k', linestyle = '--', lw = 1.5)

n, bins, patches = plt.hist(few, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
fewp, = plt.plot(bincenters,n,'k')

n, bins, patches = plt.hist(mksb, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
mksbp, = plt.plot(bincenters,n,'r', linestyle = '--', lw = 1.5)

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
#
#del MM, PM, M, lin_M, specinfc, lin_sum, mks_F, m, micr, pm
#del febp, fewp, mksbp, mkswp, ax
#
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
#
#resp_fft_lin = np.reshape(resp_fft[:,:,:,-1],el**3).real
#freq = range(el**3)
#plt.plot(freq,resp_fft_lin,'b')