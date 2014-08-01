# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script evaluates the success of a given MKS calibration and validation
through metrics like MASE and maximum error as well as plotting strain
fields and histograms.

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt
import functions_ti_alpha_fip_v1 as rr
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
    
    Evm_pre = np.zeros((21**3))
    c = -1
    
    ## This reads through all the lines in the file.
     
    for k in xrange(21**3):
        c += 1                        
        
        st = np.zeros(6)
        for jj in range(6):
            st[jj] = linelist[line0 + c].split()[jj + 1]
        
        if k == 0:
            print st
            
        Evm_pre[k] = np.sqrt( 0.5*( (st[0]-st[1])**2 +(st[1]-st[2])**2 + (st[2]-st[0])**2 + 6*(st[3]**2 + st[4]**2 + st[5]**2) ) )

    
    f.close()    
         
    Evm = np.swapaxes(np.reshape(np.flipud(Evm_pre), [el,el,el]),1,2)

    return Evm


filename = 'Results_Ti64_RandomMicroFZreducedNewBCs_21x21x21_AbqInp_AnisoLE_00001_data_stress_max_C3.txt'
max_el = file_read(filename)

filename = 'Results_Ti64_RandomMicroFZreducedNewBCs_21x21x21_AbqInp_PowerLaw_00001_data_stress_max_C3.txt'
max_pl = file_read(filename)


### VISUAL COMPARISON OF ELASTIC AND PLASTIC SIMULATIONS ###

plt.close()

## pick a slice perpendicular to the z-direction
slc = 0

## find the min and max of both datasets for the slice of interest
#(needed to scale both images the same) 
dmin = np.amin([max_el[:,:,slc],max_pl[:,:,slc]])
dmax = np.amax([max_el[:,:,slc],max_pl[:,:,slc]])

## Plot slices of the response
plt.subplot(221)
ax = plt.imshow(max_el[:,:,slc], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.title('Linear Elastic, $\sigma_{vm}$ (MPa)')


plt.subplot(222)
ax = plt.imshow(max_pl[:,:,slc], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('CPFEM, $\sigma_{vm}$ (MPa)')



# Plot a histogram representing the frequency of strain levels with separate
# channels for each phase of each type of response.
plt.subplot(212)

## find the min and max of both datasets
dmin = np.amin([max_el,max_pl])
dmax = np.amax([max_el,max_pl])

elast = np.reshape(max_el,el**3)
plast = np.reshape(max_pl,el**3)

# select the desired number of bins in the histogram
bn = 40

# response histograms
n, bins, patches = plt.hist(elast, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
bincenters = 0.5*(bins[1:]+bins[:-1])
elast, = plt.plot(bincenters,n,'k', linestyle = '-', lw = 0.5)

# 1st order terms MKS histogram
n, bins, patches = plt.hist(plast, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
plast, = plt.plot(bincenters,n,'b', linestyle = '-', lw = 0.5)

plt.grid(True)

plt.legend([elast, plast], ["LE response", "CPFEM response"])

plt.xlabel("$\sigma_{vm}$ (MPa)")
plt.ylabel("Frequency")
plt.title("Frequency comparison of CPFEM and linear elastic results")



#### MEAN ABSOLUTE STRAIN ERROR (MASE) ###
avg_CPFEM = np.average(max_pl)
avg_LE= np.average(max_el)
MASE = 0
for k in xrange(el**3):
    [u,v,w] = np.unravel_index(k,[el,el,el])
    MASE += ((np.abs(max_pl[u,v,w] - max_el[u,v,w]))/(avg_CPFEM * el**3))

max_err = np.amax(max_pl-max_el)/avg_CPFEM    

msg = 'Mean Sigma_vm from LE: %s' %avg_LE
rr.WP(msg,wrt_file)
msg = 'Minimum Sigma_vm from LE: %s' % np.min(max_el)
rr.WP(msg,wrt_file)
msg = 'Maximum Sigma_vm from LE: %s' % np.max(max_el)
rr.WP(msg,wrt_file)

msg = 'Mean Sigma_vm from CPFEM: %s' %avg_CPFEM
rr.WP(msg,wrt_file)
msg = 'Minimum Sigma_vm from CPFEM: %s' % np.min(max_pl)
rr.WP(msg,wrt_file)
msg = 'Maximum Sigma_vm from CPFEM: %s' % np.max(max_pl)
rr.WP(msg,wrt_file)

msg = 'The mean absolute error is %s%%' %(MASE*100)
rr.WP(msg,wrt_file)
msg = 'The maximum error is %s%%' %(max_err*100)
rr.WP(msg,wrt_file)



