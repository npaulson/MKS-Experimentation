# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 13:52:33 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt


def results(el, ns, set_id, step, comp, typ):

    mks_R = np.load('mksR%s_%s%s_s%s.npy' % (comp, ns, set_id, step))
    tmp = np.load('euler_%s%s_s%s.npy' % (ns, set_id, step))
    euler = tmp.reshape([ns, 3, el, el, el])

    del tmp

    # VISUALIZATION OF MKS RESULTS

    # pick a slice perpendicular to the x-direction
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
    plt.figure(num=2, figsize=[4, 2.7])

    ax = plt.imshow(mks_R[sn, slc, :, :],
                    origin='lower',
                    interpolation='none',
                    cmap='jet')
    plt.title('MKS $\%s_{%s}$ response, slice %s' % (typ, comp, slc))
    plt.colorbar(ax)

    # Plot a histogram representing the frequency of strain levels with
    # separate channels for each phase of each type of response.
    plt.figure(num=3, figsize=[12, 5])

    # find the min and max of both datasets (in full)
    dmin = np.amin(mks_R)
    dmax = np.amax(mks_R)

    mks = np.reshape(mks_R, ns*(el**3))

    # select the desired number of bins in the histogram
    bn = 200
    weight = np.ones_like(mks)/(el**3)

    # 1st order terms MKS histogram
    n, bins, patches = plt.hist(mks,
                                bins=bn,
                                histtype='step',
                                hold=True,
                                range=(dmin, dmax),
                                weights=weight,
                                color = 'white')
    bincenters = 0.5*(bins[1:]+bins[:-1])
    mks, = plt.plot(bincenters, n, 'b', linestyle='-', lw=0.5)

    plt.grid(True)
    plt.xlabel("$\%s_{%s}$" % (typ, comp))
    plt.ylabel("Number Fraction")
    plt.title("Histogram of $\%s_{%s}$ in all samples" % (typ, comp))

    plt.show()

if __name__ == '__main__':
    results(21, 400, 'val_actual', 1, '11', 'epsilon')
