# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 13:52:33 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt


def results(el, ns, set_id, step, comp, typ):

    mks_R = np.load('mksR%s_%s%s_s%s.npy' % (comp, ns, set_id, step))
    resp = np.load('r%s_%s%s_s%s.npy' % (comp, ns, set_id, step))

#    pre_euler = np.load('euler_%s%s_s%s.npy' %(ns,set_id,step))
#
#    euler = np.zeros([ns,3,el,el,el])
#    for h in xrange(3):
#        for sn in range(ns):
#            euler[sn,h,...] = np.swapaxes(np.reshape(np.flipud
#                                    (pre_euler[sn,h,:]), [el,el,el]),1,2)

    tmp = np.load('euler_%s%s_s%s.npy' % (ns, set_id, step))
    euler = tmp.reshape([ns, 3, el, el, el])

    del tmp

    maxindx = np.unravel_index(np.argmax(np.abs(resp - mks_R)), resp.shape)
    maxresp = resp[maxindx]
    maxMKS = mks_R[maxindx]
    maxerr = (np.abs(resp - mks_R)[maxindx]/0.00498753590078)*100

    print 'indices of max error'
    print maxindx
    print 'reference response at max error'
    print maxresp
    print 'MKS response at max error'
    print maxMKS
    print 'maximum error'
    print maxerr

    print euler[maxindx[0], :, maxindx[1], maxindx[2], maxindx[3]]

    # VISUALIZATION OF MKS VS. FEM

    # pick a slice perpendicular to the x-direction
    # sn = maxindx[0]
    # slc = maxindx[1]
    sn = 0
    slc = 0

    plt.close(1)

    # Plot slices of the response
    plt.figure(num=1, figsize=[18, 4])

    plt.subplot(131)
    ax = plt.imshow(euler[sn, 0, slc, :, :], origin='lower',
                    interpolation='none', cmap='jet')
    plt.colorbar(ax)
    plt.title('Microstructure, slice %s' % slc)

#    plt.subplot(132)
#    ax = plt.imshow(mks_R[sn,slc,:,:], origin='lower', interpolation='none',
#        cmap='jet')
#    plt.colorbar(ax)
#    plt.title('MKS $\%s_{%s}$ response, slice %s' %(typ,comp,slc))
#
#    plt.subplot(133)
#    ax = plt.imshow(resp[sn,slc,:,:], origin='lower', interpolation='none',
#        cmap='jet')
#    plt.colorbar(ax)
#    plt.title('CPFEM $\%s_{%s}$ response, slice %s' %(typ,comp,slc))

    dmin = np.min([mks_R[sn, slc, :, :], resp[sn, slc, :, :]])
    dmax = np.max([mks_R[sn, slc, :, :], resp[sn, slc, :, :]])

    plt.subplot(132)
    ax = plt.imshow(mks_R[sn, slc, :, :], origin='lower', interpolation='none',
                    cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('MKS $\%s_{%s}$ response, slice %s' % (typ, comp, slc))

    plt.subplot(133)
    ax = plt.imshow(resp[sn, slc, :, :], origin='lower', interpolation='none',
                    cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('CPFEM $\%s_{%s}$ response, slice %s' % (typ, comp, slc))

    plt.show()

if __name__ == '__main__':
    results(21, 100, 'val', 1, '11', 'epsilon')
