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


def validation(el, H, ns_cal, ns_val, set_id_cal, set_id_val, step, comp,
               typ, wrt_file):

    start = time.time()

    # open HDF5 file
    base = tb.open_file("infl_%s%s_s%s.h5" % (ns_cal, set_id_cal, step),
                        mode="r")
    infl = base.get_node('/', 'infl%s' % comp)
    infl_coef = infl.infl_coef[...].reshape(H, el, el, el)
    # close HDF5 file
    base.close()

    # open HDF5 file
    base = tb.open_file("gsh_try_%s%s_s%s.h5" % (ns_val, set_id_val, step),
                        mode="a")
    M = base.root.msf.M[...]

    # perform the validation calculations
    tmp = np.sum(np.conjugate(infl_coef) * M, 1)
    r_mks = np.fft.ifftn(tmp, [el, el, el], [1, 2, 3]).real

    # create a group one level below root called r[comp]
    group = base.create_group('/%s' % typ,
                              'r%s' % comp,
                              'comp %s response fields' % comp)

    # save the MKS predicted total strain fields
    base.create_array(group, 'r_mks', r_mks)

    # close HDF5 file
    base.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'validation performed for component %s: %s seconds' % (comp, timeE)
    rr.WP(msg, wrt_file)
