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
import h5py


def calibration_procedure(el, H, ns, set_id, step, comp, typ, wrt_file):

    st = time.time()

    f = h5py.File("D_%s%s_s%s.hdf5" % (ns, set_id, step), 'r')
    r_fft = f.get('rfft%s_%s' % (comp, typ))[...]
    M = f.get('M')[...]
    f.close()

    specinfc = np.zeros((H, el**3), dtype='complex64')

    # here we perform the calibration for the scalar FIP

    specinfc[:, 0] = rr.calib(0, M, r_fft, 0, H, el, ns)
    [specinfc[:, 1], p] = rr.calib(1, M, r_fft, 0, H, el, ns)

    # calib_red is simply calib with some default arguments
    calib_red = partial(rr.calib, M=M, r_fft=r_fft,
                        p=p, H=H, el=el, ns=ns)

    specinfc[:, 2:(el**3)] = np.asarray(map(calib_red, range(2, el**3))).swapaxes(0, 1)

    f = h5py.File("infl_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    f.create_dataset('infl%s_%s' % (comp, typ), data=specinfc)
    f.close()

    msg = 'Calibration, component %s: %s seconds' % \
          (comp, np.round((time.time() - st), 3))
    rr.WP(msg, wrt_file)
