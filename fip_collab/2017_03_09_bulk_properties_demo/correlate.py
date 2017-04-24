import numpy as np
import h5py


def correlate(C, ns, set_id):

    f = h5py.File("spatial_L%s.hdf5" % C['H'], 'a')
    M = f.get('M_%s' % set_id)[...]

    ff = f.create_dataset("ff_%s" % set_id,
                          (ns, C['cmax'], C['vmax'], C['vmax'], C['vmax']),
                          dtype='float64')

    S = C['el']**3

    for c in xrange(C['cmax']):

        ii, jj = C['cmat'][c, :]

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

        ff[:, c, ...] = tmp.real

        # tmp = np.fft.ifftn(FFtmp, [C['el'], C['el'], C['el']], [1, 2, 3])
        # ff[:, ii, jj, ...] = tmp.real

    f.close()


if __name__ == '__main__':
    ns = 10
    set_id = 'random'

    correlate(ns, set_id)
