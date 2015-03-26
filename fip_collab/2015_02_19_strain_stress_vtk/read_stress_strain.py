# -*- coding: utf-8 -*-
"""
Created on 2/19/2015 by Noah Paulson
"""

import time
import vtk_read as vtk_r
import all_hist as hst

ns_val_list = [22, 22, 22, 22]
set_id_val_list = ['actual', 'basaltrans', 'trans', 'random']
dir_val_list = ['actual', 'basaltrans', 'trans', 'random']

H = 15
el = 21

step = 1
comp = '11'

for case in xrange(4):

    ns_val = ns_val_list[case]
    set_id_val = set_id_val_list[case]
    dir_val = dir_val_list[case]

    wrt_file = 'log_step%s_case%s_%s.txt' % (step, set_id_val, time.strftime("%Y-%m-%d_h%Hm%M"))

    # The tensorID determines the type of tensor data read from the .vtk
    # file
    # if tensorID == 0, we read the stress tensor
    # if tensorID == 1, we read the strain tensor
    # if tensorID == 2, we read the plastic strain tensor

    tensor_ID = 0

    vtk_r.read_meas(el, ns_val, set_id_val, step, comp, tensor_ID, dir_val,
                    wrt_file)

    tensor_ID = 1

    vtk_r.read_meas(el, ns_val, set_id_val, step, comp, tensor_ID, dir_val,
                    wrt_file)

