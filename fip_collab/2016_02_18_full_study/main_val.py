# -*- coding: utf-8 -*-
"""
"""

import vtk_read as vtk
import time
import validation
import field_blur
import euler_to_gsh as gsh
import results_text as rtex
import get_fips as fip
import fip_sort as fs
import h5py
import numpy as np


ns_cal = 300
set_id_cal = 'cal'
dir_cal = 'cal'

ns_val = 100
set_id_val = 'val'
dir_val = 'val'

typ = 'epsilon_t'
nfac = 0.00747

L = 4
H = 15
el = 21

compl = ['11', '22', '33', '12', '13', '23']
# compl = ['11']

for step in xrange(5, 6):

    wrt_file = 'log_step%s_%s.txt' % (step, time.strftime("%Y-%m-%d_h%Hm%M"))

    """
    The tensorID determines the type of tensor data read from the .vtk file
    if tensorID == 0, we read the stress tensor
    if tensorID == 1, we read the strain tensor
    if tensorID == 2, we read the plastic strain tensor
    """

    """Gather data from validation vtk files"""
    tensorID = 1

    vtk.read_euler(el, ns_val, set_id_val, step, dir_val, wrt_file, tensorID)

    for comp in compl:
        vtk.read_meas(el, ns_val, set_id_val, step, comp, tensorID,
                      dir_val, wrt_file)

    vtk.read_fip(el, ns_val, set_id_val, step, dir_val, wrt_file)

    """Convert the orientations from the calibration datasets from bunge euler
    angles to GSH coefficients"""
    gsh.euler_to_gsh(el, H, ns_val, set_id_val, step, wrt_file)

    """Perform the validation"""
    for comp in compl:
        validation.validation(el, H, ns_cal, ns_val, set_id_cal, set_id_val,
                              step, comp, typ, wrt_file)

    """Get error metrics for each total strain component"""
    newID = 'rmks'
    traID = 'r'
    for comp in compl:
        rtex.results(el, ns_val, set_id_val, step, typ, comp,
                     newID, traID, nfac)

    """Calculate FIP fields"""
    fipmat = np.zeros((ns_val, el**3))

    for sn in xrange(ns_val):
        fipmat[sn, :] = fip.fip(sn, el, ns_val, set_id_val, step, typ, compl)

    f = h5py.File("fip_%s%s_s%s.hdf5" % (ns_val, set_id_val, step), 'a')
    f.create_dataset('fipmks', data=fipmat)
    f.close()

    # """Perform Blurring on FIPs"""
    # parID = 'fip'
    # field_blur.blur(el, ns_val, set_id_val, step, parID)
    # fs.fip_sort(el, ns_val, set_id_val, step, parID)

    # parID = 'fipmks'
    # field_blur.blur(el, ns_val, set_id_val, step, parID)
    # fs.fip_sort(el, ns_val, set_id_val, step, parID)
