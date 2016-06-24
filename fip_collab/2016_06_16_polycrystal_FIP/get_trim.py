import functions as rr
import numpy as np
from constants import const
import time
import h5py


def trim(ns, set_id):

    st = time.time()

    C = const()

    f = h5py.File("spatial.hdf5", 'a')
    tmp = f.get("ff_raw_%s" % set_id)[...]
    f.close()

    rv = np.int64(np.floor(C['vmax']/2.))
    tmp = np.roll(tmp, rv, 3)
    tmp = np.roll(tmp, rv, 4)
    tmp = np.roll(tmp, rv, 5)
    tmp = tmp[..., :C['vmax'], :C['vmax'], :C['vmax']]
    tmp = np.fft.ifftshift(tmp, [3, 4, 5])

    f = h5py.File("spatial_trim.hdf5", 'a')
    f.create_dataset("ff_%s" % set_id, data=tmp)

    # ff = f_rd.create_dataset("ff_%s" % set_id,
    #                          (ns, C['H'], C['H'], C['vmax'], C['vmax'], C['vmax']),
    #                          dtype='float64')

    timeE = np.round(time.time()-st, 5)

    msg = "correlations trimmed for %s: %ss" % (set_id, timeE)
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    ns = 10
    set_id = 'random'

    trim(ns, set_id)
