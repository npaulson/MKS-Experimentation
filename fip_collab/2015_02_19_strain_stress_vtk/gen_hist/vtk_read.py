# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 11:32:08 2014

@author: nhpnp3
"""

import functions as rr
import numpy as np
import os


def read_meas(el, ns, set_id, step, typ, comp, tensor_id, newdir):

#    nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    compd = {'11': 0, '22': 4, '33': 8, '12': 1, '23': 5, '31': 6}
    compp = compd[comp]

    r_real = np.zeros([ns, el, el, el])

    sn = 0
    for filename in os.listdir(nwd):
        if filename.endswith('.vtk'):
            r_temp = rr.read_vtk_tensor(filename=filename, tensor_id=tensor_id,
                                        comp=compp)
            r_real[sn, ...] = r_temp.reshape([el, el, el])
            sn += 1

    # return to the original directory
    os.chdir('..')

    np.save('%s%s_%s%s_s%s' % (typ, comp, ns, set_id, step), r_real)
