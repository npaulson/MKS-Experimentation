# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:45:46 2014

@author: nhpnp3
"""

import numpy as np
import functions as rr
import matlab.engine
import time


def euler_to_gsh(el, H, ns, set_id, step, wrt_file):

    start = time.time()

    euler = np.load('euler_%s%s_s%s.npy' % (ns, set_id, step))

    euler_GSH = np.zeros([ns, H, el**3], dtype='complex128')

    # start the matlab engine
    eng = matlab.engine.start_matlab()

    for sn in range(ns):

        if sn == 0:
            print matlab.double(list(euler[sn, 0, 0:10]))

        # call the desired GSH function in matlab
        tmp = eng.gsh_hex_tri_L0_4(matlab.double(list(euler[sn, 0, :])),
                                   matlab.double(list(euler[sn, 1, :])),
                                   matlab.double(list(euler[sn, 2, :])))

        # convert the result back to a numpy array and store
        euler_GSH[sn, :, :] = np.array(tmp)

        del tmp

        print sn

    # stop the matlab engine
    eng.quit()

    np.save('euler_GSH_%s%s_s%s.npy' % (ns, set_id, step), euler_GSH)

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "Conversion from Euler angles to GSH coefficients completed:" +\
          "%s seconds" % timeE
    rr.WP(msg, wrt_file)


if __name__ == "__main__":
    st = time.time()
    euler_to_gsh(21, 15, 97, 'val_basal', 1, 'test.txt')
    print "elapsed time: %s" % (time.time() - st)
