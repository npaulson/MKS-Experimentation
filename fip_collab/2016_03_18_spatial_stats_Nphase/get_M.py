import functions as rr
import numpy as np
import time
import h5py


def get_M(el, ns, H, set_id, step, wrt_file):

    st = time.time()

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    sves = f.get('sves')
    M = f.create_dataset('M', (ns, H, el, el, el), dtype='complex128')

    for h in xrange(H):
        micrf = sves[...] == h
        M[:, h, ...] = np.fft.fftn(micrf, axes=[1, 2, 3])

    msg = "M computed: %ss" % np.round(time.time()-st, 5)
    rr.WP(msg, wrt_file)


if __name__ == '__main__':
    el = 21
    ns = 10
    H = 5
    set_id = 'random'
    step = 0
    wrt_file = 'test.txt'

    get_M(el, ns, set_id, step, wrt_file)
