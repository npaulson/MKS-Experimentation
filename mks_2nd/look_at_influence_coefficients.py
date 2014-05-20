# -*- coding: utf-8 -*-
"""
3D, Isotropic, 2st Order MKS

This script calibrates against reference datasets and plots the influence
coefficents to make sure they look good

Noah Paulson, 4/8/2014
"""

import os
import time
import numpy as np
import mks2nd_functions as rr
import matplotlib.pyplot as plt

el = 21
# ns refers to calibration datasets + VALIDATION DATASET
ns = 51
# H is the number of conformations of location and phase
H = 2

### THE MICROSTRUCTURE FUNCTION ###

## import delta and random microstructures
start = time.time()

micr = rr.pha_loc("cont5_micr_old.txt", el, ns)

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

M = np.zeros((el, el, el, ns, H),dtype = 'complex128')
for n in xrange(ns):
    for h in xrange(H):
        M[:,:,:,n,h] = np.fft.fftn(m[:,:,:,n,h])

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
    
    os.chdir("C:\mks_data\iso_2ph_5cont_dat")
    
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
    resp = np.load('FE_results.npy')
    print "FE results loaded"    

## responses in frequency space
start = time.time()

resp_fft = np.zeros((el,el,el,ns),dtype = 'complex128')
for n in xrange(ns):
    resp_fft[:,:,:,n] = np.fft.fftn(resp[:,:,:,n])
    
end = time.time()
timeE = np.round((end - start),3)
print "Convert FE results to frequency space: "
print "%s seconds" %np.round((end - start),3)

### CALIBRATION OF INFLUENCE COEFFICIENTS ###

start = time.time()

specinfc = np.zeros((el**3,H),dtype = 'complex128')
for k in xrange(el**3):
    
    [u,v,w] = np.unravel_index(k,[el,el,el])

    MM = np.zeros((H,H),dtype = 'complex128') # Microstucture matrix (M' M*) 
    PM = np.zeros((H,1),dtype = 'complex128') # Property matrix (P M*) 
    
    for n in xrange(ns-1):
        mSQc = np.conjugate(M[u,v,w,n,:]) # Conjugate of FFT of Microstructure      
        mSQt = np.mat(M[u,v,w,n,:]).T  # Transpose of FFT of Microstructure
        
        MM = MM + np.outer(mSQt,mSQc) # Calculate MM
        PM = PM + (resp_fft[u,v,w,n] * mSQc) # Calculate PM
        
    if k < 2:
        p = rr.independent_columns(MM, .001)
    
    calred = MM[p,:][:,p] # Linearly independent columns of MM
    resred = PM[p,0].conj().T  # Linearly independent columns of PM 

    ## for examining variables at desired frequency    
#    if k == 7:
#        print calred
#        print resred
#        print np.linalg.solve(calred,resred)
#        print specinfc[k, range(len(p))]

    if k % 500 == 0:
        print "frequency completed: %s" % k
    
    specinfc[k, p] = np.linalg.solve(calred, resred)   

#end = time.time()
#timeE = np.round((end - start),3)
#print "Calibration: %s seconds" %np.round((end - start),1)

### LOOK AT INFLUENCE COEFFICIENTS ###
R_inf_pre = np.fft.ifftn(np.reshape(specinfc[:,0],[21,21,21])).real;
R_inf = np.roll(np.roll(np.roll(R_inf_pre, 10, 0),10,1),10,2)

plt.close()

slc = 0

dmin = np.amin(R_inf[:,:,:])
dmax = np.amax(R_inf[:,:,:])

plt.subplot(111)
ax = plt.imshow(R_inf[slc,:,:], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('Influence Coefficients')