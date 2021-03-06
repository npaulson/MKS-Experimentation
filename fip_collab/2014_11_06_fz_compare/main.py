# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 16:46:35 2014

@author: nhpnp3
"""

import time
import fegrab 
import microstructure_function as msf
import validation_viz
import results_field
import calibration
import matplotlib.pyplot as plt

plt.close('all')

H = 15

wrt_file = 'log_%s.txt' %(time.strftime("%Y-%m-%d_h%Hm%M"))


### TOTAL CALIBRATION PROCEDURE ###

el_cal = 21
ns_cal = 150
set_id_cal = 'phi2is0edgeV4'
set_id_abq = 'phi2is0edgeV4'


## Read the calibration microstructures and build the microstructure function
msf.msf(el_cal,ns_cal,H,set_id_cal,wrt_file)

## Read the responses from the FE .dat files and perform the fftn for the calibration
fegrab.fegrab(el_cal,ns_cal,set_id_cal,set_id_abq,wrt_file)

## Perform the calibration
calibration.calibration_procedure(el_cal,ns_cal,H,set_id_cal,wrt_file)


### TOTAL VALIDATION PROCEDURE ###

el_val = 21
ns_val = 50
set_id_val = 'val'

### Read the validation microstructures and build the microstructure function
#msf.msf(el_val,ns_val,H,set_id_val,wrt_file)
#
### Read the responses from the FE .dat files and perform the fftn for the validation
#fegrab.fegrab(el_val,ns_val,set_id_val,wrt_file)

## Perform the validation  
validation_viz.validation_zero_pad(el_cal,el_val,ns_cal,ns_val,H,set_id_cal,set_id_val,wrt_file)

## Calculate the results of the validation
results_field.results(el_val,ns_val,set_id_cal,set_id_val,'11','epsilon')
        