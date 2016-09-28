import functions as rr
import numpy as np
import time
import h5py


def get_M(el, ns, H, set_id, wrt_file):

    st = time.time()

    f = h5py.File("spatial_stats.hdf5", 'a')
    sves = f.get('sves_%s' % set_id)
    M = f.create_dataset('M_%s' % set_id,
                         (ns, H, el, el), dtype='complex128')

    for h in xrange(H):
        micrf = sves[...] == h
        M[:, h, ...] = np.fft.fftn(micrf, axes=[1, 2])

    f.close()

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
