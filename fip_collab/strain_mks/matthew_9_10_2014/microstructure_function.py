# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script reads a set of microstructures designated by the set-ID and saves
the microstructure function in real and frequency space.

@author: nhpnp3
"""

import time
import numpy as np
import scipy.io as sio
import functions_ti_alpha_fip_v1 as rr

## el is the # of elements per side of the cube 
el = 21 
## the number of sample microstructures for calibration.
ns = 200
## specify the number of local states you are using
H = 15
## specify the set designation (string format)
set_id = 'cal'
## specify the file to write messages to 
wrt_file = 'mf_%s%s_%s.txt' %(ns,set_id,time.strftime("%Y-%m-%d_h%Hm%M")) 


## import microstructures
micr = np.zeros([el,el,el,ns,H], dtype = 'complex128')

#pre_micr = np.load('euler_GSH_%s%s.npy' %(ns,set_id))
pre_micr = sio.loadmat('euler_GSH_%s%s.mat' %(ns,set_id))['euler_GSH']

for h in xrange(H):
    for sn in range(ns):
        micr[:,:,:,sn,h] = np.swapaxes(np.reshape(np.flipud
                                (pre_micr[:,sn,h]), [el,el,el]),1,2)

msg = 'microstructures imported'
rr.WP(msg,wrt_file)

## Microstructure functions in frequency space
start = time.time()
M = np.fft.fftn(micr, axes = [0,1,2])
del micr
size = M.nbytes
np.save('M_%s%s' %(ns,set_id),M)
end = time.time()
timeE = np.round((end - start),2)

msg = 'Size of microstructure function in frequency space: %s bytes' % size
rr.WP(msg,wrt_file)
msg = 'Convert calibration microstructure function to frequency space: %s seconds' %timeE
rr.WP(msg,wrt_file)