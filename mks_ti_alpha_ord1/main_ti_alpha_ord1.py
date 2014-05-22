# -*- coding: utf-8 -*-
"""
3D, 1st Order, Polycrystalline MKS

Noah Paulson, 5/7/2014
"""

import time
import numpy as np
import functions_ti_alpha_ord1 as rr
from functools import partial
import os

## el is the # of elements per side of the cube 
el = 21 
## select which order terms with nearest neighbors you would like to analyze
order = 1
## the number of sample microstructures for calibration and validation.
ns = 200
## specify the number of local states you are using
H = 15
## specify the file to write messages to 
wrt_file = 'output_%s.txt' %time.strftime("%Y-%m-%d_h%Hm%M") 

cwd = os.getcwd()

### THE MICROSTRUCTURE FUNCTION ###

## import microstructures
[micr, timeE] = rr.gen_micr('extremeorientc_hexa.mat','orientation1.mat',
                    0,ns,el,H)
msg = 'Import microstructures: %s seconds' %timeE
rr.WP(msg,wrt_file)


### microstructure functions
#m = rr.mf(micr,el,order,H)
#

## Microstructure functions in frequency space
start = time.time()
M = np.fft.fftn(micr, axes = [0,1,2])
del micr
size = M.nbytes
end = time.time()
timeE = np.round((end - start),2)

msg = 'Size of microstructure function in frequency space: %s bytes' % size
rr.WP(msg,wrt_file)
msg = 'Convert microstructure function to frequency space: %s seconds' %timeE
rr.WP(msg,wrt_file)


### FINITE ELEMENT RESPONSES ###
[resp_all, msg] = rr.load_fe('orientation1.mat',0,ns,el)
resp = resp_all[:,:,:,0,:]
#resp_val = resp[:,:,:,-1]
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

#specinfc[2:(el**3),:] = np.asarray(map(calib_red,range(2,el**3)))
result = map(calib_red,range(2,el**3))
specinfc[2:(el**3),:] = np.asarray(result)
del result    

np.save('specinfc_ti_alpha_ord1_samp%s' %ns,specinfc)

end = time.time()
timeE = np.round((end - start),3)
msg = 'Calibration: %s seconds' %timeE
rr.WP(msg,wrt_file)


#### VALIDATION WITH RANDOM ARRANGEMENT ###
#M_val = np.fft.fftn(rr.mf_sn(micr[:,:,:,-1],el,order, H), axes = [0,1,2])
#mks_R = rr.validate(M_val,specinfc,H,el)
#np.save('MKS_R_ord%s_%s_old' %(order,ns), mks_R)
#
#
#### MEAN ABSOLUTE STRAIN ERROR (MASE) ###
#[avgE, MASE] = rr.eval_meas(mks_R,resp_val,el)
#msg = 'The average strain is %s' %avgE
#rr.WP(msg,wrt_file)
#msg = 'The mean absolute strain error (MASE) is %s%%' %(MASE*100)
#rr.WP(msg,wrt_file)
