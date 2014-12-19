# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 13:52:33 2014

@author: nhpnp3
"""

import numpy as np
import functions as rr
import time
import matplotlib.pyplot as plt
import scipy.io as sio


def results(el,ns,set_id_cal,set_id,ccur,typ):    
    
    wrt_file = 'results_%s_%s%s_%s.txt' %(set_id_cal,ns,set_id,time.strftime("%Y-%m-%d_h%Hm%M"))        
    
    mks_R = np.load('mksR_%s%s.npy' %(ns,set_id))
    resp = np.load('r_%s%s.npy' %(ns,set_id)).reshape([ns,el,el,el])
    pre_euler = sio.loadmat('orientation_%s_%s.mat' %(set_id,ns))['eulerS'];

    euler = pre_euler.reshape([el,el,el,ns,3])


    ### VISUALIZATION OF MKS VS. FEM ###
    
    ## pick a slice perpendicular to the x-direction
    slc = 10
    sn = 0
    
    ## Plot slices of the response
    plt.close(2)    
    
    plt.figure(num=2,figsize=[18,4])


    plt.subplot(131)
    ax = plt.imshow(euler[slc,:,:,sn,0], origin='lower', interpolation='none',
        cmap='jet')#, vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('$\phi_1$ Euler Angle, slice %s' %slc)
   
    plt.subplot(132)
    ax = plt.imshow(mks_R[sn,slc,:,:], origin='lower', interpolation='none',
        cmap='jet')#, vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('MKS $\%s_{%s}$ response, slice %s' %(typ,ccur,slc))
    
    plt.subplot(133)
    ax = plt.imshow(resp[sn,slc,:,:], origin='lower', interpolation='none',
        cmap='jet')#, vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('CPFEM $\%s_{%s}$ response, slice %s' %(typ,ccur,slc)) 

    
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
        avgr_fe_indv= np.average(resp[sn,...])   
        avgr_mks_indv = np.average(mks_R[sn,...])
        
        avgr_fe_tot += avgr_fe_indv
        avgr_mks_tot += avgr_mks_indv
        max_diff_all[sn] = np.amax(abs(resp[sn,...]-mks_R[sn,...]))

    avgr_fe = avgr_fe_tot/ns
    avgr_mks = avgr_mks_tot/ns 
          
    ### DIFFERENCE MEASURES ###
    mean_diff_meas = np.mean(abs(resp-mks_R))/avgr_fe
    mean_max_diff_meas = np.mean(max_diff_all)/avgr_fe
    max_diff_meas_all = np.amax(abs(resp-mks_R))/avgr_fe
   
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
    msg = 'Standard deviation, %s%s, CPFEM: %s' %(typ,ccur,np.std(resp))
    rr.WP(msg,wrt_file)
    msg = 'Standard deviation, %s%s, MKS: %s' %(typ,ccur,np.std(mks_R))
    rr.WP(msg,wrt_file)  
    
    resp_min = np.mean(np.amin(resp.reshape([el**3,ns]), axis=0))
    mks_R_min = np.mean(np.amin(mks_R.reshape([el**3,ns]), axis=0))
    
    resp_max = np.mean(np.amax(resp.reshape([el**3,ns]), axis=0))
    mks_R_max = np.mean(np.amax(mks_R.reshape([el**3,ns]), axis=0))
    
    msg = 'Mean minimum, %s%s, CPFEM: %s' %(typ,ccur,resp_min)
    rr.WP(msg,wrt_file)
    msg = 'Mean minimum, %s%s, MKS: %s' %(typ,ccur,mks_R_min)
    rr.WP(msg,wrt_file)
    msg = 'Mean maximum, %s%s, CPFEM: %s' %(typ,ccur,resp_max)
    rr.WP(msg,wrt_file)
    msg = 'Mean maximum, %s%s, MKS: %s' %(typ,ccur,mks_R_max)
    rr.WP(msg,wrt_file)
       
    
if __name__ == '__main__':
    results(21,25,'calV2','val_equiaxed','11','sigma')
 