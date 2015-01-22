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
import functions as rr
#import matplotlib.pyplot as plt


def results_all(el,ns,set_id,step,typ,compl,comp_app):

    ## specify the file to write messages to 
    wrt_file = 'results_all_step%s_%s%s_%s.txt' %(step,ns,set_id,time.strftime("%Y-%m-%d_h%Hm%M")) 
    
    mks_R = np.zeros([ns,6,el,el,el])
    resp = np.zeros([ns,6,el,el,el])      
    
    for comp in xrange(6):
        ccur = compl[comp]
        mks_R[:,comp,...] = np.load('mksR%s_%s%s_s%s.npy' %(ccur,ns,set_id,step))
        resp[:,comp,...] = np.load('r%s_%s%s_s%s.npy' %(ccur,ns,set_id,step))
    
    
    app_resp = np.mean(resp[:,comp_app,...])
    
    for comp in xrange(6):

        ccur = compl[comp]

        ### WRITE HEADER TO FILE ###
        msg = ''
        rr.WP(msg,wrt_file)
        rr.WP(msg,wrt_file)
        msg = 'Results report for %s%s' %(typ,ccur)        
        rr.WP(msg,wrt_file)
        msg = ''
        rr.WP(msg,wrt_file)
        
        #### MEAN ABSOLUTE STRAIN ERROR (MASE) ###
        avgr_fe_tot = 0
        avgr_mks_tot = 0
        max_diff_all = np.zeros(ns)
        
        for sn in xrange(ns):
            avgr_fe_indv= np.average(resp[sn,comp,...])   
            avgr_mks_indv = np.average(resp[sn,comp,...])
            
            avgr_fe_tot += avgr_fe_indv
            avgr_mks_tot += avgr_mks_indv
            max_diff_all[sn] = np.amax(abs(resp[sn,comp,...]-mks_R[sn,comp,...]))
    
        avgr_fe = avgr_fe_tot/ns
        avgr_mks = avgr_mks_tot/ns
        
              
        ### DIFFERENCE MEASURES ###
        mean_diff_meas = np.mean(abs(resp[:,comp,...]-mks_R[:,comp,...]))/app_resp
        mean_max_diff_meas = np.mean(max_diff_all)/app_resp
        max_diff_meas_all = np.amax(abs(resp[:,comp,...]-mks_R[:,comp,...]))/app_resp
       
        msg = 'Mean voxel difference over all microstructures (divided by mean von-Mises meas), %s%s: %s%%' %(typ,ccur,mean_diff_meas*100)
        rr.WP(msg,wrt_file)
        msg = 'Average Maximum voxel difference per microstructure (divided by mean von-Mises meas), %s%s: %s%%' %(typ,ccur,mean_max_diff_meas*100)
        rr.WP(msg,wrt_file)  
        msg = 'Maximum voxel difference in all microstructures (divided by mean von-Mises meas), %s%s: %s%%' %(typ,ccur,max_diff_meas_all*100)
        rr.WP(msg,wrt_file)
        
        ### STANDARD STATISTICS ###
        msg = 'Average, %s%s, CPFEM: %s' %(typ,ccur,avgr_fe)
        rr.WP(msg,wrt_file)
        msg = 'Average, %s%s, MKS: %s' %(typ,ccur,avgr_mks)
        rr.WP(msg,wrt_file)
        msg = 'Standard deviation, %s%s, CPFEM: %s' %(typ,ccur,np.std(resp[:,comp,...]))
        rr.WP(msg,wrt_file)
        msg = 'Standard deviation, %s%s, MKS: %s' %(typ,ccur,np.std(mks_R[:,comp,...]))
        rr.WP(msg,wrt_file)  
        
        resp_min = np.mean(np.amin(np.reshape(resp[:,comp,...],[ns,el**3]), axis=1))
        mks_R_min = np.mean(np.amin(np.reshape(mks_R[:,comp,...],[ns,el**3]), axis=1))
        
        resp_max = np.mean(np.amax(np.reshape(resp[:,comp,...],[ns,el**3]), axis=1))
        mks_R_max = np.mean(np.amax(np.reshape(mks_R[:,comp,...],[ns,el**3]), axis=1))
        
        msg = 'Mean minimum, %s%s, CPFEM: %s' %(typ,ccur,resp_min)
        rr.WP(msg,wrt_file)
        msg = 'Mean minimum, %s%s, MKS: %s' %(typ,ccur,mks_R_min)
        rr.WP(msg,wrt_file)
        msg = 'Mean maximum, %s%s, CPFEM: %s' %(typ,ccur,resp_max)
        rr.WP(msg,wrt_file)
        msg = 'Mean maximum, %s%s, MKS: %s' %(typ,ccur,mks_R_max)
        rr.WP(msg,wrt_file)
   
        
