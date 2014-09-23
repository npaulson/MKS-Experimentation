# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 12:24:47 2014

@author: nhpnp3
"""

import numpy as np
import functions_polycrystal_strain as rr
import matplotlib.pyplot as plt

ns = 50
set_id = 'val'
typ = 'sigma'

## el is the # of elements per side of the cube 
el = 21 

## vector of the indicial forms of the tensor components 
real_comp_desig = ['11','12','13','21','22','23','31','32','33','vm']    

mks_R = np.zeros([el,el,el,10,ns])
resp = np.zeros([el,el,el,10,ns])      

for comp in xrange(9):
    mks_R[:,:,:,comp,:] = np.load('mksR%s_%s%s.npy' %(comp,ns,set_id))
    resp[:,:,:,comp,:] = np.load('r%s_%s%s.npy' %(comp,ns,set_id))

resp[:,:,:,9,:] = np.sqrt( 0.5*( (resp[:,:,:,0,:]-resp[:,:,:,4,:])**2 +(resp[:,:,:,4,:]-resp[:,:,:,8,:])**2 + (resp[:,:,:,8,:]-resp[:,:,:,0,:])**2 + 6*(resp[:,:,:,5,:]**2 + resp[:,:,:,6,:]**2 + resp[:,:,:,1,:]**2) ) )
mks_R[:,:,:,9,:] = np.sqrt( 0.5*( (mks_R[:,:,:,0,:]-mks_R[:,:,:,4,:])**2 +(mks_R[:,:,:,4,:]-mks_R[:,:,:,8,:])**2 + (mks_R[:,:,:,8,:]-mks_R[:,:,:,0,:])**2 + 6*(mks_R[:,:,:,5,:]**2 + mks_R[:,:,:,6,:]**2 + mks_R[:,:,:,1,:]**2) ) )

mean_resp_vm = np.mean(resp[:,:,:,9,:])

plt.close('all')


comp = 9;
    
real_comp = real_comp_desig[comp]        

### DIFFERENCE MEASURE ###
error = (100*abs(resp[:,:,:,comp,:]-mks_R[:,:,:,comp,:]))/mean_resp_vm

### VISUALIZATION OF ERROR HISTOGRAM ###

error = np.reshape(error,ns*(el**3))
resp_lin = np.reshape(resp[:,:,:,comp,:],ns*(el**3))

# Plot a histogram representing the frequency of strain levels with separate
# channels for each phase of each type of response.
plt.figure(num=1,figsize=[12,5])        
       
# select the desired number of bins in the histogram
bn = 15

# find the bin locations for the CPFEM response of interest
n, bins, patches = plt.hist(resp_lin, bins = bn, histtype = 'step', hold = True,
                            color = 'white')
                            
print "values per bin: "
print n

bincenters = 0.5*(bins[1:]+bins[:-1])
bincenters_l = list(np.round(bincenters).astype(int).astype(str))

min_error = np.zeros(bn)
perc02_error = np.zeros(bn)
quart1_error = np.zeros(bn)        
mean_error = np.zeros(bn)      
median_error = np.zeros(bn)    
quart3_error = np.zeros(bn)
perc99_error = np.zeros(bn)        
max_error = np.zeros(bn)      

error_in_bin_list = []     
bin_labels = []

for ii in xrange(bn):
    in_bin = (resp_lin >= bins[ii]) * (resp_lin < bins[ii + 1])
    error_in_bin = error * in_bin  
    error_in_bin = error_in_bin[(error_in_bin != 0)]       
    error_in_bin_list.append(error_in_bin)            
    
    min_error[ii] = np.min(error_in_bin)
    perc02_error[ii] = np.percentile(error_in_bin,2)    
    quart1_error[ii] = np.percentile(error_in_bin,25)
    median_error[ii] = np.median(error_in_bin)
    quart3_error[ii] = np.percentile(error_in_bin,75)            
    perc99_error[ii] = np.percentile(error_in_bin,98)    
    max_error[ii] = np.max(error_in_bin)
    
    label_cur = str(int(round(bins[ii]))) + ' - ' + str(int(round(bins[ii + 1])) - 1)
    bin_labels.append(label_cur)

plt.figure(num=2,figsize=[12,5])        

plt.boxplot(x = error_in_bin_list, labels = bin_labels)

plt.xticks(rotation=45)

plt.xlabel("bin ranges, $\%s_{%s}$ MPa" %(typ,real_comp))
plt.ylabel("%% error (normalized by mean $\%s_{vm}$)" %typ)
plt.title("Error Histogram, $\%s_{%s}$" %(typ,real_comp))


plt.figure(num=3,figsize=[12,5])

p1 = plt.scatter(bincenters, min_error, c='r', marker = '+')
p2 =plt.scatter(bincenters, perc02_error, c='k', marker = '.')
p3 = plt.scatter(bincenters, quart1_error, c='b', marker = '+')
p4 = plt.scatter(bincenters, median_error, c='k', marker = '_')
p5 = plt.scatter(bincenters, quart3_error, c='b', marker = 'x')
p6 =plt.scatter(bincenters, perc99_error, c='k', marker = '.')
p7 = plt.scatter(bincenters, max_error, c='r', marker = 'x')


plt.legend((p1, p2, p3, p4, p5, p6, p7),
           ('minimum','2nd percentile', '25th percentile', 'median', '75th percentile', '98th percentile', 'maximum'),
           scatterpoints=1,
           loc='upper left',
           ncol=3,
           fontsize=8)

plt.grid(True)
plt.axis([400,610,-.1,3])

plt.xlabel("bin centers, $\%s_{%s}$ MPa" %(typ,real_comp))
plt.ylabel("%% error (normalized by mean $\%s_{vm}$)" %typ)
plt.title("Error Histogram, $\%s_{%s}$" %(typ,real_comp))

#plt.savefig('hist_error%s_%s%s.png' %(comp,ns,set_id)