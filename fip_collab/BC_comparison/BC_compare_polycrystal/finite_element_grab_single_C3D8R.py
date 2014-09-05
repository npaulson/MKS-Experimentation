# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

@author: nhpnp3
"""

import time
import numpy as np
import function_load_fe_single_C3D8R as rr

## el is the # of elements per side of the cube 
el = 21 
## select which order terms with nearest neighbors you would like to analyze
order = 1
## the number of sample microstructures for calibration.
ns = 1
## specify the number of local states you are using
H = 15
## specify the set designation (string format)
set_id = 'test'
## specify the file to write messages to 
wrt_file = 'fe_%s%s_%s.txt' %(ns,set_id,time.strftime("%Y-%m-%d_h%Hm%M")) 


### FINITE ELEMENT RESPONSES: CALIBRATION ###
[resp, msg] = rr.load_fe('orientation1.mat','yuksel_ori_test_C3D8R.dat',el)
np.save('FE_results_%s%s' %(ns,set_id),resp)  
rr.WP(msg,wrt_file)

## responses in frequency space
start = time.time()
resp_fft = np.fft.fftn(resp, axes = [0,1,2]) 
del resp
np.save('FE_results_fft_%s%s' %(ns,set_id),resp_fft)  
end = time.time()
timeE = np.round((end - start),3)

msg = 'Convert calibration FE results to frequency space: %s seconds' %timeE
rr.WP(msg,wrt_file)