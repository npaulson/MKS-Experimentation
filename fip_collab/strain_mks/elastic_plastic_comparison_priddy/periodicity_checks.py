# -*- coding: utf-8 -*-
"""
Created on Fri Aug 01 09:20:36 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt
import time



set_id = 'Comparo_C3maxStressVM'

## specify the file to write messages to 
wrt_file = '%s_%s.txt' %(set_id,time.strftime("%Y-%m-%d_h%Hm%M"))

## el is the # of elements per side of the cube 
el = 21 



### READ DATA FROM TEXT FILE ###
def file_read(filename):
    
    f = open(filename, "r")
    
    linelist = f.readlines()
    
    # line0 is the index of first line of the data
    line0 = 2;      
    
    resp = np.zeros((21**3,6))
    c = -1
    
    ## This reads through all the lines in the file.
     
    for k in xrange(21**3):
        c += 1                        
        resp[k,:] = linelist[line0 + c].split()[1:7]
    
    f.close()    
         
    return resp



filename = 'Results_Ti64_RandomMicroFZreducedNewBCs_21x21x21_AbqInp_AnisoLE_00001_data_strain_max_C3.txt'
resp = file_read(filename)


print np.mean(resp, axis = 0)

plt.close()

#resp_fft = np.fft.fftn(np.swapaxes(np.reshape(np.flipud(resp[:,3]), [el,el,el]),1,2), axes = [0,1,2])
#resp_lin = np.reshape(resp_fft, el**3)
#
#plt.subplot(211)
#plt.plot(np.real(resp_lin),'k.')
#
#plt.subplot(212)
#plt.plot(np.imag(resp_lin),'b.')



field_pr_fft = np.fft.fftn(np.swapaxes(np.reshape(np.flipud(resp[:,3]), [el,el,el]),1,2), axes = [0,1,2])
#resp_lin = np.reshape(resp_fft, el**3)

vec_pr = field_pr_fft[:,10,9]

plt.subplot(411)
plt.plot(np.real(vec_pr),'k-')

plt.subplot(412)
plt.plot(np.imag(vec_pr),'b-')



field_ya = np.load("FE_results_200cal.npy")

print np.mean(field_ya)

field_ya_fft = np.fft.fftn(field_ya[:,:,:,0], axes = [0])

vec_ya = field_ya_fft[:,10,9]

plt.subplot(413)
plt.plot(np.real(vec_ya),'k-')

plt.subplot(414)
plt.plot(np.imag(vec_ya),'b-')

