import functions as rr
import numpy as np
import time
import h5py


def correlate(el, ns, set_id, step, wrt_file):

    st = time.time()

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    M = f.get('M')[...]

    FF = f.create_dataset("FF",
                          (ns, el, el, el),
                          dtype='complex128')

    ff = f.create_dataset("ff",
                          (ns, el, el, el),
                          dtype='float64')

    S = el**3

    mag = np.abs(M)
    ang = np.arctan2(M.imag, M.real)
    exp1 = np.exp(-1j*ang)
    exp2 = np.exp(1j*ang)
    term1 = mag*exp1
    term2 = mag*exp2

    FFtmp = term1*term2/S

    FF[...] = FFtmp

    tmp = np.fft.ifftn(FFtmp, [el, el, el], [1, 2, 3])
    ff[...] = tmp.real

    szgb = np.round(FFtmp.nbytes/(1e9), 3)
    msg = "ff = %s gb" % szgb
    rr.WP(msg, wrt_file)

    f.close()

    msg = "correlations computed: %ss" % np.round(time.time()-st, 5)
    rr.WP(msg, wrt_file)


if __name__ == '__main__':
    el = 21
    ns = 10
    set_id = 'random'
    step = 0
    wrt_file = 'test.txt'

    correlate(el, ns, set_id, step, wrt_file)
