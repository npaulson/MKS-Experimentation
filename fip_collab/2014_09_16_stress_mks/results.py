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
import functions_polycrystal_strain as rr
import matplotlib.pyplot as plt

def results(ns,set_id,comp,typ,real_comp):

    ## el is the # of elements per side of the cube 
    el = 21 
    ## specify the file to write messages to 
    wrt_file = 'results_comp%s_%s%s_%s.txt' %(comp,ns,set_id,time.strftime("%Y-%m-%d_h%Hm%M")) 
    
    mks_R = np.load('mksR%s_%s%s.npy' %(comp,ns,set_id))
    resp = np.load('r%s_%s%s.npy' %(comp,ns,set_id))
    
    
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
        
    
    msg = 'Average, %s%s, CPFEM: %s' %(typ,real_comp,avgE_fe)
    rr.WP(msg,wrt_file)
    msg = 'Average, %s%s, MKS: %s' %(typ,real_comp,avgE_mks)
    rr.WP(msg,wrt_file)
    msg = 'Standard deviation, %s%s, CPFEM: %s' %(typ,real_comp,np.std(resp))
    rr.WP(msg,wrt_file)
    msg = 'Standard deviation, %s%s, MKS: %s' %(typ,real_comp,np.std(mks_R))
    rr.WP(msg,wrt_file)  
    
    resp_min = np.mean(np.amin(np.reshape(resp,[el**3,ns]), axis=0))
    mks_R_min = np.mean(np.amin(np.reshape(mks_R,[el**3,ns]), axis=0))
    
    resp_max = np.mean(np.amax(np.reshape(resp,[el**3,ns]), axis=0))
    mks_R_max = np.mean(np.amax(np.reshape(mks_R,[el**3,ns]), axis=0))
    
    msg = 'Mean minimum, %s%s, CPFEM: %s' %(typ,real_comp,resp_min)
    rr.WP(msg,wrt_file)
    msg = 'Mean minimum, %s%s, MKS: %s' %(typ,real_comp,mks_R_min)
    rr.WP(msg,wrt_file)
    msg = 'Mean maximum, %s%s, CPFEM: %s' %(typ,real_comp,resp_max)
    rr.WP(msg,wrt_file)
    msg = 'Mean maximum, %s%s, MKS: %s' %(typ,real_comp,mks_R_max)
    rr.WP(msg,wrt_file)
    msg = 'mean absolute error (MAE): %s%%' %(MASE*100)
    rr.WP(msg,wrt_file)
    msg = 'Maximum error in all samples: %s%%' %(max_err*100)
    rr.WP(msg,wrt_file)
    msg = 'Average maximum error over all samples: %s%%' %(max_err_avg*100)
    rr.WP(msg,wrt_file)
    
    
    
    ### VISUALIZATION OF MKS VS. FEM ###
    
    plt.close('all')
    
    ## pick a slice perpendicular to the x-direction
    slc = 11
    sn = 20
    
    
    ## find the min and max of both datasets for the slice of interest
    #(needed to scale both images the same) 
    dmin = np.amin([resp[:,:,slc,sn],mks_R[:,:,slc,sn]])
    dmax = np.amax([resp[:,:,slc,sn],mks_R[:,:,slc,sn]])
    
    
    ## Plot slices of the response
    plt.figure(num=1,figsize=[12,4])
    
    plt.subplot(121)
    ax = plt.imshow(mks_R[:,:,slc,sn], origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('MKS $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))
    
    plt.subplot(122)
    ax = plt.imshow(resp[:,:,slc,sn], origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('CPFEM $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))
    
    
    # Plot a histogram representing the frequency of strain levels with separate
    # channels for each phase of each type of response.
    plt.figure(num=2,figsize=[12,5])
    
    ## find the min and max of both datasets (in full)
    dmin = np.amin([resp,mks_R])
    dmax = np.amax([resp,mks_R])
    
    fe = np.reshape(resp,ns*(el**3))
    mks = np.reshape(mks_R,ns*(el**3))
    
    
    # select the desired number of bins in the histogram
    bn = 40
    weight = np.ones_like(fe)/(el**3)
    
    # FEM histogram
    n, bins, patches = plt.hist(fe, bins = bn, histtype = 'step', hold = True,
                                range = (dmin, dmax), weights=weight, color = 'white')
    bincenters = 0.5*(bins[1:]+bins[:-1])
    fe, = plt.plot(bincenters,n,'k', linestyle = '-', lw = 0.5)
    
    # 1st order terms MKS histogram
    n, bins, patches = plt.hist(mks, bins = bn, histtype = 'step', hold = True,
                                range = (dmin, dmax), weights=weight, color = 'white')
    mks, = plt.plot(bincenters,n,'b', linestyle = '-', lw = 0.5)
    
    plt.grid(True)
    
    plt.legend([fe, mks], ["CPFEM response", "MKS predicted response"])
    
    plt.xlabel("$\%s_{%s}$" %(typ,real_comp))
    plt.ylabel("Number Fraction")
    plt.title("Frequency comparison of MKS and CPFEM $\%s_{%s}$ strain responses" %(typ,real_comp))