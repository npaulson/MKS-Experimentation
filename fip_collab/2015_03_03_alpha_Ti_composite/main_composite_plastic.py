# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 16:46:35 2014

@author: nhpnp3
"""

import time
# import fegrab
# import microstructure_function as msf
# import validation_viz
import results
# import calibration
import fip
import matplotlib.pyplot as plt

plt.close('all')

Hi = 2
H = 2
order = 1

el_cal = 21
ns_cal = 399
set_id_cal = 'cal'
direc_cal = 'cal'

el_val = 21
ns_val = 400
set_id_val = 'val'
direc_val = 'val'


wrt_file = 'log_order%s_%s%s_%s%s_%s.txt' % \
    (order, ns_cal, set_id_cal, ns_val, set_id_val,
        time.strftime("%Y-%m-%d_h%Hm%M"))


# # TOTAL CALIBRATION PROCEDURE

# # Read the calibration microstructures and build the microstructure function
# msf.msf(el_cal, ns_cal, Hi, H, order, set_id_cal, wrt_file)

# # Read the responses from the FE .dat files and perform the fftn for the
# # calibration
# fegrab.fegrab(el_cal, ns_cal, set_id_cal, direc_cal, wrt_file)

# # Perform the calibration
# calibration.calibration_procedure(el_cal, ns_cal, H, set_id_cal, wrt_file)


# # TOTAL VALIDATION PROCEDURE

# # Read the validation microstructures and build the microstructure function
# msf.msf(el_val, ns_val, Hi, H, order, set_id_val, wrt_file)

# # Read the responses from the FE .dat files and perform the fftn for the
# # validation
# fegrab.fegrab(el_val, ns_val, set_id_val, direc_val, wrt_file)

# # Perform the validation
# validation_viz.validation_zero_pad(el_cal, el_val, ns_cal, ns_val, H,
#                                    set_id_cal, set_id_val, wrt_file)

# # Calculate the FIPs
# fip.fip_calc(el_val, ns_val, set_id_val, wrt_file)

# Calculate the results of the validation
results.results(el_val, ns_val, set_id_val, 'epsilon', wrt_file)
