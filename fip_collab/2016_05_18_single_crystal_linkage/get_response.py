import numpy as np
import functions as rr
from constants import const
import h5py
import time


def read(ns, set_id):

    start = time.time()

    C = const()

    f = h5py.File('data_%s.hdf5' % set_id, 'r')
    modulus = f.get('data')[:, 3]
    strength = f.get('data')[:, 4]

    f = h5py.File("responses.hdf5", 'a')

    dset_name = 'modulus_%s' % set_id
    f.create_dataset(dset_name, data=modulus)

    dset_name = 'strength_%s' % set_id
    f.create_dataset(dset_name, data=strength)

    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'responses read for %s: %s seconds' \
          % (set_id, timeE)
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    C = const()
    ns = C['ns_cal'][0]
    set_id = C['set_id_cal'][0]

    read(ns, set_id)
