# -*- coding: utf-8 -*-
import functions as rr
import numpy as np
from constants import const
import time
import h5py


def collect():

    st = time.time()

    C = const()

    f_master = h5py.File('spatial_L%s.hdf5' % C['H'], 'a')

    """load the microstructures"""
    for set_id in C['set_id']:
        f = h5py.File('spatial_%s.hdf5' % set_id, 'r')
        ff = f.get('ff')[...]
        f.close()
        f_master.create_dataset('ff_%s' % set_id, data=ff)

    f_master.close()

    msg = 'correlation sets collected: %s seconds' \
          % np.round(time.time()-st)
    rr.WP(msg, C['wrt_file'])
