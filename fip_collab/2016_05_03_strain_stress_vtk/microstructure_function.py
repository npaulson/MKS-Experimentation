# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script reads a set of microstructures designated by the set-ID and saves
the microstructure function in real and frequency space.

@author: nhpnp3
"""

import time
import numpy as np
import functions as rr
import h5py


def micr_func(el, H, ns, set_id, step, wrt_file):

    start = time.time()

    f = h5py.File("data.hdf5", 'a')
    dset_name = 'euler_GSH_%s%s_s%s.npy' % (ns, set_id, step)
    tmp = f.get(dset_name)[...]

#    tmp = np.swapaxes(np.swapaxes(tmp,0,2),0,1)
    micr = tmp.reshape([ns, H, el, el, el])

    del tmp

    end = time.time()
    timeE = np.round((end - start), 3)
    msg = "generate real-space microstructure function from GSH-coefficients:"\
          " %s seconds" % timeE
    rr.WP(msg, wrt_file)

    # Microstructure functions in frequency space
    start = time.time()

    M = np.fft.fftn(micr, axes=[2, 3, 4])
    del micr
    size = M.nbytes

    dset_name = 'M_%s%s_s%s' % (ns, set_id, step)
    f.create_dataset(dset_name, data=M)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "FFT3 conversion of micr to M_%s%s_s%s: %s seconds" % (ns, set_id,
                                                                 step, timeE)
    rr.WP(msg, wrt_file)
    msg = 'Size of M_%s%s_s%s: %s bytes' % (ns, set_id, step, size)
    rr.WP(msg, wrt_file)
