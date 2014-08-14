# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script evaluates the success of a given MKS calibration and validation
through metrics like MASE and maximum error as well as plotting strain
fields and histograms.

@author: nhpnp3
"""

import time
import numpy as np
import functions_ti_alpha_fip_v1 as rr
import matplotlib.pyplot as plt

## el is the # of elements per side of the cube 
el = 21 
## select which order terms with nearest neighbors you would like to analyze
order = 1
## the number of sample microstructures for validation.
ns = 50
## specify the number of local states you are using
H = 15
## specify the set designation (string format)
set_id = 'val'
## specify the file to write messages to 
wrt_file = 'results_%s%s_%s.txt' %(ns,set_id,time.strftime("%Y-%m-%d_h%Hm%M")) 

mks_R = np.load('mksR_ord%s_%s%s.npy' %(order,ns,set_id))
resp = np.load('E33_%s%s.npy' %(ns,set_id))


#### MEAN ABSOLUTE STRAIN ERROR (MASE) ###
avgE_fe_tot = 0
avgE_mks_tot = 0
MASE_tot = 0
max_err_sum = 0
max_err_all = np.zeros(ns)

for sn in xrange(ns):
    [avgE_fe_indv,avgE_mks_indv, MASE_indv] = rr.eval_meas(mks_R[:,:,:,sn],
                                resp[:,:,:,sn],el)
    avgE_fe_tot += avgE_fe_indv
    avgE_mks_tot += avgE_mks_indv
    MASE_tot += MASE_indv
    max_err_sum += np.amax(resp[:,:,:,sn]-mks_R[:,:,:,sn])
    max_err_all[sn] = np.amax(resp[:,:,:,sn]-mks_R[:,:,:,sn])

avgE_fe = avgE_fe_tot/ns
avgE_mks = avgE_mks_tot/ns
MASE = MASE_tot/ns
max_err = np.amax(resp-mks_R)/avgE_fe
max_err_avg = max_err_sum/(ns * avgE_fe)
    

msg = 'The average E33 from the CPFEM %s' %avgE_fe
rr.WP(msg,wrt_file)
msg = 'The average E33 from the MKS %s' %avgE_mks
rr.WP(msg,wrt_file)
msg = 'The mean absolute error (MASE) is %s%%' %(MASE*100)
rr.WP(msg,wrt_file)
msg = 'The maximum error in all samples is %s%%' %(max_err*100)
rr.WP(msg,wrt_file)
msg = 'The average maximum error over all samples is %s%%' %(max_err_avg*100)
rr.WP(msg,wrt_file)


### VISUALIZATION OF MKS VS. FEM ###

plt.close()

## pick a slice perpendicular to the x-direction
slc = 9
sn = 15


## find the min and max of both datasets for the slice of interest
#(needed to scale both images the same) 
dmin = np.amin([resp[:,:,slc,sn],mks_R[:,:,slc,sn]])
dmax = np.amax([resp[:,:,slc,sn],mks_R[:,:,slc,sn]])


## Plot slices of the response
plt.subplot(221)
ax = plt.imshow(mks_R[:,:,slc,sn], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('MKS E33, 1st order terms')

plt.subplot(222)
ax = plt.imshow(resp[:,:,slc,sn], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('CPFEM E33')


# Plot a histogram representing the frequency of strain levels with separate
# channels for each phase of each type of response.
plt.subplot(212)

## find the min and max of both datasets (in full)
dmin = np.amin([resp,mks_R])
dmax = np.amax([resp,mks_R])

fe = np.reshape(resp,ns*(el**3))
mks = np.reshape(mks_R,ns*(el**3))


# select the desired number of bins in the histogram
bn = 40

# FEM histogram
n, bins, patches = plt.hist(fe, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
bincenters = 0.5*(bins[1:]+bins[:-1])
fe, = plt.plot(bincenters,n,'k', linestyle = '-', lw = 0.5)

# 1st order terms MKS histogram
n, bins, patches = plt.hist(mks, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
mks, = plt.plot(bincenters,n,'b', linestyle = '-', lw = 0.5)

plt.grid(True)

plt.legend([fe, mks], ["CPFEM FIP response", "MKS, 1st order terms"])

plt.xlabel("E33")
plt.ylabel("Frequency")
plt.title("Frequency comparison of 1st order MKS with CPFEM results")