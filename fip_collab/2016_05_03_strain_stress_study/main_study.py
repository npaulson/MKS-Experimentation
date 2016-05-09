# -*- coding: utf-8 -*-

import time
import vtk_read as vtk_r
import euler_to_gsh as gsh
import microstructure_function as msf
import strain2stress as s2s
import vtk_write as vtk_w
import validation
import h5py


ns_cal = 400
set_id_cal = 'cal'
dir_cal = 'cal'

ns_val_list = [500, 500, 500, 500]
set_id_val_list = ['val_actual', 'val_random', 'val_basaltrans', 'val_trans']
dir_val_list = ['actual', 'random', 'basaltrans', 'trans']

# ns_val_list = [400]
# set_id_val_list = ['val_actual']
# dir_val_list = ['actual']

comp_app = '11'
loading = 'Xdir'

H = 15
el = 21

compl = ['11', '22', '33', '23', '12', '13']
# compl = ['11']

f = h5py.File("data.hdf5", 'w')
f.close()

for step in xrange(1, 3):

    wrt_file = 'log_step%s_case%s_%s.txt' % (step,
                                             set_id_cal,
                                             time.strftime("%Y-%m-%d_h%Hm%M"))

    for case in xrange(len(ns_val_list)):

        ns_val = ns_val_list[case]
        set_id_val = set_id_val_list[case]
        dir_val = dir_val_list[case]

        """read grain IDs from the VTK files"""
        vtk_r.read_scalar(el, ns_val, set_id_val, step, dir_val, wrt_file)

        """Gather data from validation vtk files"""
        vtk_r.read_euler(el, ns_val, set_id_val, step, dir_val, wrt_file, 0)

        """Convert the orientations from the validation datasets from bunge euler
        angles to GSH coefficients"""
        gsh.euler_to_gsh(el, H, ns_val, set_id_val, step, wrt_file)

        """Generate the fftn of the validation microstructure function"""
        msf.micr_func(el, H, ns_val, set_id_val, step, wrt_file)

        """Perform the validation"""
        for comp in compl:
            validation.validation(el, H, ns_cal, ns_val, set_id_cal,
                                  set_id_val, step, comp, 'epsilon', wrt_file)

        """Convert strain to stress"""
        s2s.strain2stress(el, ns_val, set_id_val, step, wrt_file)

        """Write .vtk files"""
        newdir = 'vtk'
        vtk_w.vtk_write(el, ns_val, set_id_val, step, loading, newdir,
                        wrt_file)
