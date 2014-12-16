# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 16:46:35 2014

@author: nhpnp3
"""

import vtk_read as vtk
import time
import euler_to_gsh as gsh
import microstructure_function as msf
#import calibration
import validation
import results


ns_cal = 200
set_id_cal = 'cal'

ns_val = 50
set_id_val = 'val'

compl = ['11','22','33','12','23','31']

for step in xrange(1,7):

    wrt_file = 'log_step%s_%s.txt' %(step,time.strftime("%Y-%m-%d_h%Hm%M"))    
    
    vtk_filename = 'Results_Ti64_RandomMicroFZfinal_21x21x21_AbqInp_PowerLaw_%s_data_v2_0%s.vtk' %('%s',step)
    
    ## The tensorID determines the type of tensor data read from the .vtk file
    ## if tensorID == 0, we read the stress tensor        
    ## if tensorID == 1, we read the strain tensor        
    ## if tensorID == 2, we read the plastic strain tensor 
    
    tensor_ID = 0
    

#    ## Gather data from calibration vtk files
#    
#    dir_cal = 'cal'
#    
#    vtk.read_euler(ns_cal,set_id_cal,step,vtk_filename,dir_cal, wrt_file, 0)
#    
#    for comp in compl:
#        vtk.read_meas(ns_cal,set_id_cal,step,comp,vtk_filename,tensor_ID,dir_cal,wrt_file)
    
    
    ## Gather data from validation vtk files 
    
    dir_val = 'val'
    
    vtk.read_euler(ns_val,set_id_val,step,vtk_filename, dir_val, wrt_file)
    
    for comp in compl:
        vtk.read_meas(ns_val,set_id_val,step,comp,vtk_filename,tensor_ID,dir_val,wrt_file, 1)
        
        
#    ## Convert the orientations from the calibration datasets from bunge euler angles
#    ## to GSH coefficients
#    gsh.euler_to_gsh(ns_cal,set_id_cal,step,wrt_file)
    
    
    ## Convert the orientations from the validation datasets from bunge euler angles
    ## to GSH coefficients
    gsh.euler_to_gsh(ns_val,set_id_val,step,wrt_file)
    
    
#    ## Generate the fftn of the calibration microstructure function
#    msf.micr_func(ns_cal,set_id_cal,step,wrt_file)
       
       
    ## Generate the fftn of the validation microstructure function
    msf.micr_func(ns_val,set_id_val,step,wrt_file)
       
       
#    ## Perform the calibration
#    for comp in compl:
#        calibration.calibration_procedure(ns_cal,set_id_cal,step,comp,wrt_file)
       
       
    ## Perform the validation
    for comp in compl:
        validation.validation_procedure(ns_cal,ns_val,set_id_cal,set_id_val,step,comp,wrt_file)
        
    comp_app = 1;
    
    results.results_all(ns_val,set_id_val,step,'sigma',compl, comp_app)

