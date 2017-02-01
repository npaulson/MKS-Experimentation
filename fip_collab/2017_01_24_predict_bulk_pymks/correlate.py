import numpy as np
import time


def correlate(M, tail, head):

    st = time.time()

    el = M.shape[2]

    M1 = M[:, tail, ...]
    mag1 = np.abs(M1)
    ang1 = np.arctan2(M1.imag, M1.real)
    exp1 = np.exp(-1j*ang1)
    term1 = mag1*exp1
    del M1, mag1, ang1, exp1

    M2 = M[:, head, ...]
    mag2 = np.abs(M2)
    ang2 = np.arctan2(M2.imag, M2.real)
    exp2 = np.exp(1j*ang2)
    term2 = mag2*exp2
    del M2, mag2, ang2, exp2

    FFtmp = term1*term2/(el**2)
    del term1, term2

    ff = np.fft.ifftn(FFtmp, [el, el], [1, 2]).real

    timeE = np.round(time.time()-st, 5)
    print "correlation computed: %ss" % timeE

    return ff


if __name__ == '__main__':
    ns = 10
    set_id = 'random'

    correlate(ns, set_id)
