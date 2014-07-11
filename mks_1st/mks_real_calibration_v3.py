# -*- coding: utf-8 -*-
"""
3D, Isotropic, 1st Order MKS in real space

This script calibrates against reference datasets and plots the FE and MKS
response for a validation microstructure.

Noah Paulson
"""

import time
import numpy as np
import mks_func as rr


## el is the # of elements per side of the cube 
el = 21 
## the number of sample microstructures for calibration
ns = 2
## specify the number of local states you are using
H = 2
## specify the file to write messages to 
wrt_file = 'nofft_%s.txt' %time.strftime("%Y-%m-%d_h%Hm%M")


### THE MICROSTRUCTURE FUNCTION ###

## import delta microstructures for calibration and a random microstructure
## for validation
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
    msg = "%s is loaded" %filename
    rr.WP(msg,wrt_file)

### CALIBRATION OF INFLUENCE COEFFICIENTS ###

MM = np.zeros([H * el**3, H * el**3], dtype='int8')
PM = np.zeros(H * el**3)

for sn in range(ns):
    # this portion of the code generates the 'X' for the equation of multiple
    # linear regression X'XB=X'Y
    preMM = np.zeros([el**3, H * el**3], dtype='int8')    
    for h in xrange(H):    
        for t in xrange(el**3):
            [u,v,w] = np.unravel_index(t,[el,el,el])
            c = (h * el**3) + t
            preMM[:,c] = np.reshape(np.roll(np.roll(np.roll(
                                    m[:,:,:,sn,h],-u,0),-v,1),-w,2),el**3)
    
            if t % 9000 == 0:
                msg = 't=%s ,h=%s, sn=%s' %(t,h,sn)
                rr.WP(msg,wrt_file)
    
    start = time.time() 
    MM += np.dot(preMM.T,preMM)
    end = time.time()
    timeE = end - start       
    msg = 'MM, sn=%s, time=%s' %(sn, timeE)
    rr.WP(msg,wrt_file)
    
    start = time.time()     
    PM += np.dot(preMM.T,np.reshape(resp[:,:,:,sn],el**3))
    end = time.time()
    timeE = end - start       
    msg = 'PM, sn=%s, time=%s' %(sn, timeE)
    rr.WP(msg,wrt_file)

np.save('MM_final_v3',MM)
np.save('PM_final_v3',PM)

start = time.time()     
spec = np.linalg.solve(MM, PM).T
end = time.time()
timeE = end - start       
msg = 'lin solve, time=%s' %timeE
rr.WP(msg,wrt_file)

np.save('spec_v3',spec)

msg = 'calibration completed'
rr.WP(msg,wrt_file)