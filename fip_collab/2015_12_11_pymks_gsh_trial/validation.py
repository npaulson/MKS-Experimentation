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
import tables as tb


def validation(M, infl_coef, el, wrt_file):

    start = time.time()

    # perform the validation calculations

    print M.shape
    print infl_coef.shape

    tmp = np.sum(np.conjugate(infl_coef) * M, 4)
    y_mks = np.fft.ifftn(tmp, [el, el, el], [1, 2, 3]).real

    print y_mks.shape

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'validation performed for component 11: %s seconds' % timeE
    rr.WP(msg, wrt_file)

    return y_mks
