import functions as rr
import numpy as np
from constants import const
import time
import h5py


def neighbors(ns, set_id):

    st = time.time()

    C = const()

    f = h5py.File("spatial.hdf5", 'a')
    mf = f.get('mf_%s' % set_id)[...]
    mf = mf.swapaxes(1, 2)
    mf = mf.reshape((ns, C['el'], C['el'], C['el'], C['H']))

    exth = np.floor(0.5*C['ext'])
    cvec = np.arange(C['cmax'])
    cmat = np.unravel_index(cvec, (C['ext'], C['ext'], C['ext']))
    cmat = np.array(cmat).T

    neig = np.zeros((ns, C['el'], C['el'], C['el'], C['H'], C['cmax']),
                    dtype='int16')

    for cc in cvec:
        ii, jj, kk = cmat[cc, :]
        inx = np.int16(ii - exth)
        iny = np.int16(jj - exth)
        inz = np.int16(kk - exth)

        tmp = np.roll(mf, inx, 1)
        tmp = np.roll(tmp, iny, 2)
        tmp = np.roll(tmp, inz, 3)

        neig[..., cc] = tmp

    neig = neig.reshape((ns, C['el']**3, C['H'], C['cmax']))
    neig = f.create_dataset('neig_%s' % set_id, data=neig)

    f.close()

    timeE = np.round(time.time()-st, 5)
    msg = "neighbors found for %s: %ss" % (set_id, timeE)
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    ns = 10
    set_id = 'random'

    neighbors(ns, set_id)
