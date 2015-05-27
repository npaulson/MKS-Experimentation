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
import functions as rr
import tables as tb
import numpy as np


ns_cal = 100
set_id_cal = 'cal'
dir_cal = 'cal_alt'

ns_val = 398
set_id_val = 'val'
dir_val = 'val_alt'

el = 21
H = 90
comp = '11'

step = 5

wrt_file = 'log_step%s_%s.txt' % (step, time.strftime("%Y-%m-%d_h%Hm%M"))

# create HDF5 file
base = tb.open_file("ref_%s%s_s%s.h5" % (ns_cal, set_id_cal, step),
                    mode="w",
                    title="data for set %s%s"
                    % (ns_cal, set_id_cal))
# create a group one level below root called msf
base.create_group("/", 'msf', 'euler angles')
base.create_group("/", 'epsilon_t', 'total strain')
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
# close the HDF5 file
base.close()

"""
The tensorID determines the type of tensor data read from the .vtk file
if tensorID == 0, we read the stress tensor
if tensorID == 1, we read the strain tensor
if tensorID == 2, we read the plastic strain tensor
"""

# Gather data from calibration vtk files
vtk.read_euler(el, ns_cal, set_id_cal, step, dir_cal, wrt_file, 1)

tensor_ID = 1
vtk.read_meas(el, ns_cal, set_id_cal, step, comp, tensor_ID,
              dir_cal, wrt_file)

# Gather data from validation vtk files
vtk.read_euler(el, ns_val, set_id_val, step, dir_val, wrt_file, 1)

tensor_ID = 1
vtk.read_meas(el, ns_val, set_id_val, step, comp, tensor_ID, dir_val, wrt_file)

res_file = 'results_step%s_%s.txt' % (step, time.strftime("%Y-%m-%d_h%Hm%M"))
res_file2 = 'resultsComputer_step%s_%s.txt' % (step, time.strftime("%Y-%m-%d_h%Hm%M"))

for ii in xrange(14, 15):

    # create HDF5 file
    base = tb.open_file("gsh_try_%s%s_s%s.h5" % (ns_cal, set_id_cal, step),
                        mode="w",
                        title="data for set %s%s"
                        % (ns_val, set_id_val))
    # create a group one level below root called data
    base.create_group("/", 'msf', 'microstructure functions')
    base.create_group("/", 'epsilon_t', 'FFT of total strain')
    # close the HDF5 file
    base.close()

    # create HDF5 file
    base = tb.open_file("gsh_try_%s%s_s%s.h5" % (ns_val, set_id_val, step),
                        mode="w",
                        title="data for set %s%s"
                        % (ns_val, set_id_val))
    # create a group one level below root called data
    base.create_group("/", 'msf', 'microstructure functions')
    base.create_group("/", 'epsilon_t', 'FFT of total strain')
    # close the HDF5 file
    base.close()

    Hset_ = np.array(range(15))
    # Hset_ = np.hstack([np.array(range(15)), 15, 19, 23, 25, 48, 56, 60, 64, 68, 69])

    if ii == 14:
        Hset = Hset_
        msg = "coefficients L=0-4"
        rr.WP(msg, wrt_file)
        rr.WP(msg, res_file)
        print(Hset)
    else:
        Hset = np.hstack([Hset_, ii])
        msg = "coefficients L=0-4 and coeff %s" % ii
        rr.WP(msg, wrt_file)
        rr.WP(msg, res_file)
        print(Hset)

    # Convert the orientations from the calibration datasets from bunge euler
    # angles to GSH coefficients
    gsh.euler_to_gsh(el, Hset, ns_cal, set_id_cal, step, wrt_file)

    # Convert the orientations from the validation datasets from bunge euler
    # angles to GSH coefficients
    gsh.euler_to_gsh(el, Hset, ns_val, set_id_val, step, wrt_file)

    # Perform the calibration
    calibration.calibration_procedure(el, Hset.size, ns_cal, set_id_cal, step,
                                      comp, 'epsilon_t', wrt_file)

    # Perform the validation
    validation.validation(el, Hset.size, ns_cal, ns_val, set_id_cal,
                          set_id_val, step, comp, 'epsilon_t', wrt_file)

    results.results(el, ns_val, set_id_val, step, 'epsilon', comp, 't',
                    ii, res_file, res_file2)