#        ### VISUALIZATION OF MKS VS. FEM ###
#        
#        plt.close('all')
#        
#        ## pick a slice perpendicular to the x-direction
#        slc = 11
#        sn = 20
#        
#        
#        ## find the min and max of both datasets for the slice of interest
#        #(needed to scale both images the same) 
#        dmin = np.amin([resp[:,:,slc,comp,sn],mks_R[:,:,slc,comp,sn]])
#        dmax = np.amax([resp[:,:,slc,comp,sn],mks_R[:,:,slc,comp,sn]])
#        
#        
#        ## Plot slices of the response
#        plt.figure(num=1,figsize=[12,4])
#        
#        plt.subplot(121)
#        ax = plt.imshow(mks_R[:,:,slc,comp,sn], origin='lower', interpolation='none',
#            cmap='jet', vmin=dmin, vmax=dmax)
#        plt.colorbar(ax)
#        plt.title('MKS $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))
#        
#        plt.subplot(122)
#        ax = plt.imshow(resp[:,:,slc,comp,sn], origin='lower', interpolation='none',
#            cmap='jet', vmin=dmin, vmax=dmax)
#        plt.colorbar(ax)
#        plt.title('CPFEM $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))
#        
#        plt.savefig('field_step%s_comp%s_%s%s.png' %(step,comp,ns,set_id))                
#        
#        
#        # Plot a histogram representing the frequency of strain levels with separate
#        # channels for each phase of each type of response.
#        plt.figure(num=2,figsize=[12,5])
#        
#        ## find the min and max of both datasets (in full)
#        dmin = np.amin([resp[:,:,:,comp,:],mks_R[:,:,:,comp,:]])
#        dmax = np.amax([resp[:,:,:,comp,:],mks_R[:,:,:,comp,:]])
#        
#        fe = np.reshape(resp[:,:,:,comp,:],ns*(el**3))
#        mks = np.reshape(mks_R[:,:,:,comp,:],ns*(el**3))
#        
#        
#        # select the desired number of bins in the histogram
#        bn = 40
#        weight = np.ones_like(fe)/(el**3)
#        
#        # FEM histogram
#        n, bins, patches = plt.hist(fe, bins = bn, histtype = 'step', hold = True,
#                                    range = (dmin, dmax), weights=weight, color = 'white')
#        bincenters = 0.5*(bins[1:]+bins[:-1])
#        fe, = plt.plot(bincenters,n,'k', linestyle = '-', lw = 0.5)
#        
#        # 1st order terms MKS histogram
#        n, bins, patches = plt.hist(mks, bins = bn, histtype = 'step', hold = True,
#                                    range = (dmin, dmax), weights=weight, color = 'white')
#        mks, = plt.plot(bincenters,n,'b', linestyle = '-', lw = 0.5)
#        
#        plt.grid(True)
#        
#        plt.legend([fe, mks], ["CPFEM response", "MKS predicted response"])
#        
#        plt.xlabel("$\%s_{%s}$" %(typ,real_comp))
#        plt.ylabel("Number Fraction")
#        plt.title("Frequency comparison of MKS and CPFEM $\%s_{%s}$ strain responses" %(typ,real_comp))
#
#        plt.savefig('hist_step%s_comp%s_%s%s.png' %(step,comp,ns,set_id))                



if __name__ == '__main__':
    results_all(50,'val','sigma')
