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


def results_all(ns,set_id,typ):

    ## el is the # of elements per side of the cube 
    el = 21 
    ## specify the file to write messages to 
    wrt_file = 'results_all_%s%s_%s.txt' %(ns,set_id,time.strftime("%Y-%m-%d_h%Hm%M")) 
    
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
    
    for comp in xrange(10):
        
        real_comp = real_comp_desig[comp]        

        ### WRITE HEADER TO FILE ###
        msg = ''
        rr.WP(msg,wrt_file)
        rr.WP(msg,wrt_file)
        msg = 'Results report for %s%s' %(typ,real_comp)        
        rr.WP(msg,wrt_file)
        msg = ''
        rr.WP(msg,wrt_file)
        
        #### MEAN ABSOLUTE STRAIN ERROR (MASE) ###
        avgr_fe_tot = 0
        avgr_mks_tot = 0
        MASE_tot = 0
        max_err_sum = 0
        max_diff_all = np.zeros(ns)
        
        for sn in xrange(ns):
            [avgr_fe_indv,avgr_mks_indv, MASE_indv] = rr.eval_meas(mks_R[:,:,:,comp,sn],
                                        resp[:,:,:,comp,sn],el)
            avgr_fe_tot += avgr_fe_indv
            avgr_mks_tot += avgr_mks_indv
            MASE_tot += MASE_indv
            max_err_sum += np.amax(abs(resp[:,:,:,comp,sn]-mks_R[:,:,:,comp,sn]))
            max_diff_all[sn] = np.amax(abs(resp[:,:,:,comp,sn]-mks_R[:,:,:,comp,sn]))
    
        avgr_fe = avgr_fe_tot/ns
        avgr_mks = avgr_mks_tot/ns
        MASE = MASE_tot/ns
        max_err = np.amax(abs(resp[:,:,:,comp,:]-mks_R[:,:,:,comp,:]))/avgr_fe
        max_err_avg = max_err_sum/(ns * avgr_fe)
        
        msg = 'mean absolute error (MAE), %s%s: %s%%' %(typ,real_comp,MASE*100)
        rr.WP(msg,wrt_file)
        msg = 'Maximum error in all samples, %s%s: %s%%' %(typ,real_comp,max_err*100)
        rr.WP(msg,wrt_file)
        msg = 'Average maximum error over all samples, %s%s: %s%%' %(typ,real_comp,max_err_avg*100)
        rr.WP(msg,wrt_file)        
        
        ### DIFFERENCE MEASURES ###
        mean_diff_meas = np.mean(abs(resp[:,:,:,comp,:]-mks_R[:,:,:,comp,:]))/mean_resp_vm
        mean_max_diff_meas = np.mean(max_diff_all)/mean_resp_vm
        max_diff_meas_all = np.amax(abs(resp[:,:,:,comp,:]-mks_R[:,:,:,comp,:]))/mean_resp_vm
       
        msg = 'Mean voxel difference over all microstructures (divided by mean von-Mises meas), %s%s: %s%%' %(typ,real_comp,mean_diff_meas*100)
        rr.WP(msg,wrt_file)
        msg = 'Average Maximum voxel difference per microstructure (divided by mean von-Mises meas), %s%s: %s%%' %(typ,real_comp,mean_max_diff_meas*100)
        rr.WP(msg,wrt_file)  
        msg = 'Maximum voxel difference in all microstructures (divided by mean von-Mises meas), %s%s: %s%%' %(typ,real_comp,max_diff_meas_all*100)
        rr.WP(msg,wrt_file)
        
        ### STANDARD STATISTICS ###
        msg = 'Average, %s%s, CPFEM: %s' %(typ,real_comp,avgr_fe)
        rr.WP(msg,wrt_file)
        msg = 'Average, %s%s, MKS: %s' %(typ,real_comp,avgr_mks)
        rr.WP(msg,wrt_file)
        msg = 'Standard deviation, %s%s, CPFEM: %s' %(typ,real_comp,np.std(resp[:,:,:,comp,:]))
        rr.WP(msg,wrt_file)
        msg = 'Standard deviation, %s%s, MKS: %s' %(typ,real_comp,np.std(mks_R[:,:,:,comp,:]))
        rr.WP(msg,wrt_file)  
        
        resp_min = np.mean(np.amin(np.reshape(resp[:,:,:,comp,:],[el**3,ns]), axis=0))
        mks_R_min = np.mean(np.amin(np.reshape(mks_R[:,:,:,comp,:],[el**3,ns]), axis=0))
        
        resp_max = np.mean(np.amax(np.reshape(resp[:,:,:,comp,:],[el**3,ns]), axis=0))
        mks_R_max = np.mean(np.amax(np.reshape(mks_R[:,:,:,comp,:],[el**3,ns]), axis=0))
        
        msg = 'Mean minimum, %s%s, CPFEM: %s' %(typ,real_comp,resp_min)
        rr.WP(msg,wrt_file)
        msg = 'Mean minimum, %s%s, MKS: %s' %(typ,real_comp,mks_R_min)
        rr.WP(msg,wrt_file)
        msg = 'Mean maximum, %s%s, CPFEM: %s' %(typ,real_comp,resp_max)
        rr.WP(msg,wrt_file)
        msg = 'Mean maximum, %s%s, MKS: %s' %(typ,real_comp,mks_R_max)
        rr.WP(msg,wrt_file)
   
        
        ### VISUALIZATION OF MKS VS. FEM ###
        
        plt.close('all')
        
        ## pick a slice perpendicular to the x-direction
        slc = 11
        sn = 20
        
        
        ## find the min and max of both datasets for the slice of interest
        #(needed to scale both images the same) 
        dmin = np.amin([resp[:,:,slc,comp,sn],mks_R[:,:,slc,comp,sn]])
        dmax = np.amax([resp[:,:,slc,comp,sn],mks_R[:,:,slc,comp,sn]])
        
        
        ## Plot slices of the response
        plt.figure(num=1,figsize=[12,4])
        
        plt.subplot(121)
        ax = plt.imshow(mks_R[:,:,slc,comp,sn], origin='lower', interpolation='none',
            cmap='jet', vmin=dmin, vmax=dmax)
        plt.colorbar(ax)
        plt.title('MKS $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))
        
        plt.subplot(122)
        ax = plt.imshow(resp[:,:,slc,comp,sn], origin='lower', interpolation='none',
            cmap='jet', vmin=dmin, vmax=dmax)
        plt.colorbar(ax)
        plt.title('CPFEM $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))
        
        plt.savefig('field_comp%s_%s%s.png' %(comp,ns,set_id))                
        
        
        # Plot a histogram representing the frequency of strain levels with separate
        # channels for each phase of each type of response.
        plt.figure(num=2,figsize=[12,5])
        
        ## find the min and max of both datasets (in full)
        dmin = np.amin([resp[:,:,:,comp,:],mks_R[:,:,:,comp,:]])
        dmax = np.amax([resp[:,:,:,comp,:],mks_R[:,:,:,comp,:]])
        
        fe = np.reshape(resp[:,:,:,comp,:],ns*(el**3))
        mks = np.reshape(mks_R[:,:,:,comp,:],ns*(el**3))
        
        
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

        plt.savefig('hist_comp%s_%s%s.png' %(comp,ns,set_id))                


def error_hist(ns,set_id,typ):

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
    
    
    for comp in xrange(8,9):
        
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
        bn = 10
        
        # find the bin locations for the CPFEM response of interest
        n, bins, patches = plt.hist(resp_lin, bins = bn, histtype = 'step', hold = True,
                                    color = 'white')
                                    
        print "values per bin: "
        print n
        
        bincenters = 0.5*(bins[1:]+bins[:-1])
        bincenters_l = list(np.round(bincenters).astype(int).astype(str))
        
        print bincenters_l

        
        min_error = np.zeros(bn)
        quart1_error = np.zeros(bn)        
        mean_error = np.zeros(bn)        
        quart3_error = np.zeros(bn)        
        max_error = np.zeros(bn)      
        
        error_in_bin_list = []     
        
        
        for ii in xrange(bn):
            in_bin = (resp_lin >= bins[ii]) * (resp_lin < bins[ii + 1])
            error_in_bin = error * in_bin          
            error_in_bin_list.append(error_in_bin)            
            
#            min_error[ii] = np.min(error_in_bin)
#            quart1_error[ii] = np.percentile(error_in_bin,25)
#            mean_error[ii] = np.mean(error_in_bin)
#            quart3_error[ii] = np.percentile(error_in_bin,75)            
#            max_error[ii] = np.max(error_in_bin)
            
        plt.boxplot(x = error_in_bin_list)
    
        
#        error, = plt.plot(bincenters,n,'r', linestyle = '-', lw = 1)       
#        plt.plot(bincenters, min_error, )        
#        
#        plt.grid(True)
#        
#        plt.legend([error], ["Von-Mises Normalized Error"])
#        
#        plt.xlabel("Percent Error, $\%s_{%s}$" %(typ,real_comp))
#        plt.ylabel("Number Fraction")
#        plt.title("Error Histogram, $\%s_{%s}$" %(typ,real_comp))
#        plt.xscale('log')
#        plt.yscale('log')
#        plt.axis([.01,2, 1e-6, 0.2])
        
#        plt.savefig('hist_error%s_%s%s.png' %(comp,ns,set_id)
          
if __name__ == '__main__':
    error_hist(50,'val','sigma')