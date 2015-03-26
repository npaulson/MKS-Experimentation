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
import results
import tables as tb


ns_cal = 300
set_id_cal = 'cal'
dir_cal = 'cal'

ns_val = 100
set_id_val = 'val'
dir_val = 'val'

H = 56
el = 21

compl = ['11', '22', '33', '12', '13', '23']

for step in xrange(1, 2):

    wrt_file = 'log_step%s_%s.txt' % (step, time.strftime("%Y-%m-%d_h%Hm%M"))

    # # create HDF5 file
    # base = tb.open_file("ref_%s%s_s%s.h5" % (ns_cal, set_id_cal, step),
    #                     mode="w",
    #                     title="data for set %s%s"
    #                     % (ns_cal, set_id_cal))
    # # create a group one level below root called msf
    # group = base.create_group("/", 'msf', 'euler angles')
    # # close the HDF5 file
    # base.close()

    # # create HDF5 file
    # base = tb.open_file("D_%s%s_s%s.h5" % (ns_cal, set_id_cal, step),
    #                     mode="w",
    #                     title="data for set %s%s"
    #                     % (ns_cal, set_id_cal))
    # # create a group one level below root called msf
    # group = base.create_group("/", 'msf', 'microstructure functions')
    # # close the HDF5 file
    # base.close()

    # # create HDF5 file
    # base = tb.open_file("ref_%s%s_s%s.h5" % (ns_val, set_id_val, step),
    #                     mode="w",
    #                     title="data for set %s%s"
    #                     % (ns_val, set_id_val))
    # # create a group one level below root called data
    # group = base.create_group("/", 'msf', 'euler angles')
    # # close the HDF5 file
    # base.close()

    # # create HDF5 file
    # base = tb.open_file("D_%s%s_s%s.h5" % (ns_val, set_id_val, step),
    #                     mode="w",
    #                     title="data for set %s%s"
    #                     % (ns_val, set_id_val))
    # # create a group one level below root called data
    # group = base.create_group("/", 'msf', 'microstructure functions')
    # # close the HDF5 file
    # base.close()

    # # The tensorID determines the type of tensor data read from the .vtk file
    # # if tensorID == 0, we read the stress tensor
    # # if tensorID == 1, we read the strain tensor
    # # if tensorID == 2, we read the plastic strain tensor

    # tensor_ID = 1

    # # Gather data from calibration vtk files

    # vtk.read_euler(el, ns_cal, set_id_cal, step, dir_cal, wrt_file, 1)

    # for comp in compl:
    #     vtk.read_meas(el, ns_cal, set_id_cal, step, comp, tensor_ID, dir_cal,
    #                   wrt_file)

    # # Gather data from validation vtk files

    # vtk.read_euler(el, ns_val, set_id_val, step, dir_val, wrt_file, 1)

    # for comp in compl:
    #     vtk.read_meas(el, ns_val, set_id_val, step, comp, tensor_ID, dir_val,
    #                   wrt_file)

    # Convert the orientations from the calibration datasets from bunge euler
    # angles to GSH coefficients
    gsh.euler_to_gsh(el, H, ns_cal, set_id_cal, step, wrt_file)

    # Convert the orientations from the validation datasets from bunge euler
    # angles to GSH coefficients
    gsh.euler_to_gsh(el, H, ns_val, set_id_val, step, wrt_file)

    # Perform the calibration
    for comp in compl:
        calibration.calibration_procedure(el, H, ns_cal, set_id_cal, step,
                                          comp, wrt_file)

    # Perform the validation
    for comp in compl:
        validation.validation(el, H, ns_cal, ns_val, set_id_cal, set_id_val,
                              step, comp, wrt_file)

    comp_app = 0

    results.results_all(el, ns_val, set_id_val, step, 'epsilon', compl,
                        comp_app)
