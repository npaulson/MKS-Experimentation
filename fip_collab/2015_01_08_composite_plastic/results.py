# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 13:52:33 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt
import functions_composite as rr


def results(el,ns,set_id,typ,wrt_file):

    ## vector of the indicial forms of the tensor components 
    real_comp = '11'
    
    mks_R = np.load('mksR_%s%s.npy' %(ns,set_id))
    resp = np.load('r_%s%s.npy' %(ns,set_id)).reshape([ns,el,el,el])

    ### VISUALIZATION OF MKS VS. FEM ###
    
    ## pick a slice perpendicular to the x-direction
    slc = 10
    sn = 0

    ## Plot slices of the response
    plt.figure(num=2,figsize=[12,4])
    
    dmin = np.min([mks_R[sn,slc,:,:],resp[sn,slc,:,:]])
    dmax = np.max([mks_R[sn,slc,:,:],resp[sn,slc,:,:]])
    
    plt.subplot(121)
    ax = plt.imshow(mks_R[sn,slc,:,:], origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('MKS $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))
    
    plt.subplot(122)
    ax = plt.imshow(resp[sn,slc,:,:], origin='lower', interpolation='none',
        cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('CPFEM $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))

    
#    plt.subplot(121)
#    ax = plt.imshow(mks_R[sn,slc,:,:], origin='lower', interpolation='none',
#        cmap='jet')
#    plt.colorbar(ax)
#    plt.title('MKS $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))
#    
#    plt.subplot(122)
#    ax = plt.imshow(resp[sn,slc,:,:], origin='lower', interpolation='none',
#        cmap='jet')
#    plt.colorbar(ax)
#    plt.title('CPFEM $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))

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
    msg = 'Standard deviation, %s%s, CPFEM: %s' %(typ,real_comp,np.std(resp))
    rr.WP(msg,wrt_file)
    msg = 'Standard deviation, %s%s, MKS: %s' %(typ,real_comp,np.std(mks_R))
    rr.WP(msg,wrt_file)  
    
    resp_min = np.mean(np.amin(resp.reshape([el**3,ns]), axis=0))
    mks_R_min = np.mean(np.amin(mks_R.reshape([el**3,ns]), axis=0))
    
    resp_max = np.mean(np.amax(resp.reshape([el**3,ns]), axis=0))
    mks_R_max = np.mean(np.amax(mks_R.reshape([el**3,ns]), axis=0))
    
    msg = 'Mean minimum, %s%s, CPFEM: %s' %(typ,real_comp,resp_min)
    rr.WP(msg,wrt_file)
    msg = 'Mean minimum, %s%s, MKS: %s' %(typ,real_comp,mks_R_min)
    rr.WP(msg,wrt_file)
    msg = 'Mean maximum, %s%s, CPFEM: %s' %(typ,real_comp,resp_max)
    rr.WP(msg,wrt_file)
    msg = 'Mean maximum, %s%s, MKS: %s' %(typ,real_comp,mks_R_max)
    rr.WP(msg,wrt_file)
    
if __name__ == '__main__':
    results(21,10,'val','epsilon','test.txt')
 