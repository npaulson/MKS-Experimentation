# -*- coding: utf-8 -*-
"""
3D, Isotropic, 1st Order MKS


Noah Paulson, 7/25/2014
"""

import time
import numpy as np
import functions_small as rr
from functools import partial


## el is the # of elements per side of the cube 
el = 21 
## the number of sample microstructures for calibration and validation.
ns = 3
## specify the number of local states you are using
H = 2
## specify the file to write messages to 
wrt_file = 'output_serial_%s.txt' %time.strftime("%Y-%m-%d_%H-%M") 


### THE MICROSTRUCTURE FUNCTION ###

## import delta and random microstructures
micr = rr.gen_micr('M_seventhorder.mat',0, ns, el)

## microstructure functions
m = rr.mf(micr,el,H)

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
[resp_all, msg] = rr.load_fe(0,ns,el)
resp = resp_all[:,:,:,0,:]

resp_val = resp[:,:,:,-1]
rr.WP(msg,wrt_file)

## responses in frequency space
start = time.time()
resp_fft = np.fft.fftn(resp, axes = [0,1,2]) 
end = time.time()
timeE = np.round((end - start),3)

msg = 'Convert FE results to frequency space: %s seconds' %timeE
rr.WP(msg,wrt_file)


### CALIBRATION OF INFLUENCE COEFFICIENTS ###

start = time.time()
specinfc = np.zeros((el**3,H),dtype = 'complex64')

specinfc[0,:] = rr.calib(0,M,resp_fft,0,H,el,ns)
[specinfc[1,:],p] = rr.calib(1,M,resp_fft,0,H,el,ns)

## calib_red is simply calib with some default arguments
calib_red = partial(rr.calib,M=M,resp_fft=resp_fft,p=p,H=H,el=el,ns=ns)

specinfc[2:(el**3),:] = np.asarray(map(calib_red,range(2,el**3)))


end = time.time()
timeE = np.round((end - start),3)
msg = 'Calibration: %s seconds' %timeE
rr.WP(msg,wrt_file)


### VALIDATION WITH RANDOM ARRANGEMENT ###
M_val = np.fft.fftn(rr.mf_sn(micr[:,:,:,-1],el, H), axes = [0,1,2])
mks_R = rr.validate(M_val,specinfc,H,el)
np.save('mks_R_' %(order,ns), mks_R)


### MEAN ABSOLUTE STRAIN ERROR (MASE) ###
[avgE, MASE] = rr.eval_meas(mks_R,resp_val,el)
msg = 'The average strain is %s' %avgE
rr.WP(msg,wrt_file)
msg = 'The mean absolute strain error (MASE) is %s%%' %(MASE*100)
rr.WP(msg,wrt_file)
