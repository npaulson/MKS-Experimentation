# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 17:19:03 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt


# ns: # samples in validation dataset
ns = 50
# set_id: name of the validation dataset
set_id = 'val'
# typ: what sort of parameter are we evaluating the error for
typ = 'sigma'
# step: which step in the loading cycle is it
step = 1
# el: how many elements per side of a microstructure cube
el = 21

# real_comp_desig: vector of the indicial forms of the tensor components 
real_comp_desig = ['11','12','13','21','22','23','31','32','33','vm']    

# ns_sizes: array of the number of samples used in each calibration
ns_sizes = np.array([15, 20, 25, 50, 100, 150, 200, 300, 400, 500])
# num_sizes: how many different calibrations were performed
num_sizes = len(ns_sizes)
    

## Here we load all components of the validation dataset FEM responses   

# resp: array of the FEM responses for each component + the calculated von-Mises measure
resp = np.zeros([el,el,el,10,ns])
    
for comp in xrange(9):    
    resp[:,:,:,comp,:] = np.load('r%s_%s%s_s%s.npy' %(comp,ns,set_id,step))
    
# here we calculate the von-Mises measure from the other components    
resp[:,:,:,9,:] = np.sqrt( 0.5*( (resp[:,:,:,0,:]-resp[:,:,:,4,:])**2
                               + (resp[:,:,:,4,:]-resp[:,:,:,8,:])**2
                               + (resp[:,:,:,8,:]-resp[:,:,:,0,:])**2
                               + 6*(resp[:,:,:,5,:]**2
                                  + resp[:,:,:,6,:]**2
                                  + resp[:,:,:,1,:]**2) ) )    

print "FEM responses loaded"

# mean_resp_vm: the mean von-Mises measure in the validation datasets
mean_resp_vm = np.mean(resp[:,:,:,9,:])    
  

## Here we load all components of the MKS response for each component and calibration (with #samples detailed in 'ns_sizes')

# mks_R: array of mks resonses for each component + the calculated von-Mises measure for each calibration
mks_R = np.zeros([el,el,el,10,ns,num_sizes])
  
for cal_id in xrange(num_sizes):      
    
    for comp in xrange(9):
        mks_R[:,:,:,comp,:,cal_id] = np.load('mksR%s_%s%s_step%s_cal%s.npy' %(comp,ns,set_id,step,ns_sizes[cal_id]))
    
    # here we calculate the von-Mises measure from the other components
    mks_R[:,:,:,9,:,cal_id] = np.sqrt(0.5*((mks_R[:,:,:,0,:,cal_id] - mks_R[:,:,:,4,:,cal_id])**2
                                         + (mks_R[:,:,:,4,:,cal_id] - mks_R[:,:,:,8,:,cal_id])**2
                                         + (mks_R[:,:,:,8,:,cal_id] - mks_R[:,:,:,0,:,cal_id])**2
                                         + 6*(mks_R[:,:,:,5,:,cal_id]**2
                                            + mks_R[:,:,:,6,:,cal_id]**2
                                            + mks_R[:,:,:,1,:,cal_id]**2) ) )

print "MKS responses loaded"

plt.close('all')

# comp: which component id to plot
comp = 9
    
# real_comp: the real component form of the component id
real_comp = real_comp_desig[comp]        

### DIFFERENCE MEASURE ###

# error: vectorized array of errors for each calibration size
error = np.zeros([(el**3)*ns,num_sizes])

for cal_id in xrange(num_sizes):
    
    # calculate the error over all voxels and all samples per calibration type
    # error is the difference in responses in each voxel divided by the 
    # mean von-Mises error and multiplied by 100%
    pre_error = (100*abs(resp[:,:,:,comp,:]-mks_R[:,:,:,comp,:,cal_id]))/mean_resp_vm
    
    # vectorize the error for each calibration type and put into the error array    
    error[:,cal_id] = np.reshape(pre_error,(el**3)*ns)

print "Errors calculated"

### VISUALIZATION OF FIELDS OF INTEREST ###

## pick a slice perpendicular to the x-direction
slc = 11
sn = 20
cal_id = 0

## find the min and max of both datasets for the slice of interest
#(needed to scale both images the same) 
dmin = np.amin([resp[slc,:,:,comp,sn],mks_R[slc,:,:,comp,sn,cal_id]])
dmax = np.amax([resp[slc,:,:,comp,sn],mks_R[slc,:,:,comp,sn,cal_id]])

## Plot slices of the response
plt.figure(num=1,figsize=[12,4])

plt.subplot(121)
ax = plt.imshow(mks_R[slc,:,:,comp,sn,cal_id], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('MKS $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))

plt.subplot(122)
ax = plt.imshow(resp[slc,:,:,comp,sn], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.colorbar(ax)
plt.title('CPFEM $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))



### VISUALIZATION OF ERROR VIOLIN PLOTS ###

# create the figure as a subplot (this was the only way I got the violin plot
# to work)
fig, ax = plt.subplots(1, figsize=(12,7))

# calculate the violin plot, show the means on this plot
ax.violinplot(dataset = error, showextrema = False, showmedians= False, showmeans = True)

# create a vector of indexes for the x-ticks
x = np.arange(1, num_sizes + 1) 

# set the x-ticks and assign labels from a list of strings generated from 'ns_sizes'
ax.set_xticks(x)
ax.set_xticklabels(list(ns_sizes.astype(str)), rotation = 'vertical')

plt.xlabel("Number of calibration datasets")
plt.ylabel("%% error (normalized by mean $\%s_{vm}$)" %typ)
plt.title("Error Violin Chart, $\%s_{%s}$" %(typ,real_comp))
plt.grid(True)
# this makes the axis labels clearer, it may not be necessary
plt.tight_layout(pad = 0.1)
