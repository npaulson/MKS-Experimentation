# -*- coding: utf-8 -*-
"""
3D, Isotropic, 1st Order MKS in real space

This script calibrates against reference datasets and plots the FE and MKS
response for a validation microstructure.

Noah Paulson
"""

import numpy as np
import mks_func as rr
import matplotlib.pyplot as plt


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


### FINITE ELEMENT RESPONSES ###

## responses of the black and white delta microstructure and a random
## microstructure.
resp = np.zeros((el,el,el,ns+1))
for n in range(ns+1):
    filename = "21_%s_noah.dat" %(n+1) 
    resp[:,:,:,n] = rr.res_red(filename)
    print "%s is loaded" %filename
    

### CALIBRATION OF INFLUENCE COEFFICIENTS ###

spec = np.zeros([el**3,H])
#for t in xrange(el**3):
for t in xrange(4620,4640):
    
    [u,v,w] = np.unravel_index(t,[el,el,el])
    mroll = np.roll(np.roll(np.roll(m,-u,0),-v,1),-w,2)

    MM = np.zeros([H,H])
    PM = np.zeros(H)
    
    for n in range(ns):
        for s in range(el**3):
            [h,k,l] = np.unravel_index(s,[el,el,el])
            
            mSQ = np.array(mroll[h,k,l,n,:])     
#            mSQt = mSQ[:,None]
            
            MM += np.outer(mSQ, mSQ)
            PM += resp[h,k,l,n] * mSQ
        
#            if t == 4622 and n == 1 and np.allclose(mSQ,np.array([1.,0.])) == True:
#                print s                
#                print mSQ
#                print resp[h,k,l,n]

#    p = rr.independent_columns(MM, .001)
#    calred = MM[p,:][:,p]
#    resred = PM[p,0].T   
#    spec[t, p] = np.linalg.solve(calred, resred)
#    p = np.array([0, 1])
    spec[t, :] = np.linalg.solve(MM, PM).T

    if t % 1 == 0:
        print spec[t, :]        
        print "Vector index completed: %s" % t

print "Calibration Completed"      


### VALIDATION WITH RANDOM ARRANGEMENT ###

spec = spec/20
mks_R = np.zeros([el,el,el])

for t in xrange(el**3):
    [u,v,w] = np.unravel_index(t,[el,el,el])    

    for h in xrange(H):

        mroll = np.roll(np.roll(np.roll(m[:,:,:,-1,h],-u,0),-v,1),-w,2)        
        
        mks_R += spec[t,h] * mroll


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

feb = rr.remzer(np.reshape(resp[:,:,:,-1]*m[:,:,:,-1,1],el**3))
few = rr.remzer(np.reshape(resp[:,:,:,-1]*m[:,:,:,-1,0],el**3))
mksb = rr.remzer(np.reshape(mks_R*m[:,:,:,-1,1],el**3))
mksw = rr.remzer(np.reshape(mks_R*m[:,:,:,-1,0],el**3))
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