# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 13:52:33 2014

@author: nhpnp3
"""

import numpy as np
#import matplotlib.pyplot as plt
import functions_composite as rr


def results(el,ns,set_id,typ,wrt_file):

    ## vector of the indicial forms of the tensor components 
    real_comp = '11'
    
    mks_R = np.load('mksR_%s%s.npy' %(ns,set_id))
    resp = np.load('r_%s%s.npy' %(ns,set_id)).reshape([ns,el,el,el])
#    micr = np.load('pre_msf_%s%s.npy' %(ns,set_id))





#    maxindx = np.unravel_index(np.argmax(np.abs(resp - mks_R)),resp.shape)
#    maxresp = resp[maxindx]
#    maxMKS = mks_R[maxindx]
#    maxerr = (np.abs(resp - mks_R)[maxindx]/np.mean(resp))*100
#   
#    print 'indices of max error'
#    print maxindx    
#    print 'reference response at max error'    
#    print maxresp
#    print 'MKS response at max error'
#    print maxMKS
#    print 'maximum error'    
#    print maxerr
#
#    print micr[maxindx[0],:,maxindx[1],maxindx[2],maxindx[3]]
#
#
#    ### VISUALIZATION OF MKS VS. FEM ###
#    
#    ## pick a slice perpendicular to the x-direction
#    slc = maxindx[1]
#    sn = maxindx[0]
#
#    ## Plot slices of the response
#    plt.figure(num=2,figsize=[16,8])
#    
#    dmin = np.min([mks_R[sn,slc,:,:],resp[sn,slc,:,:]])
#    dmax = np.max([mks_R[sn,slc,:,:],resp[sn,slc,:,:]])
#    
#    plt.subplot(231)
#    ax = plt.imshow(micr[sn,0,slc,:,:], origin='lower', interpolation='none',
#        cmap='jet', vmin=dmin, vmax=dmax)
#    plt.colorbar(ax)
#    plt.title('phase map, slice %s' %(slc))    
#        
#    plt.subplot(232)
#    ax = plt.imshow(mks_R[sn,slc,:,:], origin='lower', interpolation='none',
#        cmap='jet', vmin=dmin, vmax=dmax)
#    plt.colorbar(ax)
#    plt.title('MKS $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))
#    
#    plt.subplot(233)
#    ax = plt.imshow(resp[sn,slc,:,:], origin='lower', interpolation='none',
#        cmap='jet', vmin=dmin, vmax=dmax)
#    plt.colorbar(ax)
#    plt.title('CPFEM $\%s_{%s}$ response, slice %s' %(typ,real_comp,slc))
#
#
#    # Plot a histogram representing the frequency of strain levels with separate
#    # channels for each phase of each type of response.
#    plt.subplot(212)
#    
#    ## find the min and max of both datasets (in full)
#    dmin = np.amin([resp,mks_R])
#    dmax = np.amax([resp,mks_R])
#    
#    
#    micr0 = micr[:,0,:,:,:].reshape(ns*el*el*el).astype(int)
#    
#    resp_lin = resp.reshape(ns*el*el*el)    
#    mks_lin = mks_R.reshape(ns*el*el*el)
#    
#    tmp = np.nonzero(micr0)
#    feb = resp_lin[tmp]
#    mks1b = mks_lin[tmp]
#    
#    tmp = np.nonzero(micr0 == 0)
#    few = resp_lin[tmp]
#    mks1w = mks_lin[tmp]        
#            
#        
#    # separating each response by phase
##    tmp = resp.reshape(ns*el*el*el)
##    feb = tmp[micr0]
##    print feb
##    few = tmp[micr1]
##    tmp = mks_R.reshape(ns*el*el*el)
##    mks1b = tmp[micr0] 
##    mks1w = tmp[micr1]
#        
#    # select the desired number of bins in the histogram
#    bn = 40
#    
##    n, bins, patches = plt.hist(feb, bins = bn, histtype = 'step', hold = True,
##                                color = 'white')
##    bincenters = 0.5*(bins[1:]+bins[:-1])
##    febp, = plt.plot(bincenters,n,'k', linestyle = '--', lw = 1.5)    
#
#
#
#    # FEM histogram
#    n, bins, patches = plt.hist(feb, bins = bn, histtype = 'step', hold = True,
#                                range = (dmin, dmax), color = 'white')
#    bincenters = 0.5*(bins[1:]+bins[:-1])
#    febp, = plt.plot(bincenters,n,'k', linestyle = '--', lw = 1.5)
#    
#    n, bins, patches = plt.hist(few, bins = bn, histtype = 'step', hold = True,
#                                range = (dmin, dmax), color = 'white')
#    fewp, = plt.plot(bincenters,n,'k')
#    
#    # MKS histogram
#    n, bins, patches = plt.hist(mks1b, bins = bn, histtype = 'step', hold = True,
#                                range = (dmin, dmax), color = 'white')
#    mks1bp, = plt.plot(bincenters,n,'b', linestyle = '--', lw = 1.5)
#    
#    n, bins, patches = plt.hist(mks1w, bins = bn, histtype = 'step', hold = True,
#                                range = (dmin, dmax), color = 'white')
#    mks1wp, = plt.plot(bincenters,n,'b')
#
#    
#    plt.grid(True)
#    
#    plt.legend([febp,fewp,mks1bp,mks1wp], ["FE - stiff phase", 
#               "FE - compliant phase", "MKS - stiff phase",
#               "MKS - compliant phase"])
#    
#    plt.xlabel("Strain")
#    plt.ylabel("Frequency")
#    plt.title("Frequency comparison MKS with FE results")


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
    results(21,190,'valRpc','epsilon','test.txt')
 