# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 13:52:33 2014

@author: nhpnp3
"""

import numpy as np
import tables as tb
import matplotlib.pyplot as plt


def results(el, ns, set_id, step, comp, typ):

    # open HDF5 file
    base = tb.open_file("ref_%s%s_s%s.h5" % (ns, set_id, step),
                        mode="r")

    euler = base.root.msf.euler[...].reshape(ns, 3, el, el, el)
    response = base.get_node('/', 'r%s' % comp)
    r_fem = response.r_fem[...]
    r_mks = response.r_mks[...]

    # close HDF5 file
    base.close()

    r_app = 0.007474

    maxindx = np.unravel_index(np.argmax(np.abs(r_fem - r_mks)), r_fem.shape)
    maxr_fem = r_fem[maxindx]
    maxMKS = r_mks[maxindx]
    maxerr = (np.abs(r_fem - r_mks)[maxindx]/r_app)*100

    print 'indices of max error'
    print maxindx
    print 'reference response at max error'
    print maxr_fem
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

    plt.close(2)

    # Plot slices of the response
    plt.figure(num=2, figsize=[8, 2.7])

    dmin = np.min([r_mks[sn, slc, :, :], r_fem[sn, slc, :, :]])
    dmax = np.max([r_mks[sn, slc, :, :], r_fem[sn, slc, :, :]])

    plt.subplot(121)
    ax = plt.imshow(r_mks[sn, slc, :, :],
                    origin='lower',
                    interpolation='none',
                    cmap='jet',
                    vmin=dmin, vmax=dmax)
    plt.title('MKS $\%s_{%s}$ response, slice %s' % (typ, comp, slc))

    plt.subplot(122)
    ax = plt.imshow(r_fem[sn, slc, :, :],
                    origin='lower',
                    interpolation='none',
                    cmap='jet',
                    vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('CPFEM $\%s_{%s}$ response, slice %s' % (typ, comp, slc))

    # VIOLIN PLOT FOR STRAIN BINS

    r_fem_L = r_fem.reshape(ns*el**3)
    r_mks_L = r_mks.reshape(ns*el**3)

    error = ((r_fem_L - r_mks_L)/0.00814)*100

    sort_list = np.argsort(r_fem_L)

    e_sort = r_fem_L[sort_list[np.round(0.99*len(error)):]]

    err_sort = error[sort_list[np.round(0.99*len(error)):]]

    # select the desired number of bins in the histogram
    bn = 10

    # number of error values per bin in the violin plot
    num_per_bin = np.floor(len(e_sort)/bn)

    error_in_bin_list = []
    bin_labels = []

    for ii in xrange(bn):

        if ii != bn-1:
            error_in_bin = err_sort[ii*num_per_bin:(ii+1)*num_per_bin-1]
            r_in_bin = e_sort[ii*num_per_bin:(ii+1)*num_per_bin-1]
        else:
            error_in_bin = err_sort[ii*num_per_bin:]
            r_in_bin = e_sort[ii*num_per_bin:]

        print len(r_in_bin)

        error_in_bin_list.append(error_in_bin)

        label_cur = str(np.round(100*r_in_bin[0], 4)) + '% - ' + \
            str(np.round(100*r_in_bin[-1], 4)) + '%'
        bin_labels.append(label_cur)

    plt.close(3)

    plt.figure(num=3, figsize=[12, 7])

    ax = plt.subplot(111)

    x = np.arange(1, bn + 1)

    ax.violinplot(dataset=error_in_bin_list, showextrema=False,
                  showmedians=False, showmeans=False)

    ax.set_xticks(x)
    ax.set_xticklabels(bin_labels, rotation='vertical')

    plt.xlabel("bin centers, $\%s_{%s}$" % (typ, comp))
    plt.ylabel("% error")
    plt.title("Error Histogram, $\%s_{%s}$" % (typ, comp))
    plt.grid(True)
    plt.tight_layout(pad=0.1)
    plt.ylim([1.25*np.min(err_sort), 1.25*np.max(err_sort)])

    # MAX ERROR DISTRIBUTIONS

    plt.close(4)

    plt.figure(num=4, figsize=[10, 6])

    # find the min and max of both datasets (in full)

    r_fem_max = np.max(r_fem.reshape(ns, el**3), 1)*100
    r_mks_max = np.max(r_mks.reshape(ns, el**3), 1)*100

    dmin = np.amin([r_fem_max, r_mks_max])
    dmax = np.amax([r_fem_max, r_mks_max])

    # select the desired number of bins in the histogram
    bn = 10

    # FEM histogram
    n, bins, patches = plt.hist(r_fem_max, bins=bn, histtype='step', hold=True,
                                range=(dmin, dmax), color='white')
    bincenters = 0.5*(bins[1:]+bins[:-1])
    fep, = plt.plot(bincenters, n, 'b', linestyle='-', lw=1.0)

    # MKS histogram
    n, bins, patches = plt.hist(r_mks_max, bins=bn, histtype='step', hold=True,
                                range=(dmin, dmax), color='white')
    mksp, = plt.plot(bincenters, n, 'r', linestyle='-', lw=1.0)

    plt.grid(True)

    plt.legend([fep, mksp], ["CPFEM", "MKS"])

    plt.ylim([0, 35])
    plt.xlabel("$\%s_{%s}$ %%" % (typ, comp))
    plt.ylabel("Frequency")
    plt.title("Maximum $\%s_{%s}$ per MVE, FE vs. MKS,"
              % (typ, comp))

    plt.show()

if __name__ == '__main__':
    results(21, 100, 'val', 1, '11', 'epsilon')
