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
import mks_functions_serial_chunk as rr
from functools import partial
import os

## el is the # of elements per side of the cube 
el = 21 
## select which order terms with nearest neighbors you would like to analyze
order = 1
## the number of sample microstructures for calibration and validation.
ns = 151
## specify the number of local states you are using
H = 2
## specify the file to write messages to 
wrt_file = 'output_%s.txt' %time.strftime("%Y%m%d%H%M%S") 


### THE MICROSTRUCTURE FUNCTION ###

start = time.time()

micr = rr.gen_micr('M_seventhorder.mat',0, ns, el)

main_dir = 'M_main_%s' % time.strftime("%Y%m%d%H%M") 
os.mkdir(main_dir)
os.chdir(main_dir)

for k in range(el**3):
    sub_dir = 'M_freq%s' %k    
    os.mkdir(sub_dir)

for n in range(ns):
    M_samp = np.fft.fftn(rr.mf_sn(micr[:,:,:,n],el,order,H), axes = [0,1,2])

    for k in range(el**3):    
        sub_dir = 'M_freq%s' %k        
        os.chdir(sub_dir)

        [u,v,w] = np.unravel_index(k,[el,el,el])
        
        file_M = 'M_samp%s_freq%s' %(n, k)        
        np.save(file_M, M_samp[u,v,w,:])
        
        os.chdir('..')

os.chdir('..')

end = time.time()
timeE = np.round((end - start),2)
print 'Microstructure function file generation: %s' %timeE

### microstructure functions
#m = rr.mf(micr,el,order,H)
#
### Microstructure functions in frequency space
#start = time.time()
#M = np.fft.fftn(m, axes = [0,1,2])
#del m
#size = M.nbytes
#end = time.time()
#timeE = np.round((end - start),2)
#
#msg = 'Size of microstructure function in frequency space: %s bytes' % size
#rr.WP(msg,wrt_file)
#msg = 'Convert microstructure function to frequency space: %s seconds' %timeE
#rr.WP(msg,wrt_file)


#### FINITE ELEMENT RESPONSES ###
#[resp, msg] = rr.load_fe(0,ns,el)
#resp_val = resp[:,:,:,-1]
#rr.WP(msg,wrt_file)
#
### responses in frequency space
#start = time.time()
#resp_fft = np.fft.fftn(resp, axes = [0,1,2]) 
#end = time.time()
#timeE = np.round((end - start),3)
#
#msg = 'Convert FE results to frequency space: %s seconds' %timeE
#rr.WP(msg,wrt_file)
#
#
#### CALIBRATION OF INFLUENCE COEFFICIENTS ###
#
#start = time.time()
#specinfc = np.zeros((el**3,H),dtype = 'complex64')
#
#specinfc[0,:] = rr.calib(0,M,resp_fft,0,H,el,ns)
#[specinfc[1,:],p] = rr.calib(1,M,resp_fft,0,H,el,ns)
#
### calib_red is simply calib with some default arguments
#calib_red = partial(rr.calib,M=M,resp_fft=resp_fft,p=p,H=H,el=el,ns=ns)
#
##specinfc[2:(el**3),:] = np.asarray(map(calib_red,range(2,el**3)))
#result = map(calib_red,range(2,el**3))
#specinfc[2:(el**3),:] = np.asarray(result)
#del result    
#
#end = time.time()
#timeE = np.round((end - start),3)
#msg = 'Calibration: %s seconds' %timeE
#rr.WP(msg,wrt_file)
#
#
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
