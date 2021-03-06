# -*- coding: utf-8 -*-
"""
Created on Thursday, August 14th, 2014


@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt
import functions_ti_alpha_fip_v1 as rr
import time

set_id = 'C_Epeff_comparison'
st_comp = "Epeff"
comp_latex = "$\epsilon^p_{eff}$"
column_num = 10

## specify the file to write messages to 
wrt_file = '%s_%s.txt' %(set_id,time.strftime("%Y-%m-%d_h%Hm%M"))

## el is the # of elements per side of the cube 
el = 21 


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

C_cp = np.zeros([el,el,el,3])
C_py = np.zeros([el,el,el,3])

filename = 'Results_Prebuilt_HCP_SinglePhase_Output_FakeMatl_1_0mm_9261el_LinElast_data_strain_pl_max_C1.txt'
C_py[:,:,:,0] = file_read(filename,column_num)

filename = 'Results_Prebuilt_HCP_SinglePhase_Output_FakeMatl_1_0mm_9261el_LinElast_data_strain_pl_max_C2.txt'
C_py[:,:,:,1] = file_read(filename,column_num)

filename = 'Results_Prebuilt_HCP_SinglePhase_Output_FakeMatl_1_0mm_9261el_LinElast_data_strain_pl_max_C3.txt'
C_py[:,:,:,2] = file_read(filename,column_num)

filename = 'Results_Prebuilt_HCP_SinglePhase_Output_FakeMatl_1_0mm_9261el_PowerLaw_data_strain_pl_max_C1.txt'
C_cp[:,:,:,0] = file_read(filename,column_num)

filename = 'Results_Prebuilt_HCP_SinglePhase_Output_FakeMatl_1_0mm_9261el_PowerLaw_data_strain_pl_max_C2.txt'
C_cp[:,:,:,1] = file_read(filename,column_num)

filename = 'Results_Prebuilt_HCP_SinglePhase_Output_FakeMatl_1_0mm_9261el_PowerLaw_data_strain_pl_max_C3.txt'
C_cp[:,:,:,2] = file_read(filename,column_num)

### VISUAL COMPARISON OF CPFEM AND LE+PY SIMULATIONS ###

plt.close()

## pick a slice perpendicular to the z-direction
slc = 10


## Plot slices of the response
plt.figure(1)

## find the min and max of both datasets for the slice of interest
#(needed to scale both images the same) 
dmin = np.amin(C_cp[:,:,slc,:])
dmax = np.amax(C_cp[:,:,slc,:])

for ii in xrange(3):
    plt_num = 231 + ii
    cyc = ii + 1

    plt.subplot(plt_num)
    ax = plt.imshow(C_cp[:,:,slc,ii], origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.title('Cycle %s maximum, CPFEM, %s' %(cyc, comp_latex))
    
    if ii == 2:
        plt.colorbar(ax)

## find the min and max of both datasets for the slice of interest
#(needed to scale both images the same) 
dmin = np.amin(C_py[:,:,slc,:])
dmax = np.amax(C_py[:,:,slc,:])

for ii in xrange(3):
    plt_num = 234 + ii
    cyc = ii + 1

    plt.subplot(plt_num)
    ax = plt.imshow(C_py[:,:,slc,ii], origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.title('Cycle %s maximum, LE+PY, %s' %(cyc, comp_latex))

    if ii == 2:
        plt.colorbar(ax)

# Plot a histogram representing the frequency of strain levels with separate
# channels for each phase of each type of response.
plt.figure(2)

C_cp_lin = np.zeros([el**3,3])
C_py_lin = np.zeros([el**3,3])

for ii in xrange(3):
    C_cp_lin[:,ii] = np.abs(np.reshape(C_cp[:,:,:,ii],el**3))
    C_py_lin[:,ii] = np.abs(np.reshape(C_py[:,:,:,ii],el**3))
    
## find the min and max of both datasets
dmin = np.amin([C_cp_lin,C_py_lin])
dmax = np.amax([C_cp_lin,C_py_lin])

# select the desired number of bins in the histogram
#bn = 250

## response histograms
for ii in xrange(3):
    plt_num = ii+2
    cyc = ii + 1

    plt.figure(plt_num)
    
#    n, bins, patches = plt.hist(C_cp_lin[:,ii], bins = bn, histtype = 'step', hold = True,
#                                range = (dmin, dmax), color = 'white')
#    bincenters = 0.5*(bins[1:]+bins[:-1])
    C_cp_lins = C_cp_lin[:,ii]
#    C_cp_lins, = plt.plot(bincenters,n,'k', linestyle = '-', lw = 0.5)
#    
#    n, bins, patches = plt.hist(C_py_lin[:,ii], bins = bn, histtype = 'step', hold = True,
#                                range = (dmin, dmax), color = 'white')
    C_py_lins = C_py_lin[:,ii]
#    C_py_lins, = plt.plot(bincenters,n,'b', linestyle = '-', lw = 0.5)
    
    bins = [1.0E-15,3.162E-15,1.0E-14,3.162E-14,1.0E-13,3.162E-13,1.0E-12,3.162E-12,1.0E-11,3.162E-11,1.0E-10,3.162E-10,1.0E-9,3.162E-9,1.0E-8,3.162E-8,1.0E-7,3.162E-7]    
    weight = np.ones_like(C_cp_lins)/(el**3)
    
    plt.hist([C_cp_lins,C_py_lins],histtype='step',bins=bins,color=['blue','purple'],weights=[weight, weight])    
#    plt.hist([C_cp_lins,C_py_lins],histtype='step',bins=bins,color=['blue','purple'],weights=[weight, weight],label=['poo','fart'])    

    
    plt.grid(True)
    
#    plt.legend([C_cp_lins,C_py_lins], ["CPFEM","LE+PY"])
    
    plt.xlabel(comp_latex)
    plt.ylabel("Number Fraction")
    plt.xscale('log')

    plt.axis([1.0E-15,5.0E-7, 0, 0.1])

    plt.title("Frequency comparison of %s in CPFEM (blue) and LE+PY (purple) for cycle %s" %(comp_latex,cyc))


## Generate data file for statistical summary
C_cp_avg = np.zeros(3)
for ii in xrange(3):
    C_cp_avg[ii] = np.average(C_cp[:,:,:,ii])


def mase_meas(C_cp,C_py,C_cp_avg):    
    MASE = 0
    for k in xrange(el**3):
        [u,v,w] = np.unravel_index(k,[el,el,el])
        MASE += ((np.abs(C_cp[u,v,w] - C_py[u,v,w]))/(C_cp_avg * el**3))
        
    return MASE
    
def max_err_meas(C_cp,C_py,C_cp_avg):
    max_err = np.amax(C_cp-C_py)/C_cp_avg  
    
    return max_err



for ii in xrange(3):
    cyc = ii + 1
    msg = 'Average %s, CPFEM, Cycle %s: %s' %(st_comp,cyc,np.average(C_cp[:,:,:,ii]))
    rr.WP(msg,wrt_file)
    msg = 'Average %s, LE+PY, Cycle %s: %s' %(st_comp,cyc,np.average(C_py[:,:,:,ii]))
    rr.WP(msg,wrt_file)

for ii in xrange(3):
    cyc = ii + 1
    msg = 'Standard deviation %s, CPFEM, Cycle %s: %s' %(st_comp,cyc,np.std(C_cp[:,:,:,ii]))
    rr.WP(msg,wrt_file)
    msg = 'Standard deviation %s, LE+PY, Cycle %s: %s' %(st_comp,cyc,np.std(C_py[:,:,:,ii]))
    rr.WP(msg,wrt_file)    
    
for ii in xrange(3):
    cyc = ii + 1
    msg = 'Minimum %s, CPFEM, Cycle %s: %s' %(st_comp,cyc,np.min(C_cp[:,:,:,ii]))
    rr.WP(msg,wrt_file)
    msg = 'Minimum %s, LE+PY, Cycle %s: %s' %(st_comp,cyc,np.min(C_py[:,:,:,ii]))
    rr.WP(msg,wrt_file)
    
for ii in xrange(3):
    cyc = ii + 1
    msg = 'Maximum %s, CPFEM, Cycle %s: %s' %(st_comp,cyc,np.max(C_cp[:,:,:,ii]))
    rr.WP(msg,wrt_file)
    msg = 'Maximum %s, LE+PY, Cycle %s: %s' %(st_comp,cyc,np.max(C_py[:,:,:,ii]))
    rr.WP(msg,wrt_file)
    
for ii in xrange(3):
    cyc = ii + 1
    msg = 'Mean absolute strain error (MASE), Cycle %s: %s%%' %(cyc,mase_meas(C_cp[:,:,:,ii],C_py[:,:,:,ii],C_cp_avg[ii])*100)
    rr.WP(msg,wrt_file)

for ii in xrange(3):
    cyc = ii + 1
    msg = 'Maximum error, Cycle %s: %s%%' %(cyc,max_err_meas(C_cp[:,:,:,ii],C_py[:,:,:,ii],C_cp_avg[ii])*100)
    rr.WP(msg,wrt_file)