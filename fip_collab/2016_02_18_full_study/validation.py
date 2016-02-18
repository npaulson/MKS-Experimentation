# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script predicts the FE response of a set of microstructures designated by
a specific set-ID using a previously calibrated MKS

@author: nhpnp3
"""

import time
import numpy as np
import functions as rr
import h5py


def validation(el, H, ns_cal, ns_val, set_id_cal, set_id_val, step, comp,
               typ, wrt_file):

    start = time.time()

    f = h5py.File("infl_%s%s_s%s.hdf5" % (ns_cal, set_id_cal, step), 'a')
    infl_coef = f.get('infl_coef')[...].reshape(H, el, el, el)
    f.close()

    f = h5py.File("D_%s%s_s%s.hdf5" % (ns_val, set_id_val, step), 'r')
    M = f.get('M')[...]
    f.close()

    # perform the validation calculations
    tmp = np.sum(np.conjugate(infl_coef) * M, 1)
    r_mks = np.fft.ifftn(tmp, [el, el, el], [1, 2, 3]).real

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns_val, set_id_val, step), 'a')
    f.create_dataset('rmks%s_%s' %(comp, typ), data=r_mks)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'validation performed for component %s: %s seconds' % (comp, timeE)
    rr.WP(msg, wrt_file)
