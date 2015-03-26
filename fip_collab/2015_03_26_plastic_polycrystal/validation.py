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
               wrt_file):

    start = time.time()

    # open HDF5 file
    base = tb.open_file("infl_%s%s_s%s.h5" % (ns_cal, set_id_cal, step),
                        mode="r")
    infl = base.get_node('/', 'infl%s' % comp)
    infl_coef = infl.infl_coef[...].reshape(H, el, el, el)
    # close HDF5 file
    base.close()

    # open HDF5 file
    base = tb.open_file("D_%s%s_s%s.h5" % (ns_val, set_id_val, step),
                        mode="r")
    M = base.root.msf.M[...]
    # close HDF5 file
    base.close()

    # perform the validation calculations
    tmp = np.sum(np.conjugate(infl_coef) * M, 1)
    r_mks = np.fft.ifftn(tmp, [el, el, el], [1, 2, 3]).real

    # open HDF5 file
    base = tb.open_file("ref_%s%s_s%s.h5" % (ns_val, set_id_val, step),
                        mode="a")

    # save the MKS predicted total strain fields
    group = base.get_node('/epsilon', 'r%s' % comp)
    base.create_array(group, 'r_mks', r_mks)

    # find the node containing the fem total strain fields
    r_et = base.get_node('/epsilon', 'r%s' % comp)
    et_fem = r_et.r_fem[...]
    # find the node containing the fem plastic strain fields
    r_ep = base.get_node('/epsilon_p', 'r%s' % comp)
    ep_fem = r_ep.r_fem[...]

    # estimate the plastic strain predicted by fem as the mks predicted total
    # strain minus the FEM elastic strain field
    ep_mks = r_mks - (et_fem - ep_fem)

    del et_fem, ep_fem

    # save the estimated plastic strain from MKS to an array
    base.create_array(r_ep, 'r_mks', ep_mks)
    # close HDF5 file
    base.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'validation performed for component %s: %s seconds' % (comp, timeE)
    rr.WP(msg, wrt_file)
