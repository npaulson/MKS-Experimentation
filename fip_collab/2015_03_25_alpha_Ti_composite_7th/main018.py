# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 16:46:35 2014

@author: nhpnp3
"""

import time
import fegrab
import microstructure_function as msf
import validation_viz
import results
import calibration
# import matplotlib.pyplot as plt

Hi = 2  # number of distinct local states in microstructure
order = 1  # choose 1, 2 or 7 local neighbors in MKS procedure

el_cal = 21  # number of elements per side of cube for calibration dataset
ns_cal = 399  # total number of samples in calibration dataset
set_id_cal = 'cal018'  # set ID for calibration dataset
dir_cal = 'cal018'  # directory name for .dat files

el_val = 21  # number of elements per side of cube for validation dataset
ns_val = 400  # total number of samples in validation dataset
set_id_val = 'val018'  # set ID for validation dataset
dir_val = 'val018'  # directory name for .dat files

doplt = 0  # if plotting of results desired set doplt = 1

# if doplt == 1:
#     plt.close('all')

wrt_file = 'log_order%s_%s%s_%s%s_%s.txt' % \
    (order, ns_cal, set_id_cal, ns_val, set_id_val,
        time.strftime("%Y-%m-%d_h%Hm%M"))

# TOTAL CALIBRATION PROCEDURE

# Read the calibration microstructures and build the microstructure function
H = msf.msf(el_cal, ns_cal, Hi, order, set_id_cal, wrt_file)

# Read the responses from the FE .dat files and perform the fftn for the
# calibration
fegrab.fegrab(el_cal, ns_cal, set_id_cal, dir_cal, wrt_file)

# Perform the calibration
calibration.calibration_main(el_cal, ns_cal, H, set_id_cal, wrt_file)

# # TOTAL VALIDATION PROCEDURE

# Read the validation microstructures and build the microstructure function
H = msf.msf(el_val, ns_val, Hi, order, set_id_val, wrt_file)

# Read the responses from the FE .dat files and perform the fftn for the
# validation
fegrab.fegrab(el_val, ns_val, set_id_val, dir_val, wrt_file)

# Perform the validation
validation_viz.validation_zero_pad(el_cal, el_val, ns_cal, ns_val, H,
                                   set_id_cal, set_id_val, wrt_file)

# Calculate the results of the validation
results.results(el_val, ns_val, set_id_val, 'epsilon', doplt, wrt_file)
