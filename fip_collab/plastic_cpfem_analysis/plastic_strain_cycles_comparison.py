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

set_id = 'CmaxE33_plastic_comparison'

## specify the file to write messages to 
wrt_file = '%s_%s.txt' %(set_id,time.strftime("%Y-%m-%d_h%Hm%M"))


## el is the # of elements per side of the cube 
el = 21 

st_comp = "E33"
comp_latex = "$\epsilon^p_{33}$"

### READ DATA FROM TEXT FILE ###

def file_read(filename, column_num):
    
    f = open(filename, "r")
    
    linelist = f.readlines()
    
    # line0 is the index of first line of the data
    line0 = 2;      
    
    E_pre = np.zeros((21**3))
    c = -1
    
    ## This reads through all the lines in the file.
     
    for k in xrange(21**3):
        c += 1                        
        E_pre[k] = linelist[line0 + c].split()[column_num]
    
    f.close()    
         
    E = np.swapaxes(np.reshape(np.flipud(E_pre), [el,el,el]),1,2)

    return E

column_num = 3

filename = 'Results_Ti64_RandomMicroFZreducedNewBCs_21x21x21_AbqInp_PowerLaw_00001_data_strain_pl_max_C1_Python.txt'
C1 = file_read(filename,column_num)

filename = 'Results_Ti64_RandomMicroFZreducedNewBCs_21x21x21_AbqInp_PowerLaw_00001_data_strain_pl_max_C2_Python.txt'
C2 = file_read(filename,column_num)

filename = 'Results_Ti64_RandomMicroFZreducedNewBCs_21x21x21_AbqInp_PowerLaw_00001_data_strain_pl_max_C3_Python.txt'
C3 = file_read(filename,column_num)


### VISUAL COMPARISON OF ELASTIC AND PLASTIC SIMULATIONS ###

plt.close()

## pick a slice perpendicular to the z-direction
slc = 10

## find the min and max of both datasets for the slice of interest
#(needed to scale both images the same) 
dmin = np.amin([C1[:,:,slc],C2[:,:,slc],C3[:,:,slc]])
dmax = np.amax([C1[:,:,slc],C2[:,:,slc],C3[:,:,slc]])

## Plot slices of the response
plt.subplot(231)
ax = plt.imshow(C1[:,:,slc], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.title('Cycle 1 maximum, %s' %comp_latex)


plt.subplot(232)
ax = plt.imshow(C2[:,:,slc], origin='lower', interpolation='none',
    cmap='jet', vmin=dmin, vmax=dmax)
plt.title('Cycle 2 maximum, %s' %comp_latex)


plt.subplot(233)
ax = plt.imshow(C3[:,:,slc], origin='lower', interpolation='none',
    cmap='jet')
plt.colorbar(ax)
plt.title('Cycle 3 maximum, %s' %comp_latex)


# Plot a histogram representing the frequency of strain levels with separate
# channels for each phase of each type of response.
plt.subplot(212)

## find the min and max of both datasets
dmin = np.amin([C1,C2,C3])
dmax = np.amax([C1,C2,C3])

C1_lin = np.reshape(C1,el**3)
C2_lin = np.reshape(C2,el**3)
C3_lin = np.reshape(C3,el**3)

# select the desired number of bins in the histogram
bn = 250

# response histograms
n, bins, patches = plt.hist(C1_lin, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
bincenters = 0.5*(bins[1:]+bins[:-1])
C1_lin, = plt.plot(bincenters,n,'k', linestyle = '-', lw = 0.5)

n, bins, patches = plt.hist(C2_lin, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
C2_lin, = plt.plot(bincenters,n,'b', linestyle = '-', lw = 0.5)

n, bins, patches = plt.hist(C3_lin, bins = bn, histtype = 'step', hold = True,
                            range = (dmin, dmax), color = 'white')
C3_lin, = plt.plot(bincenters,n,'g', linestyle = '-', lw = 0.5)


plt.grid(True)

plt.legend([C1_lin,C2_lin,C3_lin], ["Cycle 1 Max", "Cycle 2 Max", "Cycle 3 Max"])

plt.xlabel(comp_latex)
plt.ylabel("Frequency")
plt.title("Frequency comparison of plastic strain over 3 loading cycles")


msg = 'Average %s, Cycle 1: %s' %(st_comp,np.average(C1))
rr.WP(msg,wrt_file)
msg = 'Average %s, Cycle 2: %s' %(st_comp,np.average(C2))
rr.WP(msg,wrt_file)
msg = 'Average %s, Cycle 3: %s' %(st_comp,np.average(C3))
rr.WP(msg,wrt_file)

msg = 'Standard deviation %s, Cycle 1: %s' %(st_comp,np.std(C1))
rr.WP(msg,wrt_file)
msg = 'Standard deviation %s, Cycle 2: %s' %(st_comp,np.std(C2))
rr.WP(msg,wrt_file)
msg = 'Standard deviation %s, Cycle 3: %s' %(st_comp,np.std(C3))
rr.WP(msg,wrt_file)

msg = 'Minimum %s, Cycle 1: %s' %(st_comp,np.min(C1))
rr.WP(msg,wrt_file)
msg = 'Minimum %s, Cycle 2: %s' %(st_comp,np.min(C2))
rr.WP(msg,wrt_file)
msg = 'Minimum %s, Cycle 3: %s' %(st_comp,np.min(C3))
rr.WP(msg,wrt_file)

msg = 'Maximum %s, Cycle 1: %s' %(st_comp,np.max(C1))
rr.WP(msg,wrt_file)
msg = 'Maximum %s, Cycle 2: %s' %(st_comp,np.max(C2))
rr.WP(msg,wrt_file)
msg = 'Maximum %s, Cycle 3: %s' %(st_comp,np.max(C3))
rr.WP(msg,wrt_file)

#MASE = 0
#for k in xrange(el**3):
#    [u,v,w] = np.unravel_index(k,[el,el,el])
#    MASE += ((np.abs(max_pl[u,v,w] - max_el[u,v,w]))/(avg_CPFEM * el**3))
#
#max_err = np.amax(max_pl-max_el)/avg_CPFEM    

