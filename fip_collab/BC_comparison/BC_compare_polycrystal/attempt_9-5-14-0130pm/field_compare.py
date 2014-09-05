# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 15:59:54 2014

@author: nhpnp3
"""
import numpy as np
import functions_ori_compare as fs
import matplotlib.pyplot as plt
import time

el = 21


column_num = 1

dat1 = np.load('FE_results_1test.npy')

filename = 'Results_Ti64_RandomMicroFZreducedNewBCs_21x21x21_AbqInp_AnisoLE_00001_data_strain_max_C1.txt'
dat2 = fs.file_read(filename,column_num, el = el)


slc = 10
   
plt.close('all')

dmin = np.amin([dat1[slc,:,:],dat2[slc,:,:]])
dmax = np.amax([dat1[slc,:,:],dat2[slc,:,:]])

plt.figure(num=1, figsize=[14,5])

plt.subplot(121)
ax = plt.imshow(dat1[slc,:,:], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.title('MINED LE, E11, C3D8R')
plt.colorbar(ax)  

plt.subplot(122)
ax = plt.imshow(dat2[slc,:,:], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.title('GOALI-Ti LE, E11, C3D8R')
plt.colorbar(ax)

def mase_meas(dat1,dat2,dat1avg):    
    MASE = 0
    for k in xrange(el**3):
        [u,v,w] = np.unravel_index(k,[el,el,el])
        MASE += ((np.abs(dat1[u,v,w] - dat2[u,v,w]))/(dat1avg * el**3))
        
    return MASE
    
def max_err_meas(dat1,dat2,dat1avg):
    max_err = np.amax(dat1-dat2)/dat1avg  
    
    return max_err

## specify the file to write messages to 
wrt_file = 'stats_compare_MINED_GOALI_C3D8R_%s.txt' %(time.strftime("%Y-%m-%d_h%Hm%M")) 
msg = 'Mean E11, MINED: ' + str(np.mean(dat1))
fs.WP(msg,wrt_file)
msg = 'Mean E11, GOALI: ' + str(np.mean(dat2))
fs.WP(msg,wrt_file)
msg = 'E11 Standard Deviation, MINED: ' + str(np.std(dat1))
fs.WP(msg,wrt_file)
msg = 'E11 Standard Deviation, GOALI: ' + str(np.std(dat2))
fs.WP(msg,wrt_file)
msg = 'E11 Mean Absolute Strain Error: ' + str(mase_meas(dat1,dat2,np.mean(dat1))*100) + '%'
fs.WP(msg,wrt_file)
msg = 'E11 Maximum Error: ' + str(max_err_meas(dat1,dat2,np.mean(dat1))*100) + '%'
fs.WP(msg,wrt_file)


#plt.subplot(121)
#ax = plt.imshow(dat1[slc,:,:], origin='lower', interpolation='none',
#    cmap='jet')
#plt.title('MINED LE')
#plt.colorbar(ax)  
#
#plt.subplot(122)
#ax = plt.imshow(dat2[slc,:,:], origin='lower', interpolation='none',
#    cmap='jet')
#plt.title('GOALI-Ti CPFEM')
#plt.colorbar(ax)
    