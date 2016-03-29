import functions as rr
import numpy as np
import time
import h5py


def correlate(el, ns, H, set_id, step, wrt_file):

    st = time.time()

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    M = f.get('M')[...]

    FF = f.create_dataset("FF",
                          (ns, H, H, el, el, el),
                          dtype='complex128')

    ff = f.create_dataset("ff",
                          (ns, H, H, el, el, el),
                          dtype='float64')

    # ff = f.create_dataset("ff",
    #                       (ns, H, H, el, el, el),
    #                       dtype='complex128')

    S = el**3

    cmax = H*H
    cmat = np.unravel_index(np.arange(cmax), [H, H])
    cmat = np.array(cmat).T

    for c in xrange(cmax):

        ii, jj = cmat[c, :]
        if np.mod(c, 20) == 0:
            print str([ii, jj])

        M1 = M[:, ii, ...]
        mag1 = np.abs(M1)
        ang1 = np.arctan2(M1.imag, M1.real)
        exp1 = np.exp(-1j*ang1)
        term1 = mag1*exp1
        del M1, mag1, ang1, exp1

        M2 = M[:, jj, ...]
        mag2 = np.abs(M2)
        ang2 = np.arctan2(M2.imag, M2.real)
        exp2 = np.exp(1j*ang2)
        term2 = mag2*exp2
        del M2, mag2, ang2, exp2

        FFtmp = term1*term2/S
        del term1, term2

        FF[:, ii, jj, ...] = FFtmp

        tmp = np.fft.ifftn(FFtmp, [el, el, el], [1, 2, 3])
        ff[:, ii, jj, ...] = tmp.real

        if c == 0:
            szgb = np.round(H*H*FFtmp.nbytes/(1e9), 3)
            msg = "ff = %s gb" % szgb
            rr.WP(msg, wrt_file)

    f.close()

    msg = "correlations computed: %ss" % np.round(time.time()-st, 5)
    rr.WP(msg, wrt_file)


if __name__ == '__main__':
    el = 21
    ns = 10
    H = 15
    set_id = 'random'
    step = 0
    wrt_file = 'test.txt'

    correlate(el, ns, H, set_id, step, wrt_file)
