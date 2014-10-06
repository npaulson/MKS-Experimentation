# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 16:46:35 2014

@author: nhpnp3
"""

import fe_grab
import time
import euler_to_gsh as gsh
import microstructure_function as msf
import calibration
import validation
import results

wrt_file = 'log_%s.txt' %time.strftime("%Y-%m-%d_h%Hm%M")

ns_cal = 200
set_id_cal = 'cal'

ns_val = 50
set_id_val = 'val'


## Gather data from calibration dat files

dir_cal = 'cal_stress_all_comp'

fe_grab.fe_grab(ns_cal, set_id_cal, dir_cal, wrt_file)


## Gather data from validation dat files 

dir_val = 'val_stress_all_comp'

fe_grab.fe_grab(ns_val, set_id_val, dir_val, wrt_file)
    
    
## Convert the orientations from the calibration datasets from bunge euler angles
## to GSH coefficients
gsh.euler_to_gsh(ns_cal,set_id_cal,wrt_file)


## Convert the orientations from the validation datasets from bunge euler angles
## to GSH coefficients
gsh.euler_to_gsh(ns_val,set_id_val,wrt_file)


## Generate the fftn of the calibration microstructure function
msf.micr_func(ns_cal,set_id_cal,wrt_file)
   
   
## Generate the fftn of the validation microstructure function
msf.micr_func(ns_val,set_id_val,wrt_file)
   
   
## Perform the calibration
for comp in xrange(6):
    calibration.calibration_procedure(ns_cal,set_id_cal,comp,wrt_file)
   
   
## Perform the validation
for comp in xrange(6):
    validation.validation_procedure(ns_cal,ns_val,set_id_cal,set_id_val,comp,wrt_file)
    

results.results_all(ns_val, set_id_val, 'sigma')

