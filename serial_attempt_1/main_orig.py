# -*- coding: utf-8 -*-
"""
3D, Isotropic, 7th Order MKS

This code is designed to calibrate with 7th order terms for the nearest
neighbors, and to run on the PACE cluster

It should require a large amount of RAM (64Gb) and can only be run on a
single processor

It saves the mks_R.npy file which contains the response of the validation
microstructure

It also writes updates to the 'output.txt' file

Noah Paulson, 5/7/2014
"""

import time
import numpy as np
import mks_functions_1001 as rr

## el is the # of elements per side of the cube 
el = 21 
## select which order terms with nearest neighbors you would like to analyze
order = 1
## the number of sample microstructures for calibration and validation.
ns = 1001
## specify the file to write messages to 
wrt_file = 'output_%s.txt' %time.strftime("%Y%m%d%H%M%S") 

 
### THE MICROSTRUCTURE FUNCTION ###

## import delta and random microstructures
micr = rr.gen_micr('M_seventhorder.mat',0, ns, el)

# Black cells = 1, White cells = 0
# The black delta has a high stiffness cell surrounded by low stiffness cells,
# The white delta has a low stiffness cell surrounded by high stiffness cells

## microstructure functions
[m,H,pm,timeE] = rr.mf(micr,el,ns,order)
np.save('pm',pm)

msg = 'Microstructure function generation: %s seconds' %timeE
rr.WP(msg,wrt_file)

## Microstructure functions in frequency space
start = time.time()
M = np.fft.fftn(m, axes = [0,1,2])
del m
size = M.nbytes
end = time.time()
timeE = np.round((end - start),2)

msg = 'Size of microstructure function in frequency space: %s bytes' % size
rr.WP(msg,wrt_file)
msg = 'Convert microstructure function to frequency space: %s seconds' %timeE
rr.WP(msg,wrt_file)


### FINITE ELEMENT RESPONSES ###
[resp, msg] = rr.load_fe(0,ns,el) 
rr.WP(msg,wrt_file)
## responses in frequency space
start = time.time()
resp_fft = np.fft.fftn(resp, axes = [0,1,2]) 
end = time.time()
timeE = np.round((end - start),3)

msg = 'Convert FE results to frequency space: %s seconds' %timeE
rr.WP(msg,wrt_file)


### CALIBRATION OF INFLUENCE COEFFICIENTS ###
[specinfc,timeE] = rr.calibrator(M,resp_fft,wrt_file,H,el,ns)

msg = 'Calibration: %s seconds' %timeE
rr.WP(msg,wrt_file)


### VALIDATION WITH RANDOM ARRANGEMENT ###
mks_R = rr.validate(M,specinfc,H,el)
np.save('MKS_R_ord%s_%s_old' %(order,ns), mks_R)


### MEAN ABSOLUTE STRAIN ERROR (MASE) ###
[avgE, MASE] = rr.eval_meas(mks_R,resp,el)
msg = 'The average strain is %s' %avgE
rr.WP(msg,wrt_file)
msg = 'The mean absolute strain error (MASE) is %s%%' %(MASE*100)
rr.WP(msg,wrt_file)
