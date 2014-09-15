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
ns = 200
## specify the number of local states you are using
H = 15
## specify the set designation (string format)
set_id = 'cal'
## specify the file to write messages to 
wrt_file = 'vtk_%s%s_%s.txt' %(ns,set_id,time.strftime("%Y-%m-%d_h%Hm%M")) 


euler = np.zeros([el**3,ns,3])
E11 = np.zeros([el,el,el,ns])

for sn in xrange(ns):
    l_sn = str(sn+1).zfill(5)  
    [euler_temp,E11_temp] = rr.read_vtk('Results_Ti64_RandomMicroFZfinal_21x21x21_AbqInp_PowerLaw_%s_data_v2_01.vtk' %l_sn)
    euler[:,sn,:] = euler_temp
    E11[:,:,:,sn] = np.swapaxes(np.reshape(np.flipud(E11_temp), [el,el,el]),1,2)


np.save('euler_%s%s' %(ns,set_id), euler)
#sio.savemat('euler_%s%s' %(ns,set_id), {'euler':euler})
np.save('E11_%s%s' %(ns,set_id), E11)


## responses in frequency space
start = time.time()
E11_fft = np.fft.fftn(E11, axes = [0,1,2]) 
del E11
np.save('E11_fft_%s%s' %(ns,set_id),E11_fft)  
end = time.time()
timeE = np.round((end - start),3)

msg = 'Convert calibration FIP results to frequency space: %s seconds' %timeE
rr.WP(msg,wrt_file)