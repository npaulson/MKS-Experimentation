# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 14:20:06 2014

@author: nhpnp3
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
wrt_file = 'nofft_p2_%s.txt' %time.strftime("%Y-%m-%d_h%Hm%M")


MM = np.load('MM_final_v3.npy')

start = time.time()     
p = rr.independent_columns(MM, .001) 
end = time.time()
timeE = end - start       
msg = 'find independent columns, time=%s' %timeE

calred = MM[p,:][:,p]
del MM

PM = np.load('PM_final_v3.npy')
resred = PM[p]
del PM


start = time.time()     
spec = np.linalg.solve(calred, resred).T
end = time.time()
timeE = end - start       
msg = 'lin solve, time=%s' %timeE
rr.WP(msg,wrt_file)

np.save('spec_v3',spec)

msg = 'calibration completed'
rr.WP(msg,wrt_file)