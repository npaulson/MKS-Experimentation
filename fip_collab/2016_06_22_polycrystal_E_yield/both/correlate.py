import functions as rr
import numpy as np
from constants import const
import time
import h5py


def correlate(ns, set_id):

    st = time.time()

    C = const()

    f = h5py.File("spatial_L%s.hdf5" % C['H'], 'a')
    M = f.get('M_%s' % set_id)[...]

    ff = f.create_dataset("ff_%s" % set_id,
                          (ns, C['H'], C['H'], C['vmax'], C['vmax'], C['vmax']),
                          dtype='float64')

    S = C['el']**3

    cmax = C['H']*C['H']
    cmat = np.unravel_index(np.arange(cmax), [C['H'], C['H']])
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

        tmp = np.fft.ifftn(FFtmp, [C['el'], C['el'], C['el']], [1, 2, 3]).real

        rv = np.int64(np.floor(C['vmax']/2.))
        tmp = np.roll(tmp, rv, 1)
        tmp = np.roll(tmp, rv, 2)
        tmp = np.roll(tmp, rv, 3)
        tmp = tmp[:, :C['vmax'], :C['vmax'], :C['vmax']]
        tmp = np.fft.ifftshift(tmp, [1, 2, 3])

        ff[:, ii, jj, ...] = tmp.real

        # tmp = np.fft.ifftn(FFtmp, [C['el'], C['el'], C['el']], [1, 2, 3])
        # ff[:, ii, jj, ...] = tmp.real

        if c == 0:
            szgb = np.round(C['H']*C['H']*FFtmp.nbytes/(1e9), 3)
            msg = "ff = %s gb" % szgb
            rr.WP(msg, C['wrt_file'])

    f.close()

    timeE = np.round(time.time()-st, 5)

    msg = "correlations computed for %s: %ss" % (set_id, timeE)
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    ns = 10
    set_id = 'random'

    correlate(ns, set_id)
