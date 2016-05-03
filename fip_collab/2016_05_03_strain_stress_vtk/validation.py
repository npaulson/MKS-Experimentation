# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script predicts the FE response of a set of microstructures designated by
a specific set-ID using a previously calibrated MKS

@author: nhpnp3
"""

import time
import h5py
import numpy as np
import functions as rr


def validation(el, H, ns_cal, ns_val, set_id_cal, set_id_val, step, comp, typ,
               wrt_file):

    start = time.time()

    f = h5py.File("coef.hdf5", 'r')
    dset_name = 'coef%s_%s%s_s%s' % (comp, ns_cal, set_id_cal, step)
    coef = f.get(dset_name)[...].reshape(H, el, el, el)
    f.close()

    f = h5py.File("data.hdf5", 'a')
    dset_name = 'M_%s%s_s%s' % (ns_val, set_id_val, step)
    M = f.get(dset_name)[...]

    tmp = np.sum(np.conjugate(coef) * M, 1)
    mks_R = np.fft.ifftn(tmp, [el, el, el], [1, 2, 3]).real

    dset_name = '%s%s_mks_%s%s_s%s' % (typ, comp, ns_val, set_id_val, step)
    f.create_dataset(dset_name, data=mks_R)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'validation performed for component %s: %s seconds' % (comp, timeE)
    rr.WP(msg, wrt_file)
