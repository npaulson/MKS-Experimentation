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

    # Plot slices of the response
    plt.figure(num=1, figsize=[12, 2.7])

    plt.subplot(131)
    ax = plt.imshow(euler[sn, 0, slc, :, :],
                    origin='lower',
                    interpolation='none',
                    cmap='jet')
    plt.colorbar(ax)
    plt.title('Slice %s, $\phi_1$' % slc)

    plt.subplot(132)
    ax = plt.imshow(euler[sn, 1, slc, :, :],
                    origin='lower',
                    interpolation='none',
                    cmap='jet')
    plt.colorbar(ax)
    plt.title('$\Phi$')

    plt.subplot(133)
    ax = plt.imshow(euler[sn, 2, slc, :, :],
                    origin='lower',
                    interpolation='none',
                    cmap='jet')
    plt.colorbar(ax)
    plt.title('$\phi_2$')

    # Plot slices of the response
    plt.figure(num=2, figsize=[8, 2.7])

    dmin = np.min([mks_R[sn, slc, :, :], resp[sn, slc, :, :]])
    dmax = np.max([mks_R[sn, slc, :, :], resp[sn, slc, :, :]])

    plt.subplot(121)
    ax = plt.imshow(mks_R[sn, slc, :, :],
                    origin='lower',
                    interpolation='none',
                    cmap='jet',
                    vmin=dmin, vmax=dmax)
    plt.title('MKS $\%s_{%s}$ response, slice %s' % (typ, comp, slc))

    plt.subplot(122)
    ax = plt.imshow(resp[sn, slc, :, :],
                    origin='lower',
                    interpolation='none',
                    cmap='jet',
                    vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('CPFEM $\%s_{%s}$ response, slice %s' % (typ, comp, slc))

    # Plot a histogram representing the frequency of strain levels with
    # separate channels for each phase of each type of response.
    plt.figure(num=3, figsize=[12, 5])

    # find the min and max of both datasets (in full)
    dmin = np.amin([resp, mks_R])
    dmax = np.amax([resp, mks_R])

    fe = np.reshape(resp, ns*(el**3))
    mks = np.reshape(mks_R, ns*(el**3))

    # select the desired number of bins in the histogram
    bn = 40
    weight = np.ones_like(fe)/(el**3)

    # FEM histogram
    n, bins, patches = plt.hist(fe,
                                bins=bn,
                                histtype='step',
                                hold=True,
                                range=(dmin, dmax),
                                weights=weight,
                                color='white')
    bincenters = 0.5*(bins[1:]+bins[:-1])
    fe, = plt.plot(bincenters, n, 'k', linestyle='-', lw=0.5)

    # 1st order terms MKS histogram
    n, bins, patches = plt.hist(mks,
                                bins=bn,
                                histtype='step',
                                hold=True,
                                range=(dmin, dmax),
                                weights=weight,
                                color = 'white')
    mks, = plt.plot(bincenters, n, 'b', linestyle='-', lw=0.5)

    plt.grid(True)

    plt.legend([fe, mks], ["CPFEM response", "MKS predicted response"])

    plt.xlabel("$\%s_{%s}$" % (typ, comp))
    plt.ylabel("Number Fraction")
    plt.title("Frequency comparison of MKS and CPFEM $\%s_{%s}$ strain responses" % (typ, comp))

    plt.show()

if __name__ == '__main__':
    results(21, 400, 'actual', 1, '11', 'epsilon')
