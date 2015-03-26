# -*- coding: utf-8 -*-
"""
Created on 2/19/2015 by Noah Paulson
"""

import vtk_read as vtk_r
# import all_hist as hst

ns_val_list = [390, 22, 44, 399]
set_id_val_list = ['actual', 'basaltrans', 'trans', 'random']
dir_val_list = ['actual', 'basaltrans', 'trans', 'random']

el = 21
step = 1
comp = '22'

for case in xrange(4):

    ns_val = ns_val_list[case]
    set_id_val = set_id_val_list[case]
    dir_val = dir_val_list[case]

    # The tensorID determines the type of tensor data read from the .vtk
    # file
    # if tensorID == 0, we read the stress tensor
    # if tensorID == 1, we read the strain tensor
    # if tensorID == 2, we read the plastic strain tensor

    tensor_ID = 0
    typ = 'sigma'

    vtk_r.read_meas(el, ns_val, set_id_val, step, typ, comp, tensor_ID,
                    dir_val)

    tensor_ID = 1
    typ = 'epsilon'

    vtk_r.read_meas(el, ns_val, set_id_val, step, typ, comp, tensor_ID,
                    dir_val)

# hst.make_hist(el, ns_val_list, set_id_val_list, step, comp, 'epsilon')
# hst.make_hist(el, ns_val_list, set_id_val_list, step, comp, 'sigma')
