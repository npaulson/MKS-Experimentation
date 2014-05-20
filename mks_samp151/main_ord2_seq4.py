# -*- coding: utf-8 -*-
"""
3D, Isotropic, 2st Order MKS

This code works in a completely serial manner. Most variables are not computed
before they are used.

Noah Paulson, 4/28/2014
"""

import time
import numpy as np
import mks_functions_seq4 as rr
#import matplotlib.pyplot as plt
#import scipy.io as sio

## el is the # of elements per side of the cube 
el = 21 
## select which order terms with nearest neighbors you would like to analyze
order = 7
## specify the number of local states you are using
H = 128

### IMPORT SAMPLE MICROSTRUCTURES ###
[micr, ns, timeE] = rr.pha_loc("cont5_micr151.txt",0,el)
print "Import microstructures: %s seconds" %timeE

### FINITE ELEMENT METHOD (FEM) RESPONSES ###
## resp: FEM responses of all samples
## get resp from inp files (1) or from a saved .npy file (0)
resp = rr.load_fe(0,ns,el) 
## resp_fin: the FEM response for the validation microstructure
resp_fin = resp[:,:,:,-1]
np.save('resp_fin',resp_fin)

### CALIBRATION OF INFLUENCE COEFFICIENTS ###
start = time.time()

specinfc = np.zeros((el**3,H),dtype = 'complex64')
MM = np.zeros((H,H,el**3),dtype = 'complex128')
PM = np.zeros((H,el**3),dtype = 'complex128')
 
for n in xrange(ns-1):
        
    m = rr.mf(micr[:,:,:,n],el,H,order)
    M = np.fft.fftn(m, axes = [0,1,2])
    resp_fft = np.fft.fftn(resp[:,:,:,n], axes = [0,1,2])
    
    for k in xrange(el**3):
        [u,v,w] = np.unravel_index(k,[el,el,el])        
        
        mSQ = np.array(M[u,v,w,:])     
        mSQc = np.conj(mSQ[None,:])
        mSQt = mSQ[:,None]
        
        MM[:,:,k] = MM[:,:,k] + np.dot(mSQt, mSQc)
        PM[:,k] = PM[:,k] + np.dot(resp_fft[u,v,w],mSQc)

    if n % 25 == 0:
        print "Calibration data extracted from sample: %s" %n

for k in xrange(el**3):
    MM_k = MM[:,:,k]
    PM_k = PM[:,k]

    if k < 2:
        p = rr.independent_columns(MM_k, .001)

    calred = MM_k[p,:][:,p]
    resred = PM_k[p].conj().T
    specinfc[k, p] = np.linalg.solve(calred, resred)

    if k % 3000 == 0:
        print "frequency completed: %s" %k

np.save('specinfc', specinfc)
print 'Size of MM: %s bytes' %MM.nbytes
print 'Size of PM: %s bytes' %PM.nbytes
del MM,PM

end = time.time()
timeE = np.round((end - start),3)
print "Calibration: %s seconds" %timeE


### VALIDATION WITH RANDOM ARRANGEMENT ###
M_val = np.fft.fftn(rr.mf(micr[:,:,:,-1],el,H,order), axes = [0,1,2])
mks_R = rr.validate(M_val,specinfc,H,el)
np.save('mks_R_ord%s_%s' %[order,ns],mks_R)
del specinfc

### MEAN ABSOLUTE STRAIN ERROR (MASE) ###
[avgE, MASE] = rr.eval_meas(mks_R,resp_fin,el)
print "The average strain is %s" %avgE
print "The mean absolute strain error (MASE) is %s%%" %(MASE*100)


