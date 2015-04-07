# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 16:46:35 2014

@author: nhpnp3
"""

import vtk_read as vtk
import time
import euler_to_gsh as gsh
import calibration
import validation
import field_blur
import results
import tables as tb


ns_cal = 100
set_id_cal = 'cal'
dir_cal = 'cal'

ns_val = 398
set_id_val = 'val'
dir_val = 'val'

L = 7
H = 56
el = 21

compl = ['11', '22', '33', '12', '13', '23']

for step in xrange(5, 6):

    wrt_file = 'log_step%s_%s.txt' % (step, time.strftime("%Y-%m-%d_h%Hm%M"))

    # create HDF5 file
    base = tb.open_file("ref_%s%s_s%s.h5" % (ns_cal, set_id_cal, step),
                        mode="w",
                        title="data for set %s%s"
                        % (ns_cal, set_id_cal))
    # create a group one level below root called msf
    base.create_group("/", 'msf', 'euler angles')
    base.create_group("/", 'epsilon_t', 'total strain')
    base.create_group("/", 'epsilon_p', 'plastic strain')
    # close the HDF5 file
    base.close()

    # create HDF5 file
    base = tb.open_file("D_%s%s_s%s.h5" % (ns_cal, set_id_cal, step),
                        mode="w",
                        title="data for set %s%s"
                        % (ns_cal, set_id_cal))
    # create a group one level below root called msf
    base.create_group("/", 'msf', 'microstructure functions')
    base.create_group("/", 'epsilon_t', 'FFT of total strain')
    base.create_group("/", 'epsilon_p', 'FFT of plastic strain')
    # close the HDF5 file
    base.close()

    # create HDF5 file
    base = tb.open_file("ref_%s%s_s%s.h5" % (ns_val, set_id_val, step),
                        mode="w",
                        title="data for set %s%s"
                        % (ns_val, set_id_val))
    # create a group one level below root called data
    base.create_group("/", 'msf', 'euler angles')
    base.create_group("/", 'epsilon_t', 'total strain')
    base.create_group("/", 'epsilon_p', 'plastic strain')
    group = base.create_group("/", 'epsilon_p_b', 'blurred response')
    # close the HDF5 file
    base.close()

    # create HDF5 file
    base = tb.open_file("D_%s%s_s%s.h5" % (ns_val, set_id_val, step),
                        mode="w",
                        title="data for set %s%s"
                        % (ns_val, set_id_val))
    # create a group one level below root called data
    base.create_group("/", 'msf', 'microstructure functions')
    base.create_group("/", 'epsilon_t', 'FFT of total strain')
    base.create_group("/", 'epsilon_p', 'FFT of plastic strain')
    # close the HDF5 file
    base.close()

    # The tensorID determines the type of tensor data read from the .vtk file
    # if tensorID == 0, we read the stress tensor
    # if tensorID == 1, we read the strain tensor
    # if tensorID == 2, we read the plastic strain tensor

    # Gather data from calibration vtk files
    vtk.read_euler(el, ns_cal, set_id_cal, step, dir_cal, wrt_file, 1)

    tensor_ID = 1

    for comp in compl:
        vtk.read_meas(el, ns_cal, set_id_cal, step, comp, tensor_ID,
                      dir_cal, wrt_file)

    # Gather data from validation vtk files
    vtk.read_euler(el, ns_val, set_id_val, step, dir_val, wrt_file, 1)

    tensor_ID = 1
    for comp in compl:
        vtk.read_meas(el, ns_val, set_id_val, step, comp, tensor_ID,
                      dir_val, wrt_file)

    tensor_ID = 2
    for comp in compl:
        vtk.read_meas(el, ns_val, set_id_val, step, comp, tensor_ID,
                      dir_val, wrt_file)

    # Convert the orientations from the calibration datasets from bunge euler
    # angles to GSH coefficients
    gsh.euler_to_gsh(el, H, ns_cal, set_id_cal, step, wrt_file)

    # Convert the orientations from the validation datasets from bunge euler
    # angles to GSH coefficients
    gsh.euler_to_gsh(el, H, ns_val, set_id_val, step, wrt_file)

    # Perform the calibration
    tensor_ID = 1
    for comp in compl:
        calibration.calibration_procedure(el, H, ns_cal, set_id_cal, step,
                                          comp, 'epsilon_t', wrt_file)

    # Perform the validation
    for comp in compl:
        validation.validation(el, H, ns_cal, ns_val, set_id_cal, set_id_val,
                              step, comp, wrt_file)

    # Perform Blurring on Solutions
    for comp in compl:
        field_blur.blur(el, ns_val, set_id_val, step, 'epsilon_p', comp)

    comp_app = 0

    for comp in compl:
        results.results(el, ns_val, set_id_val, step, L, 'epsilon', comp, 't')

    for comp in compl:
        results.results(el, ns_val, set_id_val, step, L, 'epsilon', comp, 'p')

    for comp in compl:
        results.results(el, ns_val, set_id_val, step, L, 'epsilon', comp, 'p_b')
