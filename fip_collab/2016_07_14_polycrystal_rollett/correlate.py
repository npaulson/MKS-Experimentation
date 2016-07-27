import functions as rr
import numpy as np
import gsh_cub_tri_L0_16 as gsh_c
import gsh_hex_tri_L0_16 as gsh_h
from constants import const
import time
import h5py
import sys


def get_M(set_id):

    start = time.time()

    C = const()

    """get the euler angle files"""
    f = h5py.File("euler_L%s.hdf5" % C['H'], 'a')
    euler = f.get('euler_%s' % set_id)[...]
    f.close()

    mf = np.zeros([C['H'], C['el']**3], dtype='float64')

    indxvec_c = gsh_c.gsh_basis_info()
    indxvec_h = gsh_c.gsh_basis_info()

    """calculate the microstructure coefficients for the cubic cells"""
    vec_c = euler[:, 3] == 1
    euler_c = euler[vec_c, :3]

    c = 0
    for h in xrange(C['H_cub']):
        tmp = gsh_c.gsh_eval(euler_c, [h])
        tmp = np.squeeze(tmp)
        if indxvec_c[h, 1] < 0:
            mf[c, vec_c] = tmp.imag/(2.*indxvec_c[h, 0]+1.)
        else:
            mf[c, vec_c] = tmp.real/(2.*indxvec_c[h, 0]+1.)
        c += 1

    del vec_c, euler_c

    """calculate the microstructure coefficients for the hexagonal cells"""
    vec_h = euler[:, 3] == 2
    euler_h = euler[vec_h, :3]

    for h in xrange(C['H_hex']):
        tmp = gsh_h.gsh_eval(euler_h, [h])
        tmp = np.squeeze(tmp)
        if indxvec_h[h, 1] < 0:
            mf[c, vec_h] = tmp.imag/(2.*indxvec_h[h, 0]+1.)
        else:
            mf[c, vec_h] = tmp.real/(2.*indxvec_h[h, 0]+1.)
        c += 1

    del vec_h, euler_h

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "Conversion from Euler angles to GSH coefficients completed:" + \
          " %s seconds" % timeE
    rr.WP(msg, C['wrt_file'])

    mf = mf.reshape([C['H'], C['el'], C['el'], C['el']])

    """mf in frequency space/ preparation for correlations"""
    start = time.time()

    M = np.fft.fftn(mf, axes=[1, 2, 3])
    del mf
    mag = np.abs(M)
    ang = np.arctan2(M.imag, M.real)
    del M
    exp = np.exp(-1j*ang)
    del ang
    preFF = mag*exp
    del mag

    f = h5py.File("spatial_%s.hdf5" % set_id, 'a')
    f.create_dataset('preFF', data=preFF)
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "preparation of mf for correlation %s: %s seconds" % \
          (set_id, timeE)
    rr.WP(msg, C['wrt_file'])


def correlate(set_id):

    st = time.time()

    C = const()

    f = h5py.File("spatial_%s.hdf5" % set_id, 'a')
    preFF = f.get('preFF')[...]

    ff = f.create_dataset("ff",
                          (C['cmax'], C['vmax'], C['vmax'], C['vmax']),
                          dtype='float64')

    S = C['el']**3

    for c in xrange(C['cmax']):

        ii, jj = C['cmat'][c, :]
        if np.mod(c, 20) == 0:
            print str([ii, jj])

        FFtmp = preFF[ii, ...]*preFF[jj, ...]/S

        tmp = np.fft.ifftn(FFtmp, [C['el'], C['el'], C['el']], [0, 1, 2]).real

        rv = np.int64(np.floor(C['vmax']/2.))
        tmp = np.roll(tmp, rv, 0)
        tmp = np.roll(tmp, rv, 1)
        tmp = np.roll(tmp, rv, 2)
        tmp = tmp[:C['vmax'], :C['vmax'], :C['vmax']]
        tmp = np.fft.ifftshift(tmp, [0, 1, 2])

        ff[c, ...] = tmp.real

        # tmp = np.fft.ifftn(FFtmp, [C['el'], C['el'], C['el']], [1, 2, 3])
        # ff[:, ii, jj, ...] = tmp.real

        if c == 0:
            szgb = np.round(C['cmax']*tmp.nbytes/(1e9), 3)
            msg = "ff = %s gb" % szgb
            rr.WP(msg, C['wrt_file'])

    f.close()

    timeE = np.round(time.time()-st, 5)

    msg = "correlations computed for %s: %ss" % (set_id, timeE)
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    tnum = np.int16(sys.argv[1])
    C = const()
    set_id = C['set_id'][tnum]

    get_M(set_id)
    correlate(set_id)

    f_flag = open("flag%s" % str(tnum).zfill(5), 'w')
    f_flag.close()
