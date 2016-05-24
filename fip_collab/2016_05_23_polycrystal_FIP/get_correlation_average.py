import functions as rr
import numpy as np
from constants import const
import time
import h5py


def avg(ns, set_id):

    st = time.time()

    C = const()

    f = h5py.File("spatial.hdf5", 'a')

    tmp = f.get('ff_%s' % set_id)[...]

    ff_avg = np.mean(tmp, axis=0)

    f.create_dataset('ff_avg_%s' % set_id, data=ff_avg)

    f.close()

    timeE = np.round(time.time()-st, 5)

    msg = "correlations averaged for %s: %ss" % (set_id, timeE)
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    ns = 10
    set_id = 'random'

    avg(ns, set_id)