#### VISUALIZATION OF MKS VS. FEM ###
#
#plt.close()
#
### pick a slice perpendicular to the x-direction
#slc = 10
#
### load the 1st order terms results
#mks_R1st = np.load('MKS_1stOrd_resp.npy')
#
### find the min and max of both datasets for the slice of interest
##(needed to scale both images the same) 
#dmin = np.amin([resp_fin[slc,:,:],mks_R[slc,:,:],mks_R1st[slc,:,:]])
#dmax = np.amax([resp_fin[slc,:,:],mks_R[slc,:,:],mks_R1st[slc,:,:]])
#
### Plot slices of the response
#plt.subplot(231)
#ax = plt.imshow(mks_R1st[slc,:,:], origin='lower', interpolation='none',
#    cmap='jet', vmin=dmin, vmax=dmax)
#plt.colorbar(ax)
#plt.title('MKS 1st order terms, E11')
#
#plt.subplot(232)
#ax = plt.imshow(mks_R[slc,:,:], origin='lower', interpolation='none',
#    cmap='jet', vmin=dmin, vmax=dmax)
#plt.colorbar(ax)
#plt.title('MKS 2nd order terms, E11')
#
#plt.subplot(233)
#ax = plt.imshow(resp_fin[slc,:,:], origin='lower', interpolation='none',
#    cmap='jet', vmin=dmin, vmax=dmax)
#plt.colorbar(ax)
#plt.title('FE response, E11')   
#
## Plot a histogram representing the frequency of strain levels with separate
## channels for each phase of each type of response.
#plt.subplot(212)
#
### find the min and max of both datasets (in full)
#dmin = np.amin([resp_fin,mks_R[:,:,:],mks_R1st[:,:,:]])
#dmax = np.amax([resp_fin,mks_R[:,:,:],mks_R1st[:,:,:]])
#
#pm = np.zeros([el,el,el,ns,2])
#pm[:,:,:,:,0] = (micr == 0)
#pm[:,:,:,:,1] = (micr == 1)
#
## separating each response by phase
#feb = rr.remzer(np.reshape(resp_fin*pm[:,:,:,-1,1],el**3))
#few = rr.remzer(np.reshape(resp_fin*pm[:,:,:,-1,0],el**3))
#mks1b = rr.remzer(np.reshape(mks_R1st[:,:,:]*pm[:,:,:,-1,1],el**3))
#mks1w = rr.remzer(np.reshape(mks_R1st[:,:,:]*pm[:,:,:,-1,0],el**3))
#mks2b = rr.remzer(np.reshape(mks_R[:,:,:]*pm[:,:,:,-1,1],el**3))
#mks2w = rr.remzer(np.reshape(mks_R[:,:,:]*pm[:,:,:,-1,0],el**3))
#
#del pm
#
## select the desired number of bins in the histogram
#bn = 40
#
## FEM histogram
#n, bins, patches = plt.hist(feb, bins = bn, histtype = 'step', hold = True,
#                            range = (dmin, dmax), color = 'white')
#bincenters = 0.5*(bins[1:]+bins[:-1])
#febp, = plt.plot(bincenters,n,'k', linestyle = '--', lw = 1.5)
#
#n, bins, patches = plt.hist(few, bins = bn, histtype = 'step', hold = True,
#                            range = (dmin, dmax), color = 'white')
#fewp, = plt.plot(bincenters,n,'k')
#
## 1st order terms MKS histogram
#n, bins, patches = plt.hist(mks1b, bins = bn, histtype = 'step', hold = True,
#                            range = (dmin, dmax), color = 'white')
#mks1bp, = plt.plot(bincenters,n,'b', linestyle = '--', lw = 1.5)
#
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
#
#plt.grid(True)
#
#plt.legend([febp,fewp,mks1bp,mks1wp,mks2bp,mks2wp], ["FE - stiff phase", 
#           "FE - compliant phase", "MKS, 1st order terms - stiff phase",
#           "MKS, 1st order terms - compliant phase",
#           "MKS, 2nd order terms - stiff phase",
#           "MKS, 2nd order terms - compliant phase"])
#
#plt.xlabel("Strain")
#plt.ylabel("Frequency")
#plt.title("Frequency comparison of 1st and 2nd order MKS with FE results")
#
##del MM, PM, M, lin_M, specinfc, lin_sum, mks_F, m, micr, pm
##del febp, fewp, mksbp, mkswp, ax
#
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