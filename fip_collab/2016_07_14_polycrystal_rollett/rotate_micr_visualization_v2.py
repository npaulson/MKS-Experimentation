# -*- coding: utf-8 -*-
import functions as rr
import numpy as np
from constants import const
import matplotlib.pyplot as plt
import euler_func as ef
import time
import os
import sys


def read_euler(set_id, newdir):

    st = time.time()

    C = const()
    # nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    """read the file"""
    """file format: phi1, phi, phi2, x, y, z, grain_id, phase_id"""
    # tmp = np.loadtxt('%s.txt' % set_id)
    f = open('%s.txt' % set_id, 'r')
    linelist = f.readlines()

    """in euler the first 3 columns are for euler angles,
    the last is for the phase id"""
    """phase id 1 is for beta phase, phase id 2 is for alpha phase"""
    euler = np.zeros([C['el'], C['el'], C['el'], 4])
    spatial = np.zeros([C['el'], C['el'], C['el'], 3])

    for ii in xrange(C['el']**3):
        if np.mod(ii, 1e6) == 0:
            print ii

        tmp = np.float32(np.array(linelist[ii].split()))

        i0 = tmp[3]-1
        i1 = tmp[4]-1
        i2 = tmp[5]-1
        euler[i0, i1, i2, :3] = tmp[:3]*(np.pi/180.)
        euler[i0, i1, i2, 3] = tmp[7]
        spatial[i0, i1, i2, :] = tmp[3:6]

        # i0 = tmp[ii, 3]-1
        # i1 = tmp[ii, 4]-1
        # i2 = tmp[ii, 5]-1
        # euler[i0, i1, i2, :3] = tmp[ii, :3]*(np.pi/180.)
        # euler[i0, i1, i2, 3] = tmp[ii, 7]
        # spatial[i0, i1, i2, :] = tmp[ii, 3:6]

    # euler[:, :3] = tmp[:, :3]*(np.pi/180.)
    # euler[:, 3] = tmp[:, 7]
    # spatial = tmp[:, 3:6]

    f.close()

    print "euler: %s Gb" % str(np.round(euler.nbytes/1e9, 3))

    print spatial[1, 0, 0, :]
    print spatial[0, 1, 0, :]
    print spatial[0, 0, 1, :]

    del tmp

    os.chdir('..')

    msg = 'euler angles read from file for %s: %s seconds' \
          % (set_id, np.round(time.time()-st))
    rr.WP(msg, C['wrt_file'])

    """rotate the microstructure"""
    st = time.time()

    euler_r = np.zeros(euler.shape)
    for ii in xrange(C['el']):
        euler_r[:, ii, :, :] = np.rot90(euler[:, ii, :, :], k=3)

    msg = 'rotation performed for %s: %s seconds' \
          % (set_id, np.round(time.time()-st))

    """rotate euler angles"""
    ang = np.pi/2
    rmat = np.array([[np.cos(ang), 0, -np.sin(ang)],
                     [0, 1, 0],
                     [np.sin(ang), 0, np.cos(ang)]])
    print rmat
    g = ef.bunge2g(euler_r[..., 0], euler_r[..., 1], euler_r[..., 2])
    g_ = np.einsum('ij,...jk', rmat, g)
    del g
    phi1, Phi, phi2 = ef.g2bunge(g_)
    del g_
    euler_rr = np.zeros(euler_r.shape)
    euler_rr[..., 0] = phi1
    euler_rr[..., 1] = Phi
    euler_rr[..., 2] = phi2
    del phi1, Phi, phi2

    lt0 = euler_rr < 0
    euler_rr += lt0*2*np.pi

    """plot the original and rotated microstructures"""
    plt.figure(num=1, figsize=[3, 3])
    ax = plt.imshow(spatial[:, 0, :, 0].T, origin='lower',
                    interpolation='none', cmap='magma')
    plt.colorbar(ax)
    plt.title('x')

    plt.figure(num=2, figsize=[3, 3])
    ax = plt.imshow(spatial[:, 0, :, 1].T, origin='lower',
                    interpolation='none', cmap='magma')
    plt.colorbar(ax)
    plt.title('y')

    plt.figure(num=3, figsize=[3, 3])
    ax = plt.imshow(spatial[:, 0, :, 2].T, origin='lower',
                    interpolation='none', cmap='magma')
    plt.colorbar(ax)
    plt.title('z')

    plt.figure(num=4, figsize=[3, 3])
    ax = plt.imshow(euler[:, 0, :, 0].T, origin='lower',
                    interpolation='none', cmap='magma')
    plt.colorbar(ax)
    plt.title('phi1 field')

    plt.figure(num=5, figsize=[3, 3])
    ax = plt.imshow(euler_r[:, 0, :, 0].T, origin='lower',
                    interpolation='none', cmap='magma')
    plt.colorbar(ax)
    plt.title('rotated micr (phi1) field')

    plt.figure(num=6, figsize=[3, 3])
    ax = plt.imshow(euler_rr[:, 0, :, 0].T, origin='lower',
                    interpolation='none', cmap='magma')
    plt.colorbar(ax)
    plt.title('rotated micr and phi1 field')

    # plt.figure(num=7, figsize=[3, 3])
    # ax = plt.imshow(euler[:, 0, :, 2],
    #                 interpolation='none', cmap='magma')
    # plt.colorbar(ax)
    # plt.title('phi2 field')

    # plt.figure(num=8, figsize=[3, 3])
    # ax = plt.imshow(euler_r[:, 0, :, 2],
    #                 interpolation='none', cmap='magma')
    # plt.colorbar(ax)
    # plt.title('rotated micr (phi2) field')

    # plt.figure(num=9, figsize=[3, 3])
    # ax = plt.imshow(euler_rr[:, 0, :, 2],
    #                 interpolation='none', cmap='magma')
    # plt.colorbar(ax)
    # plt.title('rotated micr and phi2 field')

    plt.show()


if __name__ == '__main__':
    set_id = sys.argv[1]
    newdir = sys.argv[2]
    read_euler(set_id, newdir)
