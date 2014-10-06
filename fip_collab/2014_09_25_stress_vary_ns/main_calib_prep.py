# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 16:46:35 2014

@author: nhpnp3
"""

#import numpy as np
#import vtk_read as vtk
import time
#import euler_to_gsh as gsh
#import microstructure_function as msf
import calibration
import validation
#import results

ns_cal = 500
set_id_cal = 'cal'

ns_val = 50
set_id_val = 'val'


for step in xrange(1,3):

    wrt_file = 'log_step%s_%s.txt' %(step,time.strftime("%Y-%m-%d_h%Hm%M"))
#    
#    vtk_filename = 'Results_Ti64_RandomMicroFZfinal_21x21x21_AbqInp_PowerLaw_%s_data_v2_0%s.vtk' %('%s',step)
#    
#    ## The tensorID determines the type of tensor data read from the .vtk file
#    ## if tensorID == 0, we read the stress tensor        
#    ## if tensorID == 1, we read the strain tensor        
#    ## if tensorID == 2, we read the plastic strain tensor 
#    
#    tensor_ID = 0
#    
#    if step == 1:    
#    
#        ## Gather euler angles from vtk files
#    
#        dir_cal = 'vtk_cal_stress_all_comp'
#        
#        vtk.read_euler(ns_cal,set_id_cal,vtk_filename,dir_cal, wrt_file)
#        
#        dir_val = 'vtk_val_stress_all_comp'
#        
#        vtk.read_euler(ns_val,set_id_val,vtk_filename, dir_val, wrt_file)
#             
#        
#        ## Convert the orientations from the calibration datasets from bunge euler angles
#        ## to GSH coefficients
#        gsh.euler_to_gsh(ns_cal,set_id_cal,wrt_file)
#        
#        
#        ## Convert the orientations from the validation datasets from bunge euler angles
#        ## to GSH coefficients
#        gsh.euler_to_gsh(ns_val,set_id_val,wrt_file)
#    
#    
#        ## Generate the fftn of the calibration microstructure function
#        msf.micr_func(ns_cal,set_id_cal,wrt_file)
#           
#           
#        ## Generate the fftn of the validation microstructure function
#        msf.micr_func(ns_val,set_id_val,wrt_file)
#    
#    
#    ## get response fields from vtk files
#    
#    for comp in xrange(9):
#        vtk.read_meas(ns_cal,set_id_cal,step,comp,vtk_filename, tensor_ID,dir_cal, wrt_file) 
#        
#    for comp in xrange(9):
#        vtk.read_meas(ns_val,set_id_val,step,comp,vtk_filename, tensor_ID, dir_val, wrt_file)

    ns_sizes = [50, 100, 150, 200, 300, 400, 500]     
    
    ## Perform the Calibration and Validation procedures for varying sample sizes    
    
    for ns_cal_v in ns_sizes:     

        ## Perform the calibration for varying sample sizes    
        for comp in xrange(9):
            calibration.calibration_procedure(ns_cal,ns_cal_v,set_id_cal,step,comp,wrt_file)
           
           
        ## Perform the validation for varying sample sizes
        for comp in xrange(9):
            validation.validation_procedure(ns_cal_v,ns_val,set_id_cal,set_id_val,step,comp,wrt_file)
            
        
#        results.results_all(ns_cal_v, ns_val, set_id_val, step, 'sigma')

