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
dir_cal = 'cal'

ns_val = 398
set_id_val = 'val'
dir_val = 'val'

el = 21

comp = '11'

step = 5

wrt_file = 'log_step%s_%s.txt' % (step, time.strftime("%Y-%m-%d_h%Hm%M"))

# # create HDF5 file
# base = tb.open_file("ref_%s%s_s%s.h5" % (ns_cal, set_id_cal, step),
#                     mode="w",
#                     title="data for set %s%s"
#                     % (ns_cal, set_id_cal))
# # create a group one level below root called msf
# base.create_group("/", 'msf', 'euler angles')
# base.create_group("/", 'epsilon_t', 'total strain')
# # close the HDF5 file
# base.close()

# # create HDF5 file
# base = tb.open_file("ref_%s%s_s%s.h5" % (ns_val, set_id_val, step),
#                     mode="w",
#                     title="data for set %s%s"
#                     % (ns_val, set_id_val))
# # create a group one level below root called data
# base.create_group("/", 'msf', 'euler angles')
# base.create_group("/", 'epsilon_t', 'total strain')
# # close the HDF5 file
# base.close()

# """
# The tensorID determines the type of tensor data read from the .vtk file
# if tensorID == 0, we read the stress tensor
# if tensorID == 1, we read the strain tensor
# if tensorID == 2, we read the plastic strain tensor
# """

# # Gather data from calibration vtk files
# vtk.read_euler(el, ns_cal, set_id_cal, step, dir_cal, wrt_file, 1)

# tensor_ID = 1
# vtk.read_meas(el, ns_cal, set_id_cal, step, comp, tensor_ID,
#               dir_cal, wrt_file)

# # Gather data from validation vtk files
# vtk.read_euler(el, ns_val, set_id_val, step, dir_val, wrt_file, 1)

# tensor_ID = 1
# vtk.read_meas(el, ns_val, set_id_val, step, comp, tensor_ID, dir_val, wrt_file)

res_file = 'results_step%s_%s.txt' % (step, time.strftime("%Y-%m-%d_h%Hm%M"))
res_file2 = 'resultsComputer_step%s_%s.txt' % (step, time.strftime("%Y-%m-%d_h%Hm%M"))

# for L=6
# pair_l = [np.array([0]), np.array([1, 5]), np.array([2, 4]),
#           np.array([3]), np.array([6, 14]), np.array([7, 13]),
#           np.array([8, 12]), np.array([9, 11]), np.array([10]),
#           np.array([15, 39]), np.array([16, 40]), np.array([17, 37]),
#           np.array([18, 38]), np.array([19, 35]), np.array([20, 36]),
#           np.array([21, 33]), np.array([22, 34]), np.array([23, 31]),
#           np.array([24, 32]), np.array([25, 29]), np.array([26, 30]),
#           np.array([27]), np.array([28])]

# term removal for L=6
# pair_l = [np.array([0]), np.array([1, 5]), np.array([2, 4]),
#           np.array([3]), np.array([6, 14]), np.array([7, 13]),
#           np.array([8, 12]), np.array([9, 11]), np.array([10]),
#           np.array([15, 39]), np.array([19, 35]), np.array([21, 33]),
#           np.array([23, 31])]

# for L=8
# pair_l = [np.array([0]), np.array([1, 5]), np.array([2, 4]),
#           np.array([3]), np.array([6, 14]), np.array([7, 13]),
#           np.array([8, 12]), np.array([9, 11]), np.array([10]),
#           np.array([15, 39]), np.array([16, 40]), np.array([17, 37]),
#           np.array([18, 38]), np.array([19, 35]), np.array([20, 36]),
#           np.array([21, 33]), np.array([22, 34]), np.array([23, 31]),
#           np.array([24, 32]), np.array([25, 29]), np.array([26, 30]),
#           np.array([27]), np.array([28]), np.array([41, 55]),
#           np.array([42, 54]), np.array([43, 53]), np.array([44, 52]),
#           np.array([45, 51]), np.array([46, 50]), np.array([47, 49]),
#           np.array([48]), np.array([56, 88]), np.array([57, 89]),
#           np.array([58, 86]), np.array([59, 87]), np.array([60, 84]),
#           np.array([61, 85]), np.array([62, 82]), np.array([63, 83]),
#           np.array([64, 80]), np.array([65, 81]), np.array([66, 78]),
#           np.array([67, 79]), np.array([68, 76]), np.array([69, 77]),
#           np.array([70, 74]), np.array([71, 75]), np.array([72]),
#           np.array([73])]

# term removal for L=8
pair_l = [np.array([0]), np.array([1, 5]), np.array([2, 4]),
          np.array([3]), np.array([6, 14]), np.array([7, 13]),
          np.array([8, 12]), np.array([9, 11]), np.array([10]),
          np.array([15, 39]), np.array([16, 40]),
          np.array([23, 31]),
          np.array([27]), np.array([28]),
          np.array([48]), np.array([56, 88]), np.array([71, 75]),
          np.array([72]),
          np.array([73])]

# for ii in xrange(15, len(pair_l)):
for ii in xrange(0, 1):

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

    if pair_l[ii][0] == 0:
        Hset = np.sort(np.hstack(pair_l))
        msg = "full set of coefficients used"
        rr.WP(msg, wrt_file)
        rr.WP(msg, res_file)
        print(Hset)
    elif ii == len(pair_l)-1:
        Hset = np.sort(np.int8(np.hstack(pair_l[:ii])))
        msg = 'GSH components removed: %s' % pair_l[ii]
        rr.WP(msg, wrt_file)
        rr.WP(msg, res_file)
        print(Hset)
    else:
        pt1 = np.hstack(pair_l[:ii])
        pt2 = np.hstack(pair_l[(ii+1):])
        tmp = np.hstack([pt1, pt2])
        Hset = np.sort(np.int8(tmp))
        msg = 'GSH components removed: %s' % pair_l[ii]
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
