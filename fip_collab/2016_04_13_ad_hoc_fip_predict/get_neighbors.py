import functions as rr
import numpy as np
import time
import h5py


def neighbors(el, ns, H, set_id, step, wrt_file):

    st = time.time()

    f = h5py.File("spatial.hdf5", 'a')
    mf = f.get('mf_%s' % set_id)[...]
    mf = mf.swapaxes(1, 2)
    mf = mf.reshape((ns, el, el, el, H))

    ext = 3
    exth = np.floor(0.5*ext)
    cmax = ext**3
    cvec = np.arange(cmax)
    cmat = np.unravel_index(cvec, (ext, ext, ext))
    cmat = np.array(cmat).T

    neig = np.zeros((ns, el, el, el, H, cmax), dtype='complex128')

    for cc in cvec:
        ii, jj, kk = cmat[cc, :]
        inx = np.int16(ii - exth)
        iny = np.int16(jj - exth)
        inz = np.int16(kk - exth)

        tmp = np.roll(mf, inx, 1)
        tmp = np.roll(tmp, iny, 2)
        tmp = np.roll(tmp, inz, 3)

        neig[..., cc] = tmp

    neig = neig.reshape((ns*el**3, H*cmax))
    neig = f.create_dataset('neig_%s' % set_id, data=neig)

    f.close()

    timeE = np.round(time.time()-st, 5)
    msg = "neighbors found for %s: %ss" % (set_id, timeE)
    rr.WP(msg, wrt_file)


if __name__ == '__main__':
    el = 21
    ns = 10
    H = 15
    set_id = 'random'
    step = 0
    wrt_file = 'test.txt'

    neighbors(el, ns, H, set_id, step, wrt_file)
