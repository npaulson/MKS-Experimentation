# -*- coding: utf-8 -*-

import time
import numpy as np
import h5py
import functions as rr
from functools import partial


def calibration_procedure(el, H, ns, set_id, step, comp, typ, wrt_file):

    f = h5py.File("data.hdf5", 'r')
    dset_name = 'M_%s%s_s%s' % (ns, set_id, step)
    M = f.get(dset_name)[...]
    dset_name = '%s%s_fft_fem_%s%s_s%s' % (typ, comp, ns, set_id, step)
    r_fft = f.get(dset_name)[...]
    f.close()

    start = time.time()

    coef = np.zeros((H, el**3), dtype='complex64')

    # here we perform the calibration for the scalar FIP

    coef[:, 0] = rr.calib(0, M, r_fft, 0, H, el, ns)
    [coef[:, 1], p] = rr.calib(1, M, r_fft, 0, H, el, ns)

    # calib_red is simply calib with some default arguments
    calib_red = partial(rr.calib, M=M, r_fft=r_fft, p=p, H=H, el=el, ns=ns)

    coef[:, 2:(el**3)] = np.asarray(map(calib_red,
                                    range(2, el**3))).swapaxes(0, 1)

    f = h5py.File("coef.hdf5", 'a')
    dset_name = 'coef%s_%s%s_s%s' % (comp, ns, set_id, step)
    f.create_dataset(dset_name, data=coef)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)
    msg = 'Calibration, component %s: %s seconds' % (comp, timeE)
    rr.WP(msg, wrt_file)
