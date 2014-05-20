# -*- coding: utf-8 -*-
"""
3D, Isotropic MKS

This code works in a completely serial manner. Most variables are not computed
before they are used.

The code works for 1st, 2nd and 7th order nearest neighbor terms

Noah Paulson, 5/8/2014
"""

import time
import numpy as np
import mks_functions_serial as rr
#import scipy.io as sio

## el is the # of elements per side of the cube 
el = 21 
## select which order terms with nearest neighbors you would like to analyze
order = 1
## specify the number of local states you are using
H = 2
## specify the number of samples (including 1 validation microstructure)
ns = 1001
## specify the file to write messages to
wrt_file = 'output_%s.txt' %time.strftime("%Y%m%d%H%M%S")

### IMPORT SAMPLE MICROSTRUCTURES ###
micr = rr.gen_micr('M_seventhorder.mat',0, ns, el)

### FINITE ELEMENT METHOD (FEM) RESPONSES ###
## resp: FEM responses of all samples
## get resp from inp files (1) or from a saved .npy file (0)
[resp,msg] = rr.load_fe(0,ns,el) 
## resp_val: the FEM response for the validation microstructure
resp_val = resp[:,:,:,-1]
np.save('resp_val',resp_val)
rr.WP(msg,wrt_file)


### CALIBRATION OF INFLUENCE COEFFICIENTS ###
## For each frequency the calibration matrix (MM) and response matrix (PM) are
## calculated (X'X and X'Y respectively in the X'XB=X'Y, the formula for
## multiple linear regression). The matrix and response are reduced to thier
## independent rows and columns and the regression is solved for B (specinfc)

start = time.time()

## initialize the required arrays
specinfc = np.zeros((el**3,H),dtype = 'complex64')
MM = np.zeros((H,H,el**3),dtype = 'complex128')
PM = np.zeros((H,el**3),dtype = 'complex128')

## here we loop over the number of samples. 
for n in xrange(ns-1):
        
    m = rr.mf(micr[:,:,:,n],el,H,order)
    M = np.fft.fftn(m, axes = [0,1,2])
    resp_fft = np.fft.fftn(resp[:,:,:,n], axes = [0,1,2])
    
    ## The calibration matrix above must be calculated for every frequency,
    ## where the number of frequencies equals the number of spatial locations
    ## in the discrete microstructure (#elements ^ 3)
    for k in xrange(el**3):
        [u,v,w] = np.unravel_index(k,[el,el,el])        
        
        mSQ = np.array(M[u,v,w,:])     
        mSQc = np.conj(mSQ[None,:])
        mSQt = mSQ[:,None]
        
        MM[:,:,k] = MM[:,:,k] + np.dot(mSQt, mSQc)
        PM[:,k] = PM[:,k] + np.dot(resp_fft[u,v,w],mSQc)

    if n % 50 == 0:
        msg = "Calibration data extracted from sample %s" %n
        rr.WP(msg,wrt_file)


## Here we perform the actual linear regression mentioned earlier. It is 
## important to note that the independent rows/columns are found for the 
## calibration and reponses matrices for the first 2 frequencies. The 0th
## frequency uses the first set of independent rows/columns, while
## the rest use the second set.
for k in xrange(el**3):
    MM_k = MM[:,:,k]
    PM_k = PM[:,k]

    ## The independent rows/columns are found for frequencies 0 and 1
    if k < 2:
        p = rr.independent_columns(MM_k, .001)

    ## Dependent rows/columns for the k-th frequency calibration matrix and
    ## response are removed
    calred = MM_k[p,:][:,p]
    resred = PM_k[p].conj().T
    ## The equation for multiple linear regression is solved (solve X'XB=X'Y
    ## for B)    
    specinfc[k, p] = np.linalg.solve(calred, resred)

    if k % 3000 == 0:
        msg = "frequency completed: %s" %k
        rr.WP(msg,wrt_file)

np.save('specinfc_ord%s_%s' %(order,ns), specinfc)
msg = 'Size of MM: %s bytes' %MM.nbytes
rr.WP(msg,wrt_file)
msg = 'Size of PM: %s bytes' %PM.nbytes
rr.WP(msg,wrt_file)
del MM,PM

end = time.time()
timeE = np.round((end - start),3)
msg = "Calibration: %s seconds" %timeE
rr.WP(msg,wrt_file)

### VALIDATION WITH RANDOM ARRANGEMENT ###
M_val = np.fft.fftn(rr.mf(micr[:,:,:,-1],el,H,order), axes = [0,1,2])
mks_R = rr.validate(M_val,specinfc,H,el)
del specinfc
np.save('mks_R_ord%s_%s' %(order,ns), mks_R)


### MEAN ABSOLUTE STRAIN ERROR (MASE) ###
[avgE, MASE] = rr.eval_meas(mks_R,resp_val,el)
msg = "The average strain is %s" %avgE
rr.WP(msg,wrt_file)
msg = "The mean absolute strain error (MASE) is %s%%" %(MASE*100)
rr.WP(msg,wrt_file)
