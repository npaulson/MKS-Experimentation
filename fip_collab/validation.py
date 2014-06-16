# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script predicts the FE response of a set of microstructures designated by
a specific set-ID using a previously calibrated MKS

@author: nhpnp3
"""

import time
import numpy as np
import functions_ti_alpha_ord1_alt as rr


## el is the # of elements per side of the cube 
el = 21 
## select which order terms with nearest neighbors you would like to analyze
order = 1
## the number of sample microstructures for validation.
ns = 50
## the number of sample microsturctures for calibration.
ns_cal = 200
## specify the number of local states you are using
H = 15
## specify the set designation (string format)
set_id = 'val'
## specify the set-ID for calibration (string format)
set_id_cal = 'cal'
## specify the file to write messages to 
wrt_file = 'validation_%s%s_%s.txt' %(ns,set_id,
                                      time.strftime("%Y-%m-%d_h%Hm%M")) 

M = np.load('M_%s%s.npy' %(ns,set_id))
specinfc = np.load('specinfc_%s%s.npy' %(ns_cal,set_id_cal))


mks_R = np.zeros([el,el,el,6,ns])

for sn in xrange(ns):
    mks_R[:,:,:,sn] = rr.validate(M[:,:,:,sn,:],specinfc[:,:],H,el)

msg = 'validation performed'
rr.WP(msg,wrt_file)

np.save('mksR_ord%s_%s%s' %(order,ns,set_id), mks_R)