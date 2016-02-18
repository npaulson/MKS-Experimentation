# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 16:46:35 2014

@author: nhpnp3
"""

import vtk_read as vtk
import time
import validation
# import field_blur
import euler_to_gsh as gsh
import results


ns_cal = 300
set_id_cal = 'cal'
dir_cal = 'cal'

ns_val = 100
set_id_val = 'val'
dir_val = 'val'

L = 4
H = 15
el = 21

compl = ['11', '22', '33', '12', '13', '23']
# compl = ['11']

for step in xrange(5, 6):

    wrt_file = 'log_step%s_%s.txt' % (step, time.strftime("%Y-%m-%d_h%Hm%M"))

    # The tensorID determines the type of tensor data read from the .vtk file
    # if tensorID == 0, we read the stress tensor
    # if tensorID == 1, we read the strain tensor
    # if tensorID == 2, we read the plastic strain tensor

    # Gather data from validation vtk files
    vtk.read_euler(el, ns_val, set_id_val, step, dir_val, wrt_file, 1)

    tensor_ID = 1
    for comp in compl:
        vtk.read_meas(el, ns_val, set_id_val, step, comp, tensor_ID,
                      dir_val, wrt_file)

    # Convert the orientations from the calibration datasets from bunge euler
    # angles to GSH coefficients
    gsh.euler_to_gsh(el, H, ns_val, set_id_val, step, wrt_file)

    # Perform the validation
    for comp in compl:
        validation.validation(el, H, ns_cal, ns_val, set_id_cal, set_id_val,
                              step, comp, 'epsilon_t', wrt_file)

    # # Perform Blurring on Solutions
    # for comp in compl:
    #     field_blur.blur(el, ns_val, set_id_val, step, 'epsilon_t', comp)

    comp_app = 0

    for comp in compl:
        results.results(el, ns_val, set_id_val, step, L, 'epsilon_t', comp)