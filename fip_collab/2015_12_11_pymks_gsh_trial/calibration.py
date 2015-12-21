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


def calibration_procedure(M, y_fft, el, H, ns, wrt_file):

    st = time.time()

    specinfc = np.zeros((el**3, H), dtype='complex64')

    # here we perform the calibration for the scalar FIP

    specinfc[0, :] = rr.calib(0, M, y_fft, 0, H, el, ns)
    [specinfc[1, :], p] = rr.calib(1, M, y_fft, 0, H, el, ns)

    # calib_red is simply calib with some default arguments
    calib_red = partial(rr.calib, M=M, y_fft=y_fft,
                        p=p, H=H, el=el, ns=ns)

    specinfc[2:(el**3), :] = np.asarray(map(calib_red, range(2, el**3)))

    msg = 'Calibration, component 11: %s seconds' % \
          np.round((time.time() - st), 3)
    rr.WP(msg, wrt_file)

    return specinfc.reshape(el, el, el, H)