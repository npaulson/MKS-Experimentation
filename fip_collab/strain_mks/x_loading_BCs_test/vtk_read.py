# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 11:32:08 2014

@author: nhpnp3
"""

import functions_ti_alpha_fip_v1 as rr
import numpy as np
import time
#import scipy.io as sio


## el is the # of elements per side of the cube 
el = 21 
## the number of sample microstructures for calibration.
ns = 5
## specify the number of local states you are using
H = 15
## specify the set designation (string format)
set_id = 'bc_test'
## specify the file to write messages to 
wrt_file = 'vtk_%s%s_%s.txt' %(ns,set_id,time.strftime("%Y-%m-%d_h%Hm%M")) 


euler = np.zeros([el**3,ns,3])
E = np.zeros([el**3,9,ns])
E11 = np.zeros([el,el,el,ns])

for sn in xrange(ns):
    l_sn = str(sn+1).zfill(5)  
    [euler_temp,E_temp] = rr.read_vtk('Results_Ti64_RandomMicroFZreducedNewBCs_21x21x21_AbqInp_PowerLaw_%s_data_v2_05.vtk' %l_sn)
    euler[:,sn,:] = euler_temp
    E[:,:,sn] = E_temp
    E11[:,:,:,sn] = np.swapaxes(np.reshape
                    (np.flipud(E_temp[:,0]), [el,el,el]),1,2)

np.save('E_%s%s' %(ns,set_id),E)
np.save('euler_%s%s' %(ns,set_id), euler)
np.save('E11_%s%s' %(ns,set_id), E11)


## responses in frequency space
start = time.time()
E11_fft = np.fft.fftn(E11, axes = [0,1,2]) 
np.save('E11_fft_%s%s' %(ns,set_id),E11_fft)  
end = time.time()
timeE = np.round((end - start),3)

msg = 'Convert calibration FIP results to frequency space: %s seconds' %timeE
rr.WP(msg,wrt_file)