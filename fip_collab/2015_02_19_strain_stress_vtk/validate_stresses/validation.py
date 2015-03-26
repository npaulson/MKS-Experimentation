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


def validation(el, H, ns_cal, ns_val, set_id_cal, set_id_val, step, comp, typ,
               wrt_file):

    start = time.time()

    # perform the prediction procedure
    specinfc = np.load('specinfc%s_%s%s_s%s.npy'
                       % (comp, ns_cal, set_id_cal, step)).reshape(H, el, el,
                                                                   el)

    M = np.load('M_%s%s_s%s.npy' % (ns_val, set_id_val, step))
    tmp = np.sum(np.conjugate(specinfc) * M, 1)
    mks_R = np.fft.ifftn(tmp, [el, el, el], [1, 2, 3]).real

    np.save('%s%s_mks_%s%s_s%s' % (typ, comp, ns_val, set_id_val, step), mks_R)

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'validation performed for component %s: %s seconds' % (comp, timeE)
    rr.WP(msg, wrt_file)
