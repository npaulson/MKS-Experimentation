import functions as rr
import numpy as np
import time
import h5py


def correlate(el, ns, H, set_id, wrt_file):

    st = time.time()

    f = h5py.File("spatial_stats.hdf5", 'a')
    M = f.get('M_%s' % set_id)[...]

    FF = f.create_dataset('FF_%s' % set_id,
                          (ns, H-1, el, el),
                          dtype='complex128')

    ff = f.create_dataset('ff_%s' % set_id,
                          (ns, H-1, el, el),
                          dtype='float64')

    S = el**2

    cmax = H-1

    for c in xrange(cmax):

        if np.mod(c, 10) == 0 and c > 0:
            print "correlation number %s computed" % c

        M1 = M[:, 0, ...]
        mag1 = np.abs(M1)
        ang1 = np.arctan2(M1.imag, M1.real)
        exp1 = np.exp(-1j*ang1)
        term1 = mag1*exp1
        del M1, mag1, ang1, exp1

        M2 = M[:, c, ...]
        mag2 = np.abs(M2)
        ang2 = np.arctan2(M2.imag, M2.real)
        exp2 = np.exp(1j*ang2)
        term2 = mag2*exp2
        del M2, mag2, ang2, exp2

        FFtmp = term1*term2/S
        del term1, term2

        FF[:, c, ...] = FFtmp

        tmp = np.fft.ifftn(FFtmp, [el, el], [1, 2])
        ff[:, c, ...] = tmp.real

        if c == 0:
            szgb = np.round((H-1)*FFtmp.nbytes/(1e9), 3)
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
