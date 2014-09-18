# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 16:46:35 2014

@author: nhpnp3
"""

import vtk_read as vtk
import time
import euler_to_gsh as gsh
import microstructure_function as msf
import calibration
import validation

wrt_file = 'log_%s.txt' %time.strftime("%Y-%m-%d_h%Hm%M")

ns_cal = 200
set_id_cal = 'cal'

ns_val = 50
set_id_val = 'val'

vtk_filename = 'Results_Ti64_RandomMicroFZfinal_21x21x21_AbqInp_PowerLaw_%s_data_v2_01.vtk'

## The tensorID determines the type of tensor data read from the .vtk file
## if tensorID == 0, we read the stress tensor        
## if tensorID == 1, we read the strain tensor        
## if tensorID == 2, we read the plastic strain tensor 

tensor_ID = 0

## Gather data from calibration vtk files

vtk.read_euler(ns_cal,set_id_cal,vtk_filename, wrt_file)

for comp in xrange(9):
    vtk.read_meas(ns_cal,set_id_cal,comp,vtk_filename, tensor_ID, wrt_file)

## Gather data from validation vtk files 

vtk.read_euler(ns_cal,set_id_cal,vtk_filename, wrt_file)

for comp in xrange(9):
    vtk.read_meas(ns_val,set_id_val,comp,vtk_filename, tensor_ID, wrt_file)
    
    
## Convert the orientations from the calibration datasets from bunge euler angles
## to GSH coefficients
gsh.euler_to_gsh(ns_cal,set_id_cal,wrt_file)

## Convert the orientations from the validation datasets from bunge euler angles
## to GSH coefficients
gsh.euler_to_gsh(ns_val,set_id_val,wrt_file)

## Generate the fftn of the calibration microstructure function
for comp in xrange(9):
    msf.micr_func(ns_cal,set_id_cal,comp,wrt_file)
    
## Generate the fftn of the validation microstructure function
for comp in xrange(9):
    msf.micr_func(ns_val,set_id_val,comp,wrt_file)
    
## Perform the calibration
for comp in xrange(9):
    calibration.calibration_procedure(ns_cal,set_id_cal,comp,wrt_file)
    
## Perform the validation
for comp in xrange(9):
    validation.validation_procedure(ns_cal,ns_val,set_id_cal,set_id_val,comp,wrt_file)
    

    


