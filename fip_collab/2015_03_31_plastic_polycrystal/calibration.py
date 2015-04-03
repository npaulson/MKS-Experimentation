# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script performs the MKS calibration given the microstructure function
and the FIP response, both in frequency space.

@author: nhpnp3
"""

import time
import numpy as np
import functions as rr
from functools import partial
import tables as tb


def calibration_procedure(el, H, ns, set_id, step, comp, tensor_ID, wrt_file):

    st = time.time()

    typ = ['sigma', 'epsilon', 'epsilon_p']

    # open HDF5 file
    base = tb.open_file("D_%s%s_s%s.h5" % (ns, set_id, step), mode="r")
    # retrieve data from HDF5 file
    resp = base.get_node('/%s' % typ[tensor_ID], 'r%s' % comp)
    r_fft = resp.r_fft[...]
    M = base.root.msf.M[...]
    # close the HDF5 file
    base.close()

    specinfc = np.zeros((H, el**3), dtype='complex64')

    # here we perform the calibration for the scalar FIP

    specinfc[:, 0] = rr.calib(0, M, r_fft, 0, H, el, ns)
    [specinfc[:, 1], p] = rr.calib(1, M, r_fft, 0, H, el, ns)

    # calib_red is simply calib with some default arguments
    calib_red = partial(rr.calib, M=M, r_fft=r_fft,
                        p=p, H=H, el=el, ns=ns)

    specinfc[:, 2:(el**3)] = np.asarray(map(calib_red, range(2, el**3))).swapaxes(0, 1)

    # open HDF5 file
    base = tb.open_file("infl_%s%s_s%s.h5" % (ns, set_id, step), mode="a")
    # create a group one level below root called infl[comp]
    group = base.create_group('/',
                              'infl%s' % comp,
                              'influence function for component %s' % comp)
    base.create_array(group,
                      'infl_coef',
                      specinfc,
                      'array of influence coefficients')
    # close the HDF5 file
    base.close()

    msg = 'Calibration, component %s: %s seconds' % \
          (comp, np.round((time.time() - st), 3))
    rr.WP(msg, wrt_file)
