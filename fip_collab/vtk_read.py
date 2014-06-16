# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 11:32:08 2014

@author: nhpnp3
"""

import functions_ti_alpha_fip_v1 as rr
import numpy as np
import time


## el is the # of elements per side of the cube 
el = 21 
## select which order terms with nearest neighbors you would like to analyze
order = 1
## the number of sample microstructures for calibration.
ns = 200
## specify the number of local states you are using
H = 15
## specify the set designation (string format)
set_id = 'cal'
## specify the file to write messages to 
wrt_file = 'fe_%s%s_%s.txt' %(ns,set_id,time.strftime("%Y-%m-%d_h%Hm%M")) 


euler = np.zeros([el**3,ns,3])
fip = np.zeros([el,el,el,ns])

for sn in xrange(ns):
    l_sn = str(sn+1).zfill(5)  
    [euler_temp,fip_temp] = rr.read_vtk('Results_Ti64_RandomMicro_21x21x21_AbaqusInput_%s_data_v2_06.vtk' %l_sn)
    euler[:,sn,:] = euler_temp
    fip[:,:,:,sn] = np.swapaxes(np.reshape
                        (np.flipud(fip_temp), [el,el,el]),1,2)

np.save('euler_%s%s' %(ns,set_id), euler)
np.save('fip_%s%s' %(ns,set_id), fip)


## responses in frequency space
start = time.time()
fip_fft = np.fft.fftn(fip, axes = [0,1,2]) 
del fip
np.save('fip_fft_%s%s' %(ns,set_id),fip_fft)  
end = time.time()
timeE = np.round((end - start),3)

msg = 'Convert calibration FIP results to frequency space: %s seconds' %timeE
rr.WP(msg,wrt_file)