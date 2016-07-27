# -*- coding: utf-8 -*-
import functions as rr
import numpy as np
from constants import const
import time
import h5py


def collect():

    st = time.time()

    C = const()

    f_master = h5py.File('euler_L%s.hdf5' % C['H'], 'a')

    """load the microstructures"""
    for set_id in C['set_id']:
        f = h5py.File('euler_%s.hdf5' % set_id, 'r')
        euler = f.get('euler')[...]
        f.close()
        f_master.create_dataset('euler_%s' % set_id, data=euler)

    f_master.close()

    msg = 'euler sets collected: %s seconds' \
          % np.round(time.time()-st)
    rr.WP(msg, C['wrt_file'])
