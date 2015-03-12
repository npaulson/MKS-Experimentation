# -*- coding: utf-8 -*-
"""
Created on 2/19/2015 by Noah Paulson
"""

import time
import vtk_read as vtk_r
import euler_to_gsh as gsh
import microstructure_function as msf
# import calibration
import validation
import strain2stress as s2s
# import results
import vtk_write as vtk_w


ns_cal = 399
set_id_cal = 'cal'
dir_cal = 'cal'

ns_val = 400
set_id_val = 'val_basaltrans'
dir_val = 'basaltrans'

H = 15
el = 21

compl = ['11', '22', '33', '12', '23', '31']

for step in xrange(1, 3):

    wrt_file = 'log_step%s_%s.txt' % (step, time.strftime("%Y-%m-%d_h%Hm%M"))

    # The tensorID determines the type of tensor data read from the .vtk file
    # if tensorID == 0, we read the stress tensor
    # if tensorID == 1, we read the strain tensor
    # if tensorID == 2, we read the plastic strain tensor

    tensor_ID = 1

    # # Gather data from calibration vtk files

    # vtk_r.read_euler(el, ns_cal, set_id_cal, step, dir_cal, wrt_file, 1)

    # for comp in compl:
    #     vtk_r.read_meas(el, ns_cal, set_id_cal, step, comp, tensor_ID, dir_cal,
    #                     wrt_file)

    # Gather data from validation vtk files

    vtk_r.read_euler(el, ns_val, set_id_val, step, dir_val, wrt_file, 1)

    # for comp in compl:
    #     vtk_r.read_meas(el, ns_val, set_id_val, step, comp, tensor_ID, dir_val,
    #                     wrt_file)

    # read grain IDs from the VTK files
    vtk_r.read_scalar(el, ns_val, set_id_val, step, dir_val, wrt_file)

    # # Convert the orientations from the calibration datasets from bunge euler
    # # angles to GSH coefficients
    # gsh.euler_to_gsh(el, H, ns_cal, set_id_cal, step, wrt_file)

    # Convert the orientations from the validation datasets from bunge euler
    # angles to GSH coefficients
    gsh.euler_to_gsh(el, H, ns_val, set_id_val, step, wrt_file)

    # # # Generate the fftn of the calibration microstructure function
    # # msf.micr_func(el, H, ns_cal, set_id_cal, step, wrt_file)

    # Generate the fftn of the validation microstructure function
    msf.micr_func(el, H, ns_val, set_id_val, step, wrt_file)

    # # Perform the calibration
    # for comp in compl:
    #     calibration.calibration_procedure(el, H, ns_cal, set_id_cal, step,
    #                                       comp, wrt_file)

    # Perform the validation
    for comp in compl:
        validation.validation(el, H, ns_cal, ns_val, set_id_cal, set_id_val,
                              step, comp, wrt_file)

    s2s.strain2stress(el, ns_val, set_id_val, step, wrt_file)

    # comp_app = 1

    # results.results_all(el, ns_val, set_id_val, step, 'epsilon', compl,
    #                     comp_app)

    newdir = 'vtk'

    vtk_w.vtk_write(el, ns_val, set_id_val, step, newdir, wrt_file)
