# -*- coding: utf-8 -*-
import functions as rr
import numpy as np
from constants import const
import euler_func as ef
import time
import sys
import h5py


def rotate(set_id1, set_id2, newdir):

    st = time.time()

    C = const()

    """load the microstructure"""
    f = h5py.File('euler_%s.hdf5' % set_id1, 'r')
    euler = f.get('euler')[...]
    f.close()
    euler = euler.reshape([C['el'], C['el'], C['el'], 4])

    """rotate the microstructure"""
    euler_r = np.zeros(euler.shape)
    for ii in xrange(C['el']):
        euler_r[:, ii, :, :] = np.rot90(euler[:, ii, :, :], k=3)
    del euler

    """transform euler angles"""
    ang = np.pi/2
    rmat = np.array([[np.cos(ang), 0, -np.sin(ang)],
                     [0, 1, 0],
                     [np.sin(ang), 0, np.cos(ang)]])
    g = ef.bunge2g(euler_r[..., 0], euler_r[..., 1], euler_r[..., 2])
    g_ = np.einsum('ij,...jk', rmat, g)
    del g, rmat
    phi1, Phi, phi2 = ef.g2bunge(g_)
    del g_
    euler_rr = np.zeros(euler_r.shape)
    euler_rr[..., 0] = phi1
    euler_rr[..., 1] = Phi
    euler_rr[..., 2] = phi2
    euler_rr[..., 3] = euler_r[..., 3]
    del phi1, Phi, phi2

    lt0 = euler_rr < 0
    euler_rr += lt0*2*np.pi
    del lt0

    """save the rotated microstructure"""
    euler_rr = euler_rr.reshape([C['el']**3, 4])
    f = h5py.File('euler_%s.hdf5' % set_id2, 'w')
    f.create_dataset('euler', data=euler_rr)
    f.close()

    msg = 'rotation performed for %s: %s seconds' \
          % (set_id2, np.round(time.time()-st))
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    tnum = np.int16(sys.argv[1])
    C = const()
    set_id1 = C['set_id'][tnum+6]
    set_id2 = C['set_id'][tnum+12]
    newdir = C['dir_micr']
    rotate(set_id1, set_id2, newdir)

    f_flag = open("flag%s" % str(tnum).zfill(5), 'w')
    f_flag.close()
